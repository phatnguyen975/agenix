# Fitness Functions

Use to define **objective, repeatable checks** that detect when architecture changes threaten important qualities or design constraints. An architectural fitness function evaluates a specified architectural property; it does not by itself establish that the overall design is correct.

## Selection and Coverage

Start with **risk and drivers**, not with available tooling:

1. Choose consequential scenarios, structural boundaries, contracts, ownership rules or evolution risks that can regress.
2. Define a clear observable property, failure signal, decision owner and response.
3. Choose a suitable method and cadence. Automate when repeatable, feasible and valuable; permit manual review when an objective protocol is possible but automation is impractical.
4. Distinguish proposed checks from actually operating guardrails; do not present a plan as implemented enforcement.

Aim to cover critical quality goals **by one or more appropriate checks**, but avoid a ceremonial one-to-one mapping of every driver or ADR to an FF. A single FF may protect several drivers; a single driver may require several FFs. A qualitative architectural decision may be best guarded by a periodic architecture review with defined criteria and artifacts.

## Function Specification

Each `FF-nn` entry should state:

| Field      | Guidance                                      |
| ---------- | --------------------------------------------- |
| Purpose    | Driver/decision IDs and property guarded      |
| Check      | Method, measured population, data source      |
| Criterion  | Explicit condition, units, environment/window |
| Execution  | Stage, cadence, owner role, status            |
| On Failure | Block, alert, investigate or decide           |

Where a trigger watches _headroom_, distinguish an **early-warning threshold** from the **mandatory quality target**. Choose both with stakeholder validation when they affect decisions. Define sampling, false positives and data availability where relevant. Do not silently invent a default percentage or date.

**Example `FF-01`:**

- **Purpose:** protect `QUA-01` checkout response time.
- **Check:** load-test peak of 250 requests/s; measure p95 latency and error fraction for the checkout endpoint; include the relevant dependencies.
- **Criterion:** p95 ≤ 300 ms in the agreed five-minute window, with separately agreed error target.
- **Execution:** pre-release performance stage; owner role: performance owner; **status: planned** until configured.
- **On Failure:** block promotion and assess the regression against the architecture decision.

**Example `FF-02`:** module dependency test for `Ordering` → `Catalog`: direct imports of `Catalog` internals are forbidden; run on each build; **status: active** only when code/test evidence confirms it runs.

## Categories

These dimensions are useful labels; they are not mutually exclusive across dimensions:

- **Atomic / holistic:** one architectural characteristic or interaction versus combined end-to-end behavior.
- **Triggered / continuous / scheduled:** execute on a build, monitor ongoing behavior, or periodically re-evaluate an important property.
- **Static analysis / runtime assessment:** inspect design/code/dependency artifacts or observe a running system under representative conditions.
- **Automated / manual:** execution method. Manual checks still require criteria, cadence and a recorded outcome.

Avoid using `static` to mean "fixed threshold" and `dynamic` to mean "variable threshold"; this conflates implementation/evaluation with conditional limits. An SLO with a rolling window may be a monitoring fitness function, but an SLO alone is a goal, not evidence of an active check.

## Check Patterns by Driver

| Driver           | Suitable Guard                                 | Important Limitation                      |
| ---------------- | ---------------------------------------------- | ----------------------------------------- |
| Time Behaviour   | Representative load test, production SLI       | Test load and real traffic may differ     |
| Availability     | Good-event ratio and failure drills            | Define denominator/exclusions             |
| Recovery         | Restore test for RTO/RPO                       | A backup job alone does not prove restore |
| Modularity       | Boundary and cycle assertions                  | Static rules cannot prove maintainability |
| Modifiability    | Sample change exercises, change lead time      | Depends on change class/team context      |
| Security         | Access tests, dependency checks, threat review | Scans alone do not establish security     |
| Interoperability | Consumer/provider compatibility tests          | Unknown external consumers remain a risk  |
| Deployability    | Release/rollback rehearsal and metrics         | Pipeline success is not rollback proof    |
| Observability    | Correlation/log/metric coverage checks         | Presence of telemetry ≠ diagnostic value  |
| Data Ownership   | Access-control or dependency checks            | Does not prove consistency behavior       |

For user-facing SLOs, base measurements on **service experience** and clearly define the SLI population/window; avoid misleading averages. For distributed interactions, include negative tests (dependency unavailable, duplicate delivery, partial result, schema compatibility) where a corresponding driver exists.

## Placement and Failure Policy

- **Build or review:** fast boundary checks, cycles, architectural lint rules and contract shape checks.
- **Integration/pre-release:** contract compatibility, scenario-specific load, failover and rollback exercises.
- **Runtime:** SLI monitoring, alerting, queue depth/headroom, reconciliation lag and critical failure signals.
- **Scheduled:** backup restore, incident exercises, security/architecture reviews, deprecation checks.

Record whether a check **blocks**, **alerts**, or **opens a review**. A production alert should not automatically block deployments unless a specific policy says so. Add ownership, exception procedure and expiration for any approved waiver. Separate alert thresholds from the hard quality requirement.

## Revisit Signals for Deferred Decisions

A numeric FF can evaluate a DD when the signal is observable. Example: sustained queue lag approaches the business freshness target for two agreed observation periods; re-evaluate partitioning. Other revisit signals can be release milestones, a new regulatory requirement or a vendor contract end date; these are decision-review triggers, **not fake numeric fitness functions**.

Record each DD's **interim design, signal, owner, next step and review date/condition** in System Design §4.4. When a trigger fires, reassess options and their drivers; do not automatically execute a preselected migration.

## When an Objective Check Is Not yet Feasible

If a quality requirement cannot yet be measured reliably, do not fabricate an FF with a guessed threshold. Specify the required observation or experiment, its owner and the decision it unlocks; classify the related driver `unverified`. A manual architectural review qualifies as a repeatable guardrail only when its inputs, criteria, cadence and result record are explicit.

**Example:** a proposed independent-deployability guardrail asks whether `Catalog` can release against the supported `Ordering` contract without coordinating the other release. Initially assess this through a documented contract/release rehearsal. When it is implemented as an automated compatibility check, update the execution state and evidence rather than claiming the check always existed.

## Lifecycle and Anti-Patterns

- Mark status `planned`, `active` or `suspended` (execution method: `automated` or `manual`), with meaningful evidence for `active`. Record last result separately (`pass`, `fail`, `not run`, or unknown); an active check can fail, and a planned check cannot pass.
- Keep a source of truth for each check; define ownership of its threshold and runtime environment. If a measure is still unconfirmed, document a check proposal without inventing a pass threshold.
- Review check usefulness, flakiness, false positives and changing business drivers; retire obsolete guardrails with a documented decision.
- Reject subjective tests ("architecture is clean"), silent estimate-to-target promotion, unexecuted checks called enforced, or code coverage called a direct modifiability measure.
