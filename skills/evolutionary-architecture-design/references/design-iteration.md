# Design Iteration

Use when deriving architectural drivers, comparing baseline candidates, timing consequential decisions, evaluating architecture-level technology choices or refining an evolving architecture. The sequence adapts **Attribute-Driven Design** to select relevant drivers and architectural elements, choose design concepts, instantiate responsibilities/interfaces, analyze against scenarios, record decisions and repeat. It is a design method, not a claim of formal ADD conformance.

## Driver Identification

| Type       | Prefix | Include When                                                               | Detail Location     |
| ---------- | ------ | -------------------------------------------------------------------------- | ------------------- |
| Functional | `FUN`  | A use case materially changes boundaries, flows or responsibilities        | System Design §1.1  |
| Quality    | `QUA`  | A quality scenario constrains architectural choices                        | System Design §10.2 |
| Constraint | `CST`  | A genuine non-negotiable limit on viable design                            | System Design §2    |
| Concern    | `CNC`  | A stakeholder concern demands architecture analysis not captured elsewhere | System Design §1.3  |

- Give every architecturally significant driver a stable ID, concise statement, stakeholder/source and applicability horizon. Do not turn every feature into a driver.
- A desired or preferred technology is a preference/option until a stakeholder authorizes it as a constraint. Policies, regulations and contractual requirements may contain both a constraint and a measurable quality obligation; record each without duplicating the same driver.
- Stakeholder concerns are broader than constraints. Avoid creating a separate `CNC` entry when it merely repeats an existing `QUA` or `FUN`.
- Quality scenarios have source, stimulus, environment, artifact, response and response measure (`quality-attributes.md`). A missing target is `unconfirmed`, not an estimated fact.

## Prioritization and Trade-Offs

Assess drivers with stakeholders; keep the method simple and transparent:

| Rating                   | Interpretation                             | Example                                    |
| ------------------------ | ------------------------------------------ | ------------------------------------------ |
| Importance               | Impact on stakeholder or system success    | Lost orders would be critical              |
| Architectural Difficulty | Risk, uncertainty or cost of fulfilling it | Multi-region consistency is uncertain      |
| Timing                   | When the requirement must hold             | Launch, forecast growth, future regulation |

Rate **Importance** and **Architectural Difficulty** as `High`, `Medium`, or `Low`. Prioritize architectural drivers based on both ratings, using timing and dependencies to refine their order. Apply judgment when priorities conflict and document the rationale. Treat hard constraints as pass/fail feasibility conditions rather than ranking them as alternatives. Surface stakeholder disagreements and request a decision instead of resolving them silently.

Select **up to five** top quality goals for the executive overview when practical; that presentation limit does not remove lower-ranked quality scenarios. A goal can relate to several scenarios. Record tensions with the IDs of affected scenarios and the likely cost/risk (e.g. stronger isolation versus latency). No fixed margin/headroom percentage is universal.

**Example:** `QUA-01` requires p95 checkout latency ≤ 300 ms at 250 requests/s at launch; `QUA-02` requires completion of acknowledged orders during a 10-minute downstream outage. A direct synchronous call can favor simple immediate responses but may violate `QUA-02`; queueing can protect acceptance but changes consistency and confirmation semantics. The scenarios require distinct responses; do not merely pick "event-driven" from a label.

## Baseline and Candidate Evaluation

**Existing system:** discover actual topology, release units, external dependencies, data ownership, operational boundaries and failure modes from code, diagrams, configurations and observability where available. Separate `observed as-is`, `proposed target` and `transition`. An observed current solution is not automatically fit for the new drivers. Preserve documented rationale; do not invent missing reasons.

**New system:** compare at least two _meaningfully different, viable_ candidates when a structural choice remains open. If every meaningful dimension is constrained, record the dictated baseline and assess its consequences; do not fabricate an alternative. For large systems, compare at an appropriate scope, not all possible architecture styles.

**Candidate evaluation procedure:**

1. Identify candidate style, module boundaries, C4 containers, deployable units, data ownership and cross-boundary calls.
2. Reject violated hard constraints or escalate their conflicts; do not treat them as weighted preferences.
3. Walk the highest-priority functional and quality scenarios through each candidate, including failure modes. Mark provisional coverage `addressed` / `gap` / `unverified` and explain the evidence and remaining risk; do not use `accepted-risk` before human authorization.
4. Compare operational burden, deployment coordination, coupling, data consistency, team skills, cost, reversibility and migration effort. Use an evidence statement, not fabricated numerical scores.
5. Select the **least complex candidate with acceptable evidence** for the prioritized drivers and constraints. If none suffices, surface the unresolved trade-off for human approval instead of asserting an infeasible baseline.

