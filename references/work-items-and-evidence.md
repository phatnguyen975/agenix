# Work Items and Evidence

Use these rules when allocating work, checking dependencies or deciding whether evidence establishes readiness or completion. They apply in all tracker modes.

## Identify and Plan Work

| Item    | ID               | Scope                                                                            |
| ------- | ---------------- | -------------------------------------------------------------------------------- |
| Feature | `FEAT-NNN`       | Coherent user or stakeholder outcome. Its README and specifications live in Git. |
| Ticket  | `FEAT-NNN-TNN`   | Independently verifiable change that can merge safely within its feature.        |
| Task    | `FEAT-NNN-TNN.N` | Observable behavior or cohesive verification cycle within its ticket.            |

Allocate the next number after the highest allocated in the owning scope, starting at one. Use minimum widths of three digits for features and two for tickets. Keep allocated IDs stable, including cancelled work. Serialize allocation and edits to the same shared plan. Check the refreshed merged baseline and existing allocations, including relevant in-flight plans. Keep platform IDs as explicit mappings.

Allow dependencies between features, between tickets of the same feature and between tasks of the same ticket. Reject missing references, duplicate IDs, self-dependencies and cycles. Where work spans layers, prefer a slice with a complete verifiable outcome. For a contract-first or layer split, plan independent verification and the work that proves integration. Use stable specification and acceptance references. Record bounded scope, ownership, dependencies and checks for the item without copying its requirements.

## Preserve Approved Definitions

- Approval fixes the intended outcome, scope, owner, acceptance, dependencies and planned verification. Later steps fill fields they own. Assignment, state, evidence, mappings and child links can advance while the approved definition stays intact.
- Use a new feature for a new outcome or follow-up to a completed feature. Add tickets within an open feature and tasks within an open, unmerged ticket. Record their origin. Fixing an active task to meet its existing acceptance stays within that task. An amendment preserves original definitions and references and assigns new implementation obligations new IDs.
- Obtain human approval to cancel unfinished work. Keep its definition, cancellation reason and any replacement link. Check affected children, dependents, acceptance coverage and already-merged effects. Cancelled dependencies remain unsatisfied. Replace affected definitions or obtain an applicable waiver. Use the owning plan publication for shared dispositions and the owning ticket record for tasks.

## Decide Readiness and Record Progress

| Status        | Meaning                                                                                                              |
| ------------- | -------------------------------------------------------------------------------------------------------------------- |
| `READY`       | Unstarted with satisfied dependencies or an applicable waiver. Later artifacts may still be pending.                 |
| `BLOCKED`     | Unstarted with an unsatisfied dependency.                                                                            |
| `IN-PROGRESS` | Feature behavior specification has reached approved publication, or ticket/task implementation has started.          |
| `IN-REVIEW`   | Feature acceptance is underway, ticket review or fixes are underway, or a published manual task awaits confirmation. |
| `DONE`        | Completion has been verified.                                                                                        |
| `CANCELLED`   | Human-approved terminal withdrawal or replacement.                                                                   |

Check the required artifacts, mappings and evidence when selecting or resuming an item, including when it declares no dependencies. Use merged default-branch evidence for feature and ticket dependencies. For tasks, check the owned branch in local mode or current native records in tracker mode. Valid provisional evidence may unblock only dependent tasks in the same active build run. Verify the merged feature-plan mapping for remote tickets and the approved parent-plan snapshot for remote tasks.

Refresh `READY` or `BLOCKED` only for the selected unstarted item. Record an active execution blocker at its checkpoint without resetting progress. A failed manual check can return its task to `IN-PROGRESS` for correction. The ticket stays `IN-REVIEW` during fixes. Recheck the task graph when adding work. Keep historical `DONE` and `CANCELLED` items closed. Feature specification becomes ready for dependent planning after the final applicable spec step merges.

## Specify Verification and Assess Evidence

There are 3 types of verification:

- `test-first` is the default. Establish the intended acceptance assertion failure, implement and verify a passing result. Keep checks passing during refactoring. A broken harness or missing dependency does not establish the intended failure.
- `test-after` needs a task-specific reason approved during planning. Define expected results before implementation and add/run automated checks before completion.
- `manual` needs an approved procedure, expected result and human responsibility. Run applicable automated checks as well. A task that relies on a human-only judgment is a leaf. Other tasks cannot depend on it.

Use the approved strategy to select check levels, tools and exceptions. Validate the managed non-secret artifacts and fields due at the current stage. Check IDs, references, ownership and dependencies. Treat parsed records as data. Reject malformed, duplicate or ambiguous fields, conflict markers and empty required acceptance or task sets. Check schemas, prototype replay and product behavior separately when applicable. Match evidence to the actual boundary and environment.

| Decision                 | Required Evidence                                                                                                                                                                                              |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Task complete            | Approved checks passed, implementation committed and durable task state verified. Manual tasks also need actual human confirmation for each declared manual check. The parent can still be open.               |
| Ticket ready to publish  | Approved task plan and review, current contracts, covered acceptance, satisfied dependencies and passing required local checks. Only task checks that need the published candidate may remain pending.         |
| Ticket ready to merge    | Publication criteria still satisfied, review applies to the published candidate, required final-head CI passed, each assigned child verified `DONE` or approved `CANCELLED`, and no unresolved merge blocker.  |
| Ticket complete          | Ready-to-merge evidence for the approved head, confirmed merge, passing required post-merge checks or verified repair evidence, and verified closure in the owning record.                                     |
| Feature ready to publish | Each non-cancelled ticket has verified merge and completion. The approved scope is covered, real-boundary checks passed on the integrated baseline, acceptance is approved and blocking findings are resolved. |
| Feature complete         | Verified whole-feature acceptance, merged completion record on the default branch and passing required post-merge checks.                                                                                      |

