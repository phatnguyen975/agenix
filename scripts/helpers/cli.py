"""CLI adapters for managed artifact and local tracker checks."""

import re
from functools import partial
from pathlib import Path

from .core import Invalid, Repository, Unavailable, emit, parser, strict_json
from .evidence import (
    Completion,
    ancestor,
    bind_candidate,
    check_decision,
    checkpoints,
    definition,
    record_at,
    task_passed,
    work_waiver,
)
from .records import CATALOG, ENVIRONMENT, Records, feature_path, indexed, ticket_path
from .schema import equal

BUNDLE = Path(__file__).resolve().parents[2]


def schema_paths(values):
    result = {}
    for value in values:
        kind, sep, path = value.partition("=")
        if (
            not sep
            or kind not in {"config", "environment", "catalog"}
            or kind in result
        ):
            raise Invalid(
                "Use --schema KIND=relative/path for one owned schema per kind"
            )
        result[kind] = path
    return result


def prepare(args):
    repository = Repository(args.project_root)
    return Records(repository, BUNDLE, schemas=schema_paths(args.schema))


def override_context(raw, *, accepted=False):
    value = strict_json(raw.encode("utf-8"))
    text_fields = {"work", "consumers"} | ({"item"} if accepted else set())
    if (
        not isinstance(value, dict)
        or value.keys() != text_fields | {"conditions"}
        or not isinstance(value["conditions"], dict)
        or not value["conditions"]
        or not all(
            isinstance(entry, str) and entry
            for entry in [
                *(value[name] for name in text_fields),
                *value["conditions"].values(),
            ]
        )
    ):
        raise Invalid(
            "Override context must identify the precise conditions, work and consumers"
        )
    return value


def ci_policy(raw):
    if not raw:
        return {}
    entries = strict_json(raw.encode("utf-8"))
    if not isinstance(entries, dict):
        raise Invalid("Expected CI check policy keyed by work-item ID")
    for policy in entries.values():
        if (
            not isinstance(policy, dict)
            or policy.keys() != {"head", "merge"}
            or any(
                not isinstance(names, list)
                or any(not isinstance(name, str) or not name for name in names)
                or len(names) != len(set(names))
                for names in policy.values()
            )
        ):
            raise Invalid(
                "Each CI check policy needs distinct head and merge check name arrays"
            )
    return entries


def validate(args):
    store = prepare(args)
    config = store.config()
    commands = None
    if store.exists(ENVIRONMENT) or args.stage in {
        "environment",
        "feature-plan",
        "task-plan",
    }:
        commands = store.environment()
    if store.exists(CATALOG) or args.stage in {"feature", "feature-plan", "task-plan"}:
        features = store.work_items(config["tracker"], commands)
        if args.item:
            feature = features.get(args.item.split("-T")[0])
            if not feature:
                raise Invalid("Selected feature is absent from the catalog")
            if (
                args.stage == "feature-plan"
                and not {"references", "tickets", "delivery-strategy"} <= feature.keys()
            ):
                raise Invalid("Feature plan is incomplete")
            if args.stage == "task-plan":
                if config["tracker"] != "local":
                    raise Unavailable(
                        "Remote task plans are verified through the native tracker"
                    )
                mapping = indexed(feature.get("tickets", [])).get(args.item)
                if not mapping or not store.record("ticket", mapping["path"]).get(
                    "tasks"
                ):
                    raise Invalid("Selected local ticket has no task plan")
        elif args.stage in {"feature-plan", "task-plan"}:
            raise Invalid("Use --item to select the owner of the current plan stage")
    return {"result": "valid", "stage": args.stage, "tracker": config["tracker"]}


