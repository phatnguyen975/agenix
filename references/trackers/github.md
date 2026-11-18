# GitHub Issues Tracker

Use this guide when `tracker: github`. A ticket is a GitHub issue and each task is a native sub-issue. The feature stays in Git.

## Verify Setup

Use an authenticated `gh` session and explicitly select the configured repository. Confirm issue, label and sub-issue permissions. Verify that the installed `gh issue create --help` lists `--parent`. Check current platform limits before publishing a batch. If the batch exceeds a limit, present a revised plan before creating items. Create missing lifecycle or ticket labels during approved setup. Change existing label definitions only within the approved setup scope.

## Create and Read Issues

1. Resolve the approved Agenix ID, feature mapping and, for a task, the verified parent issue number. Inspect existing issues and native parentage before creating anything. Preserve the approved parent body and put the task-plan snapshot and mappings in comments.
2. Use `gh issue create` against the configured repository with the approved title, draft body and labels. For a task, pass `--parent <issue-number>`. Keep the issue number, REST numeric ID and GraphQL node ID distinct. Record the returned issue URL and verify its parent.
3. Use `gh issue view` to check a known issue's state, `stateReason`, labels and body. Use `gh api --paginate` with the repository-specific issue/sub-issue endpoints to enumerate the entire collection. Resolve ambiguous creates by exact ID and parent before retrying. A search miss alone is insufficient when an earlier write may have succeeded.

## Confirm State and Closure

| Agenix State                                   | GitHub State                                                                                 |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `READY`, `BLOCKED`, `IN-PROGRESS`, `IN-REVIEW` | `OPEN` with the corresponding single lifecycle label.                                        |
| `DONE`                                         | `CLOSED` with completed reason and `status:done`.                                            |
| `CANCELLED`                                    | `CLOSED` with not-planned reason and `status:cancelled`, with approved disposition evidence. |

Use `gh issue edit` to update labels or allowed metadata. Use `gh issue close --reason completed` for verified completion or `gh issue close --reason "not planned"` for approved cancellation. Read back both label and native closure reason. If only one write succeeded, report incomplete publication and reconcile the existing issue before issuing another write.

A verified task can close while its parent is still open. Close a ticket as completed after verified delivery. Use non-closing PR references such as `Refs #42` to preserve that sequence.
