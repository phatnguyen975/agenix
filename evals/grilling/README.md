# Grilling Evaluation

## Purpose and Scope

Evaluate whether `grilling` resolves consequential ambiguity within the supplied scope while preserving user decisions, dependencies and authority boundaries. Cover standalone use and caller-composed use.

This directory contains development-only evaluation material under the repository's `evals/<skill>/` grouping. It is not a runtime dependency or a discoverable skill. The section structure below separates scope, coverage, execution and evidence so other capability evaluations can use the same organization without requiring identical tests, tools or output formats.

## Files and Execution Status

| Resource                         | Role                                                                                               | Current status                                                         |
| -------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [scenarios.json](scenarios.json) | Ten ordered-conversation cases with expected behavior, prohibited behavior and a quality criterion | Authored; exercised through read-only subagent runs during maintenance |
| Model runner / grader            | Submit cases, capture responses and assess results                                                 | No checked-in runner, automated grader or CI job                       |
| Structural checks                | Validate metadata, references and evaluation data                                                  | Performed during maintenance; no checked-in suite in this directory    |

The JSON is a local conversation format, not a standard runner interface. The [Agent Skills evaluation guide](https://agentskills.io/skill-creation/evaluating-skills#designing-test-cases) describes a different, skill-local format. Reusing an external runner would require checking its input contract and preserving turn order and isolation.

## Coverage

Distinguish structural validity, skill selection, resource selection and task behavior. A test in one layer does not prove another layer works.

| Layer                          | What it can establish                                                                                                  | Current coverage                                                                                                             |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Structural checks              | Parseable metadata/data, local files and anchors resolving, compatible templates or script interfaces where applicable | Metadata, local resource links, UTF-8, Markdown fences and scenario records checked during maintenance; no reusable CI suite |
| Trigger / selection evaluation | Appropriate activation for positive prompts and restraint for negative or neighboring-skill prompts                    | No host-level activation tests; preloading the skill in `non-trigger` tests restraint only                                   |
| Resource routing evaluation    | Relevant references loaded when needed, unrelated resources avoided, missing resources handled truthfully              | Local routes inspected; no trace-based behavioral or installed-host routing suite                                            |
| Behavioral evaluation          | Decision quality, scope, output and authority handling after loading the skill                                         | Ten scenarios mapped below; semantic assessment                                                                              |

| Concern                                                           | Cases                            |
| ----------------------------------------------------------------- | -------------------------------- |
| Standalone questioning and confirmed summary                      | `standalone-independent-choices` |
| Prior decisions, supplied facts and caller-owned output           | `caller-owned-output`            |
| Mechanical-task scope restraint after loading                     | `non-trigger`                    |
| Prerequisite order, vague reply and early stop                    | `dependency-vagueness-stop`      |
| Missing evidence and non-delegable approval                       | `missing-evidence-and-authority` |
| Missing subject                                                   | `missing-subject`                |
| Partial reply, remaining question and final summary               | `partial-answer`                 |
| Legitimate bounded delegation and rationale                       | `bounded-delegation`             |
| Changed approved premise, scoped reopening and amendment boundary | `changed-approved-premise`       |
| Untrusted source instructions and credential boundary             | `source-instruction-boundary`    |

This is scenario coverage, not executable line/branch coverage or proof of universal compatibility. Add cases for evidenced risks rather than requiring the same case count for every skill.

## Execution

1. Identify the candidate revision or uncommitted snapshot, case set and execution method. For model runs, record provider/model version, host or harness, available tools and supported generation settings.
2. Follow `execution` in the scenario file. Start a fresh context per case; provide the candidate only the skill, permitted context and the current user message. Keep grading expectations separate from candidate inputs.
3. Deliver each subsequent scripted user message only after receiving the actual assistant reply. Do not fabricate replies, replace stop signals or feed later answers into earlier turns.
4. Enforce the declared resource boundary: read only the skill and supplied context; no candidate file writes, network access, Git publication, secret access or downstream execution. Any runner-side model-service connection requires separately configured authorization; it does not authorize candidate tool access.
5. Capture actual responses and relevant tool traces for assessment. Report unavailable execution as blocked or unrun, never as a passing result.

Trigger evaluations would require a separate setup exposing the intended discovery metadata and competing skills without preloading the target instructions. Behavioral routing checks would require observable resource reads. Neither setup is implemented here.

## Assessment

For each case, check every expected behavior, absence of every prohibited behavior and the quality criterion across all turns. Accept equivalent wording. A case passes only when all checks hold; a permission violation fails it regardless of answer quality.

Use deterministic assertions for parseable data, paths or observable artifacts when applicable. Assess question relevance, faithful summaries and appropriate authority handling against actual responses with a semantic rubric. Keyword presence alone is insufficient. Identify whether grading was programmatic, model-assisted or human; model-assisted assessment is not independent human approval.

Keep behavioral failures, grader uncertainty, infrastructure errors and unrun cases distinct. A timeout or authentication error is not evidence of a skill regression, but is also not a pass. Preserve failed attempts and their dispositions; do not retry until green and discard the failures.

## CI and Reproducibility

No CI policy or provider is selected by this directory. Structural checks can run without an LLM. Automated behavioral, trigger or routing evaluations need an inference backend: a hosted API generally requires credentials and incurs usage charges; a local model needs its own provisioned runtime and compute. An LLM grader can add inference cost and variability. Scenario files themselves require neither credentials nor paid execution.

Before making model results a CI gate, choose and record the model/version, harness, rubric, settings, repetition policy and acceptance criteria. Keep candidate-model changes separate from grader changes. Compare implementations under the same setup; treat another model as a separate compatibility target rather than an interchangeable rerun.

Model outputs and model-based grading can vary even with unchanged inputs. Use semantic invariants instead of exact prose matching, review uncertain judgments and measure repeated-run variation where it matters. Pinning the setup reduces confounding changes; it does not guarantee deterministic inference. Retain results by model and run rather than hiding variation in an aggregate score.

## Results and Limitations

Keep concise run receipts with the reviewed change at the maintainer-selected evidence location: candidate identity, scenario IDs, execution/grading method, actual outcomes, failure dispositions and remaining gaps. Do not depend on temporary planning documents or runtime skill resources to locate this evaluation material. Retain raw responses or traces when needed to reproduce a failure; redact secrets. Keep current results out of this reusable procedure description.

Current gaps include actual host discovery/activation, installed resource resolution, tool-mediated lookup, unavailable-tool behavior, large-frontier batch sizing, repeated-run reliability and broader workflow integration. No controlled old-skill or no-skill baseline comparison establishes improvement. Successful maintenance runs do not establish CI readiness, cross-model reliability or complete coverage. Future runner integration and release exclusion of development-only material remain separate work.
