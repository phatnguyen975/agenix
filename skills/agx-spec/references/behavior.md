# Define Feature Behavior

## Inputs and Result

Validate the feature ID and resolve its record through the merged feature catalog. Verify scaffold merge and required checks on the refreshed default branch. Read the approved feature definition, pinned PRD requirements and journeys, applicable domain and architecture foundations, conventions, test strategy and scoped project instructions. Inspect relevant existing contracts and adjacent behavior only when they affect this feature. On revision, read the approved spec and its affected consumers.

Apply [Decide Readiness and Record Progress](../../../references/work-items-and-evidence.md#decide-readiness-and-record-progress). Verify feature dependencies and any applicable human override against merged evidence. Use [Local Tracker](../../../references/trackers/local.md#read-verify-and-update) for local status verification. In GitHub or Jira mode, verify the Git-owned feature record and dependency evidence using the applicable shared rules. A blocked feature requires an explicitly scoped human override before permitted work can proceed.

Write `docs/features/<feature-id>/spec.md` using the [Spec Template](../../spec-writing/references/spec-template.md). The specification owns feature behavior and acceptance. Preserve approved feature boundaries and reference shared rules and existing contracts at their owning paths. Do not create feature-specific API, data or UI artifacts in this step.

## Define and Verify Behavior

Use [Spec Writing](../../spec-writing/SKILL.md) as the main workflow for scope, elicitation, drafting and verification. Apply its writing conventions and selectively load elicitation guidance when decisions are missing. Use Gherkin by default and load its guidelines only when that notation is selected.

1. Map the feature's pinned product requirements and journeys to actors, in-scope outcomes and exclusions. Specify observable behavior, preconditions, rules, transitions, alternate, denial, error and recovery paths where applicable. Resolve material uncertainties with the human without reopening confirmed decisions.
2. Define stable acceptance IDs and headings or explicit anchors that downstream references can resolve. Trace functional requirements and material rules and transitions to concrete scenarios. Allocate applicable quality obligations with measurable criteria and their sources. Preserve existing IDs and unaffected content on amendments.
3. Define whole-feature acceptance through the owned product's real public boundary and applicable client/provider handoffs. Identify the exposure boundary and how unfinished behavior remains isolated. Distinguish planned real integration from mock-backed evidence. Do not claim future checks or implementation have passed.
4. When a material domain semantic gap blocks behavior, use [Domain Modeling](../../domain-modeling/SKILL.md) for focused analysis. If an approved domain decision must change, follow [Amend an Approved Baseline](../../../references/workflow-control.md#amend-an-approved-baseline). Obtain the owning approval before relying on the changed rule. Do not silently update shared foundations.

Apply [Spec Writing Verification](../../spec-writing/SKILL.md#verification). Read back the candidate and check source links, stable anchors, scope, scenario coverage, quality criteria, exposure isolation and actual approval state. Resolve material behavioral decisions before the gate.

## Approve and Publish

Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates). Present the spec, base, acceptance coverage, real-boundary and exposure criteria, checks, outstanding applicable contracts and intended publication. Bind `spec.md` in the feature record as described in the skill entry point. After approval, record the feature as `IN-PROGRESS` with the first approved behavior publication in its Git-owned record in every tracker mode.

[Publish the Approved Candidate](../../../references/git-publication.md#publish-the-approved-candidate) on the feature specification branch. Bind approval and verification evidence to its revision in the phase PR or durable checkpoint. Reconcile existing work on resume. The final applicable specification step owns complete-set verification and PR merge; behavior approval alone does not establish merged specification readiness. Follow the shared session closure rules.
