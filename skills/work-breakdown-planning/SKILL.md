---
name: work-breakdown-planning
description: Breaks a unit of work of any size into small, independently deliverable vertical slices and plans them with acceptance criteria, acyclic dependencies and status, saved as a plan document. Supports a one-level or fully recursive split, and extending an existing plan. Use when the user asks to break down, decompose, split or plan a piece of work, or to update such a breakdown, even if they do not say "slice". Not for carrying out the work or for trivial single-location edits.
metadata:
  author: phatnguyen975
  version: 1.0
---

# Work Breakdown Planning

## Overview

Turns one **Work Item** into a **Slice Plan** — a set of vertical **Slices**, each small, unambiguous and deliverable on its own — with acceptance criteria, hard dependencies forming a directed acyclic graph (DAG), execution waves and status.

- Splits with vertical slicing: every Slice delivers an observable outcome end to end, never a single layer or phase.
- Offers two modes: one split (`Flat`) or repeated splitting until every Slice is small enough (`Recursive`).
- Always plans: acceptance criteria, dependencies, order and status exist in both modes.
- Writes exactly one artifact, the Slice Plan file. It never creates or changes the work product itself.

## When to Use

- A Work Item is too large or too vague to carry out, or hand off, in one piece.
- Acceptance criteria, ordering or dependencies must be explicit before work starts.
- Work will be distributed to several people or agents, each of whom may break their part down further.
- An existing Slice Plan needs its status synchronized or needs additional scope.

## When NOT to Use

- The request is to carry out the work. This skill only plans it.
- The Work Item is a trivial single-location edit with no behavior to verify.
- The request is for effort estimates or calendar scheduling. The plan defines order, not durations.
- The request is to rewrite or reorder slices of an existing plan. Sync only appends.

## Terminology

Use these terms consistently. When the project defines its own terms, use the project's terms in the Slice Plan.

| Term                          | Definition                                                                                                     |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Work Item**                 | Input. Any unit of work to be broken down, of any size.                                                        |
| **Slice**                     | Output of a Split. A vertical, independently deliverable piece; also the unit that is planned.                 |
| **Split**                     | One cut of a Work Item or Slice into two or more Slices using exactly one technique.                           |
| **Boundary**                  | The extent the Work Item is responsible for. "Full depth" is defined against it.                               |
| **Full depth**                | Every component that must cooperate to produce a Slice's outcome, inside the Boundary.                         |
| **Acceptance Criterion (AC)** | A binary, observable condition describing a Slice's outcome.                                                   |
| **Contract**                  | The interface agreed between independent parties building parts of one Work Item.                              |
| **Reference**                 | A document outside the plan (specification, design, convention, decision record) that the Work Item relies on. |
| **Slice Quality Bar**         | The criteria a Slice must meet to be ready.                                                                    |
| **Scope Assessment**          | Evaluation of the _Small_ criterion through observable Scope Signals.                                          |
| **Atomic / Coarse**           | `Atomic`: meets the full Slice Quality Bar. `Coarse`: not confirmed small enough.                              |
| **Dependency**                | A hard prerequisite between two Slices. All Dependencies form a DAG.                                           |
| **Wave**                      | A set of Slices with no Dependencies among them; they can start together.                                      |
| **Slice Plan**                | The output document.                                                                                           |
| **Sync**                      | Updating an existing Slice Plan.                                                                               |
| **Project Conventions**       | The project's own rules: terminology, plan location, verification commands.                                    |

## Input

| Input               | Type                   | Required | Notes                                                      |
| ------------------- | ---------------------- | -------- | ---------------------------------------------------------- |
| Work Item           | Text, document or link | Required | Any kind and size.                                         |
| Mode                | `Flat` or `Recursive`  | Required | Ask the human when the request does not state it.          |
| References          | Paths or links         | Optional | Only documents the human provides or confirms.             |
| Output location     | Path                   | Optional | Overrides Project Conventions and the default.             |
| Existing Slice Plan | File                   | Optional | Its presence for the same Work Item selects the Sync flow. |

## Output

