# Agenix Implementation Plan

> **Status:** Approved  
> **Updated:** 2026-11-18

The proposal owns workflow behavior and authority. This plan selects the methods, template owners and packaged resources, then orders the work through v1 implementation. Paths proposed here describe target files. Treat the live repository and the installed package as the evidence of what exists.

## 1. Skill Inventory

### Workflow Skills and Usage Guide

| Skill           | Purpose                                                                                              |
| --------------- | ---------------------------------------------------------------------------------------------------- |
| `agx-setup`     | Establish shared project configuration and verify first-time or joining setup.                       |
| `agx-prd`       | Establish the approved product requirements baseline.                                                |
| `agx-feature`   | Allocate product outcomes to a feature catalog and feature records.                                  |
| `agx-architect` | Design the owned domain, technical foundations, conventions and test strategy.                       |
| `agx-scaffold`  | Build and verify the runnable foundation, CI and project-specific operating instructions.            |
| `agx-spec`      | Define feature behavior and applicable public interface, data and UI contracts.                      |
| `agx-plan`      | Choose the feature delivery strategy and plan its tickets.                                           |
| `agx-build`     | Plan and approve a ticket's tasks, then implement and verify the approved batch.                     |
| `agx-review`    | Review the ticket candidate against its specification, checks and applicable quality criteria.       |
| `agx-ship`      | Publish and verify ticket or whole-feature delivery with separate merge authority.                   |
| `agx-guide`     | Explain Agenix on demand, including before project setup. This read-only entry has no workflow step. |

### Imported Capability Skills

The GitHub repository, path and revision identify each selected source. Imported skills follow the same standalone contract as other capabilities.

| Skill                         | Upstream Repository and Path                                            | Pinned Revision                            | Purpose                                                                                                           |
| ----------------------------- | ----------------------------------------------------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| `accessibility`               | `addyosmani/web-quality-skills` · `skills/accessibility`                | `afa8da942115f2961fdbfa80807ea0b232ff6c00` | Evaluate and improve web accessibility with criterion-linked source, browser and manual checks.                   |
| `frontend-design`             | `anthropics/skills` · `skills/frontend-design`                          | `1780c5e5a552fd4d1c9d6a7b0cab26b0c2bef064` | Set and critique a distinctive visual direction suited to the product and its users.                              |
| `playwright-cli`              | `microsoft/playwright-cli` · `skills/playwright-cli`                    | `b21724888b8100b05ef8dee3a92f2bb03bf4dcde` | Operate a browser, replay scenarios and collect browser evidence.                                                 |
| `react-testing`               | `affaan-m/ECC` · `skills/react-testing`                                 | `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b` | Test React components and hooks with observable assertions, isolated providers and network mocks.                 |
| `security-review`             | `affaan-m/ECC` · `skills/security-review`                               | `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b` | Assess relevant security controls around trust boundaries, inputs, authentication, secrets and sensitive actions. |
| `ui-styling`                  | `nextlevelbuilder/ui-ux-pro-max-skill` · `.claude/skills/ui-styling`    | `b6a79003ad2b93c174590a4143a0ddbb2e4574e2` | Implement selected Tailwind or shadcn/ui patterns for tokens, responsive layout and accessible components.        |
| `ui-ux-pro-max`               | `nextlevelbuilder/ui-ux-pro-max-skill` · `.claude/skills/ui-ux-pro-max` | `b6a79003ad2b93c174590a4143a0ddbb2e4574e2` | Look up product-specific styles, palettes, typography, interactions and UX patterns.                              |
| `vercel-composition-patterns` | `vercel-labs/agent-skills` · `skills/composition-patterns`              | `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62` | Design reusable React component APIs, shared state and composition boundaries.                                    |
| `vercel-react-best-practices` | `vercel-labs/agent-skills` · `skills/react-best-practices`              | `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62` | Improve React and Next.js rendering, data fetching and bundle performance for the selected versions.              |
| `vitest`                      | `antfu/skills` · `skills/vitest`                                        | `d524ed287eef22757297827ce42e3cad88abd20c` | Configure and use Vitest assertions, mocks, fixtures, filtering and coverage.                                     |
| `web-design-guidelines`       | `vercel-labs/agent-skills` · `skills/web-design-guidelines`             | `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62` | Review implemented web UI against applicable interface guidelines.                                                |
| `web-perf`                    | `cloudflare/skills` · `skills/web-perf`                                 | `cbf893b954222276bf1af57e5f23379231e0efb9` | Measure and diagnose loading and interaction performance on a runnable web surface.                               |

### Agenix Capability Skills

