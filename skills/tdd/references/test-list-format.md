# Test List Format

Templates and rules for the test list file, the review view, the revision view, and the in-loop update. Use them exactly so every run has the same structure. Placeholders appear as `<...>`.

## Test list file (for the agent)

A temporary working file and the source of truth for the loop.

- Outside version-controlled source, or at a path the project already ignores. Never commit it. Tell the user the path.
- Keep the section order and column order of the template.
- Row order in `Items` is the execution order.

### Template

```markdown
# Test List: <change in one line>

## Context

| Field             | Value                                                            |
| ----------------- | ---------------------------------------------------------------- |
| Change            | <one line>                                                       |
| Sources           | <requirement, acceptance criteria, bug report, or existing code> |
| Applicable levels | <levels> (source: <project rule files or user instructions>)     |
| Seam              | <public interface where behavior is observed>                    |
| Focused run       | `<command>`                                                      |
| Full run          | `<command>`                                                      |
| Baseline          | <result; pre-existing failures, or "none">                       |
| Confirmation      | <"unconfirmed" or "confirmed">                                   |

## Items

| ID   | Group   | Test        | Behavior                       | Expected                          | Source of expected                    | Level   | Status  |
| ---- | ------- | ----------- | ------------------------------ | --------------------------------- | ------------------------------------- | ------- | ------- |
| <ID> | <Group> | <test name> | <condition and concrete input> | <literal value, error, or effect> | <where the expected value comes from> | <level> | pending |

## Coverage Map

| Requirement or acceptance criterion | Item IDs            |
| ----------------------------------- | ------------------- |
| <criterion>                         | <IDs, or "NO ITEM"> |

## Not Tested

| Behavior   | Reason   |
| ---------- | -------- |
| <behavior> | <reason> |

## Planned Doubles

| Boundary   | Double kind                | Basis                                                      |
| ---------- | -------------------------- | ---------------------------------------------------------- |
| <boundary> | <fake, stub, spy, or mock> | <source, documentation, or real sample the double mirrors> |

## Decisions

| ID             | User decision          |
| -------------- | ---------------------- |
| <ID or "list"> | <decision in one line> |

## Added in Loop

| ID   | Behavior   | Source   |
| ---- | ---------- | -------- |
| <ID> | <behavior> | <source> |

## Evidence

| ID   | RED (command → failure message) | GREEN (command → result) | REFACTOR                         |
| ---- | ------------------------------- | ------------------------ | -------------------------------- |
| <ID> | <command → message>             | <command → result>       | <what changed, or "none needed"> |
```

Write `None.` under a heading that has no content..

### Field rules

**Items rules:**

| Field              | Rule                                                                                                                                                                                                                  |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID                 | Short prefix plus number. Unique, stable, never renumbered or reused.                                                                                                                                                 |
| Group              | Exactly one value from the Group table below.                                                                                                                                                                         |
| Test               | Name of the test this item belongs to. Items with the same name are rows of one data-driven test. A single-item test has its own name.                                                                                |
| Behavior           | The condition plus a concrete input, in domain language. Describe observable behavior, never implementation.                                                                                                          |
| Expected           | A literal value, an error type, or an observable effect. Never a formula or a reference to the code. `needs decision` is allowed only with status `needs-confirmation`, or `dropped` after the user dropped the item. |
| Source of expected | A requirement ID, a document and section, existing code (current behavior), or a short hand computation (for example, `8.00 + 1.50 × 1`). Never `assumed` or `obvious`.                                               |
| Level              | One of the applicable levels.                                                                                                                                                                                         |
| Status             | One value from the status table below.                                                                                                                                                                                |

| Group              | Meaning                                                                                            |
| ------------------ | -------------------------------------------------------------------------------------------------- |
| `happy path`       | The main successful scenario                                                                       |
| `alternative path` | Another valid scenario: other partitions, rules, or transitions, or an unusual but valid condition |
| `boundary`         | A value at or next to a limit                                                                      |
| `invalid input`    | Input or event the system must reject or ignore                                                    |
| `error handling`   | Behavior when a dependency or the environment fails (timeout, error response, partial failure)     |
| `regression`       | Existing behavior that must not change                                                             |

