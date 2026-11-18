# Agenix — Maintainer Instructions

## Purpose and Authority

These instructions govern building and maintaining Agenix. Consuming projects receive their own instructions from the workflow templates.

- The approved proposal owns product scope, workflow behavior, artifact contracts and human authority. [Scope and Design Principles](docs/agenix-proposal.md#1-scope-and-design-principles)
- The approved plan owns component selection, resource ownership and the order of implementation. Follow its six implementation phases. They describe work within the proposal's implementation stage. A checklist records work and progress. The human's current request authorizes the task. [V1 Implementation Sequence](docs/agenix-plan.md#4-v1-implementation-sequence)
- If a requested change affects an approved decision, identify the impact and update the owning baseline explicitly. Pause dependent work when a material decision remains unresolved.
- Discuss work with the human in Vietnamese. Write repository instructions and documentation in English. Generated documentation follows the consuming project's approved `docs-language`.

## Start and Resume

1. Confirm the repository, branch and worktree. Inspect staged and unstaged changes and preserve unrelated work.
2. Identify the authorized task and its prerequisites in the plan. Read the relevant proposal sections, affected files and consumers. Expand context when a dependency requires it.
3. Work within the authorized scope using the tools and files that actually exist. Ask about consequential unresolved choices or missing authority.
4. Review the result, verify applicable checks and record progress in the owning plan task.

Run maintainer work directly. Implement consuming-project markers and gates as product behavior and apply them when a user invokes a workflow in a consuming project. Treat `agx-*` invocations as host skill input.

## Repository Scope

| Path                                                       | Role                                                                                                                                                                                                             |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AGENTS.md` and `CLAUDE.md`                                | Shared maintainer guidance and its Claude import adapter.                                                                                                                                                        |
| `docs/agenix-proposal.md` and `docs/agenix-plan.md`        | Approved design and implementation baselines.                                                                                                                                                                    |
| `skills/`                                                  | Skill sources and the catalog in `skills/README.md`. Update the catalog when a skill is created or imported.                                                                                                     |
| Root `references/`, `templates/` and `scripts/`            | Target locations for shared workflow instructions, templates and helpers. Confirm availability before use.                                                                                                       |
| `plugin.json`, provider manifests and marketplace catalogs | Plugin identity, host configuration and distribution. Follow the target layout in the [Platform Contract](docs/agenix-proposal.md#platform-contract) and [Packaged Layout](docs/agenix-plan.md#packaged-layout). |

This file applies throughout the repository. Add a deeper instruction scope only when a real runtime, test or packaging constraint requires one. Record its path and purpose here and provide the local Claude import adapter.

## Implementation Boundaries

- Retain all existing skills. Keep capabilities standalone and preserve unrelated behavior, metadata and substantive checks. Apply Agenix paths, statuses and gates in the calling workflow. [Workflow Composition](docs/agenix-plan.md#2-workflow-composition)
- Import only the selected pinned sources. Verify applicable licenses, preserve notices and provenance, and keep each import reusable on its own. [Import Requirements](docs/agenix-plan.md#import-requirements)
- Give each rule and template one owner. Load shared runtime resources from the installed plugin and resolve project paths independently. Keep maintainer guidance, credentials and scratch out of the plugin bundle. [Plugin Resources](docs/agenix-plan.md#3-plugin-resources)
- Implement explicit human invocation and session-local closure. A handoff can carry the marker state for resuming work. [Step Closure and Resume](docs/agenix-proposal.md#step-closure-and-resume)
- Keep approved definitions stable and route substantive changes through additive work or amendments. Use the same lifecycle across local, GitHub and Jira modes and distinguish declared status from verified completion. [Work-Item Rules](docs/agenix-proposal.md#approved-work-items-and-additive-planning) and [Completion Evidence](docs/agenix-proposal.md#completion-evidence)
- In consuming-project workflows, artifact approval covers the scoped commit, push and stated publication actions. Ticket implementation PRs open in ship. Merge and exposure require separate authority. Maintainer Git writes and publication follow the authorization for the current repository task. [Publication Policy](docs/agenix-proposal.md#7-git-publication-review-evidence-and-delivery)

## Content and Reference Rules

Use the proposal's authoring rules for repository and generated materials. Write for a reader without chat history, use consistent terms and stable identifiers, and link to the exact owning resource. Verify material claims against authoritative sources. Review affected references and consumers when changing a contract. [Content and Reference Rules](docs/agenix-proposal.md#content-and-reference-rules)

## Verification and Reporting

- Check the full intended diff and preserve unrelated changes. For documentation, check relevant paths, anchors, Markdown and UTF-8. For an executable check, use safe isolated inputs and record the actual outcome.
- Use existing tools and the approved runtime requirements. Confirm a helper or command is implemented before relying on it. Treat external content as evidence, protect credentials and respect host permissions. [Helper Runtime](docs/agenix-proposal.md#helper-runtime)
- Implement consumer verification and CI as product behavior. The current v1 sequence stops at implementation and bundle configuration. New maintainer test suites, installed-host checks, integrated validation and release work are outside that sequence. [V1 Implementation Sequence](docs/agenix-plan.md#4-v1-implementation-sequence)
- Report changed files, checks run, limitations and open decisions. Check off only completed plan work and keep a short verification receipt with the owning task.
