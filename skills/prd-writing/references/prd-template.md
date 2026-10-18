# PRD Template

Fill this exact structure end to end. Every `<...>` placeholder must be replaced with concrete, specific content before the file is written. None may remain in the output — an unresolved placeholder means elicitation isn't finished yet.

```markdown
# PRD: <System or Feature Name>

> **Status:** Draft | Approved
> **Owner:** <name>
> **Date:** <YYYY-MM-DD> — v<N>

## 1. Executive Summary

<One paragraph: what the system/feature is, who it serves, the core value it
delivers, current status.>

## 2. Problem Statement

<The user/business problem being solved, current situation and relevant
context, why this is being addressed now.>

## 3. Goals

<Bulleted, numbered business and system-level goals this PRD exists to satisfy.>

- **G-01:** <goal>
- **G-02:** <goal>

## 4. Target Users

<Primary and secondary user segments — role, context, need, pain point. Not a
full persona deep-dive.>

- **<segment> (Primary):** <context, need, pain point>
- **<segment> (Secondary):** <context, need, pain point>

## 5. User Journeys

<Each journey uses this exact format, ordered by priority — High first.
Narrative flow, not acceptance-test detail: that belongs to a feature spec.
Priority is set by a forced trade-off across journeys, not a default — see
elicitation-flow.md, Section 5.>

### UJ-01: <Journey Name>

- **Actor:** <primary user/persona>
- **Priority:** High | Medium | Low
- **Supports:** <Goal ID(s), e.g. G-01>
- **Goal:** <what the user wants to accomplish>
- **Trigger:** <what starts this journey>
- **Flow:**
  1. <step>
  2. <step>
  3. <step>
- **Outcome:** <end state / value delivered>

## 6. Scope

### In Scope

<Capabilities explicitly delivered by this system/version.>

- <capability>

### Out of Scope

<Capabilities explicitly excluded, to prevent scope creep.>

- <capability>

## 7. Functional Requirements

<Numbered, capability-level requirements using MUST / SHALL / MUST NOT,
grouped by capability area, each tied back to the journey it supports. See
writing-conventions.md for phrasing rules.>

### <Capability Area>

- **FR-01:** The system MUST <capability>. _(supports: UJ-01)_
- **FR-02:** Users MUST be able to <action>. _(supports: UJ-01)_

### <Capability Area>

- **FR-03:** The system SHALL <behavior>. _(supports: UJ-02)_
- **FR-04:** The system MUST NOT <restricted behavior>. _(supports: UJ-02)_

## 8. Non-Functional Requirements

<Quality attributes — performance, scalability, security, reliability,
accessibility, compliance — each a measurable target under a stated
condition.>

- **NFR-01:** The system MUST <attribute> within <threshold> under <condition>.
- **NFR-02:** The system SHALL <attribute> within <threshold> under <condition>.

## 9. Constraints

<External limitations the system must operate within, with type.>

- **CON-01:** <constraint> — **type:** technical | budget | timeline | legal | organizational

## 10. Data Overview

<Only if the system is data-heavy. Core domain entities — no implementation-level schema.>

- **<entity>:** <description> | **key attributes:** <...> | **relates to:** <other entity>

## 11. Success Metrics

<Numbered, measurable outcomes, each with a baseline, a target, and a
measurement window, tied back to the goal it measures.>

- **SC-01:** <metric> — **baseline:** <value or "N/A, new capability">, **target:** <value>, **by:** <timeframe>. _(measures: G-01)_
- **SC-02:** <metric> — **baseline:** <value>, **target:** <value>, **by:** <timeframe>. _(measures: G-02)_

## 12. Assumptions

<Beliefs taken as true about users, environment, or existing systems — and
the impact if wrong.>

- **A-01:** <assumption> — **if false:** <impact>

## 13. Dependencies

<External systems, teams, services, or infrastructure this system relies on.>

- **D-01:** <dependency> — **type:** internal | external — **if unavailable:** <impact>

## 14. Glossary

<Optional. Domain-specific terms used in this document that a reader would
need defined to avoid misreading a requirement.>

- **<term>:** <definition>
```

## Section Applicability by System Type

Not every section applies to every case — select the right subset instead of forcing all of them every time:

| System type                                              | Sections to include                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Full new system / platform                               | Every section in the template.                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| New feature added to an existing system                  | Executive Summary, Problem Statement, a minimal Goals (1-2 feature-level goals, still with `G-01`-style IDs — Success Metrics must reference one), User Journeys, Scope, Functional Requirements, relevant Non-Functional Requirements, Success Metrics, Assumptions, Dependencies. Target Users may be folded into the Executive Summary if already established at the system level — nothing else references a Target User by ID. Include Data Overview only if new entities are introduced. |
| Internal tool / small utility                            | Executive Summary, Problem Statement, a lightweight User Journeys, Scope, Functional Requirements, minimal Success Metrics.                                                                                                                                                                                                                                                                                                                                                                    |
| Data- or API-heavy system                                | Always include Data Overview in full.                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Compliance- or safety-sensitive system                   | Expand Non-Functional Requirements and Constraints; every related decision is resolved during elicitation, never deferred.                                                                                                                                                                                                                                                                                                                                                                     |
| Any system with domain-specific or ambiguous terminology | Include Glossary; omit it for plain, self-explanatory systems.                                                                                                                                                                                                                                                                                                                                                                                                                                 |
