# PRD Template

Use these fourteen numbered sections for a fresh standalone PRD. Replace all instructions/placeholders, keep only real entries and apply [Writing Conventions](writing-conventions.md). Do not copy sample counts as requirements. Use a caller-supplied template when provided, preserving equivalent coverage. Metadata describes actual authorship/review state; it does not grant approval.

## Coverage and Applicability

Keep all fourteen headings in the default format so coverage is visible. A genuinely inapplicable section can contain one specific reason (for example, no external dependency beyond the already defined parent-product services). Do not fill a gap with "None" unless established; unknown is not inapplicable. Scale detail rather than dropping goals, users, constraints or success measures for a small feature.

For a feature, identify the parent product/version and inherited requirements by precise reference, state changed versus unchanged behavior and avoid duplicating the parent baseline. For a whole product, cover end-to-end roles and major capabilities. Data Overview applies whenever data meaning, sensitivity, retention or lifecycle affects scope, not only for data-heavy systems or new entities. Expand applicable safety/compliance constraints with qualified input; do not invent obligations or claim certification. Glossary is brief when terminology is already unambiguous.

## Document Structure

```markdown
# PRD: <Product or Feature Name>

> **Status:** <actual document review state, normally Draft initially>
> **Owner:** <responsible person or role>
> **Revision:** <document revision under project convention, initially 1>
> **Last Updated:** <YYYY-MM-DD for this document revision>
> **Context:** <product boundary or feature and parent-product reference>

## 1. Executive Summary

<Problem, intended users, proposed capability and expected value in one
short paragraph. State whether this covers a product or feature.>

## 2. Problem Statement

<Current situation, affected users, consequence and why now. Separate
observed evidence from stakeholder hypotheses; cite relevant sources.>

## 3. Goals

- **G-01:** <intended outcome and affected population; related context>

## 4. Target Users

### <Role or Segment>

- **Role:** <primary or secondary, where relevant>
- **Context and Need:** <situation, intended outcome and pain point>
- **Access Conditions:** <relevant access or operational conditions>

## 5. User Journeys

### UJ-01: <Journey Name>

- **Actor:** <role or segment from Target Users>
- **Priority:** <agreed priority and brief rationale>
- **Supports:** <G-ID(s)>
- **Goal:** <user outcome>
- **Trigger:** <initiating event and relevant precondition>
- **Main Flow:**
  1. <initiating user action or event>
  2. <meaningful interaction and system response>
  3. <completion step>
- **Success Outcome:** <observable end state and delivered value>
- **Failure or Recovery:** <material alternative outcome and recovery;
  use a separate short numbered flow when branching needs explanation>

## 6. Scope

### In Scope

- <included capability and boundary for this release/change>

### Out of Scope

- <explicit exclusion and relevant boundary/rationale>

## 7. Functional Requirements

### <Capability Area>

#### FR-01: <Short Requirement Name>

<Subject> MUST <observable behavior under relevant condition>.

- **Supports:** <UJ-ID(s), or G/CON-ID and rationale for a cross-cutting need>
- **Verification Basis:** <observable outcome or assessment criterion;
  not a full downstream test procedure>

## 8. Non-Functional Requirements

### NFR-01: <Quality Attribute>

<Subject> MUST <verifiable quality criterion under stated conditions>.

- **Source/Need:** <goal, journey or constraint>
- **Verification:** <measurement, test, inspection or analysis basis>

## 9. Constraints

### CON-01: <Constraint Name>

<Confirmed limitation>.

- **Type:** <technical, budget, timeline, legal or organizational>
- **Source/Rationale:** <authority and reason for the limitation>

## 10. Data Overview

### <Concept>

<Business meaning and relevant information>.

- **Relationships:** <relevant domain relationships>
- **Lifecycle/Sensitivity:** <applicable ownership, access, retention,
  deletion or migration obligations; reference requirements rather than
  defining a second copy of the rule>

## 11. Success Metrics

### SC-01: <Outcome Measure>

- **Measures:** <G-ID(s)>
- **Baseline:** <observed value/source, or agreed collection plan>
- **Target:** <agreed concrete success threshold or observable criterion>
- **Population:** <users, events or other units included in the measure>
- **Measurement Method:** <data source and calculation or observation method>
- **Measurement Window:** <duration and start/end condition>

## 12. Assumptions

### A-01: <Assumption Name>

<Accepted empirical assumption and its basis>.

- **If False:** <scope/feasibility impact>
- **Validation Owner:** <responsible role>
- **Validation Plan:** <method and decision point>

## 13. Dependencies

### D-01: <Dependency Name>

<External/internal system, team or service and required capability>.

- **Owner:** <responsible party>
- **Readiness:** <required condition and timing>
- **If Unavailable:** <impact and agreed response>

## 14. Glossary

- **<Term>:** <one precise meaning used throughout; authoritative reference
  when a shared definition already exists>
```

## Completion

Final content has no instruction placeholders, unanswered questions or unapproved product choices. An agreed plan is a concrete decision, not proof its future measurement or dependency is already satisfied. Success targets must be resolved before finalization; a promise to choose them later does not satisfy this requirement. Use the document's actual review state, not "Approved" merely because all sections are populated.
