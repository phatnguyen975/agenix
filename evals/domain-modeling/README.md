# Domain Modeling Evaluation

## Purpose and Scope

Assess scope-sensitive DDD reasoning, business authority and evidence boundaries. Development resources are independent of runtime use. Read-only cases assess focused modeling/review, not implementation or expert-workshop participation.

## Files and Execution Status

| Resource                         | Role                                                 | Status                                            |
| -------------------------------- | ---------------------------------------------------- | ------------------------------------------------- |
| [scenarios.json](scenarios.json) | Two raw inputs, expectations and prohibited behavior | Independently exercised and semantically assessed |
| Behavioral runner / grader       | Deliver inputs and inspect actual responses/actions  | No checked-in runner or CI job                    |
| Structural checks                | Metadata, paths/anchors, Markdown and UTF-8          | Maintainer checks; no per-skill static runner     |

## Coverage

| Case                                | Assessed Behavior                                                                                                           |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `review-credit-concurrency`         | Standalone read-only review, hard consistency, counterexample, human decisions and reasoning versus production evidence     |
| `composed-focused-language-mapping` | Caller-owned focused output, prior-decision reuse, contextual language, influence/message directions and selective patterns |

Full-document authoring/save, evolution/regression writes, strategic classification, value-object modeling, event-type discovery, host trigger/non-trigger selection, renderer behavior and repeated-run stability remain unverified. No executable line-coverage metric applies to instructions.

## Execution

Give a fresh context one raw case input and the runtime skill path, hiding assessment criteria and other cases. Allow runtime reads under the declared permissions; do not execute product checks, write files or invent user replies. Preserve actual responses/actions for semantic assessment. No disposable product fixture is needed for these read-only cases.

## Assessment

Pass requires all expected behaviors, no prohibited actions and concrete, useful domain reasoning. Inspect whether evidence supports claims, scope stays focused and unresolved business decisions are surfaced without inventing policy. Do not grade by headings/keyword matches. Model assessment is not human acceptance.

Structural checks verify frontmatter/UI YAML, scenario JSON, file paths/anchors, fences, UTF-8 and whitespace. They do not establish business correctness.

## CI and Reproducibility

Static checks need no LLM key; common static verification belongs in shared infrastructure. Behavioral runs need an inference backend and may incur costs. Pin candidate, model/settings, harness, permissions and rubric before comparing runs or adopting a CI gate. No runner, provider or dependency is added here.

## Results and Limitations

Two independent fresh-context read-only cases passed semantic assessment with inherited model settings. The review produced a 100-credit/two-70-orders counterexample, rejected eventual overrun as contrary to R1, distinguished reasoning from execution and asked for missing authority/release semantics. The composed case preserved both terms, upstream influence and reverse query direction; it described ACL as a modeling responsibility and avoided invented organizational relationships.

These are single supplied-context observations, not implementation or general reliability evidence. Later process-policy wording and the branched event illustration received static review without replay. Fowler's Bounded Context article, Vernon's Effective Aggregate Design Parts I/II and official EventStorming material supported source review; the Evans reference PDF endpoint returned HTTP 403, so a full reread of that source is not claimed. No renderer or installed-host proof is claimed. Exclude development resources from runtime packaging; package contents are not verified here.
