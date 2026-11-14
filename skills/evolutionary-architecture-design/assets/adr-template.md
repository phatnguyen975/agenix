---
status: <proposed | accepted | rejected | deprecated | superseded by ADR-NNNN>
date: <Insert the actual creation or status-update date as YYYY-MM-DD>
decision-makers: <Name known people or roles authorized to decide; omit if unknown>
consulted: <Name known people or roles whose input was requested; omit if unknown>
informed: <Name known people or roles notified of the decision; omit if unknown>
---

<!--
AUTHORING INSTRUCTIONS — REMOVE THIS BLOCK IN THE FINAL ADR

- Replace each <...> with actual content and remove the angle brackets.
- Name the file NNNN-short-decision-title.md using the next available number,
  unless the repository already has an established ADR convention.
- A newly drafted decision starts as 'proposed'. Use 'rejected',
  'deprecated' or 'superseded by ADR-NNNN' only when their lifecycle
  meaning applies. Change to 'accepted' only after documented authorization.
  Never infer approval or historical dates.
- Omit 'decision-makers', 'consulted', and 'informed' when the information is
  unavailable. Never infer or invent stakeholders.
- One ADR per consequential choice. Name realistic alternatives; explain
  material option trade-offs under Pros and Cons when needed. If a constraint
  eliminates other choices, explain why rather than inventing a competitor.
- Keep driver IDs (FUN/QUA/CST/CNC) and related FF/ADR references consistent
  with the system architecture. Consequences describe the selected option's
  implications; option-by-option comparison explains why alternatives lost.
- Omit optional Confirmation, Pros and Cons, or More Information sections if
  they add no value. Unknowns that affect adoption or validation remain
  explicit, not omitted.
- To replace an accepted decision, create a proposed successor; supersede the
  prior ADR only once the successor is accepted and both records are linked.
-->

# <Short Title: Naming the Architectural Decision and Chosen Direction>

## Context and Problem Statement

<!-- Separate observed facts from assumptions. Identify what must be decided,
     why the decision matters now, affected boundaries and evidence sources. -->

<Describe the current situation, relevant source or assumption, and the specific architectural question to decide; cite driver IDs>

## Decision Drivers

<!-- List only requirements/constraints that distinguish the options. -->

- **<FUN/QUA/CST/CNC ID>:** <Explain how this driver influences the decision and cite its agreed target or constraint>.

## Considered Options

<!-- List the alternatives actually considered, including an incumbent option
     when relevant. When only one remains feasible, identify the decisive
     constraint rather than inventing a viable competitor. Use Pros and Cons
     below when more comparison is necessary. -->

- <Name the preferred or evaluated architectural option>
- <Name another real option, or remove this item if none is viable>

## Decision Outcome

<!-- For proposed ADRs use **Proposed:**; after authorization use **Decision:**.
     If the choice is not yet supportable, state the open issue and keep the ADR
     proposed; do not misrepresent it as accepted. -->

**Proposed:** <Name the preferred option and its driver-based rationale, or state which evidence/authorization is needed before a choice can be proposed>.

### Consequences

<!-- Record material benefits, negative effects, change impact and risk.
     Drop a label only when there is genuinely no such consequence. -->

- **Benefit:** <Describe the improvement expected from this option and why>.
- **Cost/Trade-Off:** <Describe complexity, operational burden, quality compromises or migration cost>.
- **Risk/Uncertainty:** <Describe assumptions, failure modes, evidence gaps and necessary follow-up>.

### Confirmation

<!-- OPTIONAL: identify how the decision will be assessed; if an FF is named,
     report its actual execution state. Do not claim a test has run if it has not. -->

<Describe the planned or performed review, experiment, scenario check or FF ID; include method, evidence and planned/active/suspended state as applicable>

## Pros and Cons of the Options

<!-- OPTIONAL: Include when meaningful trade-offs among alternatives require
     detail beyond the Decision Outcome. Repeat the H3 subsection for every
     considered option; include only supported Good / Neutral / Bad points.
     Explain each point relative to the same decision drivers. Do not copy
     the selected option's Consequences here word-for-word. Remove this
     section if the Outcome already gives sufficient comparative rationale. -->

### <Name the first considered option>

- **Good:** <Describe a supported advantage relative to the decision drivers>.
- **Bad:** <Describe a supported disadvantage, risk or disqualifying constraint>.

## More Information

<!-- OPTIONAL: related ADRs, sources and conditions requiring reconsideration.
     A successor ADR explicitly names 'Supersedes: ADR-NNNN'. -->

<Link supporting sources or related ADRs and state the revisit condition or supersession relationship, when relevant>