| Skill                              | Purpose                                                                                         |
| ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| `api-contract-design`              | Design or evolve consumer-visible API, RPC, message and stream contracts.                       |
| `autonomous-git-workflow`          | Execute authorized Git operations with branch ownership, candidate checks and safe recovery.    |
| `code-review`                      | Assess a bounded change and produce evidence-backed findings and coverage.                      |
| `code-simplification`              | Simplify verified code while preserving observable behavior.                                    |
| `codebase-design`                  | Define release units, source boundaries, module ownership and structural tests.                 |
| `codegraph-intelligence`           | Trace structural relationships and potential impact through a usable CodeGraph index.           |
| `context-priming`                  | Load and reconcile the context relevant to starting, resuming or refocusing work.               |
| `data-impact-analysis`             | Assess persistence changes, consumers, compatibility and migration risks against a baseline.    |
| `database-design`                  | Design initial relational or document models and their integrity rules.                         |
| `domain-modeling`                  | Establish business language, concepts, boundaries and invariants.                               |
| `evolutionary-architecture-design` | Evaluate system structures, trade-offs and incremental evolution against architectural drivers. |
| `grilling`                         | Resolve multiple consequential uncertainties through focused questions.                         |
| `handoff`                          | Preserve the evidence, remaining work and next action needed to continue across sessions.       |
| `ideation`                         | Explore meaningful alternatives when a product direction remains open.                          |
| `incremental-implementation`       | Implement and verify dependency-aware increments from an approved plan.                         |
| `prd-writing`                      | Turn stakeholder decisions into traceable requirements, journeys and success measures.          |
| `spec-writing`                     | Specify one feature's rules, states and verifiable acceptance scenarios.                        |
| `systematic-debugging`             | Reproduce, isolate and diagnose failures, then verify authorized repairs.                       |
| `tdd`                              | Derive behavior checks and implement with Red-Green-Refactor.                                   |
| `test-strategy-design` _(planned)_ | Design risk-based verification across owned units, public boundaries and supported targets.     |
| `work-breakdown-planning`          | Decompose scope into verifiable outcomes with hard dependencies and coverage.                   |

## 2. Workflow Composition

**Required** means use the method for new or materially changed work in the applicable step. **Conditional** means use it when the stated technical trigger is present. **Optional** means it can help with a specific gap. A direct step uses its own instructions and the approved project tools. These labels control skill loading. Required checks still apply.

### Shared Support

| Capability                              | When to use it and what to return                                                                                                                                                                                                                                                  |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `context-priming` (conditional)         | At unfamiliar entry, explicit resume or material drift, reconcile the selected step, relevant instructions, baseline and evidence. Return only the context the step needs.                                                                                                         |
| `grilling` (optional)                   | Use focused rounds when several unresolved decisions affect the artifact. Reuse settled choices and capture answers in the artifact they govern.                                                                                                                                   |
| `autonomous-git-workflow` (conditional) | Use for an actual branch/worktree, commit, push, PR, safe reconciliation or authorized merge operation. Supply the exact scope and candidate. The shared Agenix publication rule controls the gate and timing.                                                                     |
| `systematic-debugging` (conditional)    | Use reproduction and isolation for unexpected failures or regressions. Return diagnosis and evidence to the active step. During review or ship, diagnosis does not authorize product fixes. An expected test-first RED needs no debugging route.                                   |
| `codegraph-intelligence` (optional)     | Use for structural or change-impact questions during architecture amendments, planning, build or review only when the project has selected CodeGraph and the relevant worktree has a verified CLI and usable index. Validate findings against the source and keep required checks. |
| `handoff` (conditional)                 | Use when work transfers to another session or owner. Supply `.agenix/HANDOFF.md` as the destination, with open or ended marker state, pending work and evidence links. Never infer new approval from the handoff.                                                                  |

### Setup, Product and Feature Catalog

| Step                  | Method and workflow-owned output                                                                                                                                                                                                                  |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agx-setup configure` | Direct. Establish scope, settings, helper binding, managed instructions, ignores and bootstrap CI. Use only the selected tracker adapter.                                                                                                         |
| `agx-setup verify`    | Direct. Verify actual prerequisites, permissions and tracker mappings. For a joining user, read merged configuration and establish only required personal state.                                                                                  |
| `agx-prd define`      | **Required** `prd-writing` for product elicitation, traceable requirements and measurable outcomes. **Optional** `ideation` when the direction is still open. Feed evaluated options back into the PRD rather than creating an idea file.         |
| `agx-feature define`  | Direct catalog, ID, coverage and dependency work. **Conditional** `work-breakdown-planning` in `Flat` for an undecided outcome split. Adapt the results to feature records. Reuse approved feature boundaries and skip the standalone slice plan. |

### Architecture

| Step                        | Method and workflow-owned output                                                                                                                                                                                                                                                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agx-architect domain`      | **Required** `domain-modeling` for language, business rules, workflows and relevant model validation. Load strategic or tactical methods only where useful. Produce the domain model.                                                                                                                                                                         |
| `agx-architect system`      | **Required** `evolutionary-architecture-design` where system design applies. Use drivers, alternatives, relevant views and fitness criteria for owned technical boundaries. Record significant decisions as ADRs.                                                                                                                                             |
| `agx-architect stack`       | Direct compatibility and prerequisite analysis. **Conditional** `evolutionary-architecture-design` for consequential comparisons or client architecture decisions. Own the tech stack, verified tool requirements and applicable Client Design section.                                                                                                       |
| `agx-architect data`        | **Required for relational or document design** `database-design`. Match the selected model and cover access patterns, integrity and lifecycle. Use direct store-specific guidance for an approved unsupported model. Output the initial design and ownership rules.                                                                                           |
| `agx-architect ui`          | **Required** `frontend-design` for a new visual direction. **Conditional** `ui-ux-pro-max` for targeted design research, `ui-styling` for the selected styling stack, and `accessibility` for criterion-specific evaluation. **Required** `playwright-cli` for the initial browser demonstration. Publish one global written UI design and its verified demo. |
| `agx-architect conventions` | Direct synthesis of approved design choices, applicability and enforcement intent. **Conditional** `codebase-design` for structural rules, `api-contract-design` for shared interface conventions, and security or accessibility specialists for a specific approved concern. Write only applicable convention files.                                         |
| `agx-architect tests`       | **Required** `test-strategy-design` for risk, boundary, level, tool, environment and evidence choices across units. **Optional** `tdd` test design techniques for case selection. Inspect tool-specific references only for decisions that need them. Write the strategy before implementing harnesses.                                                       |

