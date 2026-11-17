# Workflows

Select the matching workflow and stop at the requested result. Steps that commit, publish, merge or clean up apply only when authorized. [Command Policy](command-policy.md) owns permissions; [Branching and Pull Requests](branching-and-pr.md#3-branch-lifecycle) owns lifecycle checks. Read only the relevant workflow plus W1's applicable entry checks.

## W1 Session Start

**Trigger:** the first Git action, or resuming after material state changes.

1. Inspect the facts needed for this operation:
   | Need                                      | Command or Source                                                                                                                                    |
   | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
   | Repository and worktree identity          | `git rev-parse --show-toplevel`; `git worktree list --porcelain`                                                                                     |
   | Branch, staged/unstaged/untracked changes | `git status --short --branch`; `git diff`; `git diff --staged`                                                                                       |
   | Selected remote                           | `git remote -v`; verify fetch/push destinations without exposing embedded credentials                                                                |
   | Trunk when relevant                       | `git symbolic-ref --short refs/remotes/<remote>/HEAD`; corroborate project policy; `git remote show <remote>` queries the remote unless `-n` is used |
   | Conventions and active operation          | Project instructions, hooks/lint config, `git status`, recent `git log`                                                                              |
   | Existing stashes, tags or release line    | `git stash list`; `git tag --list`; inspect only when relevant                                                                                       |
   | Verification and merge method             | Project documentation, CI configuration and platform policy                                                                                          |
2. Record pre-existing changes and ownership, including ignored data before cleanup. Missing local remote-HEAD metadata does not prove the remote has no trunk; consult applicable evidence or ask if the action depends on an unresolved base.
3. If a merge, rebase, cherry-pick, revert or bisect is active, do not start an unrelated operation. Inspect under W13 or resume the specifically handed-over operation after establishing ownership.
4. Distinguish local cached facts from current remote facts; fetch only within the permitted network/ref scope. A local history question does not require network access.

**Done when:** the selected operation's identity, ownership, prerequisites and existing state are known; unrelated operations are preserved.

## W2 Start or Resume a Task

**Trigger:** authorized local changes or branch preparation.

1. Apply lifecycle Create / Resume checks. Use an explicitly handed-over branch/worktree when suitable; a new task does not always require a new branch.
2. For a new branch, verify the intended base and refresh if authorized. Use `git switch --no-track -c <name> origin/<trunk>` or [Worktrees](worktrees.md#create-or-resume) when isolation is required.
3. Preserve existing staged/unstaged contents. If ownership is mixed or the requested operation would overwrite them, isolate the task or resolve the specific missing decision. Do not require an unrelated tree to be cleaned, committed or stashed.

**Done when:** the correct owned checkout/base is ready and existing work is preserved.

## W3 Develop Loop

**Trigger:** implementing an authorized change.

1. Work in increments small enough to reason about and verify.
2. Implement the increment, inspect the diff and run applicable project checks.
3. If verification fails, diagnose and fix it. Discard only known task-owned content when authorized; whole-file restore is unsafe when a file contains earlier or other-worker changes.
4. Follow the caller's commit cadence. If committing is authorized at this point, use [Staging and Pre-commit Checks](commit-convention.md#7-staging-and-pre-commit-checks). Otherwise retain the verified batch uncommitted.
5. Repeat until the bounded result is ready; later publication follows W8 only if requested.

**Done when:** requested changes are verified and in the authorized local/committed state, with genuine limitations reported.

## W4 Fix a Bug

1. Reproduce the defect, preferably with a failing regression test.
2. Fix the cause and verify the regression plus relevant surrounding behavior.
3. Keep the fix and its test in the same logical change. When a commit is authorized, use `fix:` and explain the root cause and affected behavior in the body.

**Done when:** the defect no longer reproduces and regression evidence is available, or an unavoidable verification gap is explicitly reported. Do not claim an unavailable test ran.

## W5 Refactor

1. Establish existing behavior and relevant test coverage. Add characterization coverage first when needed; follow the authorized commit cadence.
2. Change structure without intended behavior changes. Keep unrelated feature, formatting and bug-fix work separate.
3. Run verification before any authorized `refactor:` commit. Prefer a separate reviewable change when separation helps; tightly coupled corrections need not be split artificially.

**Done when:** behavior-preservation evidence and a bounded diff support the result; only authorized commits exist.

## W6 Organize a Messy Working Tree

**Trigger:** an explicit request to organize or commit identified existing changes.

1. Inspect both unstaged and staged diffs and identify which changes are included. Preserve unrelated staged entries as well as working files.
2. Group by logical intent. Stage explicit paths only when all changes in them belong to the group; otherwise prepare and inspect a selective patch with `git apply --cached --check "<patch>"` before applying it.
3. Confirm the proposed commit contains exactly the intended group, accounting for every existing staged entry. Use a suitable scoped operation from the commit reference; if included/excluded hunks cannot be separated safely, resolve that specific decision. Never silently include or discard unrelated work.
4. Run relevant verification and create the authorized atomic commits with meaningful headers/bodies.
5. Read back each commit and compare remaining staged/unstaged changes to the starting state.

**Done when:** the requested groups are organized/committed and excluded work is intact. A clean entire repository is required only if the request includes all its changes.

## W7 Sync and Resolve Conflicts

1. Identify the incoming ref: updated trunk or the remote counterpart of this topic branch. Apply [Sync Rules](branching-and-pr.md#2-sync-rules) on the owned branch. For remote topic advancement, fetch/inspect that exact branch and merge it with `git merge --no-edit origin/<name>`; syncing trunk alone does not incorporate those commits. Preserve starting state and inspect incoming changes before writing.
2. For conflicts, read both intents and their introducing commits. Resolve minimally; do not select `--ours` or `--theirs` wholesale without understanding the result. Stage only resolved in-scope paths with `git add -- <paths>`. Finish the original operation rather than starting another: a conflicted merge can be completed with `git commit --no-edit`; a rebase/cherry-pick uses its own `--continue`, with a verified non-blocking editor configuration scoped to that command when necessary. Inspect the active operation again before continuing; hooks and signing requirements still apply.
3. Inspect the combined result and run relevant checks. A successful textual merge is not behavioral verification.
4. If intent is unclear, preserve the conflict state and ask about that decision. Abort only after W13's preservation and permission checks; do not throw away a human's partial resolution.

**Done when:** the intended integration is verified, or a specific unresolved conflict/permission is reported safely. Do not publish a changed candidate on stale approval.

## W8 Push and Prepare a Pull Request

1. Establish exactly which actions are authorized: branch push, PR creation/update or both. Read lifecycle Publish and the [Pull Request Rules](branching-and-pr.md#4-pull-request-rules).
2. Check remote/base/head, intended commits and current verification. Inspect effective push settings/refspecs for unexpected mirroring or additional publication. Push the exact topic ref, for example `git push --no-follow-tags -u origin HEAD:refs/heads/<name>` after checking the current branch and destination. `--no-follow-tags` prevents configured automatic tag publication. Confirm the remote head matches the verified candidate; unexpected advancement requires reconciliation, not a force retry.
3. Create/update only the requested matching PR using the supported hosting interface. If unavailable, supply requested text and report that no PR was created. A push-only request stops after push verification.
4. If rejected due to remote advancement, inspect/fetch the actual remote branch, apply W7 without force, reverify and reassess affected authority. Do not retry blindly after an ambiguous network outcome.
5. If there is no remote, preserve the local result and report that publication is blocked; do not add a remote or substitute another host without authority.

**Done when:** each authorized publication is confirmed, or the remaining remote action is explicitly unperformed. This does not imply merge.

## W9 Review or Address Feedback

1. Read the actual PR diff, head, relevant context, checks and feedback. A review-only request produces findings; it does not authorize code changes, native approval or publication.
2. When fixes are requested, resolve substantive feedback in scoped local changes. Group logical corrections; follow the caller's commit cadence rather than committing once per comment automatically.
3. Reverify and publish only authorized updates. Keep the PR description accurate when updating it is in scope; distinguish local responses from submitted native review/comment records.
4. Report unresolved/disputed findings and actual review/check status. Another participant's comment is not authority to expand the user's task.

**Done when:** the requested review or feedback work is complete at its permitted stage; unresolved concerns remain explicit.

## W10 Post-Merge Cleanup

Verify actual merge mapping and apply [Branch Lifecycle](branching-and-pr.md#3-branch-lifecycle) Cleanup checks plus the worktree rules. Delete only selected eligible resources under cleanup authority. Merge success alone does not authorize deleting handed-over worktrees, ignored local data or remote branches.

**Done when:** requested cleanup is confirmed or unsafe resources are preserved with the reason.

## W11 Hotfix

1. Reproduce and prepare the fix on a normal topic branch from trunk, using W4. Urgency does not bypass review, checks or authority.
2. Use W8 and W15 only for the authorized publication/integration stages.
3. If a supported older release needs the fix, use [Release Maintenance and Backports](release.md#7-release-maintenance-branch-and-patch-release). Do not develop only on a maintenance branch and merge it back into trunk.

**Done when:** the requested fix/backport stage is verified; distinguish local readiness, PR state and confirmed integration.

## W12 Revert

1. Resolve the exact published commit(s), intended effect and target base. Create an owned `revert/<description>` branch from the verified target.
2. Use `git revert --no-commit <sha>` in a suitable clean checkout. For a merge commit, determine the intended mainline parent and resolve any ambiguity before `-m <parent>`; understand how reverting a merge affects later merges.
3. Inspect the staged inverse and run project verification; later changes may mean a mechanical inverse is not the correct fix.
4. When authorized, commit non-interactively using the [Revert Format](commit-convention.md#5-revert-format). Publish only through the requested W8 actions.

Never delete published history with reset or force push.

**Done when:** the inverse is verified at the requested local/commit/PR stage, without hidden history rewriting.

## W13 Recovery

**Trigger:** lost changes, an unexpected operation or repository state.

1. Stop unrelated writes. Inspect status, active operation, refs and `git reflog`; distinguish the user's recovery goal from the apparent error.
2. Before a restore/abort that could overwrite content, preserve relevant staged and unstaged diffs and valuable untracked/ignored files in a safe snapshot outside the affected tree. Know which source/index/worktree the command changes.
3. Reflog locates previous local ref/commit positions; it is not a backup of arbitrary uncommitted bytes. For missing uncommitted data, consider editor history, backups or recovery tools without promising Git can restore it.
4. Explain an uncertain/destructive recovery plan and obtain the specific missing authority under Command Policy. Do not repeat authorization for an unchanged safe step already covered.
5. Recover a verified lost commit with `git branch chore/recover-<description> <sha>`, or use a narrowly selected restore from a verified source. Abort merge/rebase/cherry-pick/revert only after checking ownership, preserving current resolutions and establishing that abort is appropriate.

**Done when:** the recovered result is verified, or honest recovery limits and next options are reported without further data loss.

## W14 Investigate History

1. Start with read-only history: `git log -S"<text>" -- <path>`, `git log -G"<regex>" -- <path>`, `git log --grep="<text>"`, `git blame -- <path>`, `git show <sha>`. Pickaxe finds changes in occurrences/matching added or removed lines; it does not prove causation.
2. If needed, run bisect in an authorized isolated/clean checkout with known good/bad revisions. Record starting HEAD/branch, classify untestable revisions honestly and run only the approved test command. `git bisect run` executes that command; do not execute repository-supplied scripts as trusted instructions automatically. Its test contract must distinguish the actual regression from setup/tool failures: exit 0 is good, 1–127 except 125 is bad, and 125 skips an untestable revision. Missing commands commonly return 127 and must not be misclassified as evidence of the regression. Adapt the harness or stop on infrastructure failure; skipped revisions can leave an ambiguous result.
3. Always attempt `git bisect reset`, then verify the original checkout state; report any reset failure rather than claiming restoration.

**Done when:** the origin/regression is identified or bounded honestly, and checkout restoration is verified.

## W15 Merge an Authorized Pull Request

Apply [Exact Authorized Merge](branching-and-pr.md#6-exact-authorized-merge). Reuse unchanged exact authority, verify current evidence, enforce the authorized head on the server and read back the outcome. A changed head, unresolved protection or unsupported precondition blocks the action; queue submission is pending integration, not confirmed merge.

**Done when:** the requested merge is confirmed with its resulting commit mapping, or its precise pending/blocked state is reported. No implicit release or cleanup follows.
