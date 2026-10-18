# Gherkin Guidelines

Rules for writing the Acceptance Criteria block in `spec.md`. Assumes Cucumber-compatible Gherkin. Reference: [cucumber.io](https://cucumber.io/docs/gherkin/reference/)

**Goals:** readable by non-automation stakeholders, deterministic enough for an AI to follow without guessing, automation-ready without leaking implementation details.

This block lives embedded inside `spec.md`, not as a standalone `.feature` file — one `Feature` per spec, authored exactly as shown here.

## Guiding Principles

- **Behavior-driven:** describe _what_ the system does, not _how_ it's built.
- **Specification by example:** each scenario is a concrete, executable example — part documentation, part test.
- **One behavior per scenario**, runnable independently of every other.
- **Written for humans first:** any reader should understand the setup and the expected result without extra explanation.

## Structure

- **One `Feature` per spec.** The purpose of `Feature` is to give a high-level description of the behavior area and group its scenarios.
- **`Rule` groups scenarios by the business rule they illustrate.** Each `Rule` should contain one or more scenarios. In this spec, every `Rule` maps to a `BR-xxx` from the Business Rules section.
- **`Background` is optional, and at most one per `Feature` and one per `Rule`** — never more than one in the same place. Use it only for a `Given` state shared by _multiple_ scenarios in that `Feature` (or that `Rule`); never for a single scenario's setup. Keep it to a handful of steps (roughly 4 lines as a rule of thumb) and make it vivid and concrete rather than abstract — a `Background` long enough that the reader has to scroll back to re-read it has grown too large; move incidental detail into a higher-level `Given` step instead, or split the feature.
- **A `Scenario` not nested in any `Rule` is valid** — `Rule` is optional, so a scenario with no business rule behind it sits directly under `Feature` instead of being forced into an unrelated `Rule` block.
- **`Example` and `Scenario` are synonyms** — use `Scenario` for consistency.
- **`Scenario Outline` (synonym: `Scenario Template`) runs the same scenario once per row of its `Examples` table, and MUST have at least one `Examples` table.** Use it only when the _same_ behavior needs multiple input variations; otherwise write separate `Scenario`s. Steps reference table headers with `<column>` placeholders — this substitution also works inside a Doc String or Data Table attached to the step, not only in the step's own text.
- **Free-form description text** may be placed under `Feature`, `Rule`, `Background`, `Scenario`, or `Scenario Outline`, before any steps, for extra human-readable context — it has no effect on execution. Use sparingly; prefer making the steps self-explanatory instead.

## Formatting

- Indent the body of `Feature`, `Rule`, `Background`, `Scenario`, `Scenario Outline`, and `Examples` by 2 spaces.
- One blank line between adjacent `Scenario` / `Scenario Outline` blocks; no blank line between steps within one scenario or background.
- Keep lines reasonably short (under ~120 characters) for readability.
- Avoid comments (`#` lines) — scenario text should be self-explanatory without one. Gherkin supports them, but they're a sign the steps need rewording, not annotating.
- Use double quotes (`"`) for string parameters in steps.
- **Colon placement is not optional and not symmetric.** `Feature:`, `Rule:`, `Background:`, `Scenario:`, `Scenario Outline:`, and `Examples:` each take a colon. `Given`, `When`, `Then`, `And`, `But`, and `*` never do — adding one there, or dropping one from a section keyword, produces invalid Gherkin that silently fails to parse as intended.

## Vocabulary

- One stable vocabulary for roles, domain objects, and states throughout.
- Never swap synonyms for the same concept (e.g. "order" vs "purchase") unless the product genuinely distinguishes them.

## Steps

- Third person, present tense, subject–predicate ("the system sends...", not "send..." or "I will send...").
- Proper grammar; minimal punctuation.
- `Given` / `When` / `Then` map to Arrange / Act / Assert:
  - `Given` puts the system in a known starting state — incidental, something that already happened. Avoid describing user interaction here; these are preconditions.
  - `When` describes one event or action — a person interacting with the system, or an event from another system.
  - `Then` describes an observable, checkable outcome — what changed, what a user sees, what gets reported. Never verify something only visible inside internal storage; verify what's observable from the outside.
- Strict `Given` → `When` → `Then` order; never repeat a phase within one scenario — split into separate scenarios instead.
- Use `And` / `But` to continue the same phase instead of repeating the keyword. `*` may replace any step keyword when a set of steps reads more like a plain list than a narrative.
- Never use `Or` as a step keyword — if a choice matters, use separate scenarios or a `Scenario Outline`.
- Don't combine multiple actions or assertions with "and" inside one step line — split into separate steps instead.
- **Avoid steps whose text collides once the keyword is dropped** — Gherkin matches step text independent of `Given`/`When`/`Then`, so `Given there is money in my account` and `Then there is money in my account` are the same step text and become ambiguous. State the fact precisely instead: `Given my account has a balance of "$430"` / `Then my account should have a balance of "$430"`.
- **"Imagine it's 1922."** Phrase `When` steps around what a person could conceivably do without software, not around today's interface or technology — this keeps steps behavior-level instead of implementation-level.

### Domain level, not implementation level

- Describe actors and system behavior in product language — not framework, interface, or storage mechanics.
- Never put selectors, XPath, "click", "scroll to", HTTP endpoints, SQL, or raw schema into step text, unless the behavior being specified is inherently at that layer (e.g. a feature whose entire behavior is an external integration or protocol).
- Prefer a meaningful starting **state** in `Given` over a click-by-click tour, unless the interaction path itself is what the scenario specifies.
- Use the minimal `Given` context a reader needs to understand the behavior — omit setup that doesn't change the example's meaning.

### Scope per scenario

- Never bundle independent concerns into one scenario (e.g. core behavior plus performance or security checks) — split them, unless the scenario is explicitly and legitimately about the behavior spanning both.
- Target 3–5 steps per scenario; treat 10 as the outer limit, not a target to approach — beyond it, split the scenario or restructure it around a table.

### Example data

- Use concrete, realistic values (names, amounts, dates) so the scenario reads as a believable example.
- Avoid meaningless placeholders (`foo`, `bar`, `test`) unless the scenario is deliberately about generic, invalid, or nonsensical input.

## Tags

- `@AC-xxx` tags a `Scenario` or `Scenario Outline` with its ID — the sole mechanism for numbering one. A tag can also sit above a `Feature` or `Rule` to apply to every scenario beneath it.

## Step Arguments

### Doc Strings

For a multiline or structured payload (e.g. a body of text, JSON, XML):

```gherkin
Given a message with body
  """
  Some content here,
  across multiple lines.
  """
```

- Delimit with `"""` or, equivalently, three backticks (` ``` `) on their own line — useful for Markdown-flavored content, though not every tool renders backticks yet.
- Optionally annotate the content type right after the opening delimiter (e.g. `"""json`) for tooling that understands it.
- Indentation of the opening delimiter is not significant; indentation _inside_ the doc string is — each line is dedented relative to the opening delimiter.

### Data Tables

For a list of values passed to one step:

```gherkin
Given the following accounts exist:
  | name  | email           | plan |
  | Ada   | ada@example.com | Pro  |
  | Grace | gh@example.com  | Free |
```

- Use short, descriptive, kebab-case-or-single-token headers.
- Keep step tables and `Examples` tables small enough to read on one screen; a table that keeps growing is a sign the scenario is drifting into pure data-driven testing rather than a specific example.
- Escape a literal newline in a cell as `\n`, a literal `|` as `\|`, and a literal `\` as `\\`.

## Language of the Scenarios

Gherkin's keywords are localized for many spoken languages — the language chosen should match the language domain experts actually use when discussing the feature, not be translated from it. This file's examples are in English; if the project's business language is not English, use that language consistently and the matching localized keywords instead, noting the choice at the top of the Acceptance Criteria block.

## Anti-Patterns

- Multiple unrelated behaviors or assertions crammed into one scenario.
- Independent quality concerns (functional + performance, functional + security) mixed into a single scenario instead of split.
- Automation selectors, DOM structure, HTTP/SQL, or other implementation mechanics encoded directly into step text.
- Navigation/click sequences used where a starting state would communicate the same precondition more clearly.
- A bloated `Given` chain that sets up context the scenario never uses.
- A vague `Then` ("it works", "it succeeds", "the user is logged in") with no observable signal stated.
- Placeholder example data that doesn't read like a real example.
- `Scenario Outline` used to generate rows with no distinct behavioral value — effectively a data dump, not a specification.
- A scenario or table so long no one would actually read it end to end.
- Step text that collides with another step once its keyword is dropped.

## Quick Checklist

Before a scenario is finalized, confirm:

- [ ] One behavior only; runs independently of every other scenario.
- [ ] No unrelated concerns bundled into it.
- [ ] Consistent vocabulary; no synonym swapping.
- [ ] Domain-level language; no interface, automation, or storage mechanics leaked into steps.
- [ ] State preferred over navigation, unless the path is the point.
- [ ] Minimal but sufficient `Given` context.
- [ ] Concrete, realistic example data.
- [ ] Third person, present tense, one clear action or assertion per step.
- [ ] Strict `Given` → `When` → `Then` order; `Then` is observable and checkable.
- [ ] No step's text collides with another step once the keyword is dropped.
- [ ] 3–5 steps typical, 10 as the outer limit.
- [ ] Colons only after `Feature`/`Rule`/`Background`/`Scenario`/`Scenario Outline`/`Examples`, never after `Given`/`When`/`Then`/`And`/`But`.
- [ ] At most one `Background` per `Feature` and one per `Rule`.
- [ ] Every `Scenario Outline` has at least one `Examples` table.
- [ ] Every `Rule` block maps to a `BR-xxx`; every `Scenario` carries an `@AC-xxx` tag; a scenario with no `BR` sits directly under `Feature`.

## Reference Template

```gherkin
Feature: <behavior area>
  As a <role>
  I want <goal>
  So that <reason>

  Background:
    Given <state shared by every scenario in this Feature — omit if not needed>

  @AC-001
  Scenario: <behavior with no Business Rule behind it — implements an FR only>
    Given <context>
    When <action>
    Then <observable outcome>

  Rule: <maps to BR-001>

    @AC-002
    Scenario: <single behavior>
      Given <context>
      And <additional context>
      When <action>
      Then <observable outcome>
      And <additional observable outcome>

    @AC-003
    Scenario: <single behavior, using a data table>
      Given the following <domain entities> exist:
        | <column-a> | <column-b> |
        | <value-1>  | <value-2>  |
      When <action>
      Then <observable outcome>

    @AC-004
    Scenario Outline: <same behavior, varying inputs>
      Given <context>
      When <action> with "<input>"
      Then the outcome is "<outcome>"

      Examples:
        | input   | outcome   |
        | <case1> | <result1> |
        | <case2> | <result2> |

  Rule: <maps to BR-002>

    @AC-005
    Scenario: <single behavior>
      Given <context>
      When <action>
      Then <observable outcome>
```
