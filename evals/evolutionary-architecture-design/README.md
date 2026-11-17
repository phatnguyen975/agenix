# Evolutionary Architecture Design Evaluation

## Purpose and Scope

Assess scoped architecture reasoning, decision authority and evidence. The cases use supplied facts and ask for results in chat.

## Files and Execution Status

| Resource                         | Role                                            | Status                                  |
| -------------------------------- | ----------------------------------------------- | --------------------------------------- |
| [scenarios.json](scenarios.json) | Raw requests and semantic assessment criteria   | Two independent read-only runs assessed |
| Structural checks                | Metadata, paths, anchors and template structure | Maintainer checks                       |

## Coverage

| Case                               | Behavior                                                                                           |
| ---------------------------------- | -------------------------------------------------------------------------------------------------- |
| `review-irreversible-cutover`      | Standalone review, single write authority, data recovery, ADR supersession and fitness check state |
| `composed-client-offline-decision` | Caller-owned fields, focused client trade-offs, prior approvals and missing freshness target       |

Host discovery, full-document save, actual migration, recurring fitness check execution and repeated-run reliability are outside these runs.

## Execution

Use one case per fresh context and follow the permissions in the scenario file. Give the raw request and runtime skill path. Keep the rubric and other cases hidden. Preserve the response or a concise assessment receipt. The cases require no product execution.

## Assessment

Pass when the response meets the expected behaviors, respects the prohibited actions and explains the trade-offs in the supplied context. Assess readiness, authority and the limits of evidence by meaning. Structural checks can confirm file and template consistency. The quality of the architectural judgment needs semantic assessment.

## CI and Reproducibility

Structural checks do not require an inference backend. Pin the candidate, host permissions, model settings, inputs and rubric before comparing behavioral runs. This directory uses the repository's scenario convention and adds no runner.

## Results and Limitations

Both read-only cases passed semantic assessment using inherited host and model settings. The cutover review identified competing writers and the schema recovery boundary, held the successor at proposed and recorded the staging load result separately from recurring operation. The client case compared storage choices in the caller's fields, surfaced the missing freshness decision and described planned browser checks.

These single runs used supplied evidence. Final wording and template checks were static. The runs did not exercise a real cutover, save a model-generated artifact, render diagrams or verify installed-host routing.
