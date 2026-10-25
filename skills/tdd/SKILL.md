---
name: tdd
description: Drives code changes with tests written first, using the Red-Green-Refactor cycle. Builds a test list from the requirements, has the user confirm it, then repeats one failing test, minimal code, and a refactoring review until the list is done, and checks that the tests would catch realistic mistakes. Also guides which kinds of tests to write, how to derive test cases, and how to write reliable tests. Use when implementing a feature, fixing a bug, changing behavior, or planning and writing tests.
metadata:
  author: phatnguyen975
  version: 1.0
---

# Test-Driven Development

## Overview

Change behavior test-first: agree on a test list with the user, then repeat Red → Green → Refactor, one test at a time, until the list is done.

- A test is an executable specification. A test that was observed failing before the code existed, then passing, is the evidence that a change works.
- After the change, old behavior is still correct, new behavior is correct, and the code is ready for the next change.
- The user confirms expected behavior before any test or production code is written. Never invent expected behavior.

## When to Use

- Implementing a feature.
- Fixing a bug.
- Changing existing behavior.
- Adding validation, error handling, or edge-case handling.
- Any change that can break existing behavior.
- Choosing a test level, deriving test cases, or writing, reviewing, or planning tests.

## When NOT to Use

Skip TDD only when there is no behavior to verify:

- Documentation, comment, or formatting changes.
- Declarative configuration without logic.
- Generated code: test the generator's input or contract, not its output.
- Throwaway spikes: discard the spike, then restart from a test.
- Pure refactoring: add no new tests. Tests covering the area must already exist and be green. If they do not, add characterization tests first.

When skipping, state the reason to the user. If unsure whether a case qualifies, ask. Every other case uses TDD.

## Input

| Input                    | Type                                                           | Required | Notes                                                                                               |
| ------------------------ | -------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------- |
| Change description       | Feature, bug report, or behavior change                        | Required | Must be small enough to produce a test list a user can review. Otherwise ask the user to narrow it. |
| Expected-behavior source | Requirement, acceptance criteria, bug report, or existing code | Required | If no source exists, ask.                                                                           |
| Project test rules       | Contribution docs, CI config, existing test layout             | Optional | Source of commands, naming, and applicable levels.                                                  |
| Level instructions       | Free text from the user                                        | Optional | Overrides or extends project rules.                                                                 |

## Output

| Output                                 | Where it appears                                                                                         |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Production code and tests, all passing | In the project                                                                                           |
| Test list file                         | A temporary working file outside version-controlled source (templates: `references/test-list-format.md`) |
| Review view and revision view          | Printed in the conversation, for the user to confirm (templates: `references/test-list-format.md`)       |
| Exit summary                           | Printed in the conversation as the final message of the work                                             |

Exit summary template:

```markdown
## TDD exit summary: <change>

> **Result:** <done>/<total> items done
> **Full run:** <pass or fail> (`<command>`)

| Field                                              | Value                                                   |
| -------------------------------------------------- | ------------------------------------------------------- |
| Applicable levels                                  | <levels> (source: <project rules or user instructions>) |
| Dropped items                                      | <ID — reason or none>                                   |
| Items added in loop                                | <ID — source or none>                                   |
| Pre-existing failures                              | <list or none>                                          |
| Possible impact on tests outside applicable levels | <list or none>                                          |
| Not tested                                         | <behavior — reason or none>                             |
| Refactoring suggestions (outside touched code)     | <list or none>                                          |

### Evidence

| ID   | RED (command → failure message) | GREEN (command → result) | REFACTOR                      |
| ---- | ------------------------------- | ------------------------ | ----------------------------- |
| <ID> | <command → message>             | <command → result>       | <what changed or none needed> |

### Mutation analysis

| Behavior   | Mutation   | Catching test | Differing result                                 |
| ---------- | ---------- | ------------- | ------------------------------------------------ |
| <behavior> | <mutation> | <ID>          | <what the mutated code would return vs expected> |
```

## Core Principles

