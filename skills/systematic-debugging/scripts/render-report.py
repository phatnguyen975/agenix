#!/usr/bin/env python3
"""Render the debug report (self-contained HTML) from a structured findings file.

Usage:
  python render-report.py --input FINDINGS.json --output REPORT.html
                          [--template TEMPLATE.html] [--overwrite] [--dry-run]
  python render-report.py --example      # print a sample findings file
  python render-report.py --labels       # print the default labels (to translate)

Steps:
  1. Validate the findings file for the report status (rules in references/report.md).
  2. Require a reason for every section that has no content (key "empty"), so no
     section is ever left blank.
  3. Scan every string for likely secrets (private keys, cloud and VCS tokens,
     JWTs, bearer tokens, credential assignments, URL credentials). On a match,
     nothing is written; the JSON path and pattern name are printed, never the value.
  4. Render the template. Every inserted value is HTML-escaped; GUIDE comments in
     the template are removed.

Template syntax (see assets/debug-report-template.html):
  {{name}}  {{a.b}}  value from the findings (innermost loop entry first)
  {{label.key}}      title in the report language (English default)
  {{.}}  {{@n}}      current list entry; its 1-based position
  <!--EACH list-->...<!--/EACH-->            repeat for every entry of a list
  <!--IF value-->...<!--ELSE-->...<!--/IF-->  choose a block (ELSE optional)

Exit codes: 0 written (or valid with --dry-run); 2 invalid input, template error,
usage error, or output exists without --overwrite; 3 likely secret detected.
"""

import argparse
import copy
import html
import json
import os
import re
import sys
from datetime import date as date_type
from pathlib import Path

DEFAULT_LABELS = {
    "report_kind": "Debug report",
    "skip_link": "Skip to content",
    "contents": "Contents",
    "not_provided": "Not provided",
    "date": "Date",
    "status_resolved": "Resolved",
    "status_mitigated": "Mitigated",
    "status_unresolved": "Unresolved",
    "glance": "At a glance",
    "glance_root_causes": "Root causes",
    "glance_hypotheses": "Hypotheses tested",
    "glance_refuted": "Refuted",
    "glance_checks": "Checks passed",
    "glance_files": "Files changed",
    "summary": "Summary",
    "symptom": "Symptom and impact",
    "expected": "Expected behavior",
    "actual": "Actual behavior",
    "impact": "Impact",
    "root_causes": "Root causes",
    "where": "Where",
    "why": "Why",
    "evidence": "Evidence",
    "investigation": "Investigation",
    "prediction": "Prediction",
    "experiment": "Experiment",
    "result_confirmed": "Confirmed",
    "result_refuted": "Refuted",
    "result_inconclusive": "Inconclusive",
    "fix": "Fix",
    "files_changed": "Files changed",
    "guard": "Regression guard",
    "guard_level": "Level",
    "guard_level_1": "Automated regression test at the correct test seam",
    "guard_level_2": "Committed reproduction script or check",
    "guard_level_3": "Benchmark with a threshold",
    "guard_level_4": "Repeated-run check with pinned reproduction rate",
    "guard_level_5": "Documented manual verification (unguarded)",
    "before": "Before the fix",
    "after": "After the fix",
    "verification": "Verification",
    "checks": "Checks",
    "command": "Command",
    "output": "Output",
    "verdict_pass": "Pass",
    "verdict_fail": "Fail",
    "verdict_not_run": "Not run",
    "statistics": "Statistics",
    "metric": "Metric",
    "follow_ups": "Follow-ups",
    "appendix": "Appendix",
    "command_log": "Command log",
    "exit_code": "Exit code",
    "environment": "Environment",
}

# Sections that may be empty; each needs a reason under findings["empty"][key].
EMPTY_KEYS = (
    "root_causes",
    "investigation",
    "fix",
    "guard",
    "verification",
    "statistics",
    "follow_ups",
    "appendix_commands",
    "appendix_environment",
)

