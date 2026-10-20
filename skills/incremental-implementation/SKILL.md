---
name: incremental-implementation
description: Breaks a unit of work into small vertical slices and drives each one through test-driven development (Red-Green-Refactor) before committing it. Use when implementing a non-trivial change, or picking up a unit of work already broken into slices by a prior planning step — especially when the work is large enough that writing it in one pass risks producing untested, unreviewable code. Not for trivial single-location edits (a label, a comment, a config value, a formatting change) or for a pure investigation/spike that isn't meant to produce kept code.
---

# Incremental Implementation

## Overview

Implementing a unit of work as a sequence of small, independently verifiable vertical slices — each committed before the next begins — keeps every increment of work provably correct and reviewable on its own, with nothing considered finished until a test demonstrates it works.

## When to Use

- A change spanning more than one file or more than one part of the system.
- Implementing a unit of work broken down from a larger plan — whether or not it has already been broken into slices.
- Modifying or extending existing behavior where side effects are a real risk.

## When Not to Use

- A trivial, single-location change with no distinct behavior to verify (a label, a comment, a config value, a formatting-only change, a dependency bump with no behavior change).
- A change with no outcome a test can observe (a purely visual or manual-only adjustment).
- A pure exploratory spike or investigation that isn't meant to produce kept code.

## Input

- A description of the unit of work (required).
- Access to the codebase and the ability to run its test command, plus whichever of build, lint, and type-check the project defines (required).
- An existing slice breakdown from a prior planning step (optional; if absent, this skill produces one).

## Output

- The unit of work fully implemented as a sequence of separate commits, one per slice.
- Each commit leaves the test suite passing and, where the project has a build step, still building successfully.
- Each slice's behavior is covered by at least one test introduced specifically for it.

## Core Principles

1. **Vertical slice, defined precisely.** A slice crosses the full depth of its unit of work — never stopping partway through — and produces an outcome verifiable on its own. Full depth is set by the boundary of that unit of work, not a fixed, named list of parts.
2. **One strategy, two kinds of technique.** Vertical slicing is the only strategy. Some techniques perform the actual cut; others only reorder or coordinate around slices already cut, and apply only when their specific condition holds — never as a substitute for a real cut.
3. **Slicing is recursive.** A slice still too large to implement safely in one pass is split again, narrowed to whatever is making it too large.
4. **TDD drives each slice from the inside.** A slice is built behavior by behavior through Red-Green-Refactor; it isn't complete until every behavior it needs has gone through that cycle.
5. **Discover before assuming.** Verification commands, the unit-of-work boundary, and existing conventions are read from the project itself, never assumed by default.

## Workflow

### Step 1 — Discover Boundary, Commands, Baseline, and Existing Slicing

Before doing anything else, establish:

- **Unit-of-work boundary** — the part of the system this task is responsible for, and therefore what "full depth" means for it. Infer it from the task description and the codebase's own structure; ask only if it cannot be determined from them.
- **Verification commands** — the test, build, lint, and type-check commands the project actually defines. Read its configuration/manifest files; never assume a default command exists.
- **Baseline health** — run the existing test suite once. It must be green before any new slice starts; if it is not, fixing it is a prerequisite, not one of this task's own slices.
- **Existing slicing** — check whether the work is already broken into slices by an earlier step. If so, skip Step 2 and take each given slice, in order, into Step 3. If not, proceed to Step 2.

### Step 2 — Identify the Next Slice

Skip this step entirely if Step 1 found an existing breakdown. Otherwise, apply a default-tier technique (see Slicing Techniques) to pick the smallest next slice that still crosses the full depth of the unit-of-work boundary and meets the Slice Quality Bar. Apply a conditional-tier technique alongside this step only if its condition holds. Re-apply this step recursively if the candidate slice still fails the quality bar.

### Step 3 — Implement the Slice Through TDD Micro-Cycles

For each behavior the slice needs:

1. **Red** — write one test for the behavior; run it; confirm it fails for the expected reason.
2. **Green** — write the minimum code to make that test pass; run it; confirm it passes.
3. **Refactor** — clean up only while all tests stay green; introduce no new behavior here.

Repeat for the next behavior until the slice's scope is fully covered.

### Step 4 — Verify the Slice

Run the project's own verification commands from Step 1 and confirm the slice works end-to-end within its boundary:

- The full test suite passes, not just the new slice's tests.
- The project builds successfully, if it has a build step.
- Type-checking passes, if the project has a type-checking step.
- Linting/formatting passes, if the project enforces one.
- The new behavior is confirmed working, via its test and a manual/exploratory check where relevant.

### Step 5 — Commit

Commit the slice with a message that accurately describes the one behavior it adds. Follow the project's existing commit convention where one is already established; otherwise, an accurate, specific description is sufficient. One slice corresponds to one commit.

### Step 6 — Move to the Next Slice

If slices were already defined in Step 1, move to the next one and return to Step 3. If not, return to Step 2. Build on completed slices; never redo them.

## Slicing Techniques

All of the following exist to find a valid vertical cut (Principle 1) or to work with slices already cut that way (Principle 2) — never to replace the cut itself. "Depth" means every distinct part of the unit of work that has to cooperate to produce the slice's outcome; what those parts actually are depends entirely on the codebase being worked in, not on a fixed list. The example beside each technique illustrates one instance of it, not a required shape. See `references/slicing-techniques.md` for further variants, additional worked examples across different kinds of work, and a full worked walkthrough of recursive slicing.

### Default tier — techniques that perform the cut

- **Selection rule:** pick the one technique that best fits the current source of size — do not run through the whole catalog for every unit of work.
- **Recursion rule:** after producing a slice, check it against the Slice Quality Bar; if it still fails, split it again using whichever technique fits what is making it too large.

| Technique                   | Fits when…                                                                   | Example                                                                                                                                                                               |
| --------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Workflow step               | The unit of work is a multi-step process.                                    | A checkout process → slice 1: add an item to the cart; slice 2: apply a discount code; slice 3: confirm payment.                                                                      |
| Operation boundary          | The unit of work exposes several distinct operations on the same thing.      | A "manage notes" feature → slice 1: create a note; slice 2: list notes; slice 3: edit a note; slice 4: delete a note.                                                                 |
| Happy path / rule variation | The unit of work has one main success case plus several rules or edge cases. | A "transfer money" feature → slice 1: transfer between two valid accounts with sufficient balance; slice 2: reject insufficient balance; slice 3: enforce a daily transfer limit.     |
| Data / input variation      | The unit of work handles more than one kind or source of data.               | An "import contacts" feature → slice 1: add a contact through a form; slice 2: import contacts from a file.                                                                           |
| Tracer bullet               | The connection between the parts of the current boundary is unproven.        | Before building a full messaging feature, first prove one hardcoded message can travel from the entry point through to storage and back. Still a full-depth cut — only a minimal one. |

### Conditional tier — techniques that order or coordinate, never cut

| Technique      | Condition to apply                                                                                                                     | What it actually does                                                                                                                                                                                                                                                                                                       |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Risk-first     | Several valid vertical slices are already identified, and uncertainty is concentrated in one of them.                                  | Changes the _order_ in which already-cut slices are implemented — the one that resolves the greatest uncertainty goes first. It does not define a new kind of cut; the prioritized slice still has to meet the full Slice Quality Bar on its own.                                                                           |
| Contract-first | The same unit of work is being built by more than one independent party at the same time, each responsible for a different part of it. | Defines the interface between the parties as an explicit, agreed artifact before either side implements against it. Each party still produces its own vertical slice within its own boundary using the default tier — this technique only removes the need for both sides to be built together before either can be tested. |

## Slice Quality Bar

A slice is ready to implement — and a split can stop — once it satisfies all of:

