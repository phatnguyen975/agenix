# Branching and Pull Requests

## 1. Branch Naming

Default to `<type>/<kebab-description>` or `<type>/<ticket-id>-<kebab-description>` using the project's commit types. Prefer a descriptive short name; retain the tracker ID's spelling. Release-metadata branches default to `chore/release-<version>`; optional maintenance lines use `release/<MAJOR>.<MINOR>` as described in [Release](release.md).

Validate with `git check-ref-format --branch "<name>"`; this verifies Git syntax, not the project's naming policy. Lowercase descriptions are a style default, not a Git restriction. Never reuse an existing ref or checkout path without inspecting ownership and intent.

## 2. Sync Rules

Resolve the actual remote/trunk and refresh them when the action permits network/ref writes. On an owned branch:

| Branch-only Commits                                                  | Method                                                          |
| -------------------------------------------------------------------- | --------------------------------------------------------------- |
| Agent-authored and confirmed never published, with rewrite authority | `git rebase origin/<trunk>` after preserving the starting state |
| Published, other-authored or uncertain                               | `git merge --no-edit origin/<trunk>`; no history rewrite        |

A missing upstream does not prove unpublished history. Preserve unrelated index/worktree changes before sync; if they prevent a safe operation, isolate or resolve ownership rather than automatically stashing them. Compare the actual base/candidate and incoming changes. Conflicts or integration changes need their relevant verification; material candidate drift may invalidate prior approval.

A local trunk can be fast-forwarded to its verified remote with `git merge --ff-only origin/<trunk>` in a clean, authorized checkout. This is not a remote PR merge or authority to push trunk. Do not switch another worker's checkout to do it.

## 3. Branch Lifecycle

Stages describe eligibility, not automatic execution. Resume an explicitly owned existing branch when appropriate rather than recreating it from trunk.

| Stage             | Preconditions and Action                                                                                                                                                                   | Observable Result                                                                       |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| Create / Resume   | Inspect ownership, base, operation state and working changes. For a new branch use `git switch --no-track -c <name> origin/<trunk>` or the worktree equivalent after an authorized refresh | Intended branch/worktree at the verified base; existing changes preserved               |
| Develop           | Execute verified local increments using the caller's commit cadence                                                                                                                        | Checked candidate or authorized commits; no implied push                                |
| Publish           | Exact candidate/ref and publication actions authorized; checks current                                                                                                                     | Push the explicit branch, then read remote head; create/update only the requested PR    |
| Review            | Inspect actual feedback and candidate                                                                                                                                                      | Findings or approved feedback changes, new verification and authorized publication      |
| Merge             | Section 6 authority and preconditions hold                                                                                                                                                 | Confirmed platform merge, or explicitly pending/blocked result                          |
| Cleanup / Abandon | Confirmed merge or exact abandonment disposition, owned resources and authorized cleanup                                                                                                   | Only selected safe refs/worktrees removed, or preserved with an explicit pending action |

**Before deletion:** record the branch tip, verify actual merge mapping or abandonment, check unpushed/divergent work and pending follow-up, and inspect `git worktree list`. Never delete a branch checked out anywhere. Squash/rebase integration may not preserve source-commit ancestry; verify platform mapping and final content rather than relying only on ancestor tests.

For an eligible worktree, inspect `git -C "<path>" status --short --ignored` and preserve valuable local/untracked/ignored data before removal. A Git-clean tracked tree is not proof of disposable local content. Remove only the exact authorized path. Move to an owned checkout not on the topic branch before `git branch -d <name>`.

As documented in Git's [branch deletion options](https://git-scm.com/docs/git-branch#_options), `branch -d` checks merging relative to its upstream, or HEAD when no upstream is set. Success is not independent proof of integration into trunk. If it refuses after a confirmed squash merge, retain the branch or use R4 only after exact deletion authority and preserved evidence. Remote deletion, forced worktree removal and metadata pruning each require their own policy checks. A closed PR alone is not authority to abandon local work.

## 4. Pull Request Rules

Use the hosting platform's supported CLI or API interface. Detect actual authentication, repository identity, PR lookup/create/update/review capabilities and relevant permissions; consult its help rather than inventing commands. If unavailable, prepare the requested title/body and report the remote action as unperformed. Reconcile an uncertain create/update result before retrying.

Follow the project's title/body template and conventions. By default use a Conventional Commit title with a specific description, bounded to the relevant change. Choose the real target base (trunk or the maintained release line), and identify source branch/head. Reuse the existing matching PR; do not create duplicates or a PR when only push was requested.

After local checks, present the actual scope and publication actions when required by the caller. Native review submission is itself a remote write: submit only the authorized comment/review, distinguish analysis from native approval, and never invent an approver. Resolve findings or prepare authorized fixes without treating review feedback as a new broad implementation mandate.

Use non-closing issue references unless complete issue closure is intended and authorized; platform auto-close semantics vary. Update a stale PR title/body to describe the final change when authorized. Do not modify labels, reviewers or other metadata beyond the applicable scope.

## 5. Pull Request Template

Prefer the project's template. Otherwise use the following reviewer-oriented shape, omitting irrelevant sections and stating limitations honestly:

```markdown
<type>[(scope)][!]: <description>

## Summary

<problem, resulting behavior and why the change is needed>

## Changes

<bounded scope and relevant issue/contract references>

## Verification

<actual local checks, tested candidate, CI state and genuine manual gaps>

## Impact and Risks

<compatibility, user-facing impact and any applicable rollout/rollback>
```

Use screenshots, migration notes or reviewer focus only when they help assess the change. Required checks remain required even when a template section is omitted. Do not mark an unchecked checklist item complete or call a review approved merely to fill a format.

## 6. Exact Authorized Merge

A human may merge directly, or explicitly authorize the agent for an identified repository, PR, target base and head revision. Applicable previous authority can be reused while those conditions remain unchanged. Artifact approval, requested review, green CI and ordinary publication authority do not authorize merge or auto-merge.

Before merging, verify the live PR is the intended open candidate, its head matches the authorized SHA, the target base/merge method comply with project policy, required final-head checks and native reviews actually passed, dependencies/blockers are resolved and relevant base drift has been assessed. A missing, skipped or pending required check is not a pass. Material integration changes require updated verification and any affected approval before publication.

Use the platform's supported expected-head/compare-and-swap merge precondition with the exact SHA. A client-side read followed by an unconditional merge leaves a race; if the interface cannot enforce the authorized head, stop the agent merge and let the human use an appropriate supported route. Never bypass protections or substitute a local merge-and-push to trunk. Honor the project-selected merge method rather than imposing one globally.

Read back actual merged state and resulting commit/base mapping, accounting for squash/rebase/merge methods. Queue submission or enabled auto-merge is not confirmed merge; changed heads require new assessment and authority. Unknown outcomes must be reconciled before retry. Release/deployment and cleanup remain separate actions after merge.
