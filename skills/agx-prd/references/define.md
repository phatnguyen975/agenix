# Define Product Requirements

**Input.** Merged setup, approved project scope and documentation language, and available product context such as stakeholder notes, an idea, a proposal or an existing PRD.

**Output.** One product baseline at `docs/PRD.md`. An approved, merged PRD with verified delivery is the prerequisite for feature definition.

## 1. Establish Scope and Baseline

1. Verify setup on the refreshed default branch using the merged project configuration and available setup merge and required check evidence. A local setup candidate alone does not satisfy this prerequisite. Use the same procedure for local, GitHub and Jira tracker modes. This step creates no tracker records.
2. Apply the shared branch rule to use the owned `docs/prd` branch and its phase PR. Inspect the existing PRD, branch and PR before writing. Resume matching work from its actual state. For an approved baseline, require an authorized amendment scope before changing it and assess impact on existing references and consumers.
3. Load [PRD Writing](../../prd-writing/SKILL.md) as the primary workflow for intake, elicitation, drafting and review. Map what is known to the [PRD template](../../prd-writing/references/prd-template.md). Reuse prior decisions and identify any gaps that materially affect the product scope, users, outcomes or requirements.

## 2. Resolve Material Gaps

Use the [PRD elicitation flow](../../prd-writing/references/elicitation-flow.md) for missing or conflicting requirements, priorities and success targets. Ask focused questions and carry confirmed answers directly into the draft.

Use [Ideation](../../ideation/SKILL.md) only when materially different product directions are still plausible and selecting one would change the proposed users, outcomes, scope or core capabilities. An agreed direction with missing requirement details stays in PRD elicitation.

1. Pause drafting the affected requirements. Frame the open decision with the affected users, intended outcome, available evidence and confirmed constraints. Use [Explore](../../ideation/SKILL.md#1-explore--divergent-thinking) to generate distinct options only if viable alternatives are missing. Reuse earlier exploration and read [Ideation Techniques](../../ideation/references/ideation-techniques.md) only if additional framing or generation is needed.
2. Use [Compare](../../ideation/SKILL.md#2-compare--convergent-thinking) and the [Evaluation Criteria](../../ideation/references/evaluation-criteria.md) to surface trade-offs against the agreed outcome and constraints. Present the recommendation, decision-critical assumptions and what evidence could change it. Ask the human to choose when the direction remains open.
3. Return to PRD elicitation after the decision. Carry forward the chosen direction, consequences for scope and assumptions with agreed validation plans. Keep the comparison in conversation and retain only rationale needed to understand the PRD. Skip the standalone concept workflow, idea document and discovery transcript. If the choice remains unresolved, report the blocker and pause the dependent content and final approval.

## 3. Draft and Verify the PRD

Write `docs/PRD.md` using the [PRD template](../../prd-writing/references/prd-template.md), shared authoring rules and [Requirement Writing Conventions](../../prd-writing/references/writing-conventions.md). Identify the source and rationale for imposed constraints. Leave architecture, implementation tasks and feature catalog creation to their owning workflows.

Apply the [PRD verification checklist](../../prd-writing/SKILL.md#verification). In particular:

- Keep stable, unique journey and requirement IDs using the template conventions. Preserve existing IDs on amendments, allocate unused IDs for new items and verify that references resolve.
- Check that goals have measurable outcomes, in-scope journeys have coverage, and each requirement traces to its source or need. Use evidence and human decisions for targets. Label accepted assumptions and how they will be validated.
- Read back the saved document and review the full intended diff. Check headings, links, Markdown, language, scope and actual revision and approval state. Resolve material choices and remove instruction placeholders before presenting the complete candidate. Report any applicable check still pending.

## 4. Approve, Publish and Verify Delivery

1. Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates) to approve the PRD candidate and intended publication. Record truthful document metadata and retain approval evidence on the PR.
2. [Publish the Approved Candidate](../../../references/git-publication.md#publish-the-approved-candidate), then [Bind Review and CI](../../../references/git-publication.md#bind-review-and-ci-to-the-candidate) to the final head. Apply those rules to any approved metadata updates. On resume, reconcile the existing PR and evidence before retrying a write.
3. Follow [Merge the Approved Head](../../../references/git-publication.md#merge-the-approved-head) and [Verify Delivery](../../../references/git-publication.md#verify-delivery-and-recover-from-a-failed-check). Wait for human merge or separate authority to merge the exact head. Report the PRD path, PR, merge revision and actual check results when complete. If pending, report the blocker and resume the same PR. After the matching human `END`, suggest `agx-feature define` only when its PRD prerequisite is satisfied.
