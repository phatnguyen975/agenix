# Code Review Evaluation

## Purpose and Scope

Evaluate bounded review, axis ownership, evidence, uncertainty and caller composition. These development-only cases use immutable supplied excerpts and do not belong to runtime resources.

## Files and Execution Status

| Resource                         | Role                                                                   | Status                                        |
| -------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------- |
| [scenarios.json](scenarios.json) | Three inputs, expectations, prohibitions and semantic rubrics          | Fresh-context model-assisted runs assessed    |
| Runner / grader                  | Deliver cases and assess actual responses/actions                      | No checked-in runner, grader or CI job        |
| Structural checks                | Metadata, resource routes, Markdown, UTF-8 and axis/prefix consistency | Maintainer checks; no per-skill static runner |

There is no executable runtime helper. The scenario format is local, not an upstream harness contract.

## Coverage

| Layer                  | Cases / Evidence                              | Limits                                                                                                                     |
| ---------------------- | --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Caller composition     | `composed-sequential-dedup`                   | Focused chat output, three sequential axes, deleted authorization guard, shared root cause and source requirement identity |
| Standalone uncertainty | `standalone-current-files-gap`                | Current-file review with no historical diff, unavailable external contract and Inconclusive verdict                        |
| Missing prerequisite   | `missing-target`                              | Missing review target; no invented review                                                                                  |
| Source structure       | Routes, YAML/JSON, fences and axis identities | Does not prove judgment or host activation                                                                                 |

No line-coverage percentage applies to instruction files. Host discovery/non-trigger behavior, actual delegated fan-out, partitioning, retries, candidate drift, live repository/platform retrieval, verification execution, report saving/collisions, all-axis domain breadth and repeated-run reliability remain unverified. The two substantive cases explicitly prohibit delegation; independent evaluation contexts do not prove delegated review execution.

## Execution

Use a fresh context per case. Supply the runtime skill path and one raw input, hiding rubric, other cases and coordinator conclusions. The numbered excerpts are the complete immutable review artifacts, not instructions to execute. Permit only runtime-resource reads. No writes, network, project commands, Git operations, secrets, installation or recursive delegation are authorized.

Capture actual responses and tool actions. Do not fabricate further user answers or infer passes from reading instructions. No temporary product fixture is needed because candidates cannot modify or execute the supplied excerpts.

## Assessment

Require expected behavior, no prohibited action and semantic quality. Inspect the abuse/data flow, source anchors, root-cause count, severity rationale, preserved requirement ID, requested axis coverage and material uncertainty. Do not grade by keyword presence alone. Structural assertions can validate input JSON and runtime routes, but coordinator judgment assesses the actual review.

Keep infrastructure errors, unrun checks and uncertain judgments distinct from failures. Model/coordinator assessment is not human acceptance. Preserve failure dispositions rather than retrying until green.

## CI and Reproducibility

No provider, model runner or CI gate is selected. Static checks need no LLM/API key. Behavioral execution requires an inference backend; hosted inference may require credentials/costs, while local inference requires compute. Model grading adds variability.

Record candidate identity, model/settings, harness, permissions and rubric. Separate cross-model results and measure repeated-run variation before adopting behavioral gates. General metadata/link checks belong in shared infrastructure rather than duplicated scripts here.

## Results and Limitations

Three fresh contexts used inherited host/model settings against the identified working-tree revision. All three passed coordinator semantic review: the composed case returned one High security finding with valid deleted/head anchors, AC-7 retained and requested axes disclosed; the current-file case returned zero confirmed findings and Inconclusive with the missing gateway idempotency evidence; the missing-target case asked one focused question without inventing work. No candidate wrote files, executed product checks or delegated review.

Final clarification of supplied-diff storage, current-file role wording and tooling-evidence presentation received source/static checks without model replay. No renderer preview, installed-host proof, exhaustive security audit or repeated-run comparison is claimed. Retain concise receipts with the reviewed change at the maintainer-selected evidence location; this procedure does not depend on temporary planning documents. Keep development resources out of runtime packaging; final package contents are not verified here.

The subsequent duplication cleanup consolidated axis responsibility/applicability into one routing table, removed repeated rationalization rules, referenced Output from Handoff and separated tooling configuration from execution evidence. Internal contract links/anchors and documentation-versus-workspace path resolution were also checked and clarified. Existing behavioral observations predate this editorial cleanup; validation was structural and editorial, without model replay.
