"""Candidate binding and read-only verification of local completion evidence."""

import re
from datetime import datetime
from functools import cache

from .core import Invalid, Unavailable, contained, run, strict_json
from .records import indexed
from .schema import equal

MUTABLE_FIELDS = {"status", "checkpoints", "checkpoint-refs", "approval-ref"}


class CheckFailure(Invalid):
    def __init__(self, names):
        self.names = set(names)
        super().__init__("Required GitHub checks failed: " + ", ".join(sorted(names)))


class AcceptanceFailure(Invalid):
    def __init__(self, conditions):
        self.conditions = conditions
        super().__init__(
            "Recorded acceptance failures: " + ", ".join(sorted(conditions))
        )


def definition(record):
    return {
        key: value
        for key, value in record.items()
        if key not in MUTABLE_FIELDS
        and key not in {"tasks", "tickets", "schema-version", "kind"}
    }


def delivery_definition(record):
    frozen = definition(record)
    if "tasks" in record:
        frozen["tasks"] = [definition(task) for task in record["tasks"]]
    if "tickets" in record:
        frozen["tickets"] = record["tickets"]
    return frozen


def same_candidate(repo, earlier, current, path):
    """Compare candidate trees while ignoring only record metadata for the selected owner."""
    if earlier == current:
        return True
    paths = repo.git(
        "diff-tree",
        "-r",
        "--no-renames",
        "--name-only",
        "-z",
        repo.oid(earlier, "tree"),
        repo.oid(current, "tree"),
    )
    if paths != path.encode("utf-8") + b"\0":
        return False
    before = strict_json(repo.snapshot(earlier, path, "tree"))
    after = strict_json(repo.snapshot(current, path, "tree"))
    return equal(delivery_definition(before), delivery_definition(after))


def record_at(repo, tree, path, item):
    data = strict_json(repo.snapshot(tree, path, "tree"))
    if not isinstance(data, dict):
        raise Invalid("Approved record snapshot must be an object")
    if data.get("id") == item:
        return data
    return indexed(data.get("tasks", [])).get(item, {})


def bind_candidate(repo, candidate, commit, *, bookkeeping=()):
    """Bind a direct publication commit, including explicitly approved exact blob changes."""
    before = repo.oid(candidate["tree"], "tree")
    base = repo.oid(candidate["base-commit"], "commit")
    parents = repo.git(
        "rev-list", "--parents", "-n", "1", repo.oid(commit, "commit")
    ).split()
    if parents[1:] != [base.encode()]:
        raise Invalid("Publication commit parent differs from the approved candidate")
    after = repo.tree(commit)
    if before == after and not bookkeeping:
        return
    changed = {
        path.decode("utf-8")
        for path in repo.git(
            "diff-tree", "-r", "--no-renames", "--name-only", "-z", before, after
        ).split(b"\0")
        if path
    }
    expected = {entry["path"]: entry["blob"] for entry in bookkeeping}
    if changed != expected.keys():
        raise Invalid("Publication changed paths outside exact approved bookkeeping")
    for path, blob in expected.items():
        contained(repo.root, path)
        entry = repo.git("ls-tree", "-z", after, "--", f":(literal){path}")
        metadata = entry.split(b"\t", 1)[0].split()
        if (
            metadata[:2] != [b"100644", b"blob"]
            or len(metadata) != 3
            or metadata[2].decode() != repo.oid(blob, "blob")
        ):
            raise Invalid("Publication bookkeeping differs from its approved content")


def ancestor(repo, older, newer):
    repo.oid(older, "commit")
    repo.oid(newer, "commit")
    try:
        repo.git("merge-base", "--is-ancestor", older, newer)
    except Unavailable as exc:
        raise Unavailable("Expected commit ancestry could not be established") from exc


