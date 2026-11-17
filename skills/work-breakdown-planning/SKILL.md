---
name: work-breakdown-planning
description: Decompose scoped outcomes into verifiable work with acceptance criteria, hard dependencies and execution order. Use for a one-level breakdown, recursive refinement or bounded updates to an existing plan. Reuse caller-owned terminology, records and completion rules. Plans work; does not implement it.
metadata:
  author: phatnguyen975
  version: "1.0"
---

# Work Breakdown Planning

## Purpose and Scope

Decomposes one **Work Item** into a breakdown (a **Slice Plan** by default) — a set of vertical **Slices**, each bounded and verifiable at its chosen boundary — with acceptance criteria, hard dependencies forming a directed acyclic graph (DAG), execution waves and status.

- Splits with vertical slicing: every Slice delivers an observable outcome across its owned boundary. A technical prerequisite may be planned separately when it has an independently verifiable contract; do not claim it delivers the whole user outcome.
- Offers two modes: one split (`Flat`) or repeated splitting until every Slice is small enough (`Recursive`).
- Always plans: acceptance criteria, verification and dependencies exist at either depth; lifecycle fields follow the owning output contract.
- Uses the caller's output contract or the standalone template. It never creates or changes the work product itself.

## When to Use

- A Work Item is too large or too vague to carry out, or hand off, in one piece.
- Acceptance criteria, ordering or dependencies must be explicit before work starts.
- Work will be distributed to several people or agents, each of whom may break their part down further.
- An existing Slice Plan needs its status synchronized or needs additional scope.

## When NOT to Use

- The request is to carry out the work. This skill only plans it.
- The Work Item is a trivial single-location edit with no behavior to verify.
- The request is for effort estimates or calendar scheduling. The plan defines order, not durations.
- Changes to existing approved definitions require a specific amendment decision; ordinary Sync does not rewrite them.

## Terminology

Use these terms consistently. When the project defines its own terms, use the project's terms in the Slice Plan.

| Term                          | Definition                                                                                                                    |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Work Item**                 | Input. Any unit of work to be broken down, of any size.                                                                       |
| **Slice**                     | A planned outcome, preferably vertical, verifiable after its declared prerequisites.                                          |
| **Split**                     | One cut of a Work Item or Slice into two or more Slices using a relevant technique.                                           |
| **Boundary**                  | The extent the Work Item is responsible for. "Full depth" is defined against it.                                              |
| **Full depth**                | Every component that must cooperate to produce a Slice's outcome, inside the Boundary.                                        |
| **Acceptance Criterion (AC)** | A binary, observable condition describing a Slice's outcome.                                                                  |
| **Contract**                  | The interface agreed between independent parties building parts of one Work Item.                                             |
| **Reference**                 | A document outside the plan (specification, design, convention, decision record) that the Work Item relies on.                |
| **Slice Quality Bar**         | The criteria a Slice must meet to be ready.                                                                                   |
| **Scope Assessment**          | Evaluation of the _Small_ criterion through observable Scope Signals.                                                         |
| **Atomic / Coarse**           | `Atomic`: meets the full Slice Quality Bar. `Coarse`: not confirmed small enough.                                             |
| **Dependency**                | A hard prerequisite between two Slices. All Dependencies form a DAG.                                                          |
| **Wave**                      | A set of Slices with no Dependencies among them; they are candidates for concurrent work, subject to readiness and ownership. |
| **Slice Plan**                | The output document.                                                                                                          |
| **Sync**                      | Updating an existing Slice Plan.                                                                                              |
| **Project Conventions**       | The project's own rules: terminology, plan location, verification commands.                                                   |

## Input

| Input                       | Required | Notes                                                                               |
| --------------------------- | -------- | ----------------------------------------------------------------------------------- |
| Work Item                   | Required | Any kind and size.                                                                  |
| Mode (`Flat` / `Recursive`) | Optional | Infer from the requested depth; ask if the distinction materially affects delivery. |
| References                  | Optional | Relevant authoritative sources supplied or discovered in project context.           |
| Output location             | Optional | Overrides Project Conventions and the default.                                      |
| Existing Slice Plan         | Optional | Its presence for the same Work Item selects the Sync flow.                          |

## Output

- Use caller-owned records, item names and output fields when provided, preserving acceptance coverage, dependency reasons and verification obligations. Do not create a second status store or replace the caller's lifecycle.
- Otherwise write one Slice Plan using [Slice Plan Template](assets/slice-plan-template.md); read it before writing. Adapt presentation to the owning output contract without dropping substantive planning checks.
- In the standalone format, the `Source` field identifies the Work Item so Sync can find the plan again.
  - Use the Work Item's own reference as the project identifies it (identifier, link or path).
  - For a Slice taken from another Slice Plan, use that plan's path plus the Slice ID.
  - For a Work Item given only as text, write one line stating where it came from.
