# Test List Format

Templates and rules for the test list file, the review view, the revision view, and the in-loop update. Adapt them to caller-owned records while retaining sources, decisions, coverage and actual cycle evidence. Placeholders appear as `<...>`.

## Working Record

The working view of cases and evidence. Reuse the caller's canonical record; a separate file is optional.

- Use an authorized destination or conversation record. Do not change ignore rules or create a duplicate tracker. Preserve durable evidence; clean a temporary copy only after useful content is retained in the owning record.
- The default template keeps the information below together; a supplied format may organize it differently.
- Row order in `Items` is the execution order.

### Template

```markdown
# Test List: <change in one line>

## Context

| Field             | Value                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------ |
| Change            | <one line>                                                                                 |
| Sources           | <requirement, acceptance criteria or bug contract; observed behavior for characterization> |
| Applicable levels | <levels> (source: <project rule files or user instructions>)                               |
| Seam              | <public interface where behavior is observed>                                              |
| Focused run       | `<command>`                                                                                |
| Full run          | <required final commands, including separate CI checks and execution prerequisites>        |
| Baseline          | <result; pre-existing failures, or "none">                                                 |
| Authorization     | <existing approval/source and scope, or specific pending decision>                         |

## Items

| ID   | Group   | Test        | Behavior                       | Expected                                        | Source of Expected                    | Level   | Status   |
| ---- | ------- | ----------- | ------------------------------ | ----------------------------------------------- | ------------------------------------- | ------- | -------- |
| <ID> | <Group> | <test name> | <condition and concrete input> | <independent value, property, error, or effect> | <where the expected value comes from> | <level> | <status> |

## Coverage Map

| Requirement or Acceptance Criterion | Item IDs            |
| ----------------------------------- | ------------------- |
| <criterion>                         | <IDs, or "NO ITEM"> |

## Not Tested

| Behavior   | Reason   |
| ---------- | -------- |
| <behavior> | <reason> |

## Test Doubles

| Boundary   | Double Kind                | Basis                                                      |
| ---------- | -------------------------- | ---------------------------------------------------------- |
| <boundary> | <fake, stub, spy, or mock> | <source, documentation, or real sample the double mirrors> |

## Decisions

| ID             | User Decision          |
| -------------- | ---------------------- |
| <ID or "list"> | <decision in one line> |

## Added in Loop

| ID   | Behavior   | Source   |
| ---- | ---------- | -------- |
| <ID> | <behavior> | <source> |

## Evidence

| ID   | RED                 | GREEN              | REFACTOR                         |
| ---- | ------------------- | ------------------ | -------------------------------- |
| <ID> | <command → message> | <command → result> | <what changed, or "none needed"> |
```

Write `None.` under a heading that has no content.

### Field Rules

**Items rules:**

| Field              | Rule                                                                                                                                                                                                                                    |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID                 | Short prefix plus number. Unique, stable, never renumbered or reused.                                                                                                                                                                   |
| Group              | Exactly one value from the Group table below.                                                                                                                                                                                           |
| Test               | Name of the test this item belongs to. Items with the same name are rows of one data-driven test. A single-item test has its own name.                                                                                                  |
| Behavior           | The condition plus a concrete input, in domain language. Describe observable behavior, never implementation.                                                                                                                            |
| Expected           | An independently sourced value, error, effect or property. Do not derive the oracle from the subject's implementation. `needs decision` is allowed only with status `needs-confirmation`, or `dropped` after the user dropped the item. |
| Source of expected | A requirement ID, a document and section, observed existing behavior (characterization only), or a short hand computation (for example, `8.00 + 1.50 × 1`). Never `assumed` or `obvious`.                                               |
| Level              | One of the applicable levels.                                                                                                                                                                                                           |
| Status             | One value from the status table below.                                                                                                                                                                                                  |

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
| `pending`            | Sourced, authorized and not started                                                         |
| `in-progress`        | The current cycle is working on it                                                          |
| `done`               | RED and GREEN observed (or the exception in Core Principle 7 applied), refactoring finished |
| `dropped`            | Removed; the reason is in `Decisions`                                                       |
| `needs-confirmation` | Expected behavior cannot be derived; blocks dependent work until resolved                   |

**Other section rules:**

