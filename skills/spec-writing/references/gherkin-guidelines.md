# Gherkin Guidelines

Use Gherkin to present acceptance criteria as concrete examples of feature behavior. Write for stakeholders and AI readers: the starting situation, event and expected outcome should be understandable without guessing or inspecting implementation details. The [official Gherkin reference](https://cucumber.io/docs/gherkin/reference/) defines the notation.

The acceptance criteria belong in a fenced `gherkin` block within the feature specification. This guide covers how to choose and present that block's structure, steps, example data and identifiers.

## Guiding Principles

- **Behavior first.** Describe what actors and external consumers observe, using the feature's domain vocabulary.
- **Concrete examples.** Show meaningful situations and outcomes rather than restating a requirement in abstract terms.
- **One cohesive behavior per scenario.** Related outcomes can belong together; independent concerns need separate examples.
- **Self-contained scenarios.** State the context each example needs without depending on another scenario's outcome or order.
- **Readable before compact.** Include enough detail to remove ambiguity, then remove incidental setup and repetition.
- **Faithful to the specification.** Scenarios illustrate agreed requirements and rules; they do not introduce unapproved behavior or exceptions.

## Choosing the Structure

### Feature

Use one `Feature` for the behavior area covered by the specification. Give it a meaningful name. An optional description explains purpose and context; the `As a` / `I want` / `So that` form is useful when it adds clarity, but is not mandatory.

### Rule

A `Rule` groups one or more scenarios illustrating one business rule. Include its `BR-xxx` identifier in the name so the relationship is explicit. Use separate `Rule` blocks for distinct policies rather than gathering unrelated examples under a broad label.

`Rule` is optional. A scenario without an appropriate business-rule grouping belongs directly under `Feature`; do not invent a BR merely to group it. Place these ungrouped scenarios before the `Rule` blocks. Indentation alone does not return a later scenario to `Feature` scope after a `Rule`.

### Background

Use an optional `Background` for preconditions shared by multiple scenarios in the same `Feature` or `Rule`. There can be at most one feature `Background` and one `Background` per rule. Each belongs before the scenarios in its container; feature-level context also applies to scenarios inside its rules.

Keep `Background` short, concrete and relevant to every scenario it affects. Around four short steps is a useful readability guide, not a syntax limit. Put a scenario-specific precondition in that scenario instead. If readers must repeatedly scroll back to understand the context, simplify the shared description or reconsider the grouping.

### Scenario

Use `Scenario` for one concrete example. `Example` is an equivalent keyword; prefer `Scenario` consistently within a document. The name should describe the behavior or distinguishing outcome, not just repeat the feature name.

### Scenario Outline and Examples

Use `Scenario Outline` when the same behavior and step structure need several meaningful value combinations. `Scenario Template` is an equivalent keyword.

- Include at least one `Examples` table with a header and concrete data rows.
- Reference column headers using `<parameter>` in the steps.
- Parameter substitution can also appear in an attached `Doc String` or `Data Table`.
- Multiple `Examples` tables can separate meaningful categories of values; label them when helpful.
- Use separate scenarios when the behavior or narrative differs, rather than forcing unrelated cases into one outline.
- Include boundary and invalid cases where they reveal a relevant distinction. Avoid a large inventory of interchangeable rows.

### Descriptions and Comments

Short free-form descriptions can appear under `Feature`, `Rule`, `Background`, `Scenario` and `Scenario Outline` before their structured content. Keep them relevant and avoid beginning a description line with a Gherkin keyword.

Full-line comments start with `#`, optionally preceded by whitespace. Use comments sparingly for helpful context; they must not carry an outcome or rule that is missing from the scenario. Prefer clear names and steps over explanations of unclear wording. Inline comments are not part of this comment syntax.

## Formatting

- Put `:` after `Feature`, `Rule`, `Background`, `Scenario`, `Scenario Outline` and `Examples`, or their localized equivalents.
- Do not put `:` between `Given`/`When`/`Then`/`And`/`But`/`*` and the step text. A colon later in step text is allowed, such as `Given the following accounts exist:`.
- Prefer two-space indentation for each nested level. Keep `Rule` scenarios visibly nested under their `Rule` and step arguments under the step they describe.
- Separate neighboring scenarios, outlines and `Rule` blocks with blank lines. Keep the steps of one scenario together.
- Keep lines reasonably short, roughly 120 characters where practical. Wrap descriptions without relying on a source newline to create a separate field or step.
- Use double quotes consistently around string values when they help distinguish data from prose.
- Use matching Markdown fences. If the example contains triple backticks, use an outer fence of four or more backticks.

## Vocabulary

Use one stable term for each actor, domain object, action and state. Do not alternate between synonyms such as "order" and "purchase" unless the product distinguishes them. Match terminology and identifiers in the owning requirements.

Prefer explicit subjects and consistent present-tense descriptions. Third-person wording is a useful default; a consistent first-person domain narrative is also valid. Meaning and clarity matter more than enforcing a grammatical style for its own sake.

## Writing Steps

### Given: Starting Context

State the relevant initial situation: actor permissions, existing domain objects, current state and conditions that affect the outcome. Prefer a meaningful starting state over a navigation history. Omit setup that does not change the example's meaning.

A prior action may explain how that state arose, but `Given` should not hide the main action whose outcome the scenario describes.

### When: Event or Action

Describe the event that causes the behavior: an actor's request, elapsed time or an event from another system. Make the actor and affected object clear.

Prefer domain actions over interface mechanics. Describe an interaction or protocol explicitly when that interaction is itself the required behavior; do not obscure it with an artificial nontechnical analogy.

### Then: Observable Outcome

State the resulting response, visible state, denial, notification or other observable effect. Replace "it works" or "it succeeds" with the actual result and its relevant values.

For uniqueness, retry or data-integrity behavior, describe the public result and subsequent read behavior. A hidden database row count or internal object is not a substitute for the actor-facing outcome. Keep other members' data and unchanged state explicit when those are part of the agreed behavior.

### Sequence and Continuation

- Prefer `Given`, then `When`, then `Then` as a clear narrative. Gherkin permits other sequences; a sequence's meaning must still be clear.
- Use `And`/`But` to continue the preceding phase instead of repeating its keyword. Use `But` when it communicates a meaningful contrast.
- `*` can replace a step keyword when a list is clearer than a narrative; retain an understandable distinction between context, action and outcome.
- `Or` is not a step keyword. Use separate scenarios or outline rows for meaningful alternatives.
- Keep each step focused. Separate independently meaningful actions or outcomes rather than joining them into a long sentence. Related conditions may remain together when splitting them would obscure one coherent obligation.
- If a failure-and-recovery example needs another action/outcome pair, keep the causal sequence explicit and confined to that one recovery behavior. Split independent paths rather than writing a long tour of the feature.
- Do not rely on a different keyword to give identical step text contradictory meanings. Make the starting fact and expected change distinguishable in the wording.

### Domain Detail and Scenario Size

Avoid selectors, XPath, internal class names, SQL, storage layout and click-by-click navigation unless the specified interface is inherently the subject. An externally visible protocol can legitimately require protocol terminology; keep its detailed contract with its authoritative definition.

Often 3–5 steps communicate one example well. Length is a readability signal, not a hard limit. If a scenario grows, remove incidental setup, use a suitable step argument or split unrelated behaviors. Do not shorten an example by hiding a necessary outcome.

Security, performance or recovery may be the central behavior of a scenario. Do not bundle independent quality concerns into an ordinary success path, but retain related effects needed to understand the behavior being specified.

### Example Data

Use concrete, plausible names, amounts, dates and states. State any relevant time zone, ordering or boundary condition rather than relying on the reader's environment. Use identifiers consistently without implying a particular identifier format unless it is required.

Avoid meaningless `foo`/`bar` values unless nonsensical input is the point. The angle-bracket instructions in the templates below must be replaced in final content; outline parameters such as `<quantity>` intentionally remain and must match their `Examples` headers.

## Tags and Traceability

Give each `Scenario` or `Scenario Outline` a unique `@AC-xxx` tag immediately above it. This tag is its acceptance-criterion identity; do not add a second competing number in the scenario title. Preserve existing IDs during revisions, and do not recycle retired ones.

Other descriptive tags may group examples. Tags on `Feature` or `Rule` apply to the scenarios beneath them, so do not place a unique AC identity on those containers. Each outline has one AC identity; its rows are examples of that criterion, not separate AC IDs.

Name each `Rule` with its BR ID. Keep the scenario's relationship to functional requirements and relevant state behavior explicit in the specification's coverage mapping or equivalent references. A scenario can illustrate several related requirements without combining unrelated behaviors.

## Step Arguments

### Doc Strings

Use a `Doc String` for multiline text or a structured payload whose actual content matters to the example. Place it directly beneath the step it describes.

```gherkin
Given a notification with the following body
  """text/plain
  Your reservation is confirmed.
  Keep this message for your records.
  """
```

- Use matching triple double quotes or triple backticks on separate lines.
- An optional content type follows the opening delimiter, such as `text/plain` or `json`.
- Align the closing delimiter with the opening delimiter for readability.
- Content is dedented relative to the opening delimiter. Preserve any additional indentation that belongs to the content itself.
- If using triple backticks, use a longer outer Markdown fence to keep the sample intact.

### Data Tables

Use a `Data Table` for structured information belonging to one step, not for alternative scenarios.

```gherkin
Given the following accounts exist:
  | name  | email             | plan |
  | Ada   | ada@example.com   | Pro  |
  | Grace | grace@example.com | Free |
```

- Use clear, short headers with consistent naming.
- Keep rows aligned for source readability. Row meaning must be clear from the preceding step and headers.
- A `Data Table` describes one step's data; an `Examples` table supplies alternative values for an outline.
- Escape a newline, literal pipe and literal backslash in a cell as `\n`, `\|` and `\\` respectively.
- Keep tables focused enough to read as examples. Split meaningful categories rather than accumulating a large data dump.

## Language of the Scenarios

Use the agreed documentation/domain language consistently. For localized Gherkin, put `# language: <code>` on the first line of the Gherkin block and use that language's exact keywords. English is the default when no language directive is present.

Keep machine identifiers such as `BR-001`, `FR-001` and `AC-001` unchanged. Translate descriptions and step prose consistently with the chosen domain vocabulary; do not mix keyword dialects within a block.

## Anti-Patterns

- Unrelated behaviors or action sequences in one scenario.
- A vague outcome with no observable signal.
- Hidden storage or implementation details replacing the required public outcome.
- A navigation tour where a starting state would communicate the same context.
- A `Background` containing conditions irrelevant to some affected scenarios.
- Scenario names, steps and referenced requirements using inconsistent terms.
- Outline rows that add volume but no distinct behavioral information.
- Data Tables confused with `Examples` tables.
- A required rule or outcome stated only in a description or comment.
- An AC identity inherited from `Feature`/`Rule` or reused across scenarios.
- A scenario depending on another scenario's outcome.

## Quick Checklist

Before finalizing the acceptance criteria, review:

- [ ] One cohesive behavior per scenario, with all necessary context stated.
- [ ] Faithful coverage of agreed rules and requirements, including relevant failure and boundary outcomes.
- [ ] Concrete, meaningful data and consistent domain vocabulary.
- [ ] Clear context/action/outcome, with observable `Then` results.
- [ ] No incidental interface or internal storage mechanics replacing domain behavior.
- [ ] `Background` used only for relevant shared preconditions and placed before its container's scenarios.
- [ ] Ungrouped scenarios placed before `Rule` blocks; each `Rule` names its BR ID.
- [ ] Each `Scenario`/`Scenario Outline` has a unique scenario-level AC tag.
- [ ] Every outline parameter matches an `Examples` header and has meaningful concrete rows.
- [ ] Data Tables and Doc Strings belong to the intended preceding step; escaping and delimiters are correct.
- [ ] Correct colon placement, readable indentation and matching Markdown fences.
- [ ] Agreed language/dialect, with a language directive when needed.
- [ ] No unresolved instruction placeholder or unapproved choice in final content.

## Reference Templates

Select only the structures the feature needs. These patterns illustrate placement and relationships; they do not require every feature to have `Background`, `Rule`, `Scenario Outline`, tables or multiline content.

### Feature, Background and Standalone Scenario

```gherkin
Feature: <behavior area>
  <short purpose or context, if helpful>

  Background:
    Given <state shared by the feature's scenarios>

  @AC-001
  Scenario: <behavior without a business-rule grouping>
    Given <additional context specific to this scenario>
    When <domain action or event>
    Then <observable result>

  @AC-002
  Scenario: <another behavior sharing the background>
    Given <a different relevant starting condition>
    When <domain action or event>
    Then <observable result for this condition>
```

### Rules and Rule-Level Background

```gherkin
Feature: <behavior area>

  @AC-001
  Scenario: <ungrouped behavior, placed before the rules>
    Given <context>
    When <event>
    Then <observable outcome>

  Rule: BR-001 – <policy illustrated by this group>

    Background:
      Given <context shared by multiple scenarios in this rule>

    @AC-002
    Scenario: <accepted case>
      Given <case-specific context>
      When <event>
      Then <observable outcome>
      And <related observable outcome>

    @AC-003
    Scenario: <boundary or rejected case>
      Given <case-specific boundary condition>
      When <event>
      Then <observable rejection>
      And <required unchanged public state>

  Rule: BR-002 – <another policy>

    @AC-004
    Scenario: <behavior illustrating the second policy>
      Given <context>
      When <event>
      Then <observable outcome>
```

### Scenario Outline with Examples

In this pattern, `<available>` and `<requested>` are intentional outline parameters. The two rows illustrate distinct boundary conditions for the same behavior.

```gherkin
Feature: Reserve available places

  Rule: BR-001 – Reservations cannot exceed availability

    @AC-001
    Scenario Outline: Reject requests exceeding availability
      Given a session has <available> available places
      When a participant requests <requested> places
      Then the request is rejected
      And the session still has <available> available places

      Examples:
        | available | requested |
        | 0         | 1         |
        | 1         | 2         |
```

### Scenario with a Data Table

```gherkin
Feature: View the member directory

  @AC-001
  Scenario: Show the listed members
    Given the following members belong to the directory:
      | name  | role   |
      | Ada   | editor |
      | Grace | reader |
    When an administrator views the directory
    Then the directory lists Ada as an editor and Grace as a reader
```

### Scenario with a Doc String

```gherkin
Feature: View a reservation notification

  @AC-001
  Scenario: Show the confirmation message
    Given a participant has a confirmed reservation with this notification:
      """text/plain
      Your reservation is confirmed.
      Keep this message for your records.
      """
    When the participant opens the notification
    Then the displayed message contains the confirmation and record-keeping instruction
```

AC identifiers restart in these separate template illustrations for readability. In a single finished specification, every scenario/outline identity must remain unique across its `Feature` and `Rule` groups.