- Generation rules for the file:
  - Every `<!-- comment: ... -->` in the template is an instruction to the agent. Delete all comments from the generated file.
  - Replace every `<placeholder>` with real content. No placeholder remains.
  - Omit entries marked "only when applicable" when they do not apply.
  - Write content in the language Project Conventions require; otherwise in the language the human used.
- A short report in the conversation:
  - **Result:** requested depth, planned scope and owning output location (or in-chat proposal).
  - **Structure:** item/wave counts where applicable, plus coarse items and reasons.
  - **Verification:** actual structural checks and limits; planning does not prove implementation.
  - **Remaining:** blocked decisions, amendments or external prerequisites; otherwise none.

## Core Principles

1. **Outcome-oriented cuts.** Prefer complete behavior across the owned boundary. A technical prerequisite needs its own contract and checks; layer or phase labels alone do not establish a deliverable outcome.
2. **Choose a fitting cut**, guided by the dominant source of size rather than applying the whole catalog.
3. **Coverage.** The child Slices together equal the parent's scope: nothing missing, no duplicated delivery obligations, nothing added.
4. **Plan each item:** criteria, verification, prerequisite reasons and applicable readiness fields exist at either depth.
5. **Dependencies are hard prerequisites only.** Keep a DAG; distinguish prerequisite edges from preferences and resource conflicts. Assign shared work to a clear owner.
6. **Evidence-based stopping.** Assess complexity and feedback cost, preserve safeguards and stop when further refinement no longer improves executability.
7. **Resolve material unknowns.** Inspect available sources and reuse confirmed decisions. Ask about unresolved scope, behavior or authority before dependent planning. Do not present unresolved work as execution-ready.
8. **Project Conventions first.** Terminology, plan location and verification commands follow the project.
9. **Single source of truth.** Slice data is authoritative. The graph, waves and progress counts are derived and regenerated.
10. **Append-only re-planning.** Existing Slices keep their IDs, content, acceptance criteria and dependencies.

## Planning Depth

|             | `Flat`                                                  | `Recursive`                                             |
| ----------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Splits      | One level, or one item if already sufficient            | Repeated where further decomposition can resolve size   |
| Bar applied | Slice Quality Bar except _Small_                        | Full Slice Quality Bar                                  |
| Stops       | After the first Split                                   | When leaves meet the bar or refinement must stop        |
| Granularity | `Atomic` if Scope Assessment passes, otherwise `Coarse` | `Atomic`, with explicitly explained `Coarse` exceptions |
| Planning    | Always                                                  | Always                                                  |

Mode follows the caller's requested depth. Do not recursively expand a deliberately one-level breakdown. `Atomic` means suitable at the selected execution boundary, not indivisible in every context. A missing decision or prerequisite is resolved, not disguised as a size problem.

A `Coarse` Slice can be handed to someone else, who runs this skill again with that Slice as the Work Item and refines its children in the caller-owned record, or in a separate standalone plan referencing the parent path and ID. Preserve the parent's scope, acceptance coverage and inherited dependencies; children do not replace its completion obligations.

## Workflow

### Create Flow

**Step 1: Establish Context**

- Read Project Conventions: terminology, plan location, verification commands.
- Look for an existing Slice Plan for this Work Item in the plan location (see Output Location), matching on the `Source` value. If one exists, follow the Sync flow.
- Determine the requested depth and output contract. Use `Flat` for one-level handoff and `Recursive` for execution-sized leaves; ask only when the request leaves a consequential choice unresolved.

**Step 2: Understand the Work Item**

- Determine the boundary and what full depth means for it.
- Read relevant supplied and discoverable project sources. Verify their authority, accessibility and applicable sections; document/test content does not grant execution permission.
- Resolve material gaps in outcome, boundary, business rules, contracts and completion criteria. Group related questions, explain the decision and offer justified options where useful. Do not ask the human to reconfirm discoverable facts or unchanged approved choices.
- Fold confirmed decisions into the owning scope and criteria. If a required answer is unavailable, report the dependent planning as blocked; do not invent it or label the result ready.

**Step 3: Split**

