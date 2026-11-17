---
name: code-simplification
description: Simplify tested code within an authorized scope while preserving observable behavior. Use for concrete readability, duplication or control-flow improvements, including a focused refactor during implementation. Keep bug fixes, feature changes, performance tuning and architectural rewrites separate; do not edit uncovered code on inspection alone.
metadata:
  author: phatnguyen975
  version: "1.0"
---

# Code Simplification

## Purpose and Scope

Improve how easily a maintainer can understand and change working code, without altering its observable contract. Fewer lines, fewer helpers or a more fashionable idiom are not sufficient reasons to edit. A clear no-change result is appropriate when no worthwhile simplification exists.

Work only on the supplied files/functions and their authorized owned changes. A standalone simplification request and a focused refactor inside an approved implementation scope use the same behavior-preservation rules. Keep the refactor distinguishable from feature/fix work while following the caller's agreed batch and publication cadence. Read-only review produces findings, not edits.

## Inputs and Prerequisites

- **Scope:** the exact files/functions, intended readability concern and permitted write ownership. Read callers/dependencies as necessary; discovering them does not expand edit authority.
- **Safety net:** the existing test command(s) exercising the affected behavior, execution prerequisites and any required build/lint/type checks. Discover documented commands when not supplied; do not invent commands or install tools implicitly.
- **Project context:** applicable instructions, naming/style conventions, interfaces, relevant history, performance/resource constraints and caller-supplied output/verification expectations.

For edits, relevant existing tests must cover the affected behavior and pass before simplification. A green unrelated suite, a coverage percentage or a compiler alone is not sufficient. Inspect assertions and error/boundary coverage, not just filenames. If coverage is absent, relevant tests fail or prerequisites are unavailable, stop dependent edits and report the gap. Establishing characterization coverage or fixing failures requires separately authorized work; do not silently add or weaken tests to unblock this pass.

## Core Principles

1. **Understand before changing.** Establish the responsibility, callers, inputs, outputs, side effects, edge cases and reason for non-obvious code. Consult history when needed; unfamiliar code is not automatically unnecessary.
2. **Preserve observable behavior.** Keep results, public interfaces, error types and contractual messages, side effects and their order, observable evaluation counts, state/identity semantics, resource lifetime and relevant timing/concurrency properties. Respect existing performance budgets where applicable. Tests provide evidence, not a substitute for reasoning about the diff.
3. **Clarity over cleverness.** Preserve useful names, domain boundaries, explicit error handling and documented extension points. Do not collapse independent concerns or extract helpers that merely move complexity elsewhere.
4. **Convention with correctness.** Follow applicable project style and local language idioms; style preferences do not authorize changing semantics. KISS, DRY and YAGNI are heuristics, not instructions to remove meaningful duplication or required abstractions.
5. **Small, reversible increments.** One coherent transformation at a time, followed by relevant checks before another. A transformation may need several coordinated edits, such as an internal rename across owned call sites; do not leave an inconsistent intermediate result.
6. **Bounded authority and preservation.** Reuse existing approval that covers the scope and transformation. Preserve pre-existing staged/unstaged and unrelated content. Ask only for a material change, unclear ownership or another consequential decision outside current authority.

## Complexity Signals

Signals prompt investigation; they do not prove a defect or mandate a particular rewrite. Assess whether the proposed change makes this code easier to reason about while preserving its contract. Numeric size/nesting counts are review aids, not universal thresholds.

### Structure and Control Flow

| Signal                                          | Possible Improvement                               | Check Before Applying                                                                    |
| ----------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Deep nesting or repeated conditional structure  | Guard clauses, named predicates or focused helpers | Preserve condition order, short-circuiting, exceptions and cleanup paths                 |
| A long function with separable responsibilities | Extract a meaningful operation                     | A cohesive sequence may be clearer together; preserve shared state and evaluation order  |
| Nested ternaries or dense expressions           | Explicit branches or a named intermediate value    | Preserve laziness, coercion, defaults and branch-specific effects                        |
| Unclear boolean flags or positional arguments   | Clarify internal calls or group related inputs     | Do not break public signatures, external callers or language-specific argument semantics |
| Repeated calculations or checks                 | Name or consolidate a genuinely shared operation   | Repeated evaluation may be deliberate or time/state dependent                            |

### Names and Explanations