### Scaffold

| Step                        | Method and workflow-owned output                                                                                                                                                                                                                                                                                                                    |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agx-scaffold structure`    | **Required** `codebase-design` in design mode. Bind approved release units, public surfaces, dependency directions, instruction scopes and source/test locations to a concrete layout.                                                                                                                                                              |
| `agx-scaffold runtime`      | Direct. Create the source and toolchain skeleton, application configuration, safe environment examples and selected application container build/run configuration. Verify service-independent commands. **Conditional** `incremental-implementation` for nontrivial behavior-bearing work and `tdd` for test-first behavior.                        |
| `agx-scaffold services`     | Direct. Wire approved disposable dependencies, including Compose or equivalent orchestration when selected. Verify startup, readiness, isolation, reset and applicable initial migrations. **Conditional** implementation methods for support code with its own behavior. Omit when inapplicable.                                                   |
| `agx-scaffold tests`        | Direct harness wiring and proof of meaningful discovery and failures. **Conditional** `vitest` for the chosen compatible runner, `react-testing` for supported React component/hook checks, and `playwright-cli` for browser proof. Use `tdd` for authored test-first probe behavior when appropriate. Use the selected schema validators directly. |
| `agx-scaffold ci`           | Direct. Generate CI from verified operations and prove the approved failure/restoration sequence on the draft PR. Configure an optional project Git pre-commit hook only for selected fast checks. Keep required checks in CI.                                                                                                                      |
| `agx-scaffold instructions` | Direct. Use the verified layout, commands, service and CI evidence to finalize root/scoped `AGENTS.md`, Claude adapters, README and `environment.agenix.json`. Record allowed, approval-required and disallowed operations per environment. Verify scope resolution and actual enforcement, then present the complete scaffold for final approval.  |

`setup configure` supplies the root guardrails and `agx-guide` entry point used during scaffold. `structure` selects the scopes, and `instructions` binds them to verified operations. This final step checks the complete candidate, publishes it to the same scaffold PR and verifies final-head CI before a separately authorized merge.

### Feature Specification

| Step                | Method and workflow-owned output                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agx-spec behavior` | **Required** `spec-writing` for rules, states, acceptance scenarios and traceability. **Conditional** `domain-modeling` for a real semantic gap via the amendment route. Record exposure and real-boundary acceptance in the feature spec.                                                                                                                                                                                                           |
| `agx-spec api`      | **Conditional** `api-contract-design` for supported owned interactions or substantive compatibility analysis. Select the applicable protocol/reference and schema version. Pin an unchanged external contract directly. Use direct guidance for other public surfaces.                                                                                                                                                                               |
| `agx-spec data`     | **Required for supported impact analysis** `data-impact-analysis`. Pin the integrated schema/migration baseline, trace affected consumers and record migration prerequisites, compatibility and verification. Use direct model-specific analysis where unsupported. The step records intent and leaves migration scripts to implementation.                                                                                                          |
| `agx-spec ui`       | **Conditional** `frontend-design` for unresolved visual direction, `ui-ux-pro-max` for feature-specific flows or interaction choices, and `ui-styling` for selected styling. **Required** `playwright-cli` for initial prototype checks. **Conditional** `accessibility` for applicable criteria requiring specialist evidence. Inherit the approved global design and publish the written UI contract with the initial verified prototype revision. |

### Planning, Build and Review

