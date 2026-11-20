# Design the Owned System

## Applicability and Inputs

This step is required for backend and fullstack projects. For a library, CLI or infrastructure project, use it when the owned product has technical boundaries, runtime or operational interactions that warrant a system blueprint. For frontend-only projects, record that system design does not apply and route client design to `stack`. For any inapplicable scope, report the reason and leave the worktree unchanged.

Read these inputs before making dependent decisions.

| Input                                                                    | What to Extract                                                                                                                                                 |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Project instructions and root `config.agenix.json`                       | Approved scope, targets, documentation language and project constraints.                                                                                        |
| Merged `docs/PRD.md`                                                     | Product goals, critical journeys, mandated constraints and quality targets.                                                                                     |
| Merged `docs/features/catalog.agenix.json` and relevant feature records  | Feature outcomes, pinned PRD coverage, dependencies and provisional quality responsibilities that affect the design.                                            |
| Approved `docs/blueprint/domain-model.md`                                | Business responsibilities, rules, invariants and external obligations. Verify the approval against the artifact revision on the architecture branch.            |
| Existing system design, ADRs and implementation evidence, when available | Accepted decisions, current runtime and deployment boundaries, external contracts and compatibility constraints. Read only the material relevant to the change. |

Verify the merged PRD and catalog against the refreshed default branch and use the owned architecture branch for approved design artifacts. Distinguish observed behavior, approved constraints and proposed design. If a material input is missing or conflicting, pause the affected decision. Route changes to approved business semantics through the owning amendment workflow.

## Outputs

- Write `docs/blueprint/system-design.md` using the [System Design Template](../../evolutionary-architecture-design/assets/system-design-template.md). Apply its section and view guidance to the owned scope.
- Record new or materially changed significant decisions in `docs/blueprint/decisions/` using the [ADR Template](../../evolutionary-architecture-design/assets/adr-template.md) and [ADR Guide](../../evolutionary-architecture-design/references/adr-guide.md). Link ADRs from the system design and preserve their identity, status and history.

The system design supplies approved boundaries, constraints and unresolved technology choices to `stack`. Record technology mandates and decisions needed to evaluate the architecture here. Leave detailed tool and version selection to `stack`.

## Design and Evaluate

Use [Evolutionary Architecture Design](../../evolutionary-architecture-design/SKILL.md) as the main workflow. Use **Design** for a new blueprint and focused **Evolve** for an authorized amendment. Follow its reference routing for the decisions at hand.

1. Turn approved scenarios, quality targets and constraints into prioritized architectural drivers. Trace each material driver to its source and map it to a design choice and a verification criterion. Confirm material gaps or trade-offs with the human.
2. Define the repository's owned responsibilities, runtime and lifecycle, and external interactions. Cover owned client and server responsibilities together for fullstack. Describe external systems through their interfaces and obligations. Use domain boundaries and invariants as design inputs and justify any proposed technical separation.
3. Compare viable alternatives for consequential decisions. Walk representative success, failure and change scenarios through the candidate. Document applicable context, building block, runtime and deployment views at the depth needed to explain the design. Include consequential data ownership, trust boundaries and operational responsibilities where relevant.
4. Specify observable quality criteria and fitness checks for critical architectural properties. Record what each check measures, its threshold, when it should run and what evidence exists. Carry planned checks forward for later strategy and implementation. For an existing system, address compatibility, recovery and migration only where the change affects them.

## Verify and Approve

Check driver coverage, alignment with the approved domain model, consistency across views and ADRs, quality criteria and residual risks. Read back the artifacts, resolve their references and inspect the scoped diff. Record which scenarios were reasoned through and which checks actually ran.

Prepare the root documentation map update for the candidate using [Configure Instructions and Scope](../../../references/project-content.md#configure-instructions-and-scope). Include it in the same approval and publication.

Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates) to the system design and applicable ADRs. Present the candidate and base, material trade-offs, evidence, remaining risks and intended publication. After approval, [publish the candidate](../../../references/git-publication.md#publish-the-approved-candidate) on the architecture branch and bind approval and verification evidence to its revision in the phase PR or a durable checkpoint. Follow the phase publication and session closure rules in the skill entry point.
