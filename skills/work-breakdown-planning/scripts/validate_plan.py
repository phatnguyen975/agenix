#!/usr/bin/env python3
"""Validate a Slice Plan file produced with the work-breakdown-planning skill.

Usage: python validate_plan.py <plan-file.md>

Checks (errors):
  - Header fields present and well formed
  - Every Slice has the required fields and sections
  - Dependencies reference existing Slices, no self-dependency, no duplicate
    entry, no cycle (one concrete cycle is reported)
  - Status invariants (BLOCKED iff an unfinished Dependency; IN-PROGRESS / DONE
    need finished Dependencies; DONE needs every acceptance criterion checked)
  - Dependency Graph edges and classes match the Slice data
  - Execution Order matches the Waves computed from the Dependencies
  - Progress counts match the Slice data
  - References table rows complete with unique IDs; every Reference used by a
    Slice exists in the table

Warnings: A Dependency implied through another Dependency, a Slice reference
  without a section part, a registered Reference that no Slice uses, leftover
  template comments, possible leftover placeholders, Atomic Slices with more
  than 5 acceptance criteria.

Exit code: 0 when there are no errors, 1 otherwise. Standard library only.
"""

import re
import sys
from pathlib import Path

STATUSES = ["READY", "BLOCKED", "IN-PROGRESS", "DONE"]
CLASS_OF = {
    "READY": "ready",
    "BLOCKED": "blocked",
    "IN-PROGRESS": "inProgress",
    "DONE": "done",
}
REQUIRED_SECTIONS = [
    "Outcome",
    "In scope",
    "Out of scope",
    "Acceptance Criteria",
    "Verification",
]
MAX_ATOMIC_CRITERIA = 5
EXPECTED_ARGS = 2


def section(text, title):
    """Body of a '## title' section, or None."""
    m = re.search(
        r"^## " + re.escape(title) + r"\s*$(.*?)(?=^## |\Z)",
        text,
        re.DOTALL | re.MULTILINE,
    )
    return m.group(1) if m else None


def block(content, title):
    """Body of a '**title:**' block, or an empty string."""
    m = re.search(
        r"\*\*" + re.escape(title) + r":\*\*(.*?)(?=\n\*\*|\Z)",
        content,
        re.DOTALL,
    )
    return m.group(1) if m else ""


def parse_slices(body):
    """Parse Slice headings into a mapping of Slice ID to Slice data."""
    slices = {}
    parts = re.split(r"^### (S\d+) · (.+)$", body, flags=re.MULTILINE)
    for i in range(1, len(parts), 3):
        sid, title, content = parts[i], parts[i + 1].strip(), parts[i + 2]
        fields = {
            m.group(1).strip(): m.group(2).strip()
            for m in re.finditer(
                r"^\|\s*([A-Za-z ]+?)\s*\|\s*([^|]*?)\s*\|\s*$",
                content,
                re.MULTILINE,
            )
        }
        deps = []
        raw = fields.get("Depends on", "—").strip()
        if raw not in ("—", "-", ""):
            for seg in re.split(r";\s*(?=S\d+\b)", raw):
                m = re.match(r"\s*(S\d+)\b", seg)
                deps.append(m.group(1) if m else "?" + seg.strip())
        ac = re.findall(
            r"^- \[([ xX])\]",
            block(content, "Acceptance Criteria"),
            re.MULTILINE,
        )
        refs = re.findall(r"\bR\d+\b", block(content, "References"))
        slices[sid] = {
            "title": title,
            "fields": fields,
            "deps": deps,
            "status": fields.get("Status", "").strip(),
            "gran": fields.get("Granularity", "").strip(),
            "ac_total": len(ac),
            "ac_done": sum(1 for c in ac if c in "xX"),
            "refs": refs,
            "content": content,
        }
    return slices


def waves(deps):
    """Kahn layering in O(V+E). Returns (list_of_waves, leftover_nodes)."""
    indegree = {n: len(set(d)) for n, d in deps.items()}
    dependents = {n: [] for n in deps}
    for n, prerequisites in deps.items():
        for p in set(prerequisites):
            dependents[p].append(n)
    layer = sorted(n for n, k in indegree.items() if k == 0)
    out = []
    while layer:
        out.append(layer)
        released = []
        for n in layer:
            for m in dependents[n]:
                indegree[m] -= 1
                if indegree[m] == 0:
                    released.append(m)
        layer = sorted(released)
    return out, sorted(n for n, k in indegree.items() if k > 0)


