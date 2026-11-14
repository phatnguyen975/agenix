# Architecture Styles

Use when architecture topology is an open, driver-significant choice. **Styles are descriptive design options, not rankings, maturity levels or mutually exclusive labels.** Deployment topology, partitioning, interaction style and data ownership are separate design dimensions.

## Distinguish the Dimensions

- **Style:** recurring overall structure and collaboration model (e.g. layered, microservices, microkernel).
- **Partitioning:** divide by business capability/subdomain, technical layer or a justified combination.
- **Granularity:** size of responsibility and independently released units.
- **Communication:** in-process, request/response, event notification or messaging; asynchronous communication does not alone imply a distributed system.
- **Deployment:** one releasable system or independently released applications/services; C4 containers can include data stores or browser/mobile applications and are not necessarily deployable server binaries.

"Event-driven" or "pipeline" can be realized inside one process or across services. Serverless/FaaS describes a hosting and execution model, not by itself a guarantee of coherent domain/service boundaries. A modular monolith can contain layers, processing pipelines, events and a plugin boundary. A distributed system can have a shared database, although that may compromise independent changes.

## Candidate Styles and Forces

### Layered

- **Structure:** modules grouped by technical responsibility (presentation, application/domain, persistence), with explicit permitted dependency directions.
- **Fit:** modest complexity and stable cross-layer conventions.
- **Watch:** feature work crossing all layers, pass-through logic, forbidden layer bypass, one release boundary if deployed together.
- **Example:** an internal workflow tool with one delivery team.

### Modular Monolith

- **Structure:** one application release unit containing bounded modules with explicit public interfaces; module ownership may follow business capabilities or other coherent boundaries.
- **Fit:** strong internal modularity with lower distributed-operating cost.
- **Watch:** module dependency cycles, accidental shared mutable state, build/release coupling, scaling all application functions together.
- **Example:** ordering and catalog modules deployed as one application.

### Hexagonal / Ports and Adapters

- **Structure:** core application/domain behavior depends on owned ports (contracts); external delivery and persistence adapters depend inward on those contracts.
- **Fit:** volatile integrations, multiple delivery channels and testable core rules.
- **Watch:** abstraction without actual variation, unclear ownership and adapters that leak external semantics into core logic.
- **Example:** keep checkout policy independent of a specific payment-provider SDK. This is primarily an internal dependency-structure pattern and may coexist with layered, modular-monolith or service-based topologies.

### Pipes and Filters

- **Structure:** processing stages linked by defined data flows (in-memory, streams or messages).
- **Fit:** transformation and batch/stream processing.
- **Watch:** failure propagation, ordering, intermediate formats, retries and backpressure.
- **Example:** validate → normalize → enrich → export documents.

### Microkernel or Plugin Architecture

- **Structure:** stable core plus independently varying extensions through governed extension contracts. Plugins may share a process or run externally.
- **Fit:** deliberate product variants or third-party extensions.
- **Watch:** API versioning, isolation, permissions, backward compatibility and core bottlenecks.
- **Example:** document editor with configurable import/export extensions.

### Service-Based Architecture

- **Structure:** a small set of coarse-grained services organized around major responsibilities, with independent deployments where needed.
- **Fit:** some isolation and separate scaling without maximal service decomposition.
- **Watch:** shared schema/database coupling, synchronous call chains and unclear ownership.
- **Example:** back office and customer-facing services sharing a legacy data platform during modernization.

### Event-Driven Architecture

- **Structure:** producers publish events and consumers react asynchronously, optionally using workflow coordination.
- **Fit:** time decoupling, multiple consumers and variable processing rates.
- **Watch:** duplicate/late/out-of-order events, delivery guarantees, eventual consistency, replay, poison messages, observability and broker availability.
- **Example:** order accepted → asynchronous fulfillment and notifications. This style can complement any deployment topology.

### Microservices

