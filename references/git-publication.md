# Git Publication

Use this guide to publish the approved candidate, verify its remote state and complete delivery under separate merge and exposure authority.

## Establish the Branch and Pull Request

Fetch the configured `origin` and verify the repository matches `github-repo`. Use `origin/<default-branch>` for merged-baseline decisions. A failed fetch, remote mismatch or unclear worktree ownership blocks dependent actions. Preserve unrelated edits and index state. Never commit directly to the default branch, force-push, rewrite published history or bypass protections.

| Work                                         | Branch                      | Pull Request                                                                         |
| -------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------ |
| Initial setup or scaffold                    | `chore/<phase>`             | One branch and PR for each phase.                                                    |
| PRD, catalog or architecture                 | `docs/<phase>`              | One branch and PR for each phase.                                                    |
| Feature specification or feature plan        | `docs/<phase>-<feature-id>` | One branch and PR for each phase and feature.                                        |
| Ticket build, review, fixes and ticket ship  | `feat/<ticket-id>-<slug>`   | One branch across these phases and one implementation PR, opened during ticket ship. |
| Feature finalization                         | `docs/status-<feature-id>`  | One branch and separate finalization PR per feature.                                 |
| Joining verification or native task planning | Existing scope              | No Git PR for this operation.                                                        |

Select the row for the current work. For rows that specify one branch per phase, use a different branch for each phase or feature as indicated. All steps within that phase share its branch. For the ticket row, use the same owned branch and worktree across build planning, build, review, fixes and ticket ship. Reuse a matching owned branch and PR when resuming. Create a branch only if the selected work needs one and no matching owned branch exists. Stop on conflicting ownership or ambiguous state.

## Name Commits and Pull Requests

| Purpose                  | Format                                              | Example                                                    |
| ------------------------ | --------------------------------------------------- | ---------------------------------------------------------- |
| Planning commit          | `docs(<phase>): <summary>`                          | `docs(plan): define checkout tickets`                      |
| Setup or scaffold commit | `chore(<phase>): <summary>`                         | `chore(scaffold): wire contract checks`                    |
| Ticket build commit      | `<type>(<component>): <summary> [<ticket-id>]`      | `feat(checkout): validate delivery address [FEAT-003-T01]` |
| Spec amendment commit    | `docs(spec): <summary> [<ticket-id>]`               | `docs(spec): clarify address validation [FEAT-003-T01]`    |
| Ticket PR title          | `<ticket-id>: <ticket title>`                       | `FEAT-003-T01: Validate delivery address`                  |
| Ticket squash title      | `<type>(<component>): <ticket title> [<ticket-id>]` | `feat(checkout): validate delivery address [FEAT-003-T01]` |

Omit `agx-` from phase tokens. Choose the type by the nature of the change and the component by the project's codebase conventions. The ticket's delivery scope is recorded separately. List the implemented task IDs in the build commit body. In the ticket PR body, link the applicable requirements, tasks and verification evidence, including UI and manual results where relevant. Keep ticket references non-closing until delivery is verified.

## Publish the Approved Candidate

1. Verify required local checks and inspect the whole intended diff. Exclude secrets and unrelated changes. Identify the candidate tree and its parent revision before approval.
2. After artifact approval, perform the approved writes. A tracker write may run before the commit when the Git output needs its verified native mapping. Commit only when the approved batch contains Git changes. Before pushing, compare the commit's tree and parent with the approved candidate and base. Allow only changes explicitly approved for recording returned IDs, URLs or completion metadata.
3. Push the verified commit and confirm its remote revision. Store evidence through the PR or another durable checkpoint. If a write fails or its result is uncertain, report the incomplete publication and read back existing commits, PRs and tracker records before retrying. Reuse the approved commit if it still matches the intended publication.
4. For foundation and feature-definition work, use the owning phase PR and move it from draft to ready after the final applicable verification and gate. Merge a feature's published ticket plan before starting its tickets. For ticket implementation, commit and push on the owned branch during build and review. If a PR already exists, verify the updated candidate again before declaring it ready to merge.

Before artifact approval, remote updates are limited to truthful nonterminal progress on selected existing items.

## Bind Review and CI to the Candidate