def verify(args):
    if args.tree and args.mode == "delivery":
        raise Invalid(
            "Provisional trees are supported only for active build or candidate CI"
        )
    if args.test_merge_revision and not args.pr_number:
        raise Invalid("A test merge revision requires its exact PR number")
    store = prepare(args)
    config = store.config()
    if config["tracker"] != "local":
        raise Invalid("Use the native tracker for remote ticket or task verification")
    repo = store.repo
    baseline = repo.baseline(config)
    commands = store.environment() if store.exists(ENVIRONMENT) else None
    features = store.work_items("local", commands)
    base_store = Records(repo, BUNDLE, revision=baseline, schemas=store.paths)
    if base_store.config() != config:
        raise Unavailable("Working configuration differs from the merged configuration")
    merged_commands = (
        base_store.environment() if base_store.exists(ENVIRONMENT) else None
    )
    complete = Completion(
        base_store,
        config,
        baseline,
        merged_commands,
        {
            "head": args.head_check if not args.no_head_checks else [],
            "merge": args.post_merge_check if not args.no_post_merge_checks else [],
        },
        policy=ci_policy(args.ci_policy),
        acceptance_context=override_context(
            args.accept_incomplete_context, accepted=True
        )
        if args.accept_incomplete_context
        else None,
    )

    item = args.item
    feature_id = item.split("-T")[0]
    if feature_id not in features:
        raise Invalid("Selected feature is absent from the catalog")
    feature = features[feature_id]
    ticket_id = item.split(".")[0]
    level = "feature"
    path = feature_path(feature_id)
    ticket = {}
    record = feature
    if feature_id != item:
        level = "ticket" if ticket_id == item else "task"
        mapping = indexed(feature.get("tickets", [])).get(ticket_id)
        if not mapping:
            raise Invalid("Selected ticket is absent from the feature plan")
        path = mapping["path"]
        ticket = store.record("ticket", path)
        record = (
            ticket if level == "ticket" else indexed(ticket.get("tasks", [])).get(item)
        )
        if record is None:
            raise Invalid("Selected task is absent from the ticket plan")

    blockers: list[dict[str, str]] = []
    result: dict[str, object] = {
        "result": "evaluated",
        "item": item,
        "declared-status": record["status"],
        "baseline": baseline,
        "candidate": "not-requested",
        "completion": "not-established",
        "dependency-ready": True,
        "blockers": blockers,
    }

    def evaluate(label, operation):
        try:
            operation()
            return "verified"
        except (Invalid, Unavailable) as exc:
            state = "failed" if isinstance(exc, Invalid) else "unavailable"
            blockers.append({"area": label, "result": state, "detail": str(exc)})
            return state

    def active_task(task):
        if args.tree:
            tree = repo.oid(args.tree, "tree")
            repo.git("diff-index", "--cached", "--quiet", tree, "--")
        elif args.revision:
            head = repo.git("rev-parse", "HEAD").decode().strip()
            ancestor(repo, args.revision, head)
            tree = repo.tree(args.revision)
        else:
            raise Unavailable(
                "Active task verification requires the selected implementation commit or staged tree"
            )
        actual = record_at(repo, tree, path, task["id"])
        if not equal(definition(task), definition(actual)):
            raise Invalid(
                "Selected implementation commit has a different task definition"
            )
        chain = checkpoints(task, store)
        check_decision(
            task, path, chain + checkpoints(ticket, store), repo, {"artifact"}
        )
        task_passed(
            task,
            chain,
            store,
            args.revision,
            commands or {},
            github=complete.gh,
            tree=tree,
        )

    for dependency in record["depends-on"]:
        if level == "feature":
            operation = partial(
                complete.merged, feature_path(dependency), dependency, feature=True
            )
        elif level == "ticket":
            operation = partial(
                complete.merged, ticket_path(feature_id, dependency), dependency
            )
        elif args.mode in {"active-build", "candidate-ci"}:
            operation = partial(active_task, indexed(ticket["tasks"])[dependency])
        else:
            operation = lambda: complete.merged(path, ticket_id)
        if evaluate(dependency, operation) != "verified":
            result["dependency-ready"] = False
    if args.allow_work_context and not result["dependency-ready"]:
        context = override_context(args.allow_work_context)
        if context["conditions"].keys() != {blocker["area"] for blocker in blockers}:
            raise Invalid(
                "Allow-work context must identify every observed dependency blocker and its exact scope"
            )
        revision = args.revision or baseline
        repo.oid(revision, "commit")
        if work_waiver(
            record,
            checkpoints(record, store),
            revision=revision,
            conditions=list(context["conditions"].values()),
            work=context["work"],
            consumers=context["consumers"],
        ):
            result["work-waiver"] = "verified"
            result["dependency-ready"] = True
            result["waived-blockers"] = blockers.copy()
            blockers.clear()

    if record["status"] == "CANCELLED":
        result["dependency-ready"] = False
        blockers.append(
            {"area": item, "result": "failed", "detail": "Item is cancelled"}
        )

    if args.revision and level != "task":

        def validate_candidate():
            kinds = {"artifact", "review", "feature-acceptance"}
            if args.pr_number:
                kinds = {"feature-acceptance"} if level == "feature" else {"review"}
            candidate = check_decision(
                record, path, checkpoints(record, store), repo, kinds
            )
            bookkeeping = []
            for value in args.approved_blob:
                changed, sep, blob = value.rpartition("=")
                if (
                    not sep
                    or not changed
                    or not blob
                    or changed in {entry["path"] for entry in bookkeeping}
                ):
                    raise Invalid(
                        "Use one --approved-blob PATH=OID per approved bookkeeping file"
                    )
                bookkeeping.append({"path": changed, "blob": blob})
            bind_candidate(repo, candidate, args.revision, bookkeeping=bookkeeping)

        result["candidate"] = evaluate("candidate", validate_candidate)
    elif args.tree and level != "task":
        raise Invalid("A provisional tree is supported only for a selected task")
    elif (
        level == "task"
        and (args.revision or args.tree)
        and args.mode in {"active-build", "candidate-ci"}
    ):
        result["candidate"] = evaluate("candidate", lambda: active_task(record))

    if args.pr_number:
        if args.pr_number < 1 or level == "task" or not args.revision:
            raise Invalid(
                "A PR check requires a positive PR number and exact feature or ticket revision"
            )

        def check_pr():
            url = f"https://github.com/{config['github-repo']}/pull/{args.pr_number}"
            pr = complete.gh.pull_request(args.pr_number, url)
            if pr.get("headRefOid") != args.revision or pr.get("state") not in {
                "OPEN",
                "MERGED",
            }:
                raise Invalid("PR state or head does not match the selected candidate")
            required = complete.check_policy(item)["head"]
            if required is None:
                raise Unavailable("Required head checks must be supplied")
            checked = args.revision
            if args.test_merge_revision:
                if not re.fullmatch(
                    rf"[0-9a-f]{{{repo.oid_length}}}", args.test_merge_revision
                ):
                    raise Invalid("Expected a full PR test merge object ID")
                checked = complete.gh.test_merge_revision(
                    args.pr_number, args.test_merge_revision, args.revision, baseline
                )
            complete.gh.checks(checked, tuple(required))

        result["pr-checks"] = evaluate("pr-checks", check_pr)

    if record["status"] == "DONE":
        if args.mode == "candidate-ci":
            result["completion"] = "pending"
        elif args.mode == "active-build" and level == "task":
            if result["candidate"] == "not-requested":
                result["candidate"] = evaluate("candidate", lambda: active_task(record))
            result["completion"] = (
                "provisional" if result["candidate"] == "verified" else "unavailable"
            )
        else:

            def verify_merged():
                merged = base_store.record(
                    "feature" if level == "feature" else "ticket", path
                )
                if level == "task":
                    merged = indexed(merged.get("tasks", [])).get(item, {})
                if not equal(definition(record), definition(merged)):
                    raise Invalid(
                        "Selected definition differs from the merged work item"
                    )
                complete.merged(path, ticket_id, feature=level == "feature")

            result["completion"] = evaluate("completion", verify_merged)
            completed_id = ticket_id if level == "task" else item
            if (
                result["completion"] == "verified"
                and completed_id in complete.exceptions
            ):
                result["completion"] = "verified-with-exception"

    if complete.exceptions:
        result["acceptance-exceptions"] = complete.exceptions

    if blockers:
        result["exit-code"] = (
            2 if any(blocker["result"] == "failed" for blocker in blockers) else 3
        )
    return result


