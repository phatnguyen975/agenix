# Agenix — Skill Catalog

This directory contains reusable skills maintained in this repository. This index helps maintainers find a skill by purpose and navigate to its instructions. Each linked `SKILL.md` owns that skill's detailed scope, prerequisites, procedure and resource routes.

Capability skills provide independently reusable methods. Workflow skills compose methods into explicitly invoked steps. Index membership does not mean a skill should run for every task, or that it is already compatible with a particular workflow.

## Available Skills

The current directory contains 20 capability skills. Workflow skills and additional capabilities selected in the implementation plan are not present yet; add their index entries when their directories are created or imported.

| Skill                                                                         | Purpose / When to Use                                                                                        |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [api-contract-design](api-contract-design/SKILL.md)                           | Design, review or evolve a consumer-visible API/message contract; not its implementation.                    |
| [autonomous-git-workflow](autonomous-git-workflow/SKILL.md)                   | Perform scoped Git, branch, worktree and PR operations under the applicable authorization policy.            |
| [code-review](code-review/SKILL.md)                                           | Review a bounded implementation change through applicable evidence-backed review axes.                       |
| [code-simplification](code-simplification/SKILL.md)                           | Simplify tested code while preserving observable behavior.                                                   |
| [codebase-design](codebase-design/SKILL.md)                                   | Design or assess source layout, module boundaries, dependencies, public surfaces and structural conventions. |
| [codegraph-intelligence](codegraph-intelligence/SKILL.md)                     | Investigate code structure and impact using a verified CodeGraph CLI and project index.                      |
| [context-priming](context-priming/SKILL.md)                                   | Load relevant context when starting, switching or resuming work.                                             |
| [data-impact-analysis](data-impact-analysis/SKILL.md)                         | Analyze persisted-data effects against an existing model and propose approved model changes.                 |
| [database-design](database-design/SKILL.md)                                   | Design an initial relational or document data model for an already selected storage paradigm.                |
| [domain-modeling](domain-modeling/SKILL.md)                                   | Establish or refine technology-independent product language, business rules and domain boundaries.           |
| [evolutionary-architecture-design](evolutionary-architecture-design/SKILL.md) | Evaluate architectural drivers, boundaries, trade-offs and evolutionary decisions.                           |
| [grilling](grilling/SKILL.md)                                                 | Resolve consequential ambiguity through structured rounds of questions.                                      |
| [handoff](handoff/SKILL.md)                                                   | Capture the current work thread and next action for another session or agent.                                |
| [ideation](ideation/SKILL.md)                                                 | Explore and refine an open product idea before requirements are settled.                                     |
| [incremental-implementation](incremental-implementation/SKILL.md)             | Implement nontrivial work through small verified increments.                                                 |
| [prd-writing](prd-writing/SKILL.md)                                           | Turn product requirements and confirmed decisions into a PRD.                                                |
| [spec-writing](spec-writing/SKILL.md)                                         | Specify one feature's observable behavior, rules and acceptance criteria.                                    |
| [systematic-debugging](systematic-debugging/SKILL.md)                         | Reproduce a failure, establish its cause and verify an authorized repair.                                    |
| [tdd](tdd/SKILL.md)                                                           | Derive behavior-focused cases and implement through Red-Green-Refactor.                                      |
| [work-breakdown-planning](work-breakdown-planning/SKILL.md)                   | Decompose outcomes into verifiable work with acceptance coverage and dependencies.                           |

## Resources and Sources

Resource paths start at the selected skill's directory. Read its `SKILL.md` first, then only the references, scripts, templates or data it actually requires. Optional directories vary by skill; do not infer a resource exists from another skill's layout or preload all resources.

For Agenix composition, consult the implementation plan's [reuse boundaries](../docs/agenix-plan.md#2-audit-findings-and-reuse-boundaries) and [workflow mapping](../docs/agenix-plan.md#3-workflow-to-capability-mapping). Those describe planned integration; they do not replace current skill instructions or prove the planned corrections are complete.

The current skills identify `phatnguyen975` as their metadata author and are maintained in this repository under its [root license](../LICENSE). No selected third-party imports have been added yet. When importing a skill, record its upstream repository/directory, exact revision, applicable license and concise adaptation summary here, next to its entry. Keep the applicable upstream `LICENSE` beside its `SKILL.md` and preserve any required attribution/notices for included resources. Repository licensing does not replace third-party terms.

## Maintaining the Index

- Add an entry whenever a skill is created or imported; update it when its name, purpose, scope or source changes. Link the actual `SKILL.md` and explain its trigger concisely.
- Keep entries aligned with directories that exist. Implementation proposals and unimplemented selections belong in the plan, not in the available-skill list.
- Preserve independent capability use. Workflow routing, artifact destinations and publication authority belong in workflow instructions, not in this index.
- Verify links and resource closure after moves or edits. Keep one source index here; do not create separate provenance reports or a README in every skill directory.