class GitHub:
    def __init__(self, repo, config):
        self.root = repo.root
        self.name = config["github-repo"]
        self.base = config["default-branch"]
        self.pull_request = cache(self.pull_request)
        self.checks = cache(self.checks)

    def query(self, *args):
        return strict_json(run(self.root, "gh", *args))

    def pull_request(self, number, url):
        expected = f"https://github.com/{self.name}/pull/{number}"
        if url.casefold() != expected.casefold():
            raise Invalid("PR reference belongs to another repository or number")
        result = self.query(
            "pr",
            "view",
            str(number),
            "--repo",
            f"github.com/{self.name}",
            "--json",
            "url,state,headRefOid,mergeCommit,baseRefName",
        )
        if (
            not isinstance(result, dict)
            or result.get("url", "").casefold() != expected.casefold()
            or result.get("baseRefName") != self.base
        ):
            raise Invalid("Live PR identity or target branch differs")
        return result

    def checks(self, revision, required):
        if not required:
            return
        prefix = f"repos/{self.name}/commits/{revision}"
        sources = [
            (
                "check-runs?filter=latest&per_page=100",
                "check_runs",
                "name",
                "conclusion",
            ),
            ("statuses?per_page=100", None, "context", "state"),
        ]
        runs = {}
        contexts = {}
        for (endpoint, collection, name, result), target in zip(
            sources, (runs, contexts)
        ):
            pages = self.query(
                "api",
                "--hostname",
                "github.com",
                "--paginate",
                "--slurp",
                f"{prefix}/{endpoint}",
            )
            if not isinstance(pages, list) or not pages:
                raise Unavailable("GitHub check response is unavailable")
            for page in pages:
                entries = (
                    page.get(collection)
                    if collection and isinstance(page, dict)
                    else page
                )
                if not isinstance(entries, list):
                    raise Unavailable("GitHub check response is incomplete")
                for entry in entries:
                    if not isinstance(entry, dict) or name not in entry:
                        raise Unavailable("GitHub check response lacks an identifier")
                    key = entry[name]
                    if key not in required:
                        continue
                    if collection:
                        if entry.get("head_sha") != revision:
                            raise Invalid("GitHub check revision mismatch")
                        target.setdefault(key, []).append(entry.get(result))
                    else:  # The commit-status endpoint returns newest statuses first.
                        target.setdefault(key, [entry.get(result)])
        failures = []
        for name in required:
            values = runs.get(name, []) + contexts.get(name, [])
            if not values or any(value in (None, "pending") for value in values):
                raise Unavailable(f"Required GitHub check pending or missing: {name}")
            if len(values) != 1 or values[0] in {"skipped", "neutral"}:
                raise Invalid(f"Required GitHub check is ambiguous or skipped: {name}")
            if values[0] != "success":
                failures.append(name)
        if failures:
            raise CheckFailure(failures)

    def published_head(self, link, item):
        match = re.fullmatch(
            rf"https://github\.com/{re.escape(self.name)}/pull/([1-9][0-9]*)"
            r"#issuecomment-([1-9][0-9]*)",
            link,
            re.IGNORECASE,
        )
        if not match:
            raise Unavailable("Expected a pinned GitHub PR checkpoint comment URL")
        number, comment = map(int, match.groups())
        url = link.partition("#")[0]
        entry = self.query(
            "api",
            "--hostname",
            "github.com",
            f"repos/{self.name}/issues/comments/{comment}",
        )
        issue = f"https://api.github.com/repos/{self.name}/issues/{number}"
        if (
            entry.get("id") != comment
            or entry.get("issue_url", "").casefold() != issue.casefold()
            or entry.get("html_url", "").casefold() != link.casefold()
        ):
            raise Invalid("Live checkpoint comment is on another PR")
        body = entry.get("body", "")
        headers = re.findall(
            r"^## Checkpoint[ \t]*\r?\n(.*?)(?=^#{2,6} |\Z)",
            body,
            re.MULTILINE | re.DOTALL,
        )
        items = (
            re.findall(r"^- \*\*Item:\*\* (\S+)\s*$", headers[0], re.MULTILINE)
            if len(headers) == 1
            else []
        )
        sections = re.findall(
            r"^## Publication[ \t]*\r?\n(.*?)(?=^## |\Z)",
            body,
            re.MULTILINE | re.DOTALL,
        )
        heads = (
            re.findall(
                r"^- \*\*Head Commit:\*\* ([0-9a-f]{40}|[0-9a-f]{64})\s*$",
                sections[0],
                re.MULTILINE,
            )
            if len(sections) == 1
            else []
        )
        if items != [item] or len(heads) != 1:
            raise Invalid("PR comment lacks an unambiguous item and published head")
        return {"pr": {"number": number, "url": url}, "head-commit": heads[0]}

    def test_merge_revision(self, number, revision, head, base):
        prefix = f"repos/{self.name}"
        pr = self.query("api", "--hostname", "github.com", f"{prefix}/pulls/{number}")
        if (
            pr.get("number") != number
            or pr.get("state") != "open"
            or pr.get("merge_commit_sha") != revision
            or pr.get("head", {}).get("sha") != head
            or pr.get("base", {}).get("sha") != base
        ):
            raise Unavailable(
                "GitHub does not confirm the current PR test merge revision"
            )
        commit = self.query(
            "api", "--hostname", "github.com", f"{prefix}/git/commits/{revision}"
        )
        if commit.get("sha") != revision or [
            parent.get("sha") for parent in commit.get("parents", [])
        ] != [base, head]:
            raise Invalid(
                "PR test merge parents differ from the selected baseline and head"
            )
        return revision


