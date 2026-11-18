---
name: data-impact-analysis
description: Analyze or review a proposed change to how an existing product reads, writes, derives, or retains data. Use to compare requirements with a persistence baseline, identify affected consumers and model changes, and plan migration compatibility, dependencies, recovery, and verification. Initial database design, implementation, and migration execution are separate tasks.
metadata:
  author: phatnguyen975
  version: "1.0"
---

# Data Impact Analysis

## Scope

Analyze owned persistence effects against an established model. A new query, invariant, retention policy, or write path can require analysis even when the schema stays the same. For externally owned storage, reason about the published interface and any local persistence effects. Record provider dependencies for the owner to resolve.

The deliverable explains requirements, the current baseline, proposed changes, compatibility, and verification. Keep shared design and schema artifacts read-only. Route any material change to a shared decision to its owner for a scoped amendment. Migration authoring, execution, and environment changes belong to implementation.

## Establish the Baseline

- Start with the request, relevant requirements, owned stores and affected consumers. Reuse prior decisions when their requirements and assumptions still hold.
- Use the caller's baseline or establish the relevant integrated revision. Prefer the selected toolchain's schema declarations and migration history for technical structure. Before implementation exists, an approved design can serve as the design baseline. Use shared design and decision records for ownership, invariants, and rationale.
- Keep the repository baseline, proposed change, and any observed environment state distinct. Merge establishes that a migration is present in repository history. Use separately supplied or authorized environment evidence for an applied-state claim.
- Read the affected structures and relevant history, including migrations or shared changes that may overlap. Name evidence gaps and stale or contradictory sources. Ask only when a material decision remains unresolved. Report the supported analysis and leave affected decisions open.

## Analyze the Impact

1. **Trace requirements to operations.** Map each material requirement to a source, the affected data and operation, and its disposition. Say what is read, written, derived, or transient. Record exact objects and paths when known. Reuse requirement IDs from the caller.
2. **Assess fit and gaps.** Check key and query shapes, cardinality, null and missing values, ownership and tenancy, and integrity under concurrent writes. For each important access pattern assess its existing supporting key or index, or justify a proposed change. State the enforcement point and failure behavior of material constraints. Cover lifecycle, retention, privacy, duplication, and consistency when relevant. State transaction and failure boundaries for multi-record or cross-store effects. Claim verified query plans only when the relevant evidence was inspected.
3. **Propose the smallest change.** Explain before and after, reason, affected consumers, and consequences for existing data and supported reader/writer versions. Distinguish compatible changes, breaking changes, and unverified compatibility. Record concrete alternatives when the choice matters. Use stable change IDs where traceability benefits from them. Distinguish proposals, approved intent, and integrated changes. Reuse an equivalent approved choice and check it against current evidence.
4. **Reconcile parallel work.** Check relevant known changes against the baseline for overlapping objects, incompatible invariants, and order-dependent prerequisites. Give a new shared structure one owner. Represent reliance on an outstanding change as a dependency, with its owner or unresolved ownership and the evidence needed before dependent implementation. Reassess affected assumptions when the integration baseline advances. Disjoint changes can proceed independently when no dependency or conflict is found within the examined scope.
5. **Specify rollout and evidence.** For material model or data changes, state the order, old/new compatibility, existing-data treatment, acceptance checks, and recovery or irreversible point. Describe only applicable stages. Link to actual migration artifacts when known and relevant. If implementation is pending, describe the required outcome and dependencies without fabricating paths, IDs, or results.

## Reference Routing

Load only the references needed for the current decisions.

| Situation                                                             | Reference                                                                |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Selecting a baseline, checking drift, or reconciling parallel changes | [Baseline and Reconciliation](references/baseline-reconciliation.md)     |
| Material ambiguity or a decision requiring approval                   | [Clarification and Decision Review](references/decision-review.md)       |
| Relational keys, constraints, indexes, or compatibility               | [Relational Impact](references/design-rules-relational.md)               |
| Document, key-value, or wide-column changes                           | [NoSQL Impact](references/design-rules-nosql.md)                         |
| Persisted state or transition changes                                 | [State Transition Modeling](references/state-transition-modeling.md)     |
| Compatibility, backfill, rollout, or recovery                         | [Change Classification and Rollout](references/change-classification.md) |
| Full standalone report                                                | [Data Impact Template](assets/data-impact-template.md)                   |

For specialized stores, use the project's actual model and authoritative documentation for the selected technology.

## Output and Verification

Use the caller's format, identifiers, and destination where provided. Return focused analysis in the requested medium and default to chat. Use the standalone template for a full report when the caller has no format. Omit sections that do not apply.

For a requested file, follow the project's documentation layout and use `data-impact.md` when it has no naming convention. Save or update only within the authorized scope. Read back the saved report before returning its path.

Before delivery, check that:

- Each material requirement has a source and disposition. Exact baseline revision or snapshot, scope, drift, and evidence limits are explicit.
- The proposed changes, cited definitions, and dependencies resolve. No cyclic dependencies, duplicate creation ownership, or unsupported assumptions remain in an implementation-ready proposal.
- Applicable checks cover existing data, supported versions, integrity and concurrency, and the combined change against the current integration baseline. Identify required clean initialization and representative upgrade evidence when migration is planned.
- Planned verification and executed evidence are distinct. Unresolved material questions identify the blocked decision, its consequence, and the evidence or approval needed. Approval of intent does not establish implementation or applied state.
