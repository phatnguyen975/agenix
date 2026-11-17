# Code Simplification Evaluation

## Purpose and Scope

Evaluate behavior-preserving simplification, a covering test baseline, scoped ownership and caller-selected output. These development-only cases are independent of runtime use. They exercise actual edits and checks in disposable Python fixtures; Python is an evaluation choice, not a capability prerequisite.

## Files and Execution Status

| Resource                         | Role                                                      | Status                                                   |
| -------------------------------- | --------------------------------------------------------- | -------------------------------------------------------- |
| [scenarios.json](scenarios.json) | Three requests, raw fixture files and semantic rubrics    | Model-assisted execution; results below                  |
| Runner / grader                  | Provision isolated cases and assess transcripts/artifacts | No checked-in runner, grader or CI job                   |
| Structural checks                | Metadata, resource paths, Markdown and UTF-8              | Maintainer checks; no duplicated per-skill static script |

The scenario format is local, not an upstream runner contract. No executable runtime helper is added by this change.

## Coverage

| Layer                                       | Case / Evidence                                                 | Limits                                                                                                   |
| ------------------------------------------- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Caller-composed edit                        | `composed-covered-refactor`, patch-delivery variant             | Approved implementation batch with deferred publication; coordinator applies the candidate's replacement |
| Standalone report / insufficient safety net | `standalone-uncovered-report`                                   | Green unrelated tests, no target coverage, authorized Markdown destination                               |
| Baseline failure                            | `standalone-failing-baseline`                                   | Relevant tests expose a seeded behavior defect before editing                                            |
| Preservation assertions                     | Existing fixture unittest assertions                            | Identity/falsy payloads, lazy evaluation, event order and exceptions in one small function               |
| Source contracts                            | Metadata, routes, fences, encoding and template routing | Structural validity does not prove semantic correctness or host compatibility                            |

No executable line-coverage percentage applies to the instruction files. Fixture assertions distinguish specific semantic regressions; they do not prove equivalence for every input. Autonomous file writes for the composed case, host discovery/trigger selection, a successful standalone full report, multi-file transformations, mixed Git index/worktree ownership, failed-transformation rollback, unavailable toolchains, cross-language/platform behavior and repeated-run reliability remain unverified.

## Execution

Create a fresh disposable directory from each case's `files` map. Supply only its realistic `messages`, the runtime skill path and the substituted fixture path to a fresh candidate context. Withhold rubrics, other cases and coordinator conclusions. Do not load this development directory as a skill resource.

Permit reads only of the runtime skill/resources and the fixture. The composed case may edit only the selected function. The uncovered case may write only its requested report and parent directory; source edits remain subject to the skill's prerequisites. The failing-baseline case must preserve existing content. Run `python -B -m unittest discover -v` inside the fixture; `-B` prevents bytecode artifacts. No network, Git operations, secrets, installation or shared repository writes are permitted. Model-service authority is separate from candidate tool authority.

Capture actual command outcomes, responses and changed files. Compare every pre-existing file against the raw fixture, inspect the function diff, rerun covering tests where appropriate and read any generated report. Do not fabricate additional user answers or results.

The composed case also defines a read-only `patch_delivery_variant`. In this variant, the candidate runs the baseline and returns an exact replacement function. The coordinator applies only that replacement within the disposable fixture and sends the recorded follow-up. The candidate then inspects the actual final file and runs the existing tests. Assess this delivery contract separately; it does not establish autonomous write/tool integration. Provision a fresh fixture for a new run and remove generated fixtures after assessment.

## Assessment

Require all expected behaviors, no prohibited behavior and the case's semantic quality criterion. Deterministic assertions check permitted file sets, preservation outside the selected function, unchanged tests and fixture command results. They do not select a preferred rewrite or grade wording. Semantic review assesses improved comprehension, preserved evaluation/error/side-effect behavior, relevant coverage, reused authority and truthful reporting.

Distinguish an expected fixture failure from an evaluation failure: the seeded-bug case succeeds when the candidate observes the failure and stops without repairing it. Infrastructure errors, unrun checks and uncertain judgments remain separate from pass/fail. Inspect actions and artifacts rather than accepting the candidate's completion claim. Coordinator assessment is not human approval; retain failure dispositions rather than retrying until green.

## CI and Reproducibility

No provider, model runner or CI gate is selected. Static checks and fixture unittest execution require no LLM/API key. Behavioral execution requires an inference backend; hosted inference may require credentials/costs, while local inference requires compute. Model grading adds variability.

Record candidate identity, fixture/runtime versions, model/settings, permissions, harness and rubric. Compare models separately and measure repeated-run variation before adopting behavioral CI gates. General skill structure/link validation belongs in a shared check rather than a separate implementation here.

## Results and Limitations

Keep concise receipts with the reviewed change at the maintainer-selected evidence location. Retain raw artifacts only when needed to reproduce a result and redact sensitive data. This procedure does not depend on temporary planning documents.

Fresh-context runs used inherited model/settings on Windows with Python 3.14.10, without independently pinned inference settings or a repeated-run comparison:

- **Composed refactor:** two direct-write attempts were infrastructure-blocked by host access denial before changing source, including one attempt in an already-writable coordinator workspace. They are not behavioral passes. A fresh read-only patch-delivery run returned a guard-clause transformation; the coordinator applied it, and candidate baseline/final runs each passed seven tests. Coordinator assertions confirmed the exact allowed file set, unchanged tests/notes and byte-for-byte preservation outside the selected function. Semantic review confirmed a clearer branch sequence with the same conditional evaluation, exceptions, event order and returned identity. This variant passed; autonomous write behavior remains unverified.
- **Uncovered standalone report:** passed semantic/artifact review. The candidate recognized that one passing test covered only an unrelated function, made no source/test edits, and saved/read back only the authorized Markdown report. The report correctly states the blocker, empty change set and verification limits without invented scores or approval.
- **Failing standalone baseline:** passed semantic/artifact review. Seven tests ran, with seven failures arising from two test methods in the seeded-bug fixture. The candidate stopped without changing source/tests or creating a report. Coordinator replay confirmed the intentionally failing state and unchanged files.

Source checks passed for frontmatter/UI YAML, version/author, local routes, fences, UTF-8 and JSON/fixture syntax. The skill-creator validator passed. UI metadata is unchanged; runtime routing selects only Markdown. The human approved the Markdown template and removed the HTML asset. No executable runtime helper, per-skill static runner, dependency, provider configuration or CI job was added. No Markdown renderer/browser preview or final package verification was performed. These observations concern the identified working-tree revision, not human approval or installed-host compatibility.

The report template was subsequently consolidated into Summary, Scope, Changes, Verification and optional Remaining Items. This received filled-case editorial review and static checks, without replaying the earlier report-generation case. Earlier saved output is not evidence for the revised presentation.