- **Structure:** separately deployable, loosely coupled business capabilities with stable contracts and logically private data.
- **Fit:** clear bounded responsibilities, genuinely independent release/scale needs, organizational and operational maturity.
- **Watch:** distributed failure, consistency, cross-service transactions, consumer compatibility, telemetry, ownership and automation. Service boundaries are not automatically one per class, entity, aggregate or bounded context.
- **Example:** high-change fulfillment and billing services with distinct release teams.

### Space-Based Architecture

- **Structure:** processing instances operate primarily against distributed/replicated in-memory state, with durable storage outside the hottest request path.
- **Fit:** exceptional variable-load scenarios with demonstrated database bottlenecks and suitable consistency tolerance.
- **Watch:** eviction, recovery, consistency, memory cost, state distribution and operational complexity.
- **Example:** a high-throughput transient session workload, only if measured requirements justify it.

## Comparison Questions

For each viable candidate, evaluate the same drivers:

| Force             | Favors Less Distribution               | May Justify More Distribution            |
| ----------------- | -------------------------------------- | ---------------------------------------- |
| Release cadence   | Coordinated team releases acceptable   | Independent release required             |
| Runtime scaling   | Whole application can scale            | Workloads differ substantially           |
| Consistency       | Local atomic operations critical       | Eventual/managed coordination acceptable |
| Failure isolation | One operational blast radius tolerable | Risk requires isolated failures          |
| Team/operations   | Limited platform capacity              | Teams support autonomous services        |

**Additional forces:** plugin extensibility, streaming throughput, integration ecosystem, security/trust zones, regulated data placement, legacy constraints and total operational cost. Do not use rules like "more than N users → microservices"; user count alone does not define an architecture style.

**Example:** a six-person team with a new order product and no measured independent-deployment need may choose a **domain-modular monolith**. A separate asynchronous worker can be added for long-running fulfillment without committing to microservices for all domains. The decision must still check quality scenarios and skills rather than treating this example as a default.

## Distributed-Systems Review

For networked candidates, specify at architecture level:

- **Failure classes:** timeout, partial failure, dependency saturation, retry storms, network partition and recovery.
- **Interaction semantics:** sync/async; idempotency, ordering, duplicate delivery and backpressure if messaging is used.
- **Consistency:** ownership, transaction boundary, propagation delay, reconciliation and compensating action where needed.
- **Observability:** cross-boundary correlation, critical service objectives and problem localization.
- **Deployment independence:** contract compatibility and whether a schema/event change forces coordinated releases.
- **Security:** identity/authentication, authorization and trust-zone crossing.

Do not assume the network is free, reliable or secure. For each remote dependency, state expected failure behavior rather than prescribing the same timeout/retry for every call.

## Avoid Misleading Shortcuts

- Do not equate **number of teams, users or database tables** with a required number of services. Independent release is a capability demonstrated by contracts, data ownership and delivery practice — not the number of running processes.
- Avoid the false choice of "one monolith or hundreds of microservices". A modular application, separate batch/worker processes, coarse-grained services and selective event flows can be combined where independently justified.
- An event broker does not guarantee decoupling: shared schemas, synchronized consumers or a required synchronous downstream response may preserve temporal or release coupling. Specify message ownership and semantics.
- A style name is not an architectural evaluation. Describe actual responsibilities, authoritative data, communication, scaling and failure boundaries in the candidate.

**Example — Mixed Style:** A single deployable ordering application owns order state, calls a payment provider synchronously for authorization, and publishes durable events to a worker for notifications. Document the synchronous checkout requirement separately from asynchronous notification behavior; do not call the whole system "microservices" because it has a worker and a queue.

## Selection Rules

1. Eliminate candidates that violate confirmed hard constraints.
2. Use prioritized scenarios to distinguish candidates and explain the smallest needed set of distribution and coordination boundaries.
3. Include operational ownership, cost, migration and reversibility in the evaluation.
4. Mix compatible styles when clearly helpful, but name which part uses which style.
5. Record a significant new style/topology decision in one ADR; do not invent an ADR for an unchanged observed as-is topology.
