# Work Breakdown Planning Evaluation

## Purpose and Scope

Assess decomposition, dependency reasoning, output ownership and truthful readiness. Read-only model cases cover planning decisions; structural maintainer checks cover resources and metadata. Development resources are not runtime dependencies.

## Files and Execution Status

| Resource                         | Role                                            | Status                               |
| -------------------------------- | ----------------------------------------------- | ------------------------------------ |
| [scenarios.json](scenarios.json) | Two raw inputs and semantic assessment criteria | Independently exercised and assessed |
| Behavioral runner / grader       | Deliver inputs and assess responses             | No checked-in runner or CI job       |

## Coverage

Behavioral cases cover caller-composed Flat planning with a required amendment and custom lifecycle, plus standalone recursive reasoning with safeguards and a proposed cycle. The latter remains a draft where exact procedures/criteria are not supplied. Trigger/non-trigger host discovery, full generated-plan save, nested record integration, live tracker updates, large graphs, Mermaid rendering, inaccessible files, non-UTF-8 input, repeated-run reliability and multi-OS behavior remain unverified.

## Execution

For behavioral evaluation, provide one raw case input and the runtime skill path to a fresh context. Hide the rubric and other cases. Permit runtime reads only under the scenario restrictions; preserve actual response/action evidence. Do not invent user answers or treat proposed checks as executed.

## Assessment

Semantic assessment requires each expected behavior, no prohibited action and a usable explanation of actual scope/dependencies/remaining decisions. Status labels and structural review do not establish real verification evidence or historical immutability. Model assessment does not constitute human acceptance.

## CI and Reproducibility

Resource/metadata checks need no LLM key. Shared static checks belong in common infrastructure; no per-skill execution helper or test runner is required. Behavioral runs require an inference backend and may incur cost. Pin candidate, harness, permissions, model/settings and rubric before comparing runs or adopting a behavioral gate. No runner, provider or shared infrastructure is added.

## Results and Limitations

Two fresh-context read-only cases passed semantic assessment with inherited model settings. The composed response preserved X and requested the Z amendment, kept caller fields and distinguished unknown prerequisites. The recursive response retained coupled safeguards, reasoned A before B and disclosed missing commands rather than claiming execution readiness.

No model-generated product artifacts or helper invocations were allowed. After human approval, the format-specific parser and its dedicated fixtures were removed. Behavioral cases predate that change; final routing/consistency and recursive stopping/progress clarifications received static review without replay. These observations do not establish autonomous plan generation, installed-host support or reliability across repeated/model-varied runs. Exclude development resources from runtime packaging; final package contents are not verified here.