| Step                             | Method and workflow-owned output                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agx-plan <feature-id> strategy` | Direct. Compare delivery boundaries, ownership, safe exposure and real integration. **Conditional** `work-breakdown-planning` in `Flat` when viable delivery slices or their dependencies need exploration. Record the chosen strategy once.                                                                                                                                                                                                               |
| `agx-plan <feature-id> tickets`  | **Required** `work-breakdown-planning` in `Flat` for the ticket set or approved additions. Map coverage and hard dependencies into feature and ticket records. Keep real integration in the initial delivery scope.                                                                                                                                                                                                                                        |
| `agx-build <ticket-id> plan`     | **Required** `work-breakdown-planning` in `Recursive` for executable tasks. **Optional** `tdd` case-design references for test selection. Map leaves to task IDs, dependencies, acceptance and check IDs. Preserve approved definitions during additions. Commit and push the local ticket record or create verified GitHub sub-issues/Jira sub-tasks and record mappings separately from the approved parent definition.                                  |
| `agx-build <ticket-id> run`      | **Required** `incremental-implementation` for nontrivial implementation and `tdd` for approved test-first behavior. Use selected test and UI methods only for the affected surfaces. **Optional** `code-simplification` for a concrete improvement within passing coverage. Verify and publish the approved batch on the ticket branch. Defer human-only and PR-dependent checks to their owning steps.                                                    |
| `agx-review <ticket-id> assess`  | **Required** `code-review` for implementation, using sequential applicable axis passes on the same candidate. **Conditional** `spec-writing`, `api-contract-design` or `data-impact-analysis` for substantive findings about the corresponding contract. Route UI specialists by their evidence boundary below. Consolidate findings and manual checks into one decision, then route new tasks to `build plan` and existing approved tasks to `build run`. |

### Delivery and Guide

| Step                        | Method and workflow-owned output                                                                                                                                                                                                                                                                                                                               |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agx-ship <ticket-id> run`  | Direct candidate, task, PR/CI, merge and closure checks. **Conditional** `autonomous-git-workflow` for authorized Git operations and `systematic-debugging` for diagnosis. Open the implementation PR here, reconcile PR-dependent checks and verify the actual merge and required post-merge results.                                                         |
| `agx-ship <feature-id> run` | Direct delivery-set checks, reruns and whole-feature acceptance on the integrated baseline. **Conditional** `autonomous-git-workflow` for authorized Git operations or a declared verification specialist for a concrete evidence gap. Publish the Git-owned completion record, verify merge and post-merge results, and keep any exposure authority separate. |
| `agx-guide`                 | Direct read-only orientation. Answer using the workflow map and relevant step/rule references. This entry can be selected on demand by the agent, requires no setup or step marker, and is authored after workflows stabilize.                                                                                                                                 |

### UI Composition by Stage

| Stage                     | Design, implementation and evidence boundaries                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Global design             | `frontend-design` leads. Use `ui-ux-pro-max` to compare targeted product, style, palette, typography or interaction options when a decision remains open. Reconcile options into one approved direction, token set and interaction model. Use `ui-styling` only for relevant selected Tailwind or shadcn/ui techniques. Replay relevant layouts and interactions on the declared browser/viewports with `playwright-cli`. |
| Initial feature prototype | Start from approved behavior, wire examples and global UI foundations. Use `frontend-design` only for unresolved design choices, and `ui-ux-pro-max` for specific feature states, flows or usability gaps. Use deterministic mocks and reset/replay. Demonstrate the written contract with browser evidence before approval.                                                                                              |
| Production build          | Implement the approved written contract and verify the actual client. Use `ui-styling` for selected styling, `vercel-composition-patterns` for a real reusable React API/state boundary, and `vercel-react-best-practices` for relevant React/Next.js rendering, fetch or bundle work. Preserve historical demo code.                                                                                                     |
| Tests and review          | Use `vitest` only where selected and version-compatible. Use `react-testing` for supported component/hook checks with the selected Vitest or Jest harness. Use `playwright-cli` to explore, replay and collect browser evidence. Persist asserted production checks through the approved test harness. DOM simulation does not establish real-browser behavior.                                                           |
| Specialist findings       | Use `web-design-guidelines` for changed implemented UI, `accessibility` for applicable criterion-specific or manual checks, `web-perf` for declared measurement or a real regression, and `security-review` for sensitive owned surfaces. Select relevant compatible React rules and reuse valid evidence. Return findings to the existing review axes. Automated scans and lab traces have bounded scope.                |

Bind browser tools in the applicable stack, strategy and environment records. A missing required tool blocks its check. Select one runner per test unit, and verify the installed version against the imported reference before using an API. Approved runner, tool or framework changes belong to the owning workflow. Do not install optional tooling merely because an import mentions it.

### Template Ownership

Reuse source templates in place when they cover the approved output. A step supplies the destination, required fields or references and applicability rules. Method-only routes return information to the owning record. A template becomes shared when multiple steps instantiate or update its structure, rather than merely reading the generated output.

