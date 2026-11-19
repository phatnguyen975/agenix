"""Managed records, relationships and artifact references."""

import re
from graphlib import CycleError, TopologicalSorter

from .core import Invalid, Unavailable, contained, https, read_json, strict_json
from .schema import Schemas

FEATURE = r"FEAT-(?=[0-9]*[1-9])[0-9]{3,}"
TICKET = FEATURE + r"-T(?=[0-9]*[1-9])[0-9]{2,}"
TASK = TICKET + r"\.[1-9][0-9]*"
GITHUB_REPO = r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+"
CONFIG = "config.agenix.json"
ENVIRONMENT = "environment.agenix.json"
CATALOG = "docs/features/catalog.agenix.json"
SCHEMAS = {
    "config": "skills/agx-setup/assets/config.schema.json",
    "environment": "skills/agx-scaffold/assets/environment.schema.json",
    "catalog": "skills/agx-feature/assets/feature-catalog.schema.json",
    "feature": "templates/records/feature.schema.json",
    "ticket": "templates/records/local-ticket.schema.json",
}


def feature_path(item):
    return f"docs/features/{item}/feature.agenix.json"


def ticket_path(parent, item):
    return f"docs/features/{parent}/tickets/{item}.agenix.json"


def object_record(value, kind):
    if (
        not isinstance(value, dict)
        or value.get("kind") != kind
        or type(value.get("schema-version")) is not int
        or value["schema-version"] != 1
    ):
        raise Invalid(f"Expected a version 1 {kind} record")
    return value


def indexed(items, key="id"):
    result = {}
    for item in items:
        name = item[key]
        if name in result:
            raise Invalid(f"Duplicate {key}: {name}")
        result[name] = item
    return result


def check_graph(by_id):
    pending = {name: set(item["depends-on"]) for name, item in by_id.items()}
    for name, dependencies in pending.items():
        if name in dependencies:
            raise Invalid(f"Self-dependency: {name}")
        if missing := dependencies - by_id.keys():
            raise Invalid(f"{name} has unknown dependency {min(missing)}")
    try:
        tuple(TopologicalSorter(pending).static_order())
    except CycleError as exc:
        raise Invalid("Work-item dependency cycle") from exc


def validate_config(config):
    if (
        config.get("tracker") not in {"local", "github", "jira"}
        or not isinstance(config.get("github-repo"), str)
        or not re.fullmatch(GITHUB_REPO, config["github-repo"])
        or not isinstance(config.get("default-branch"), str)
        or not config["default-branch"]
    ):
        raise Invalid("Invalid tracker, GitHub repository or default branch")