def checkpoints(record, store):
    result = list(record.get("checkpoints", []))
    refs = record.get("checkpoint-refs", []) + (
        [record["approval-ref"]] if "approval-ref" in record else []
    )
    for ref in refs:
        if (
            "checkpoint-id" not in ref
            or "revision" not in ref
            or "://" in ref["target"]
        ):
            continue
        path = ref["target"].partition("#")[0]
        payload = strict_json(store.repo.snapshot(ref["revision"], path))
        for owner in [payload, *payload.get("tasks", [])]:
            result.extend(
                cp
                for cp in owner.get("checkpoints", [])
                if cp["checkpoint-id"] == ref["checkpoint-id"]
            )
    by_id = {}
    for cp in result:
        store.schemas.validate("templates/evidence/checkpoint.schema.json", cp)
        if cp.get("item-id") != record["id"]:
            raise Invalid("Checkpoint belongs to another item")
        previous = by_id.setdefault(cp["checkpoint-id"], cp)
        if not equal(previous, cp):
            raise Invalid("Conflicting snapshots for one checkpoint ID")
    return sorted(
        by_id.values(), key=lambda cp: timestamp(cp["recorded-at"]), reverse=True
    )


def work_waiver(
    record, timeline, *, revision, conditions, work, consumers, action="allow-work"
):
    """Apply only the exact current waiver selected by the calling workflow."""
    for cp in timeline:
        decision = cp.get("decision", {})
        disposition = cp.get("disposition", {})
        if decision.get("kind") != "override" or disposition.get("action") != action:
            continue
        return (
            decision["result"] == "approved"
            and decision["actor"] == "human-in-session"
            and disposition["item-id"] == record["id"]
            and disposition["revision"] == revision
            and set(disposition["waived-conditions"]) == set(conditions)
            and disposition["permitted-work"] == work
            and disposition["consumer-scope"] == consumers
        )
    return False


def check_decision(record, path, timeline, repo, kinds):
    for cp in timeline:
        decision = cp.get("decision", {})
        if decision.get("kind") not in kinds:
            continue
        if decision["result"] != "approved":
            raise Invalid(f"{decision['kind']} did not approve {record['id']}")
        candidate = cp.get("candidate", {})
        if not {"tree", "base-commit"} <= candidate.keys():
            raise Unavailable("No Git candidate on the approval checkpoint")
        repo.oid(candidate["base-commit"], "commit")
        approved = record_at(repo, candidate["tree"], path, record["id"])
        if not equal(definition(approved), definition(record)):
            raise Invalid(f"Approved definition has changed: {record['id']}")
        return candidate
    raise Unavailable(f"Missing approval for {record['id']}")


def same_revision(receipt, revision, tree):
    if "revision" in receipt:
        return receipt["revision"] == revision
    return receipt.get("tree") == tree


