---
name: evolutionary-architecture-design
description: Design, review, and evolve software architecture using evolutionary architecture principles. Use for new or existing systems, from end-to-end design to focused architectural decisions, to address architectural drivers, evaluate trade-offs, and enable safe, incremental evolution through adaptable structures and architectural fitness functions. Do not use for implementation code, detailed database or API schemas, UI design, tactical domain modeling or infrastructure provisioning.
metadata:
  author: phatnguyen975
  version: 1.0
---

# Evolutionary Architecture Design

## Purpose and Scope

Design or evolve a **sufficient, defensible software architecture that can change safely**. Work from architectural drivers, choose boundaries and interactions deliberately, evaluate important trade-offs, preserve decision rationale, and protect critical properties as the system evolves. Use scenario-specific evidence rather than prescribing an architecture style, technology, or complexity level.

This skill supports three **task intents**, not three separate design methods:

- **Design:** establish architecture for a new system or a new architecturally significant subsystem.
- **Evolve:** change an existing architecture; distinguish observed current, transition, and proposed target states.
- **Review:** assess an existing or proposed design against its drivers; recommend changes without silently making or approving them.

A task may be **end-to-end** (architecture description and any significant ADRs) or **focused** (one boundary, quality trade-off, ADR, fitness function, or migration). Follow only relevant steps and produce only requested or necessary artifacts. Do not create a full architecture document to answer a focused question. A review is read-only unless the user requests edits.

**In scope:** system context; architecturally significant capabilities and quality requirements; constraints; styles and deployment topology; modules and service boundaries; architecture-level data, integration, security and operational policies; key runtime/deployment behavior; technology trade-offs; decisions, fitness functions and migration planning.

**Out of scope:** class-level and tactical domain modeling, API fields, database table schemas, UI/UX, application code, tool configuration, deployment scripts and runbooks. Record architecture-level obligations and interfaces; hand implementation details to another workflow. A framework or vendor choice belongs here only if it materially affects architectural drivers.

## Deliverables and Conventions

For an **end-to-end** design or an explicitly requested architecture document, use the project's established locations and conventions; otherwise default to:

- `docs/system-design.md` — living architecture description structured around the twelve arc42 sections; load `assets/system-design-template.md` only when writing or updating it.
- `docs/decisions/NNNN-short-title.md` — an ADR **only for each newly proposed, architecturally significant decision**; load `assets/adr-template.md` and `references/adr-guide.md` only when needed.

For a **focused design or review**, return the decision, analysis, affected architecture documentation or suggested diff at the requested scope; do not force the full document or create a redundant source of truth. Prefer links to existing requirements, decisions and checks over duplication. Do not overwrite unrelated content or reformat an existing repository merely to match this skill.

Use the project's writing language and documentation conventions; default to English when absent. In templates, `<...>` gives instructions for what to fill, not literal output. Do not emit template comments, sample rows or unresolved placeholders as completed architecture documentation.

## Core Principles

1. **Distinguish evidence from intent.** Label stakeholder-confirmed facts, observed implementation, estimates, assumptions, proposed choices and unknowns. Cite their sources. Do not invent targets, approvals, historical reasoning, test results, owners or compliance claims.
2. **Start with drivers.** Prioritize architectural requirements and constraints before style or technology. Define measurable quality scenarios when a criterion is relevant; an unconfirmed target is a gap to resolve, not a license to invent a number.
3. **Keep states distinct.** Separate as-is, transition and target design; distinguish design coverage from demonstrated runtime compliance; distinguish proposed from accepted decisions and planned from active checks.
4. **Make trade-offs explicit.** Compare materially different, viable choices for open, consequential questions. Prefer the simplest design supported by the actual drivers and evidence. Do not manufacture alternatives for mandated choices.
5. **Defer choices, not obligations.** Defer an optional decision only when an interim design is viable, the decision can be revisited safely, and a trigger, owner role and next action are clear. Unmet mandatory requirements remain visible.
6. **Evolve incrementally.** Reassess affected drivers, contracts, data ownership, failure modes and guardrails after structural revisions. For live systems, design compatibility, verification, cutover, rollback or forward recovery, and retirement.
7. **Protect important properties.** Define objective architecture fitness functions or explicit review methods for critical change-sensitive characteristics where feasible. Do not claim an unimplemented check is active; not every ADR requires its own check.
8. **Record consequential rationale.** Use ADRs for new significant choices and supersession for changed accepted decisions. Observed undocumented architecture is not a retroactively accepted ADR.
9. **Respect human authority.** Never self-approve significant trade-offs, accepted risk, requirement changes or breaking/irreversible changes. When confirmation is unavailable, keep the affected decision proposed and surface the blocker; progress on independent work may continue.
10. **Be proportionate.** Include only views, scenarios, concepts and records that explain a real driver, choice or risk. Do not require every possible diagram, pattern or check.

