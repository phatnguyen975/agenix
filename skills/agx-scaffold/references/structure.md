# Design the Codebase Structure

## Inputs and Output

Verify the approved architecture phase was merged and its required checks passed on the refreshed default branch. Read the project instructions and `config.agenix.json` for scope and targets. Read the approved `docs/blueprint/domain-model.md`, `tech-stack.md`, applicable `system-design.md`, `test-strategy.md` and relevant convention files for owned responsibilities, release boundaries, tooling, test placement and structural constraints. Consult applicable data or UI design only when it affects ownership or source boundaries. Read existing repository structure and manifests as evidence where present.

Write `docs/blueprint/codebase-design.md` using the [Codebase Design Template](../../codebase-design/assets/codebase-design-template.md). Use the approved design as the input to later scaffold steps. This step proposes paths and instruction scopes; it does not create runtime skeletons or scoped instruction files.

## Design the Structure

Use [Codebase Design](../../codebase-design/SKILL.md) in **Design** mode and select its references according to the decisions being made.

1. Inventory the owned release units and their consumers. Derive source and test roots, module responsibilities, public surfaces and shared-code ownership from approved foundations and the selected toolchain. Distinguish release units from packages and modules. Do not add an unowned application or an empty layer merely to complete a pattern.
2. Specify intended static dependency directions and cross-unit contract ownership. Map applicable frontend client responsibilities, backend behavior and data ownership to source boundaries. Keep existing approved system and domain decisions authoritative. Surface any material conflict through the owning amendment route.
3. Map test strategy check IDs and applicable levels to intended test locations and boundaries. Describe structural enforcement as planned, verified or a review responsibility based on actual evidence. Do not claim planned directories, commands or checks already exist or pass.
4. Select meaningful module or release-unit instruction scopes. Record proposed paths, responsibilities, parent relationships and relevant design and convention links. Do not create an instruction file in every directory. The final scaffold instructions step writes and verifies actual scoped entries and the root scope index.

Present material alternatives and trade-offs for release boundaries, shared ownership or dependency rules. Obtain human decisions before relying on an unapproved choice. Reuse prior approved decisions. Use the [ADR Guide](../../evolutionary-architecture-design/references/adr-guide.md#decide-what-deserves-a-record) and [ADR Template](../../evolutionary-architecture-design/assets/adr-template.md) for new or changed architecturally significant decisions.

## Verify and Publish

Apply the [Codebase Design Verification Checklist](../../codebase-design/SKILL.md#verification-checklist). Check scope coverage, valid references, ownership, public surfaces, dependency direction, test locations, intended enforcement and consistency with approved foundations. Read back the design, check links and inspect the scoped diff. Distinguish planned controls from observed evidence.

Prepare the root documentation map update using [Configure Instructions and Scope](../../../references/project-content.md#configure-instructions-and-scope). Include the design, map update and applicable ADRs in [Artifact Gates](../../../references/workflow-control.md#artifact-gates). Present the candidate and base, material choices, evidence and intended publication. [Publish the Approved Candidate](../../../references/git-publication.md#publish-the-approved-candidate) on the scaffold branch and bind approval and verification evidence to the published revision in the phase PR or a durable checkpoint. Follow the shared phase and session rules.