class Records:
    def __init__(self, repository, bundle, *, revision=None, schemas=None):
        self.repo = repository
        self.root = repository.root
        self.schemas = Schemas(bundle)
        self.paths = SCHEMAS | (schemas or {})
        self.revision = revision
        self.cache = {}

    def exists(self, path):
        if self.revision is None:
            return contained(self.root, path).is_file()
        try:
            self.repo.snapshot(self.revision, path)
        except Unavailable:
            return False
        return True

    def record(self, kind, path):
        if path not in self.cache:
            if self.revision:
                value = strict_json(self.repo.snapshot(self.revision, path))
            else:
                value = read_json(contained(self.root, path))
            self.cache[path] = object_record(value, kind)
            self.schemas.validate(self.paths[kind], value)
        return self.cache[path]

    def validate_target(self, ref):
        target = ref["target"]
        if https(target):
            return
        path, _, anchor = target.partition("#")
        location = contained(self.root, path)
        revision = ref.get("revision") or self.revision
        raw = None
        if revision:
            raw = self.repo.snapshot(revision, path)
        elif not location.is_file():
            raise Unavailable(f"Artifact missing: {path}")
        if anchor or ref.get("acceptance-ids"):
            if raw is None:
                raw = location.read_bytes()
            try:
                source = raw.decode("utf-8")
            except UnicodeError as exc:
                raise Invalid(f"Referenced document is not UTF-8: {path}") from exc
            explicit = re.search(
                rf"""\b(?:id|name)=["']{re.escape(anchor)}["']""", source
            )
            if anchor and not explicit and anchor not in heading_anchors(source):
                raise Unavailable(f"Anchor cannot be resolved: {target}")
            for criterion in ref.get("acceptance-ids", []):
                if not re.search(rf"(?<![\w-]){re.escape(criterion)}(?![\w-])", source):
                    raise Unavailable(
                        f"Acceptance ID {criterion} cannot be resolved: {target}"
                    )
        if "checkpoint-id" in ref:
            if raw is None:
                raw = location.read_bytes()
            data = strict_json(raw)
            if not isinstance(data, dict):
                raise Invalid("Checkpoint reference must point to a JSON record")
            checkpoints = data.get("checkpoints", []) + [
                cp
                for task in data.get("tasks", [])
                for cp in task.get("checkpoints", [])
            ]
            if (
                sum(cp["checkpoint-id"] == ref["checkpoint-id"] for cp in checkpoints)
                != 1
            ):
                raise Invalid(f"Missing or ambiguous checkpoint at {target}")

    def config(self):
        config = self.record("config", CONFIG)
        validate_config(config)
        return config

    def environment(self):
        value = self.record("environment", ENVIRONMENT)
        units = indexed(value["units"])
        commands = indexed(value["commands"])
        services = indexed(value["services"])
        permissions = indexed(value["permissions"])
        contained(self.root, value["instruction-entry"])
        if not self.exists(value["instruction-entry"]):
            raise Unavailable("Environment instruction entry is missing")
        for unit in units.values():
            for path in [unit["root"], *unit["owned-modules"]]:
                contained(self.root, path)
        operations = set()
        command_slots = set()
        for command in commands.values():
            unit = units.get(command["unit-id"])
            if not unit or command["target"] not in unit["targets"]:
                raise Invalid("Command unit or target is unresolved")
            if (
                set(command.get("service-ids", [])) - services.keys()
                or set(command.get("permission-ids", [])) - permissions.keys()
            ):
                raise Invalid("Command service or permission is unresolved")
            if (
                not command["argv"]
                or not command["argv"][0]
                or "\0" in "".join(command["argv"])
            ):
                raise Invalid("Invalid command argument vector")
            if command["operation"] == "check" and not command.get("check-level"):
                raise Invalid("Check command requires a level")
            slot = tuple(
                command[key] for key in ("operation", "unit-id", "target", "mode")
            )
            if slot in command_slots:
                raise Invalid(
                    "Duplicate command for the same operation, unit, target and mode"
                )
            command_slots.add(slot)
            operations.add(command["operation"])
            contained(self.root, command["cwd"])
        for service in services.values():
            if set(service["operations"].values()) - commands.keys():
                raise Invalid("Service command is unresolved")
            for ref in service.get("fixtures", []):
                self.validate_target(ref)
        for permission in permissions.values():
            if set(permission["operation-ids"]) - operations - commands.keys():
                raise Invalid("Permission operation is unresolved")
            for path in permission["boundary"].get("roots", []):
                contained(self.root, path)
            ref = permission.get("evidence-ref")
            if permission["enforcement"] == "verified" and not ref:
                raise Invalid("Verified permission requires evidence")
            if ref:
                self.validate_target(ref)
        for ref in value["evidence"]:
            self.validate_target(ref)
        return commands

    def work_items(self, tracker, commands):
        catalog = self.record("catalog", CATALOG)
        config = self.config()
        native_ids = set()
        features = {
            item: self.feature(mapping, tracker, commands, config, native_ids)
            for item, mapping in indexed(catalog["features"]).items()
        }
        check_graph(features)
        return features

    def feature(self, mapping, tracker, commands, config, native_ids):
        item, path = mapping["id"], mapping["path"]
        if not re.fullmatch(FEATURE, item) or path != feature_path(item):
            raise Invalid("Catalog feature path or ID mismatch")
        feature = self.record("feature", path)
        if item != feature["id"]:
            raise Invalid("Feature ID does not match its record path")
        self.references(feature)
        strategy = feature.get("delivery-strategy", {})
        for ref in strategy.get("integration-coverage", []):
            self.validate_target(ref)
        tickets = {}
        for ticket_id, ticket in indexed(feature.get("tickets", [])).items():
            if not ticket_id.startswith(item + "-"):
                raise Invalid("Ticket mapping belongs to another feature")
            if tracker == "local":
                expected = ticket_path(item, ticket_id)
                if ticket.get("path") != expected:
                    raise Invalid("Invalid local ticket mapping")
                record = self.record("ticket", expected)
                self.ticket(record, ticket_id, item, commands)
                tickets[ticket_id] = record
            else:
                ref = ticket.get("native-ref", {})
                keys = {
                    "github": {"number", "url"},
                    "jira": {"key", "native-id", "url"},
                }
                if ref.keys() != keys[tracker]:
                    raise Invalid("Ticket mapping does not match tracker mode")
                if tracker == "github":
                    expected = f"https://github.com/{config['github-repo']}/issues/{ref['number']}"
                    if ref["url"].casefold() != expected.casefold():
                        raise Invalid(
                            "Native ticket URL is outside the configured GitHub repository"
                        )
                else:
                    jira = config.get("jira", {})
                    if not jira.get("site-url") or not jira.get("project-key"):
                        raise Unavailable(
                            "Jira site URL and project key are required to verify ticket mappings"
                        )
                    expected = f"{jira['site-url'].rstrip('/')}/browse/{ref['key']}"
                    if (
                        not ref["key"].startswith(jira["project-key"] + "-")
                        or ref["url"] != expected
                    ):
                        raise Invalid(
                            "Native ticket URL or key is outside the configured Jira project"
                        )
                identity = (
                    ref.get("number") if tracker == "github" else ref["native-id"]
                )
                if identity in native_ids:
                    raise Invalid("Native ticket is mapped more than once")
                native_ids.add(identity)
        check_graph(tickets)
        return feature

    def ticket(self, ticket, item, parent, commands):
        if (
            ticket["id"] != item
            or ticket["feature-id"] != parent
            or ticket["feature-ref"]["target"] != feature_path(parent)
        ):
            raise Invalid("Ticket identity or feature reference mismatch")
        self.references(ticket)
        self.validate_target(ticket["feature-ref"])
        tasks = indexed(ticket.get("tasks", []))
        check_graph(tasks)
        covered = {
            criterion
            for ref in ticket["references"]
            for criterion in ref.get("acceptance-ids", [])
        }
        checkpoint_ids = set()
        for owner in [ticket, *tasks.values()]:
            current = set(indexed(owner.get("checkpoints", []), "checkpoint-id"))
            if current & checkpoint_ids:
                raise Invalid("Duplicate checkpoint ID in ticket record")
            checkpoint_ids.update(current)
        for task_id, task in tasks.items():
            if not task_id.startswith(item + "."):
                raise Invalid("Task ID does not match its parent ticket")
            for dependency in task["depends-on"]:
                if tasks[dependency]["verification"]["method"] == "manual":
                    raise Invalid(f"Task {task_id} depends on manual task {dependency}")
            self.references(task)
            for criterion in indexed(task["acceptance"]).values():
                if set(criterion["covers"]) - covered:
                    raise Invalid("Task coverage refers outside its ticket")
            checks = task["verification"]["checks"]
            if checks and commands is None:
                raise Unavailable(
                    "Task check IDs require the verified environment record"
                )
            for check in checks:
                if check not in commands or not commands[check].get("check-level"):
                    raise Invalid(f"Unresolved task check: {check}")

    def references(self, owner):
        for key in ("requirements", "journeys", "references", "checkpoint-refs"):
            for ref in owner.get(key, []):
                self.validate_target(ref)
        for key in ("approval-ref", "origin-ref"):
            if key in owner:
                self.validate_target(owner[key])
        for allocation in owner.get("quality-allocations", []):
            self.validate_target(allocation["requirement-ref"])
        for checkpoint in indexed(
            owner.get("checkpoints", []), "checkpoint-id"
        ).values():
            if checkpoint.get("item-id") != owner["id"]:
                raise Invalid("Checkpoint item does not match its owner")
            for ref in checkpoint["references"]:
                self.validate_target(ref)


def heading_anchors(source):
    seen = set()
    fence = ""
    for line in source.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            if not fence:
                fence = marker[1]
            elif marker[1].startswith(fence) and not marker[2].strip():
                fence = ""
            continue
        if fence:
            continue
        heading = re.match(r"^ {0,3}#{1,6}[ \t]+(.+?)\s*#*\s*$", line)
        if heading:
            slug = re.sub(r"[^\w -]", "", heading[1].lower()).replace(" ", "-")
            candidate = slug
            index = 0
            while candidate in seen:
                index += 1
                candidate = f"{slug}-{index}"
            seen.add(candidate)
    return seen
