# Verify Project Setup

## Select the Verification Route

Identify the local setup candidate, any matching setup PR and the state of the verified default-branch baseline.

| Route                             | Authoritative Input                                                                           | Result                                                                                |
| --------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| First setup or approved amendment | The local configure candidate in the owned worktree, plus any existing matching PR on resume. | Complete validated configuration, published PR and verified merge evidence.           |
| Joining                           | The merged setup baseline and the developer's local tools, access and worktree.               | Verification summary and optional initialization of missing private Jira credentials. |

If the initial candidate is missing, report that `configure` must prepare it. If setup already merged, check the actual merge and CI evidence before reporting a resumed first setup complete. If local files differ during joining, validate the merged records separately and report drift. Preserve the developer's edits and checkout.

## 1. Verify Prerequisites for All Modes

Verify Git, Python 3.11 or later, authenticated `gh`, the repository and default branch, and the compatible installed helper and pin. Check effective ignores, tracked paths, root instruction links, the Claude import (optional) and the rendered CI settings.

Verify the actual PR and Actions path, including repository permissions, required checks and native reviews, squash support and any required merge queue. Identify `Agenix Artifacts Gate` as the stable artifact check and verify that it requires successful validation on every configured operating system. Check the actual ruleset and resolve any missing or obsolete required check with the human. Check that the review path is feasible for a solo maintainer when applicable. Access to read metadata establishes only read access. If required permission cannot be established, report the gap or use authoritative administrator evidence.

## 2. Verify the Selected Tracker

| Tracker  | Additional Checks                                                                                                                                                                                                                                                                                                                                         |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `local`  | Apply [Read, Verify and Update](../../../references/trackers/local.md#read-verify-and-update). Check the installed [status verifier](../../../scripts/verify-status.py) with `--help` and confirm access to PR/check evidence. Setup needs no sample project records.                                                                                     |
| `github` | Apply [Verify Setup](../../../references/trackers/github.md#verify-setup) and [Remote Tracker Records](../../../references/work-items-and-evidence.md#remote-tracker-records). Check Issues, permissions, sub-issue support and applicable labels. Include missing label writes in the first-setup approval. Joining reports gaps without editing labels. |
| `jira`   | Follow **Jira Credentials and Mappings** below.                                                                                                                                                                                                                                                                                                           |

### Jira Credentials and Mappings

1. Apply [Verify Project and Access](../../../references/trackers/jira.md#verify-project-and-access) and [Protect Private Workspace State](../../../references/project-content.md#protect-private-workspace-state). Before initializing credentials or calling Jira, bind the worktree to the intended project. For first setup, check the site URL, Cloud ID and project key against the configure decisions. Re-establish the identity if evidence is missing or the candidate changed. For joining, require the worktree's Jira config to match the verified merged config. Pause on a mismatch and keep credentials in their original worktree.
2. If credentials are absent, initialize the [empty template](../assets/jira-credentials.json) only at the verified private path. Give the developer the path for private entry. Preserve existing credentials. Only the [Jira helper](../../../scripts/jira.py) reads the file. Report sanitized errors and the path to check if credential validation or authentication fails.
3. Use [Helper Operations](../../../references/trackers/jira.md#helper-operations) and [Setup Mapping Defaults](../../../references/trackers/jira.md#setup-mapping-defaults). On first setup, use the working config and private credentials to read Jira metadata, resolve pending mappings and verify permissions and required transitions. Ask only about ambiguous mappings or required settings that cannot be established. Record verified IDs before validating the complete record. When joining, check the stored mappings and personal access. If an approved mapping needs to change, return to `configure` through the amendment route.

## 3. Validate the Complete Configuration

Use the installed [artifact validator](../../../scripts/validate-artifacts.py) with `--project-root <absolute-project-root> --stage config` in all three modes. For first setup, validate the completed local candidate. For joining, validate the merged baseline in the matching worktree or an isolated checkout. Report actual results and block dependent actions when required checks fail.

## 4. Report or Publish

### First Setup or Amendment

1. Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates). Present the complete candidate and base, verification results and intended commit, push, applicable tracker writes and PR publication. Reuse earlier decisions for unchanged settings.
2. Apply [Publish the Approved Candidate](../../../references/git-publication.md#publish-the-approved-candidate). Perform the approved writes and verify their results. Create the ready setup PR or update the existing matching PR. On resume, reconcile publication before retrying any write. Apply [Bind Review and CI to the Candidate](../../../references/git-publication.md#bind-review-and-ci-to-the-candidate) to verify bootstrap CI for the final head or its proven test-merge revision.
3. Apply [Merge the Approved Head](../../../references/git-publication.md#merge-the-approved-head) and [Verify Delivery](../../../references/git-publication.md#verify-delivery-and-recover-from-a-failed-check). Wait for human merge or separate exact-head authority. Report completion only after actual merge and required post-merge checks. If pending, report the exact blocker and resume the same PR on the next `verify` invocation.

### Joining

Report the merged revision, pin, tool and permission checks, tracker readiness and blockers. Give the path and outcome of any private initialization. Joining requires no shared artifact approval or publication.
