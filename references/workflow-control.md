# Workflow Control

Use this guide to handle one human-selected workflow step, from invocation through approval and closure.

## Select and Prepare a Step

A workflow invocation has the form `agx-<phase> [<item-id>] <step>`. Treat it as skill input. Validate the phase, step and item type before acting. Spec and plan take a feature ID, build and review take a ticket ID, and ship accepts either. If input is invalid, give the accepted form and leave state untouched. The usage guide is read-only and leaves the active step unchanged.

1. Confirm the project, worktree, approved scope and ownership. Use one coordinating session per worktree. Delegates stay within its step and permissions. Separate concurrent ticket worktrees and agree ownership before parallel writes.
2. Determine which steps and outputs apply to the approved scope. Check the selected step's prerequisites and existing approvals, artifacts, PRs and tracker mappings. Resume matching work and reconcile partial writes. Pause only the action that depends on a missing prerequisite or ambiguous state.
3. Run the selected procedure only. The final applicable step also checks the complete applicable phase output. When the procedure requires a phase PR merge or verified delivery, include that outcome before reporting completion.

## Artifact Gates

1. Complete the analysis, changes, self-review and applicable checks. Resolve routine choices within scope. Ask the human for material decisions, conflicting requirements, missing authority and judgments that require human confirmation.
2. Present the exact candidate and base, what changed, decisions and acceptance coverage, actual results, outstanding checks and the intended writes. Acceptance requires passing checks or an applicable recorded exception. A review with findings, a repair plan or an incomplete handoff can record failures as blockers.
3. Wait for a decision on that candidate and the stated actions. Address requested changes and rerun affected checks. Record the actual human decision. If the material content changes, obtain approval of the new candidate before publishing it.
4. Carry out approved actions in the same step and report the resulting revisions, links, checks and blockers. A read-only verification step records its outcome without an artifact gate. Merge and exposure use their own authority.

## Session Markers and Handoff

| Marker                               | Author | When to Use It                                                                                           |
| ------------------------------------ | ------ | -------------------------------------------------------------------------------------------------------- |
| `BEGIN AGX-<NAME> [item-id] <step>`  | AI     | First line of the first response to a valid new step.                                                    |
| `DURING AGX-<NAME> [item-id] <step>` | AI     | First line of subsequent work or feedback in an open step, including an open step restored from handoff. |
| `END AGX-<NAME> [item-id] <step>`    | Human  | Closes the matching step after actions already authorized or explicitly authorized in the same message.  |

### Close the Current Step

A session has at most one open step. Use `DURING` until the human sends the matching `END`, including after successful work or a human merge. Markers carry no work-item status or publication, merge or exposure authority.

When the human sends the matching `END`:

1. Finish only actions already authorized or explicitly authorized in the same message.
2. Summarize the step's outputs, verification evidence and actual outcome. If work remains incomplete, state the blockers and outstanding actions.
3. Give the next eligible invocation the human can use. If none is eligible, state what must be resolved first. Wait for the human to invoke a step explicitly. Never invoke or start it yourself.

### Continue from a Handoff

Keep marker state in the current session. To transfer work, record the phase, item, step, open or ended state, worktree and branch, durable evidence, unresolved decisions and next action in `.agenix/HANDOFF.md`. When the human chooses to continue an open step from a handoff, verify the actual approvals, writes and completion records, then use `DURING`. Use `BEGIN` for a new invocation, including an explicit restart of an ended step.

## Amend an Approved Baseline

When an approved requirement or contract needs to change, handle the amendment before continuing work that relies on it.

1. **Assess impact.** Identify the step that owns the baseline and the affected requirements, plans, checks and consumers. Pause dependent work and identify the decisions the human needs to make.
2. **Return to the owning step.** If it is already open, prepare the amendment there. Otherwise, record where the current step stopped. Wait for the human to close it and explicitly invoke the owning step.
3. **Verify, approve and publish.** Verify the scoped amendment and obtain human approval. Publish shared changes through the owning phase PR or a new scoped PR if the original has merged. Review may record approval for a ticket-local amendment published on its implementation branch. Merge shared changes before other affected tickets resume.
4. **Reassess dependent work.** Preserve prior decisions and evidence. Recheck affected dependencies and coverage, and revalidate affected approvals and checks. Keep existing approved work-item definitions intact. Plan new obligations as new work with their own approval.