- **Vertical** — crosses the full depth of the unit-of-work boundary; does not stop partway through it.
- **Testable** — at least one test can express its behavior through the project's test mechanism.
- **Verifiable** — its outcome can be confirmed without any other unfinished slice existing.
- **Shippable** — it can be tested and merged on its own; the project still builds, where it has a build step, and every existing test still passes after it lands.
- **Small** — completable within one focused run of TDD micro-cycles, without an extended stretch of code written ahead of a running test.

## Implementation Rules

- **Simplicity first.** Build the simplest version that satisfies the behavior's test — not one that anticipates requirements the test doesn't yet demand. Afterward, check it: could it be shorter, is each abstraction already earning its complexity at this one use, would a reviewer reasonably ask "why not just do it directly?" Prefer a few duplicated lines over a shared abstraction introduced before a third real use case demands it.
- **Footprint discipline.** Touch only the files and lines the current slice's behavior requires. Do not clean up, reformat, refactor, or modernize anything adjacent just because it's nearby, and do not add behavior the slice's tests don't call for. If something outside the slice looks worth improving, note it instead of fixing it inline, and raise it as a separate decision.
- **One thing at a time.** Each slice, and each commit within it, changes exactly one logical thing. A change that adds new behavior, reshapes unrelated existing code, and edits configuration all at once is several changes wearing one commit — split it into one commit per change instead.
- **Keep it green.** After every slice, not only at the end of the whole unit of work, the project is left in a state where it builds (where it has a build step) and every existing test passes — nothing is committed in a state the next slice would have to work around.
- **Feature flags for incomplete work.** When a slice is correct and tested but the unit of work it belongs to isn't ready to be user-visible, merge it behind a flag defaulted off rather than holding the commit back. Add that flag with the first such slice, not after several have already landed unflagged.
- **Safe defaults.** New behavior defaults to off, or to its most conservative option, unless a test specifically requires otherwise; anything riskier or more user-facing is opt-in, not opt-out.
- **Rollback-friendly.** Prefer additive changes — new files, functions, fields — over modifying existing ones, since additive changes revert cleanly on their own. Where existing code must change, keep the change minimal and isolated. Where the unit of work includes a reversible operation (e.g., a data or schema migration), give it a corresponding rollback path. Never delete something and replace it with its successor in the same commit — land the replacement first, remove the old path in a later, separate commit.

## Common Rationalizations to Reject

| Rationalization                                                                 | Reality                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "I'll write the test after — the logic is already right."                       | A test written after the code is no longer an independent check; it stops functioning as the constraint that TDD depends on.                                                                                                                 |
| "This test is just wrong, I'll loosen or remove the assertion."                 | A known failure mode under TDD: weakening or deleting a failing test instead of fixing the implementation behind it. Only acceptable if the test is demonstrably incorrect, and that reasoning must be stated explicitly before changing it. |
| "This needs to work end-to-end, so I'll touch parts outside what was assigned." | Vertical means full depth within the current unit-of-work boundary — not more than what that boundary includes.                                                                                                                              |
| "I'll write several tests, then implement all of them together."                | Breaks the micro-cycle and reintroduces code-first risk inside a slice that is nominally test-driven.                                                                                                                                        |
| "This slice is basically done, I'll skip re-running the full suite."            | A slice is not verified until Step 4 actually runs; skipping it is how regressions slip between slices unnoticed.                                                                                                                            |
| "These changes are too small to commit separately."                             | Small commits are free. Large commits hide bugs and make rollbacks painful.                                                                                                                                                                  |

## Verification

Before presenting the work as complete, check all of the following:

- [ ] Every slice went through Red before any implementation code for it existed.
- [ ] No failing test was weakened or deleted to make it pass; every fix addressed the implementation instead.
- [ ] Every slice independently satisfies the Slice Quality Bar.
- [ ] Every slice has its own commit, and each commit message accurately describes what it does.
- [ ] The full test suite, build, lint, and type-check (whichever the project defines) all pass after the final slice.
- [ ] No file or part was touched outside the unit-of-work boundary established in Step 1.
- [ ] None of the Common Rationalizations above were used to justify skipping a step.