def main(operation):
    cli = parser(
        "Validate project artifacts"
        if operation == validate
        else "Verify local tracker evidence"
    )
    cli.add_argument(
        "--schema",
        action="append",
        default=[],
        metavar="KIND=PATH",
        help="Override an owned schema path relative to the installed bundle",
    )
    if operation == validate:
        cli.add_argument("--item")
        cli.add_argument(
            "--stage",
            required=True,
            choices=["config", "environment", "feature", "feature-plan", "task-plan"],
        )
    else:
        cli.add_argument("--item", required=True)
        cli.add_argument(
            "--mode",
            choices=["active-build", "candidate-ci", "delivery"],
            default="delivery",
        )
        snapshot = cli.add_mutually_exclusive_group()
        snapshot.add_argument(
            "--revision", help="Exact local implementation or publication commit"
        )
        snapshot.add_argument(
            "--tree", help="Exact staged tree for provisional task verification"
        )
        cli.add_argument(
            "--pr-number",
            type=int,
            help="Exact PR to inspect for the selected candidate",
        )
        cli.add_argument(
            "--test-merge-revision",
            help="GitHub's exact test merge revision for an open PR",
        )
        cli.add_argument(
            "--approved-blob",
            action="append",
            default=[],
            metavar="PATH=OID",
            help="Exact post-approval bookkeeping blob expressly covered by the human gate",
        )
        cli.add_argument(
            "--allow-work-context",
            help="JSON of the exact approved work, consumers and conditions by dependency ID",
        )
        cli.add_argument(
            "--accept-incomplete-context",
            help="JSON of the exact approved item, work, consumers and acceptance conditions",
        )
        cli.add_argument(
            "--ci-policy",
            help="JSON of approved head and merge check names by work-item ID",
        )
        for flag in ("head", "post-merge"):
            group = cli.add_mutually_exclusive_group()
            group.add_argument(f"--{flag}-check", action="append")
            group.add_argument(f"--no-{flag}-checks", action="store_true")
    return emit(operation, cli.parse_args())