| Status               | Meaning                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `pending`            | Confirmed and not started                                                                   |
| `in-progress`        | The current cycle is working on it                                                          |
| `done`               | RED and GREEN observed (or the exception in Core Principle 7 applied), refactoring finished |
| `dropped`            | Removed; the reason is in `Decisions`                                                       |
| `needs-confirmation` | Expected behavior cannot be derived; blocks the loop until the user resolves it             |

**Other section rules:**

- **Context > Confirmation:** set to `confirmed` only after the user approves every Group.
- **Coverage Map:** when the request has no acceptance criteria, use the expected behavior stated in the request or bug report. A row with no items stays visible as `NO ITEM`.
- **Decisions:** record every user answer that changes the list (resolved questions, drops, approved edits to existing tests, level choices) as soon as it is given.
- **Planned Doubles:** list a double only when it stands in for the behavior of a boundary (fake, stub, spy, or mock), with the source or sample it mirrors. A dummy only fills a parameter that the behavior never uses, so it has no behavior to review and is not listed.
- **Evidence:** add one row when an item reaches `done`. For the two exceptions in Core Principle 7, write `exception: pins existing behavior` in the RED cell. Rows of one data-driven test may share one evidence row listing their IDs. The exit summary is built from it.

## Review view (for the user)

Present the list in the conversation. The reader must be able to check three things quickly: the expected values and their sources, the open decisions, and what is not tested. Rules:

- Put decisions first, details after.
- Use plain words. Write "Tested through (seam)" and describe it as the function or interface the tests call.
- Show every item with a concrete example, the expected value, its source, and its level. Never hide an item.
- One table per Group, in this order: `happy path`, `alternative path`, `boundary`, `invalid input`, `error handling`, `regression`. Skip empty groups.
- Show counts so the reader can see the size of the review.

```markdown
## Test list for review: <change>

> Please check the expected values and their sources, the decisions needed, and what is not tested.

### Summary

- <N> items in <G> groups · levels: <levels> · <K> need your decision · <M> behaviors not tested

### Decisions needed from you

| #   | ID   | Question            | Proposed default |
| --- | ---- | ------------------- | ---------------- |
| 1   | <ID> | <specific question> | <default>        |

### Scope and setup

- **Change:** <one line>
- **Sources:** <requirement, acceptance criteria, bug report, or existing code>
- **Applicable levels:** <levels> (source: <rule or instruction>)
- **Tested through (seam):** <function or interface the tests call>
- **Commands:** focused `<command>` · full `<command>`
- **Baseline:** <result; pre-existing failures, or "none">

### Coverage

| Requirement or acceptance criterion | Items             |
| ----------------------------------- | ----------------- |
| <criterion>                         | <IDs>             |
| <criterion>                         | **NO ITEM (gap)** |

### Items by group

#### <Group> (<count>)

| ID   | Behavior (concrete example) | Expected   | Source of expected | Level   |
| ---- | --------------------------- | ---------- | ------------------ | ------- |
| <ID> | <behavior>                  | <expected> | <source>           | <level> |

Full list with status: `<path to the test list file>`

### Not tested

| Behavior   | Reason   |
| ---------- | -------- |
| <behavior> | <reason> |

### Planned test doubles

| Boundary   | Kind   |
| ---------- | ------ |
| <boundary> | <kind> |

### Execution order

<ID> → <ID> → <ID>

### How to respond

- Reply **confirmed** to approve everything, or name the groups or IDs you want changed.
- Answer the questions above, or accept the proposed defaults.
```

Write `None.` under a heading that has no content.

## Revision view

After feedback, reprint only what changed, mark each change, and ask again.

```markdown
### Changes since the last version

| Change  | ID   | Behavior       | Expected       | Source of expected | Level   |
| ------- | ---- | -------------- | -------------- | ------------------ | ------- |
| ADDED   | <ID> | <behavior>     | <expected>     | <source>           | <level> |
| CHANGED | <ID> | <new behavior> | <new expected> | <source>           | <level> |
| REMOVED | <ID> | <behavior>     | —              | reason: <reason>   | —       |

### Updated coverage

| Requirement or acceptance criterion | Items |
| ----------------------------------- | ----- |
| <criterion>                         | <IDs> |

Please confirm, or tell me what else to change.
```

## In-loop update

When an item is added after confirmation, report it in the next message to the user:

```markdown
### Item added during implementation

- **<ID>:** <behavior> → expected <expected> (source: <source>).
- **Found by:** <mutation analysis, new edge case, or other reason>.
```
