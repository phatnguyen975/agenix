# Worked Examples

Read these fictional examples when adapting exploration, evaluation or the concept format. Supplied observations are scenario inputs, not market research or real execution results. Numerical targets below are proposed pilot decisions, not universal thresholds.

## Example: A Process Idea

**Request:** "Our weekly retrospectives feel stale. Help us explore a better approach."

**Known context:** Eight people attend. The user reports that a few dominate discussion and action items rarely receive follow-up. No evidence yet establishes why quieter people do not participate.

### Explore

**Frame:** "How might we turn team reflection into useful changes while giving people different ways to contribute?"

Clarify the desired improvement, existing follow-up practices and constraints before prescribing another meeting format. Possible directions include:

- **Follow-through first:** retain the meeting, but choose one owned action and review its result. Bet: visible follow-through makes participation worthwhile.
- **Written input first:** collect concerns before discussion. Bet: another contribution channel surfaces important topics currently missed.
- **Experiment review:** use the meeting to review one proposed change and decide whether to keep it. Bet: a learning loop reduces repeated unresolved discussion.

These alternatives address different possible causes. The user says the meeting length must remain unchanged and wants to compare the approaches under that constraint.

### Compare

Follow-through needs little tooling but uses owner time. Written input may broaden contributions but introduces collection/moderation work and privacy questions. Experiment review may improve learning but still needs someone to run and report the experiment.

Recommend a follow-through pilot because it tests the reported action-item problem directly under the time constraint. Keep participation barriers open rather than claiming that follow-up will solve them. After reviewing this comparison, the user chooses that direction. This is a choice of pilot, not proof that the diagnosis is correct.

### Concept Output

```markdown
# Retrospective Follow-Through Pilot

## Problem and Desired Outcome

The team reports unresolved action items and uneven participation. The immediate goal is to learn whether explicit follow-through produces useful changes without lengthening the meeting.

## Direction and Rationale

The user selected a follow-through pilot. Retain the current meeting, agree one bounded action and review its outcome next time. Written input and experiment-review formats remain alternatives if follow-through alone does not help.

## Assumptions and Validation

| Priority       | Assumption                                                  | Evidence / Uncertainty                           | Proposed Check and Decision Signal                                                                                                            |
| -------------- | ----------------------------------------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Must Be True   | An owner can complete a small action within normal capacity | Capacity has not been checked                    | Agree a bounded action with its owner; if it requires unavailable capacity, revise scope before starting                                      |
| Should Be True | Visible follow-through makes the meeting more useful        | Plausible interpretation of the reported problem | For two meetings, review action outcomes and ask participants for concrete benefits; revise if work completes but usefulness does not improve |
| Might Be True  | A shared board would improve visibility                     | No tool gap established                          | Defer; investigate only if the existing notes prove hard to find                                                                              |

## Minimal Scope and Next Experiment

Propose a two-meeting pilot using existing notes and unchanged meeting length. Account for action-owner effort and obtain agreement before running it. No pilot results exist yet.

## Not Doing

- New tools — no evidenced tooling gap.
- Mandatory anonymous submissions — participation causes and privacy needs remain unexamined.

## Open Questions and Next Action

Who can own a suitably small action? Next, agree capacity and the pilot's useful-outcome signal with the team. Investigate participation separately if it remains a problem.
```

If the user requests saving and accepts the default, save to `docs/ideas/retrospective-follow-through-pilot.md`. If only brainstorming was requested, present the concept and proposed path. An existing caller-owned output receives the contribution instead of a duplicate document.

## Example: An Existing Project Boundary

A caller supplies an approved document-editor audience and asks only for alternatives to handle overlapping edits. Reuse that audience. Inspect the relevant editor/contract sections when available; if not, label technical feasibility provisional.

Compare locking, explicit conflict detection and isolated draft/merge approaches by user interruption, integrity requirements and actual implementation support. Do not assert that adding a field or transport layer alone makes locking safe. If the caller requests only alternatives, return that comparison and its unresolved assumptions without choosing a direction, saving another concept file or implementing it.