def find_cycle(deps, nodes):
    """One concrete cycle among nodes, written prerequisite -> dependent."""
    left = set(nodes)
    dependents = {n: {m for m in left if n in deps[m]} for n in left}
    queue = [n for n in left if not dependents[n]]
    while queue:  # discard nodes that no remaining node depends on
        n = queue.pop()
        left.discard(n)
        for p in deps[n]:
            if p in left and n in dependents[p]:
                dependents[p].discard(n)
                if not dependents[p]:
                    queue.append(p)
    if not left:
        return sorted(nodes)
    walk, seen = [], {}
    cur = min(left)
    while cur not in seen:  # walk back through prerequisites until a repeat
        seen[cur] = len(walk)
        walk.append(cur)
        cur = min(p for p in deps[cur] if p in left)
    cycle = walk[seen[cur] :][::-1]
    return cycle + cycle[:1]


def ancestors_of(node, deps, memo):
    """All Slices that node depends on, directly or indirectly (DAG only)."""
    if node not in memo:
        found = set()
        for d in deps[node]:
            found.add(d)
            found |= ancestors_of(d, deps, memo)
        memo[node] = found
    return memo[node]


def check_redundant_dependencies(dep_map, warn):
    """Warn about Dependencies already implied through another Dependency."""
    memo = {}
    for sid, ds in dep_map.items():
        for d in ds:
            others = [o for o in ds if o != d]
            if any(d in ancestors_of(o, dep_map, memo) for o in others):
                warn(f"{sid}: Dependency {d} is implied through another Dependency")


def check_header(text, err):
    """Validate the plan header fields."""
    head = text.split("\n## ", 1)[0]
    meta = dict(
        re.findall(
            r"^> (?:\*\*)?([A-Za-z ]+?):(?:\*\*)? (.+?)\s*$",
            head,
            re.MULTILINE,
        )
    )
    for k in ("Source", "Mode", "Created", "Last synced"):
        if k not in meta:
            err(f"Header: missing '{k}'")
    if meta.get("Mode") not in (None, "Flat", "Recursive"):
        err(f"Header: Mode must be Flat or Recursive, found '{meta['Mode']}'")
    for k in ("Created", "Last synced"):
        if k in meta and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta[k]):
            err(f"Header: '{k}' must be YYYY-MM-DD, found '{meta[k]}'")


def check_slice_ids(slices, body, err, warn):
    """Check Slice IDs for duplicates and listing order."""
    ids = re.findall(r"^### (S\d+) · .+$", body, re.MULTILINE)
    if len(set(ids)) != len(ids):
        err("Duplicate Slice IDs")
    ordered = list(slices)
    if ordered != sorted(ordered, key=lambda s: int(s[1:])):
        warn("Slices are not listed in ID order")


def check_references(text, err):
    """Validate the Work Item References table and return its IDs."""
    wi = section(text, "Work Item") or ""
    rows = [
        (
            m.group(1),
            m.group(2).strip(),
            m.group(3).strip(),
            m.group(4).strip(),
        )
        for m in re.finditer(
            r"^\|\s*(R\d+)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*"
            r"\|\s*([^|]*?)\s*\|\s*$",
            wi,
            re.MULTILINE,
        )
    ]
    ref_ids = {r[0] for r in rows}
    if len(ref_ids) != len(rows):
        err("References: duplicate Reference IDs")
    for r in rows:
        if not all(c.strip() for c in r[1:]):
            err(f"References: {r[0]} has an empty Document, Location or Defines cell")
    if "**References:**" in wi and not rows:
        err("References: heading present but no Reference row found")
    return ref_ids


