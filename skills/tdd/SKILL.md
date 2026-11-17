---
name: tdd
description: Drives code changes with tests written first, using the Red-Green-Refactor cycle. Derives test cases from sourced behavior and existing authorization, then repeats one failing test, minimal code, and a refactoring review until the list is done, and checks that the tests would catch realistic mistakes. Also guides which kinds of tests to write, how to derive test cases, and how to write reliable tests. Use when implementing a feature, fixing a bug, changing behavior, or deriving behavior-focused test cases.
metadata:
  author: phatnguyen975
  version: "1.0"
---

# Test-Driven Development

## Overview

Change behavior test-first: establish sourced expected behavior and a test list, then repeat Red → Green → Refactor, one test at a time, until the list is done.

- A test is an executable specification. Observed RED followed by GREEN provides evidence for the exercised behavior, not proof of universal correctness.
- Check preserved behavior as well as new behavior; disclose gaps, failures and unavailable verification.
- Use approved requirements or equivalent prior authorization for expected behavior; ask only for unresolved material choices. Never invent expected behavior.

## When to Use

- Implementing a feature.
- Fixing a bug.
- Changing existing behavior.
- Adding validation, error handling, or edge-case handling.
- Any change that can break existing behavior.
- Choosing a test level, deriving test cases, or writing and assessing behavior-focused tests.

## When NOT to Use

This capability owns test-first implementation, not the choice of every project's verification method. When the caller selected test-after/manual implementation, supply relevant case-design advice if requested and leave that execution method to the caller; do not invent TDD evidence.

Documentation/formatting with no executable behavior does not need a Red-Green cycle. Configuration and generated artifacts can have behavior: test the owning input, generator, rendered contract or execution boundary as appropriate. For pure refactoring, begin with passing coverage; add authorized characterization checks when coverage is missing. A throwaway experiment is not evidence of a test-first implementation.

## Input

| Input                    | Type                                                                                   | Required | Notes                                                                                  |
| ------------------------ | -------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------- |
| Change description       | Feature, bug report, or behavior change                                                | Required | Bound the work and choose a small next behavior; ask only if scope cannot be resolved. |
| Expected-behavior source | Requirement, acceptance criteria, bug contract; current code only for characterization | Required | Resolve material unknowns before dependent tests or implementation.                    |
| Project test rules       | Contribution docs, CI config, existing test layout                                     | Optional | Source of commands, naming, and applicable levels.                                     |
| Level instructions       | Free text from the user                                                                | Optional | Use within applicable authority; resolve conflicts with project constraints.           |

## Output

| Output                        | Where It Appears                                                                               |
| ----------------------------- | ---------------------------------------------------------------------------------------------- |
| Production code and tests     | When implementation is requested; report actual passing checks and blockers                    |
| Test record                   | Caller-owned record or a working list using [Test List Format](references/test-list-format.md) |
| Review view and revision view | Present only when decisions or material changes need review; reuse existing approval           |
| Exit summary                  | Printed in the conversation as the final message of the work                                   |

Exit summary template:

```markdown
## TDD Summary: <change>

> **Outcome:** <completed / partial / blocked>
> **Result:** <done>/<total> items done
> **Full run:** <pass / fail / not run, with reason> (`<command>`)

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

| ID   | RED                 | GREEN              | REFACTOR                      |
| ---- | ------------------- | ------------------ | ----------------------------- |
| <ID> | <command → message> | <command → result> | <what changed or none needed> |

### Test Sensitivity Review

Label the assessment as reasoning or executed mutation-tool evidence; record gaps and limitations.

| Behavior   | Mutation / Method | Catching Test | Predicted or Observed Difference                 |
| ---------- | ----------------- | ------------- | ------------------------------------------------ |
| <behavior> | <mutation>        | <ID>          | <what the mutated code would return vs expected> |
```

## Core Principles

