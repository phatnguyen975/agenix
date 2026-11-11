---
name: codebase-design
description: Design, review, document, and incrementally improve codebase structure across languages and frameworks. Use for repository layout, package or module boundaries, feature versus layer organization, dependency direction, public interfaces, shared libraries, code conventions, test placement, structural enforcement, and migration plans; also use for targeted structural reviews of existing projects. Not for system architecture style, deployment topology, database or API schema design, UI visual design, or feature implementation.
metadata:
  author: phatnguyen975
  version: 1.0
---

# Codebase Design

## Purpose and Scope

Design the **source-code organization** of new or existing codebases so that responsibilities, ownership, boundaries, dependencies, tests, and change paths are discoverable and maintainable. Handle full designs, focused reviews, document updates, and incremental restructuring. The result must follow the actual project's supported conventions and constraints, not a universal folder tree.

**In scope:** repository grouping, build/release unit placement, module decomposition, internal organization patterns, public surfaces, static dependencies, shared code, boundary-facing conventions, test placement, structural enforcement, and migration steps.

**Out of scope:** choosing deployment topology or system architecture; inventing domain models or business rules; database/API contract contents; UI appearance; feature implementation; full test strategy or coverage targets; formatter and tool tutorials. Treat established upstream decisions as inputs and flag any conflict affecting code organization rather than silently redesigning those domains.

## Operating Modes

- **Design:** propose a new or substantially revised source structure from requirements and evidence. Produce a full document only when requested.
- **Review:** inspect existing structure and return evidence-backed findings or recommendations; do not assume authorization to edit files.
- **Update:** change only affected parts of an approved design/document. Preserve existing names, paths, boundaries, and rule IDs unless the change is justified and approved.
- **Restructure:** establish current-to-target differences and plan incremental migration; implement only when explicitly requested.

Modes may be combined, but only run steps relevant to the requested scope. Design intent does not imply permission to create a document; a migration plan does not imply permission to change production code.

## Inputs and Evidence

Gather enough evidence for the **affected decisions**, not an exhaustive inventory of every file:

- **Requirements and forces:** capabilities/responsibilities, consumers, independently changing concerns, complexity, testability, ownership, delivery coordination, and structural risks.
- **Actual boundaries:** existing repositories, build targets/packages, release units, module entry points, public consumers, and release/compatibility obligations.
- **Project authority:** explicit user requirements; repository/agent instructions; manifests and supported language/framework rules; existing architecture/domain/codebase documents; established conventions and working constraints.
- **Existing state:** source/test trees, imports and build references, public exports, ownership metadata, checks, observed violations, and relevant change history when available.

Mark material information as **Observed**, **Specified**, **Proposed**, or **Unverified**. Do not fabricate release independence, owner, consumer, language/framework version, path, rule, or check result. When an unknown materially changes a choice, ask a focused consolidated question or present explicitly provisional alternatives; do not silently finalize an assumption. Do not request information already supplied by the project.

## Terminology

| Term                   | Meaning                                                                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Repository             | Version-control boundary; does not by itself define builds or release cadence.                                                                                                 |
| Build Target / Package | Unit recognized by a build/package system; not necessarily distributed independently.                                                                                          |
| Release Unit           | Application, service, library, or tool distributed, published, or deployed as one identifiable unit; can contain several build targets.                                        |
| Module                 | Cohesive architectural source boundary owning a responsibility and hiding decisions; can be implemented by packages, exports, namespaces, assemblies, or enforced directories. |
| Public Interface       | Intended surface visible to the module's authorized consumers; internal-only code need not expose a cross-module API.                                                          |
| Contract               | Consumer-visible agreement between independently evolving units (published package API or protocol); its detailed contents are out of scope.                                   |
| Dependency             | Directed **static** import/type/build edge unless explicitly called runtime interaction, data flow, or deployment dependency.                                                  |
| Shared Code            | Code reused across responsibility boundaries; reuse inside one module is not automatically a shared package.                                                                   |
| Design Forces          | Evidence-backed conditions influencing boundaries and patterns: change locality, consumers, volatility, ownership, testability, tooling, and constraints.                      |
| Composition Root       | Application-entry assembly of concrete collaborators when explicit wiring is useful; not required for every framework/module.                                                  |
| Rule / Check           | Structural requirement and a stated mechanism to detect, review, or report violations.                                                                                         |