def check_slice_fields(sid, s, err):
    """Validate one Slice's fields and required sections."""
    if s["status"] not in STATUSES:
        err(f"{sid}: invalid Status '{s['status']}'")
    if s["gran"] not in ("Atomic", "Coarse"):
        err(f"{sid}: invalid Granularity '{s['gran']}'")
    has_reason = "Coarse reason" in s["fields"]
    if s["gran"] == "Coarse" and not has_reason:
        err(f"{sid}: Coarse Slice needs a 'Coarse reason' row")
    if s["gran"] == "Atomic" and has_reason:
        err(f"{sid}: Atomic Slice must not have a 'Coarse reason' row")
    if "Depends on" not in s["fields"]:
        err(f"{sid}: missing 'Depends on'")
    for sec in REQUIRED_SECTIONS:
        if f"**{sec}:**" not in s["content"]:
            err(f"{sid}: missing section '{sec}'")


def check_slice_criteria(sid, s, err, warn):
    """Validate one Slice's acceptance criteria."""
    if s["ac_total"] == 0:
        err(f"{sid}: no acceptance criteria")
    if s["gran"] == "Atomic" and s["ac_total"] > MAX_ATOMIC_CRITERIA:
        warn(
            f"{sid}: Atomic Slice has {s['ac_total']} acceptance criteria (> {MAX_ATOMIC_CRITERIA})"
        )


def check_slice_dependencies(sid, s, slices, err):
    """Validate Dependency entries and return them without duplicates."""
    deps = list(dict.fromkeys(s["deps"]))
    duplicates = [d for d in deps if s["deps"].count(d) > 1]
    if duplicates:
        labels = ", ".join(d.removeprefix("?") for d in duplicates)
        err(f"{sid}: duplicate Dependency entries: {labels}")
    for d in deps:
        if d.startswith("?"):
            err(f"{sid}: unreadable Dependency entry '{d[1:]}'")
        elif d == sid:
            err(f"{sid}: depends on itself")
        elif d not in slices:
            err(f"{sid}: depends on unknown Slice {d}")
    return deps


def check_slice_references(sid, s, ref_ids, err, warn):
    """Validate one Slice's References against the table and sections."""
    for r in s["refs"]:
        if r not in ref_ids:
            err(f"{sid}: Reference {r} is not in the Work Item References table")
    for line in re.findall(
        r"^- (R\d+.*)$",
        block(s["content"], "References"),
        re.MULTILINE,
    ):
        if "§" not in line:
            warn(f"{sid}: reference '{line[:40]}' names no section (§)")


def check_slices(slices, ref_ids, err, warn):
    """Validate every Slice's fields, dependencies and references."""
    for sid, s in slices.items():
        check_slice_fields(sid, s, err)
        check_slice_criteria(sid, s, err, warn)
        s["deps"] = check_slice_dependencies(sid, s, slices, err)
        check_slice_references(sid, s, ref_ids, err, warn)


def check_status(slices, dep_map, err):
    """Validate status invariants against unfinished Dependencies."""
    for sid, s in slices.items():
        unfinished = [d for d in dep_map[sid] if slices[d]["status"] != "DONE"]
        if s["status"] == "BLOCKED" and not unfinished:
            err(f"{sid}: BLOCKED but every Dependency is DONE (should be READY)")
        if s["status"] == "READY" and unfinished:
            err(
                f"{sid}: READY but {', '.join(unfinished)} not DONE (should be BLOCKED)"
            )
        if s["status"] in ("IN-PROGRESS", "DONE") and unfinished:
            err(f"{sid}: {s['status']} while {', '.join(unfinished)} not DONE")
        if s["status"] == "DONE" and s["ac_done"] != s["ac_total"]:
            err(
                f"{sid}: DONE but {s['ac_total'] - s['ac_done']} acceptance criteria unchecked"
            )


def check_graph(text, slices, dep_map, err):
    """Validate Dependency Graph edges, classes and node set."""
    graph = section(text, "Dependency Graph") or ""
    edges = set(re.findall(r"\b(S\d+)\s*-->\s*(S\d+)\b", graph))
    expected = {(d, sid) for sid, ds in dep_map.items() for d in ds}
    for e in sorted(expected - edges):
        err(f"Graph: missing edge {e[0]} --> {e[1]}")
    for e in sorted(edges - expected):
        err(f"Graph: edge {e[0]} --> {e[1]} is not in any 'Depends on'")
    classes = dict(re.findall(r"^\s*class (S\d+) (\w+)\s*$", graph, re.MULTILINE))
    for sid, s in slices.items():
        want = CLASS_OF.get(s["status"])
        if classes.get(sid) != want:
            err(f"Graph: {sid} has class '{classes.get(sid)}', expected '{want}'")
    nodes = set(re.findall(r"^\s*(S\d+)\[", graph, re.MULTILINE))
    if nodes != set(slices):
        err("Graph: node set differs from the Slice set")


