# Quality Attributes

Use to turn stakeholder expectations into assessable architectural requirements, select tactics, and expose trade-offs. ISO/IEC 25010 provides a **product quality vocabulary**; it is not a complete architectural design method or a mandatory classification for every operational concern.

## Product Quality Vocabulary

The ISO/IEC 25010 product quality model includes nine characteristics. Use the applicable characteristic/subcharacteristic consistently rather than relabeling stakeholder language without explanation.

- **Functional Suitability:** functional completeness, functional correctness, functional appropriateness.
- **Performance Efficiency:** time behaviour, resource utilization, capacity.
- **Compatibility:** co-existence, interoperability.
- **Interaction Capability:** appropriateness recognizability, learnability, operability, user error protection, user engagement, inclusivity, user assistance, self-descriptiveness.
- **Reliability:** faultlessness, availability, fault tolerance, recoverability.
- **Security:** confidentiality, integrity, non-repudiation, accountability, authenticity, resistance.
- **Maintainability:** modularity, reusability, analysability, modifiability, testability.
- **Flexibility:** adaptability, scalability, installability, replaceability.
- **Safety:** operational constraint, risk identification, fail safe, hazard warning, safe integration.

This model is a reference, not a checklist demanding nine requirements. For example, "observability" is an architectural/operational concern typically supporting analysability; "resilience" involves fault tolerance, recoverability and possibly availability; "deployability" overlaps installability, automation and release risk. Keep the operational term in the scenario while noting the relevant quality attribute. **Privacy, cost, regulatory compliance, sustainability and time-to-market** can involve multiple attributes and/or separate constraints; do not force them into a single ISO label.

## Quality Scenario Construction

Use six parts (SEI/Software Architecture in Practice):

| Part             | Question               | Typical Content                           |
| ---------------- | ---------------------- | ----------------------------------------- |
| Stimulus Source  | Who/what causes it?    | Client, engineer, component, attacker     |
| Stimulus         | What happens?          | Request, failure, change, malicious input |
| Environment      | Under what conditions? | Peak load, degraded state, release window |
| Artifact         | What is affected?      | System, interface, service, data store    |
| Response         | What should happen?    | Respond, isolate, recover, reject, adapt  |
| Response Measure | How is success judged? | Target, unit, workload, percentile/window |

Six parts can be written in prose; avoid a six-column table. **Source of the requirement** (stakeholder, document) is additional provenance, not the scenario's **Stimulus Source**. Record baseline and target separately.

Good measures specify the viewpoint and population, a boundary, time/window and necessary workload where relevant. For errors and availability, define eligible events and exclusions. Distinguish an agreed target from an estimate, a forecast and an observed measurement. If the response target is unknown, record `target unconfirmed` and bring it to Human Gate A; do not pick arbitrary numbers to satisfy the template.

**Additional scenario considerations:** For authorization, state attacker/actor, protected resource, trust boundary, requested action, reject/audit behavior and the observable criterion. For compatibility, state producer/consumer revisions, overlapping deployment conditions and what continues to work during migration. For data freshness, define update stimulus, consumers, normal/degraded operation and the maximum tolerated lag.

### Worked Scenarios

These are illustrative scenarios; their targets and workloads are not project defaults.

**QUA-01 — Performance Efficiency / Time Behaviour**

- **Stimulus Source:** signed-in customer.
- **Stimulus:** submits a checkout request.
- **Environment:** peak load of 250 requests/s, healthy region, 5-minute measurement window.
- **Artifact:** checkout interface and its required dependencies.
- **Response:** acknowledges a valid order or returns an explicit business rejection.
- **Response Measure:** p95 end-to-end response ≤ 300 ms over eligible requests, with request failures measured separately.

**QUA-02 — Reliability / Recoverability**

- **Stimulus Source:** infrastructure fault.
- **Stimulus:** primary instance becomes unavailable.
- **Environment:** production during ordinary operation.
- **Artifact:** order persistence capability.
- **Response:** fail over and restore order processing without unacknowledged data loss beyond the agreed bound.
- **Response Measure:** recovery time ≤ 5 minutes and recovery point ≤ 1 minute, measured by a restore exercise.

**QUA-03 — Maintainability / Modifiability**

- **Stimulus Source:** product team.
- **Stimulus:** requests support for another payment provider.
- **Environment:** routine development with established interfaces.
- **Artifact:** payment integration boundary.
- **Response:** add and verify the provider without modifying checkout core behavior.
- **Response Measure:** ≤ 3 engineer-days; existing payment adapters require no changes. The effort target is assessed over multiple changes, not inferred from a static diagram.

## Common Measures and Interpretation