1. **Independent expected values.** Take expected values from requirements, acceptance criteria, hand-computed examples, or verified literals. Never compute them with the code under test. Never paste actual output into an expected value.
2. **No invented expected behavior.** If expected behavior cannot be derived from available sources, mark the item `needs-confirmation` and ask the user.
3. **Verify before use.** Confirm every API, function, flag, config key, and library behavior against the codebase or the documentation for the installed version.
4. **Use the project's real commands.** Discover them from build files, scripts, README, or CI. Prefer project wrappers over global tools. Never assume a default command.
5. **Evidence over claims.** Report pass or fail only after running. Judge by the command's exit status and the reported counts; do not pipe test output through a filter that hides the exit status. Quote the command and result. Confirm the target test actually executed (it appears in the output, is not skipped, and the filter is not empty).
6. **Never weaken tests.** Do not delete, skip, disable, or loosen a test or assertion to reach green. Change a test that existed before this change only when the requirement changed, and state why.
7. **Red first.** Observe a test fail before writing the implementation. Do not produce test and implementation in the same step. Do not edit or break production code to force a failure. Two exceptions: characterization tests and data-driven rows added after the behavior exists. They pass on first run; verify them with the mutation analysis instead.
8. **Faithful test doubles.** Take the structure and behavior of a double from source, documentation, or a captured real sample.
9. **Minimal code.** Write only what the current failing test requires.
10. **Code before test is discarded.** Remove the production change written before its test, then restart from the test. Leave the user's changes untouched.
11. **Gate before RED.** Start RED only after the user explicitly confirms the test list.
12. **The test list file is the source of truth.** Re-read it at the start of every cycle and after any context loss. Update item status after every cycle, and record user decisions and evidence in it. Never rebuild the list from memory.
13. **Applicable levels only.** Write tests only at levels in the applicable set (Phase 0).

## Workflow

### Phase 0 — Discover & Baseline

