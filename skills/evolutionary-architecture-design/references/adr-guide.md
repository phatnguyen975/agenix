# ADR Guide

Use when a **new or changed, architecturally significant decision** needs durable rationale. Follow the structure of Markdown Architectural Decision Records (MADR), adapting optional sections to the actual choice. The template is `assets/adr-template.md`.

## Decide What Deserves a Record

Create an ADR when a decision materially affects system structure, a difficult quality trade-off, public contracts, trust/data ownership, technology/platform dependencies, deployment independence or expensive migration. One ADR covers **one cohesive question**.

| Situation                                 | Action                                                                 |
| ----------------------------------------- | ---------------------------------------------------------------------- |
| New consequential style/boundary decision | ADR                                                                    |
| New architecture-level technology choice  | ADR if significant                                                     |
| Accepted decision materially changed      | New superseding ADR                                                    |
| Mandated technology with no choice        | Record constraint; ADR only for consequential implementation trade-off |
| As-is behavior with unknown rationale     | Document observation; do not invent ADR history                        |
| Trivial internal refactoring              | Usually no ADR                                                         |
| Optional choice deferred                  | Record DD; ADR when the choice is made                                 |

A single design iteration may produce zero, one or several ADRs. Do not manufacture choices or records to meet a quota. If only one feasible option exists, state why alternatives are non-viable; do not invent an equally viable option.

## Record Structure

**Required for a substantive decision:** title, context/problem, options actually considered, outcome and rationale, significant consequences, status and trace to driver IDs. Relevant optional information: decision makers/consulted/informed (provided roles only), confirmation mechanism, conditions for review and related decisions.

- **Title:** short decision phrased as problem and chosen approach; Title Case, no numeric prefix in H1.
- **Context and Problem Statement:** observed background, driver IDs, constraints, specific question; distinguish facts from assumptions.
- **Decision Drivers:** prioritized relevant facts/scenarios, not every system requirement.
- **Considered Options:** realistic alternatives compared using the same decision drivers, with their main benefit, cost or disqualifier. Avoid duplicate pros/cons sections.
- **Decision Outcome:** identify chosen option **only when a decision has been proposed**; tie its rationale to drivers, consequences, constraints and confidence.
- **Consequences:** benefits, trade-offs, operational work, impact on existing consumers, risks and reversibility. Acknowledge uncertainty.
- **Confirmation:** if applicable, how the decision will be checked; reference an FF only when it exists and state its `planned`/`active`/`suspended` state and execution method. Verification may be a review, experiment or rollout check instead.
- **More Information:** links to prior ADRs, issue/context sources, revisit condition and migration plan. Longer option-by-option pros/cons sections are optional when a short comparison is not sufficient.

Avoid bloated sections that merely repeat the system-design document; use references. An ADR is an immutable **historical rationale**, not a continuously rewritten technical specification.

## Status and Human Approval

| Status                   | Meaning                                                            |
| ------------------------ | ------------------------------------------------------------------ |
| `proposed`               | Suggested, not yet accepted                                        |
| `accepted`               | Explicitly approved or authorized by documented project governance |
| `rejected`               | Considered but not adopted                                         |
| `deprecated`             | Previously accepted, no longer applicable without replacement      |
| `superseded by ADR-NNNN` | Replaced by an accepted newer ADR                                  |

Use `date: YYYY-MM-DD` for the actual creation/status-update date (from an available trusted clock), not a fabricated date. Must not turn `proposed` into `accepted` by assuming the human agrees. In Update mode, keep accepted ADR reasoning unchanged; correct clerical errors or status metadata transparently, and supersede when a material choice changes.

## Supersession Procedure

1. Identify affected accepted ADR and drivers; draft a new proposed ADR with changed conditions and trade-offs.
2. Add `Supersedes: ADR-NNNN` to the new record's More Information. Keep old record unchanged while the replacement remains proposed.
3. After human approval, mark the new ADR `accepted`, old ADR `superseded by ADR-MMMM`, and link the old record to the new one in More Information or status metadata.
4. Update the ADR index and affected architecture views, crosscutting rules, migration decisions and fitness functions. Preserve old context for auditability.

If a planned decision is rejected before acceptance, mark it `rejected` and explain what happens next; do not quietly delete the history where the repository expects an audit trail.

## File and Link Rules

- Use `NNNN-short-decision-title.md` under the project's decision directory; default `docs/decisions/`. Reuse repository numbering conventions if established.
- Allocate the **next unused four-digit numeric prefix** rather than filling gaps that could clash; do not renumber existing ADRs.
- Use relative Markdown links, e.g. `[ADR-0004](decisions/0004-use-queue.md)` when referenced from `docs/system-design.md`.
- The H1 title is not automatically the filename, but should describe the same decision; maintain one authoritative file for each ID.
- YAML frontmatter values must be valid; quote status strings containing spaces. Omit unprovided optional people/role fields entirely.

## Worked Example

The following is **illustrative**, not project evidence:

```markdown
---
status: proposed
date: 2026-11-14
---

# Decouple Order Acceptance from Fulfillment with Messaging

## Context and Problem Statement

`QUA-02` requires accepting valid orders during a fulfillment outage.
Should the checkout path wait synchronously for fulfillment?

## Decision Drivers

- QUA-02: order acceptance during a 10-minute downstream outage
- CST-01: use existing managed platform capabilities

## Considered Options

- **Synchronous Fulfillment Request:** simple flow but dependent on fulfillment uptime.
- **Durable Asynchronous Message:** decouples acknowledgment from downstream processing;
  introduces eventual consistency and message recovery obligations.

## Decision Outcome

**Proposed:** Durable Asynchronous Message. It permits acceptance
without requiring immediate fulfillment availability, subject to
message durability and consumer recovery being validated.

### Consequences

- Benefit: checkout can acknowledge durable acceptance separately from processing.
- Cost: eventual order status and operational reconciliation are required.
- Risk: duplicate delivery needs idempotent processing.

### Confirmation

A planned outage/replay exercise will check QUA-02; no active fitness
function has yet been established.

## More Information

Review if durability or consistency requirements change.
```

Replace every `<...>` instruction with confirmed project-specific content and remove its brackets; illustrative text is not evidence. Keep the ADR `proposed` until explicit approval. When using `assets/adr-template.md`, remove guidance comments and placeholder-only backticks as well.