| Output                            | Source or owner                                                                                                    | Binding                                                                                                                                                                                                                                                   |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Product PRD                       | `prd-writing/references/prd-template.md`                                                                           | Write `docs/PRD.md`. Bind stable requirement and journey IDs and preserve actual approval state.                                                                                                                                                          |
| Domain model                      | `domain-modeling/assets/domain-model-template.md`                                                                  | Write `docs/blueprint/domain-model.md` with the applicable model sections.                                                                                                                                                                                |
| System design and ADRs            | `evolutionary-architecture-design/assets/system-design-template.md` and `assets/adr-template.md` in the same skill | Write the system blueprint and significant decisions under `docs/blueprint/decisions/`. Include applicable views and drivers.                                                                                                                             |
| Initial database design           | `database-design/assets/database-design-sql.md` or `database-design-nosql.md` in the same directory                | Use the asset compatible with the selected relational or document model and write `docs/blueprint/database-design.md`.                                                                                                                                    |
| Codebase design                   | `codebase-design/assets/codebase-design-template.md`                                                               | Bind the approved layout, verification references and instruction scopes in `docs/blueprint/codebase-design.md`.                                                                                                                                          |
| Test strategy                     | Planned generic template owned by `test-strategy-design`                                                           | Bind `docs/blueprint/test-strategy.md` to project units, modes and evidence. Scaffold supplies concrete commands.                                                                                                                                         |
| Feature behavior                  | `spec-writing/references/spec-template.md`                                                                         | Bind the feature-ID path and stable acceptance anchors. Use the selected acceptance notation and reference separate owned contracts.                                                                                                                      |
| API and data impact               | Protocol assets under `api-contract-design/assets/` and `data-impact-analysis/assets/data-impact-template.md`      | Use protocol assets as compatible examples or starting fragments. Write the canonical owned contract paths and feature `data-impact.md` with the baseline and verification obligations. Use the spec or short residual API prose for uncovered semantics. |
| Feature, ticket and task records  | `templates/records/{feature,local-ticket}.json` and `templates/records/{native-ticket,native-task}.md`             | Write `feature.agenix.json` in every mode. Render each local ticket with a `tasks` array. Render remote tickets and tasks as Markdown on GitHub and corresponding ADF on Jira.                                                                            |
| Project instructions              | `templates/instructions/{root-agents,scoped-agents,claude-adapter}.md`                                             | Setup adds usage and baseline guardrails. Scaffold finalizes root and scoped guidance. Root instructions reference the managed configuration and environment files as they become available.                                                              |
| Checkpoints and handoff           | `templates/evidence/checkpoint.json` and `templates/evidence/{checkpoint,handoff}.md`                              | Embed JSON checkpoints in Git records or render readable tracker or PR comments. Handoffs use Markdown and session-local markers. Keep full standalone review and TDD outputs out of the composed path unless explicitly requested.                       |
| Feature catalog                   | `agx-feature/assets/feature-catalog.json`                                                                          | Write `docs/features/catalog.agenix.json` with feature IDs and paths. Read coverage from the referenced feature records.                                                                                                                                  |
| Stack and conventions             | `agx-architect/assets/{tech-stack,convention}.md`                                                                  | Include Client Design when applicable. Keep convention rules distinct from verified environment commands.                                                                                                                                                 |
| Global and feature UI             | `agx-architect/assets/ui-design.md` and `agx-spec/assets/ui-prototype.md`                                          | Render each as the README of its respective design directory. Keep the initial demo with its written design. Preserve one approved global token source and one written feature contract.                                                                  |
| Bootstrap CI and Jira placeholder | `agx-setup/assets/agenix-artifacts.yml` and `jira-credentials.json` in the same directory                          | Write approved bootstrap config and initialize the private empty credential file only where required.                                                                                                                                                     |
| Application CI                    | `agx-scaffold/assets/agenix-application.yml`                                                                       | `scaffold ci` binds verified project commands to selected CI lanes. The optional project Git hook uses the chosen existing runner or project commands.                                                                                                    |
| Project configuration             | `agx-setup/assets/config.json`                                                                                     | Setup writes root `config.agenix.json`.                                                                                                                                                                                                                   |
| Environment record                | `agx-scaffold/assets/environment.json`                                                                             | `scaffold instructions` binds verified units, commands, services, permissions and evidence in root `environment.agenix.json`. README exposes the corresponding verified setup and run instructions.                                                       |
| Runtime and service configuration | Approved project toolchain                                                                                         | `runtime` owns app settings and standalone build/run definitions. `services` owns service integration and orchestration. Use stack-native formats and project-owned files.                                                                                |

## 3. Plugin Resources

### Packaged Layout

```text
agenix/
├── plugin.json                      portable manifest with extensions.com.openai
├── .claude-plugin/plugin.json
├── .antigravity-plugin/plugin.json
├── .agents/plugins/marketplace.json distribution catalog for Codex discovery
├── skills/
│   ├── README.md                    installed skill and provenance index
│   ├── <capability>/
│   │   ├── SKILL.md
│   │   ├── LICENSE                  required for an import
│   │   └── assets/, references/, scripts/ as used
│   ├── agx-<phase>/
│   │   ├── SKILL.md                workflow overview and explicit step router
│   │   ├── agents/openai.yaml       Codex skill metadata
│   │   ├── references/<step>.md    selected step procedure
│   │   └── assets/, scripts/       private resources only where needed
│   └── agx-guide/SKILL.md            on-demand entry with focused references if useful
├── references/
│   ├── workflow-control.md          invocation, scope, gates, re-entry and handoff
│   ├── work-items-and-evidence.md   identity, lifecycle, readiness and completion
│   ├── git-publication.md           branches, revision evidence, PRs, CI and merge
│   ├── project-content.md           project authoring, ownership and instruction scopes
│   └── trackers/
│       ├── local.md                 local records, status and Git/verifier operations
│       ├── github.md                native issue mappings, status and GitHub CLI operations
│       └── jira.md                  native issue mappings, status and Jira helper operations
├── templates/
│   ├── instructions/                root, scoped and Claude adapter templates
│   ├── records/                     JSON configuration and records, Markdown native drafts
│   └── evidence/                    JSON checkpoints and Markdown comments or handoffs
└── scripts/
    ├── validate-artifacts.py        stage-aware structural checks for every tracker
    ├── verify-status.py             read-only local status and evidence verification
    ├── jira.py                      selected Jira read/write operations
    └── agenix_helpers/              shared parsing, paths, Git/CI and evidence logic
```

The layout describes the intended bundle and its catalog. Include required runtime resources and notices. Keep the proposal, implementation plan, maintainer instructions, record schema specification, scratch, real credentials and development fixtures outside the runtime package. The approved layout uses the root OpenAI extension instead of the existing Codex compatibility overlay. The guide is loaded on demand. No startup hook is needed.