## Terms and Statuses

- **Architectural driver:** a significant function (`FUN-nn`), quality scenario (`QUA-nn`), mandatory constraint (`CST-nn`), or distinct stakeholder concern requiring architectural analysis (`CNC-nn`). Do not turn every requirement or duplicate concern into a driver. Maintain stable IDs for drivers in the architecture scope being documented.
- **Quality scenario:** a specific stimulus source, stimulus, environment, affected artifact, response and response measure. A quality goal can group several scenarios. See `references/quality-attributes.md`.
- **Baseline:** the observed as-is architecture for an existing system, or an initial architecture candidate for a new system. The target is the architecture being proposed or approved; a baseline is not proof of suitability.
- **Design coverage:** `addressed` (credible design explanation, not implementation proof), `gap` (known unmet need), `unverified` (insufficient information or validation), `accepted-risk` (documented shortfall explicitly authorized by an accountable human). Assess a hard constraint separately as `meets`, `gap` or `unverified`, with evidence. A non-waivable legal, contractual or other hard constraint cannot be waived merely by choosing `accepted-risk`; it requires an authorized change to the underlying obligation, if one is possible.
- **Evidence:** `observed`, `analyzed`, `tested`, `measured`, `estimated` or `unverified`, with source, environment and limitations. These describe kinds of support, not a universal ranking of certainty.
- **ADR status:** `proposed`, `accepted`, `rejected`, `deprecated`, or `superseded by ADR-NNNN`; use project conventions when already established.
- **Deferred decision (`DD-nn`):** an optional choice not yet made, with safe interim approach and revisit condition.
- **Fitness function (`FF-nn`):** an objective architectural integrity assessment. Execution status is `planned`, `active` or `suspended`; the last result is recorded separately as `pass`, `fail`, `not-run` or `unknown` when applicable. `active` requires evidence of an operating check, not a passing result.
- **C4 container:** an application or data store in a logical architecture, not necessarily a Docker container or a separately releasable unit. A release/deployment unit is a different concern.
- **Compatible change:** existing consumers and guarantees can continue without coordinated change; otherwise assess it as breaking, including for data and operational contracts.

## Inputs and Reference Routing

Inspect the user's task, repository instructions and the relevant requirements, existing design, ADRs, code topology, release/deployment evidence and available observations. Identify the system boundary, stakeholders, prioritized scenarios, hard constraints, existing dependencies, and — when changing a live system — migration restrictions. Ask only questions whose answers materially change the decision. Mark nonblocking unknowns explicitly and use reversible assumptions where safe.

Load only the references for the active work, and open templates only when producing those artifacts. References are guides for particular design questions, not a required reading sequence:

| Need                                                     | Reference                                    | Load When                                                             |
| -------------------------------------------------------- | -------------------------------------------- | --------------------------------------------------------------------- |
| Drivers, baseline, iteration, timing, technology choices | `references/design-iteration.md`             | Framing, choosing or refining a significant design                    |
| Quality scenarios, tactics, trade-offs                   | `references/quality-attributes.md`           | Defining or evaluating quality requirements                           |
| Style/topology comparison                                | `references/architecture-styles.md`          | A structural style or distribution choice is open                     |
| Module/service/data boundaries                           | `references/partitioning-and-granularity.md` | Partitioning, splitting, merging or assessing coupling                |
| Architectural views                                      | `references/views-and-diagrams.md`           | Creating or revising context, structural, runtime or deployment views |
| Crosscutting policy                                      | `references/crosscutting-concepts.md`        | A policy spans multiple architectural elements                        |
| Architecture guardrails                                  | `references/fitness-functions.md`            | Defining, evaluating or revising fitness checks                       |
| Safe migration                                           | `references/incremental-change-patterns.md`  | Changing a running system with consumers or state to preserve         |
| ADR lifecycle                                            | `references/adr-guide.md`                    | Proposing, reviewing or superseding an ADR                            |

Do not load style, migration or vendor guidance solely because it exists. Reuse references already read; do not insert their entire text into the deliverable.

## Workflow

**Apply these activities in order where dependencies exist, then iterate as evidence changes.** For focused tasks, start from known drivers and perform only the affected activities. For a review, evaluate and report without assuming permission to mutate files. The checkpoints below are conditional decisions, not mandatory ceremonies or a requirement for three separate conversations.

### Phase 1: Frame the Architecture Problem

1. **Discover intent and baseline.** Identify Design, Evolve or Review and the exact scope. Examine existing evidence and accepted decisions; describe observed facts separately from the proposed state. For a new system, record the decision context instead of pretending an as-is implementation exists.
2. **Define context and drivers.** Identify external actors/systems, key responsibilities, relevant stakeholders, constraints and important functional scenarios. Derive quality scenarios with objective criteria or explicitly unconfirmed targets. Assign IDs and rank by importance, design difficulty, timing and interactions. Read `references/design-iteration.md` and `references/quality-attributes.md` when this analysis is needed.
3. **Resolve design-blocking ambiguity.** Present conflicting requirements or missing facts that could change the chosen architecture. **Checkpoint A — Drivers:** obtain human agreement on disputed scope, priorities or targets before treating them as approved. If already documented and authoritative, reuse that agreement; if unavailable, label the affected choices provisional and avoid irreversible commitments.

### Phase 2: Establish and Evaluate a Candidate

4. **Develop architecture candidates.** For an existing system, use the observed as-is baseline to identify gaps and candidate changes. For new design, establish an initial candidate and compare alternatives when a meaningful structural choice is open. Define major responsibilities, modules/containers, interfaces, data ownership, deployment/release boundaries and critical dependency paths. Load style/partitioning references only when those decisions matter.
5. **Evaluate consequential choices.** Walk priority scenarios — including failure and change scenarios — through candidates. Check hard constraints as pass/fail conditions; compare operations, cost, coupling, consistency, security, reversibility and migration. For architecture-level technology choices, distinguish mandated, retained existing and open options; compare viable alternatives when a choice is open, and verify consequential claims. Apply the decision-timing and technology-evaluation guidance in `references/design-iteration.md` when relevant. Investigate material uncertainties rather than asserting suitability. Record the preferred candidate, remaining gaps and significant proposed ADRs.
6. **Review the proposed direction.** **Checkpoint B — Architecture:** obtain agreement on material structural trade-offs and new decisions when stakeholder authorization is required. If a proposal includes breaking contracts or irreversible change, acceptance is conditional on the impact review in Checkpoint C; do not mark affected ADRs accepted prematurely. For review-only tasks, provide findings and recommendations rather than fabricating authorization.

### Phase 3: Refine and Plan Evolution