SECRET_PATTERNS = [
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("aws-access-key-id", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    (
        "github-token",
        re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{22,}"),
    ),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("stripe-live-key", re.compile(r"\b[sr]k_live_[0-9A-Za-z]{16,}\b")),
    (
        "jwt",
        re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    ),
    (
        "bearer-token",
        re.compile(r"(?i)\bbearer\s+(?!\[?redacted)[A-Za-z0-9._~+/=-]{20,}"),
    ),
    (
        "credential-assignment",
        re.compile(
            r"(?i)\b(?:password|passwd|pwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token|"
            r"client[_-]?secret)\b\s*[:=]\s*[\"']?(?!\*{3}|<|\[?redacted|x{3}|[$%{]|[\w.]+\()"
            r"(?=[^\s\"',;]*[^A-Za-z\s\"',;])[^\s\"',;]{6,}"
        ),
    ),
    (
        "url-credentials",
        re.compile(r"\b[a-z][a-z0-9+.\-]*://[^\s/:@]+:(?!\*+@|\[?REDACTED)[^\s/@]+@"),
    ),
]

STATUSES = ("resolved", "mitigated", "unresolved")
VERDICTS = {"pass": "pass", "fail": "fail", "not_run": "neutral"}
RESULTS = {"confirmed": "pass", "refuted": "fail", "inconclusive": "neutral"}
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LANG_TAG = re.compile(r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$")

EXAMPLE = {
    "lang": "en",
    "title": "Order total ignores item quantity",
    "date": "2026-01-15",
    "status": "resolved",
    "summary": "Order totals were computed from unit prices only. The summing loop overwrote the running total instead of accumulating it. The fix accumulates the line totals; a regression test and the full suite pass.",
    "symptom": {
        "expected": "An order of 3 items at 10.00 totals 30.00.",
        "actual": "The same order totals 10.00.",
        "impact": "Invoices undercharge multi-item orders.",
    },
    "root_causes": [
        {
            "id": "RC-1",
            "what": "The line-total loop assigns instead of accumulates.",
            "where": "orders/totals (calculate_total, line 42)",
            "why": "Each iteration replaces the running total, so only the last line contributes.",
            "evidence": "Experiment 2 predicted that a two-line order returns the second line only; observed 20.00 for lines 10.00 and 20.00.",
        }
    ],
    "investigation": [
        {
            "hypothesis": "Quantity is lost while parsing the request.",
            "prediction": "The parsed order shows quantity 1 for every line.",
            "experiment": "Print the parsed order before totaling.",
            "result": "refuted",
        },
        {
            "hypothesis": "The total loop overwrites the running total.",
            "prediction": "A two-line order returns only the last line total.",
            "experiment": "Run the loop on a two-line order.",
            "result": "confirmed",
        },
    ],
    "fix": {
        "description": "Accumulate each line total into the running total.",
        "changes": [
            {
                "path": "orders/totals",
                "summary": "Use accumulation instead of assignment in calculate_total.",
            }
        ],
    },
    "guard": {
        "level": 1,
        "description": "Regression test for multi-item totals in the orders test suite.",
        "before": "1 failed: expected 30.00, got 10.00",
        "after": "1 passed",
    },
    "verification": [
        {
            "claim": "The regression guard fails before the fix",
            "command": "run the orders tests",
            "output": "1 failed",
            "verdict": "pass",
        },
        {
            "claim": "The relevant suite passes after the fix",
            "command": "run the orders tests",
            "output": "13 passed",
            "verdict": "pass",
        },
    ],
    "statistics": [
        {
            "metric": "Orders suite",
            "before": "12 passed, 1 failed",
            "after": "13 passed",
        }
    ],
    "follow_ups": ["Validate quantity at the request boundary."],
    "appendix": {
        "commands": [
            {"command": "run the orders tests", "exit_code": 1},
            {"command": "run the orders tests", "exit_code": 0},
        ],
        "environment": "Operating system and runtime versions of the machine used.",
    },
    "empty": {},
}


class TemplateError(Exception):
    pass


def esc(value):
    if isinstance(value, (dict, list)):
        raise TemplateError("a list or object was used where text is expected")
    return html.escape("" if value is None else str(value), quote=True)


def truthy(value):
    if isinstance(value, str):
        return bool(value.strip())
    return bool(value)


# ---------------------------------------------------------------- engine
TOKEN = re.compile(
    r"<!--\s*(?P<open>EACH|IF)\s+(?P<arg>[^\s>]+?)\s*-->"
    r"|<!--\s*(?P<else>ELSE)\s*-->"
    r"|<!--\s*/(?P<close>EACH|IF)\s*-->"
    r"|\{\{\s*(?P<var>[^{}]+?)\s*\}\}"
)
GUIDE = re.compile(r"<!--\s*GUIDE\b.*?-->", re.DOTALL)


def parse(template):
    template = GUIDE.sub("", template)
    root = []

    def append_text(target, text):
        if "{{" in text or "}}" in text:
            raise TemplateError("malformed template token; expected {{name}}")
        target.append(("text", text))

    stack = []
    current = root
    pos = 0
    for match in TOKEN.finditer(template):
        if match.start() > pos:
            append_text(current, template[pos : match.start()])
        pos = match.end()
        if match.group("var"):
            current.append(("var", match.group("var")))
        elif match.group("open"):
            frame = {
                "kind": match.group("open"),
                "arg": match.group("arg"),
                "then": [],
                "else": [],
                "in_else": False,
                "parent": current,
            }
            stack.append(frame)
            current = frame["then"]
        elif match.group("else"):
            if not stack or stack[-1]["kind"] != "IF" or stack[-1]["in_else"]:
                raise TemplateError("ELSE outside an IF block or used twice")
            stack[-1]["in_else"] = True
            current = stack[-1]["else"]
        else:
            kind = match.group("close")
            if not stack or stack[-1]["kind"] != kind:
                raise TemplateError(f"unbalanced /{kind}")
            frame = stack.pop()
            node = (
                ("each", frame["arg"], frame["then"])
                if kind == "EACH"
                else ("if", frame["arg"], frame["then"], frame["else"])
            )
            frame["parent"].append(node)
            current = frame["parent"]
    if stack:
        raise TemplateError(f"unclosed {stack[-1]['kind']} {stack[-1]['arg']}")
    if pos < len(template):
        append_text(current, template[pos:])
    return root


class Context:
    def __init__(self, labels):
        self.labels = labels
        self.used_defaults = set()

    def label(self, key):
        if key in self.labels and isinstance(self.labels[key], str):
            return self.labels[key]
        if key not in DEFAULT_LABELS:
            raise TemplateError(f"unknown label: {key}")
        self.used_defaults.add(key)
        return DEFAULT_LABELS[key]

    def resolve(self, name, frames):
        if name == ".":
            return frames[-1][0]
        if name == "@n":
            return frames[-1][1]
        parts = name.split(".")
        if parts[0] == "label" and len(parts) == 2:
            return self.label(parts[1])
        for value, _ in reversed(frames):
            if isinstance(value, dict) and parts[0] in value:
                current = value[parts[0]]
                for part in parts[1:]:
                    if isinstance(current, dict) and part in current:
                        current = current[part]
                    else:
                        raise KeyError(name)
                return current
        raise KeyError(name)

    def render(self, nodes, frames):
        out = []
        for node in nodes:
            kind = node[0]
            if kind == "text":
                out.append(node[1])
            elif kind == "var":
                try:
                    out.append(esc(self.resolve(node[1], frames)))
                except KeyError:
                    raise TemplateError("no value for {{" + node[1] + "}}")
            elif kind == "if":
                try:
                    chosen = truthy(self.resolve(node[1], frames))
                except KeyError:
                    chosen = False
                out.append(self.render(node[2] if chosen else node[3], frames))
            else:
                try:
                    items = self.resolve(node[1], frames)
                except KeyError:
                    raise TemplateError(f"no list for EACH {node[1]}")
                if not isinstance(items, list):
                    raise TemplateError(f"EACH {node[1]} needs a list")
                for index, item in enumerate(items, 1):
                    out.append(self.render(node[2], frames + [(item, index)]))
        return "".join(out)


# ------------------------------------------------------------ validation
def is_text(value):
    return isinstance(value, str) and bool(value.strip())


def section_content(data):
    appendix = data.get("appendix") if isinstance(data.get("appendix"), dict) else {}
    fix = data.get("fix")
    return {
        "root_causes": data.get("root_causes"),
        "investigation": data.get("investigation"),
        "fix": fix
        if isinstance(fix, dict) and is_text(fix.get("description"))
        else None,
        "guard": data.get("guard") if isinstance(data.get("guard"), dict) else None,
        "verification": data.get("verification"),
        "statistics": data.get("statistics"),
        "follow_ups": data.get("follow_ups"),
        "appendix_commands": appendix.get("commands"),
        "appendix_environment": appendix.get("environment"),
    }


def validate(data):
    errors = []

    def need(condition, message):
        if not condition:
            errors.append(message)

    if not isinstance(data, dict):
        return ["findings must be a JSON object"]
    status = data.get("status")
    need(is_text(data.get("title")), "title is required")
    need(status in STATUSES, f"status must be one of {', '.join(STATUSES)}")
    need(is_text(data.get("summary")), "summary is required")
    lang = data.get("lang", "en")
    need(
        isinstance(lang, str) and LANG_TAG.fullmatch(lang),
        "lang must be a language tag such as en or vi",
    )
    if data.get("date") not in (None, ""):
        date_value = data["date"]
        valid_date = isinstance(date_value, str) and ISO_DATE.fullmatch(date_value)
        if valid_date:
            try:
                date_type.fromisoformat(date_value)
            except ValueError:
                valid_date = False
        need(valid_date, "date must be YYYY-MM-DD")
    symptom = data.get("symptom")
    need(
        isinstance(symptom, dict)
        and is_text(symptom.get("expected"))
        and is_text(symptom.get("actual")),
        "symptom.expected and symptom.actual are required",
    )
    if isinstance(symptom, dict) and symptom.get("impact") not in (None, ""):
        need(isinstance(symptom["impact"], str), "symptom.impact must be text")

    def list_of_dicts(key):
        value = data.get(key)
        if value is None:
            return []
        if not isinstance(value, list) or not all(
            isinstance(item, dict) for item in value
        ):
            errors.append(f"{key} must be a list of objects")
            return []
        return value

    for i, rc in enumerate(list_of_dicts("root_causes")):
        for key in ("what", "where", "why", "evidence"):
            need(is_text(rc.get(key)), f"root_causes[{i}].{key} is required")
        need(
            rc.get("id") in (None, "") or isinstance(rc.get("id"), str),
            f"root_causes[{i}].id must be text",
        )
    for i, row in enumerate(list_of_dicts("investigation")):
        for key in ("hypothesis", "prediction", "experiment"):
            need(is_text(row.get(key)), f"investigation[{i}].{key} is required")
        result = row.get("result")
        need(
            isinstance(result, str) and result in RESULTS,
            f"investigation[{i}].result must be one of {', '.join(RESULTS)}",
        )
    for i, row in enumerate(list_of_dicts("verification")):
        need(is_text(row.get("claim")), f"verification[{i}].claim is required")
        verdict = row.get("verdict")
        need(
            isinstance(verdict, str) and verdict in VERDICTS,
            f"verification[{i}].verdict must be one of {', '.join(VERDICTS)}",
        )
        for key in ("command", "output"):
            need(
                row.get(key) in (None, "") or isinstance(row.get(key), str),
                f"verification[{i}].{key} must be text",
            )
    for i, row in enumerate(list_of_dicts("statistics")):
        need(is_text(row.get("metric")), f"statistics[{i}].metric is required")
        for key in ("before", "after"):
            value = row.get(key)
            valid_value = (
                is_text(value)
                if isinstance(value, str)
                else isinstance(value, (int, float)) and not isinstance(value, bool)
            )
            need(
                valid_value,
                f"statistics[{i}].{key} is required as text or a number",
            )
    follow_ups = data.get("follow_ups")
    if follow_ups is not None:
        need(
            isinstance(follow_ups, list) and all(is_text(x) for x in follow_ups),
            "follow_ups must be a list of non-empty text items",
        )

    fix = data.get("fix")
    if fix is not None:
        need(isinstance(fix, dict), "fix must be an object")
        if isinstance(fix, dict) and fix:
            need(
                is_text(fix.get("description")),
                "fix.description is required when fix has content",
            )
        if isinstance(fix, dict) and fix.get("changes") is not None:
            changes = fix["changes"]
            need(
                isinstance(changes, list)
                and all(
                    isinstance(c, dict)
                    and is_text(c.get("path"))
                    and is_text(c.get("summary"))
                    for c in changes
                ),
                "fix.changes items need path and summary",
            )
    guard = data.get("guard")
    if guard is not None:
        need(isinstance(guard, dict), "guard must be an object")
        if isinstance(guard, dict):
            level = guard.get("level")
            need(
                isinstance(level, int)
                and not isinstance(level, bool)
                and 1 <= level <= 5,
                "guard.level must be an integer from 1 to 5",
            )
            for key in ("description", "before", "after"):
                need(
                    guard.get(key) in (None, "") or isinstance(guard.get(key), str),
                    f"guard.{key} must be text",
                )
    appendix = data.get("appendix")
    if appendix is not None:
        need(isinstance(appendix, dict), "appendix must be an object")
        if isinstance(appendix, dict):
            commands = appendix.get("commands")
            if commands is not None:
                need(
                    isinstance(commands, list)
                    and all(
                        isinstance(c, dict)
                        and is_text(c.get("command"))
                        and isinstance(c.get("exit_code"), int)
                        and not isinstance(c.get("exit_code"), bool)
                        for c in commands
                    ),
                    "appendix.commands items need command and integer exit_code",
                )
            need(
                appendix.get("environment") in (None, "")
                or isinstance(appendix.get("environment"), str),
                "appendix.environment must be text",
            )
    labels = data.get("labels")
    if labels is not None:
        need(
            isinstance(labels, dict)
            and all(isinstance(v, str) for v in labels.values()),
            "labels must be an object of text values",
        )

    content = section_content(data)
    if status == "resolved":
        for key in ("root_causes", "fix", "guard", "verification"):
            need(truthy(content[key]), f"status resolved requires {key}")
    elif status == "mitigated":
        for key in ("fix", "verification"):
            need(
                truthy(content[key]),
                f"status mitigated requires {key} (the mitigation and its checks)",
            )
    elif status == "unresolved":
        need(
            truthy(content["investigation"]), "status unresolved requires investigation"
        )

    reasons = data.get("empty")
    if reasons is not None and not isinstance(reasons, dict):
        errors.append("empty must be an object")
        reasons = {}
    reasons = reasons or {}
    for key in EMPTY_KEYS:
        if not truthy(content[key]):
            need(
                is_text(reasons.get(key)),
                f"section {key} has no content: add empty.{key} with the reason it is empty",
            )
    return errors


def scan_secrets(node, path="$"):
    found = []
    if isinstance(node, str):
        found.extend(
            (path, name) for name, pattern in SECRET_PATTERNS if pattern.search(node)
        )
    elif isinstance(node, dict):
        for key, value in node.items():
            found.extend(scan_secrets(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(scan_secrets(value, f"{path}[{index}]"))
    return found


def enrich(data, ctx):
    d = copy.deepcopy(data)
    d["lang"] = d.get("lang") or "en"
    d["status_class"] = d["status"]
    d["status_label"] = ctx.label("status_" + d["status"])
    d.setdefault("empty", {})
    for i, rc in enumerate(d.get("root_causes") or [], 1):
        if not is_text(rc.get("id")):
            rc["id"] = f"RC-{i}"
    for row in d.get("investigation") or []:
        row["result_class"] = RESULTS[row["result"]]
        row["result_label"] = ctx.label("result_" + row["result"])
    for row in d.get("verification") or []:
        row["verdict_class"] = VERDICTS[row["verdict"]]
        row["verdict_label"] = ctx.label("verdict_" + row["verdict"])
    if isinstance(d.get("guard"), dict):
        d["guard"]["level_name"] = ctx.label(f"guard_level_{d['guard']['level']}")
    checks = d.get("verification") or []
    fix = d.get("fix") if isinstance(d.get("fix"), dict) else {}
    d["glance"] = {
        "root_causes": len(d.get("root_causes") or []),
        "hypotheses": len(d.get("investigation") or []),
        "refuted": sum(r["result"] == "refuted" for r in d.get("investigation") or []),
        "checks_passed": sum(c["verdict"] == "pass" for c in checks),
        "checks_total": len(checks),
        "files_changed": len(fix.get("changes") or []),
    }
    return d


def paths_refer_to_same_file(first, second):
    """Compare resolved paths and, when possible, filesystem identities."""
    try:
        if first.exists() and second.exists() and os.path.samefile(first, second):
            return True
        return first.resolve() == second.resolve()
    except (OSError, RuntimeError):
        return False


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--input", help="findings JSON file")
    parser.add_argument("--output", help="report path to write")
    parser.add_argument(
        "--template", default=None, help="HTML template (default: bundled)"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace an existing report only with explicit approval",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate, scan, and render; write nothing",
    )
    parser.add_argument(
        "--example", action="store_true", help="print a sample findings file"
    )
    parser.add_argument(
        "--labels",
        action="store_true",
        help="print the default labels as JSON (translate the values for a non-English report)",
    )
    args = parser.parse_args()

    if args.labels:
        print(json.dumps(DEFAULT_LABELS, indent=2, ensure_ascii=False))
        return 0

    if args.example:
        print(json.dumps(EXAMPLE, indent=2))
        return 0
    if not args.input or (not args.output and not args.dry_run):
        parser.error(
            "--input and --output are required (or use --dry-run, or --example)"
        )

    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"error: cannot read findings: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        print("error: invalid findings:", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 2

    findings = scan_secrets(data)
    if findings:
        print(
            f"error: {len(findings)} likely secret(s) detected; nothing was written. "
            "Redact them in the findings file and run again:",
            file=sys.stderr,
        )
        for path, name in findings:
            print(f"  - {path}: {name}", file=sys.stderr)
        return 3

    template_path = (
        Path(args.template)
        if args.template
        else (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "debug-report-template.html"
        )
    )
    try:
        template = template_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"error: cannot read template: {exc}", file=sys.stderr)
        return 2

    ctx = Context(data.get("labels") or {})
    try:
        enriched = enrich(data, ctx)
        page = ctx.render(parse(template), [(enriched, 0)])
    except TemplateError as exc:
        print(f"error: template problem: {exc}", file=sys.stderr)
        return 2

    if ctx.used_defaults and not str(enriched["lang"]).lower().startswith("en"):
        print(
            "warning: no translation provided; English used for labels: "
            + ", ".join(sorted(ctx.used_defaults)),
            file=sys.stderr,
        )
    if args.dry_run:
        print("ok: findings are valid, no secrets detected, template renders")
        return 0
    output = Path(args.output)
    for source_name, source_path in (
        ("findings input", Path(args.input)),
        ("template", template_path),
    ):
        if paths_refer_to_same_file(output, source_path):
            print(
                f"error: output path must differ from {source_name}; nothing was written",
                file=sys.stderr,
            )
            return 2
    if output.exists() and not args.overwrite:
        print(
            f"error: {output} already exists; ask the human before overwriting",
            file=sys.stderr,
        )
        return 2
    # Fail before touching the output path if inserted text cannot be encoded as UTF-8.
    try:
        page.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"error: report cannot be encoded as UTF-8: {exc}", file=sys.stderr)
        return 2

    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(page, encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot write report: {exc}", file=sys.stderr)
        return 2
    print(f"report written: {output}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(1)
