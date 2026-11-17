# Code Simplification Report Template

Use when a full report is requested, adapting to a caller-owned format when supplied. Replace instructional placeholders with actual findings. Keep the report proportional to the work: do not invent activity, approval, metrics or evidence to fill sections. Counts and line deltas are optional measured context, not quality scores.

`COMPLETED` means the bounded pass finished with its required checks, including a justified no-change result. `BLOCKED` means prerequisites or authority prevented completion. `PARTIAL` means some verified changes remain while other requested work is blocked or deferred. Always identify retained changes and unresolved state accurately.

Use `PASS`, `FAIL`, `NOT RUN` and `NOT APPLICABLE` for checks. Missing prerequisites are not executed failures; passing commands alone do not establish relevant coverage or universal equivalence.

```markdown
# Code Simplification: <Scope Name>

> **Outcome:** <COMPLETED, BLOCKED or PARTIAL>
> **Date:** <YYYY-MM-DD; include time/time zone when relevant>
> **Candidate:** <source revision or identifiable workspace state; branch when applicable>

## Summary

<Briefly state the requested improvement, what was achieved and the overall
verification outcome. For blocked/partial work, name the main obstacle and
what remains unchanged or unresolved. For a no-change result, explain why
no worthwhile simplification was warranted. Leave detailed evidence below.>

## Scope

<Identify the request or existing approval defining this scope when needed
for traceability. Do not invent a separate approval event.>

- **Included:** <files/functions and the authorized concern>
- **Boundaries:** <relevant exclusions and pre-existing work preserved>

## Changes

### <File / Function>

<Include short before/after snippets when they make the transformation
clearer; otherwise give a precise explanation or a stable diff reference.
Use the actual language label for snippets. Repeat for distinct retained
changes, without dumping whole files. If no changes were applied, replace
this subsection with a brief statement; do not populate a dummy change.
Mention reverted attempts only when needed to explain the final state.>

- **Improvement:** <the concrete clarity problem, transformation and why it helps>
- **Preserved Behavior:** <relevant results, interfaces, errors, evaluation order and effects>

## Verification

<Use separate rows for distinct commands or inspections. Combine incremental
and final rows if they refer to the same check on the same unchanged
candidate. Include commands actually used and meaningful outcomes, such as
test counts or failure details. Explain missing coverage and required unrun
checks explicitly. Omit irrelevant checks rather than padding the table.
Semantic review complements tests; neither alone proves equivalence.>

| Stage / Candidate | Command or Inspection                     | Result          | Evidence and Limits                                                   |
| ----------------- | ----------------------------------------- | --------------- | --------------------------------------------------------------------- |
| Baseline          | <covering tests>                          | <actual status> | <actual outcome and affected behavior covered>                        |
| <Transformation>  | <relevant incremental checks>             | <actual status> | <checked state and findings>                                          |
| Final             | <applicable tests/build/lint/type checks> | <actual status> | <final outcome and gaps>                                              |
| Final             | <semantic and scope review>               | <actual status> | <behavior risks checked, authorized diff and preserved existing work> |

## Remaining Items

<Include blockers, out-of-scope findings and unresolved recovery state
when present. Do not repeat verification evidence or the applied changes.
Omit this section when there are no remaining items in the bounded review.>

- **<Issue / Deferred Work>:** <specific gap, impact and next action or decision>
```