- One Slice Plan file following `assets/slice-plan-template.md`. Read the template before writing.
- `Source` field identifies the Work Item so Sync can find the plan again.
  - Use the Work Item's own reference as the project identifies it (identifier, link or path).
  - For a Slice taken from another Slice Plan, use that plan's path plus the Slice ID.
  - For a Work Item given only as text, write one line stating where it came from.
- Generation rules for the file:
  - Every `<!-- comment: ... -->` in the template is an instruction to the agent. Delete all comments from the generated file.
  - Replace every `<placeholder>` with real content. No placeholder remains.
  - Omit entries marked "only when applicable" when they do not apply.
  - Write content in the language Project Conventions require; otherwise in the language the human used.
- A short report in the conversation: Slice count, Wave count, and every `Coarse` Slice with its reason.

## Core Principles

1. **Vertical only.** Each Slice crosses full depth and has an outcome that can be checked on its own. Splitting by layer or by work phase is invalid.
2. **One technique per Split**, chosen by the dominant source of size.
3. **Coverage.** The child Slices together equal the parent's scope: nothing missing, nothing overlapping, nothing added.
4. **Every Slice is planned:** acceptance criteria, dependencies and status, in both modes.
5. **Dependencies are hard prerequisites only.** The graph is a DAG. Shared parts belong to the first Slice that needs them.
6. **Rule-based stopping.** Scope Assessment and the stop guards end the recursion, not impression.
7. **No assumptions.** Every unclear point is asked and confirmed with the human before splitting. The plan contains no assumptions and no open questions.
8. **Project Conventions first.** Terminology, plan location and verification commands follow the project.
9. **Single source of truth.** Slice data is authoritative. The graph, waves and progress counts are derived and regenerated.
10. **Append-only re-planning.** Existing Slices keep their IDs, content, acceptance criteria and dependencies.

## Modes

|             | `Flat`                                                  | `Recursive`                                         |
| ----------- | ------------------------------------------------------- | --------------------------------------------------- |
| Splits      | Exactly one, on the Work Item                           | Repeated on every Slice that fails the bar          |
| Bar applied | Slice Quality Bar except _Small_                        | Full Slice Quality Bar                              |
| Stops       | After the first Split                                   | When all Slices are `Atomic`, or a guard is reached |
| Granularity | `Atomic` if Scope Assessment passes, otherwise `Coarse` | `Atomic`; `Coarse` only when a guard is reached     |
| Planning    | Always                                                  | Always                                              |

A `Coarse` Slice can be handed to someone else, who runs this skill again with that Slice as the Work Item and gets a separate Slice Plan whose `Source` is the original plan's path plus that Slice's ID.

## Workflow

### Create flow

**Step 1: Establish Context**

- Read Project Conventions: terminology, plan location, verification commands.
- Look for an existing Slice Plan for this Work Item in the plan location (see Output Location), matching on the `Source` value. If one exists, follow the Sync flow.
- Determine the Mode. Ask the human when it is not stated.

**Step 2: Understand the Work Item**

- Determine the boundary and what full depth means for it.
- List every unclear point: outcome, boundary, business rules, data, interfaces, constraints, completion criteria, supporting documents.
- Ask the human about each point, grouped into one round per topic. Use this form for every question:
  ```
  Q<n>. <question>
    Recommended: <option> — <short reason>
    Alternatives:
      - <option>
      - <option>
  ```
  When only the human can know the answer, ask openly and state that no recommendation exists.
- A recommendation takes effect only after the human confirms it. Never decide on the human's behalf.
- Register as references only documents the human provides or confirms, after checking they are accessible.
- Continue only when no point remains unconfirmed. Fold the answers into outcome, boundary, references, scope lists and acceptance criteria.

**Step 3: Split**

- If the Work Item already meets the full Slice Quality Bar, produce a single Slice, apply no technique, and log it with the technique "None (already meets the Quality Bar)".
- Otherwise read `references/slicing-techniques.md`, choose a technique, and Split.
- Check Coverage after every Split.
- Evaluate every Slice against the Slice Quality Bar.
- `Recursive`: repeat on each failing Slice under the guards below. `Flat`: stop after the first Split.
- Record every Split in the Slicing Log. Only final Slices receive IDs; intermediate Slices that were split further appear by title.
- When a new unclear point appears, stop, ask the human with the question form above, and continue after confirmation.

