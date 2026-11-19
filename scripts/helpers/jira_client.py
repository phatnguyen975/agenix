"""Bounded Jira Cloud REST operations for the configured project."""

import base64
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .core import Invalid, Unavailable, contained, read_json, strict_json

CREDENTIALS = ".agenix/credentials/jira.json"
ISSUE_TYPES = {"ticket", "task"}
LIFECYCLE = {
    "ready": "todo",
    "blocked": "todo",
    "in-progress": "in-progress",
    "in-review": "in-progress",
    "done": "done",
    "cancelled": "cancelled",
}
ISSUE_FIELDS = "project,issuetype,parent,summary,description,labels,status,issuelinks"


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class RejectedWrite(Unavailable):
    """The endpoint explicitly rejected a write before creation."""


def credential_header(root, relative):
    expected = root / CREDENTIALS
    location = contained(root, relative, private=True)
    if relative != CREDENTIALS or location != expected:
        raise Invalid("Use the private Jira credentials file at its declared location")
    try:
        credentials = read_json(location)
    except Invalid:
        raise Invalid("Invalid Jira credential file") from None
    if not isinstance(credentials, dict) or credentials.keys() != {
        "email",
        "api-token",
    }:
        raise Invalid("Jira credentials require email and api-token")
    email, token = credentials["email"], credentials["api-token"]
    if (
        not isinstance(email, str)
        or not re.fullmatch(r"[^\s:@]+@[^\s:@]+", email)
        or not isinstance(token, str)
        or not token
        or any(ord(ch) <= 32 for ch in token)
    ):
        raise Invalid("Invalid Jira credential fields")
    encoded = base64.b64encode(f"{email}:{token}".encode()).decode("ascii")
    return "Basic " + encoded


def label_list(value):
    if (
        not isinstance(value, list)
        or any(not isinstance(label, str) or not label for label in value)
        or len(set(value)) != len(value)
    ):
        raise Invalid("Expected unique nonempty Jira labels")
    return value


def adf(value):
    if (
        not isinstance(value, dict)
        or value.get("type") != "doc"
        or value.get("version") != 1
        or not isinstance(value.get("content"), list)
    ):
        raise Invalid("Expected an ADF version 1 document")
    return value


def exposed_issue(data):
    fields = data["fields"]
    result = {
        "key": data["key"],
        "id": data["id"],
        "summary": fields["summary"],
        "type": fields["issuetype"]["id"],
        "labels": fields["labels"],
        "status": fields["status"]["id"],
        "description": fields.get("description"),
        "links": fields.get("issuelinks", []),
    }
    if fields.get("parent"):
        result["parent"] = fields["parent"]["key"]
    return result


