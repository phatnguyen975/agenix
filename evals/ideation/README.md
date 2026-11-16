# Ideation Evaluation

## Purpose and Scope

Evaluate problem framing, meaningful alternatives, evidence-aware comparison and caller-owned output. This directory is development-only and independent of runtime resources.

## Files and Execution Status

| Resource                         | Role                             | Status                                                           |
| -------------------------------- | -------------------------------- | ---------------------------------------------------------------- |
| [scenarios.json](scenarios.json) | Three cases and semantic rubrics | Intended for isolated model execution and one real concept write |
| Runner / grader                  | Execute and assess cases         | No checked-in runner, automated grader or CI job                 |
| Structural checks                | Metadata, links and case data    | Maintainer checks; no per-skill structural script                |

This conversation format is local, not an upstream runner contract.

## Coverage

| Layer                             | Cases / evidence                               | Limits                                                        |
| --------------------------------- | ---------------------------------------------- | ------------------------------------------------------------- |
| Structural                        | YAML, UTF-8, references, Markdown and JSON     | Not evidence of model decisions                               |
| Standalone persistence            | `confirmed-direction-default-save`             | Prior exploration supplied; real file write/read-back         |
| Caller composition and evaluation | `bounded-caller-and-rare-need`                 | Comparison only, fixed constraints and uncertain causes       |
| Framing / missing inputs          | `open-problem-framing`                         | First response to an open idea                                |
| Trigger / resource routing        | Explicit skill loading and selective resources | No host discovery, competing-skill or installed routing suite |

Scenario coverage does not measure executable line/branch coverage or establish universal model reliability.

## Execution

Use one fresh context per case. Supply the skill path, case messages and execution constraints without the expected/prohibited rubric. For the save case, provide an empty disposable project root and authorize only its selected idea file and parent directories. Other cases are read-only. Do not use a real project, paid service or expanded permissions without separate authorization.

Capture actual replies and saved content. If later turns are added, deliver them only after the preceding assistant response. Do not fabricate user selection, research or experiment results. Candidate permission does not include network, product execution, Git operations or unrelated files.

## Assessment

Pass only when all expected behavior holds, prohibited behavior is absent and the quality criterion is met. Use deterministic checks for file existence, exact destination and permitted writes. Use semantic assessment for meaningful variation, faithful constraints, evidence status, trade-offs and useful validation. Equivalent language is acceptable; keyword matching alone is insufficient.

Record programmatic, model-assisted and human judgments distinctly. Preserve behavioral failures, grader uncertainty and infrastructure errors; blocked or unrun cases are not passes.

## CI and Reproducibility

No runner, provider or CI gate is selected here. Structural checks need no LLM. Model execution requires a configured backend; hosted inference may need credentials and incur costs, while local inference needs provisioned compute. Model grading may add cost and variability.

Record model/version, candidate identity, settings, harness and rubric. Compare under matching conditions and retain failed attempts. Measure repeated-run variation before adopting a gate; another model is a separate target rather than an interchangeable retry.

## Results and Limitations

Keep concise receipts with the reviewed change at the maintainer-selected evidence location. Retain raw output only when needed to reproduce a problem; redact sensitive data. This procedure does not depend on temporary planning documents.

No full multi-turn divergence-to-selection session, old-skill/no-skill baseline, repeated-run reliability, write failure, existing-file collision or host integration is proven by these cases. A concept's plausibility is not evidence of user demand or experiment success. Runtime packaging excludes development-only material.