def check_execution_order(text, computed, leftover, err):
    """Validate the Execution Order table against the computed Waves."""
    eo = section(text, "Execution Order") or ""
    found = []
    for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*([^|]*?)\s*\|\s*$", eo, re.MULTILINE):
        waves_in_row = sorted(re.findall(r"\bS\d+\b(?= ·)", m.group(2)))
        found.append((int(m.group(1)), waves_in_row))
    found.sort()
    want_waves = [(i + 1, w) for i, w in enumerate(computed)]
    if not leftover and found != want_waves:
        err(f"Execution Order {found} differs from computed Waves {want_waves}")


def check_progress(text, slices, err):
    """Validate the Progress counts against the Slice data."""
    prog = section(text, "Progress") or ""
    row = [
        m.groups()
        for m in re.finditer(
            r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|"
            r"\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*$",
            prog,
            re.MULTILINE,
        )
    ]
    if not row:
        err("Progress: counts row not found")
        return
    got = list(map(int, row[0]))
    sl = slices.values()
    want = (
        [len(slices)]
        + [sum(1 for s in sl if s["status"] == st) for st in STATUSES]
        + [sum(1 for s in sl if s["gran"] == g) for g in ("Atomic", "Coarse")]
    )
    if got != want:
        err(f"Progress {got} differs from computed {want}")


def check_reference_usage(slices, ref_ids, warn):
    """Warn about registered References that no Slice uses."""
    used = {r for s in slices.values() for r in s["refs"]}
    for r in sorted(ref_ids - used):
        warn(f"References: {r} is registered but no Slice uses it")


def check_document_sections(text, err, warn):
    """Check Slicing Log, Status Rules and leftover artifacts."""
    log = section(text, "Slicing Log")
    if not log or not re.search(
        r"^\|\s*\d+\s*\|\s*\d{4}-\d{2}-\d{2}\s*\|", log, re.MULTILINE
    ):
        err("Slicing Log: no valid row found")

    if section(text, "Status Rules") is None:
        err("Missing '## Status Rules' section")

    if "<!--" in text:
        warn("Template comments remain in the file")
    no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    no_code = re.sub(r"`[^`\n]*`", "", no_code)
    ph = re.findall(r"<[A-Z][^<>\n]*>", no_code)
    if ph:
        warn("Possible leftover placeholders: " + ", ".join(sorted(set(ph))[:5]))


def main(path):
    """Validate the plan file at path and return the process exit code."""
    errors, warnings = [], []
    err, warn = errors.append, warnings.append
    text = Path(path).read_text(encoding="utf-8")

    check_header(text, err)

    body = section(text, "Slices")
    if body is None:
        err("Missing '## Slices' section")
        return report(errors, warnings)
    slices = parse_slices(body)
    if not slices:
        err("No Slice found (expected headings '### S01 · Title')")
        return report(errors, warnings)

    check_slice_ids(slices, body, err, warn)
    ref_ids = check_references(text, err)
    check_slices(slices, ref_ids, err, warn)

    dep_map = {
        sid: [d for d in s["deps"] if d in slices and d != sid]
        for sid, s in slices.items()
    }

    computed, leftover = waves(dep_map)
    if leftover:
        err("Dependency cycle: " + " -> ".join(find_cycle(dep_map, leftover)))
    else:
        check_redundant_dependencies(dep_map, warn)

    check_status(slices, dep_map, err)
    check_graph(text, slices, dep_map, err)
    check_execution_order(text, computed, leftover, err)
    check_progress(text, slices, err)
    check_reference_usage(slices, ref_ids, warn)
    check_document_sections(text, err, warn)

    return report(errors, warnings, len(slices), len(computed))


def report(errors, warnings, n_slices=0, n_waves=0):
    """Print findings and summary, then return the process exit code."""
    for e in errors:
        print("ERROR:  " + e)
    for w in warnings:
        print("WARN:   " + w)
    if not errors:
        print(f"OK: {n_slices} Slices, {n_waves} Waves, {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != EXPECTED_ARGS:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