Record the review decision, reviewed revision or tree, target-base revision, human confirmation and time, findings, manual results and accepted risks. Before a ticket PR exists, keep durable receipts in the local ticket or native tracker comments. At ship, reference those receipts on the PR and bind them to its published head. Record whole-feature acceptance on the finalization PR. A chat decision and a repository-required native review are distinct records.

If the candidate changes after review, compare the full diff. Carry review evidence forward only for explicitly approved bookkeeping, such as routine status, the PR URL, the local review summary or feature completion evidence. For substantive changes, rerun affected checks and obtain fresh approval. Verify required CI on the final head in either case.

- Select checks by affected behavior and consumers. Text needs applicable artifact checks. Changed design demonstrations need replay/render checks. Wire schemas and examples need their contract checks. Preserve historical prototypes as design evidence.
- Setup provisions pinned artifact CI for Windows, Linux and macOS with the stable `Agenix Artifacts Gate`. Require the gate in the applicable ruleset and verify all matrix jobs actually succeeded for the candidate. Scaffold adds applicable verified project commands and its application gate. Until a PR exists, report its required checks as pending. A skipped, missing, empty or stale check cannot prove readiness.
- Bind PR results to the current head and to the tested merge revision when repository checks use one. A passing check on an earlier head does not carry forward. When GitHub Actions supplies required merge-queue checks, configure `merge_group` for those jobs and verify results in the queue context.
- In scaffold CI, get approval for the intentional failure and passing restoration snapshots. Publish them in sequence on the draft PR. Verify the expected failure and the restored result. Final scaffold approval uses the complete restored candidate and its final-head CI.

## Merge the Approved Head

The human may merge directly or authorize AI to merge the exact PR and head. Refresh the base, head, required native reviews, checks and dependencies before an authorized merge. If the candidate needs integration changes, verify and obtain approval for that changed snapshot first. Never use an administrative bypass or enable auto-merge.

- **No required merge queue.** Use `gh pr merge <PR> --repo <owner/repo> --squash --match-head-commit <SHA>`. Setup verifies squash support.
- **Required merge queue.** Verify that the queue uses squash and its pre-queue requirements have passed. Submit the approved head with `--match-head-commit <SHA>` against the configured repository. Pending checks can cause the CLI to enable auto-merge instead of enqueueing. If safe submission is unavailable, report the blocker for the human. Treat queue submission as pending merge.

## Verify Delivery and Recover from a Failed Check

Confirm the actual merge and required post-merge checks on the refreshed default branch. Record reviewed head, verified merge SHA and durable receipts. Resolve squash history with PR mappings when the original commit is no longer available. On interruption, read the existing PR and finish only outstanding actions after revalidation. Reuse the same PR when a human merges later.

A required post-merge ticket failure blocks closure. Keep the failed result on its original revision and create a new repair ticket. Link the original for provenance so the repair can proceed while the original remains open. Once the repair merges, verify the required checks covering the failed scope on the repaired merged revision. Record both PRs, revisions and results before closing the original ticket.

## Clean Up Branches After Merge

After confirming the merge and required post-merge checks, evaluate the local and remote topic branches separately.

1. Check which branches still exist. If the host already removed the remote branch, report it as absent.
2. Keep any branch required by retention policy or pending work. Also keep a local branch with unpushed or divergent changes, or one checked out in any worktree. Report the reason.
3. For each eligible branch, give the human its exact name and remote, if applicable, and ask whether to keep or delete it. Reuse an explicit cleanup decision for the same refs and recheck eligibility before deletion. Merge approval alone does not authorize deletion.

Report which branches were removed or retained. Keep branches while a decision is pending. Cleanup is optional and does not block verified delivery.

## Authorize Feature Exposure

Apply the approved boundary that keeps unfinished behavior away from real users and resources. Use the mechanism suited to the product, such as selective activation, withholding a release or withholding infrastructure application. If a ticket merge would cross that boundary, correct it before merging. Exercise feature acceptance on the integrated baseline with isolation appropriate to the target.

Once feature completion is verified, a configured release, deployment, application or enablement may run during the same ship step only with human authorization for the exact target and verified revision or artifact. Report acceptance, merge, verified completion and exposure separately. Deferred exposure uses the project's operational workflow.