## Design Principles

1. **Purpose and change locality:** group code by coherent responsibilities and decisions that change together; assess actual coupling and navigation costs instead of choosing a fashionable pattern or directory count.
2. **Information hiding and deep modules:** protect volatile choices behind a small, meaningful consumer interface where justified. Avoid exposing internals, shallow forwarding wrappers, and artificial public APIs for internal-only code.
3. **Distinct boundaries:** decide repositories, build targets, release units, and modules separately. Do not infer one-to-one relationships or deployment behavior from directory layout.
4. **Explicit dependency direction:** define which _static graph_ is governed, permit cross-module access only through intentional surfaces, and prefer an acyclic architectural-module graph. Do not confuse a runtime call/event with a static import; identify and resolve actual cycles or document a scoped exception.
5. **Core independence when beneficial:** if core behavior must survive framework/storage changes, keep it independent of concrete adapters via owned abstractions or another justified seam. Do not mandate hexagonal architecture, layering, or dependency injection for trivial code.
6. **Pattern fit, not prescription:** select top-level organization and module-internal patterns from forces and constraints. Mix compatible patterns where useful and respect framework-required layout, visibility, and build mechanisms.
7. **Explicit ownership and reuse:** give shared code a cohesive purpose, owner, consumers, visibility, and change/compatibility policy. Avoid catch-all shared modules and premature generalization.
8. **Consumer-aware contracts:** preserve supported public paths, behavior, and compatibility across independently evolving units. Distinguish internal refactors from changes that affect current consumers.
9. **Boundary-relevant conventions and tests:** define conventions and test placement that reinforce ownership and integration; omit irrelevant boilerplate, obligatory layers, or test types that have no corresponding boundary.
10. **Proportionate enforcement:** make high-value rules verifiable with the strongest feasible compiler/build/import/test check; for judgment-based policies use an explicit review. Label missing, planned, and unrun enforcement truthfully.
11. **Evidence and trade-offs:** record the decisive forces, viable alternatives, consequences, and unresolved assumptions for material structural decisions; do not infer suitability solely from a pattern name.
12. **Incremental evolution:** retain working arrangements unless evidence warrants change. Separate behavior-preserving moves from functional changes where feasible; plan migration, compatibility, verification, and release recovery before disruptive edits.

## Reference Routing

Read **only** the reference files needed for the current decision, and load an additional file when its subject materially affects that decision. Do not pre-load all references.

| Decision / Trigger                                                                   | Read                                         |
| ------------------------------------------------------------------------------------ | -------------------------------------------- |
| Repository grouping, release/build unit placement, paths, ownership                  | `references/repository-layout.md`            |
| Capability/component/layer/use-case grouping; internal patterns and fit              | `references/code-organization-strategies.md` |
| Candidate modules, split/merge, public surfaces, cohesion/cycles                     | `references/module-design.md`                |
| Allowed imports, shared code, cross-unit contracts, compatibility                    | `references/dependency-rules.md`             |
| Naming, error/composition/config/state/asset boundary conventions                    | `references/conventions.md`                  |
| Test locations, integration/contract seams, fixture ownership                        | `references/test-layout.md`                  |
| Structural checks, CI/review stages, legacy violation baselines                      | `references/enforcement.md`                  |
| Existing-code assessment, gap severity, migration/change classification              | `references/restructuring.md`                |
| Explicitly requested **full** design document or complete document-structure rewrite | `assets/codebase-design-template.md`         |

**Example:** a cyclic dependency review normally needs only `references/module-design.md` and `references/dependency-rules.md`; read `references/restructuring.md` only if a migration plan is requested. A focused document update need not load the full template.

## Workflow

### 1. Establish Scope and Current Facts

