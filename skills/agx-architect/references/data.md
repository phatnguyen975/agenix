# Design Owned Persistence

## Applicability and Inputs

Use this step when the approved scope includes owned persistent data, including client-local persistence. Determine applicability from approved responsibilities and storage decisions. If no persistence is owned, report the basis for omission and leave the worktree unchanged.

| Input                                                              | What to Use                                                                                    |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| Root instructions and `config.agenix.json`                         | Approved scope, targets, documentation language and relevant constraints.                      |
| Merged `docs/PRD.md`, feature catalog and relevant feature records | Data-related outcomes, access scenarios, quality and lifecycle obligations, and their sources. |
| Approved `docs/blueprint/domain-model.md`                          | Business concepts, ownership, identities, relationships, invariants and lifecycle rules.       |
| Approved `docs/blueprint/system-design.md`, when applicable        | Storage ownership, trust boundaries, interactions and consistency requirements.                |
| Approved `docs/blueprint/tech-stack.md` and relevant ADRs          | Selected stores, versions, hosting, supported capabilities and constraints.                    |
| Existing database design and approved change, when amending        | Prior design intent, affected decisions and references.                                        |

Verify the PRD and catalog on the refreshed default branch. Verify each applicable architecture input and its approval at the published revision on the architecture branch. Reuse approved decisions. Resolve conflicts or missing material requirements with the human, using the owning amendment route when an approved baseline must change.

## Design the Initial Model

Write `docs/blueprint/database-design.md`. Use [Database Design](../../database-design/SKILL.md) for an initial relational or document model, including its input checks, selective reference routing and verification. Use the [SQL template](../../database-design/assets/database-design-sql.md) for relational storage or the [Document template](../../database-design/assets/database-design-nosql.md) for document storage. When more than one applies, combine the applicable sections in the same document and identify the owning store for each model and shared invariant. For a store outside those paradigms, use its documented capabilities and equivalent checks below, adapting the document structure to the model.

1. Establish data ownership, identity, lifecycle and access patterns from approved scenarios. Include tenant and authorization boundaries, retention and sensitive data where applicable. Ask about decisions that affect identity, ownership, cardinality, consistency or protection. Label nonblocking unknowns without inventing values.
2. Map confirmed business facts and relationships to the selected store and target version. Define authoritative enforcement of shared invariants, write and read paths, concurrency and failure behavior. Justify indexes, duplication and any store-specific features from the workload and verify support for the selected version and hosting.
3. For client-local persistence, design only owned local data and its lifecycle, synchronization and authority boundaries where applicable. Describe externally owned data through approved interactions and obligations.
4. For an authorized amendment to design intent, preserve unaffected content, assess downstream consumers and revalidate affected assumptions. Use integrated schema declarations and relevant migration history at the selected revision as evidence of current repository state. Do not infer an environment's applied state from repository history alone. Apply [Keep Design and Implementation Sources Aligned](../../../references/project-content.md#keep-design-and-implementation-sources-aligned).

Use the [ADR Guide](../../evolutionary-architecture-design/references/adr-guide.md#decide-what-deserves-a-record) and [ADR Template](../../evolutionary-architecture-design/assets/adr-template.md) for new or changed architecturally significant decisions. Store them under `docs/blueprint/decisions/` and link them from the design.

## Verify and Approve

Apply the relevant verification checklist in [Database Design](../../database-design/SKILL.md#verification), including normal and conflicting operations, data ownership, integrity, concurrency, lifecycle and version support. For other store models, check equivalent guarantees against the actual store and version. Distinguish design reasoning and documentation from checks actually executed. Resolve blocking decisions before presenting an implementation-ready candidate.

Read back the design and ADRs, check source references and consistency with approved domain, system and stack decisions, and inspect the scoped diff. Prepare the root documentation map update for the candidate using [Configure Instructions and Scope](../../../references/project-content.md#configure-instructions-and-scope). Include it in the same approval and publication.

Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates). Present the candidate, material decisions, evidence, limitations and intended publication. [Publish the Approved Candidate](../../../references/git-publication.md#publish-the-approved-candidate) on the architecture branch and bind approval and verification evidence to its revision in the phase PR or a durable checkpoint.

Scaffold owns initial schema and migration harness implementation. Feature implementation owns subsequent migrations and their execution evidence. Follow the phase publication and session closure rules in the skill entry point.
