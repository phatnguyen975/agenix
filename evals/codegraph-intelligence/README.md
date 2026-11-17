# CodeGraph Intelligence Evaluation

## Purpose and Scope

Evaluate CLI-domain selection, structural evidence interpretation, index identity/freshness and caller authority. This directory is development-only and is not a runtime dependency.

## Files and Execution Status

| Resource                         | Role                                                   | Status                                                                  |
| -------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| [check_cli.py](check_cli.py)     | Real CLI query contracts and failure/identity fixtures | Executable integration checks for installed CodeGraph 1.6.2             |
| [scenarios.json](scenarios.json) | Three candidate behavior cases with semantic rubrics   | Isolated model execution; one enabled fixture and two bounded scenarios |
| Model runner / grader            | Submit cases and capture/grade responses               | No checked-in runner or automated grader                                |

The scenario format is local, not an upstream runner contract. Shared metadata/link checks are not duplicated here.

## Coverage

| Layer                | Checks / cases                                                                                 | Limits                                                         |
| -------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| CLI contracts        | Version, status, files, query, explore, context, node, callers, callees, impact, affected      | Simple JavaScript fixture on the available host                |
| Failure and identity | Missing symbol, missing index, inherited parent index, invalid flag, modified-source indicator | Not full stale/deleted-edge or worktree coverage               |
| Domain reasoning     | `enabled-refactoring-impact`                                                                   | Actual relationships and candidate tests, not runtime coverage |
| Applicability        | `disabled-literal-search`                                                                      | Does not test actual host discovery                            |
| Review boundary      | `stale-index-and-empty-results`                                                                | Supplied evidence, not live worktree mismatch reproduction     |

No fixture establishes all language/framework graph resolution or every domain's completeness. Test-file discovery is not proof of test assertions or execution.

## Execution

Run `python evals/codegraph-intelligence/check_cli.py` from the repository root, or invoke the file by its absolute path. It requires an existing 1.6.2 CLI and the Python standard library; it never installs dependencies. The script provisions and indexes only disposable fixture projects, disables telemetry/download/daemon behavior for its child processes and checks queries without modifying a real project. Missing/incompatible CLI or an unexpected result fails the run, not a silent pass.

For behavioral cases, use a fresh context and supply the skill, permitted evidence and case messages without grading criteria. For the enabled case, prepare the same small source layout in a disposable indexed directory and provide its actual root. Only existing CLI queries are permitted; no source/index maintenance or test execution. Keep model-service authorization separate from candidate tool permissions.

## Assessment

Require every expected behavior, absence of prohibited behavior and the quality criterion. Use the script for observable query results, source preservation and prerequisite cases. Use semantic judgment for query suitability, truthful findings, static-analysis limits and caller-owned output. Equivalent wording is acceptable; keyword matching alone is insufficient.

Keep infrastructure errors, unrun cases, grader uncertainty and behavioral failures distinct. Identify programmatic, model-assisted and human assessments; model judgments are not human approval. Preserve failures and dispositions rather than retrying until green.

## CI and Reproducibility

The CLI fixture script requires no LLM/API key, but a future CI environment must provision its declared CLI version independently. No shared distribution or CI bootstrap is implemented here. Behavioral execution needs an inference backend; hosted inference may require credentials/costs and local inference requires compute. Model grading may add variability.

Record CLI/model versions, candidate identity, harness, settings and rubric. Compare under matching conditions; cross-model results are separate targets. Measure repeated-run variation before adopting model-based gates.

## Results and Limitations

Keep concise receipts with the reviewed change at the maintainer-selected evidence location. Retain raw fixture output only when needed to reproduce a failure; redact sensitive data. Temporary planning documents are not required to use this material.

The first script run exposed a test assumption: a supposedly unindexed child directory resolved to its indexed parent. The fixture now asserts that behavior and tests a separate unindexed root; runtime guidance verifies returned project identity. No host discovery, multi-OS/language matrix, installed skill-resource resolution, repeated-run reliability or baseline comparison is established. Runtime packaging excludes this development tree.