def task_passed(
    task,
    timeline,
    store,
    revision,
    commands,
    *,
    github=None,
    tree=None,
    owner_path=None,
):
    tree = tree or store.repo.tree(revision)
    acceptance = set(indexed(task["acceptance"]))
    plan = task["verification"]
    checks = plan["checks"]
    manual_covered = set()
    failures = set()
    if plan["method"] == "manual":
        confirmed = set()
        for cp in timeline:
            decision = cp.get("decision", {})
            if decision.get("kind") != "manual-confirmation":
                continue
            if cp.get("candidate", {}).get("tree") != tree:
                continue
            ids = set(decision.get("acceptance-ids", []))
            if not ids and checks and set(decision.get("check-ids", [])) == set(checks):
                ids = acceptance
            if not ids or ids - acceptance:
                continue
            fresh = ids - confirmed
            if fresh and decision["result"] != "passed":
                failures.add(task["id"] + "/manual")
            confirmed.update(ids)
        if confirmed != acceptance:
            raise Unavailable("Matching manual confirmation is missing")
        manual_covered = confirmed
    receipts = [
        receipt
        for cp in timeline
        for receipt in cp.get("verification", [])
        if receipt.get("item-id") == task["id"]
    ]

    def matches(receipt):
        if same_revision(receipt, revision, tree):
            return True
        if not owner_path:
            return False
        if "revision" in receipt:
            try:
                checked_tree = store.repo.tree(receipt["revision"])
            except Unavailable:
                return False
        else:
            checked_tree = receipt["tree"]
        return same_candidate(store.repo, checked_tree, tree, owner_path)

    covered = manual_covered
    for name in checks:
        matching = [
            receipt
            for receipt in receipts
            if receipt["check-id"] == name and matches(receipt)
        ]
        if not matching:
            raise Unavailable(f"No current receipt for {name}")
        receipt = max(matching, key=lambda value: timestamp(value["at"]))
        if any(
            timestamp(other["at"]) == timestamp(receipt["at"])
            and not equal(other, receipt)
            for other in matching
        ):
            raise Invalid(f"Conflicting check receipts: {name}")
        if receipt["result"] not in {"passed", "failed"}:
            raise Unavailable(f"Task check has no passing result: {name}")
        command = commands.get(name)
        if not command or not command.get("check-level"):
            raise Unavailable(f"Check is absent from the verified environment: {name}")
        if (
            receipt.get("mode") != command["mode"]
            or receipt.get("check-level") != command["check-level"]
        ):
            raise Invalid("Receipt level or mode differs from the approved check")
        ids = set(receipt.get("acceptance-ids", []))
        if ids - acceptance:
            raise Invalid("Receipt refers outside the task acceptance criteria")
        covered.update(ids)
        ref = receipt["evidence-ref"]
        if "://" in ref["target"]:
            if "revision" not in receipt:
                raise Invalid("GitHub Actions evidence requires the tested commit")
            verify_action_receipt(
                github, ref["target"], receipt["revision"], outcome=receipt["result"]
            )
        elif "revision" not in ref:
            raise Invalid("Task evidence must identify its Git snapshot")
        else:
            store.validate_target(ref)
        if receipt["result"] == "failed":
            failures.add(f"{task['id']}/{name}")
    if covered != acceptance:
        raise Unavailable("Passing checks do not establish full task acceptance")
    if failures:
        raise AcceptanceFailure(failures)


def timestamp(value):
    return datetime.fromisoformat(value)


def verify_action_receipt(github, target, revision, *, outcome="passed"):
    if github is None:
        raise Unavailable("External task evidence requires a verified source adapter")
    match = re.fullmatch(
        rf"https://github\.com/{re.escape(github.name)}/actions/runs/([1-9][0-9]*)",
        target,
        re.IGNORECASE,
    )
    if not match:
        raise Unavailable(
            "Task receipt URL is outside the supported GitHub Actions source"
        )
    result = github.query(
        "api",
        "--hostname",
        "github.com",
        f"repos/{github.name}/actions/runs/{match[1]}",
    )
    expected = "success" if outcome == "passed" else "failure"
    if (
        result.get("html_url", "").casefold() != target.casefold()
        or result.get("head_sha") != revision
        or result.get("conclusion") != expected
    ):
        raise Invalid("GitHub Actions receipt does not verify the selected revision")


