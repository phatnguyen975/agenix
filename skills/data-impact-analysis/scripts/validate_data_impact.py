#!/usr/bin/env python3
"""Validate a completed Data Impact Document against the skill template.

Usage:
    python scripts/validate_data_impact.py <data-impact-file.md>

Exit codes:
    0  No structural findings
    1  One or more validation findings
    2  Usage, file, or decoding error

This is a structural/cross-reference check, not proof that the design is correct,
that a query is performant, or that Mermaid diagrams render. The unfilled template
is expected to fail because it contains prompts/placeholders.
"""

from __future__ import annotations

import re
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple

SECTIONS = [
    "1. Overview",
    "2. Data Model Changes",
    "3. Entity Access Map",
    "4. Data Flow",
    "5. Access Patterns & Indexing",
    "6. Business Constraints",
    "7. State Transition Model",
    "8. Cross-cutting Concerns",
    "9. Design Decisions",
]

CHANGE_KINDS = {
    "Add entity",
    "Modify entity",
    "Remove entity",
    "Add field",
    "Modify field",
    "Remove field",
    "Rename",
    "Add relationship",
    "Modify relationship",
    "Remove relationship",
    "Add index",
    "Modify index",
    "Remove index",
    "Add constraint",
    "Modify constraint",
    "Remove constraint",
    "Modify key design",
    "Configure retention/TTL",
    "Other structural change",
}
CLASSIFICATIONS = {"Additive", "Breaking"}
ACCESS_ACTIONS = {"Create", "Read", "Update", "Delete"}
ID_RE = re.compile(r"\b(SRC|OP|AP|DMC)-(\d+)\b")
PLACEHOLDER_RE = re.compile(r"<[^>\n]+>")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^ {0,3}## (.+?)\s*#*\s*$")
DMC_HEADING_RE = re.compile(r"^###\s+(DMC-\d{2,})(?:\s*[—–:-]\s*(.*))?\s*$")
OP_HEADING_RE = re.compile(r"^###\s+(OP-\d{2,})(?:\s*[—–:-]\s*(.*))?\s*$")


class Fence(NamedTuple):
    language: str
    body: str
    start_line: int
    end_line: int


class DocumentSections(NamedTuple):
    names: list[str]
    masked_bodies: dict[str, str]
    raw_bodies: dict[str, str]
    duplicated_names: list[str]


def _normalize(text: str) -> str:
    return text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")


def mask_fenced_blocks(text: str) -> tuple[str, list[Fence], bool]:
    """Blank fenced-code lines, preserving line count, and return discovered fences."""
    lines = text.split("\n")
    masked = list(lines)
    fences: list[Fence] = []
    active: tuple[str, str, int, list[str]] | None = None
    unclosed = False

    for index, line in enumerate(lines):
        if active is None:
            match = FENCE_OPEN_RE.match(line)
            if not match:
                continue
            marker, info = match.group(1), match.group(2).strip()
            # A backtick fence's info string cannot itself contain a backtick.
            if marker.startswith("`") and "`" in info:
                continue
            active = (marker, info, index, [])
            masked[index] = ""
            continue

        marker, info, start, body_lines = active
        close = re.match(r"^ {0,3}(`{3,}|~{3,})\s*$", line)
        masked[index] = ""
        if (
            close
            and close.group(1)[0] == marker[0]
            and len(close.group(1)) >= len(marker)
        ):
            language = info.split(maxsplit=1)[0].lower() if info else ""
            fences.append(Fence(language, "\n".join(body_lines), start + 1, index + 1))
            active = None
        else:
            body_lines.append(line)

    if active is not None:
        marker, info, start, body_lines = active
        language = info.split(maxsplit=1)[0].lower() if info else ""
        fences.append(Fence(language, "\n".join(body_lines), start + 1, len(lines)))
        unclosed = True

    return "\n".join(masked), fences, unclosed