**Example candidate comparison:**

| Candidate                       | Strength                           | Limitation                         | Verdict                              |
| ------------------------------- | ---------------------------------- | ---------------------------------- | ------------------------------------ |
| Domain-modular monolith         | Simple release, local transactions | One scaling/release boundary       | Prefer if QUA-01/02 are attainable   |
| Independently deployed services | Isolates releases and scaling      | Network faults, cross-service data | Use only if a driver needs isolation |

Record explicitly _why_ a split is warranted; an architectural quantum or bounded context is not automatically one service. See `partitioning-and-granularity.md`.

## Decision Timing and Reversibility

Classify candidate decisions by **cost and risk of reversal** in the project, considering external consumers, migrated data, contracts, trust boundaries, release coordination, team responsibilities, vendor lock-in and recoverability. There is no universal list that makes every database or protocol choice irreversible.

- **Decide now:** a decision blocks the next architectural step, or postponement increases risk/cost beyond the value of new information; record an ADR when architecturally significant.
- **Defer safely:** a choice is not currently necessary, an interim approach is viable, and it can be revisited before a deadline/risk boundary. Record a `DD` with owner and revisit criterion.
- **Investigate first:** uncertainty is high and the consequence is material; request a spike, experiment or measurement, and do not pretend its outcome is known.

Apply this timing assessment to structural and technology decisions alike. Reversibility controls when a decision needs to be made; it does not determine whether a technology choice needs evaluation.

## Architecture-Level Technology Evaluation

Evaluate a technology choice when it materially affects architectural drivers, system boundaries, external contracts, data ownership, integration, deployment or operational risk. Examples include a primary data store, messaging platform, runtime platform or external protocol. Exclude routine libraries and internal frameworks unless they have such an architectural impact.

1. **Classify the choice.** A mandated technology is a hard constraint: trace its `CST` ID and assess feasibility and risks without inventing alternatives. A retained existing technology needs an as-is evidence source and reassessment against changed drivers, not a retrospective ADR. An open choice requires evaluation; a stakeholder preference alone is not a mandate.
2. **Identify viable options.** Compare at least two meaningfully different options when they exist, including retaining the current technology in a brownfield system when viable. If only one option survives constraints, explain why others are infeasible instead of manufacturing a competition.
3. **Evaluate against drivers.** Use the same relevant functional and quality scenarios and hard constraints for each option. Consider integration/data semantics, security and compliance, reliability, operational effort and observability, team expertise, maturity/support, licensing and total cost of ownership, and lock-in or migration/exit effort where relevant. Reject hard-constraint violations rather than averaging them into preference scores.
4. **Verify consequential claims.** Ground capabilities, compatibility and support status in authoritative product documentation and project evidence. Use a representative experiment or measurement when a high-impact performance or failure claim remains uncertain. Label unsupported assumptions `unverified`; do not invent benchmark results or hardcode versions.
5. **Record the outcome.** Propose a selection with its rationale, evidence, trade-offs and affected boundaries; create an ADR when the new decision is architecturally significant. Obtain human authorization when required by `SKILL.md`; until then keep the ADR `proposed`. For a safely postponed choice, record a `DD` and revisit signal instead of claiming a selection. A mandated or unchanged existing technology does not, by itself, require a new ADR.

**Example:** For reliable background processing, a database-backed work queue and a managed messaging service may both be viable. Compare expected workload, retry/idempotency semantics, failure recovery, operational dependencies and cost against the actual drivers. A separate broker is not automatically preferable, and neither option's behavior is considered verified without supporting evidence.

Technology evaluation can change a structural candidate, and a structural decision can narrow technology options. Revisit affected choices as part of the refinement loop rather than treating technology selection as an isolated, one-time phase.

## Refinement Loop

