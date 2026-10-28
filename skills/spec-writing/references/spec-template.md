# Spec Template

Fill this exact structure end to end. Every `<...>` placeholder must be replaced with concrete, specific content before the file is written — none may remain in the output.

````markdown
# Spec: <Feature Name>

> **Status:** Draft | Approved
> **Owner:** <name>
> **Date:** <YYYY-MM-DD> — v<N>

## 1. Context

<Why this feature exists and what it's for, in a few sentences. If a PRD or similar upstream document exists, this is a
short pointer to it, not a restatement.>

## 2. Scope

<Capability-level, not atomic or testable — a noun-phrase inventory of what's delivered and what isn't. The atomic,
testable breakdown of an In Scope item belongs in Functional Requirements, not here.>

### In Scope

<Capabilities this feature delivers.>

- <capability>

### Out of Scope

<Capabilities explicitly excluded from this feature.>

- <capability>

## 3. Actors and Flow

### Actors

<Identify the users, roles, or external/internal systems that interact with or trigger this feature.>

- **<actor>:** <responsibility or interaction with this feature, including relevant access permissions if applicable.>

### Preconditions

<Conditions that must hold before the main flow can start.>

- <precondition>

### Main Flow

<The primary, happy-path sequence. Alternative and failure paths are captured as Acceptance Criteria scenarios, not duplicated here.>

1. <step>
2. <step>

## 4. Business Rules

<A business rule is a policy or constraint of the domain itself — true regardless of which flow or action is in play, and true
whether or not software enforces it. One rule commonly implies several functional requirements. If a rule is entirely about one
specific state transition — whether it's valid, and what happens as a direct result — it belongs only in State Transitions below,
not restated here. Each rule here is later illustrated by a Rule block in Acceptance Criteria.>

- **BR-001:** <rule>

## 5. Functional Requirements

<A functional requirement is one atomic, testable thing the system does at a specific point — not a standing policy. Most operationalize
a Business Rule above and reference it; one that's a direct, uncontentious consequence of the Main Flow with no real "rule" behind it
doesn't need a reference. Every requirement here, with or without a reference, MUST be exercised by at least one Acceptance Criteria
scenario — see the Acceptance Criteria section below for how a requirement with no Business Rule behind it gets covered, either inside
an existing scenario or, if nothing else fits, its own.>

- **FR-001:** The system MUST <behavior>. _(implements: BR-001)_
- **FR-002:** The system MUST <behavior>.
- **FR-003:** The system MUST NOT <restricted behavior>.

## 6. State Transitions

<Only if this feature has an explicit state machine. Omit the section entirely otherwise. This table is the single source of truth for which
transitions are valid — a Business Rule above should not restate the same transition logic in prose. Leave no cell blank — write "N/A" where a
column doesn't apply to that row (e.g. Guard/Condition when nothing extra gates the transition, Expected Behavior when the row is invalid,
Rejection Behavior when the row is valid).

- From State: the state the entity is in immediately before the event.
- Event/Trigger: the action or event that attempts the transition.
- Guard/Condition: any condition required beyond the state and trigger alone for the transition to be valid. N/A if nothing extra gates it.
- To State: the resulting state if the transition is valid. N/A if invalid.
- Valid: Yes or No.
- Expected Behavior: what the system does when the transition succeeds. N/A if invalid.
- Rejection Behavior: what the system does when the transition is rejected. N/A if valid.
>

| From State | Event/Trigger | Guard/Condition     | To State        | Valid  | Expected Behavior  | Rejection Behavior |
| ---------- | ------------- | ------------------- | --------------- | ------ | ------------------ | ------------------ |
| <state>    | <event>       | <condition, or N/A> | <state, or N/A> | Yes/No | <behavior, or N/A> | <behavior, or N/A> |

## 7. Non-Functional Requirements

<A quality attribute with a measurable target under a stated condition — answers "how well" the feature behaves (how fast, how available, how
resilient). Checked against the category list in elicitation-flow.md — only the categories that actually apply to this feature appear here. Not
the same as a Technical Constraint below, which restricts _how_ the feature is built rather than setting a quality target.>

- **NFR-001:** The system MUST <attribute> within <threshold> under <condition>.

## 8. Technical Constraints

<A restriction on the approach, technology, or existing code this feature MUST or MUST NOT use — not a quality target (that's a Non-Functional
Requirement above). If it can be phrased as "must perform at level X", it's an NFR; if it's phrased as "must/must not use Y", it's a constraint.>

- <constraint>

## 9. Acceptance Criteria

<Written as Gherkin. See gherkin-guidelines.md for the full writing rules. A Rule block maps to a Business Rule above and groups the scenarios
that illustrate it. A Functional Requirement with no Business Rule behind it is exercised wherever it naturally fits — inside a Rule-grouped
scenario if one already covers it, or, if none does, its own Scenario written directly under Feature, not nested in any Rule block. Every Scenario
carries a sequential @AC-xxx tag, and together the scenarios here exercise every FR-xxx above.>

```gherkin
Feature: <Feature name>
  As a <role>
  I want <goal>
  So that <reason>

  @AC-001
  Scenario: <behavior with no Business Rule behind it — implements FR-00x only>
    Given <context>
    When <action>
    Then <observable outcome>

  Rule: <maps to BR-001>

    @AC-002
    Scenario: <behavior>
      Given <context>
      When <action>
      Then <observable outcome>
```

## 10. References

<Every document this spec was actually informed by while drafting it, and every document an implementer will need to open — for example the
originating PRD, or this feature's UI/UX design, data model, or API contract documents, if they exist. Not a general "see also" list: each
entry was either a source for this spec's content or is something implementation will need to look up.>

| File               | Purpose                |
| ------------------ | ---------------------- |
| [<filename>](path) | <what it's needed for> |
````