- Identify mode, deliverable, scope, project authority, and existing accepted decisions. Check whether design/document edits or production-code edits are actually requested.
- Inspect relevant existing paths, manifests, consumers, static dependency edges, tests, and checks; if scanning an existing codebase, use `references/restructuring.md` for evidence and confidence rules.
- Extract **design forces** per affected release unit/capability: ownership, change drivers, public consumers, isolation needs, tooling/framework constraints, and known costs. Separate observed facts from constraints and hypotheses.
- Resolve materially ambiguous inputs before committing to one design; a non-disruptive review may report uncertainty instead of blocking.

### 2. Form a Preliminary Structural Proposal

- **Repository and unit boundaries (if relevant):** distinguish repository topology from build targets, release units, and public compatibility (`references/repository-layout.md`).
- **Modules:** identify responsibilities, hidden decisions, consumers, candidate boundaries, public/internal visibility, and ownership; test split/merge choices (`references/module-design.md`).
- **Organization:** choose primary grouping and optional internal patterns from documented forces, including at least one meaningful alternative for consequential choices (`references/code-organization-strategies.md`).
- **Dependency sketch:** map important allowed/forbidden static edges and cross-unit surfaces; identify cycles, shared-code candidates, and expected migration impact (`references/dependency-rules.md`).
- Prepare an **annotated representative layout** (root/unit/pattern only where relevant) and a short decision summary. Do not pretend a proposed tree has been observed in the repository.

### 3. Decision Checkpoint

For a full new design or a material change to existing repository/module structure, stop after Step 2 and present a reviewable proposal before Step 4. This gate is about approval of architectural choices, not merely permission to edit files.

Present concisely:

1. **Proposed decisions:** repository/build/release boundaries (if affected), main modules and owners/consumers, primary organization and significant internal patterns, representative trees, and intended dependency direction.
2. **Why:** decisive forces, one serious alternative and its trade-off for each consequential choice, plus material risks, compatibility effects, and evidence limitations.
3. **Approval request:** clearly identify which choices need confirmation and which are mandated by existing project instructions; ask to **approve, revise, or reject** the proposed structural direction.

**Wait for explicit user confirmation.** If revised, rework only affected Step 2 decisions and present the changed proposal again. An already-approved equivalent plan need not be approved twice; a choice fully mandated by authoritative project constraints needs no discretionary re-approval. If _all_ structural choices are already specified or approved, record that basis and proceed without a redundant stop.

**Do not invoke this gate for:** a read-only review, a narrowly scoped explanation, or a non-structural/administrative document fix. For a focused design request, invoke it only if the proposal introduces a material new boundary, ownership change, dependency-policy change affecting consumers, or an equivalent architectural commitment. If a late discovery materially changes an approved decision, return to this checkpoint for the **changed decision**, not the entire design.

### 4. Specify the Approved Design

- Finalize module responsibilities/public surfaces and the **permitted** dependency model. Keep permitted edges distinct from the **observed** graph; document justified exceptions with scope, owner, reason, and revisit trigger (`references/module-design.md`, `references/dependency-rules.md`).
- Define cross-unit contract governance and shared-code placement only where relevant; distinguish package-API compatibility from protocol evolution (`references/dependency-rules.md`).
- Select structural conventions and interaction/composition ownership (`references/conventions.md`); map tests to real boundaries (`references/test-layout.md`).
- Assign `DR-xx` / `CV-xx` constraints to `EN-xx` checks or explicit review/gaps with honest execution status (`references/enforcement.md`).
- For restructuring, record current gaps, classify consumer impact, and sequence recoverable, verifiable steps (`references/restructuring.md`). Do not unilaterally expand the previously approved structural scope.

### 5. Approve Changes, Deliver, and Verify