1. **Select:** choose the highest-impact unaddressed/gap driver or uncertain interaction, and the architecture element(s) to design or refine. Group related drivers and elements when one scenario spans several boundaries.
2. **Evaluate:** use scenario walkthrough, dependency analysis, basic estimation, threat/failure analysis, experiment or measurement. Cite inputs and assumptions. Measurement is not automatically more informative than a correct scenario walkthrough; choose the method that fits the claim.
3. **Design:** choose feasible tactics or structural concepts; allocate responsibilities, define the affected interfaces and interactions, and update the candidate. Prefer the least disruptive design supported by the scenario. Consider scaling, isolation, asynchronous work, data ownership and operational burden as trade-offs.
4. **Record:** create or revise an ADR for a significant newly made decision. Update boundaries, runtime/deployment views, architectural policies and intended verification.
5. **Reassess:** check the selected driver and affected earlier drivers, including cost, consistency, availability, security, contracts and constraints. Reopen any driver whose design evidence is invalidated.
6. **Decide disposition:** `addressed`, `gap`, `unverified` or `accepted-risk` as defined in `SKILL.md`; show evidence level. If unresolved gaps block acceptance, return to the human with options, not another unbounded loop.

**Exit:** all high-priority drivers have credible design coverage and a validation approach, or remaining gaps are documented and escalated to the responsible human without claiming approval. An authorized risk acceptance does not override a non-waivable constraint. For a review-only task, exit with assessed coverage, evidence limits and actionable findings; do not demand a new design or ADR. Lower-priority drivers remain traceable with honest statuses. No status implies production tests passed.

## Deferred Decisions and Revisit Signals

A deferred **decision** is distinct from a deferred **requirement**. Record `DD-nn` in System Design §4.4 with:

- Decision not taken; reason to wait and safe interim approach.
- Driver/constraint IDs and the latest date or condition by which a choice becomes necessary.
- **Signal:** observable metric/threshold, delivery milestone, dependency event or review date. Name a fitness function only if one actually measures the signal.
- Owner role, next investigation/decision and estimated migration/rollback implications.

**Example:** `DD-01` — defer search-index separation while observed query latency meets `QUA-03`. Review if p95 query latency approaches the agreed response threshold for two consecutive reporting windows or when the forecast workload changes. Interim approach: keep search in the existing store; owner: architecture owner; next step: measure query profiles and compare alternatives. The signal is a _proposal_ until the human agrees the threshold/window.

Do not defer a currently violated mandatory requirement by giving the intended fix a DD ID. A fired signal **prompts re-evaluation**, not automatic implementation of the originally imagined solution.

## Change Classification and Human Gates

A change is `compatible` when existing consumers, release units and relevant behavioral guarantees can continue without coordinated modification; it is `breaking` when consumers or data must change together or an exposed contract/operational guarantee is invalidated. Changing an agreed quality target additionally requires stakeholder approval, even if the software interfaces remain compatible. A new service can be compatible; a one-line schema change can be breaking.

For breaking changes, present affected consumers, data and semantics, existing ADRs, transition states, dual-operation/compatibility policy, verification, rollback/restore plan and residual risk. Ask the human before finalizing. A provisional architecture agreement is not authorization for irreversible cutover. After approval, accept the new ADR and supersede the prior accepted record rather than rewriting its historical rationale.

## Applying the Loop to Different Tasks

- **Greenfield design:** turn requirements into drivers; compare meaningful baseline options; refine high-risk scenarios; record a proposed target and appropriate verification plan. **Example:** two modules in one application versus two independent services should be compared on actual release, failure and consistency needs — not generic microservice advantages.
- **Existing-system evolution:** reconstruct current boundaries; compare the current system against new drivers; decide the smallest safe structural change; plan transition/retirement and recheck previously satisfied scenarios. **Example:** move only a high-change search capability behind a compatible contract before considering a separately deployed service.
- **Focused review:** evaluate the specified decision against documented drivers and evidence; report what passes, what fails and what cannot yet be shown. Do not invent an architecture redesign for a narrow assessment or demand approval for observations.

For an end-to-end engagement, use the checkpoints in `SKILL.md`. For a focused task, use the relevant subset; stop only the decisions that genuinely require missing authority or information.

## Review Checklist

- Sources and evidence levels trace to each key driver and choice.
- Every hard constraint is explicitly checked; uncertain compliance is not recorded as passed.
- Viable candidates are evaluated on the same priority scenarios and realistic operations.
- Architecture-level technology choices are classified as mandated, retained existing or open; material comparisons and claims have evidence.
- Required quality targets are not overwritten to make a candidate look compliant.
- Revisions revisit affected drivers; failures and trade-offs are recorded rather than concealed.
- DD signals include owner, interim behavior and next action; only real fitness checks are referenced.
