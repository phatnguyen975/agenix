---
name: agx-spec
description: Define the approved specification and applicable contracts for an owned feature. Use for an explicitly selected step and feature ID.
disable-model-invocation: true
metadata:
  author: phatnguyen975
  version: "1.0"
---

# Agenix Spec

## Purpose and Scope

Establish a coherent feature specification and its applicable contracts from approved product and architecture foundations.

## Invocation and Steps

| Invocation                       | When to Use It                                          | Procedure                          |
| -------------------------------- | ------------------------------------------------------- | ---------------------------------- |
| `agx-spec <feature-id> behavior` | Define or amend the feature's behavioral specification. | [Behavior](references/behavior.md) |
| `agx-spec <feature-id> api`      | Define or assess the feature's applicable interfaces.   | [API](references/api.md)           |
| `agx-spec <feature-id> data`     | Assess the feature's owned persistence impact.          | [Data](references/data.md)         |
| `agx-spec <feature-id> ui`       | Define and demonstrate the feature's web UI.            | [UI](references/ui.md)             |

## Operating Rules

- Validate the explicit invocation against **Invocation and Steps**. For invalid input, show the accepted form and leave state untouched. Follow [Select and Prepare a Step](../../references/workflow-control.md#select-and-prepare-a-step). Load the selected procedure and its applicable project instructions and resources.
- Apply [Establish the Branch and Pull Request](../../references/git-publication.md#establish-the-branch-and-pull-request) to select the branch and PR for the current phase or ticket. Reuse an existing owned branch and worktree according to that table. Create a branch only when needed and no matching owned branch exists. Preserve unrelated changes. For Git operations, use the applicable [Git workflow](../autonomous-git-workflow/SKILL.md) method. For every commit, apply its [commit convention](../autonomous-git-workflow/references/commit-convention.md), including identity and attribution, a meaningful body and applicable footers when needed, together with the shared publication rules.
- Resolve packaged resources from the verified installation independently of the project worktree. Keep the installation read-only. Match the approved helper pin when one exists and pass the absolute project root to helpers. Apply [Protect Private Workspace State](../../references/project-content.md#protect-private-workspace-state) when handling private files.
- Reuse applicable approvals and verify discoverable facts. Ask the human before dependent work when a material decision, scope conflict or authority gap remains. Use [Amend an Approved Baseline](../../references/workflow-control.md#amend-an-approved-baseline) when an approved decision or contract needs to change.
- Apply [Write for the Reader and the Artifact](../../references/project-content.md#write-for-the-reader-and-the-artifact) when drafting or updating artifacts. Follow the approved language and the artifact's owning format.
- For a step that requires approval, apply [Artifact Gates](../../references/workflow-control.md#artifact-gates). For approved publication, apply [Publish the Approved Candidate](../../references/git-publication.md#publish-the-approved-candidate) and verify the actual result. Merge and production exposure require separate authority.
- After confirming a managed PR has merged and its required post-merge checks have passed, apply [Clean Up Branches After Merge](../../references/git-publication.md#clean-up-branches-after-merge). For authorized deletion, use [Branch Lifecycle](../autonomous-git-workflow/references/branching-and-pr.md#3-branch-lifecycle).
- Apply [Handle Changes and Exceptions](../../references/work-items-and-evidence.md#handle-changes-and-exceptions) when the selected work needs additions, an amendment, cancellation, an override or recovery from interrupted publication.
- Follow [Session Markers and Handoff](../../references/workflow-control.md#session-markers-and-handoff). For an authorized session transfer, use [Handoff](../handoff/SKILL.md) and the [shared template](../../templates/evidence/handoff.md). Wait for the matching human `END`, then report the outcome and suggest the next eligible invocation for the human to run.
- Use the owned `docs/spec-<feature-id>` branch and worktree for the feature specification phase. Reuse its phase PR when one exists.
- Approve prerequisite outputs before dependent work. Publish approved step outputs on the phase branch. The final applicable step checks the complete specification set and obtains separate merge authority.
- For each approved specification output, add its resolvable path and immutable revision to the feature record's `references`; preserve unrelated references. Include these bindings and their publication in the artifact gate. For a new or changed output in the same batch, first commit the approved artifact, then mechanically bind its actual commit in the feature record and commit that binding; never pin the record's own commit. Verify both commits and push the approved publication. Reconcile an existing artifact commit or binding on resume.
