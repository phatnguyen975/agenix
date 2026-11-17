---
name: incremental-implementation
description: Implement nontrivial changes through small verified increments. Use when executing an existing breakdown or organizing bounded work that is too risky to implement in one pass. Respect dependencies, selected verification methods and caller-defined commit cadence; report evidence and blockers for each increment.
metadata:
  author: phatnguyen975
  version: "1.0"
---

# Incremental Implementation

## Purpose and Scope

Coordinate implementation as a sequence of small, reviewable increments with observable outcomes. Prefer vertical slices that exercise a coherent behavior across the assigned boundary. A slice can build on verified predecessors; it must not depend on unfinished work to demonstrate its own outcome.

Use this skill to execute a supplied breakdown or select a manageable next increment within authorized work. It does not replace broader delivery planning, decide new product behavior or authorize publication. A simple edit that needs no incremental coordination or a purely exploratory investigation can be handled directly.

## Input

- **Outcome and boundary:** expected behavior, acceptance criteria, owned code/artifacts and applicable constraints. Resolve material unknowns before dependent implementation.
- **Project context:** relevant code, conventions, actual verification commands and required services/environments. Missing prerequisites block the affected work, not unrelated eligible increments.
- **Existing breakdown, when supplied:** item definitions, dependencies, selected verification methods and available completion evidence.
- **Execution policy, when supplied:** permitted operations, commit cadence, exposure requirements and output/evidence destination. Reuse existing authority; ask only for consequential unresolved choices.

## Output

Produce scoped code/artifact changes, relevant tests and verification evidence. Use the caller's record and output format when provided; do not create a competing plan or tracking file. Otherwise report progress in the conversation using the format below. Save a separate record only when requested or needed for continuity at an authorized location.

```markdown
## Implementation Summary

- **Outcome:** <completed / partial / blocked, within the requested boundary>
- **Candidate:** <commit or identifiable working-tree state; verification context>

| Increment       | Result                         | Evidence                                                                      | Remaining / Blocker |
| --------------- | ------------------------------ | ----------------------------------------------------------------------------- | ------------------- |
| <ID or outcome> | <verified / partial / blocked> | <method, command/procedure and actual result; evidence location if available> | <gap or none>       |

- **Final verification:** <combined checks, results and unavailable checks>
- **Delivery:** <local changes or actual authorized Git actions and IDs>
- **Decisions needed:** <specific unresolved choices, or none>
```

Keep detailed cycle evidence in its owning record and reference it here. A verified increment is not proof that the entire change is integrated, accepted or deployed. Do not claim completion while required checks or human-only judgments remain outstanding.

## Core Principles

1. **Honor the supplied breakdown.** Preserve approved outcomes, dependencies and verification obligations. Smaller implementation steps inside an item do not redefine its acceptance criteria.
2. **Verify at the owned boundary.** Choose observable outcomes, not layers or file counts. A provider double cannot establish real integration outside that boundary.
3. **Test first by default.** Use short Red-Green-Refactor cycles for behavior changes; honor a caller-selected test-after or manual method with explicit expected results and evidence.
4. **Keep progress recoverable.** Preserve user work, record actual results as obtained and leave each increment reviewable. Verification does not require a commit after every increment.
5. **Stay within authority.** Do routine implementation and checks under existing permission. New behavior, ownership changes, destructive operations and publication require applicable authority.

## Workflow

### Step 1 — Establish Scope and Baseline

1. Read the relevant requirements, code and instructions. Identify the owned checkout and pre-existing staged, unstaged and untracked work; preserve it.
2. Discover actual test, build, lint, type-check and other required commands. Separate focused cycle checks from increment-level and combined final checks, including CI-only requirements. Establish services, fixtures and permissions before using them.
3. Run the applicable baseline checks. Record pre-existing failures and unavailable checks; assess whether they prevent trustworthy verification. Do not silently repair unrelated failures or treat them as passing. Continue independent work only where its results remain interpretable.
4. Read the supplied breakdown and evidence, if any. Confirm dependency readiness against the caller's actual completion rules rather than trusting a status label. Resolve missing, conflicting or cyclic dependencies before affected work.

### Step 2 — Select the Next Eligible Increment

With an existing breakdown, choose the next authorized item whose prerequisites are satisfied, respecting the supplied order. Do not reslice or reorder approved items merely to match a preferred technique. Internal implementation steps may be smaller; changes to approved outcomes or dependencies need a decision from their owner.

