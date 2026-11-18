# Data Impact Analysis Evaluation

## Coverage

Three read-only cases and one isolated report-writing [case](scenarios.json) ran in fresh contexts using inherited model settings. The four results passed semantic assessment. The saved artifact needed one formatting correction during read-back.

| Case                                    | Observed Result                                                                                                                                                                                                                                                                                                                                     |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `composed-parallel-rename-and-index`    | Preserved the caller's sections, moved technical analysis to the integrated revision, and identified the conflict and verification needed for mixed writers.                                                                                                                                                                                        |
| `standalone-single-shared-owner`        | Used the standalone report in chat, kept Identity as the sole owner of the shared table, and identified tenant ownership and deletion as open decisions.                                                                                                                                                                                            |
| `focused-read-without-schema-change`    | Reused the existing index and read path, kept the display value derived, and provided scoped verification without a migration.                                                                                                                                                                                                                      |
| `saved-report-with-coordinated-rollout` | Saved and read back `data-impact.md` in an isolated temporary directory. Included rollout for mixed worker versions and left the deployment mechanism open. Maintainer read-back found 11 corrupted separators from the write path and replaced them with ASCII colons. The corrected UTF-8 artifact passed scope, heading, and placeholder checks. |

## Execution

Give each fresh context the raw request and runtime skill path. Keep the rubric private and assess the actual response against the semantic criteria and prohibited actions. These cases explicitly load the skill. The write case exercises a fresh file only. Automatic routing, edits to an existing report, and repeated-run reliability remain unverified.

Maintainer checks cover metadata, local resource links, Markdown and the template. Final wording clarifications received static review. In a separate in-memory SQLite 3.50.4 fixture, both changes passed in isolation, the original combined change failed, the corrected clean replay passed, and the corrected upgrade rejected duplicate data. This fixture establishes behavior for its own test data and engine. This directory adds no runner or runtime dependency.