class Jira:
    def __init__(self, config, authorization, *, opener=None, timeout=15):
        self.config = config
        self.project = config.get("project-key")
        cloud = config.get("cloud-id")
        if not isinstance(cloud, str) or not re.fullmatch(
            r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", cloud
        ):
            raise Invalid("Expected the configured Jira Cloud UUID")
        if not isinstance(self.project, str) or not re.fullmatch(
            r"[A-Z][A-Z0-9_]+", self.project
        ):
            raise Invalid("Invalid Jira project key")
        if not 1 <= timeout <= 60:
            raise Invalid("Jira timeout must be between 1 and 60 seconds")
        self.base = f"https://api.atlassian.com/ex/jira/{cloud}/rest/api/3/"
        self.authorization = authorization
        self.opener = opener if opener is not None else build_opener(NoRedirect())
        self.timeout = timeout

    def request(self, method, path, *, query=None, payload=None, search=False):
        url = self.base + path + ("?" + urlencode(query) if query else "")
        raw = (
            json.dumps(payload, ensure_ascii=False).encode("utf-8")
            if payload is not None
            else None
        )
        headers = {"Accept": "application/json", "Authorization": self.authorization}
        if raw is not None:
            headers["Content-Type"] = "application/json; charset=utf-8"
        request = Request(url, data=raw, headers=headers, method=method)
        writing = method != "GET" and not search
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                body = response.read(8 * 1024 * 1024 + 1)
        except HTTPError as exc:
            exc.close()
            if writing and (exc.code >= 500 or exc.code in {408, 429}):
                raise Unavailable(
                    f"Jira write outcome uncertain (HTTP {exc.code}); reconcile before retry"
                ) from None
            if writing and exc.code in {400, 401, 403, 404, 422}:
                raise RejectedWrite(
                    f"Jira rejected the write (HTTP {exc.code})"
                ) from None
            raise Unavailable(f"Jira request failed (HTTP {exc.code})") from None
        except (URLError, OSError):
            detail = "Jira request did not complete"
            if writing:
                detail += "; reconcile the write before retry"
            raise Unavailable(detail) from None
        try:
            if len(body) > 8 * 1024 * 1024:
                raise Invalid("Jira response exceeds size limit")
            value = strict_json(body) if body else {}
            if not isinstance(value, dict):
                raise Invalid("Expected a Jira response object")
            return value
        except Invalid:
            detail = "Jira returned an unusable response"
            if writing:
                detail += "; reconcile the write before retry"
            raise Unavailable(detail) from None

    def key(self, key):
        if not isinstance(key, str) or not re.fullmatch(
            re.escape(self.project) + r"-[1-9][0-9]*", key
        ):
            raise Invalid("Jira issue key is outside the configured project")
        return key

    def issue(self, key):
        key = self.key(key)
        issue = self.request("GET", f"issue/{key}", query={"fields": ISSUE_FIELDS})
        try:
            if issue["key"] != key or issue["fields"]["project"]["key"] != self.project:
                raise Invalid(
                    "Jira issue identity does not match the requested project and key"
                )
            exposed_issue(issue)
            if issue["fields"].get("parent"):
                self.key(issue["fields"]["parent"]["key"])
        except (KeyError, TypeError):
            raise Unavailable("Jira issue read lacks required fields") from None
        return issue

    def offset_pages(self, path, collection, *, query=None):
        offset = 0
        while True:
            page = self.request(
                "GET", path, query=(query or {}) | {"startAt": offset, "maxResults": 50}
            )
            values = page.get(collection)
            if (
                not isinstance(values, list)
                or page.get("startAt") != offset
                or type(page.get("total")) is not int
                or page["total"] < offset + len(values)
            ):
                raise Unavailable("Jira returned an incomplete paginated response")
            yield from values
            offset += len(values)
            if offset == page["total"]:
                return
            if not values:
                raise Unavailable("Jira pagination stopped before the final page")

    def search(self, parent=None):
        query = f'project = "{self.project}"'
        if parent is not None:
            query += f' AND parent = "{self.key(parent)}"'
        payload = {
            "jql": query + " ORDER BY key ASC",
            "fields": ISSUE_FIELDS.split(","),
            "maxResults": 100,
        }
        seen = set()
        while True:
            page = self.request("POST", "search/jql", payload=payload, search=True)
            if not isinstance(page.get("issues"), list):
                raise Unavailable("Jira search returned an incomplete page")
            yield from page["issues"]
            if page.get("isLast") is True:
                return
            cursor = page.get("nextPageToken")
            if not isinstance(cursor, str) or not cursor or cursor in seen:
                raise Unavailable("Jira search cursor missing or repeated")
            seen.add(cursor)
            payload["nextPageToken"] = cursor

    def discover(self, issue_type=None):
        path = f"issue/createmeta/{self.project}/issuetypes"
        if issue_type is not None:
            return list(
                self.offset_pages(f"{path}/{self.native_id(issue_type)}", "fields")
            )
        return list(self.offset_pages(path, "issueTypes"))

    def children(self, key):
        if self.role(self.issue(key)) != "ticket":
            raise Invalid("Jira children require a configured ticket")
        result = []
        seen = set()
        for match in self.search(key):
            issue = self.issue(match["key"])
            child = exposed_issue(issue)
            if (
                self.role(issue) != "task"
                or child.get("parent") != key
                or child["key"] in seen
            ):
                raise Invalid("Jira child mapping is inconsistent")
            seen.add(child["key"])
            result.append(child)
        return result

    def transitions(self, key):
        self.issue(key)
        response = self.request(
            "GET", f"issue/{key}/transitions", query={"expand": "transitions.fields"}
        )
        values = response.get("transitions")
        if not isinstance(values, list):
            raise Unavailable("Jira did not return a transition list")
        return values

    @staticmethod
    def native_id(value):
        if not isinstance(value, str) or not re.fullmatch(r"[0-9]+", value):
            raise Invalid("Expected a discovered numeric Jira ID")
        return value

    def role(self, issue):
        for role, native in self.config.get("issue-types", {}).items():
            if native == issue["fields"]["issuetype"]["id"]:
                return role
        raise Invalid("Jira issue type is outside the configured workflow")

    def reconcile(self, spec, known_key=None):
        item, parent, role = spec["item"], spec.get("parent"), spec["role"]
        validate_create(spec)
        if parent:
            issue = self.issue(parent)
            if self.role(issue) != "ticket" or not issue["fields"][
                "summary"
            ].startswith(item.split(".")[0] + ": "):
                raise Invalid("Jira task requires its exact native ticket parent")
        if known_key:
            keys = {self.key(known_key)}
        else:
            keys = {
                self.key(entry["key"])
                for entry in self.search()
                if entry.get("fields", {}).get("summary", "").startswith(item + ":")
            }
        if len(keys) > 1:
            raise Invalid("Multiple native Jira issues claim the same Agenix ID")
        if not keys:
            return None
        issue = self.issue(keys.pop())
        fields = issue["fields"]
        if (
            self.role(issue) != role
            or (fields.get("parent") or {}).get("key") != parent
            or fields["summary"] != spec["summary"]
            or fields.get("description") != spec["description"]
        ):
            raise Invalid(
                "Native Jira issue differs from the approved definition or parent"
            )
        classification = {
            label
            for label in spec["labels"]
            if label.startswith(("scope:", "priority:"))
        }
        actual_classification = {
            label
            for label in fields["labels"]
            if label.startswith(("scope:", "priority:"))
        }
        if classification != actual_classification:
            raise Invalid(
                "Native Jira scope or priority differs from the approved definition"
            )
        return issue

    def create(self, spec, pending=None):
        validate_create(spec)
        previous = self.reconcile(spec, known_key=pending.key() if pending else None)
        if previous:
            if pending:
                pending.record(previous["key"])
            return {"result": "existing", "issue": exposed_issue(previous)}
        fields = self.config.get("field-defaults", {}).get(spec["role"], {}) | spec.get(
            "fields", {}
        )
        reserved = {
            "project",
            "issuetype",
            "parent",
            "summary",
            "description",
            "labels",
        }
        if fields.keys() & reserved:
            raise Invalid(
                "Custom Jira fields cannot override the approved issue definition"
            )
        fields.update(
            project={"key": self.project},
            issuetype={
                "id": self.native_id(
                    self.config.get("issue-types", {}).get(spec["role"])
                )
            },
            summary=spec["summary"],
            description=spec["description"],
            labels=spec["labels"],
        )
        if spec.get("parent"):
            fields["parent"] = {"key": self.key(spec["parent"])}
        if pending:
            pending.begin()
        try:
            created = self.request("POST", "issue", payload={"fields": fields})
        except RejectedWrite:
            if pending:
                pending.clear()
            raise
        if not isinstance(created.get("key"), str):
            raise Unavailable("Jira create returned no key; reconcile before retry")
        if pending:
            pending.record(self.key(created["key"]))
        issue = self.issue(created["key"])
        actual = issue["fields"]
        if (
            self.role(issue) != spec["role"]
            or (actual.get("parent") or {}).get("key") != spec.get("parent")
            or actual["summary"] != spec["summary"]
            or actual.get("description") != spec["description"]
            or not set(spec["labels"]) <= set(actual["labels"])
        ):
            raise Invalid("Created Jira issue differs from the approved definition")
        return {"result": "created", "issue": exposed_issue(issue)}

    def status(self, key, target, fields, transition_id=None):
        issue = self.issue(key)
        role = self.role(issue)
        if target not in LIFECYCLE:
            raise Invalid("Unknown Jira lifecycle label")
        native = self.native_id(
            self.config.get("status-targets", {}).get(role, {}).get(LIFECYCLE[target])
        )
        if issue["fields"]["status"]["id"] != native:
            transitions = self.request(
                "GET",
                f"issue/{key}/transitions",
                query={"expand": "transitions.fields"},
            ).get("transitions", [])
            matches = [
                entry
                for entry in transitions
                if entry["to"]["id"] == native
                and (transition_id is None or transition_id == entry["id"])
            ]
            if len(matches) != 1:
                raise Unavailable(
                    "No unique Jira transition to the selected native status"
                )
            if fields.keys() & {
                "labels",
                "project",
                "issuetype",
                "parent",
                "summary",
                "description",
            }:
                raise Invalid(
                    "Transition fields cannot override the approved issue definition"
                )
            if any(
                field.get("required")
                and not field.get("hasDefaultValue")
                and key not in fields
                for key, field in matches[0].get("fields", {}).items()
            ):
                raise Invalid("Jira transition is missing required fields")
            self.request(
                "POST",
                f"issue/{key}/transitions",
                payload={"transition": {"id": matches[0]["id"]}, "fields": fields},
            )
        current = self.issue(key)
        current_labels = label_list(current["fields"]["labels"])
        current_status = [
            label for label in current_labels if label.casefold().startswith("status:")
        ]
        target_label = f"status:{target}"
        if current_status != [target_label]:
            edits = [
                {"remove": label} for label in current_status if label != target_label
            ]
            if target_label not in current_status:
                edits.append({"add": target_label})
            self.request("PUT", f"issue/{key}", payload={"update": {"labels": edits}})
        actual = self.issue(key)
        if actual["fields"]["status"]["id"] != native or [
            label
            for label in actual["fields"]["labels"]
            if label.casefold().startswith("status:")
        ] != [target_label]:
            raise Unavailable(
                "Jira status update is incomplete; reconcile existing issue"
            )
        return exposed_issue(actual)

    def comment(self, key, body):
        adf(body)
        self.issue(key)
        comments = self.offset_pages(f"issue/{key}/comment", "comments")
        matches = [entry for entry in comments if entry["body"] == body]
        if len(matches) > 1:
            raise Invalid("Multiple Jira comments match the same checkpoint")
        if matches:
            return {"comment-id": matches[0]["id"], "result": "existing"}
        entry = self.request(
            "POST", f"issue/{key}/comment", payload={"body": adf(body)}
        )
        identifier = self.native_id(entry.get("id"))
        actual = self.request("GET", f"issue/{key}/comment/{identifier}")
        if actual.get("id") != identifier or actual.get("body") != body:
            raise Unavailable(
                "Jira comment could not be confirmed; reconcile before retry"
            )
        return {"comment-id": identifier, "result": "created"}

    def dependency(self, dependent, prerequisite):
        issue = self.issue(dependent)
        self.issue(prerequisite)
        if prerequisite == dependent:
            raise Invalid("Jira issue cannot depend on itself")
        link = self.config.get("dependency-link", {})
        direction = link.get("direction")
        identifier = self.native_id(link.get("type-id"))
        if direction not in {"inward", "outward"}:
            raise Invalid("Invalid Jira dependency link direction")
        other = direction + "Issue"

        def present(value):
            return any(
                item.get("type", {}).get("id") == identifier
                and item.get(other, {}).get("key") == prerequisite
                for item in value["fields"].get("issuelinks", [])
            )

        if not present(issue):
            # The direction names the related issue as seen from the dependent.
            opposite = "inwardIssue" if direction == "outward" else "outwardIssue"
            self.request(
                "POST",
                "issueLink",
                payload={
                    "type": {"id": identifier},
                    other: {"key": prerequisite},
                    opposite: {"key": dependent},
                },
            )
            if not present(self.issue(dependent)):
                raise Unavailable("Jira dependency link could not be confirmed")
        return {
            "dependent": dependent,
            "prerequisite": prerequisite,
            "result": "verified",
        }


