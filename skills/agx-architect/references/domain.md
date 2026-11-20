# Model the Owned Domain

**Inputs.** The approved, merged product PRD and feature catalog with its feature records, the approved project scope and targets, and any imposed constraints that affect business behavior. For an amendment, also read the existing approved domain model and the requested change.

**Output.** An approved `docs/blueprint/domain-model.md` published on the architecture branch, with its approval and scenario evidence available to dependent steps.

## 1. Establish the Modeling Scope

Confirm the PRD and catalog are approved and merged on the refreshed default branch. Read the relevant feature outcomes and their pinned PRD references. If an older pin still resolves, check whether current approved requirements have materially changed before relying on it. Resolve conflicting approved inputs through the owning amendment route. Resume matching architecture work and reuse recorded approvals for the same content.

Use the approved scope to identify who owns each material business decision, rule and source of information. Apply the boundary appropriate to the product.

| Project Scope                  | What to Model                                                                                                                                                                     |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Frontend only                  | Owned user workflows, decisions and observable outcomes, including refusals or recovery where applicable. Capture provider rules through their confirmed effects on the client.   |
| Backend only                   | Owned business decisions, rules and state transitions. Treat clients and upstream providers as actors at the boundary where their interactions matter.                            |
| Fullstack                      | Model owned client and server behavior together. Identify who owns each decision and where rules must hold. Choose domain boundaries from business responsibilities and language. |
| Library, CLI or infrastructure | Model the concepts, operations, responsibilities and observable outcomes the product owns, using terminology appropriate to that domain.                                          |

In every scope, capture external responsibilities, inputs and outcomes only as far as the approved evidence supports them. Ask the human about missing external obligations that could change owned behavior.

## 2. Apply Domain Modeling

Use [Domain Modeling](../../domain-modeling/SKILL.md) as the main workflow. Use **Design** for a new model and **Evolve** for an authorized change. Apply its selective reference routing and reuse the [domain model template](../../domain-modeling/assets/domain-model-template.md) at blueprint scope.

1. Derive business language, decisions, outcomes and refusal paths from the approved product scenarios. Keep approved requirement and journey references and cite the feature IDs where they establish coverage. Reuse authoritative decisions and ask the human about material gaps in business meaning, responsibility or rules.
2. Identify business capabilities and model boundaries at a depth suited to the owned scope. Map cross-context responsibilities and translations where they affect behavior. A single context is sufficient when one model and language cover the scope.
3. Apply tactical modeling where identity, lifecycle or invariants justify it. State which business authority makes each consequential decision and what must hold. Leave service topology, transport, storage and tool choices to technical design.
4. On evolution, preserve unaffected decisions and trace changes through scenarios, terminology, rules and boundaries. Identify which downstream designs or specifications need revalidation before they can rely on the change.

## 3. Verify and Approve

Apply [Model Validation](../../domain-modeling/references/model-validation.md). Walk through representative success, alternative and refusal scenarios. Where a rule claims a guarantee across boundaries or under concurrent actions, check the conditions that could invalidate it. Confirm that material in-scope features and requirements have modeled responsibilities or an explicit external owner. Record the scenarios and results in the review evidence separately from the model.

Read back the artifact and inspect the scoped diff. Check source references, terminology, applicable sections, approved documentation language and removal of template instructions. Pause affected work for unresolved material decisions and present only a checked candidate for approval.

Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates). Present the candidate and base, material decisions, scenario results, affected downstream designs and intended commit and push. After approval, [publish the candidate](../../../references/git-publication.md#publish-the-approved-candidate) and bind the approval and scenario results to the published revision in the phase PR or a durable checkpoint. Apply the architecture phase publication rules in the skill entry point.

At the matching human `END`, report the model path, approved revision, scenario results and remaining blockers. Use the invocation table to suggest the next applicable supported step when eligible. A dependent step reads the approved domain model and evidence from the same architecture branch.