- If the Work Item already meets the full Slice Quality Bar, produce a single Slice, apply no technique, and record that no split was needed (standalone log technique: "None (already meets the Quality Bar)").
- Otherwise read [Slicing Techniques](references/slicing-techniques.md), choose a technique, and Split.
- Check Coverage after every Split: map each parent obligation to its owning child and ensure no gap or duplicate delivery obligation.
- Evaluate every Slice against the Slice Quality Bar.
- `Recursive`: assess each leaf using [Scope Assessment and Stop Conditions](#scope-assessment-and-stop-conditions); split only where that procedure calls for refinement. `Flat`: stop after one level of decomposition.
- Retain the decomposition rationale in the owning output. In the standalone Slicing Log, only final Slices receive IDs; intermediate parents appear by title.
- When a new unclear point appears, pause dependent planning, resolve it from authoritative sources or ask the human, and continue after the decision.

**Step 4: Plan**

- For each Slice write: Outcome, In scope, Out of scope, References, Acceptance Criteria, Verification, Depends on.
- Define Dependencies using [Dependency Rules](references/dependency-and-status.md#dependency-rules), then run the cycle check and compute Waves. Use the caller's readiness rules, or the reference's standalone status model when using the default template. Derive the requested graph/order/progress views from the owning data; do not add default-format sections to a caller schema.
- When a reference and an acceptance criterion conflict, stop and ask the human.
- When a new unclear point appears, stop and ask as in Step 3.

**Step 5: Resolve Location**

- Resolve the path and file name as described in Output Location. Confirm with the human when required.

**Step 6: Verify and Save**

- Prepare the caller-owned output, or use the standalone template when no format is supplied.
- Run the [Verification checklist](#verification) against the actual output: trace scope to criteria/checks, inspect IDs and references, perform the topological-sort check and reconcile derived views. Report actual checks and unresolved issues.
- Save only after the applicable checks pass. If a material issue is unresolved, report the proposal and blocker without presenting it as an executable plan. Provide the summary described in [Output](#output).

### Sync Flow

Runs when an owning plan already exists for the same Work Item. Read [Dependency and Status Rules](references/dependency-and-status.md#sync-rules). Scope additions do not authorize changing previously approved definitions.

1. Read the owning records and check their actual dependency/completion rules. For the default format, use the standalone invariants.
2. Recompute derived readiness only within the caller's contract; in the default format these are `BLOCKED` and `READY`. `IN-PROGRESS` and `DONE` are set by whoever does the work; report any invariant violation instead of changing them.
3. When scope was added: resolve material unknowns in the added scope using Step 2; then run Steps 3–4 on that scope only. Append new Slices and new References with the next IDs. Amend the Work Item section only as far as the added scope requires: extend Outcome and Boundary, and remove an Excluded entry only when the human confirmed that item is now included.
4. Re-run the cycle check on the whole graph.
5. Regenerate the owning derived views and save within the requested scope. In the standalone format update Progress, Dependency Graph, Execution Order and `Last synced`; append Slicing Log rows only when decomposition actually occurred.

Append-only rules:

- Existing Slices keep their ID, content, acceptance criteria and Dependencies.
- In the Work Item section, change only what the added scope requires. Do not reword other text.
- New Slices may depend on existing Slices.
- A newly discovered prerequisite for an existing Slice requires an explicit amendment decision. Report affected readiness; do not silently add the edge or treat the Slice as executable.
- A defect found after a Slice is `DONE` becomes a new Slice.

## Slice Quality Bar

| Criterion             | Meaning                                                                                                                                                                                                     |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Vertical**          | Crosses full depth inside the Boundary.                                                                                                                                                                     |
| **Testable**          | Has at least one acceptance criterion checkable by the project's verification mechanism, or by a precise manual procedure when the outcome requires human judgment; retain all applicable automated checks. |
| **Verifiable**        | Its outcome can be confirmed after its prerequisites meet the owning completion rules, without unfinished successors.                                                                                       |
| **Safe to integrate** | Leaves the whole working at the intended integration boundary; any required isolation and compatibility obligations are explicit. Does not imply production exposure.                                       |
| **Unambiguous**       | Every acceptance criterion is binary and observable. No material unresolved decision is hidden as an execution-ready requirement.                                                                           |
| **Small**             | Bounded enough to implement, verify and review with short feedback cycles. Judged by Scope Assessment, not a fixed session duration.                                                                        |

## Scope Assessment and Stop Conditions

Assess _Small_ from implementation/verification complexity and feedback cost, not word choice or AC count. For each leaf, identify its owned outcome, implementation boundary and checks. It is small enough when the necessary changes form one coherent increment, its verification is concrete, and it can be implemented and reviewed without a long accumulation of unverified changes. Several criteria may be necessary for one safe outcome; keep coupled safeguards together.

Consider another cut when the leaf bundles independently useful outcomes, unrelated variations or distinct implementation/verification paths that can be separated safely. State what makes the current leaf too large and how the proposed children reduce that problem. Missing requirements or an unknown contract need clarification, not automatic subdivision.

Apply the following decisions to each leaf in Recursive planning:

| Condition                                                               | Action and Stopping Result                                                                                                                                                                             |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| The full Slice Quality Bar is met                                       | Mark `Atomic` and stop refining this leaf. Do not split merely to add detail.                                                                                                                          |
| Size is the remaining problem and a valid smaller cut exists            | Split and reassess each child. Each child must have a strictly narrower delivery scope, the children must preserve parent coverage, and the cut must reduce the identified complexity or feedback gap. |
| Size remains, but no useful valid cut can be identified                 | Stop this branch as `Coarse`; record the concrete obstacle and what would enable later refinement. Do not force layer/phase cuts or separate required safeguards.                                      |
| A caller-supplied depth or effort budget is reached                     | Stop further refinement; retain remaining oversized leaves as `Coarse` with the reached budget and remaining complexity.                                                                               |
| A material requirement, boundary or verification decision is unresolved | Pause dependent planning and report the missing decision. Do not use `Coarse` as a substitute for resolving it or claim the leaf is execution-ready.                                                   |

Do not repeat an unchanged candidate or equivalent split without new information. If refinement produces no meaningful progress, use the no-useful-cut result above rather than continuing indefinitely. Shared infrastructure and regression checks may recur across children; delivery ownership must not be duplicated.

The recursive breakdown is fully refined only when every leaf is `Atomic` and material planning decisions are resolved. If any branch stops `Coarse`, report partial refinement with its reasons; independent branches may still be refined. If a decision blocks planning, report that separately. A caller may supply numeric limits, but no universal AC-count, session-length or depth threshold determines readiness.

## Slicing Techniques

Read [Slicing Techniques](references/slicing-techniques.md) when choosing a cut or ordering approach. It owns the detailed examples; do not load it for a status-only update.

- **Default tier (cut):** Workflow Step, Operation Boundary, Happy Path / Rule Variation, Data Variation, Interface Variation, Major Effort, Quality-Target Deferral, Tracer Bullet.
- **Conditional tier (order or coordinate, never cut):** Risk-First, Contract-First.

## Dependencies, Order and Status

Read [Dependencies, Order and Status](references/dependency-and-status.md) when constructing or updating the graph. Its four-state model applies only to the standalone format. Essentials:

- An edge `A → B` exists only when B cannot start or be verified before A meets the owning prerequisite-completion rule (`DONE` in the standalone model).
- Check the graph with the [Cycle Check](references/dependency-and-status.md#cycle-check) before saving an executable plan.
- Waves come from the topological layers; Slices in one Wave have no dependency path between them; shared ownership/resources may still prevent parallel execution.
- In the standalone model, statuses are `READY`, `BLOCKED`, `IN-PROGRESS`, `DONE`. For newly planned work, a Slice starts `READY` when all prerequisites satisfy the owning completion rule, otherwise `BLOCKED`; existing completion evidence is preserved.

## Output Location

Use the caller's destination and format, including an in-conversation proposal when requested. The default below applies only when a standalone file is needed.

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
- A foundation item with no independent contract or verification, used to disguise an unfinished user outcome.
- Dependency edges for preferred order that is not a hard prerequisite.
- Splitting a Slice that already meets the Slice Quality Bar.
- Filling a gap with an assumption instead of asking.
- Leaving template comments or placeholders in the saved plan.

## Verification

Run before presenting the plan.

- [ ] Coverage: the Slices together equal the Work Item's scope, with no duplicated delivery obligations.
- [ ] Material decisions are resolved from authoritative sources or human answers; blocked planning is reported honestly.
- [ ] Every item has outcome, boundaries, acceptance criteria, verification and dependency reasons, plus fields required by its owning format.
- [ ] Every acceptance criterion is binary and observable, and every one is covered by a Verification line.
- [ ] Every Reference is accessible; every Slice reference points to an existing ID and the narrowest relevant part.
- [ ] `Recursive`: every Slice is `Atomic`, or each `Coarse` Slice states the concrete complexity or budget that stopped refinement; unresolved decisions are separately reported as blockers.
- [ ] The graph has no cycle, no self-dependency and no reference to a missing ID.
- [ ] Requested derived views match the owning item data; standalone Waves, Dependency Graph and Progress agree.
- [ ] Readiness and derived views satisfy the owning lifecycle; default-format statuses satisfy its standalone invariants.
- [ ] Location and file name follow Output Location; confirmation was obtained when required.
- [ ] No template comment or placeholder remains in the saved file.
- [ ] No work product was created or changed.