def validate_create(spec):
    role = spec.get("role")
    if role not in ISSUE_TYPES or (role == "task") != bool(spec.get("parent")):
        raise Invalid("Select a native Jira type and the appropriate parent")
    from .records import TASK, TICKET

    pattern = TASK if role == "task" else TICKET
    item = spec.get("item")
    if not isinstance(item, str) or not re.fullmatch(pattern, item):
        raise Invalid("Invalid Agenix ID for Jira issue type")
    if not isinstance(spec.get("summary"), str) or not spec["summary"].startswith(
        item + ": "
    ):
        raise Invalid("Jira summary must include the exact Agenix ID")
    adf(spec.get("description"))
    labels = label_list(spec.get("labels"))
    if [label for label in labels if label.casefold().startswith("status:")] not in (
        ["status:ready"],
        ["status:blocked"],
    ):
        raise Invalid("New Jira issues require one initial lifecycle label")
    if role == "ticket" and any(
        sum(label.startswith(prefix) and len(label) > len(prefix) for label in labels)
        != 1
        for prefix in ("scope:", "priority:")
    ):
        raise Invalid("New Jira tickets require an approved scope and priority label")
    if "fields" in spec and not isinstance(spec["fields"], dict):
        raise Invalid("Jira custom fields must be an object")