- **Change approval:** before applying a potentially breaking change to existing design files or any destructive/consumer-impacting source restructuring, show affected units/consumers, compatibility or recovery plan, and the exact change. Seek explicit confirmation **unless the same impact and scope were already approved at Step 3**. Approval of a proposed direction alone does not authorize implementation.
- **Review:** report path/edge evidence, confidence, severity, consequences, and focused recommendations. Never claim an unrun check passed.
- **Design:** present the proposed or approved organization, decisive trade-offs, and outstanding decisions in the requested format; do not create a file without a request.
- **Explicit full document:** use `assets/codebase-design-template.md` at a specified path or else `docs/codebase-design.md`. Respect the project's documentation language, otherwise English.
- **Focused update:** modify only relevant document sections plus dependent IDs/mappings; preserve unaffected content.
- **Restructure:** present or implement only requested steps, clearly labeling what was actually executed.
- Run the Verification Checklist for affected scope. Report blocked actions, unverified facts, and unavailable checks rather than inventing a pass.

## Conflict and Change Rules

- **Late gaps:** if a new fact changes the architecture choice or its impact, stop and request a targeted decision before proceeding. A low-impact unknown can remain explicitly unresolved in a proposal or review, never silently adopted.
- **Conflicting constraints:** respect project/language/framework requirements, but surface incompatibilities with module visibility, static cycles, compatibility, ownership, or feasible enforcement. Explain consequences and a viable alternative; record the user-approved exception with a narrow scope, owner, and review trigger. Do not silently ignore the project rule or the structural risk.
- **Change classes:** **Administrative** (clarifies without consumer effects), **Additive** (extends without invalidating current consumers), **Potentially Breaking** (changes a consumed public path/behavior, allowed dependency, ownership/contract, or build/release boundary). Classify by actual impact, not edit size; do not downgrade an unverified consumer impact to Additive.
- **Authority:** distinguish the acceptance of _a design decision_, permission to _write a document_, and permission to _change source code_. A user approval covers only the stated scope; repo review settings and `CODEOWNERS` are separate controls and must not be assumed to enforce approval by themselves.
- **Preservation:** keep existing stable rule IDs and public paths; explicitly supersede changed decisions/rules rather than recycling IDs. Prefer compatible transitions to instantaneous breakage where consumers evolve independently.

## Common Failure Modes

- **"The framework folder tree is the architecture."** Follow required paths but verify actual responsibility, public access, and dependency ownership.
- **"Two modules import each other, so use events."** Show the new **static** graph; an event alone does not prove that a cycle disappeared.
- **"This belongs in `common`."** Require a cohesive purpose, specific consumers, owner, and change policy before sharing.
- **"Approval or enforcement can wait."** Do not adopt material unapproved decisions or present unenforced, unrun rules as guaranteed; state the gap explicitly.
- **"Moving everything at once is simpler."** Prefer small, verified, compatible steps; a tree-only rename does not prove preserved consumer behavior.

## Verification Checklist

Verify each **affected** part; if evidence is unavailable, report the limit:

1. **Forces and fit:** material decisions trace to actual requirements/constraints; plausible alternatives and avoid-when conditions were considered; no pattern was selected by project type alone.
2. **Checkpoint:** material new architecture/structural changes received explicit confirmation (or the decision was already accepted/mandated); late changes were re-presented; read-only reviews were not needlessly blocked.
3. **Consistency:** repository, release, build, module names/paths agree in trees, catalog, test mapping, rule and check entries; identifiers are unique, stable, and linked; no unresolved delivered placeholders.
4. **Boundaries and graph:** public/internal paths and permitted versus observed static edges are distinguished. No unintentional architectural static cycles; do not assert graph compliance without inspecting the actual graph.
5. **Shared code and contracts:** responsibilities/owners/consumers are explicit and independent release compatibility is addressed where applicable.
6. **Conventions and tests:** selected areas align with forces and framework constraints; tests belong to meaningful boundaries without artificial empty suites.
7. **Enforcement:** each numbered rule has a feasible check/review or explicit gap, with scope, stage, owner, and evidence/status; no unrun check is marked passing.
8. **Migration and approvals:** classify consumer impact, obtain authorization for affected operations, and give each migration step prerequisites, checks, compatibility, rollback/recovery, and owner; distinguish proposed from executed.
9. **Scope:** no invented domain/system/API decisions, irrelevant tool tutorials, out-of-scope changes, or wholesale rewrites for focused requests.