| Signal                                 | Possible Improvement            | Check Before Applying                                                             |
| -------------------------------------- | ------------------------------- | --------------------------------------------------------------------------------- |
| Generic or misleading names            | Use a domain-appropriate name   | Short names may be clear locally; public/exported names are contracts             |
| Obscure abbreviations                  | Follow project vocabulary       | Established abbreviations need no cosmetic expansion                              |
| Comments repeating obvious operations  | Remove redundant narration      | Retain rationale, warnings, legal notices and externally meaningful annotations   |
| A helper whose name hides side effects | Make the responsibility evident | Renaming must cover owned uses; do not silently widen scope to external consumers |

### Redundancy and Abstractions

| Signal                                                 | Possible Improvement                     | Check Before Applying                                                                            |
| ------------------------------------------------------ | ---------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Duplicated logic with the same responsibility          | Share a small, well-named operation      | Similar text can represent independently evolving rules; avoid premature coupling                |
| Apparently unused code/imports or commented-out blocks | Remove confirmed dead/redundant material | Check dynamic loading, reflection, generated registrations, side effects and compatibility paths |
| A wrapper or layered factory with no current role      | Inline or remove unnecessary indirection | Preserve instrumentation, lifecycle, extension/injection seams and public compatibility          |
| An apparently redundant type assertion                 | Rely on equivalent inference             | Preserve type guarantees, overload selection and runtime conversions; run applicable type checks |

For a repetitive mechanical change, consider an existing suitable transformation tool only within authority and after understanding its effect. Inspect its diff and verify behavior. A large diff calls for reassessment/splitting, not automatic tool installation, broad regex replacement or permission expansion.

## Workflow

1. **Inspect and bound.** Identify checkout/ownership, requested concern, applicable conventions and existing changes. Confirm analysis versus edits; record the starting diff/state needed to preserve and undo only this pass's changes.
2. **Understand and establish the baseline.** Read the affected code, callers and relevant tests. Establish what behavior must remain unchanged, then run the covering test commands. Record applicable baseline build/lint/type results. Stop edits on a missing/failing safety net; independent read-only findings can still be useful.
3. **Choose the smallest worthwhile change.** Explain the signal, intended improvement, semantic risks and affected consumers. If the existing request/plan covers it, proceed without another gate. Otherwise resolve the specific scope/decision first. A behavior defect is a separate finding, not permission to fix it here.
4. **Apply and verify incrementally.** Apply one coherent simplification and run relevant existing tests and applicable build/lint/type checks. Keep their assertions/expected behavior unchanged. Inspect the actual diff for semantic traps; passing tests alone cannot justify an observable change.
5. **Handle failure safely.** Stop the sequence if a check fails or the result is harder to understand. Inspect the cause and undo only this pass's change using the recorded starting state or a precise inverse patch. Do not reset/restore whole files over mixed user changes. Re-run relevant checks after undo; if preservation/restoration is uncertain, stop writes and report the exact state rather than claiming recovery.
6. **Review the final candidate.** Read the combined diff and rerun relevant final checks when later edits invalidate earlier evidence. Confirm scope, unchanged behavior and net clarity. Follow the caller's commit/publication cadence; this skill does not imply either action.
7. **Report and stop.** Give concise evidence in the caller's chosen channel/artifact. Record what changed, why it helps, baseline/final outcomes, unchanged behavior boundaries, preserved unrelated work and any blocked/deferred items. Do not produce a report file merely because a simplification occurred.

## Output

Default to the scoped code change and a concise completion summary. For analysis-only work, return findings and prerequisites without editing. State no change when no worthwhile simplification was found; do not invent work to fill a format.

When a full report is requested, read [Report Template](assets/report-template.md) and use it unless the caller supplied another format. Use the specified path and existing write authority. If a report location is genuinely unspecified, propose `docs/code-simplification-<scope-slug>-<YYYYMMDD>.md` and resolve the destination before saving; do not repeatedly confirm a selected authorized path. Preserve an existing artifact unless its revision/replacement is authorized, and read back the saved report.

## Verification

- Relevant baseline tests cover the changed behavior and passed; final applicable tests pass with existing expectations intact.
- Applicable build, lint and type checks introduce no regression; missing or unrun required checks remain explicit, not a pass.
- Results, interfaces, errors, side effects/order, boundary behavior and relevant performance/resource semantics are preserved.
- The diff stays within authorized ownership/scope, preserves unrelated changes and follows the agreed plan/cadence.
- Each coherent transformation received relevant verification before the next; any failed attempt was safely removed or is explicitly unresolved.
- No new dead paths, accidental dependencies, weakened error handling or inconsistent renames were introduced by this pass.
- The final diff improves comprehension for a maintainer without relying on line counts or personal naming preferences as proof.

Stop dependent edits when a required condition is unmet. Report what evidence supports the result and what remains unknown; do not assign a numerical confidence or preservation score without an agreed measurement rubric.
