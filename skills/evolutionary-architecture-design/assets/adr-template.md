---
status: <proposed | accepted | rejected | deprecated | superseded by ADR-NNNN>
date: <YYYY-MM-DD>
decision-makers: <People or roles responsible for the decision>
consulted: <People or roles consulted during the decision>
informed: <People or roles informed of the decision>
---

<!--
AUTHORING INSTRUCTIONS — REMOVE THIS BLOCK IN THE FINAL ADR

- Replace each <...> with actual content and remove the angle brackets.
- Name the file NNNN-short-decision-title.md using the next available number,
  unless the repository already has an established ADR convention.
- A newly drafted decision starts as 'proposed'. Change to 'accepted' only
  after explicit documented authorization. Other supported states are
  'rejected', 'deprecated', and 'superseded by ADR-NNNN'. Never infer approval
  or historical dates.
- Omit 'decision-makers', 'consulted', and 'informed' when the information is
  unavailable. Never infer or invent stakeholders.
- One ADR per consequential choice. Compare realistic alternatives with the
  same drivers; if a constraint eliminates other choices, explain why rather
  than invent a viable competitor. Record material costs as well as benefits.
- Keep driver IDs (FUN/QUA/CST/CNC) and related FF/ADR references consistent
  with the system architecture. Do not duplicate a long analysis in both an
  option comparison and consequences section.
- Omit optional Confirmation / More Information sections if inapplicable.
  Unknowns that affect adoption or validation remain explicit, not omitted.
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

<!-- Evaluate at least two real candidates against the same drivers; infeasible
     candidates with their disqualifying constraint rather than inventing balance. -->

- **<Name of the First Architectural Option>:** <Explain its principal benefit, cost or disqualifier, and available evidence>.
- **<Name of the Alternative Architectural Option>:** <Explain its principal benefit, cost or disqualifier, and available evidence>.

## Decision Outcome

<!-- For proposed ADRs use **Proposed:**; after authorization use **Decision:**.
     If the choice is not yet supportable, state the open issue and keep the ADR
     proposed; do not misrepresent it as accepted. -->

**Proposed:** <Name the preferred option and explain why it best serves the cited drivers compared with the alternatives, including unresolved conditions>.

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

## More Information

<!-- OPTIONAL: related ADRs, sources and conditions requiring reconsideration.
     A successor ADR explicitly names `Supersedes: ADR-NNNN`. -->

<Link supporting sources or related ADRs and state the revisit condition or supersession relationship, when relevant>
