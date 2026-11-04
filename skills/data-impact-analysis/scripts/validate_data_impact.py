#!/usr/bin/env python3
"""Check Data Impact Document structure and cross-references.

Usage:
    python scripts/validate_data_impact.py <data-impact-file.md>

Exit codes:
    0: no structural findings
    1: validation findings
    2: usage, file, or decoding error

The validator intentionally does not enforce display wording, casing, or business
semantics. It checks numbered sections, table shape, IDs, references, and diagrams.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

SECTION_NUMBERS = tuple(range(1, 10))
ID_PATTERN = re.compile(r"\b(SRC|OP|AP|DMC)-(\d{2,})\b")
SECTION_PATTERN = re.compile(r"^ {0,3}##\s+(\d+)\s*[.)—–:-]?\s*(.*?)\s*#*\s*$")
SUBSECTION_PATTERN = re.compile(r"^ {0,3}###\s+(.+?)\s*#*\s*$")
FENCE_OPEN_PATTERN = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
PLACEHOLDER_PATTERN = re.compile(r"<[^>\n]+>")
INLINE_CODE_PATTERN = re.compile(r"`[^`\n]*`")


@dataclass(frozen=True)
class Fence:
    language: str
    body: str
    start_line: int


@dataclass(frozen=True)
class Table:
    header: list[str]
    rows: list[list[str]]
    start_line: int


@dataclass(frozen=True)
class Section:
    number: int
    title: str
    body: str
    raw_body: str


def normalize_newlines(text: str) -> str:
    return text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")


def split_fenced_blocks(text: str) -> tuple[str, list[Fence], bool]:
    """Mask fenced blocks while preserving line count; return parsed fences."""
    lines = text.split("\n")
    masked_lines = list(lines)
    fences: list[Fence] = []
    active_marker: str | None = None
    active_language = ""
    active_start = 0
    active_body: list[str] = []

    for index, line in enumerate(lines):
        if active_marker is None:
            match = FENCE_OPEN_PATTERN.match(line)
            if match is None:
                continue
            marker = match.group(1)
            info = match.group(2).strip()
            if marker.startswith("`") and "`" in info:
                continue
            active_marker = marker
            active_language = info.split(maxsplit=1)[0].lower() if info else ""
            active_start = index + 1
            active_body = []
            masked_lines[index] = ""
            continue

        masked_lines[index] = ""
        close = re.match(r"^ {0,3}(`{3,}|~{3,})\s*$", line)
        if (
            close is not None
            and close.group(1)[0] == active_marker[0]
            and len(close.group(1)) >= len(active_marker)
        ):
            fences.append(Fence(active_language, "\n".join(active_body), active_start))
            active_marker = None
            active_language = ""
            active_body = []
        else:
            active_body.append(line)

    unclosed = active_marker is not None
    if unclosed:
        fences.append(Fence(active_language, "\n".join(active_body), active_start))

    return "\n".join(masked_lines), fences, unclosed


def parse_sections(masked_text: str, raw_text: str) -> tuple[list[Section], list[int]]:
    masked_lines = masked_text.split("\n")
    raw_lines = raw_text.split("\n")
    headings: list[tuple[int, str, int]] = []
    for index, line in enumerate(masked_lines):
        match = SECTION_PATTERN.match(line)
        if match is None:
            continue
        headings.append((int(match.group(1)), match.group(2).strip(), index))

    sections: list[Section] = []
    for position, (number, title, start) in enumerate(headings):
        end = (
            headings[position + 1][2]
            if position + 1 < len(headings)
            else len(masked_lines)
        )
        sections.append(
            Section(
                number,
                title,
                "\n".join(masked_lines[start + 1 : end]),
                "\n".join(raw_lines[start + 1 : end]),
            )
        )

    numbers = [section.number for section in sections]
    duplicates = sorted({number for number in numbers if numbers.count(number) > 1})
    return sections, duplicates


def split_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    cells = re.split(r"(?<!\\)\|", stripped[1:-1])
    return [cell.strip().replace(r"\|", "|") for cell in cells]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(
        not cell or re.fullmatch(r":?-{3,}:?", cell) is not None for cell in cells
    )


def extract_tables(body: str) -> list[Table]:
    """Extract Markdown tables without depending on header wording or casing."""
    lines = body.split("\n")
    tables: list[Table] = []
    index = 0
    while index + 1 < len(lines):
        header = split_table_row(lines[index])
        separator = split_table_row(lines[index + 1])
        if header is None or separator is None or not is_separator_row(separator):
            index += 1
            continue
        rows: list[list[str]] = []
        cursor = index + 2
        while cursor < len(lines):
            row = split_table_row(lines[cursor])
            if row is None:
                break
            if not is_separator_row(row):
                rows.append(row)
            cursor += 1
        tables.append(Table(header, rows, index + 1))
        index = cursor
    return tables


def row_has_id(row: list[str], prefix: str, first_cell_only: bool = True) -> bool:
    values = row[:1] if first_cell_only else row
    return any(
        re.fullmatch(rf"{prefix}-\d{{2,}}", value.strip()) is not None
        for value in values
    )


def find_table_by_id(tables: list[Table], prefix: str) -> Table | None:
    for table in tables:
        if any(row_has_id(row, prefix) for row in table.rows if row):
            return table
    return None


def nonempty_rows(table: Table) -> list[list[str]]:
    return [row for row in table.rows if any(cell.strip() for cell in row)]


def is_none_statement(body: str) -> bool:
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    if len(lines) != 1:
        return False
    return re.match(r"(?i)^none(?:\s*[—–:-].*)?$", lines[0]) is not None


def ids_in(text: str, prefix: str | None = None) -> set[str]:
    found = {f"{kind}-{number}" for kind, number in ID_PATTERN.findall(text)}
    if prefix is None:
        return found
    return {item for item in found if item.startswith(f"{prefix}-")}


def ids_in_cell(text: str, prefix: str) -> list[str]:
    return sorted(ids_in(text, prefix))


def check_table_width(
    table: Table, expected: int, context: str, findings: list[str]
) -> None:
    if len(table.header) != expected:
        findings.append(
            f"{context} has {len(table.header)} columns; expected {expected}"
        )
    for row_number, row in enumerate(nonempty_rows(table), start=1):
        if len(row) != expected:
            findings.append(
                f"{context} row {row_number} has {len(row)} cells; expected {expected}"
            )


def subsection_blocks(
    raw_body: str, masked_body: str | None = None
) -> list[tuple[str, str, str]]:
    raw_lines = raw_body.split("\n")
    masked_lines = (masked_body if masked_body is not None else raw_body).split("\n")
    starts: list[tuple[str, int]] = []
    for index, line in enumerate(masked_lines):
        match = SUBSECTION_PATTERN.match(line)
        if match is not None:
            starts.append((match.group(1).strip(), index))
    blocks: list[tuple[str, str, str]] = []
    for position, (title, start) in enumerate(starts):
        end = (
            starts[position + 1][1] if position + 1 < len(starts) else len(masked_lines)
        )
        blocks.append(
            (
                title,
                "\n".join(raw_lines[start + 1 : end]),
                "\n".join(masked_lines[start + 1 : end]),
            )
        )
    return blocks


def validate(text: str) -> list[str]:
    findings: list[str] = []
    text = normalize_newlines(text)
    masked_text, fences, unclosed_fence = split_fenced_blocks(text)

    if unclosed_fence:
        findings.append("Unclosed fenced code block")

    first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if not first_line.startswith("# Data Impact:"):
        findings.append("Document title must start with '# Data Impact:'")

    sections, duplicate_sections = parse_sections(masked_text, text)
    found_numbers = [section.number for section in sections]
    if found_numbers != list(SECTION_NUMBERS):
        findings.append(
            f"Expected numbered sections 1–9 in order; found section numbers {found_numbers}"
        )
    for number in duplicate_sections:
        findings.append(f"Section number {number} appears more than once")

    section_map: dict[int, Section] = {}
    for section in sections:
        if section.number not in section_map:
            section_map[section.number] = section
        if not section.body.strip():
            findings.append(f"Section {section.number} is empty")

    # Detect unresolved prompts outside inline/fenced code and in Mermaid diagrams.
    code_free = INLINE_CODE_PATTERN.sub("", masked_text)
    for match in PLACEHOLDER_PATTERN.finditer(code_free):
        findings.append(f"Unresolved placeholder: {match.group(0)[:80]}")
    for fence in fences:
        if fence.language == "mermaid" and PLACEHOLDER_PATTERN.search(fence.body):
            findings.append(
                f"Unresolved placeholder in Mermaid diagram near line {fence.start_line}"
            )

    # Section 1: source register, requirements, and operations.
    overview = section_map.get(1)
    source_ids: set[str] = set()
    operation_ids: set[str] = set()
    if overview is not None:
        tables = extract_tables(overview.body)
        source_table = find_table_by_id(tables, "SRC")
        if source_table is None:
            findings.append(
                "Section 1 lacks a source-register table with SRC IDs in the first column"
            )
        else:
            check_table_width(source_table, 4, "Source register", findings)
            for row in nonempty_rows(source_table):
                source_id = row[0].strip() if row else ""
                if re.fullmatch(r"SRC-\d{2,}", source_id) is None:
                    findings.append(f"Invalid source definition '{source_id}'")
                elif source_id in source_ids:
                    findings.append(f"Duplicate source definition {source_id}")
                source_ids.add(source_id)
                if len(row) >= 4 and any(not cell.strip() for cell in row[1:4]):
                    findings.append(
                        f"Source row {source_id} has an empty required cell"
                    )

        source_index = tables.index(source_table) if source_table is not None else -1
        trace_table: Table | None = None
        for table in tables[source_index + 1 :]:
            if any(ids_in_cell(row[0], "SRC") for row in nonempty_rows(table) if row):
                trace_table = table
                break
        if trace_table is None:
            findings.append("Section 1 lacks a requirement-traceability table")
        else:
            check_table_width(
                trace_table, 4, "Requirement traceability table", findings
            )
            for row in nonempty_rows(trace_table):
                if not row:
                    continue
                refs = ids_in_cell(row[0], "SRC")
                if not refs:
                    findings.append(
                        "A requirement row has no SRC ID in its first column"
                    )
                for source_id in refs:
                    if source_id not in source_ids:
                        findings.append(
                            f"Requirement row references undefined {source_id}"
                        )
                if len(row) >= 3 and (not row[1].strip() or not row[2].strip()):
                    findings.append(
                        "A requirement row has an empty requirement or disposition"
                    )

        operation_table = find_table_by_id(tables, "OP")
        if operation_table is None:
            findings.append(
                "Section 1 lacks an Operations table with OP IDs in the first column"
            )
        else:
            check_table_width(operation_table, 3, "Operations table", findings)
            for row in nonempty_rows(operation_table):
                if not row:
                    continue
                operation_id = row[0].strip()
                if re.fullmatch(r"OP-\d{2,}", operation_id) is None:
                    findings.append(f"Invalid operation definition '{operation_id}'")
                elif operation_id in operation_ids:
                    findings.append(f"Duplicate operation definition {operation_id}")
                operation_ids.add(operation_id)
                if len(row) >= 3:
                    if not row[1].strip():
                        findings.append(f"{operation_id} has no operation name/trigger")
                    source_refs = ids_in_cell(row[2], "SRC")
                    if not source_refs:
                        findings.append(f"{operation_id} has no source ID")
                    for source_id in source_refs:
                        if source_id not in source_ids:
                            findings.append(
                                f"{operation_id} references undefined {source_id}"
                            )
        if not operation_ids:
            findings.append("Section 1 defines no persisted-data operation")

    # Section 2: DMC summary/detail consistency and dependency graph.
    changes = section_map.get(2)
    dmc_ids: set[str] = set()
    dependency_graph: dict[str, list[str]] = {}
    if changes is not None and not is_none_statement(changes.body):
        tables = extract_tables(changes.body)
        dmc_table = find_table_by_id(tables, "DMC")
        if dmc_table is None:
            findings.append(
                "Section 2 requires a DMC summary table or a standalone None"
            )
        else:
            check_table_width(dmc_table, 5, "DMC summary table", findings)
            for row in nonempty_rows(dmc_table):
                if len(row) != 5:
                    continue
                dmc_id = row[0].strip()
                if re.fullmatch(r"DMC-\d{2,}", dmc_id) is None:
                    findings.append(f"Invalid DMC definition '{dmc_id}'")
                    continue
                if dmc_id in dmc_ids:
                    findings.append(f"Duplicate DMC summary {dmc_id}")
                dmc_ids.add(dmc_id)
                if any(not cell.strip() for cell in row[1:4]):
                    findings.append(
                        f"{dmc_id} has an empty change kind, target, or classification"
                    )
                dependencies = ids_in_cell(row[4], "DMC")
                dependency_graph[dmc_id] = dependencies
                for dependency in dependencies:
                    if dependency == dmc_id:
                        findings.append(f"{dmc_id} depends on itself")

        dmc_blocks = subsection_blocks(changes.body)
        block_ids: list[str] = []
        for title, block, _masked_block in dmc_blocks:
            match = re.match(r"(DMC-\d{2,})\b", title)
            if match is None:
                continue
            block_id = match.group(1)
            block_ids.append(block_id)
            if not ids_in(block, "SRC"):
                findings.append(f"{block_id} has no source ID")
        for block_id in block_ids:
            if block_ids.count(block_id) > 1:
                findings.append(f"Duplicate DMC detail block {block_id}")
        if set(block_ids) != dmc_ids:
            findings.append(
                f"DMC summary/detail IDs differ: summary={sorted(dmc_ids)}, details={sorted(set(block_ids))}"
            )
        for dmc_id, dependencies in dependency_graph.items():
            for dependency in dependencies:
                if dependency not in dmc_ids:
                    findings.append(f"{dmc_id} depends on undefined {dependency}")
        cycle = find_dependency_cycle(dependency_graph)
        if cycle:
            findings.append("DMC dependency cycle: " + " -> ".join(cycle))
        if dmc_table is not None and not nonempty_rows(dmc_table):
            findings.append(
                "Section 2 has an empty DMC summary table; use None if no relevant DMC exists"
            )

    # Section 3: every operation must appear in the access map.
    access_map = section_map.get(3)
    mapped_operations: set[str] = set()
    if access_map is not None:
        table = find_table_by_id(extract_tables(access_map.body), "OP")
        if table is None:
            findings.append("Section 3 lacks an Entity Access Map table")
        else:
            check_table_width(table, 3, "Entity Access Map", findings)
            for row in nonempty_rows(table):
                if len(row) != 3:
                    continue
                operation_id = row[0].strip()
                mapped_operations.add(operation_id)
                if operation_id not in operation_ids:
                    findings.append(
                        f"Entity Access Map references undefined {operation_id}"
                    )
                if not row[1].strip() or not row[2].strip():
                    findings.append(
                        f"Entity Access Map row {operation_id} lacks structure or access action"
                    )
        for operation_id in sorted(operation_ids - mapped_operations):
            findings.append(f"{operation_id} has no Entity Access Map row")

    # Section 4: one flow subsection and one flowchart per operation.
    data_flow = section_map.get(4)
    flow_ids: list[str] = []
    if data_flow is not None:
        for title, block, _masked_block in subsection_blocks(
            data_flow.raw_body, data_flow.body
        ):
            match = re.match(r"(OP-\d{2,})\b", title)
            if match is not None:
                flow_ids.append(match.group(1))
                _, block_fences, _ = split_fenced_blocks(block)
                diagrams = [
                    fence
                    for fence in block_fences
                    if fence.language == "mermaid"
                    and re.search(
                        r"^\s*(?:flowchart|graph)\s+(?:TD|TB|BT|LR|RL)\b",
                        fence.body,
                        re.IGNORECASE | re.MULTILINE,
                    )
                ]
                if len(diagrams) != 1:
                    findings.append(
                        f"{match.group(1)} must contain exactly one Mermaid flowchart; found {len(diagrams)}"
                    )
        for operation_id in sorted(operation_ids - set(flow_ids)):
            findings.append(f"{operation_id} has no Data Flow subsection")
        for operation_id in sorted(set(flow_ids) - operation_ids):
            findings.append(f"Data Flow defines unknown operation {operation_id}")
        for operation_id in sorted(
            {item for item in flow_ids if flow_ids.count(item) > 1}
        ):
            findings.append(f"Duplicate Data Flow subsection {operation_id}")

    # Section 5: access patterns and their operation references.
    patterns = section_map.get(5)
    access_pattern_ids: set[str] = set()
    if patterns is not None and not is_none_statement(patterns.body):
        ap_table = find_table_by_id(extract_tables(patterns.body), "AP")
        if ap_table is None:
            findings.append(
                "Section 5 requires an Access Patterns table with AP IDs or a standalone None"
            )
        else:
            check_table_width(ap_table, 9, "Access Patterns table", findings)
            for row in nonempty_rows(ap_table):
                if len(row) != 9:
                    continue
                ap_id = row[0].strip()
                if re.fullmatch(r"AP-\d{2,}", ap_id) is None:
                    findings.append(f"Invalid access-pattern definition '{ap_id}'")
                elif ap_id in access_pattern_ids:
                    findings.append(f"Duplicate access-pattern definition {ap_id}")
                access_pattern_ids.add(ap_id)
                if not row[1].strip() or not row[2].strip() or not row[3].strip():
                    findings.append(
                        f"{ap_id} lacks operation, store/entity, or pattern kind"
                    )
                for operation_id in ids_in_cell(row[1], "OP"):
                    if operation_id not in operation_ids:
                        findings.append(f"{ap_id} references undefined {operation_id}")

    # Section 6: business-constraint table shape.
    constraints = section_map.get(6)
    if constraints is not None and not is_none_statement(constraints.body):
        tables = extract_tables(constraints.body)
        constraint_table = next(
            (table for table in tables if len(table.header) == 5), None
        )
        if constraint_table is None:
            findings.append(
                "Section 6 requires a five-column Business Constraints table or a standalone None"
            )
        else:
            check_table_width(
                constraint_table, 5, "Business Constraints table", findings
            )
            if not nonempty_rows(constraint_table):
                findings.append("Business Constraints table has no data rows")

    # Section 7: state table/transition structure and state diagrams.
    states = section_map.get(7)
    if states is not None and not is_none_statement(states.body):
        state_blocks = subsection_blocks(states.raw_body, states.body)
        if not state_blocks:
            findings.append(
                "Section 7 must contain a subsection per persisted lifecycle or None"
            )
        for title, raw_block, masked_block in state_blocks:
            block_tables = extract_tables(masked_block)
            state_table = next(
                (table for table in block_tables if len(table.header) == 5), None
            )
            if state_table is None:
                findings.append(
                    f"State model '{title}' lacks a five-column state table"
                )
                state_values: set[str] = set()
            else:
                check_table_width(state_table, 5, f"State table '{title}'", findings)
                state_values = set()
                for row in nonempty_rows(state_table):
                    if len(row) != 5:
                        continue
                    state_value = row[0].strip()
                    if not state_value:
                        findings.append(
                            f"State model '{title}' has an empty state value"
                        )
                    if state_value in state_values:
                        findings.append(
                            f"State model '{title}' repeats state '{state_value}'"
                        )
                    state_values.add(state_value)
                    if any(not cell.strip() for cell in row[1:]):
                        findings.append(
                            f"State '{state_value}' has an empty required cell"
                        )
                    for source_id in ids_in_cell(row[4], "SRC"):
                        if source_id not in source_ids:
                            findings.append(
                                f"State '{state_value}' references undefined {source_id}"
                            )

            transition_table = next(
                (table for table in block_tables if len(table.header) == 7), None
            )
            if transition_table is not None:
                check_table_width(
                    transition_table, 7, f"Transition table '{title}'", findings
                )
                for row in nonempty_rows(transition_table):
                    if len(row) != 7:
                        continue
                    from_state, event, guard, to_state, effects, actor, source_cell = (
                        row
                    )
                    if from_state.strip() not in state_values:
                        findings.append(
                            f"Transition in '{title}' uses undefined From state '{from_state}'"
                        )
                    if to_state.strip() not in state_values:
                        findings.append(
                            f"Transition in '{title}' uses undefined To state '{to_state}'"
                        )
                    if any(
                        not value.strip() for value in [event, guard, effects, actor]
                    ):
                        findings.append(
                            f"Transition {from_state} -> {to_state} in '{title}' has an empty required cell"
                        )
                    for source_id in ids_in_cell(source_cell, "SRC"):
                        if source_id not in source_ids:
                            findings.append(
                                f"Transition {from_state} -> {to_state} references undefined {source_id}"
                            )

            _, state_fences, _ = split_fenced_blocks(raw_block)
            diagrams = [
                fence
                for fence in state_fences
                if fence.language == "mermaid"
                and re.search(
                    r"^\s*stateDiagram(?:-v2)?\b",
                    fence.body,
                    re.IGNORECASE | re.MULTILINE,
                )
            ]
            if len(diagrams) != 1:
                findings.append(
                    f"State model '{title}' must contain exactly one Mermaid state diagram; found {len(diagrams)}"
                )

    # Section 8: non-empty subsections if the section is expanded.
    cross_cutting = section_map.get(8)
    if cross_cutting is not None and not is_none_statement(cross_cutting.body):
        topics = subsection_blocks(cross_cutting.raw_body, cross_cutting.body)
        if not topics:
            findings.append(
                "Section 8 must contain concern subsections or a standalone None"
            )
        for title, _raw_body, body in topics:
            if not body.strip():
                findings.append(f"Cross-cutting subsection '{title}' is empty")

    # Section 9: decision table shape.
    decisions = section_map.get(9)
    if decisions is not None and not is_none_statement(decisions.body):
        decision_table = next(
            (
                table
                for table in extract_tables(decisions.body)
                if len(table.header) == 6
            ),
            None,
        )
        if decision_table is None:
            findings.append(
                "Section 9 requires a six-column Design Decisions table or a standalone None"
            )
        elif not nonempty_rows(decision_table):
            findings.append("Design Decisions table has no data rows")

    # Every referenced ID must have a definition in its canonical section.
    defined = {
        "SRC": source_ids,
        "OP": operation_ids,
        "AP": access_pattern_ids,
        "DMC": dmc_ids,
    }
    for identifier in sorted(ids_in(text)):
        prefix = identifier.split("-", maxsplit=1)[0]
        if identifier not in defined.get(prefix, set()):
            findings.append(f"{identifier} is referenced but has no definition")

    return list(dict.fromkeys(findings))


def find_dependency_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    states: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        states[node] = 1
        stack.append(node)
        for dependency in graph.get(node, []):
            if dependency not in graph:
                continue
            if states.get(dependency) == 1:
                return stack[stack.index(dependency) :] + [dependency]
            if dependency not in states:
                cycle = visit(dependency)
                if cycle is not None:
                    return cycle
        stack.pop()
        states[node] = 2
        return None

    for node in graph:
        if node not in states:
            cycle = visit(node)
            if cycle is not None:
                return cycle
    return None


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
        content = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as error:
        print(f"ERROR: cannot read {path}: {error}", file=sys.stderr)
        return 2

    findings = validate(content)
    for finding in findings:
        print(f"FINDING: {finding}")
    print(f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
