---
name: agx-scaffold
description: Prepare the approved product foundation and verified project environment. Use for an explicitly selected scaffold step.
disable-model-invocation: true
metadata:
  author: phatnguyen975
  version: "1.0"
---

# Agenix Scaffold

## Purpose and Scope

Turn approved product and architecture foundations into a project structure and runnable, verifiable foundation for the owned scope.

## Invocation and Steps

| Invocation               | When to Use It                                                        | Procedure                            |
| ------------------------ | --------------------------------------------------------------------- | ------------------------------------ |
| `agx-scaffold structure` | Design the owned codebase layout and instruction scopes.              | [Structure](references/structure.md) |
| `agx-scaffold runtime`   | Build and verify the service-independent runtime foundation.          | [Runtime](references/runtime.md)     |
| `agx-scaffold services`  | Prepare and verify applicable development and test services.          | [Services](references/services.md)   |
| `agx-scaffold tests`     | Prepare and verify the approved testing harnesses across owned units. | [Tests](references/tests.md)         |

## Operating Rules

- Validate the explicit invocation against **Invocation and Steps**. For invalid input, show the accepted form and leave state untouched. Follow [Select and Prepare a Step](../../references/workflow-control.md#select-and-prepare-a-step). Load the selected procedure and its applicable project instructions and resources.
- Apply [Establish the Branch and Pull Request](../../references/git-publication.md#establish-the-branch-and-pull-request) to select the branch and PR for the current phase or ticket. Reuse an existing owned branch and worktree according to that table. Create a branch only when needed and no matching owned branch exists. Preserve unrelated changes. Use the applicable [Git workflow](../autonomous-git-workflow/SKILL.md) method when needed.
- Resolve packaged resources from the verified installation independently of the project worktree. Keep the installation read-only. Match the approved helper pin when one exists and pass the absolute project root to helpers. Apply [Protect Private Workspace State](../../references/project-content.md#protect-private-workspace-state) when handling private files.
- Reuse applicable approvals and verify discoverable facts. Ask the human before dependent work when a material decision, scope conflict or authority gap remains. Use [Amend an Approved Baseline](../../references/workflow-control.md#amend-an-approved-baseline) when an approved decision or contract needs to change.
- Apply [Write for the Reader and the Artifact](../../references/project-content.md#write-for-the-reader-and-the-artifact) when drafting or updating artifacts. Follow the approved language and the artifact's owning format.
- For a step that requires approval, apply [Artifact Gates](../../references/workflow-control.md#artifact-gates). For approved publication, apply [Publish the Approved Candidate](../../references/git-publication.md#publish-the-approved-candidate) and verify the actual result. Merge and production exposure require separate authority.
- After confirming a managed PR has merged and its required post-merge checks have passed, apply [Clean Up Branches After Merge](../../references/git-publication.md#clean-up-branches-after-merge). For authorized deletion, use [Branch Lifecycle](../autonomous-git-workflow/references/branching-and-pr.md#3-branch-lifecycle).
- Follow [Session Markers and Handoff](../../references/workflow-control.md#session-markers-and-handoff). For an authorized session transfer, use [Handoff](../handoff/SKILL.md) and the [shared template](../../templates/evidence/handoff.md). Wait for the matching human `END`, then report the outcome and suggest the next eligible invocation for the human to run.
- Use the owned `chore/scaffold` branch and worktree across scaffold steps. Reuse its phase PR when one exists.
- Approve prerequisites before dependent work. Publish approved outputs on the phase branch and merge the phase PR only after the final applicable step verifies the complete scaffold and obtains the required approvals.