| Concern             | Useful Measure                      | Required Qualification                |
| ------------------- | ----------------------------------- | ------------------------------------- |
| Latency             | p95/p99 duration                    | Operation, clients, workload, window  |
| Throughput/Capacity | successful work per second          | Latency/error limits at that load     |
| Availability        | good events / eligible events       | Service boundary and rolling window   |
| Recovery            | RTO and RPO                         | Incident class, data scope, exercise  |
| Modifiability       | effort, time, affected modules      | Defined change class and measurement  |
| Security            | blocked unauthorized paths          | Attack/authorization scenarios, scope |
| Interoperability    | compatible consumer contracts       | Supported revisions and consumers     |
| Deployability       | rollout/rollback time, failure rate | Environments and release mechanism    |

A metric that measures a _proxy_ (code coverage, coupling count, incident count) is not automatically proof of the real-world quality target. Pair proxy indicators with outcomes when reasonable. For runtime reliability, distinguish a **service level indicator** (measurement) from a **service level objective** (target); they are not synonyms for fitness functions.

## Tactics and Architectural Options

A **tactic** is a design choice intended to influence a quality attribute response; it does not guarantee that the response target is met. Choose tactics at the relevant system element, assess side effects and link significant choices to ADRs.

| Quality Concern  | Candidate Tactics                                                           | Principal Trade-Off                 |
| ---------------- | --------------------------------------------------------------------------- | ----------------------------------- |
| Performance      | Cache, bound queues, reduce work, scale resources, partition hot work       | Staleness, cost, complexity         |
| Availability     | Monitor faults, redundancy, failover, isolate faults, degrade gracefully    | Cost, coordination, consistency     |
| Modifiability    | Encapsulate, restrict dependencies, improve cohesion, late binding          | Indirection, maintenance            |
| Security         | Least privilege, validate input, isolate trust zones, encrypt, audit        | Complexity, latency                 |
| Testability      | Control state, replace dependencies, observe outcomes, limit nondeterminism | Extra seams, maintenance            |
| Recoverability   | Restore, replication, recovery orchestration and exercises                  | Data loss trade-off, operating cost |
| Interoperability | Contract boundaries, adapters, backward-compatible evolution                | Translation cost, version support   |
| Scalability      | Horizontal scaling, partitioning, load shedding, async buffering            | Ordering, state, cost               |

For scenario-specific designs, also consider safety, correctness, usability or other attributes that cannot be reduced to the short tactic list. Do not assume a tactic is free or required just because it appears here.

## Tactic Selection by Failure or Change Mechanism

For a high-priority scenario, locate the actual constraint or failure mechanism before choosing a tactic. The following distinctions prevent pattern-name selection from substituting for analysis:

- **Performance and capacity:** distinguish latency caused by computation, contention, queueing, network hops and data access. Reduce unnecessary work or demand first; then evaluate caching, concurrency, resource scaling or partitioning. A cache must specify freshness/invalidation; buffering must specify backpressure, durability and what the caller is told.
- **Availability and recoverability:** distinguish fault detection, isolation, continuation and restoration. Replication alone does not guarantee failover, recoverable data or an acceptable RTO/RPO. Specify fault scope and test a representative loss/recovery path.
- **Modifiability and adaptability:** localize changes through cohesive responsibilities, stable interfaces, dependency direction and explicit extension points. Consider the change class, the number of elements touched and migration of existing consumers; generic layering is not automatically modifiability.
- **Security and accountability:** identify assets, actors and trust boundaries; define authentication, authorization ownership, least privilege, information flow and audit obligations. Encryption alone does not demonstrate access control, and a successful scanner result does not establish security.
- **Testability and diagnosability:** establish controllable boundaries, observable outcomes and reproducible failure modes; isolate nondeterministic dependencies where architecturally warranted. Logs without correlation or a diagnostic objective do not prove observability.
- **Interoperability and deployability:** define published contracts and supported compatibility periods, version changes, independently releasable boundaries and safe rollback. An API version label alone does not guarantee old consumers keep working.

**Example — Choosing a Tactic:** If a new external payment provider must be added without modifying core checkout behavior, place provider-specific translation behind an owned integration boundary. Evaluate adapter contract changes against `QUA-03` and test one representative provider addition; do not assume that adding an abstraction proves the engineer-day target.

## Architectural Trade-Off Analysis

- **Latency versus isolation/security:** extra hops, authorization and encryption have possible time/operational cost; measure rather than assume a violation.
- **Availability versus consistency:** describe desired behavior under _specific faults_. CAP theorem only constrains the trade-off in the presence of a network partition; it does not mean all distributed systems permanently choose "availability" or "consistency".
- **Independent deployability versus cross-service coordination:** splitting units may improve independent release and scaling while complicating contracts, transactions and troubleshooting.
- **Reliability versus feature velocity/cost:** redundancy and stronger recovery measures consume resources; agree priorities and service objectives.
- **Modifiability versus performance:** abstraction and indirection can alter critical-path latency; trace actual paths.

For each tension, name driver IDs, articulate options and operational consequences, assess against the scenario measures, and send unresolved priorities to the human. Recheck in `design-iteration.md` after architecture changes.