def parse_sections(masked_text: str, raw_text: str) -> DocumentSections:
    """Parse level-2 headings outside fences and preserve each corresponding raw body."""
    masked_lines = masked_text.split("\n")
    raw_lines = raw_text.split("\n")
    headings: list[tuple[str, int]] = []
    for idx, line in enumerate(masked_lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append((match.group(1).strip(), idx))

    names = [name for name, _ in headings]
    masked_bodies: dict[str, str] = {}
    raw_bodies: dict[str, str] = {}
    duplicates: list[str] = []
    for position, (name, start) in enumerate(headings):
        end = (
            headings[position + 1][1]
            if position + 1 < len(headings)
            else len(masked_lines)
        )
        if name in masked_bodies:
            duplicates.append(name)
            continue
        masked_bodies[name] = "\n".join(masked_lines[start + 1 : end])
        raw_bodies[name] = "\n".join(raw_lines[start + 1 : end])

    return DocumentSections(names, masked_bodies, raw_bodies, duplicates)


def _cell_split(line: str) -> list[str] | None:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    if stripped.endswith("\\|"):
        return None
    cells = re.split(r"(?<!\\)\|", stripped[1:-1])
    return [cell.strip().replace(r"\|", "|") for cell in cells]


def _is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(
        not cell or re.fullmatch(r":?-{3,}:?", cell) for cell in cells
    )


def table_rows(body: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in body.split("\n"):
        cells = _cell_split(line)
        if cells is None or _is_separator_row(cells):
            continue
        rows.append(cells)
    return rows


def _norm_header(cells: Iterable[str]) -> tuple[str, ...]:
    return tuple(re.sub(r"\s+", " ", cell.strip()).casefold() for cell in cells)


def find_table(
    body: str, expected_header: list[str]
) -> tuple[list[str], list[list[str]]] | None:
    """Find one contiguous Markdown table whose header matches expected_header exactly."""
    lines = body.split("\n")
    target = _norm_header(expected_header)
    for index, line in enumerate(lines):
        header = _cell_split(line)
        if header is None or _norm_header(header) != target:
            continue
        data: list[list[str]] = []
        cursor = index + 1
        while cursor < len(lines):
            candidate = _cell_split(lines[cursor])
            if candidate is None:
                break
            if _is_separator_row(candidate):
                cursor += 1
                continue
            data.append(candidate)
            cursor += 1
        return header, data
    return None


def _subsections(
    raw_body: str, masked_body: str, heading_regex: re.Pattern[str]
) -> list[tuple[str, str, str]]:
    """Return (heading, raw subsection body, masked subsection body)."""
    raw_lines = raw_body.split("\n")
    masked_lines = masked_body.split("\n")
    headings: list[tuple[str, int]] = []
    for idx, line in enumerate(masked_lines):
        match = heading_regex.match(line)
        if match:
            headings.append((match.group(1), idx))
    out: list[tuple[str, str, str]] = []
    for i, (name, start) in enumerate(headings):
        end = headings[i + 1][1] if i + 1 < len(headings) else len(masked_lines)
        out.append(
            (
                name,
                "\n".join(raw_lines[start + 1 : end]),
                "\n".join(masked_lines[start + 1 : end]),
            )
        )
    return out


FIELD_LABELS = [
    "Source(s)",
    "Why",
    "Classification rationale",
    "Current definition",
    "Proposed definition",
    "Migration and rollout",
    "Affected consumers",
    "Current-state storage and validation",
    "Invalid transition handling",
    "Concurrency control",
    "History",
]


def _label_content(block: str, label: str) -> str | None:
    # Section labels are bold Markdown fields at the beginning of a line.
    pattern = re.compile(rf"(?m)^\s*(?:-\s+)?\*\*{re.escape(label)}:\*\*\s*(.*)$")
    match = pattern.search(block)
    if not match:
        return None
    content_lines = [match.group(1)]
    next_label = re.compile(
        r"^\s*(?:-\s+)?\*\*(?:"
        + "|".join(re.escape(item) for item in FIELD_LABELS)
        + r"):\*\*"
    )
    for line in block[match.end() :].splitlines():
        if next_label.match(line):
            break
        if re.match(r"^###\s+", line):
            break
        content_lines.append(line)
    return "\n".join(content_lines).strip()


def _ids(value: str, prefix: str | None = None) -> set[str]:
    matches = {f"{kind}-{number}" for kind, number in ID_RE.findall(value)}
    if prefix:
        return {item for item in matches if item.startswith(prefix + "-")}
    return matches


def _parse_ref_list(
    value: str, prefix: str, allow_none: bool = True
) -> list[str] | None:
    text = value.strip()
    if allow_none and text.casefold().startswith("none"):
        return []
    if not text:
        return None
    # IDs may be surrounded by Markdown code ticks; only comma-separated IDs are supported.
    pieces = [piece.strip().strip("`") for piece in text.split(",")]
    if not pieces or any(
        not re.fullmatch(rf"{prefix}-\d{{2,}}", piece) for piece in pieces
    ):
        return None
    return pieces


def _nonempty_data_rows(rows: list[list[str]]) -> list[list[str]]:
    return [row for row in rows if any(cell.strip() for cell in row)]


def _is_none_statement(body: str) -> bool:
    """True for a standalone None declaration, optionally followed by its rationale."""
    return bool(
        re.match(r"^\s*None(?:\s*(?:—|–|:|-).*)?\s*$", body, re.IGNORECASE | re.DOTALL)
    )


def _find_dmc_blocks(changes_body: str, changes_masked: str) -> list[tuple[str, str]]:
    raw_lines = changes_body.split("\n")
    masked_lines = changes_masked.split("\n")
    starts: list[tuple[str, int]] = []
    for idx, line in enumerate(masked_lines):
        match = DMC_HEADING_RE.match(line)
        if match:
            starts.append((match.group(1), idx))
    result: list[tuple[str, str]] = []
    for i, (dmc_id, start) in enumerate(starts):
        end = starts[i + 1][1] if i + 1 < len(starts) else len(raw_lines)
        result.append((dmc_id, "\n".join(raw_lines[start:end])))
    return result


def _add_table_finding(
    findings: list[str],
    body: str,
    expected_header: list[str],
    section_name: str,
    required: bool = True,
) -> tuple[list[str], list[list[str]]] | None:
    table = find_table(body, expected_header)
    if table is None and required:
        findings.append(
            f"Section '{section_name}' lacks a table with header: {' | '.join(expected_header)}"
        )
    return table


def _check_source_references(
    value: str, source_ids: set[str], findings: list[str], context: str
) -> None:
    used = _ids(value, "SRC")
    if not used:
        findings.append(f"{context} must cite at least one defined SRC-xx ID")
    for source_id in sorted(used - source_ids):
        findings.append(f"{context} references undefined {source_id}")


def validate(text: str) -> list[str]:
    """Return all structural/cross-reference validation findings."""
    findings: list[str] = []
    text = _normalize(text)
    original_lines = text.split("\n")
    masked_text, fences, unclosed = mask_fenced_blocks(text)

    if unclosed:
        findings.append("Unclosed fenced code block")

    # Validate the title separately; template prompts are not valid completed output.
    title_line = next((line for line in original_lines if line.strip()), "")
    if not re.fullmatch(r"#\s+Data Impact:\s+\S.*", title_line.strip()):
        findings.append("Document must start with '# Data Impact: <feature name>'")
    if PLACEHOLDER_RE.search(INLINE_CODE_RE.sub("", title_line)):
        findings.append("Title contains an unresolved placeholder")

    sections = parse_sections(masked_text, text)
    if sections.names != SECTIONS:
        findings.append(
            f"Top-level sections must appear exactly once and in order: {SECTIONS}. Found: {sections.names}"
        )
    for duplicate in sorted(set(sections.duplicated_names)):
        findings.append(f"Top-level section '{duplicate}' appears more than once")

    for section_name in SECTIONS:
        if section_name not in sections.masked_bodies:
            continue
        body = sections.masked_bodies[section_name]
        if not body.strip():
            findings.append(
                f"Section '{section_name}' is empty; use None only when allowed"
            )

    # Placeholders are prohibited outside code and in Mermaid diagrams. Other fenced code
    # may legitimately contain generic syntax, so it is not scanned by this rule.
    code_free = INLINE_CODE_RE.sub("", masked_text)
    for match in PLACEHOLDER_RE.finditer(code_free):
        findings.append(f"Unresolved placeholder outside code: {match.group(0)[:80]}")
    for fence in fences:
        if fence.language == "mermaid":
            for match in PLACEHOLDER_RE.finditer(fence.body):
                findings.append(
                    f"Unresolved placeholder in Mermaid diagram at line {fence.start_line}: {match.group(0)[:80]}"
                )

    # Even when section structure is malformed, continue with any sections that can be checked.
    bodies = sections.masked_bodies
    raw_bodies = sections.raw_bodies
    overview = bodies.get(SECTIONS[0], "")
    changes = bodies.get(SECTIONS[1], "")
    access_map = bodies.get(SECTIONS[2], "")
    data_flow = bodies.get(SECTIONS[3], "")
    patterns = bodies.get(SECTIONS[4], "")
    constraints = bodies.get(SECTIONS[5], "")
    states = bodies.get(SECTIONS[6], "")
    cross_cutting = bodies.get(SECTIONS[7], "")
    decisions = bodies.get(SECTIONS[8], "")

    # Source register and traceability.
    source_table = _add_table_finding(
        findings,
        overview,
        [
            "Source ID",
            "Source type and location",
            "Relevant passage / requirement",
            "Evidence status",
        ],
        SECTIONS[0],
    )
    source_ids: set[str] = set()
    if source_table:
        _, rows = source_table
        rows = _nonempty_data_rows(rows)
        for row in rows:
            if len(row) != 4:
                findings.append(f"Source register row has {len(row)} cells; expected 4")
                continue
            source_id = row[0]
            if not re.fullmatch(r"SRC-\d{2,}", source_id):
                findings.append(f"Invalid Source ID '{source_id}' in Source register")
            elif source_id in source_ids:
                findings.append(
                    f"{source_id} is defined more than once in Source register"
                )
            else:
                source_ids.add(source_id)
            if any(not cell.strip() for cell in row[1:]):
                findings.append(
                    f"{source_id or 'Source'} has an empty required source-register cell"
                )
            if row[3].strip().casefold() not in {
                "confirmed fact",
                "user-approved assumption",
                "inference",
            }:
                findings.append(
                    f"{source_id} has invalid Evidence status '{row[3]}'; use Confirmed fact, user-approved assumption, or inference"
                )
        if not source_ids:
            findings.append("Source register defines no SRC-xx source")

    overview_subsections = _subsections(
        raw_bodies.get(SECTIONS[0], ""),
        overview,
        re.compile(r"^###\s+(.+?)\s*$"),
    )
    assumptions_section = next(
        (
            item
            for item in overview_subsections
            if item[0].strip() == "Assumptions and unknowns"
        ),
        None,
    )
    if assumptions_section is None:
        findings.append("Overview lacks '### Assumptions and unknowns'")
    else:
        _, _, masked_assumptions = assumptions_section
        assumptions_table = None
        if not _is_none_statement(masked_assumptions):
            assumptions_table = _add_table_finding(
                findings,
                masked_assumptions,
                [
                    "Item",
                    "Status (Approved assumption / Unknown)",
                    "Basis or missing evidence",
                    "Impact / follow-up",
                ],
                "Overview — Assumptions and unknowns",
            )
        if assumptions_table:
            _, assumption_rows = assumptions_table
            for row in _nonempty_data_rows(assumption_rows):
                if len(row) != 4:
                    findings.append(
                        f"Assumption/unknown row has {len(row)} cells; expected 4"
                    )
                    continue
                if row[1] not in {"Approved assumption", "Unknown"}:
                    findings.append(
                        f"Assumption/unknown '{row[0]}' has invalid status '{row[1]}'"
                    )
                if any(not cell.strip() for cell in [row[0], row[2], row[3]]):
                    findings.append(
                        f"Assumption/unknown '{row[0]}' has an empty required cell"
                    )

    traceability_table = _add_table_finding(
        findings,
        overview,
        ["Source ID", "Requirement / rule", "Disposition", "Open issue / consequence"],
        SECTIONS[0],
    )
    if traceability_table:
        _, rows = traceability_table
        rows = _nonempty_data_rows(rows)
        if not rows:
            findings.append("Overview has no data-requirement traceability rows")
        for row in rows:
            if len(row) != 4:
                findings.append(
                    f"Requirement traceability row has {len(row)} cells; expected 4"
                )
                continue
            if row[0] not in source_ids:
                findings.append(
                    f"Requirement traceability row references undefined {row[0]}"
                )
            if any(not cell.strip() for cell in row[1:3]):
                findings.append(
                    f"Requirement traceability row for {row[0]} lacks a requirement or disposition"
                )

    operations_table = _add_table_finding(
        findings,
        overview,
        ["Operation ID", "Operation name and trigger", "Source IDs"],
        SECTIONS[0],
    )
    operation_ids: set[str] = set()
    operation_rows: list[list[str]] = []
    if operations_table:
        _, rows = operations_table
        operation_rows = _nonempty_data_rows(rows)
        for row in operation_rows:
            if len(row) != 3:
                findings.append(f"Operations row has {len(row)} cells; expected 3")
                continue
            op_id = row[0]
            if not re.fullmatch(r"OP-\d{2,}", op_id):
                findings.append(f"Invalid Operation ID '{op_id}' in Operations table")
            elif op_id in operation_ids:
                findings.append(f"{op_id} is defined more than once in Operations")
            else:
                operation_ids.add(op_id)
            if not row[1].strip():
                findings.append(f"{op_id} has no operation name/trigger")
            refs = _parse_ref_list(row[2], "SRC", allow_none=False)
            if refs is None or not refs:
                findings.append(
                    f"{op_id} has invalid Source IDs; use comma-separated SRC-xx IDs"
                )
            else:
                for source_id in refs:
                    if source_id not in source_ids:
                        findings.append(f"{op_id} references undefined {source_id}")
    if not operation_ids:
        findings.append(
            "Overview defines no operation; a Data Impact Document requires at least one persisted-data operation"
        )

    # DMC summary and detail blocks.
    dmc_summaries: dict[str, list[str]] = {}
    dmc_summary_ids: list[str] = []
    dmc_summary_table = None
    if not _is_none_statement(changes):
        dmc_summary_table = _add_table_finding(
            findings,
            changes,
            ["DMC ID", "Change kind", "Target", "Classification", "Depends on"],
            SECTIONS[1],
        )
    if dmc_summary_table:
        _, rows = dmc_summary_table
        for row in _nonempty_data_rows(rows):
            if len(row) != 5:
                findings.append(f"DMC summary row has {len(row)} cells; expected 5")
                continue
            dmc_id, kind, target, classification, dep_text = row
            if not re.fullmatch(r"DMC-\d{2,}", dmc_id):
                findings.append(f"Invalid DMC ID '{dmc_id}' in summary table")
                continue
            dmc_summary_ids.append(dmc_id)
            if dmc_id in dmc_summaries:
                findings.append(f"{dmc_id} has more than one summary row")
            else:
                dmc_summaries[dmc_id] = row
            if kind not in CHANGE_KINDS:
                findings.append(f"{dmc_id} has invalid Change kind '{kind}'")
            if not target.strip():
                findings.append(f"{dmc_id} has an empty Target")
            if classification not in CLASSIFICATIONS:
                findings.append(
                    f"{dmc_id} has invalid Classification '{classification}'"
                )
            dep_ids = _parse_ref_list(dep_text, "DMC")
            if dep_ids is None:
                findings.append(f"{dmc_id} has invalid Depends on value '{dep_text}'")
                dep_ids = []
            for dependency in dep_ids:
                if dependency == dmc_id:
                    findings.append(f"{dmc_id} depends on itself")
                elif dependency not in dmc_summary_ids and dependency not in [
                    r[0]
                    for r in _nonempty_data_rows(rows)
                    if r and re.fullmatch(r"DMC-\d{2,}", r[0])
                ]:
                    findings.append(f"{dmc_id} depends on undefined {dependency}")

    if (
        not _is_none_statement(changes)
        and dmc_summary_table
        and not _nonempty_data_rows(dmc_summary_table[1])
    ):
        findings.append(
            "Section 2 has a DMC summary table but no DMC rows; use None if no structural change is proposed"
        )

    dmc_blocks = _find_dmc_blocks(raw_bodies.get(SECTIONS[1], ""), changes)
    dmc_block_ids = [dmc_id for dmc_id, _ in dmc_blocks]
    for dmc_id in sorted(
        {item for item in dmc_block_ids if dmc_block_ids.count(item) > 1}
    ):
        findings.append(f"{dmc_id} has more than one detail block")
    if set(dmc_summary_ids) != set(dmc_block_ids):
        findings.append(
            f"DMC summary IDs {sorted(set(dmc_summary_ids))} and detail-block IDs {sorted(set(dmc_block_ids))} differ"
        )
    if _is_none_statement(changes) and (dmc_summaries or dmc_blocks):
        findings.append(
            "Section 2 must not mix None with DMC summary rows or detail blocks"
        )

    dependency_graph: dict[str, list[str]] = {}
    all_summary_id_set = set(dmc_summary_ids)
    for dmc_id, row in dmc_summaries.items():
        dep_ids = _parse_ref_list(row[4], "DMC") or []
        dependency_graph[dmc_id] = []
        for dependency in dep_ids:
            if dependency == dmc_id:
                continue
            if dependency not in all_summary_id_set:
                findings.append(f"{dmc_id} depends on undefined {dependency}")
            else:
                dependency_graph[dmc_id].append(dependency)

    cycle = _find_cycle(dependency_graph)
    if cycle:
        findings.append("DMC dependency cycle: " + " -> ".join(cycle))

    field_table_header = [
        "Field name / path",
        "Data type / representation",
        "Nullable or required",
        "Default / generation",
        "Constraints / validation",
        "Description",
    ]
    index_table_header = [
        "Index / access-path name",
        "Kind",
        "Keys in order / partition and sort keys",
        "Unique",
        "Predicate / projection / options",
        "Supporting AP IDs",
    ]
    constraint_table_header = [
        "Constraint / validator name",
        "Rule",
        "Scope and enforcement",
    ]
    index_dmc_ids: set[str] = set()
    for dmc_id, block in dmc_blocks:
        summary = dmc_summaries.get(dmc_id)
        labels = [
            "Source(s)",
            "Why",
            "Classification rationale",
            "Current definition",
            "Proposed definition",
            "Migration and rollout",
            "Affected consumers",
        ]
        for label in labels:
            content = _label_content(block, label)
            if content is None:
                findings.append(f"{dmc_id} lacks **{label}:**")
            elif not content.strip():
                findings.append(f"{dmc_id} has an empty **{label}:**")

        src_content = _label_content(block, "Source(s)") or ""
        _check_source_references(
            src_content, source_ids, findings, f"{dmc_id} Source(s)"
        )
        if not (_label_content(block, "Why") or "").strip():
            findings.append(f"{dmc_id} Why must explain the gap")
        migration = _label_content(block, "Migration and rollout") or ""
        if summary and len(summary) == 5 and summary[3] == "Breaking":
            missing_phases = [
                phase
                for phase in ("expand", "migrate", "contract")
                if not re.search(rf"\b{phase}\b", migration, re.IGNORECASE)
            ]
            if missing_phases:
                findings.append(
                    f"{dmc_id} is Breaking but Migration and rollout lacks phases: {', '.join(missing_phases)}"
                )
            if (
                not re.search(r"\bold\b", migration, re.IGNORECASE)
                or not re.search(r"\bnew\b", migration, re.IGNORECASE)
                or not re.search(r"version|compatib", migration, re.IGNORECASE)
            ):
                findings.append(
                    f"{dmc_id} is Breaking but does not describe old/new application-version compatibility"
                )
            if migration.strip().casefold().startswith("none"):
                findings.append(
                    f"{dmc_id} is Breaking but Migration and rollout is None"
                )

        kind = summary[1] if summary and len(summary) == 5 else ""
        proposed = _label_content(block, "Proposed definition") or ""
        current = _label_content(block, "Current definition") or ""
        if re.search(r"(?m)^\*\*Alternatives considered:", block):
            findings.append(
                f"{dmc_id} contains Alternatives considered in its DMC block; keep alternatives in Section 9"
            )
        # Change-kind-specific details must be explicit enough for review.
        if kind == "Add entity":
            purpose = re.search(r"(?m)^- \*\*Entity / purpose:\*\*\s*(.+)$", proposed)
            if not purpose or purpose.group(1).strip().casefold().startswith("none"):
                findings.append(
                    f"{dmc_id} (Add entity) must state the entity name and responsibility"
                )
        if kind in {"Add relationship", "Modify relationship", "Remove relationship"}:
            relation_line = re.search(
                r"(?m)^- \*\*Keys and relationships:\*\*\s*(.+)$", proposed
            )
            if not relation_line or relation_line.group(
                1
            ).strip().casefold().startswith("none"):
                findings.append(
                    f"{dmc_id} ({kind}) must define relationship cardinality/ownership semantics"
                )
        if kind == "Configure retention/TTL":
            retention_line = re.search(
                r"(?m)^- \*\*Retention / TTL definition:\*\*\s*(.+)$", proposed
            )
            if not retention_line or retention_line.group(
                1
            ).strip().casefold().startswith("none"):
                findings.append(
                    f"{dmc_id} (Configure retention/TTL) must define the retention/expiry rule"
                )
        if kind == "Other structural change":
            other_line = re.search(
                r"(?m)^- \*\*Other structural definition:\*\*\s*(.+)$", proposed
            )
            if not other_line or other_line.group(1).strip().casefold().startswith(
                "none"
            ):
                findings.append(
                    f"{dmc_id} (Other structural change) must describe the exact structural change"
                )
        # Field changes must carry the full attribute shape in the proposed definition.
        if kind in {"Add field", "Modify field", "Add entity"}:
            table = find_table(proposed, field_table_header)
            if not table:
                findings.append(
                    f"{dmc_id} ({kind}) lacks the full field-definition table in Proposed definition"
                )
            else:
                _, field_rows = table
                populated = _nonempty_data_rows(field_rows)
                if not populated:
                    findings.append(f"{dmc_id} ({kind}) has no field definition rows")
                for row in populated:
                    if len(row) != 6:
                        findings.append(
                            f"{dmc_id} field definition row has {len(row)} cells; expected 6"
                        )
                        continue
                    for i, value in enumerate(row):
                        if not value.strip():
                            findings.append(
                                f"{dmc_id} field definition has an empty cell in column '{field_table_header[i]}'"
                            )
        if kind == "Remove field" and not re.search(
            r"(?i)(field|path|attribute)", current
        ):
            findings.append(
                f"{dmc_id} (Remove field) must identify the existing field in Current definition"
            )
        if kind == "Rename":
            rename_mapping = re.search(
                r"(?m)^- \*\*Rename / removal mapping:\*\*\s*(.+)$", proposed
            )
            if not rename_mapping or not any(
                token in rename_mapping.group(1) for token in ("→", "->", " to ")
            ):
                findings.append(
                    f"{dmc_id} (Rename) must state an explicit old-name to new-name mapping"
                )
        if kind in {"Add index", "Modify index", "Remove index", "Modify key design"}:
            definition_source = current if kind == "Remove index" else proposed
            index_table = find_table(definition_source, index_table_header)
            if not index_table:
                findings.append(
                    f"{dmc_id} ({kind}) lacks an index/access-path definition table in {'Current' if kind == 'Remove index' else 'Proposed'} definition"
                )
            elif not _nonempty_data_rows(index_table[1]):
                findings.append(
                    f"{dmc_id} ({kind}) has no index/access-path definition rows"
                )
            elif kind in {"Add index", "Modify index"}:
                for index_row in _nonempty_data_rows(index_table[1]):
                    if len(index_row) != 6 or any(
                        not cell.strip() for cell in index_row
                    ):
                        findings.append(
                            f"{dmc_id} index definition row must fill all six columns"
                        )
                    elif not _ids(index_row[5], "AP"):
                        findings.append(
                            f"{dmc_id} index definition must name supporting AP-xx IDs in its table"
                        )
            if not _ids(block, "AP"):
                findings.append(
                    f"{dmc_id} ({kind}) must identify the AP-xx pattern it serves or changes"
                )
            if kind in {"Add index", "Modify index"}:
                index_dmc_ids.add(dmc_id)
        if kind in {"Add constraint", "Modify constraint", "Remove constraint"}:
            definition_source = current if kind == "Remove constraint" else proposed
            constraint_table = find_table(definition_source, constraint_table_header)
            if not constraint_table:
                findings.append(
                    f"{dmc_id} ({kind}) lacks a constraint/validator definition table in {'Current' if kind == 'Remove constraint' else 'Proposed'} definition"
                )
            elif not _nonempty_data_rows(constraint_table[1]):
                findings.append(f"{dmc_id} ({kind}) has no constraint definition rows")
            else:
                for constraint_row in _nonempty_data_rows(constraint_table[1]):
                    if len(constraint_row) != 3 or any(
                        not cell.strip() for cell in constraint_row
                    ):
                        findings.append(
                            f"{dmc_id} constraint definition row must fill all three columns"
                        )

    # Entity Access Map.
    access_table = _add_table_finding(
        findings,
        access_map,
        ["Operation ID", "Entity / persisted structure", "Access actions"],
        SECTIONS[2],
    )
    mapped_ops: list[str] = []
    op_entity_pairs: set[tuple[str, str]] = set()
    if access_table:
        _, rows = access_table
        for row in _nonempty_data_rows(rows):
            if len(row) != 3:
                findings.append(
                    f"Entity Access Map row has {len(row)} cells; expected 3"
                )
                continue
            op_id, entity, actions_text = row
            if op_id not in operation_ids:
                findings.append(f"Entity Access Map refers to undefined {op_id}")
            mapped_ops.append(op_id)
            if not entity.strip() or entity.strip().casefold() in {"none", "unknown"}:
                findings.append(
                    f"Entity Access Map {op_id} must name a known entity/persisted structure"
                )
            pair = (op_id, entity.casefold())
            if pair in op_entity_pairs:
                findings.append(
                    f"Entity Access Map has duplicate row for {op_id} / {entity}"
                )
            op_entity_pairs.add(pair)
            actions = [action.strip() for action in actions_text.split(",")]
            if not actions_text.strip() or any(
                action not in ACCESS_ACTIONS for action in actions
            ):
                findings.append(
                    f"Entity Access Map {op_id} has invalid Access actions '{actions_text}'; use Create, Read, Update, Delete"
                )
            elif len(set(actions)) != len(actions):
                findings.append(
                    f"Entity Access Map {op_id} repeats an access action in '{actions_text}'"
                )
    for op_id in sorted(operation_ids - set(mapped_ops)):
        findings.append(f"{op_id} has no row in Entity Access Map")
    for op_id in sorted({item for item in mapped_ops if mapped_ops.count(item) > 1}):
        # Multiple entities per operation are allowed; duplicate operation rows are not.
        matching = [pair for pair in op_entity_pairs if pair[0] == op_id]
        if len(matching) != mapped_ops.count(op_id):
            continue

    # Data Flow: one detailed subsection and a Mermaid flowchart per operation.
    raw_flow = raw_bodies.get(SECTIONS[3], "")
    flow_subsections = _subsections(
        raw_flow, data_flow, re.compile(r"^###\s+(OP-\d{2,})(?:\s*[—–:-]\s*(.*))?\s*$")
    )
    flow_ids = [heading.split("\n", 1)[0].strip() for heading, _, _ in flow_subsections]
    for op_id in sorted({item for item in flow_ids if flow_ids.count(item) > 1}):
        findings.append(f"{op_id} has more than one Data Flow subsection")
    if set(flow_ids) != operation_ids:
        findings.append(
            f"Data Flow operation subsections {sorted(set(flow_ids))} do not match Operations {sorted(operation_ids)}"
        )
    required_flow_labels = [
        "Trigger and preconditions",
        "Reads",
        "Validation and branches",
        "Writes and side effects",
        "Transaction and consistency boundary",
        "Concurrency, idempotency, and retry",
    ]
    for heading, raw_block, _masked_block in flow_subsections:
        op_id = heading.split("\n", 1)[0].strip()
        for label in required_flow_labels:
            match = re.search(
                rf"(?m)^\s*-\s+\*\*{re.escape(label)}:\*\*\s*(\S.*)$", raw_block
            )
            if not match:
                findings.append(f"{op_id} lacks a non-empty '**{label}:**' field")
        mermaid_flowcharts = [
            fence
            for fence in fences
            if fence.language == "mermaid"
            and fence.start_line > 0
            and _fence_is_in_subsection(fence, raw_block)
            and re.search(
                r"(?m)^\s*(?:flowchart|graph)\s+(?:TD|TB|BT|LR|RL)\b", fence.body
            )
        ]
        # More robust local fallback for subsection-local fenced source.
        if not mermaid_flowcharts and not re.search(
            r"```mermaid\s*\n\s*(?:flowchart|graph)\s+(?:TD|TB|BT|LR|RL)\b",
            raw_block,
            re.IGNORECASE,
        ):
            findings.append(
                f"{op_id} lacks a Mermaid flowchart (flowchart/graph direction required)"
            )

    # Access patterns and index support.
    ap_header = [
        "AP ID",
        "Operation IDs",
        "Store / entity",
        "Kind",
        "Filter / lookup / write key",
        "Sort / pagination / result shape",
        "Expected frequency / scale",
        "Supporting key or index",
        "Assessment / reason",
    ]
    ap_table = _add_table_finding(findings, patterns, ap_header, SECTIONS[4])
    ap_ids: set[str] = set()
    ap_rows: list[list[str]] = []
    if ap_table:
        _, rows = ap_table
        ap_rows = _nonempty_data_rows(rows)
        for row in ap_rows:
            if len(row) != 9:
                findings.append(f"Access Pattern row has {len(row)} cells; expected 9")
                continue
            (
                ap_id,
                op_text,
                store_entity,
                kind,
                key,
                sort,
                scale,
                support,
                assessment,
            ) = row
            if not re.fullmatch(r"AP-\d{2,}", ap_id):
                findings.append(f"Invalid Access Pattern ID '{ap_id}'")
            elif ap_id in ap_ids:
                findings.append(f"{ap_id} is defined more than once")
            else:
                ap_ids.add(ap_id)
            op_refs = _parse_ref_list(op_text, "OP", allow_none=False)
            if op_refs is None or not op_refs:
                findings.append(
                    f"{ap_id} has invalid Operation IDs; use comma-separated OP-xx IDs"
                )
            else:
                for op_id in op_refs:
                    if op_id not in operation_ids:
                        findings.append(f"{ap_id} references undefined {op_id}")
            if not all(
                cell.strip()
                for cell in [store_entity, kind, key, sort, scale, support, assessment]
            ):
                findings.append(
                    f"{ap_id} has one or more empty required access-pattern cells"
                )
            if support.strip().casefold().startswith("none") and not assessment.strip():
                findings.append(f"{ap_id} has no supporting index/key and no reason")
            for dmc_id in _ids(support, "DMC"):
                if dmc_id not in all_summary_id_set:
                    findings.append(
                        f"{ap_id} supporting key/index references undefined {dmc_id}"
                    )
    if not ap_ids:
        findings.append("Section 5 defines no AP-xx access pattern")

    # A new/modified index must be linked from at least one AP row.
    for dmc_id in sorted(index_dmc_ids):
        dmc_block = next(
            (block for block_id, block in dmc_blocks if block_id == dmc_id), ""
        )
        dmc_ap_ids = _ids(dmc_block, "AP")
        matching_rows = [
            row for row in ap_rows if len(row) == 9 and dmc_id in _ids(row[7], "DMC")
        ]
        if not matching_rows:
            findings.append(
                f"{dmc_id} adds/modifies an index/key but no Access Pattern row names it as supporting key/index"
            )
        elif dmc_ap_ids and not any(
            ap_id in dmc_ap_ids for row in matching_rows for ap_id in _ids(row[0], "AP")
        ):
            findings.append(
                f"{dmc_id} index definition AP IDs do not match the AP row(s) that cite {dmc_id}"
            )

    # Business constraints.
    constraint_table = None
    if not _is_none_statement(constraints):
        constraint_table = _add_table_finding(
            findings,
            constraints,
            [
                "Constraint / rule",
                "Source IDs",
                "Entity / field path",
                "Enforcement",
                "Behavior on violation",
            ],
            SECTIONS[5],
        )
    if constraint_table:
        _, rows = constraint_table
        constraint_rows = _nonempty_data_rows(rows)
        if not constraint_rows:
            findings.append(
                "Section 6 has a constraints table but no rule rows; use None if no additional business constraints apply"
            )
        for row in constraint_rows:
            if len(row) != 5:
                findings.append(
                    f"Business Constraints row has {len(row)} cells; expected 5"
                )
                continue
            if (
                not row[0].strip()
                or not row[2].strip()
                or not row[3].strip()
                or not row[4].strip()
            ):
                findings.append("Business Constraints row has an empty required cell")
            _check_source_references(
                row[1], source_ids, findings, f"Business constraint '{row[0]}'"
            )

    # State Transition Model. None is valid only when no stateful lifecycle is relevant.
    state_subsections: list[tuple[str, str, str]] = []
    if not _is_none_statement(states):
        state_subsections = _subsections(
            raw_bodies.get(SECTIONS[6], ""),
            states,
            re.compile(r"^###\s+(.+?)\s*$"),
        )
        if not state_subsections:
            findings.append("Section 7 must contain a state subsection or exactly None")
    for state_name, raw_block, _masked_block in state_subsections:
        for label in [
            "Source(s)",
            "Current-state storage and validation",
            "Invalid transition handling",
            "Concurrency control",
            "History",
        ]:
            content = _label_content(raw_block, label)
            if content is None or not content.strip():
                findings.append(
                    f"State model '{state_name}' lacks a non-empty '**{label}:**' field"
                )
            elif label == "Source(s)":
                _check_source_references(
                    content,
                    source_ids,
                    findings,
                    f"State model '{state_name}' Source(s)",
                )
        state_table = _add_table_finding(
            findings,
            _mask_fenced(raw_block),
            ["State value", "Meaning", "Initial?", "Terminal?", "Source IDs"],
            f"State model '{state_name}'",
        )
        state_values: set[str] = set()
        if state_table:
            _, rows = state_table
            for row in _nonempty_data_rows(rows):
                if len(row) != 5:
                    findings.append(
                        f"State model '{state_name}' row has {len(row)} cells; expected 5"
                    )
                    continue
                value, meaning, initial, terminal, srcs = row
                if value in state_values:
                    findings.append(
                        f"State model '{state_name}' repeats state '{value}'"
                    )
                state_values.add(value)
                if not value.strip() or not meaning.strip():
                    findings.append(
                        f"State model '{state_name}' has an empty state value or meaning"
                    )
                if initial.casefold() not in {
                    "yes",
                    "no",
                } or terminal.casefold() not in {"yes", "no"}:
                    findings.append(
                        f"State '{value}' must use Yes/No for Initial? and Terminal?"
                    )
                _check_source_references(srcs, source_ids, findings, f"State '{value}'")
        transition_table = _add_table_finding(
            findings,
            _mask_fenced(raw_block),
            [
                "From state",
                "Event / operation",
                "Guard / precondition",
                "To state",
                "Data effects",
                "Actor",
                "Source IDs",
            ],
            f"State model '{state_name}'",
        )
        if transition_table:
            _, rows = transition_table
            transitions = _nonempty_data_rows(rows)
            if not transitions:
                findings.append(f"State model '{state_name}' has no transition rows")
            for row in transitions:
                if len(row) != 7:
                    findings.append(
                        f"State transition row has {len(row)} cells; expected 7"
                    )
                    continue
                from_state, event, guard, to_state, effects, actor, srcs = row
                if from_state not in state_values:
                    findings.append(
                        f"State model '{state_name}' transition has undefined From state '{from_state}'"
                    )
                if to_state not in state_values:
                    findings.append(
                        f"State model '{state_name}' transition has undefined To state '{to_state}'"
                    )
                if any(not cell.strip() for cell in [event, guard, effects, actor]):
                    findings.append(
                        f"State model '{state_name}' transition {from_state} -> {to_state} has an empty required cell"
                    )
                _check_source_references(
                    srcs,
                    source_ids,
                    findings,
                    f"State transition {from_state} -> {to_state}",
                )
        if not re.search(
            r"```mermaid\s*\n\s*stateDiagram(?:-v2)?\b", raw_block, re.IGNORECASE
        ):
            findings.append(
                f"State model '{state_name}' lacks a Mermaid stateDiagram/stateDiagram-v2 block"
            )

    # Cross-cutting concerns: each named subsection should contain a considered result.
    expected_cross_topics = [
        "Volume & growth",
        "Sensitive data & access",
        "Retention & deletion",
        "Consistency & duplication",
        "Auditing, idempotency & replay",
        "Operational reliability",
    ]
    cross_headings = [
        match.group(1).strip()
        for line in cross_cutting.split("\n")
        if (match := re.match(r"^###\s+(.+?)\s*$", line))
    ]
    for topic in expected_cross_topics:
        if topic not in cross_headings:
            findings.append(f"Section 8 lacks subsection '### {topic}'")
    raw_cross = raw_bodies.get(SECTIONS[7], "")
    cross_sections = _subsections(
        raw_cross, cross_cutting, re.compile(r"^###\s+(.+?)\s*$")
    )
    for topic, _, masked_topic in cross_sections:
        if not masked_topic.strip():
            findings.append(
                f"Cross-cutting subsection '{topic}' is empty; record None or Unknown with reason"
            )

    # Design decisions.
    if not _is_none_statement(decisions):
        decision_table = _add_table_finding(
            findings,
            decisions,
            [
                "Decision ID / topic",
                "Related IDs",
                "Selected approach",
                "Rationale and trade-offs",
                "Alternatives considered and why rejected",
                "Approval / assumption status",
            ],
            SECTIONS[8],
        )
        if decision_table:
            _, rows = decision_table
            decision_rows = _nonempty_data_rows(rows)
            if not decision_rows:
                findings.append(
                    "Section 9 has a decisions table but no decision rows; use None if there are no material decisions"
                )
            for row in decision_rows:
                if len(row) != 6:
                    findings.append(
                        f"Design Decisions row has {len(row)} cells; expected 6"
                    )
                    continue
                if any(not cell.strip() for cell in row):
                    findings.append(
                        f"Design Decision '{row[0]}' has an empty required cell; use None with reason where applicable"
                    )

    # Global cross-reference validation. Definitions are gathered from canonical tables/blocks,
    # while every mention (including diagram labels) is checked for dangling identifiers.
    defined = {
        "SRC": source_ids,
        "OP": operation_ids,
        "AP": ap_ids,
        "DMC": set(dmc_block_ids),
    }
    all_refs = _ids(text)
    for ref in sorted(all_refs):
        prefix = ref.split("-", 1)[0]
        if ref not in defined.get(prefix, set()):
            findings.append(f"{ref} is referenced but has no canonical definition")

    return _deduplicate(findings)


def _mask_fenced(text: str) -> str:
    masked, _, _ = mask_fenced_blocks(text)
    return masked


def _fence_is_in_subsection(fence: Fence, subsection_raw: str) -> bool:
    """Return whether a discovered fence body belongs to a subsection."""
    # This is a best-effort filter; the caller also has a subsection-local fallback.
    return fence.body in subsection_raw


def _find_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        state[node] = 1
        stack.append(node)
        for neighbor in graph.get(node, []):
            if state.get(neighbor) == 1:
                return stack[stack.index(neighbor) :] + [neighbor]
            if neighbor not in state:
                cycle = visit(neighbor)
                if cycle:
                    return cycle
        stack.pop()
        state[node] = 2
        return None

    for node in graph:
        if node not in state:
            cycle = visit(node)
            if cycle:
                return cycle
    return None


def _deduplicate(findings: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for finding in findings:
        if finding not in seen:
            result.append(finding)
            seen.add(finding)
    return result


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] in {"-h", "--help"}:
        print(__doc__ or "")
        return 0
    if len(argv) != 2:
        print(
            "Usage: python scripts/validate_data_impact.py <data-impact-file.md>",
            file=sys.stderr,
        )
        return 2

    path = Path(argv[1])
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as error:
        print(f"ERROR: cannot read {path}: {error}", file=sys.stderr)
        return 2

    findings = validate(text)
    for finding in findings:
        print(f"FINDING: {finding}")
    print(f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