Each workflow entry validates arguments and item type, shows step order and selects the procedure. The procedure owns the selected step's inputs, actions, methods, outputs, checks, approval batch and completion. Keep a rule in the step when it applies only there.

| Workflow                    | Files under `references/` in the skill                                                 |
| --------------------------- | -------------------------------------------------------------------------------------- |
| `agx-setup`                 | `configure.md`, `verify.md`                                                            |
| `agx-prd` and `agx-feature` | `define.md` in each skill                                                              |
| `agx-architect`             | `domain.md`, `system.md`, `stack.md`, `data.md`, `ui.md`, `conventions.md`, `tests.md` |
| `agx-scaffold`              | `structure.md`, `runtime.md`, `services.md`, `tests.md`, `ci.md`, `instructions.md`    |
| `agx-spec`                  | `behavior.md`, `api.md`, `data.md`, `ui.md`                                            |
| `agx-plan`                  | `strategy.md`, `tickets.md`                                                            |
| `agx-build`                 | `plan.md`, `run.md`                                                                    |
| `agx-review`                | `assess.md`                                                                            |
| `agx-ship`                  | `ticket-run.md`, `feature-run.md`, selected by item type                               |

### Shared Reference Ownership and Routing

Each shared reference covers one cohesive responsibility and reads on its own. Only `agx-*` instructions route to shared references, templates and helper entry points. The workflow entry or selected step names each resource and applicable section directly. Shared references contain no links to other packaged resources.

