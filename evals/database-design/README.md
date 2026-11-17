# Database Design Evaluation

## Purpose and Scope

Assess initial data-model design for relational and document databases. The cases examine concurrency, database-specific limits, and caller-owned output.

## Files and Execution Status

| Resource                         | Role                                             | Status                                          |
| -------------------------------- | ------------------------------------------------ | ----------------------------------------------- |
| [scenarios.json](scenarios.json) | Raw requests and semantic assessment criteria    | Two cases passed on their latest read-only runs |
| Structural checks                | Metadata, resource links, and template structure | Maintainer checks passed                        |

## Coverage

| Case                                | Behavior                                                                                                                        |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `standalone-reservation-invariants` | Tenant-safe references, global uniqueness, concurrent interval conflicts, and partitioning trade-offs                           |
| `composed-measurement-integrity`    | Caller-owned format and IDs, MongoDB collection limits, atomic acceptance, restricted deletion, and expiry versus deduplication |

These runs cover explicitly selected skill use. Automatic discovery, out-of-scope routing, full-document generation and saving, database execution, and repeated-run reliability remain unmeasured.

## Execution

Use one case per fresh context and follow the permissions in the scenario file. Give the raw request and runtime skill path. Keep the rubric and other cases hidden. Preserve the actual response or a concise assessment receipt.

## Assessment

Pass when the response meets the expected behaviors, respects the prohibited actions, and explains how the proposed model behaves under the supplied failure and concurrency cases. Use deterministic checks for metadata and resource structure. Assess integrity, authority, and completeness by meaning. A proposed fixture provides evidence about what to check later.

## CI and Reproducibility

Structural checks need no inference backend. Pin the candidate, host permissions, model settings, inputs, and rubric before comparing behavioral runs. This directory adds no runner.

## Results and Limitations

The PostgreSQL case passed in one read-only run. It protected tenant membership with a composite foreign key, used a conditional exclusion constraint for overlapping confirmations, and explained why start-month partitioning would complicate the global invariants.

Two early MongoDB runs modeled an event-ID registry as part of the chosen design without an approved policy for retaining IDs after readings expire. The final run passed after the lifecycle and missing-input guidance was clarified. It kept the registry conditional, explained the scope of the existing unique index, and used shared device writes to protect the acceptance/deletion race. It kept the caller's three sections and rule IDs.

The four runs used fresh contexts and inherited model settings. SQL received static review after final shared wording changes. Database behavior, template rendering, and installed-host integration were outside the execution scope.