1. **Independent oracles.** Derive expectations independently of the subject. Label observed characterization output as existing behavior, not a requirement.
2. **Sourced behavior.** Mark unresolved expectations `needs-confirmation`; ask before dependent work.
3. **Verified interfaces.** Check relevant APIs, options and library behavior against project code and installed-version documentation.
4. **Project commands.** Discover actual test commands and prefer project wrappers; do not assume defaults.
5. **Observed evidence.** Confirm the intended tests executed. Record commands, exit status and results without hiding failures or inventing passes.
6. **Preserved coverage.** Never weaken tests to reach green. Correct wrong expectations only from authoritative evidence and within scope.
7. **RED before implementation.** Observe the intended failure before implementing. Label characterization or already-supported examples with their actual first-run result and sensitivity evidence; never manufacture RED by breaking working code.
8. **Faithful doubles.** Model contract-relevant behavior from verified source, documentation or real samples.
9. **Minimal implementation.** Add only what the current failing test requires.
10. **Preserved ownership.** Undo premature implementation only when it is safely agent-owned. Preserve user/published work and disclose test-after history instead of inventing RED.
11. **Scoped authority.** Reuse existing approval. Resolve new behavior, scope or permission decisions before dependent edits.
12. **One evidence record.** Reuse the caller's record or an authorized test list. Read it each cycle/on resume; retain decisions and evidence before temporary cleanup.
13. **Relevant coverage.** Follow Phase 0's applicable checks; do not discard required coverage because it runs only in CI.

## Workflow

### Phase 0 — Discover and Baseline

