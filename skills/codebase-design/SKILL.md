---
name: codebase-design
description: Design and maintain source-code structure or review codebase structural health. Use for initial repository design, architecture-aware feature changes, module/dependency conventions, code organization, ongoing maintenance, focused or periodic codebase reviews, and incremental restructuring plans in any language or framework. Covers repository and release-unit layout, module boundaries, public surfaces, shared code, test placement, and structural enforcement. Not for detailed system deployment architecture, domain modeling, API/database schema design, or general feature implementation.
metadata:
  author: phatnguyen975
  version: 1.0
---

# Codebase Design

## Purpose and Scope

Design, maintain, and assess **source-code organization** across a repository or a selected part of it. Apply language-, framework-, and tool-agnostic principles through the **actual project's conventions, constraints, and available boundary mechanisms**. The skill supports monorepos, single-unit repositories, libraries, clients, services, and mixed stacks. Do not impose a universal directory tree.

**In scope:** repository and build/release-unit placement; module responsibilities and public surfaces; code grouping and internal patterns; static dependencies; shared code and cross-unit contract ownership; structural conventions; test locations; architecture checks; current-state findings; and incremental codebase restructuring.

**Out of scope:** selecting runtime/deployment topology, inventing domain/business models, designing detailed API/database schemas, UI appearance, full security/performance audits, general function-level code quality, and implementing features as an independent task. Use established decisions in these areas as inputs; report conflicts that affect code structure.

## Operating Modes

- **Design:** establish or evolve a target codebase structure. Includes initial design, structure-aware implementation guidance, focused design updates, and migration planning for approved structural changes. Preserve unaffected boundaries; a routine code change does not trigger a full redesign.
- **Review:** assess current structural health and return evidence-backed findings, priorities, and proposed improvements. Includes focused, repository-wide, continuous, and periodic assessments. Read-only review does not authorize changing code or adopting new architecture.

A Review may identify work that warrants a subsequent Design decision. Do not silently convert a recommendation into an approved design or an implementation task. The user determines scope and whether an output is conversational, a persistent document, or authorized code changes. **Neither mode creates files by default.** A periodic review is performed only when invoked; this skill does not schedule itself.

## Evidence and Terminology

Gather evidence proportionate to the requested scope: repository instructions, requirements, source/test structure, manifests, supported language/framework conventions, build and release boundaries, entry points, public consumers, imports/exports, ownership, existing design decisions, and actual checks/results. Mark claims as **Observed**, **Specified**, **Proposed**, or **Unverified**. Report material uncertainty rather than guessing owners, paths, versions, dependencies, or test outcomes.

| Term                   | Meaning                                                                                                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Repository             | Version-control boundary; not necessarily a build or deployment boundary                                                                                            |
| Build Target / Package | Unit identified by a build or package system; may not release independently                                                                                         |
| Release Unit           | Application, service, library, or tool distributed/published/deployed as an identifiable unit; may contain multiple build targets                                   |
| Module                 | Cohesive architectural source boundary with an owned responsibility and intentional access; realized by actual package/export/build rules or stated review controls |
| Public Surface         | Entry points intended for identified consumers; internal-only modules need no invented cross-module API                                                             |
| Contract               | Consumer-visible agreement at an independently evolving boundary; details of its API/schema are outside scope                                                       |
| Dependency             | A static source/type import or declared build edge unless explicitly called runtime interaction or data flow                                                        |
| Design Forces          | Evidence-backed drivers such as change locality, ownership, consumers, volatility, isolation, and tooling                                                           |
| Rule / Enforcement     | Structural constraint (`DR`/`CV`) and the check, review, or explicit gap (`EN`) maintaining it                                                                      |

For **repository-wide** work, identify _all relevant release units_, shared packages, and cross-unit boundaries before detailed design or sampling. In a large repository, inspect each unit at inventory level, then deepen analysis according to scope and risk. State any inaccessible or unexamined units; a sample cannot establish repository-wide compliance.

## Design Principles

1. **Organize for responsibility and change:** prefer cohesive responsibilities and change locality over fashionable patterns, directory counts, or artificial layers.
2. **Hide decisions behind useful boundaries:** minimize exposed internals and shallow forwarding APIs. Specify actual consumer access; a folder alone is not an enforced module.
3. **Keep boundaries distinct:** decide repository, build target, release unit, module, and contract boundaries separately. Independently released units may share a repository.
4. **Define the graph:** state whether a rule governs static imports, declared build edges, or runtime interaction. Keep intended and observed edges separate; check architectural cycles over a defined graph.
5. **Choose patterns by forces:** select a primary organization and only the internal separation justified by the module's needs; combine compatible patterns without imposing one layout on every unit.
6. **Protect volatile integrations selectively:** introduce ports/adapters or other seams when they meaningfully isolate core decisions; avoid speculative interfaces.
7. **Own shared code and state:** record purpose, consumers, owner, public surface, and change policy; avoid unowned `common` packages or duplicate shared invariants.
8. **Respect consumers and compatibility:** protect existing public contracts, entry paths, and independently evolving consumers; classify changes by impact, not edit size.
9. **Place tests at real boundaries:** select module, integration, contract, and end-to-end locations where applicable; follow language/framework idioms and avoid mandatory empty suites.
10. **Enforce proportionately:** prefer native visibility/build constraints and relevant automated checks; use explicit human review for judgment-based rules. Never present an unrun or absent check as passing.
11. **Distinguish observations from decisions:** findings require evidence and a source of expected behavior; proposed structure requires forces, meaningful alternatives, trade-offs, and explicit status.
12. **Evolve incrementally and with approval:** keep sound existing structure, verify small changes, plan compatibility/recovery when needed, and obtain human approval for material new architectural commitments.