7. **Refine high-impact gaps.** Choose the driver(s) and architecture element(s) that the next iteration must address. Evaluate relevant tactics, allocate responsibilities and interfaces, and refine the affected candidate. Reassess previously addressed drivers and constraints. Repeat while iterations add credible design progress; escalate material uncertainty or conflicting priorities instead of looping indefinitely.
8. **Describe consequential behavior.** Capture the required context/structure, significant success/failure runtime paths, data consistency, trust boundaries, and deployment/failure isolation. Use views and crosscutting policies only where they communicate relevant architectural obligations.
9. **Define evolution safeguards.** Specify objective checks for critical, regression-prone properties with criteria, ownership, cadence, response and actual execution state. For changes to a running system, plan compatibility phases, affected consumers and data, verification, safe cutover, recovery and retirement.
10. **Assess risk and approvals.** Trace every relevant driver to design coverage and evidence; record unknowns and residual shortfalls. **Checkpoint C — Change Impact:** obtain explicit authorization before finalizing a breaking/irreversible migration, an agreed target change or a risk exception requiring authority. This review may be combined with Checkpoint B if the necessary impact plan is already available. Never treat a hard constraint as waived by risk acceptance alone.

### Phase 4: Deliver and Verify

11. **Update only requested/necessary artifacts.** For end-to-end design, use the system design template and the applicable ADR template. For focused tasks, update only affected sections/files or report recommendations. Ensure as-is, transition and target descriptions, statuses and internal links are consistent. A user request to edit named files authorizes those scoped edits, not unrelated destructive changes.
12. **Verify and report.** Check driver coverage, constraints, scenarios, trade-offs, ADR state, diagram consistency, fitness checks, migration safety and unresolved approvals. Report files changed (if any), decisions, evidence limits, accepted risks and blockers. Do not claim validation that was not performed.

## Update and Review Rules

- Compare the requested target against observed as-is and accepted prior decisions. Preserve important architectural history. If an accepted decision materially changes, propose a new ADR; supersede the old one only when the replacement is accepted.
- Keep current, transition and target diagrams and obligations labeled; never render planned components as deployed. Trace affected consumers, contracts, data authority, invariants, failure behavior, releases, policies and fitness functions.
- Revisit a deferred choice when its signal fires; do not automatically implement the previously imagined answer. Temporary migration exceptions require owner, safety guard and retirement criteria.
- A review records findings by severity/driver and suggests feasible alternatives; do not assert that code inspection alone verifies production quality, or rewrite historical ADRs as if they had been decided today.

## Common Rationalizations to Reject

| Rationalization                        | Response                                                                             |
| -------------------------------------- | ------------------------------------------------------------------------------------ |
| "Microservices are the modern default" | Judge styles against drivers; prefer the least complex viable target design          |
| "Defer it; we can always change later" | Assess reversal cost and timing; defer only with a viable interim design and trigger |
| "Decide everything now to be safe"     | Decide only what is needed; optional choices may be deferred with clear conditions   |
| "Splitting this unit is cleaner"       | A split needs a ranked driver that a cheaper change cannot satisfy                   |
| "Performance is surely fine"           | Evidence with a method (walkthrough, estimate, spike, measurement) is required       |
| "Skip the questions to keep momentum"  | Resolve blocking ambiguity before committing; independent analysis can continue      |

## Final Verification

- The task intent, system boundary and source of each consequential fact are clear; unresolved assumptions, targets and approval conditions are visible.
- All relevant architectural drivers are traced to design coverage and available evidence; quality scenarios have six parts or explicit, actionable missing information. Hard constraints are assessed, not silently overridden.
- Candidate comparisons address the same priority drivers; significant open choices, including architecture-level technologies, have rationale and real trade-offs. Mandated and retained existing technologies are not presented as invented competitions. Document statuses distinguish proposals, accepted decisions, design coverage and verified outcomes.
- Major elements, ownership, cross-boundary flows and release/deployment boundaries agree across views; no C4 container is equated automatically with a release unit.
- Critical change-sensitive properties have feasible checks or explicit gaps, with execution status. Deferred choices have a viable interim approach, owner and revisit signal.
- Breaking changes and migrations account for compatibility, verification, cutover, rollback/forward recovery and retirement; any required human authorization is explicit.