Without a breakdown, identify a small observable outcome and its required checks within the requested scope. Prefer a vertical cut and apply the [Slice Quality Bar](#slice-quality-bar). Read [Slicing Techniques](references/slicing-techniques.md) only when the next cut, ordering or coordination boundary is unclear. Select one relevant technique rather than applying the whole catalog.

Select or confirm the increment's verification method and expected results before editing. Reuse existing approval. If the work needs a broader design or scope decision, present that specific issue and pause dependent work instead of inventing a larger plan.

### Step 3 — Implement and Check Locally

Use the selected method without changing its evidence requirements:

| Method               | Execution                                                                                                                                                                                                             |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Test-first (default) | Write one behavior-focused check, observe its intended assertion failure, add the minimum implementation, then refactor with checks passing. Repeat for the next behavior. Setup/import/service failures are not RED. |
| Test-after           | Establish expected results first, implement in small steps, then add/run the agreed automated checks before calling the increment verified. Do not claim test-first provenance.                                       |
| Manual               | Establish the procedure, expected result and responsible observer in advance. Perform all applicable automated checks as well; leave human-only judgments pending until actually supplied.                            |

Use independent expectations from the accepted behavior. Preserve existing coverage; never weaken checks just to reach green. Characterization or already-supported examples may pass initially: record that honestly rather than breaking working code to manufacture RED.

Keep changes cohesive and limited to the increment, including necessary tests, configuration and documentation. Refactor only within the owned scope while preserving behavior. Record checks, failures and decisions as they occur; do not reconstruct evidence from memory at the end.

### Step 4 — Verify and Review the Increment

- Run the required increment checks, including relevant regressions, build, type-check and lint where applicable. Confirm the intended checks actually executed and record commands/procedures, results and candidate identity.
- Demonstrate the outcome through its actual boundary. Mocks or local checks do not replace required provider, persistence, browser or other real-boundary verification. Keep required CI checks visible when local execution is unavailable.
- Review the diff against acceptance criteria and project conventions. Check error paths, compatibility, unintended exposure and unrelated edits. Apply in-scope corrections and rerun affected checks on the corrected candidate.
- Compare with the baseline. Distinguish new failures, pre-existing failures and checks not run. If required evidence is missing, report the increment as partial or blocked; do not advance dependent work unless the caller's dependency rules explicitly permit it.

When a problem exceeds scope, preserve the candidate and evidence, state what is blocked and request the specific decision needed. Other already-authorized, independent increments may proceed; do not turn the issue into silent new obligations.

### Step 5 — Record Progress and Continue

Update the owning record with the increment's actual result, evidence and remaining gaps. Commit only under the supplied cadence and authority; several verified increments may remain as one uncommitted batch. Push, PR creation, merge and exposure each require their own applicable authority.

Return to Step 2 for the next eligible increment until the requested work is exhausted or no eligible work remains. On resume, reread the record and inspect the actual candidate; revalidate affected evidence after changes or drift instead of replaying already-valid work blindly.

### Step 6 — Verify the Combined Result

Run required final checks against the combined candidate, including interactions between increments and applicable full-suite or CI checks. Increment checks alone do not establish combined correctness. Preserve passing evidence and report failures or unavailable verification truthfully; do not downgrade checks to make the batch appear complete.

Provide the [Implementation Summary](#output) and stop at the requested boundary. Unfinished items, human-only judgments, required CI results and publication remain explicit when outstanding.

## Slice Quality Bar

Use this bar to select new increments or assess supplied work without silently changing approved definitions:

- **Coherent:** one observable outcome across the assigned boundary, including the parts required for that outcome.
- **Verifiable:** expected results can be checked using the selected method; prerequisites exist or are explicitly resolved before execution.
- **Dependency-aware:** builds on verified predecessors and does not require an unfinished successor to demonstrate its own outcome.
- **Safe to integrate:** preserves required behavior and compatibility; incomplete behavior is isolated before exposure where necessary.
- **Small:** limits the amount of unverified change and can be reviewed and checked without a long gap in feedback.

A technical prerequisite can be a valid increment when it has its own verifiable contract; do not rename a layer-only change as a completed user outcome. Local verifiability and production readiness are different claims.

## Implementation Rules

- **Simplicity:** implement current requirements, not speculative flexibility. Introduce abstractions for demonstrated clarity or consistency needs, not an arbitrary number of uses.
- **Cohesion:** include code, tests, configuration and documentation needed for the same outcome together. Defer unrelated cleanup; file type alone does not determine a split.
- **Exposure:** preserve the agreed visibility and defaults. Use an appropriate isolation mechanism when incomplete behavior must remain inaccessible; feature flags are one option, not mandatory for every increment.
- **Recovery:** assess compatibility, data and operational effects before risky changes. Use staged replacement when consumers need coexistence. For irreversible operations, establish an authorized recovery/roll-forward approach; a source revert does not undo data loss.

## Verification

- Each implemented increment matches the authorized outcome, dependency order and selected method.
- Required checks actually ran on the reported candidate; test-first claims have genuine RED/GREEN evidence and refactoring retains passing checks.
- No user work or substantive coverage was discarded to obtain a passing result.
- Increment and combined verification cover required boundaries; gaps and pre-existing failures remain explicit.
- Progress and evidence are retained in the owning record or summary; no duplicate tracking system is required.
- Commits and external actions match actual authority and cadence; local verification is not publication or product acceptance.
