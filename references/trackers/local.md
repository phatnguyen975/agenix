# Local Tracker

Use this guide when `tracker: local`. The selected project uses Git for work-item records and GitHub for pull requests and required checks.

## Locate the Record

| Information                                   | Location                                                                                                                  |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Feature state and delivery set                | Feature README in Git.                                                                                                    |
| Ticket and its tasks                          | `docs/features/<feature-id>/tickets/<ticket-id>.md`. Tasks are embedded in their ticket.                                  |
| Approved task plan, build evidence and review | The owned ticket file on the implementation branch. Reference durable evidence from the implementation PR once it exists. |
| Integrated status                             | The refreshed default branch with supporting merge and verification evidence.                                             |

Use one editor per ticket and coordinate catalog allocation, shared plan edits and feature finalization. Other contributors use separate tickets and worktrees. Indexes point to the records. Write routine progress to its ticket instead of a shared index.

## Read, Verify and Update

| Tool               | Use                                                                                                                                                                                                                                                        |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Git                | Inspect owned edits, the active branch, committed records and the refreshed merged baseline. Publish approved local record changes with their owning work.                                                                                                 |
| `gh`               | Read the configured PR, reviewed head, merge SHA and required check results. Git status alone cannot establish these outcomes.                                                                                                                             |
| `verify-status.py` | Read the selected feature/ticket/task records, Git evidence and required read-only PR/CI facts. Its result distinguishes declared state, readiness, verified completion and concrete blockers. It neither fetches nor runs product checks or writes state. |

1. Refresh the baseline and resolve the selected item and its parents. Use the owned branch for active ticket tasks and verified merged evidence for cross-ticket and feature readiness.
2. Use the verifier at the applicable stage after refreshing Git and collecting the product results available at that stage. Report a declared `DONE` separately from verified completion. Missing, stale or inaccessible evidence blocks the action that requires it.
3. Keep the approved local task plan in the ticket file and publish updates on the owned branch. At ticket ship, the candidate may carry prospective `DONE` and task completion metadata bound to pending final-head checks. After merge, confirm the approved record reached the default branch and verify closure from actual PR and check results.

If another contributor updated the same record, pause publication and agree who reconciles it. Preserve both valid contributions, approved definitions, stable IDs and evidence. Recheck dependencies, coverage and affected checks. Obtain fresh approval for material changes before publishing.