1. Identify language, build system, test framework, test location, and naming conventions. Identify the command for a **focused run** (one test) and a **full run** (the project's test suite for the applicable levels).
2. Determine applicable scope/dependencies and checks from the caller's selected strategy, project rules, existing layout and the behavior's risks. Separate fast cycle checks from required final or CI checks. CI-only execution does not make relevant coverage inapplicable. Read [Test Levels](references/test-levels.md); resolve missing prerequisites rather than silently substituting a lower level.
3. Inspect the initial worktree and preserve existing changes. Run the applicable baseline commands within existing authority; if unavailable, record a blocker for dependent cycles. Record the baseline and any pre-existing failures. Report pre-existing failures; do not hide them or fix them silently.
4. Read the code, neighboring tests, and domain vocabulary. Name tests in the project's language.
5. Identify the **seam** — the public interface where the behavior is observable. Use the appropriate stable boundary for the behavior; an adapter integration test can inspect persistence when that is its contract. If the seam does not exist yet, the test is the interface's first client and shapes it.

### Phase 1 — Test List and Decisions

Read [Test Design Techniques](references/test-design-techniques.md) when deriving or checking case coverage, and [Test List Format](references/test-list-format.md) for the working record. Reuse supplied cases after checking their sources and coverage.

1. List the behaviors that must be correct: happy path, alternative paths, boundaries, invalid input, error handling (dependency or environment failures), and regression (existing behavior that must not break). Derive candidates with the techniques in [Test Design Techniques](references/test-design-techniques.md), then check relevant likely failure cases.
2. Keep an item only if a realistic wrong production change would make its test fail (name the break). Exclude trivial code and framework or library behavior.
3. Write each item as an observable behavior in domain language with a concrete input example, an independently sourced expected value, effect or property and its source.
4. Record a primary test scope/category per item: the lowest applicable level at which the behavior is observable at the seam. Behavior not observable at any applicable level goes into "Not Tested" with a reason, for the user to decide.
5. Mark items whose expected value cannot be derived as `needs-confirmation`, each with a specific question.
6. Order items: characterization items first (they must exist before the behavior changes), then from the simplest case through the seam to increasing complexity. Use later cases to drive missing behavior; record already-supported examples honestly under Principle 7.
7. Record cases and coverage using [Test List Format](references/test-list-format.md), adapting to the caller's existing record. Reuse approval covering the sourced behavior and checks; do not require a second whole-list gate.
8. Present specific unresolved decisions and material scope changes. Wait before dependent work; independent authorized work may continue. Do not invent stakeholder answers.

**Change control:** add/refine/reorder implementation cases within approved criteria as evidence emerges, preserving IDs and coverage. New delivery obligations or changed expected behavior need their own authorization, not silent addition to the list. Dropping a required check or accepting a coverage gap needs the applicable human decision. On resume, read the actual record and candidate state rather than recreating them from memory.

### Phase 2 — RED

Read [Writing Good Tests](references/writing-good-tests.md) before authoring tests; use its guidance selectively for the current seam and dependencies.

1. Pick the next item and mark it `in-progress`. Write one test for one behavior at its assigned level. Items that share a `Test` name become the rows of one data-driven test; update each item's status separately.
2. State which production change would make this test fail. If you cannot name it, redesign the test around observable behavior.
3. Run the focused run. A valid Red means:
   - The test executed.
   - It failed by assertion failure, not by compile, import, typo, or setup error.
   - The failure message matches the expectation: the behavior does not exist yet.
4. If a test passes immediately, inspect whether it genuinely exercises already-supported behavior, is redundant or is ineffective. Keep useful coverage under Core Principle 7 with truthful evidence; strengthen ineffective assertions without inventing a defect or unnecessary implementation.
5. A test that errors: fix the error and rerun until it fails correctly. Exception: for a unit that does not exist yet, a missing-symbol error on the first run only signals the empty stub to create; rerun to reach an assertion failure.

### Phase 3 — GREEN

1. Write the minimal code that passes. Choose by confidence: Fake It (return a constant, then generalize), Triangulation (add a second example that forces generalization), or Obvious Implementation (when the solution is evident). If the dependency cannot be replaced in the test, make it injectable in the smallest way the test needs.
2. If the test fails, fix the code, not the test. If the test itself is wrong, return to RED.
3. Run the focused run, then the tests located with the changed code (same module, package, or directory). Confirm other tests still pass and the output has no new errors or warnings.
4. Reuse current evidence when nothing relevant changed. Rerun when refactoring, fixture/environment changes, freshness requirements or investigation of nondeterminism warrants it; do not retry a flaky failure until green.
5. Do not refactor or add behavior beyond the current test in this phase.

### Phase 4 — REFACTOR

**Purpose:** leave the code touched in this cycle easier to read and change, without changing behavior. The review in step 1 is mandatory every cycle. Edits are made only when the review finds something worth changing.

**Precondition:** the focused run and the module tests are green. Never refactor on red; return to GREEN.

1. **Review** the production code and the tests you added or changed in this cycle:
   | Check               | Look For                                                                                                  | Typical Refactoring                                                                  |
   | ------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
   | Naming              | Names that hide intent, are vague, or differ from the domain vocabulary                                   | Rename                                                                               |
   | Duplication         | Duplicated production logic or noisy test setup; preserve independent oracles                             | Extract meaningful shared setup/production logic; retain independent expected values |
   | Size and complexity | A long function, deep nesting, one function doing several things, a comment explaining a block            | Extract function; simplify conditionals                                              |
   | Parameters and data | Long parameter lists; values that always travel together; a primitive value standing for a domain concept | Introduce a parameter object or value type                                           |
   | Placement           | Logic that uses another module's data more than its own                                                   | Move function                                                                        |
   | Leftovers           | Dead or unused code, temporary stubs, unused parameters, code no test requires, debug output              | Remove                                                                               |
   | Conventions         | Deviation from the project's style and patterns                                                           | Align                                                                                |
2. **Decide** what is worth changing: an improvement that makes the next change easier, inside the code touched in this cycle. Skip purely cosmetic edits. Do not abstract on a guess: extract shared code when real occurrences show the common shape (a named concept or real boundary may justify extraction even before duplication).
3. **Apply** one small behavior-preserving step at a time (rename, extract, inline, move, remove). After each step run the focused run and the module tests. If anything fails, undo that step and take a smaller one or leave it. Do not weaken expectations to make a refactoring pass; undo only this step while preserving prior work.
4. **Review test code separately from production edits.** Follow [Writing Good Tests](references/writing-good-tests.md): clear behavior names, visible oracles and focused setup. If an internal refactor breaks a test while its contract is unchanged, inspect implementation coupling. Undo the refactor, improve the test without weakening coverage and rerun before continuing; defer edits outside authorized ownership.
5. **Do not** change behavior, add behavior or tests, optimize without a stated requirement (performance work is a new item), or refactor beyond the touched code. Changing a public interface that code outside the touched area uses is also out of this phase. Record larger improvements as "Refactoring suggestions" for the exit summary.
6. **Finish the cycle:** retain RED/GREEN evidence, record `REFACTOR: <what changed or none needed>` and set the item to `done`. Save each observation when obtained, not only at cycle completion.

### Phase 5 — Repeat or Exit

Repeat Phase 2 for remaining cases. Before completion, review sensitivity and run the required final checks from Phase 0 against the final candidate, reusing only evidence still valid for that state. Include broader/CI checks or explicitly report why they remain unavailable. Compare failures with baseline; do not claim completion with unmet required checks.

Complete Verification and deliver the summary in the caller's format. Retain decisions and evidence in the owning record before cleaning temporary copies. Report incomplete items and blockers explicitly.

### Variant: Bug Fix

1. Do not change code first. Investigating by reading code and running observation commands is allowed. Establish the expected behavior and the observed wrong behavior.
2. Build the test list and reuse or establish behavior/repair authority like any change. If no existing test covers a behavior the fix might affect, add characterization tests for it in the same list.
3. Reproduce the bug with a test at the lowest applicable level that can expose it, even if a test at another level found it. If no applicable level can expose it, record it under "Not Tested" for the user to decide.
4. Run it. It must fail with the reported symptom, not a different error.
5. Fix the root cause with minimal code.
6. Confirm the test passes, then run the full run to check for regressions.
7. Name the test after the bug scenario so it stays as a regression test.

### Variant: Untested Behavior

- Before changing behavior that no existing test covers, add **characterization tests** — tests that record the current behavior the change might affect (only those behaviors, at an applicable level). Record them in the list within authorized scope. Pin only understood behavior, not an unexamined bug as a new intended requirement.
- They must pass on the original code. They are an exception to Red first and are verified by the test sensitivity review.
- For behavior known to violate its contract, use the Bug Fix variant. Characterization can still protect other existing behavior the fix must preserve.

### When Stuck

| Symptom                                          | Action                                                                                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| Unsure how to test                               | Write the assertion first from the desired API; make the test the interface's first client                                      |
| Test or setup is very large                      | Inspect fixture noise and design complexity; simplify only where it preserves the real behavior                                 |
| Too many doubles                                 | Check whether doubles hide behavior or mirror incidental structure; use a clearer boundary or real components where appropriate |
| Green step is too large                          | Return and pick a smaller test                                                                                                  |
| Two consecutive fixes did not change the failure | Stop; recheck assumptions, the test, and the requirement before writing more code                                               |
| Result differs between runs with no code change  | Flaky: find the uncontrolled input (time, order, shared state, concurrency) and remove it; never retry until green              |
| New test invalidates earlier work                | Refine case order within approved criteria; ask only if scope/expected behavior changes                                         |

### Stop and Ask

Stop and ask the user when:

- Required scope/strategy cannot be established or no usable command/harness exists. Propose a concrete scoped option; do not silently install tools or downgrade coverage.
- Expected behavior cannot be derived from available sources.
- The input is too large or too vague to produce a reviewable test list.
- A new public interface or seam has several reasonable designs that affect outside callers.
- A case changes approved behavior/delivery obligations, or required coverage would be removed.
- A test correction or removal changes required coverage or exceeds ownership/authority.
- The environment cannot run the required tests (missing dependency, permission, connectivity).

Ask a focused question with a reasoned option. Wait before dependent actions; continue independently authorized work when useful.

### Test Sensitivity Review

**Purpose:** confirm that the tests would notice a realistic mistake in the new code. It is analysis by reading and reasoning. Do not manually corrupt the active candidate to manufacture RED. If the project already configures a mutation-testing tool, running it in isolation within execution authority is allowed and may replace the hand evaluation. Do not install one.

**Terms:**

- **Mutation:** a small defect you imagine in the production code, for example `<=` replaced by `<`.
- **Predicted detected:** reasoning indicates at least one named assertion would fail. Reserve "killed" for an executed mutation tool result.
- **Predicted gap:** no existing assertion is expected to detect the selected defect; executed survivors require inspection for equivalence and tool limits.
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
3. For each selected mutation, take the test input most likely to expose it. Evaluate the mutated code on that input by hand, step by step, and compare the result with the test's expected value. Write down the differing result.
4. Record whether reasoning predicts detection, or an executed tool actually killed/survived the mutant. For a predicted non-equivalent gap: the behavior is unprotected or a test is tautological or weak. Add or strengthen an item (change control, Phase 1), then repeat the evaluation for it.
5. A characterization test or a data-driven row added after the behavior exists is kept only if some mutation of the pinned behavior would make it fail.

## Verification

Before printing the exit summary, confirm every item:

- [ ] Every required item in the owning test record is `done`, or `dropped` with a reason authorized within the applicable scope.
- [ ] Every acceptance criterion maps to at least one test, or sits in "Not Tested" confirmed by the user.
- [ ] Every new test was observed failing for the right reason before passing (or explicitly identified as existing-behavior coverage under Core Principle 7).
- [ ] The full run passes with the project's command at the applicable levels. No required coverage was silently skipped, disabled, removed or weakened; record authorized corrections and baseline failures.
- [ ] Every cycle has a recorded REFACTOR review (`changed` or `none needed`).
- [ ] The sensitivity review covers new behavior and resolves identified non-equivalent gaps; distinguish reasoning from executed tool results.
- [ ] The production diff contains no code that no test requires.
- [ ] New tests meet the properties in [Writing Good Tests](references/writing-good-tests.md): behavior-focused, specific assertions, independent oracles, controlled inputs and justified faithful doubles.
- [ ] The owning test record retains the user's decisions and the evidence for every `done` item.
