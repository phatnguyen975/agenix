# Partitioning and Granularity

Use when assigning responsibilities, choosing boundaries, checking coupling and evaluating service extraction. Strategic domain concepts can inform architectural boundaries; detailed DDD tactical modeling is out of scope.

## Partitioning Choices

- **Business/domain-aligned:** group responsibilities with a shared business purpose and change pattern; favors changes contained within a capability boundary.
- **Technical/layered:** group by technical responsibility; favors consistency within technical concerns but can spread business changes across layers.
- **Hybrid:** organize domain modules internally with explicit technical layers, or isolate a shared platform function where evidence supports it.

No partition is automatically the right release boundary. Conway's law is a **design consideration**: team communication and ownership influence the architecture; inspect coordination costs and mismatches, do not use it as a deterministic formula.

## Boundary Discovery

**Candidate signals:** business capability, change cadence, domain language, data ownership, transaction invariants, security/trust zone, team ownership, scaling/failure needs and integration surface.

- **Bounded context:** a boundary of consistent domain-model meaning. A context may map to one module, multiple applications or part of a larger releaseable unit; there is no mandatory one-to-one mapping to a microservice.
- **Subdomain (core/supporting/generic):** business differentiation informs design effort and investment; it does not dictate physical decomposition.
- **Module:** cohesive unit of software responsibility with a public contract and hidden internals.
- **C4 component:** grouping within a container; not automatically a release unit.

Prefer high cohesion, explicit responsibility and minimal change propagation. Record allowed dependency directions and an owner _role_ where known. Shared utilities must not become an accidental place for unrelated business logic.

**Example:** `Catalog` and `Ordering` can be separate modules in one application, with distinct ownership of catalog and order records. Both can remain within one deployment if no independent-release driver exists.

## Coupling and Architectural Quanta

An architectural quantum (as used in evolutionary architecture literature) is an analysis lens for _independent deployability and coupling_: a functionally cohesive, independently deployable unit with tightly coupled static dependencies and synchronous dynamic interactions inside the assessed boundary. It is not synonymous with a module, C4 container, runtime instance, team or process, and real systems may not have perfectly independent quanta.

Distinguish:

- **Static coupling:** build-time/configuration/data/platform dependencies that can force coordination (e.g. shared mutable schema, library ABI, shared release infrastructure).
- **Dynamic coupling:** runtime communication dependencies. A required synchronous call can couple availability/latency during a workflow; an asynchronous link can reduce temporal coupling, but broker/schema/shared-data dependencies can still couple releases or operation.
- **Release coupling:** empirically observed or design-required coordination: can one element change, release and roll back without synchronized modification of another? A separately packaged artifact is not necessarily independently releasable.

**Do not algorithmically merge every pair of units sharing a datastore, broker or synchronous call into one quantum.** Sharing infrastructure is not sufficient evidence of lockstep deployment; a synchronous call may affect one workflow without making all releases inseparable. Instead ask:

1. Can this artifact deploy or roll back independently while contracts and required data remain compatible?
2. Which dependencies must change in lockstep under expected scenarios?
3. What runtime critical paths and failure domains are coupled, and what does that imply for driver measures?
4. Are boundaries cohesive and independently governed, or only separately packaged?

Record the meaningful result in the architecture description **only if** it changes a granularity or deployment decision. A monolith usually has one application release quantum; microservices **seek** independent quanta but can create a distributed monolith through coordinated deployment and shared schemas.

## Granularity Trade-Offs

| Reason to Split                      | Reason to Keep Together                        |
| ------------------------------------ | ---------------------------------------------- |
| Different release cadence            | Transactional invariants                       |
| Distinct scaling demands             | Frequent chatty workflows                      |
| Security or fault isolation          | High cross-module change coupling              |
| Different ownership and change rates | Shared operational/skill constraints           |
| Independently valuable capability    | Data dependencies requiring strong consistency |

A split does not automatically improve reliability: synchronous chains may preserve the failure coupling. A very cohesive component is not automatically a separate service: include operations, release automation, observability, cost and migration.

**Decision example:** order placement and inventory reservation are often revised together and require a clear oversell invariant. Keep in-process until a high-priority driver justifies separation; if split, explicitly document reservations, duplicates, failure handling, compensations and customer-visible semantics.

## Boundary Counterexamples

- **Separate modules, one release:** `Catalog` and `Ordering` have different data and public contracts but are shipped as one modular application. Domain separation does not imply independent deployment.
- **Separate processes, coupled releases:** two services both write the same business tables and require coordinated schema changes. Separate infrastructure does not prove architectural autonomy; shared private schemas or contracts with compatibility can reduce this coupling.
- **Asynchronous events, coupled operation:** a broker outage prevents all new acknowledgements because publishing has no durable handoff. The interaction looks asynchronous but the required workflow remains dependent on broker availability; analyze durability and customer-visible semantics.

## Data and Consistency Boundaries

- Assign **one authoritative writer/owner per logical data set** where independence is intended. Other consumers use owned interfaces or sanctioned published copies. A **shared physical database server** is compatible with private schemas/tables; a **shared mutable data model** can create release coupling.
- A modular monolith can use one physical database with module-owned schemas/data; direct cross-module writes still violate logical boundaries.
- For read models, decide source of truth, propagation delay, replay/reconciliation and deletion semantics. Copies do not become multiple authorities without a deliberate conflict-resolution policy.
- Where operations span independent persistence boundaries, identify consistency guarantee, idempotency, event delivery, ordering, rollback/compensation and failure recovery. Consider local transactions, sagas, outbox/inbox or API composition when the scenario warrants them; do not mandate a specific pattern.
- During migration, temporary shared access or dual writes may be necessary. Mark them as **transition exceptions** with owner, verification and retirement condition rather than presenting them as the target steady state.

## Structural Signals and Guardrails

- **Afferent coupling (`Ca`):** count of elements depending on an element.
- **Efferent coupling (`Ce`):** count of elements on which it depends.
- **Instability (`I = Ce / (Ca + Ce)`):** coupling ratio, undefined when `Ca + Ce = 0`; it is _not_ a universal quality score.
- **Cycles:** cyclic dependencies between governed modules/services. Reject them when architecture layering or autonomy requires an acyclic graph.
- **Change coupling:** percentage of relevant changes spanning boundaries, or releases requiring coordination; often more directly useful than static counts.

Choose measurement scope and thresholds per project; do not assert that lower coupling numbers always mean better quality. Example fitness rule: "`Ordering` must not import `Catalog` internals; dependencies use the published module contract" (checked at each build). See `fitness-functions.md`.