## Reference Routing

Read **only** the material needed for the current decision. Start with this file; open a reference when its subject is relevant, not merely because it exists. Use paths relative to the skill root.

| Trigger                                                                     | Load                                         |
| --------------------------------------------------------------------------- | -------------------------------------------- |
| Repository grouping, build/release units, monorepo roots, ownership         | `references/repository-layout.md`            |
| Feature/component/layer/use-case grouping, internal patterns and fit        | `references/code-organization-strategies.md` |
| Module candidates, public surfaces, cohesion, split/merge, cycles           | `references/module-design.md`                |
| Allowed dependencies, shared packages, contracts, compatibility             | `references/dependency-rules.md`             |
| Structural naming, composition, configuration, error/state/asset ownership  | `references/conventions.md`                  |
| Test locations, integration/contract seams, test support                    | `references/test-layout.md`                  |
| Rule checks, CI/review coverage, legacy baselines                           | `references/enforcement.md`                  |
| Evidence-backed health review, findings, prioritization, migration planning | `references/restructuring.md`                |
| Explicit full design document                                               | `assets/codebase-design-template.md`         |
| Explicit full structural review report                                      | `assets/codebase-review-template.md`         |

**Examples:** reviewing a dependency cycle commonly needs `module-design.md` and `dependency-rules.md`, plus `restructuring.md` for findings; creating a complete health report also needs the review template. A routine module placement decision need not load either full template.

## Workflow

### 1. Establish Scope and Evidence

- Determine **Design** or **Review**, the affected repository/units/modules, task depth, output format, and whether document or source edits are explicitly authorized. Reuse accepted project decisions and prior findings when accessible.
- Inspect relevant requirements, actual code/build boundaries, consumers, constraints, and applicable tests/checks. For repository-wide scope, cover the unit inventory and cross-unit interactions before narrowing.
- Identify decisive design forces or review criteria and their evidence. After inspecting available inputs, ask the human to resolve missing or conflicting requirements, ownership, consumers, and constraints that affect Design. Do not proceed with an affected design decision until clarified; revisit clarification if new ambiguity emerges. A read-only Review may instead record evidence limits.

### 2. Follow the Applicable Path

**Design Path**

1. **Propose:** choose relevant repository/build/release boundaries, modules, primary grouping, internal patterns, public surfaces, intended static edges, and significant alternatives. Show a small annotated structure and consequences; preserve unaffected parts.
2. **Decision Checkpoint (Human Gate):** for a full discretionary design or a material new boundary, ownership, dependency-policy, or consumer-impacting choice, present the proposal, decisive forces, meaningful alternative, trade-offs, affected consumers, and unanswered questions. **Stop for explicit approval, revision, or rejection before treating the choice as adopted.** Do not repeat approval for an equivalent already-approved choice or a structure mandated by authoritative project instructions. A narrow non-material change needs no gate.
3. **Specify:** after approval, detail only applicable module rules, conventions, tests, enforcement, contract governance, and optional migration. Mark rules as proposed until accepted; link structural rules to real checks, explicit review, or gaps. If late evidence materially changes the approved choice, return only the changed decision to the gate.
4. **Execute only when authorized:** permission to approve a design, write a document, and change source are separate. Before destructive/consumer-impacting edits, confirm the exact execution scope and compatibility/recovery plan unless already explicitly authorized at that level. For routine authorized edits, maintain existing rules and verify affected boundaries without an additional gate.

**Review Path**

1. **Assess:** map current units/modules, public/internal surfaces, static dependencies, ownership, structural conventions, test placement, enforcement, and existing exceptions against accepted constraints. Broaden the scan only as evidence requires; label partial coverage.
2. **Classify:** distinguish verified violations from risks, hypotheses, and optional improvements. Give findings `G-xx` IDs within the report, paths/edges and authority, severity, confidence, affected consumers, and impact. Do not assert a preference is a violation without a binding rule or evidence of harm.
3. **Recommend:** prioritize by impact, urgency, feasibility, and dependencies. Offer the smallest appropriate improvement and trade-offs, with **high-level sequence** when useful. Keep recommendations **Proposed**, not automatically approved. Compare previous review findings when an accessible baseline exists; otherwise state no baseline.
4. **Handoff:** end read-only review with findings. If a material target redesign or detailed migration is requested, enter the Design Path and apply its Human Gate and execution-authorization rules; do not produce an adopted target or modify code just because review found issues.