| Shared Reference             | Owns                                                                                                                                                                                                            | Workflow Use                                                                                                                                                                                                                                                                                                                                                    |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workflow-control.md`        | Invocation, scope and prerequisite handling, step markers, artifact gates, amendments, resume and handoff.                                                                                                      | Workflow entry and step lifecycle across setup through ship. Read amend/resume sections only on those routes. The guide can load the relevant section for usage questions.                                                                                                                                                                                      |
| `work-items-and-evidence.md` | IDs and dependencies, frozen definitions and additive work, status semantics, verification modes, completion criteria and overrides. Owns shared remote item shape and common read-back and retry expectations. | `feature define` for feature IDs and dependencies, `spec behavior` for feature readiness, `plan strategy/tickets` for delivery coverage and ticket planning, and `build plan/run`, `review assess` and both ship routes for the selected item's checks. Setup reads the shared requirements its selected tracker must satisfy.                                  |
| `git-publication.md`         | Branch and PR ownership, candidate-to-revision binding, approved writes, PR/CI evidence, merge authority, post-merge recovery and release authority.                                                            | Publishing steps use only the branch, commit/push and PR rules they need. `setup verify` reads applicable repository prerequisites, `scaffold ci` reads failure/restoration rules, `review assess` binds the decision to its candidate, and ship reads merge and closure rules. Feature ship reads exposure rules only where applicable.                        |
| `project-content.md`         | Documentation language, authoring, paths, artifact ownership and managed project instructions, including private workspace boundaries.                                                                          | `setup configure` for configuration, ignores and root instructions, `scaffold structure` for scope selection, and `scaffold instructions` for verified operations and guardrails. Document-producing steps load applicable authoring and ownership sections. Helper resolution and execution belong to the calling workflow instructions and helper interfaces. |

Load a tracker reference only when the step reads or writes that mode's ticket/task data, or verifies its setup. The feature record stays in Git in every mode. When feature ship verifies ticket closure, it loads the selected adapter for that check.

| Tracker Reference    | Mode-Specific Guidance                                                                                                                                                                                                                                         |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `trackers/local.md`  | Explain canonical ticket files and embedded task records, working-branch versus merged state, edit reconciliation and prospective versus verified `DONE`. Explain what Git, `gh` and `verify-status.py` verify and how to interpret missing or stale evidence. |
| `trackers/github.md` | Explain required CLI authentication and repository permissions, issue and sub-issue mappings, labels and native states, batch creation, paginated reads and verified closure using `gh`.                                                                       |
| `trackers/jira.md`   | Explain project, issue-type and transition discovery, private credential setup, issue and sub-task mappings, labels and native transitions, and how to read back or reconcile writes through `jira.py`.                                                        |

The principal tracker routes are `setup configure/verify`, `plan tickets`, `build plan/run`, `review assess` and `ship run` for both item types. Each loads the selected adapter together with the applicable shared work-item rules. The adapter explains what its tool needs, what it returns and what to do on partial or ambiguous results. The calling step resolves and invokes the actual tool or helper and supplies approved write scope and project inputs.

Use the approved design as input when writing a shared guide. Organize the guide around what the caller needs to know, decide, do and verify. Keep workflow-specific sequences, examples and template bindings in the owning skill.

### Resource Resolution and Helper Boundaries

Resolve resources from the actual installed skill directory or a verified host-provided plugin root. Require the resolved paths to belong to the expected installation and match the approved version. Host-specific metadata may supply a root hint. Do not assume a single environment variable exists in every host or shell. Report unresolved resources or version mismatches before running a dependent operation.

Run packaged Python entry points with the verified interpreter. Pass the absolute project root explicitly. Pass declared input/output paths and item IDs as operation arguments. Paths must resolve within their intended roots. Keep the installed directory read-only, use argument vectors and leave host permission checks in effect. For example, the planned entry point takes this form:

```text
python "<installed-plugin>/scripts/verify-status.py" --project-root "<project-root>" --item "<id>"
```

Final argument names belong to the helper interface. Jira may take the credentials **file path** as an argument. Validate that it matches the approved private location under the selected project root, and let only the helper read it. Never put token values in arguments, model context or diagnostics. Do not generalize the path argument into a credential lookup or fallback mechanism.

- `validate-artifacts.py` checks managed non-secret records and paths. `verify-status.py` reads local tracker records and necessary Git/PR/CI evidence. Neither runs product tests, publishes changes or approves work.
- `jira.py` performs scoped REST operations with sanitized results and read-back. Use approved `gh` operations for GitHub. Any deterministic reconciliation code belongs with shared helpers if multiple steps use it.
- Put configuration, record validation, candidate binding and evidence code in the shared package. Read Git-owned `*.agenix.json` records directly as strict JSON and reject duplicate keys. Use readable sections for remote issue bodies and checkpoints, rendered as Markdown on GitHub and ADF on Jira. A skill's own `scripts/` contains code used only there.
- The consuming project retains generated artifacts, scope instructions, configuration, CI wiring and private state. Provision the reviewed helper revision in a disposable CI tool directory, using an immutable pin and verified repository access. Keep helper code in the plugin distribution.

Installed resource lookup and pinned CI provisioning remain unverified until checked on the actual targets. The implementation sequence below ends with the complete source and distribution configuration. Host installation and integrated validation follow separately.

### Import Requirements

Keep each import standalone under `skills/<name>/`. Preserve the pinned upstream revision, actual resource dependencies, source terms and notices. Place `LICENSE` beside `SKILL.md`. Set the frontmatter `license` to the verified terms and add or preserve `metadata.author` using verified upstream attribution. Preserve other valid upstream metadata and record local adaptations and provenance in `skills/README.md`.

Resolve licensing inconsistencies before vendoring. The selected `ui-styling` revision has Apache-2.0 terms in its skill license file and a conflicting MIT frontmatter value. Preserve the actual terms and align the frontmatter. Verify license coverage for each Vercel import and for any separately sourced rule content. In particular, pin and verify the guideline source loaded by `web-design-guidelines` instead of fetching floating rules at runtime.

Keep adaptations bounded to portable lookup, accurate version and scope, and caller-owned output. Retain needed scripts, data and references, and remove assumptions about an upstream suite or permissions it granted. Document the dependency and version boundaries for each route. Do not authorize dependencies, network access, style changes or unrelated reports through an import's default instructions.

## 4. V1 Implementation Sequence

Use the existing repository and tools. Follow the phases in order, and use the routes, template owners and resource layout above when implementing a step. Each phase ends when its listed implementation outputs are present and connected. Track unfinished work in the owning phase.

The endpoint is **v1 implementation complete**, with the source, runtime resources and distribution configuration assembled. The consumer CI and verification flows specified in the proposal are part of the product to implement. Maintainer install checks, integration runs, new test suites, evals and release work are outside this sequence.

### Phase 1 - Shared Workflow Contracts and Helpers

- [x] Sync the maintainer instructions with the approved proposal and this plan before using them to implement workflows. Reuse the existing instruction entry points and remove obsolete section and phase links.
  - Verified maintainer instruction alignment, Markdown, UTF-8, the 14 document links and the existing Claude import.
- [x] After human confirmation, author the shared guides using the ownership and workflow routes in Section 3. Verify each guide is self-contained and each tracker guide explains its records, status handling, supported operations and tools.
  - Reviewed all seven guides against their intended routes, including step closure, handoff and baseline amendments. UTF-8, Markdown and resource-boundary checks passed. GitHub CLI options were checked with installed help and Jira operations against the REST documentation.
- [x] Define the configuration and record schemas for features, tickets, tasks, approvals and verification receipts. Specify storage by tracker mode, immutable fields, IDs, parentage, dependencies and when each field becomes required. Define the mapping from shared fields to remote issue bodies, native metadata and checkpoints.
  - Maintainer approved `docs/record-schema.md` after review. Checked work-item ownership, stage requirements, record paths, UTF-8, four JSON examples and two matching remote Markdown examples.
- [ ] Create and settle the shared instruction, record and evidence templates from the approved schemas. Use valid JSON templates for Git-owned records and validate their rendered types against the schema. Cover the complete field set in the authoring guidance and mark local-only, remote-only, conditional and later-stage fields. Produce representative records from the templates for the applicable tracker modes and stages. Keep valid samples and copies with deliberate errors for isolated helper checks.
- [ ] Implement contained resource and project path resolution, strict record parsing, definition and candidate binding, and shared Git/PR evidence reads. Verify these against the template-derived samples as part of implementation. Keep unresolved prerequisites distinguishable from failed verification.
- [ ] Implement `validate-artifacts.py` and the read-only `verify-status.py`. Run both during implementation against valid and invalid template-derived records in isolated fixtures. Keep declared state, candidate validity, verified completion and dependency readiness separate. Neither helper runs product tests or writes status.
- [ ] Implement shared tracker operations. Use `gh` for GitHub and the root Jira helper for approved REST actions. Verify against representative template-derived remote drafts and isolated tracker responses. Handle parent links, pagination, partial outcomes, read-back and duplicate avoidance. Keep credential access and sanitized diagnostics inside the Jira helper.

When implementing the workflow steps in later phases, verify that each step selects the correct template and supplies the fields for its tracker mode and stage.

### Phase 2 - Capability Preparation

- [ ] Use the 20 existing capabilities where mapped. Preserve their standalone behavior and metadata. Limit any change to a concrete composition blocker in their actual route.
- [ ] Create `test-strategy-design` with a standalone method and template for risks, verification boundaries, levels, tooling, environments and evidence. Bind it to the project-specific output only in `agx-architect tests`.
- [ ] Vendor the 12 pinned imports with their required resources and verified licenses. Preserve notices and authorship. Resolve the import requirements above before including the affected content. Keep the choices pinned and record provenance in the skill index.
- [ ] Make the selected imports usable in their assigned roles. Keep design, styling, browser execution and specialist review separate. Adapt caller paths and output, document runner/browser prerequisites, and prevent imported defaults from expanding project scope or permissions.

### Phase 3 - Project and Architecture Foundations

- [ ] Implement `agx-setup configure` and `verify`. Write `config.agenix.json`, root scope and authority reminders, bootstrap CI and the guide pointer. Handle first setup and joining separately, including private Jira initialization only when applicable.
- [ ] Implement `agx-prd define` and `agx-feature define`. Bind product requirements and journey IDs to the feature catalog, per-feature records and feature dependencies.
- [ ] Implement `agx-architect domain`, `system` and `stack`. Select applicable system or client design, retain significant decisions, and bind chosen tools and targets.
- [ ] Implement `agx-architect data` and `ui` where applicable. Bind owned persistence decisions and the global UI design and demonstration. Route design, browser and accessibility methods according to Section 2.
- [ ] Implement `agx-architect conventions` and `tests`. Deliver approved conventions and a test strategy across owned units. Leave concrete harness commands and runtime evidence to scaffold.

### Phase 4 - Runnable Scaffold and Feature Contracts

- [ ] Implement `agx-scaffold structure` and `runtime`. Resolve concrete release units, source and test paths, instruction scopes, application configuration and the runnable skeleton.
- [ ] Implement `agx-scaffold services` and `tests`. Wire only applicable disposable services and migration prerequisites. Implement procedures for harness setup, test discovery, meaningful failure and restored success.
- [ ] Implement `agx-scaffold ci` and `instructions`. Generate consumer CI from verified commands, support the controlled failure/restoration sequence, and finalize README, scoped instructions and per-environment permissions. Keep final scaffold publication and its separate merge decision at `instructions`.
- [ ] Implement `agx-spec behavior`, `api`, `data` and `ui`. Preserve one behavior baseline and select the applicable owned interfaces, persistence impact and UI contract. Bind feature prototypes to approved interactions and keep historical prototype code separate from production maintenance.
- [ ] Implement `agx-plan strategy` and `tickets` for a feature. Record delivery boundaries, exposure constraints and real integration coverage. Publish local records or verify remote mappings under the approved feature plan.

### Phase 5 - Ticket Execution and Delivery

- [ ] Implement `agx-build plan`. Turn the approved ticket into a dependency-ordered task plan with explicit acceptance and verification. Commit and push the local ticket record or create verified native children with a linked plan checkpoint.
- [ ] Implement `agx-build run`. Execute the approved batch using selected verification methods, record actual evidence and commit and push after approval. Handle partial handoff, manual checks and PR-dependent evidence through their owning stages.
- [ ] Implement `agx-review assess`. Bind findings, manual judgments and review evidence to the candidate before shipping. Route fixes to the current approved tasks or to additive planning. Persist evidence on the branch or tracker as applicable.
- [ ] Implement ticket `agx-ship run`. Verify publication readiness, open or update the implementation PR, reconcile final-head checks, obtain separate merge authority and verify actual closure. Support resuming a human merge and preserve original and repair evidence for linked post-merge work.
- [ ] Implement feature `agx-ship run`. Verify the merged ticket set, run the applicable ticket and whole-feature checks against the integrated baseline, publish the Git-owned completion record and verify its merge. Bind optional exposure to its own authorization.
- [ ] Connect additive work, amendments, cancellation, overrides and interrupted publication to the affected routes. Preserve prior definitions and evidence. Keep the three trackers on the same lifecycle and completion contract.

### Phase 6 - Guide and Bundle Assembly

- [ ] Complete `agx-guide` from the stable routers and shared rules. Cover first use, step selection, approval, resume and common tracker or scope questions on demand.
- [ ] Complete all three manifests, Codex discovery metadata and the marketplace entry. Include the shared resources, selected skills, helpers, templates and notices in the configured bundle. Keep development-only material outside it.
- [ ] Update the README and skill index for the delivered use, routes and prerequisites. Describe installed-host behavior as pending confirmation where it has not been exercised.
- [ ] Review the final source inventory against this plan. Resolve missing handlers, dangling resource routes, unused duplicates and any unfinished v1 implementation. Record the implementation checkpoint and end this plan here.
