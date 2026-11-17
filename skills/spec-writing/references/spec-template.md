# Spec Template

## Coverage and Format

Use these ten sections as the standalone default, or a caller-owned format with equivalent applicable coverage. Replace all instruction placeholders with accepted content. Keep inapplicable sections brief with a reason; a feature without an explicit state machine needs no invented states or transition rows. An unknown decision is not non-applicability.

The feature spec owns behavior and acceptance. Its References point to relevant separately owned product/domain/API/data/UI artifacts; do not copy their detailed contracts or create fictitious links. The Context section can record accepted empirical assumptions and their validation disposition without hiding a missing behavioral decision.

For Gherkin acceptance criteria, use [Gherkin Guidelines](gherkin-guidelines.md) to choose the appropriate structure, wording and notation. The short example below illustrates placement in the document; the guide owns the full presentation rules and patterns.

## Document Structure

````markdown
# Spec: <Feature Name>

> **Status:** <actual review state, normally Draft initially>
> **Owner:** <responsible person or role>
> **Revision:** <document revision under project convention>
> **Last Updated:** <YYYY-MM-DD>

## 1. Context

<Feature purpose, relevant product intent and intended delta. Reference
existing authoritative context by exact section rather than rewriting it.
Briefly define the normative convention and any accepted empirical
assumption, its impact and validation responsibility.>

## 2. Scope

### In Scope

- <included capability and boundary>

### Out of Scope

- <explicit exclusion and boundary/rationale>

## 3. Actors and Flow

### Actors

- **<Actor>:** <role, responsibility and relevant access boundary>

### Preconditions

- <condition needed before the main flow>

### Main Flow

<Reference material alternative/failure scenarios in Acceptance Criteria.
Define their governing obligations in the owning requirements/rules or
transition rows, not only as incidental scenario wording.>

1. <event or actor action>
2. <observable response>
3. <completion>

## 4. Business Rules

- **BR-001:** <explicit domain policy using the agreed normative convention>.
  _(Source: <confirmed decision or authoritative contract>)_

## 5. Functional Requirements

- **FR-001:** <subject> MUST <one cohesive observable obligation under relevant conditions>.
  _(Source: <BR-ID, scope/flow, transition row or exact external contract>)_

## 6. State Transitions

<For explicit state behavior, name the entity and define its states. Use
separate named tables for different entities when needed. Each row owns
its guard, outcome and direct effect. For a stateless feature, state the
reason this section does not apply.>

| From State | Event   | Guard                        | Outcome                     | Observable Effect                                  |
| ---------- | ------- | ---------------------------- | --------------------------- | -------------------------------------------------- |
| <state>    | <event> | <condition or unconditional> | Accepted: <new state>       | <success effect>                                   |
| <state>    | <event> | <failed condition>           | Rejected: <resulting state> | <denial/failure and unchanged data where required> |

<State how unlisted state/event combinations behave, and define applicable
concurrent/duplicate-event behavior and the handling of overlapping guards.
Do not assume every rejection leaves all state unchanged: specify the agreed
result. Reference wider BR/FR obligations rather than creating competing
copies. Keep rows concise; reference named requirements for longer effects.>

## 7. Non-Functional Requirements

### NFR-001: <Quality Criterion>

<Subject> MUST <verifiable quality criterion under defined conditions>.

- **Source/Need:** <feature-specific or inherited requirement>
- **Assessment Basis:** <measurement, inspection or analysis under the
  relevant conditions; reference the criterion rather than redefining it>

## 8. Technical Constraints

- **<Constraint Name>:** <mandated restriction>.
  _(Source: <authority, exact contract section and reason>)_

## 9. Acceptance Criteria

<Concrete scenarios covering success, material failure and relevant
boundaries. Default to Gherkin below; preserve another supplied notation
with equivalent traceability. Use the Gherkin guide to select the
structures the feature needs; the examples below are not a required count.>

```gherkin
Feature: <Feature Name>

  @AC-001
  Scenario: <behavior not grouped by a business rule>
    Given <relevant starting state>
    When <event>
    Then <observable result>

  Rule: BR-001 <policy name>

    @AC-002
    Scenario: <concrete illustration of BR-001>
      Given <relevant starting state>
      When <event>
      Then <observable result>
```

### Coverage

<Repeat scenarios/rows only as needed. Cover every FR and material BR and
transition outcomes. Keep AC identity in its scenario tag; this table
references it and records the covered obligation and observable outcome.
NFR criteria and their assessment basis remain in Section 7.>

| Acceptance ID | Covers                                       | Observable Outcome  |
| ------------- | -------------------------------------------- | ------------------- |
| AC-001        | <FR-ID(s), applicable state/event/guard row> | <observable result> |
| AC-002        | <BR-ID and related FR-ID(s)>                 | <observable result> |

## 10. References

<Include only consulted sources or actual implementation contracts.
Resolve blocking missing contracts before finalization; do not
invent files or links to complete this table.>

| Artifact / Section                                           | Role                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------ |
| [<document title and exact section>](<verified path or URL>) | <source or implementation dependency and why relevant> |
````