1. Identify language, build system, test framework, test location, and naming conventions. Identify the command for a **focused run** (one test) and a **full run** (the project's test suite for the applicable levels).
2. Determine the **applicable levels** — the test levels the project runs during implementation.
   - Sources, in order: project rules (contribution docs, CI, conventions, existing test layout), then the user's instructions.
   - A level the project runs separately after implementation or only in CI, and the user did not request, is not applicable.
   - No rule found: ask the user. Propose unit level as the minimum.
   - Handling of applicable and non-applicable levels: `references/test-levels.md`.
3. Run the full run. Record the baseline and any pre-existing failures. Report pre-existing failures; do not hide them or fix them silently.
4. Read the code, neighboring tests, and domain vocabulary. Name tests in the project's language.
5. Identify the **seam** — the public interface where the behavior is observable. Place tests at the seam only. If the seam does not exist yet, the test is the interface's first client and shapes it.

### Phase 1 — Test List & Confirmation

Read `references/test-design-techniques.md` and `references/test-list-format.md` first.

1. List the behaviors that must be correct: happy path, alternative paths, boundaries, invalid input, error handling (dependency or environment failures), and regression (existing behavior that must not break). Derive candidates with the techniques in `test-design-techniques.md`, then make a final error-guessing pass.
2. Keep an item only if a realistic wrong production change would make its test fail (name the break). Exclude trivial code and framework or library behavior.
3. Write each item as an observable behavior in domain language with a concrete input example, a literal expected value, and the source of that expected value.
4. Assign exactly one level per item: the lowest applicable level at which the behavior is observable at the seam. Behavior not observable at any applicable level goes into "Not Tested" with a reason, for the user to decide.
5. Mark items whose expected value cannot be derived as `needs-confirmation`, each with a specific question.
6. Order items: characterization items first (they must exist before the behavior changes), then from the simplest case through the seam to increasing complexity. Place an item that composes lower-level items after them, so it is still red when its turn comes.
7. Save the list to the test list file. Present the review view. Stop and wait.
8. Revise on feedback: update the file, present the revision view (changed items plus the new coverage map), and ask again.
9. Proceed only when both hold: the user explicitly approved the whole list (or every Group in turn), and no `needs-confirmation` item remains (each is resolved to `pending` or `dropped`). A question, comment without approval, approval with edits, or silence is not confirmation. For approval with edits, apply the edits and ask again.

**Change control after confirmation**

- Updating item status: free.
- Adding an item: allowed when its expected value derives from confirmed sources and it belongs to the same behavior area (e.g. one more boundary found). Record it under "Added in Loop" with its source and report it in the next message and in the exit summary. If it needs new behavior, cannot be derived, or widens scope: stop and ask.
- Editing, dropping, or reordering a confirmed item: needs user confirmation.
- After context loss: re-read the file and continue from the first item that is not `done`.

### Phase 2 — RED

Read `references/writing-good-tests.md` before the first test.

1. Pick the next item and mark it `in-progress`. Write one test for one behavior at its assigned level. Items that share a `Test` name become the rows of one data-driven test; update each item's status separately.
2. State which production change would make this test fail. If you cannot name it, redesign the test around observable behavior.
3. Run the focused run. A valid Red means:
   - The test executed.
   - It failed by assertion failure, not by compile, import, typo, or setup error.
   - The failure message matches the expectation: the behavior does not exist yet.
4. A test that passes immediately tests existing behavior or is wrong. Fix the test or propose dropping the item (needs user confirmation). Keep it only under the exceptions in Core Principle 7.
5. A test that errors: fix the error and rerun until it fails correctly. Exception: for a unit that does not exist yet, a missing-symbol error on the first run only signals the empty stub to create; rerun to reach an assertion failure.

### Phase 3 — GREEN

1. Write the minimal code that passes. Choose by confidence: Fake It (return a constant, then generalize), Triangulation (add a second example that forces generalization), or Obvious Implementation (when the solution is evident). If the dependency cannot be replaced in the test, make it injectable in the smallest way the test needs.
2. If the test fails, fix the code, not the test. If the test itself is wrong, return to RED.
3. Run the focused run, then the tests located with the changed code (same module, package, or directory). Confirm other tests still pass and the output has no new errors or warnings.
4. Do not rerun a command when the code has not changed since its last run, except to rule out stale artifacts (Core Principle 5).
5. Do not refactor or add behavior beyond the current test in this phase.

### Phase 4 — REFACTOR

**Purpose:** leave the code touched in this cycle easier to read and change, without changing behavior. The review in step 1 is mandatory every cycle. Edits are made only when the review finds something worth changing.

**Precondition:** the focused run and the module tests are green. Never refactor on red; return to GREEN.

1. **Review** the production code and the tests you added or changed in this cycle:
   | Check               | Look for                                                                                                  | Typical refactoring                           |
   | ------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
   | Naming              | Names that hide intent, are vague, or differ from the domain vocabulary                                   | Rename                                        |
   | Duplication         | Repeated logic or structure; constants copied between a test and production code (a leftover of Fake It)  | Extract function or constant; remove the copy |
   | Size and complexity | A long function, deep nesting, one function doing several things, a comment explaining a block            | Extract function; simplify conditionals       |
   | Parameters and data | Long parameter lists; values that always travel together; a primitive value standing for a domain concept | Introduce a parameter object or value type    |
   | Placement           | Logic that uses another module's data more than its own                                                   | Move function                                 |
   | Leftovers           | Dead or unused code, temporary stubs, unused parameters, code no test requires, debug output              | Remove                                        |
   | Conventions         | Deviation from the project's style and patterns                                                           | Align                                         |
2. **Decide** what is worth changing: an improvement that makes the next change easier, inside the code touched in this cycle. Skip purely cosmetic edits. Do not abstract on a guess: extract shared code when real occurrences show the common shape (one occurrence never justifies it).
3. **Apply** one small behavior-preserving step at a time (rename, extract, inline, move, remove). After each step run the focused run and the module tests. If anything fails, undo that step and take a smaller one or leave it. Never repair a refactoring failure by editing a test.
4. **Review test code separately**, never in the same step as production edits: names state behavior, expected values are visible, setup noise is removed, and the properties in `references/writing-good-tests.md` hold. If a refactoring step would force a test edit although the public interface did not change, the test is coupled to implementation. For a test written in this change: undo the step, make the test independent of the implementation while the tests stay green, then continue. For a test that existed before: skip the step and record it under refactoring suggestions (editing it needs the user; see Stop and Ask).
5. **Do not** change behavior, add behavior or tests, optimize without a stated requirement (performance work is a new item), or refactor beyond the touched code. Changing a public interface that code outside the touched area uses is also out of this phase. Record larger improvements as "Refactoring suggestions" for the exit summary.
6. **Finish the cycle:** record `REFACTOR: <what changed or none needed>` in the Evidence section, record the RED and GREEN evidence, and set the item to `done`.

### Phase 5 — Repeat or Exit

Return to Phase 2 until every item is `done` or `dropped` (with a reason). Then run the mutation analysis, complete the Verification checklist, print the exit summary in the conversation, and delete the test list file. If the user asks for further changes afterward, build a new test list (Phase 1).

### Variant: Bug fix

1. Do not change code first. Investigating by reading code and running observation commands is allowed. Establish the expected behavior and the observed wrong behavior.
2. Build the test list and pass the confirmation gate like any change. If no existing test covers a behavior the fix might affect, add characterization tests for it in the same list.
3. Reproduce the bug with a test at the lowest applicable level that can expose it, even if a test at another level found it. If no applicable level can expose it, record it under "Not Tested" for the user to decide.
4. Run it. It must fail with the reported symptom, not a different error.
5. Fix the root cause with minimal code.
6. Confirm the test passes, then run the full run to check for regressions.
7. Name the test after the bug scenario so it stays as a regression test.

### Variant: Untested behavior

- Before changing behavior that no existing test covers, add **characterization tests** — tests that record the current behavior the change might affect (only those behaviors, at an applicable level). They go through the test list and the gate.
- They must pass on the original code. They are an exception to Red first and are verified by the mutation analysis.
- If the current behavior is a bug, treat it as the Bug fix variant instead of recording it.

### When Stuck

| Symptom                                          | Action                                                                                                             |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| Unsure how to test                               | Write the assertion first from the desired API; make the test the interface's first client                         |
| Test or setup is very large                      | The design is too complex; simplify the interface and shrink the setup                                             |
| Too many doubles                                 | Coupling is too high; inject dependencies or use real components at a suitable applicable level                    |
| Green step is too large                          | Return and pick a smaller test                                                                                     |
| Two consecutive fixes did not change the failure | Stop; recheck assumptions, the test, and the requirement before writing more code                                  |
| Result differs between runs with no code change  | Flaky: find the uncontrolled input (time, order, shared state, concurrency) and remove it; never retry until green |
| New test invalidates earlier work                | Propose a different item order (reordering needs user confirmation)                                                |

### Stop and Ask

Stop and ask the user when:

- The project defines no applicable levels (propose unit level as the default), or no test command can be discovered (propose the language's standard test runner).
- Expected behavior cannot be derived from available sources.
- The input is too large or too vague to produce a reviewable test list.
- A new public interface or seam has several reasonable designs that affect outside callers.
- A new item needs the approval described in Phase 1, or a confirmed item must be edited, dropped, or reordered.
- An existing test must be edited or deleted.
- The environment cannot run the required tests (missing dependency, permission, connectivity).

Ask one specific question with a proposed default. Wait for the answer before continuing.

### Mutation Analysis

**Purpose:** confirm that the tests would notice a realistic mistake in the new code. It is analysis by reading and reasoning. Do not edit, run, or temporarily change production code to try a mutation. If the project already configures a mutation-testing tool, running it is allowed and may replace the hand evaluation. Do not install one.

**Terms:**

- **Mutation:** a small defect you imagine in the production code, for example `<=` replaced by `<`.
- **Killed:** at least one test would fail on the mutated code.
- **Survived:** no test would fail.
- **Equivalent:** the mutated code behaves identically for every input, so it is not a defect; discard it.

Procedure, for the production code added or changed in this change:

1. Identify each decision, computed value or constant, side effect or state change, validation, and return value.
2. For each, choose realistic mutations, those a plausible mistake would produce, as many as the code warrants.
   | Kind                             | Examples                                                                |
   | -------------------------------- | ----------------------------------------------------------------------- |
   | Relational operator or boundary  | `<` ↔ `<=`, `>` ↔ `>=`, `==` ↔ `!=`                                     |
   | Arithmetic, constant, off-by-one | `+` ↔ `-`, a changed literal, `n` ↔ `n±1`                               |
   | Logic                            | `and` ↔ `or`, a removed negation, a removed condition                   |
   | Removed statement                | A dropped side effect, state update, or call                            |
   | Return value                     | An empty, default, or constant return; swapped arguments                |
   | Validation                       | A removed check for zero, empty, null, unauthorized, or malformed input |
3. For each mutation, take the test input most likely to expose it. Evaluate the mutated code on that input by hand, step by step, and compare the result with the test's expected value. Write down the differing result.
4. Killed: record behavior, mutation, catching test, and the differing result. Survived and not equivalent: the behavior is unprotected or a test is tautological or weak. Add or strengthen an item (change control, Phase 1), then repeat the evaluation for it.
5. A characterization test or a data-driven row added after the behavior exists is kept only if some mutation of the pinned behavior would make it fail.

## Common Rationalizations to Reject

| Excuse                            | Reality                                                                                 |
| --------------------------------- | --------------------------------------------------------------------------------------- |
| "Too simple to test"              | Simple code breaks too; the test is short and doubles as specification                  |
| "I'll write tests after"          | A test written after the code is shaped by the code and passes at once, proving nothing |
| "I tested it manually"            | Manual checks cannot be repeated or recorded                                            |
| "Just edit the test so it passes" | Wrong behavior needs a code fix; change a test only when the requirement changed        |
| "Keep the code as a reference"    | It will be adapted; that is test-after                                                  |
| "Explore first"                   | Fine, then discard the exploration and start from a test                                |
| "Hard to test, skip it"           | Hard to test signals a hard-to-use design                                               |
| "Just this once"                  | Only the cases in When NOT to Use skip TDD                                              |
| "Small list, no need to confirm"  | The gate applies to every list; a small list reviews fast                               |
| "Rerun to be safe"                | Rerunning unchanged code adds no confidence                                             |

## Red Flags

Stop and correct course on any of these:

- Test or production code written before the user confirmed the test list.
- Test list rebuilt from memory instead of read from the file.
- A new test passes on its first run (outside the two exceptions).
- Cannot explain why a test fails.
- "All pass" reported without knowing which tests ran.
- A test skipped, disabled, deleted, or an assertion weakened.
- Production code edited temporarily to force a failure or to try a mutation.
- An expected value taken from the code's own output, or with no source.
- Assertions on a mock instead of behavior.
- A default test command used without checking the project.
- The same command rerun on unchanged code.
- Refactoring started while a test is red, or a test edited to make a refactoring pass.
- A test written at a level outside the applicable set.
- TDD skipped without a stated reason or outside When NOT to Use.

## Verification

Before printing the exit summary, confirm every item:

- [ ] Every item in the test list file is `done`, or `dropped` with a reason the user confirmed.
- [ ] Every acceptance criterion maps to at least one test, or sits in "Not Tested" confirmed by the user.
- [ ] Every new test was observed failing for the right reason before passing (except the two exceptions in Core Principle 7).
- [ ] The full run passes with the project's command at the applicable levels. No test was skipped, disabled, or deleted. The output is clean.
- [ ] Every cycle has a recorded REFACTOR review (`changed` or `none needed`).
- [ ] The mutation analysis shows no surviving non-equivalent mutation for any new behavior.
- [ ] The production diff contains no code that no test requires.
- [ ] New tests meet the properties in `writing-good-tests.md`: behavior-focused, specific assertions, no logic, doubles only at system boundaries.
- [ ] The test list file records the user's decisions and the evidence for every `done` item.