class Completion:
    def __init__(
        self,
        store,
        config,
        baseline,
        commands,
        checks: dict[str, list[str] | None],
        *,
        policy: dict[str, dict[str, list[str] | None]] | None = None,
        acceptance_context=None,
    ):
        self.store = store
        self.repo = store.repo
        self.baseline = baseline
        self.commands = commands or {}
        self.gh = GitHub(self.repo, config)
        self.required = checks
        self.policy = policy or {}
        self.acceptance_context = acceptance_context
        self.exceptions = {}
        self.merged = cache(self.merged)

    def check_policy(self, item: str) -> dict[str, list[str] | None]:
        return self.policy.get(item, self.required)

    def merged(self, path, item, *, feature=False, allow_repair=True):
        record = self.store.record("feature" if feature else "ticket", path)
        if record["id"] != item or record["status"] != "DONE":
            raise Unavailable(
                f"{item} has no declared completion on the merged baseline"
            )
        timeline = checkpoints(record, self.store)
        kinds = {"feature-acceptance"} if feature else {"review"}
        reviewed = check_decision(record, path, timeline, self.repo, kinds)
        published = next(
            (cp["publication"] for cp in timeline if "pr" in cp.get("publication", {})),
            {},
        )
        if not {"pr", "head-commit"} <= published.keys():
            refs = record.get("checkpoint-refs", [])
            links = [ref["target"] for ref in refs if "#issuecomment-" in ref["target"]]
            if len(links) != 1:
                raise Unavailable(
                    f"Missing unambiguous PR checkpoint and reviewed head for {item}"
                )
            published = self.gh.published_head(links[0], item)
        ref = published["pr"]
        pr = self.gh.pull_request(ref["number"], ref["url"])
        head = published["head-commit"]
        if head != pr.get("headRefOid"):
            raise Invalid("Mapped head differs from the actual PR head")
        merge = (pr.get("mergeCommit") or {}).get("oid")
        if pr.get("state") != "MERGED" or not merge:
            raise Unavailable(f"PR for {item} has not merged")
        if published.get("merge-commit", merge) != merge:
            raise Invalid("Recorded merge SHA differs from the actual PR")
        ancestor(self.repo, merge, self.baseline)
        try:
            head_tree = self.repo.tree(head)
        except Unavailable:
            # A squash can remove the source commit. Require the merged tree to
            # establish the same snapshot before using the PR mapping alone.
            head_tree = self.repo.tree(merge)
        if reviewed["tree"] != head_tree:
            approved = any(
                cp.get("decision", {}).get("kind") == "artifact"
                and cp["decision"]["result"] == "approved"
                and cp.get("candidate", {}).get("tree") == head_tree
                for cp in timeline
            )
            if not approved or not same_candidate(
                self.repo, reviewed["tree"], head_tree, path
            ):
                raise Unavailable(
                    "Published changes differ from the reviewed and approved snapshot"
                )
        merged = strict_json(self.repo.snapshot(merge, path))
        if merged.get("status") != "DONE" or not equal(
            definition(record), definition(merged)
        ):
            raise Invalid("Approved completion did not reach the merged record")
        required = self.check_policy(item)
        head_checks = required["head"]
        merge_checks = required["merge"]
        if head_checks is None or merge_checks is None:
            raise Unavailable(
                "Required final-head and post-merge check sets must be supplied"
            )
        self.gh.checks(head, tuple(head_checks))
        try:
            self.gh.checks(merge, tuple(merge_checks))
        except CheckFailure as exc:
            if (
                feature
                or not allow_repair
                or not self.has_repair(path, ref, merge, timeline, exc.names)
            ):
                raise
        if feature:
            if not record.get("tickets") or not equal(
                record["tickets"], merged.get("tickets")
            ):
                raise Invalid("The merged feature has no matching approved ticket set")
            if len(record["tickets"]) == sum(
                self.store.record("ticket", m["path"])["status"] == "CANCELLED"
                for m in record["tickets"]
            ):
                raise Invalid("All planned tickets were cancelled")
            for mapping in record["tickets"]:
                child = self.store.record("ticket", mapping["path"])
                if child["status"] == "CANCELLED":
                    self.check_cancellation(child)
                else:
                    self.merged(mapping["path"], mapping["id"])
            failures = self.feature_acceptance(record, timeline, reviewed)
        else:
            failures = set()
            tasks = indexed(record.get("tasks", []))
            original = indexed(merged.get("tasks", []))
            if not tasks or tasks.keys() != original.keys():
                raise Invalid("The merged ticket has no matching approved task set")
            required_coverage = {
                key
                for ref in record["references"]
                for key in ref.get("acceptance-ids", [])
            }
            applicable = [
                task for task in tasks.values() if task["status"] != "CANCELLED"
            ]
            task_coverage = {
                key
                for task in applicable
                for criterion in task["acceptance"]
                for key in criterion["covers"]
            }
            if not applicable or task_coverage != required_coverage:
                raise Invalid("Tasks do not cover ticket acceptance")
            for task in tasks.values():
                if task["status"] == "CANCELLED":
                    self.check_cancellation(task)
                    if original[task["id"]]["status"] != "CANCELLED":
                        raise Invalid(
                            "Task cancellation did not reach the merged record"
                        )
                    continue
                if (
                    task["status"] != "DONE"
                    or original[task["id"]]["status"] != "DONE"
                    or not equal(definition(task), definition(original[task["id"]]))
                ):
                    raise Invalid(
                        "Merged task was not completed with its approved definition"
                    )
                chain = checkpoints(task, self.store)
                check_decision(task, path, chain + timeline, self.repo, {"artifact"})
                try:
                    task_passed(
                        task,
                        chain,
                        self.store,
                        head,
                        self.commands,
                        github=self.gh,
                        owner_path=path,
                        tree=head_tree,
                    )
                except AcceptanceFailure as exc:
                    failures.update(exc.conditions)
        if failures:
            context = self.acceptance_context
            if (
                not context
                or context["item"] != item
                or context["conditions"].keys() != failures
                or not work_waiver(
                    record,
                    timeline,
                    revision=head,
                    conditions=list(context["conditions"].values()),
                    work=context["work"],
                    consumers=context["consumers"],
                    action="accept-incomplete",
                )
            ):
                raise Invalid(
                    "Unresolved acceptance failures: " + ", ".join(sorted(failures))
                )
            self.exceptions[item] = sorted(failures)
        return merge

    def check_cancellation(self, record):
        for cp in checkpoints(record, self.store):
            decision = cp.get("decision", {})
            if decision.get("kind") == "cancellation":
                disposition = cp.get("disposition", {})
                if (
                    decision["result"] == "approved"
                    and disposition.get("item-id") == record["id"]
                ):
                    return
                break
        raise Unavailable(
            f"Approved cancellation evidence is missing for {record['id']}"
        )

    def feature_acceptance(self, record, timeline, candidate):
        cp = next(
            cp
            for cp in timeline
            if cp.get("decision", {}).get("kind") == "feature-acceptance"
        )
        plan_base = candidate.get("target-base-commit") or candidate["base-commit"]
        ancestor(self.repo, plan_base, self.baseline)
        receipts = cp.get("verification", [])
        if not receipts:
            raise Unavailable(
                "Whole-feature acceptance is missing verification receipts"
            )
        failures = set()
        for receipt in receipts:
            if (
                receipt.get("item-id") != record["id"]
                or receipt.get("revision") != plan_base
            ):
                raise Invalid(
                    "Feature acceptance receipt does not match the approved merged baseline"
                )
            command = self.commands.get(receipt["check-id"])
            if (
                not command
                or command.get("check-level") != receipt.get("check-level")
                or command["mode"] != receipt.get("mode")
            ):
                raise Invalid(
                    "Feature check receipt differs from the approved environment"
                )
            if receipt["result"] not in {"passed", "failed"}:
                raise Unavailable(
                    "A required feature acceptance check has no final result"
                )
            ref = receipt["evidence-ref"]
            if "://" in ref["target"]:
                verify_action_receipt(
                    self.gh, ref["target"], plan_base, outcome=receipt["result"]
                )
            else:
                if "revision" not in ref:
                    raise Invalid("Feature acceptance evidence must be pinned")
                self.store.validate_target(ref)
            if receipt["result"] == "failed":
                failures.add(f"{record['id']}/{receipt['check-id']}")
        return failures

    def has_repair(self, path, pr, merge, timeline, failed_names):
        recorded = {
            receipt["check-id"]
            for cp in timeline
            for receipt in cp.get("verification", [])
            if receipt["result"] == "failed" and receipt.get("revision") == merge
        }
        if not failed_names <= recorded:
            return False
        paths = {
            ref["target"].partition("#")[0]
            for cp in timeline
            for ref in cp["references"]
            if ref["target"].startswith(path.rpartition("/")[0] + "/")
            and ref["target"].endswith(".agenix.json")
        }
        for repair_path in sorted(paths - {path}):
            repair = self.store.record("ticket", repair_path)
            if repair.get("origin-ref", {}).get("target") not in {path, pr["url"]}:
                continue
            repaired = self.merged(repair_path, repair["id"], allow_repair=False)
            if repaired == merge:
                raise Invalid("Repair must have its own subsequent merge")
            ancestor(self.repo, merge, repaired)
            self.gh.checks(repaired, tuple(sorted(failed_names)))
            return True
        return False
