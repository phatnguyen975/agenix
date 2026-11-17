# Codebase Design Evaluation

## Purpose and Scope

Assess source-structure review and design proposal behavior using supplied evidence. The cases exercise graph granularity, ownership, compatibility, and caller output.

## Files and Execution Status

| Resource                         | Role                                             | Status                                         |
| -------------------------------- | ------------------------------------------------ | ---------------------------------------------- |
| [scenarios.json](scenarios.json) | Raw requests and semantic assessment criteria    | Two read-only cases passed semantic assessment |
| Structural checks                | Metadata, resource links, and template structure | Maintainer checks passed                       |

## Coverage

| Case                                         | Behavior                                                                                                         |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `review-module-cycle-at-correct-granularity` | Standalone review, static cycle at architectural-module granularity, partial coverage, and design authority      |
| `composed-preserve-contract-and-rule-id`     | Caller-owned format and ID, established release and contract boundaries, provisional rules, and enforcement gaps |

Both cases start with explicit skill selection. Automatic routing, full-template generation and saving, real checker execution, and repeated-run reliability remain unmeasured.

## Execution

Use one case per fresh context and follow the permissions in the scenario file. Give the raw request and runtime skill path. Keep other cases and the rubric hidden. Preserve the actual response or a concise assessment receipt.

## Assessment

Pass when the response meets the expected behaviors and respects the prohibited actions. Check metadata and document structure deterministically. Judge the graph reasoning, compatibility impact, and evidence scope semantically.

## CI and Reproducibility

Structural checks need no inference backend. Pin the candidate, host permissions, model settings, inputs, and rubric before comparing behavioral runs. This directory adds no runner.

## Results and Limitations

The review found both module edges, confirmed the observed DR-07 cycle without treating the runtime callback as an import, and prioritized broader inspection within the rule's scope. The composed design kept the caller's sections and BND-4, reused the existing service contract, and described a pending dependency rule with passing and failing examples for a proposed check.

The runs used fresh contexts and inherited model settings. Results establish reasoning over the supplied evidence. Final template and reference refinements received static review. No product build, migration, or installed-host discovery was exercised.
