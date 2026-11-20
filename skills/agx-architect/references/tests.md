# Design the Test Strategy

## Inputs and Output

Read the root project instructions and `config.agenix.json` for approved scope and targets. Use the merged PRD and relevant feature catalog records for journeys, requirements and quality risks. On the architecture branch, verify the approved revisions and evidence for the domain model, tech stack, applicable system, data and UI designs, and convention files. Read relevant ADRs for material constraints and intended fitness checks. Inspect existing tests, tool configurations and evidence only when available and relevant. Resolve material conflicts through the owning amendment route.

Write `docs/blueprint/test-strategy.md` using the [Test Strategy Template](../../test-strategy-design/assets/test-strategy-template.md). This step designs coverage and tooling. Scaffold implements the harnesses, verifies commands and environments, and wires CI.

## Design Coverage and Tooling

Use [Test Strategy Design](../../test-strategy-design/SKILL.md) as the primary workflow.

1. Identify material failures from approved requirements, journeys, boundaries, quality targets and conventions. Cover each owned unit and relevant cross-unit handoff. Record risk and requirement references and stable check IDs. Use [Test Design Techniques](../../tdd/references/test-design-techniques.md) selectively when a material risk needs additional behavior, boundary or failure cases. Keep cases at strategy depth.
2. Select unit or component, integration, API or contract, end-to-end, and specialized or manual checks where they address distinct risks. Specify the boundary exercised, meaningful pass criteria and actual target. For fullstack, allocate coverage to client and provider and include real integration for relevant handoffs. Mocks and schema validation have their own limited evidence. Use the owned public boundary for frontend-only, backend-only, library, CLI or infrastructure scope.
3. Record when each check runs, its trigger, environment and the decision that needs its evidence. Include local feedback, review or PR checks, post-merge checks and release checks where applicable. Define browser and accessibility targets for owned web UI. Prototype replay establishes design evidence; production behavior needs its own checks. Identify fixtures, real and substituted dependencies, isolation, reset and access requirements.
4. Choose tools compatible with the approved stack, including versions or compatibility constraints and intended test locations. Reuse mandated or approved choices. Compare alternatives for material open tool decisions and obtain human confirmation. If a choice would alter an approved foundation, use the owning amendment route. Record new or materially changed architecturally significant decisions using the [ADR Guide](../../evolutionary-architecture-design/references/adr-guide.md#decide-what-deserves-a-record) and [ADR Template](../../evolutionary-architecture-design/assets/adr-template.md). Link relevant ADRs.
5. Specify what scaffold must set up and how a new or changed automated harness demonstrates discovery, an intentional assertion failure and restored success. Mark planned checks and tools accurately. Do not invent measured results or verified commands.

## Verify the Blueprint and Publish

Apply the [Test Strategy Verification Checklist](../../test-strategy-design/SKILL.md#verification-checklist). Check risk and requirement coverage, unique check IDs, cross-unit and real-boundary evidence, feasible targets and run conditions, tool compatibility, and manual responsibilities. Identify gaps and outstanding harness work without presenting planned checks as executed.

As the final applicable architecture step, review the complete applicable blueprint, ADRs, approvals and their revisions. Check consistency, scope, links, shared documentation map and prerequisite evidence. Prepare the map update for the strategy using [Configure Instructions and Scope](../../../references/project-content.md#configure-instructions-and-scope). Resolve material conflicts through the owning step before dependent publication.

Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates) to the strategy, applicable ADRs and map update. Present the complete candidate, coverage, evidence, limitations and intended commit, push and phase PR actions. [Publish the Approved Candidate](../../../references/git-publication.md#publish-the-approved-candidate), then [Bind Review and CI](../../../references/git-publication.md#bind-review-and-ci-to-the-candidate) to the final head and make the phase PR ready when requirements are satisfied. On resume, reconcile the existing PR and evidence before retrying writes.

Follow [Merge the Approved Head](../../../references/git-publication.md#merge-the-approved-head) and [Verify Delivery](../../../references/git-publication.md#verify-delivery-and-recover-from-a-failed-check). Wait for human merge or separate authority to merge the exact head. Report completion only after the merge and required post-merge checks. Otherwise report the blocker and resume the same PR. Follow the shared session closure rule.