### 3. Deliver and Verify

- Return the requested outcome in the conversation unless a persistent document or source update was explicitly requested. An explicitly requested **full design document** uses the design template; a **full structural review report** uses the review template. Use the requested path, otherwise the project's documentation convention or `docs/codebase-design.md` / `docs/codebase-review.md` respectively. For dated review history, use distinct report paths when requested; never overwrite historical reports silently.
- For focused work, deliver only relevant findings or decisions; do not populate a full template. A review's improvement plan is **not** a detailed executable migration plan. Keep detailed migration in the Design deliverable when needed.
- Check scope and evidence; intended versus observed graphs; rule/check mappings; change authority; consumer compatibility; and applicable tests. State what was **Passed / Failed / Not Run / Blocked** with actual evidence. Do not claim whole-repository coverage from sampling or claim a proposal was implemented.
- Run the **Verification Checklist** for affected scope. Report blocked actions, unverified facts, and unavailable checks rather than inventing a pass.

## Decisions, Changes, and Exceptions

- **Decision status:** `Proposed`, `Pending Approval`, `Approved`, or `Superseded` with authority/reference; do not mark a proposal adopted without evidence. Record consequential alternatives and revisit triggers where useful.
- **Change impact:** `Administrative` (no consumer effect), `Additive` (does not invalidate established consumers), or `Potentially Breaking` (may change a consumed path, contract, dependency permission, ownership, or release/build boundary). Unknown consumer impact is not automatically Additive.
- **Authority:** human architecture approval does not replace project review/merge controls or authorize source changes. Approval covers only the stated choices and action scope; read-only Review never requires approval to report findings.
- **Exceptions:** specify rule, scope, reason, owner when known, and review/removal trigger. Existing violations may be baselined narrowly; never turn them silently into accepted target behavior.
- **Late or conflicting evidence:** follow applicable project/framework constraints, surface structural consequences, and seek targeted reconsideration when a material accepted choice must change. Retain stable IDs and supersede rather than repurpose adopted rules.

## Output Contract

- **Design document:** living description of the approved or explicitly proposed target structure. Use `assets/codebase-design-template.md` only for full-document requests; migration is optional. If clarification is unavailable, pause the affected Design work and ask in the conversation rather than issuing an incomplete document. A fully specified proposal may retain `Pending Approval` status without implying acceptance.
- **Review report:** time-scoped snapshot of examined current structure, findings, evidence, confidence, coverage, and improvement recommendations. Use `assets/codebase-review-template.md` only for requested full reports; findings are not accepted architecture decisions.
- **Templates:** follow their section-level fill instructions. Replace all `<...>` instructional placeholders with real content and remove instructional comments. Use `Not applicable — <Why this section does not apply>` for a required non-applicable section; never invent evidence to fill rows.
- **Identifiers:** `DR-xx` (dependency rules), `CV-xx` (boundary conventions/shared-code and contract policies), `EN-xx` (checks, explicit reviews, or enforcement gaps), `G-xx` (observed findings/gaps). Preserve IDs within a living design; report IDs are unique within each review snapshot. Every `DR`/`CV` links to one or more `EN` entries or an explicit enforcement gap; never invent check results.
- **Contract scope:** describe external contract owners, locations, consumers, compatibility, and verification responsibilities — not unrequested API/schema contents. Respect the project's documentation language and actual language/framework/build conventions. Verify version-sensitive claims against authoritative current sources rather than hardcoding versions here.

## Verification Checklist

- [ ] Scope includes all relevant release units and cross-unit boundaries, or explicitly lists excluded/unexamined units.
- [ ] Material design inputs were clarified with the human or established by authoritative project evidence; no unresolved design questions remain in the design output.
- [ ] Every important choice has forces, ownership/consumer context, trade-offs, and accurate approval status; Human Gate applied where warranted.
- [ ] Review findings separate observation, evidence, applicable authority, severity, confidence, priority, and proposal; previous-review comparisons are grounded.
- [ ] Public/internal surfaces and allowed versus observed static edges are distinct; no unverified claim of cycle freedom or check compliance.
- [ ] Shared-code and independent-release compatibility obligations have owners/consumers where applicable.
- [ ] Structural conventions, tests, enforcement and exceptions fit the actual project and have traceable IDs where documented.
- [ ] Migration steps, if requested, have prerequisites, expected graph delta, verification and recovery; nothing proposed is misreported as executed.
- [ ] Documents contain no unresolved placeholders or redundant tables; source/document edits stayed within granted authority.