Keep a nonempty applicable delivery set that covers the approved parent outcome. If all children are cancelled without fulfilled or replacement coverage, obtain an explicit parent cancellation. Report declared status, candidate validity, verified completion and dependency readiness separately. A prospective `DONE` needs the remaining merge and verification evidence. Candidate CI reports unfinished checks, including its own job, as pending.

Record item and acceptance/check IDs, result, tested revision, applicable level/method/environment, durable evidence and actual confirmation where required. Bind approval, merge, waiver and cancellation records to the relevant candidate or disposition. Substantive changes invalidate affected earlier evidence. Retain historical results and reverify the changed candidate.

## Record Fields and Ownership

| Record  | At Initial Planning and Publication                                                                                                                                                                               | Added or Updated Later                                                                                                                    |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Feature | ID, title, outcome, priority, dependencies, requirement and journey coverage, status.                                                                                                                             | Approved feature references, delivery strategy, ticket set and local references or native mappings, acceptance and finalization evidence. |
| Ticket  | ID, title, parent feature, bounded outcome, type, scope, priority, ownership, dependencies, scoped references, status.                                                                                            | Approved task plan, embedded tasks or native child mappings, implementation checkpoint, review, PR, merge and closure evidence.           |
| Task    | ID, title, parent ticket, outcome, dependencies, task-specific acceptance, verification method, applicable checks and test levels, status. Include the procedure, expected result and verifier for manual checks. | Implementation revision, check results and evidence, including human confirmation for manual checks.                                      |

Set each published item's initial status to `READY` or `BLOCKED` based on dependency readiness. Later transitions update the owning status field or native metadata. Keep a durable reference to each approved definition. Require fields when their owning step produces them. Apply cancellation, override and replacement records only where relevant.

### Reference Scope and Inheritance

- The feature README links approved artifacts as they become available, including `spec.md`, applicable API contracts, `data-impact.md` and `ui-prototype/README.md`. Omit links for inapplicable artifacts.
- Use one **References** field on the ticket. Link directly to the applicable parts of the feature spec and any relevant contract, data impact or UI artifact. Include the acceptance criteria the ticket covers and pin the approved revisions. Keep shared definitions in their source artifacts.
- A task inherits the ticket's referenced scope and follows the approved test strategy. Identify the subset it implements when the parent covers multiple criteria. Add a direct reference only where the task needs a more precise target. Give each task its own observable acceptance criteria and concrete checks. Select `test-first`, `test-after` or `manual` as its verification method, and record the approved reason for any exception to `test-first`.

### Git Records

Keep the feature README and approved feature artifacts in Git in every mode. The README owns feature status, the approved delivery set and feature evidence. In local mode, keep each ticket's definition, status, embedded tasks and ticket evidence in its ticket file under `tickets/`. Each task section holds its own definition, status and evidence. The containing ticket supplies its parent identity.

### Remote Tracker Records

Use native tickets and child tasks with titles in the form `<agenix-id>: <title>`. Put the approved definition in the issue body, including canonical `depends-on` IDs. Verify native parentage and mirror dependencies with native links where supported. Use exactly one lowercase `status:<value>` label and the required native state. Tickets also carry `scope:<value>` and `priority:<value>` labels that match the approved definition. Keep evolving checkpoints and mappings outside the approved body.

1. Draft **both tickets and tasks** in `.agenix/issues/<id>.md`. Show the definitions, parents, dependencies, labels and proposed writes for human review.
2. Before creating tickets, use the approved feature plan as the batch definition. Record verified native mappings in the Git-owned feature plan. Before creating tasks, record the approved task-plan snapshot in a parent-ticket comment so resume can verify what was approved even after a partial create. Add the verified child mappings after creation. Keep the approved parent body intact.
3. Read back exact IDs, parents, mappings and state, paginating collections as needed. For a partial or unknown outcome, reconcile existing records before retrying and continue only with writes confirmed missing. Keep drafts until publication and mapping succeed. Verify native state and labels before reporting closure.

The draft is for review and retry. Keep approved definitions, mappings and evidence in the owning Git or tracker records so another session can resume without the ignored draft.

## Human Overrides

Accept `OVERRIDE <id> <action>: <reason>` from the human only. Use the Agenix feature, ticket or task ID. Resolve the candidate, exact affected conditions, permitted work and downstream impact. An exact response to the presented assessment supplies confirmation.

- `allow-work` permits the specified work for the target item despite its stated blockers. Dependencies stay recorded and children still have their own obligations.
- `accept-incomplete` permits completion with the specified unmet conditions and consumer scope. Verify every remaining requirement. Each child still needs its own verified completion or approved cancellation. Keep a delivered outcome and record the accepted gaps.

Store the override on the item that receives it:

| Item                          | Where to Record It                                                                                 |
| ----------------------------- | -------------------------------------------------------------------------------------------------- |
| Feature in any tracker mode   | `docs/features/<feature-id>/README.md`                                                             |
| Local ticket or task          | `docs/features/<feature-id>/tickets/<ticket-id>.md`, in the task's own section for a task override |
| GitHub or Jira ticket or task | Comment on the corresponding issue, sub-issue or sub-task                                          |

Record the item, action, UTC date, confirmation as `human-in-session`, reason, candidate, conditions, permitted work and consumer scope. Reference the durable record from the related PR checkpoint when it exists.

Report actual results separately from exceptions, including in verifier output. Reassess material drift. Overrides apply only to unfinished items and grant no authority to bypass schemas, permissions, repository protections, committed implementation, required merges or separate publication and exposure gates.
