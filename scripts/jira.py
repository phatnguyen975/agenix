"""Run a scoped Jira operation against the configured project.

Usage:
    python "<script-path>" --project-root "<absolute-project-root>" --credentials-file "<project-relative-credentials-path>" <operation> [operation-arguments]

Use the configured private credential file path and select the applicable
operation. Resolve placeholders before invoking. Run with --help for
operations, or <operation> --help for its arguments.
"""

import json

from helpers.core import (
    Invalid,
    Repository,
    Unavailable,
    contained,
    emit,
    parser,
    read_json,
)
from helpers.jira_client import (
    CREDENTIALS,
    Jira,
    credential_header,
    exposed_issue,
    validate_create,
)
from helpers.records import CONFIG, object_record


class PendingCreate:
    """Keep an unresolved creation from being resubmitted after a search miss."""

    def __init__(self, repo, item):
        relative = f".agenix/issues/{item}.jira-pending.json"
        self.path = contained(repo.root, relative, private=True)
        if self.path != repo.root / relative or repo.git("ls-files", "--", relative):
            raise Invalid("Jira pending receipt must be a private local path")
        repo.git("check-ignore", "-q", "--", relative)

    def key(self):
        if self.path.is_file():
            info = read_json(self.path)
            if not isinstance(info, dict) or info.keys() - {"key"}:
                raise Unavailable("Jira pending receipt cannot be read")
            return info.get("key")
        return None

    def begin(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self.path.open("x", encoding="utf-8") as stream:
                stream.write("{}")
        except FileExistsError:
            raise Unavailable(
                "Prior Jira create remains unresolved; reconcile before repeating the write"
            ) from None

    def record(self, key):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({"key": key}), encoding="utf-8")

    def clear(self):
        self.path.unlink(missing_ok=True)


def operate(args):
    repo = Repository(args.project_root)
    root = repo.root
    config = object_record(read_json(contained(root, CONFIG)), "config")
    if config.get("tracker") != "jira" or not isinstance(config.get("jira"), dict):
        raise Invalid("Project is not configured for Jira")
    if args.credentials_file != CREDENTIALS or repo.git("ls-files", "--", CREDENTIALS):
        raise Invalid("The declared private Jira credentials file must be untracked")
    repo.git("check-ignore", "-q", "--", CREDENTIALS)
    client = Jira(
        config["jira"],
        credential_header(root, args.credentials_file),
        timeout=args.timeout,
    )
    payload = {}
    if input_path := getattr(args, "input", None):
        path = contained(root, input_path, private=True)
        parts = tuple(part.casefold() for part in path.relative_to(root).parts)
        if (
            any(part in {".git", "credentials"} for part in parts)
            or not parts
            or path.suffix != ".json"
        ):
            raise Invalid("Jira input must be a non-credential JSON file")
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise Invalid("Jira operation input must be a JSON object")
    try:
        return dispatch(args, client, payload, repo)
    except (KeyError, TypeError, AttributeError) as exc:
        raise Unavailable(
            "Jira settings or response lack required fields; reconcile before repeating a write"
        ) from exc


def dispatch(args, client, payload, repo):
    if args.operation == "issue":
        return exposed_issue(client.issue(args.key))
    if args.operation == "children":
        return {"issues": client.children(args.key)}
    if args.operation == "transitions":
        return {"transitions": client.transitions(args.key)}
    if args.operation == "link-types":
        return client.request("GET", "issueLinkType")
    if args.operation == "project-statuses":
        return client.request(
            "GET", f"project/{client.project}/statuses", list_key="values"
        )
    if args.operation == "discover":
        return {"values": client.discover(args.issue_type)}
    if args.operation in {"create", "reconcile"}:
        validate_create(payload)
        pending = PendingCreate(repo, payload["item"])
        if args.operation == "create":
            return client.create(payload, pending)
        issue = client.reconcile(payload, known_key=pending.key())
        if not issue:
            return {
                "result": "unresolved",
                "detail": "Search miss does not establish absence",
                "exit-code": 3,
            }
        pending.record(issue["key"])
        return {"result": "existing", "issue": exposed_issue(issue)}
    if args.operation == "comment":
        return client.comment(args.key, payload)
    if args.operation == "comments":
        client.issue(args.key)
        return {
            "comments": list(
                client.offset_pages(f"issue/{args.key}/comment", "comments")
            )
        }
    if args.operation == "dependency":
        return client.dependency(args.key, args.prerequisite)
    if args.operation == "status":
        return client.status(args.key, args.status, payload, args.transition_id)
    raise Invalid("Unknown Jira operation")


def main():
    cli = parser(__doc__)
    cli.add_argument(
        "--credentials-file",
        required=True,
        help="Private project-relative credential path",
    )
    cli.add_argument("--timeout", type=int, default=15)
    operations = cli.add_subparsers(dest="operation", required=True)
    operations.add_parser("discover").add_argument("--issue-type")
    operations.add_parser("link-types")
    operations.add_parser("project-statuses")
    for name in ("create", "reconcile"):
        operations.add_parser(name).add_argument("--input", required=True)
    for name in (
        "issue",
        "children",
        "transitions",
        "comments",
        "comment",
        "dependency",
        "status",
    ):
        operation = operations.add_parser(name)
        operation.add_argument("--key", required=True)
        if name == "comment":
            operation.add_argument("--input", required=True)
        if name == "dependency":
            operation.add_argument("--prerequisite", required=True)
        if name == "status":
            operation.add_argument("--status", required=True)
            operation.add_argument("--input")
            operation.add_argument("--transition-id")
    return emit(operate, cli.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
