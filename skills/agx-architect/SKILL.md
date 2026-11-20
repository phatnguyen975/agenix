---
name: agx-architect
description: Design the owned product blueprint from approved product requirements and feature definitions. Use for an explicitly selected architecture step.
disable-model-invocation: true
metadata:
  author: phatnguyen975
  version: "1.0"
---

# Agenix Architect

## Purpose and Scope

Design the applicable domain and technical foundations for the owned product. Use approved upstream artifacts and carry each approved design decision into the steps that depend on it.

## Invocation and Steps

| Invocation             | When to Use It                                                                                        | Procedure                      |
| ---------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------ |
| `agx-architect domain` | Model owned business language, behavior and responsibilities from the merged PRD and feature catalog. | [Domain](references/domain.md) |
| `agx-architect system` | Design the owned system where applicable, using the approved domain model.                            | [System](references/system.md) |
| `agx-architect stack`  | Select and confirm the technology stack for the approved scope and release units.                     | [Stack](references/stack.md)   |
| `agx-architect data`   | Design owned persistence using the approved domain, system and stack decisions.                       | [Data](references/data.md)     |
| `agx-architect ui`     | Define and demonstrate shared web UI design foundations.                                              | [UI](references/ui.md)         |

## Operating Rules

- Validate the explicit invocation against **Invocation and Steps**. For invalid input, show the accepted form and leave state untouched. Follow [Select and Prepare a Step](../../references/workflow-control.md#select-and-prepare-a-step). Load the selected procedure and its applicable project instructions and resources.
- Apply [Establish the Branch and Pull Request](../../references/git-publication.md#establish-the-branch-and-pull-request) to select the branch and PR for the current phase or ticket. Reuse an existing owned branch and worktree according to that table. Create a branch only when needed and no matching owned branch exists. Preserve unrelated changes. Use the applicable [Git workflow](../autonomous-git-workflow/SKILL.md) method when needed.
- Resolve packaged resources from the verified installation independently of the project worktree. Keep the installation read-only. Match the approved helper pin when one exists and pass the absolute project root to helpers. Apply [Protect Private Workspace State](../../references/project-content.md#protect-private-workspace-state) when handling private files.
- Reuse applicable approvals and verify discoverable facts. Ask the human before dependent work when a material decision, scope conflict or authority gap remains. Use [Amend an Approved Baseline](../../references/workflow-control.md#amend-an-approved-baseline) when an approved decision or contract needs to change.
- Apply [Write for the Reader and the Artifact](../../references/project-content.md#write-for-the-reader-and-the-artifact) when drafting or updating artifacts. Follow the approved language and the artifact's owning format.
- For a step that requires approval, apply [Artifact Gates](../../references/workflow-control.md#artifact-gates). For approved publication, apply [Publish the Approved Candidate](../../references/git-publication.md#publish-the-approved-candidate) and verify the actual result. Merge and production exposure require separate authority.
- After confirming a managed PR has merged and its required post-merge checks have passed, apply [Clean Up Branches After Merge](../../references/git-publication.md#clean-up-branches-after-merge). For authorized deletion, use [Branch Lifecycle](../autonomous-git-workflow/references/branching-and-pr.md#3-branch-lifecycle).
- Follow [Session Markers and Handoff](../../references/workflow-control.md#session-markers-and-handoff). For an authorized session transfer, use [Handoff](../handoff/SKILL.md) and the [shared template](../../templates/evidence/handoff.md). Wait for the matching human `END`, then report the outcome and suggest the next eligible invocation for the human to run.
- Use the owned `docs/architect` branch and worktree for the architecture phase. Reuse its phase PR when one exists.
- Approve prerequisites before starting dependent design. Check the recorded approval and the actual artifact revision when resuming. Revalidate affected decisions if the baseline changes.
- Publish approved step outputs on the phase branch. Merge the phase PR only after the final applicable architecture step has verified the complete blueprint and obtained the required approvals.
