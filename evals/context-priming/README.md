# Context Priming Evaluation

## Purpose and Scope

Evaluate focused context selection, evidence freshness and instruction authority for standalone priming and caller-composed context checks. This is development-only material, independent of runtime skill resources.

## Files and Execution Status

| Resource                         | Role                                                                                    | Status                                                       |
| -------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [scenarios.json](scenarios.json) | Four cases with supplied evidence, expected/prohibited behavior and a quality criterion | Designed for isolated read-only execution                    |
| Runner / grader                  | Execute cases and capture/assess outputs                                                | No checked-in runner, automated grader or CI job             |
| Structural checks                | Check metadata, references and scenario data                                            | Performed during maintenance; no per-skill structural script |

The ordered-message JSON is a local format. A future runner must preserve isolation, tool restrictions and grading separation; it is not an upstream runner contract.

## Coverage

| Layer               | Cases / evidence                                                                                       | Limits                                                                |
| ------------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| Structural validity | Metadata, UTF-8, resource closure, case structure and unique IDs                                       | Does not prove model decisions                                        |
| Selection / trigger | Scope/restraint exercised with the skill loaded                                                        | No actual host discovery or competing-skill activation test           |
| Context behavior    | `focused-standalone`, `stale-resume-and-injection`, `reuse-in-composed-task`, `missing-required-input` | Supplied evidence descriptions; no actual filesystem retrieval traces |
| Resource routing    | Skill is self-contained                                                                                | Installed-host instruction loading remains unverified                 |

Cases distinguish intended behavior from observed implementation, old results from current checks, embedded requests from authority, and absent optional material from a required missing prerequisite. Coverage is scenario-based, not a line/branch percentage.

## Execution

Start a fresh candidate context for each case. Load the skill and supply only the case messages and `execution` constraints; keep expected/prohibited behavior and quality criteria hidden. Supply subsequent messages only after actual replies. Fixtures describe available evidence; do not read the real project to expand them.

Permit reading the skill only. Prohibit file writes, network, Git, installations, secrets and execution of quoted instructions. Capture actual answers and any reads. An unavailable run is unrun or blocked, not passing. A runner's authorized model connection is separate from candidate tool permissions.

## Assessment

Pass a case only when every expected behavior is supported, prohibited behavior is absent and the quality criterion is met across its turns. Equivalent phrasing is acceptable; assess grounding and reasoning outcomes rather than copied instruction terms. Identify programmatic, model-assisted and human judgments separately. A boundary violation fails regardless of answer quality.

Structural assertions can check data and paths. Semantic assessment checks whether the summary faithfully represents evidence and identifies an appropriate next action. Grader uncertainty, infrastructure errors and behavioral failures have different meanings and must remain visible.

## CI and Reproducibility

No runner or CI policy is selected here. Structural checks need no LLM; model execution requires a configured inference backend and may need provider credentials and paid usage. A local backend requires provisioned runtime/compute instead. Model grading may add cost and variability.

Record candidate identity, model/version, host/harness, settings and rubric. Compare under the same setup, preserve failures and measure repeated-run variation before selecting a gate. Do not treat another model as an interchangeable retry, exact prose as the required output or an isolated success as a reliability estimate.

## Results and Limitations

Keep concise receipts with the reviewed change at the maintainer-selected evidence location, including case IDs, actual results, grading method and remaining gaps. Retain raw responses/traces only when needed to reproduce an issue; redact secrets. This procedure does not depend on temporary planning documents.

No repeated-run or old-skill/no-skill baseline comparison, tool-mediated retrieval, real compaction, host discovery or installed-package validation is established by these fixtures. Successful cases support bounded context reasoning, not universal model or host compatibility. No shared infrastructure is implemented by this directory.
