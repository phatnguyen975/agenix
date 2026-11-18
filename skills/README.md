# Agenix — Skill Catalog

This catalog lists the skills available in this plugin. Start with a skill's `SKILL.md` and load supporting resources as needed.

## Maintaining This Catalog

- Keep entries in alphabetical order and link to the skill's local `SKILL.md`.
- Describe the work each skill supports. Update its entry when its purpose or scope changes.
- **Capability skills** provide reusable methods for specific tasks. Record each skill's purpose and when to use it.
- **Workflow skills** coordinate related steps to achieve a larger outcome. Record the outcome and what the workflow coordinates.
- **Imported skills** bring in upstream methods for local use. Record each skill's purpose, upstream source, exact revision, license, and local adaptations. Preserve required notices with the skill.

## Capability Skills

| Skill                                                                         | Purpose and Use                                                                                                                                                                                             |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [api-contract-design](api-contract-design/SKILL.md)                           | Define or review what clients can rely on when using an HTTP API, RPC, event, or stream. Specify schemas, interaction semantics, errors, and compatibility when the contract changes.                       |
| [autonomous-git-workflow](autonomous-git-workflow/SKILL.md)                   | Carry out authorized trunk-based Git work. Establish the correct branch or worktree, keep commits atomic, and handle synchronization, pull requests, merges, recovery, or releases within the agreed scope. |
| [code-review](code-review/SKILL.md)                                           | Evaluate a bounded code change against its requirements and relevant quality criteria. Verify findings with evidence and explain the impact and corrective action.                                          |
| [code-simplification](code-simplification/SKILL.md)                           | Make tested code easier to understand and maintain by reducing duplication, indirection, or control-flow complexity. Verify that observable behavior stays the same.                                        |
| [codebase-design](codebase-design/SKILL.md)                                   | Design or review how a codebase is organized. Define release units, module boundaries, public surfaces, permitted dependencies, and the checks that protect them.                                           |
| [codegraph-intelligence](codegraph-intelligence/SKILL.md)                     | Use the project's selected CodeGraph CLI and a usable index to trace symbol relationships, investigate change impact, and identify candidate affected tests.                                                |
| [context-priming](context-priming/SKILL.md)                                   | Establish the context needed to start, resume, or redirect a task. Reconcile relevant instructions, earlier decisions, repository state, and evidence before proceeding.                                    |
| [data-impact-analysis](data-impact-analysis/SKILL.md)                         | Assess how a change affects persisted data against an established baseline. Identify affected consumers, model changes, migration dependencies, compatibility risks, and verification needs.                |
| [database-design](database-design/SKILL.md)                                   | Translate requirements into an initial relational or document data model for a selected storage paradigm. Define structures, relationships, integrity constraints, and access paths.                        |
| [domain-modeling](domain-modeling/SKILL.md)                                   | Develop a technology-independent model of the business domain. Establish shared terminology, bounded contexts, workflows, and invariants that later design can rely on.                                     |
| [evolutionary-architecture-design](evolutionary-architecture-design/SKILL.md) | Make or review architectural decisions against system drivers and trade-offs. Plan incremental evolution and define fitness functions that check whether architectural properties hold.                     |
| [grilling](grilling/SKILL.md)                                                 | Resolve multiple consequential uncertainties in an idea, plan, or decision through focused rounds of questions. Establish what is settled and what still needs a decision.                                  |
| [handoff](handoff/SKILL.md)                                                   | Prepare a concise snapshot for another session, agent, or person. Preserve the work state, decisions, evidence, open issues, and next action needed to resume.                                              |
| [ideation](ideation/SKILL.md)                                                 | Turn an open product, feature, or process idea into a clearer direction. Explore meaningful alternatives, compare trade-offs, and make assumptions explicit.                                                |
| [incremental-implementation](incremental-implementation/SKILL.md)             | Implement nontrivial work through small, dependency-aware increments. Apply the agreed verification method to each increment and record its outcome or blockers.                                            |
| [prd-writing](prd-writing/SKILL.md)                                           | Create or revise a PRD for a product or significant feature. Clarify product decisions and connect goals, user journeys, requirements, constraints, and success measures.                                   |
| [spec-writing](spec-writing/SKILL.md)                                         | Define what one feature must do from the user's or consumer's perspective. Specify rules, scenarios, state transitions, quality constraints, and verifiable acceptance criteria.                            |
| [systematic-debugging](systematic-debugging/SKILL.md)                         | Investigate a reproducible, intermittent, or regressing failure. Isolate and confirm the cause, then verify an authorized fix and its regression coverage.                                                  |
| [tdd](tdd/SKILL.md)                                                           | Derive tests from required behavior and drive implementation with Red-Green-Refactor. Observe an expected failure, make the smallest passing change, and refactor under the tests.                          |
| [work-breakdown-planning](work-breakdown-planning/SKILL.md)                   | Turn a scoped outcome into verifiable work. Define acceptance criteria, hard dependencies, and an execution order that supports independent work where possible.                                            |

## Workflow Skills

Workflow skills will be listed here as they are added.

## Imported Skills

Imported skills will be listed here as they are added.