- **Context > Authorization:** identify existing scope/approval or the exact pending decision; do not invent a second whole-list approval.
- **Coverage Map:** when the request has no acceptance criteria, use the expected behavior stated in the request or bug report. A row with no items stays visible as `NO ITEM`.
- **Decisions:** record every user answer that changes the list (resolved questions, drops, approved edits to existing tests, level choices) as soon as it is given.
- **Test Doubles:** list a double used at a deliberate isolation boundary (fake, stub, spy, or mock), with the source or sample it mirrors. A dummy only fills a parameter that the behavior never uses, so it has no behavior to review and is not listed.
- **Evidence:** record each RED, GREEN and REFACTOR observation as it occurs, with command, result and identifiable candidate state; retain partial rows for interrupted cycles. Set `done` only after required cycle checks and refactor review. For existing-behavior coverage under Core Principle 7, write `existing behavior: no new RED; provenance and sensitivity recorded` in the RED cell. Rows of one data-driven test may share one evidence row listing their IDs. The exit summary is built from it.

## Review View (for the User)

Present the list in the conversation. The reader must be able to check three things quickly: the expected values and their sources, the open decisions, and what is not tested. Rules:

- Put decisions first, details after.
- Use plain words. Write "Tested through (seam)" and describe it as the function or interface the tests call.
- Show every item with a concrete example, the expected value, its source, and its level. Never hide an item.
- One table per Group, in this order: `happy path`, `alternative path`, `boundary`, `invalid input`, `error handling`, `regression`. Skip empty groups.
- Show counts so the reader can see the size of the review.

```markdown
## Test List for Review: <change>

> Please check the expected values and their sources, the decisions needed, and what is not tested.

### Summary

- <N> items in <G> groups · levels: <levels> · <K> need your decision · <M> behaviors not tested

### Decisions Needed from You

| #   | ID   | Question            | Proposed Default |
| --- | ---- | ------------------- | ---------------- |
| 1   | <ID> | <specific question> | <default>        |

### Scope and Setup

- **Change:** <one line>
- **Sources:** <requirement, acceptance criteria or bug contract; observed behavior for characterization>
- **Applicable levels:** <levels> (source: <rule or instruction>)
- **Tested through (seam):** <function or interface the tests call>
- **Commands:** focused `<command>` · full `<command>`
- **Baseline:** <result; pre-existing failures, or "none">

### Coverage

| Requirement or Acceptance Criterion | Items             |
| ----------------------------------- | ----------------- |
| <criterion>                         | <IDs>             |
| <criterion>                         | **NO ITEM (gap)** |

### Items by Group

#### <Group> (<count>)

| ID   | Behavior   | Expected   | Source of Expected | Level   |
| ---- | ---------- | ---------- | ------------------ | ------- |
| <ID> | <behavior> | <expected> | <source>           | <level> |

Full list with status: <caller-owned record reference, conversation location or authorized file path>

### Not Tested

| Behavior   | Reason   |
| ---------- | -------- |
| <behavior> | <reason> |

### Test Doubles

| Boundary   | Kind   |
| ---------- | ------ |
| <boundary> | <kind> |

### Execution Order

<ID> → <ID> → <ID>

### How to Respond

- Identify any unresolved behavior or scope decisions. Existing approval already covering these cases remains valid.
- Answer the questions above, or accept the proposed defaults.
```

Write `None.` under a heading that has no content.

## Revision View

After feedback, reprint only what changed, mark each change, and request confirmation only for a material unresolved decision.

```markdown
### Changes Since the Last Version

| Change  | ID   | Behavior       | Expected       | Source of Expected | Level   |
| ------- | ---- | -------------- | -------------- | ------------------ | ------- |
| ADDED   | <ID> | <behavior>     | <expected>     | <source>           | <level> |
| CHANGED | <ID> | <new behavior> | <new expected> | <source>           | <level> |
| REMOVED | <ID> | <behavior>     | —              | reason: <reason>   | —       |

### Updated Coverage

| Requirement or Acceptance Criterion | Items |
| ----------------------------------- | ----- |
| <criterion>                         | <IDs> |

Resolve the specific material decision above; routine derived cases within approved criteria need no repeated gate.
```

## In-Loop Update

When a derived case is added within authorized scope, report its source in the next progress update:

```markdown
### Item Added During Implementation

- **<ID>:** <behavior> → expected <expected> (source: <source>).
- **Found by:** <test sensitivity review, new edge case, or other reason>.
```
