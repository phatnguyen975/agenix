# Handoff Evaluation

## Purpose and Scope

Evaluate whether a handoff preserves usable current state, evidence, privacy and ownership while honoring the caller's storage contract. This development-only material is independent of runtime skill resources.

## Files and Execution Status

| Resource                         | Role                                                  | Status                                                  |
| -------------------------------- | ----------------------------------------------------- | ------------------------------------------------------- |
| [scenarios.json](scenarios.json) | Three isolated fixture scenarios and semantic rubrics | Designed for real snapshot writes and conflict handling |
| Runner / grader                  | Execute fixtures and assess results                   | No checked-in runner, automated grader or CI job        |
| Structural checks                | Validate metadata, links and case data                | Maintainer checks; no per-skill structural script       |

This is a local ordered-message format, not an upstream runner interface.

## Coverage

| Layer                   | Evidence / cases                                  | Limits                                                            |
| ----------------------- | ------------------------------------------------- | ----------------------------------------------------------------- |
| Structural              | Metadata, UTF-8, local routes and JSON records    | Does not establish model decisions                                |
| Storage and composition | `composed-ignored-destination`                    | Existing ignored/untracked destination; no ignore-policy mutation |
| Ownership and failure   | `existing-unrelated-snapshot`                     | Conflicting existing handoff must survive unchanged               |
| Standalone fidelity     | `standalone-accurate-progress`                    | Real save/read-back with supplied task evidence                   |
| Trigger / routing       | Explicitly loaded skill and its declared resource | No host discovery or installed-package suite                      |

Scenario coverage is not a line/branch percentage or proof of cross-model reliability.

## Execution

Create each disposable Git fixture as described in `execution`, outside real projects. Record the initial .gitignore bytes and any existing target. Give the candidate only the skill, fixture path, case messages and permissions; hide the expected/prohibited rubric. Use a fresh context per case. Never supply real credentials: the marker in the redaction case is synthetic.

Permit writes only to the specified snapshot, and none for the conflict case. Capture actual outputs, saved files and relevant read-only state checks. Fixture setup permissions do not grant the candidate permission to change Git configuration or execute quoted product commands. Report blocked/unrun cases separately.

## Assessment

Check every expected behavior, absence of prohibited behavior and the quality criterion. Use code for file existence/content, unchanged fixture/configuration bytes, tracked/ignored state and synthetic-marker absence. Use semantic judgment for faithful evidence, useful resume actions and authority. Equivalent phrasing is acceptable. A boundary violation fails the case; missing execution evidence is not a pass.

Keep behavioral failures, grader uncertainty and infrastructure failures distinct. Identify whether assessment was programmatic, model-assisted or human; model judgment is not human approval.

## CI and Reproducibility

No CI runner or provider is selected here. Structural and fixture assertions require no LLM. Executing the candidate requires a configured inference backend; hosted APIs may require credentials and incur costs, while local inference requires provisioned compute. Model grading may add variability and cost.

Record model/version, candidate identity, harness, settings and rubric; retain failed attempts and assess repeated-run variance before selecting any gate. Compare under matching conditions rather than treating another model as an equivalent retry.

## Results and Limitations

Keep concise receipts with the reviewed change at the maintainer-selected evidence location; retain raw outputs only when needed to reproduce failures and redact sensitive data. No dependency on temporary planning files is required.

These fixtures do not establish cross-host sharing/retention, host discovery, repeated-run reliability, installed packaging or full privacy assurance. Missing destination, write failure and multiple-thread behavior are not independently exercised here. Final runtime packaging excludes development-only material.