**Step 4: Plan**

- For each Slice write: Outcome, In scope, Out of scope, References, Acceptance Criteria, Verification, Depends on.
- Define Dependencies using the rules in `references/dependency-and-status.md`, then run the cycle check, compute Waves and assign initial statuses as that file describes. Fill Progress, Dependency Graph and Execution Order from the Slice data.
- When a reference and an acceptance criterion conflict, stop and ask the human.
- When a new unclear point appears, stop and ask as in Step 3.

**Step 5: Resolve Location**

- Resolve the path and file name as described in Output Location. Confirm with the human when required.

**Step 6: Save and Verify**

- Write the Slice Plan from the template.
- Run the Verification checklist. When a Python 3 runtime is available, also run `scripts/validate_plan.py <plan-file>`.
- Report to the human: Slice count, Wave count, and each `Coarse` Slice with its reason.

### Sync flow

Runs when a Slice Plan already exists for the same Work Item.

1. Read the plan and check the status invariants in `references/dependency-and-status.md`.
2. Recompute derived statuses (`BLOCKED`, `READY`) from the graph. `IN-PROGRESS` and `DONE` are set by whoever does the work; report any invariant violation instead of changing them.
3. When scope was added: ask the human about every unclear point in the added scope, including supporting documents, applying the rules of Step 2; then run Steps 3–4 on that scope only. Append new Slices and new References with the next IDs. Amend the Work Item section only as far as the added scope requires: extend Outcome and Boundary, and remove an Excluded entry only when the human confirmed that item is now included.
4. Re-run the cycle check on the whole graph.
5. Regenerate Progress, Dependency Graph and Execution Order, append to the Slicing Log, update `Last synced`, and save in place.

Append-only rules:

- Existing Slices keep their ID, content, acceptance criteria and Dependencies.
- In the Work Item section, change only what the added scope requires. Do not reword other text.
- New Slices may depend on existing Slices.
- A Dependency may be added to an existing Slice only while it is `READY` or `BLOCKED`.
- A defect found after a Slice is `DONE` becomes a new Slice.

## Slice Quality Bar

| Criterion       | Meaning                                                                                                                                           |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Vertical**    | Crosses full depth inside the Boundary.                                                                                                           |
| **Testable**    | Has at least one acceptance criterion checkable by the project's verification mechanism, or by a manual check described exactly when none exists. |
| **Verifiable**  | Its outcome can be confirmed once its declared Dependencies are `DONE`, without any other unfinished Slice.                                       |
| **Shippable**   | Can be merged or delivered alone and leaves the whole in a working state.                                                                         |
| **Unambiguous** | Every acceptance criterion is binary and observable. No assumption, no open question.                                                             |
| **Small**       | Completable in one focused working session. Judged by Scope Assessment.                                                                           |

## Scope Assessment and Stop Conditions

_Small_ fails when any Scope Signal is present:

| #   | Scope Signal                                                                                             |
| --- | -------------------------------------------------------------------------------------------------------- |
| 1   | The outcome cannot be stated in one sentence without joining two separate behaviors with "and" or "or".  |
| 2   | More than 5 acceptance criteria.                                                                         |
| 3   | Several independent variations are bundled: operations, business rules, data shapes or entry/exit paths. |
| 4   | Two or more independent capabilities, each deliverable and usable alone.                                 |
| 5   | Acceptance criteria branch into fundamentally different results.                                         |

Guards for `Recursive` mode:

| Guard                        | Rule                                                                                                                                                 |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **G1: Pass**                 | A Slice meeting the full bar is `Atomic` and is never split again.                                                                                   |
| **G2: Progress**             | Each Split yields at least 2 Slices, each strictly narrower than the parent, and passes the Coverage check.                                          |
| **G3: Techniques exhausted** | Each technique is tried at most once per Slice. When none gives a valid Split, the Slice stays `Coarse` and is reported with the unmet Scope Signal. |
| **G4: Depth limit**          | At most 3 successive Splits from the Work Item. At the limit, failing Slices stay `Coarse` and are reported.                                         |

