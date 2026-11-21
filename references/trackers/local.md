# Local Tracker

Use this guide when `tracker: local`. The selected project uses Git for work-item records and GitHub for pull requests and required checks.

## Locate the Record

| Information                                   | Location                                                                                                                  |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Feature state and delivery set                | `docs/features/<feature-id>/feature.agenix.json`.                                                                         |
| Ticket and its tasks                          | `docs/features/<feature-id>/tickets/<ticket-id>.agenix.json` with a `tasks` array.                                        |
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

When a selected, unstarted item is `BLOCKED`, run the verifier before work begins. A result with `dependency-ready: true` permits the owning workflow to consider `READY` after checking the step's other prerequisites. The verifier leaves the record untouched. An active item keeps its lifecycle status if a new blocker appears.

## Helper Inputs

- Run `verify-status.py --project-root <absolute-root> --item <id>` after refreshing `origin`. Select `active-build` for same-worktree task evidence, `candidate-ci` for prospective state or `delivery` for merged evidence. Pass the checked `--revision` or the staged task `--tree` when evaluating a candidate.
- Pass the required GitHub check names from the approved policy using `--head-check` and `--post-merge-check`. Use `--ci-policy` with per-item `head` and `merge` name arrays when the requirements differ. Explicitly select the applicable empty set when the approved policy has no checks for that stage. Supply `--pr-number` when inspecting an open candidate's PR. Pass exact `--approved-blob` entries only for bookkeeping explicitly covered by approval.
- Read the JSON result before proceeding. Exit 2 means invalid input or contradictory evidence. Exit 3 means a required input or observation is unavailable. A successful structural check, pending candidate-CI result or provisional local result is usable only within its reported scope.
- If check results attach to an open PR's test merge, pass the exact `--test-merge-revision`. The helper checks the live PR mapping and both commit parents before reading results for that revision.
- For a post-merge repair, the helper reads the original failed checks from GitHub and discovers repair tickets from the integrated feature plan. The repair's `origin-ref` must identify the original ticket path or PR URL; its merge must follow the original and the failed checks must pass on the repaired revision. Preserve both results and PR mappings in durable PR evidence.