## Slicing Techniques

Catalog, selection rule, examples and a worked recursion are in `references/slicing-techniques.md`.

- **Default tier (cut):** Workflow step, Operation boundary, Happy path / rule variation, Data variation, Interface variation, Major effort, Quality-target deferral, Tracer bullet.
- **Conditional tier (order or coordinate, never cut):** Risk-first, Contract-first.

## Dependencies, Order and Status

Full rules, the cycle-check procedure and the status model are in `references/dependency-and-status.md`. Essentials:

- An edge `A → B` exists only when B cannot start or be verified until A is `DONE`.
- The graph must pass a topological-sort check before the plan is saved.
- Waves come from the topological layers; Slices in one Wave can run in parallel.
- Statuses are `READY`, `BLOCKED`, `IN-PROGRESS`, `DONE`. A Slice with no Dependencies starts `READY`; every other Slice starts `BLOCKED`.

## Output Location

Resolve in this order:

1. The location the human states in the request.
2. The location Project Conventions define. Use it without asking.
3. Otherwise propose the default and ask the human to confirm or override before writing.

Default: `docs/tasks/<work-item-ref>-<slug>.md`

- `<slug>`: short kebab-case form of the Work Item title.
- `<work-item-ref>`: the Work Item's own identifier when the project uses one; omit otherwise.
- Create the directory when it does not exist.

When the target file already exists:

- Same Work Item: follow the Sync flow.
- Different Work Item: do not overwrite. Propose another name and confirm with the human.

## Anti-Patterns

- Splitting by layer (all storage, then all logic, then all interface).
- Splitting by work phase (design, build, test as separate Slices).
- Cutting by arbitrary size instead of a named technique.
- A Slice without an observable outcome.
- A Split that loses or adds scope.
- A standalone "shared foundation" Slice instead of letting the first Slice that needs the part own it.
- Dependency edges for preferred order that is not a hard prerequisite.
- Splitting a Slice that already meets the Slice Quality Bar.
- Filling a gap with an assumption instead of asking.
- Leaving template comments or placeholders in the saved plan.

## Common Rationalizations to Reject

| Rationalization                                | Reality                                                                                 |
| ---------------------------------------------- | --------------------------------------------------------------------------------------- |
| "Split by layer, then join them."              | No Slice can confirm its outcome until the join; it violates Vertical.                  |
| "The order is obvious, skip the graph check."  | Cycles only show up when the procedure is run.                                          |
| "One more level of splitting to be safe."      | A Slice that meets the bar is never split again (G1).                                   |
| "This Slice is a bit large but acceptable."    | It passes Scope Assessment or it is marked `Coarse` and reported.                       |
| "The answer is probably X, so I'll proceed."   | Unclear points are asked and confirmed. Guessing is how errors spread into later steps. |
| "Rewrite the old plan to match the new scope." | Re-planning appends; existing Slices stay as they are.                                  |
| "I'll pick a location that seems fine."        | Use the human's or the project's location; otherwise confirm the default.               |

## Verification

Run before presenting the plan.

- [ ] Coverage: the Slices together equal the Work Item's scope, with no overlap.
- [ ] Every unclear point was confirmed by the human; the plan contains no assumption and no open question.
- [ ] Every Slice has Outcome, In/Out of scope, Acceptance Criteria, Verification, Depends on, Status and Granularity.
- [ ] Every acceptance criterion is binary and observable, and every one is covered by a Verification line.
- [ ] Every Reference is accessible; every Slice reference points to an existing ID and the narrowest relevant part.
- [ ] `Recursive`: every Slice is `Atomic`, or each `Coarse` Slice states the Scope Signal or guard that stopped it.
- [ ] The graph has no cycle, no self-dependency and no reference to a missing ID.
- [ ] Waves, Dependency Graph and Progress match the Slice data.
- [ ] Initial statuses are correct and satisfy the invariants.
- [ ] Location and file name follow Output Location; confirmation was obtained when required.
- [ ] No template comment or placeholder remains in the saved file.
- [ ] No work product was created or changed.
