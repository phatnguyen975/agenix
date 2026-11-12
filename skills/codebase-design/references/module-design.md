# Module Design

## Purpose

Determine cohesive architectural modules: **what each module owns, what it hides, how consumers interact with it, and when it should be split or merged**. Do not invent bounded contexts, entities, aggregates, or business rules; use them when established by existing domain documentation.

## Identify Candidate Modules

1. Extract responsibilities/capabilities from requirements, existing code, and domain decisions. Identify actual consumers, owners, and likely changes.
2. Identify design decisions that may change independently: algorithms, representations, persistence choices, integrations, validation policies, and interaction protocols.
3. Group code that must share those decisions, invariants, or lifecycle. Separate responsibilities where consumers and change drivers are substantially different.
4. Prefer names from the project's established vocabulary. A boundary can be a package, build module, namespace, directory plus import rule, or a published library; specify how it is made real.
5. Check interfaces, coupling, and change history (when available), not merely folder size. Treat proposed boundaries as hypotheses until imports and use cases support them.

**Example:** Order creation and order retrieval might belong to one `Orders` module if both share invariants and persistence ownership. They need not become separate modules merely because they are different endpoints. `Notifications` may be separate when its transport policy and providers change independently.

For a **consequential** boundary proposal, present the candidate responsibility, key change driver, intended public consumers, hidden implementation decisions, owner (if known), and **one plausible alternative**. For example, splitting `Notifications` is useful when its provider changes independently; keeping it inside `Orders` may be simpler when it is a private, stable implementation detail. Do not treat the split as approved before explicit confirmation or an existing binding project decision is identified.

## Split, Merge, or Retain

| Signal                                                             | Consider                   | Countercheck                                                               |
| ------------------------------------------------------------------ | -------------------------- | -------------------------------------------------------------------------- |
| Unrelated responsibilities or independently changing decisions     | Split                      | Will the new boundary require many cross-module calls?                     |
| Different owners or access requirements                            | Split or isolate           | Does the split duplicate an invariant or require distributed coordination? |
| Clients depend on unrelated parts of an API                        | Split interface or module  | Would smaller consumer-specific exports solve it?                          |
| Modules always change together and exchange implementation details | Merge                      | Are they genuinely cohesive, or merely under-defined?                      |
| Interface mostly forwards calls without hiding decisions           | Merge/remove facade        | Does the facade protect a meaningful external/volatile boundary?           |
| Existing module is large                                           | Do not split by size alone | Is cohesion or change locality actually poor?                              |

Do not turn the Single Responsibility Principle into "one class/function/folder per reason anyone might imagine". The unit of change should be meaningful to the project.

## Information Hiding and Public Interfaces

**Parnas' criterion:** organize modules around decisions likely to change rather than runtime processing steps. A useful module allows a consumer to rely on a stable concept without knowing its storage, algorithm, or integration details.

For each module record:

- **Responsibility:** what it owns, explicitly excluding adjacent responsibilities when confusing.
- **Consumers:** other architectural modules or release units that need it; name internal callers only when they constrain the boundary.
- **Public surface:** exported operations/types/events or `Internal only` if no cross-boundary consumer exists.
- **Hidden decisions:** implementation choices and mutable state ownership that should not leak; omit exhaustive implementation details.
- **Error/compatibility behavior:** conceptual error categories and compatibility guarantees when needed by clients.
- **Owner and dependency permissions:** when known, plus enforcement boundary.

The interface includes observable behavior and guarantees, not only function signatures. Keep exports minimal and use stable, consumer-meaningful concepts. Do not expose persistence objects or third-party types unnecessarily. An internal helper **does not need a manufactured public API**.

Favor a **deep module** when possible: a small interface that hides substantial useful complexity. A shallow wrapper that mirrors its dependency often increases navigation and coupling without protecting a design decision. Depth is a qualitative check, not a demand to make every module large or generic.

**Example:** `DocumentStore.save(document)` can hide serialization, retryable storage interactions, and format migration; a wrapper that exposes every method of one storage SDK hides little and can change whenever that SDK changes.

**Example (conceptual):**

```text
Orders
  Public: placeOrder(command), getOrder(id), OrderNotFound
  Private: persistence representation, provider SDK, internal workflow
  Consumers: Checkout, Admin
  Depends on: Inventory public interface, Payments public interface
```

The example does not prescribe domain fields, API wire format, or folder names.

## Cohesion, Coupling, and Stability

- **Cohesion:** related logic and the decisions it must share are owned together.
- **Coupling:** fewer knowledge dependencies across boundaries; count both import references and behavioral assumptions.
- **Change locality:** a feature or policy change affects a small, predictable set of modules.
- **Stability:** an interface with many consumers is costly to change. Put volatile details behind appropriately stable boundaries; do not label a whole module stable only because it changes infrequently today.
- **Acyclic dependencies:** prefer directed static dependencies among architectural modules; cycles suggest unclear responsibility or abstraction placement. Runtime request/response and notifications need not mirror static import direction.

Robert C. Martin's package cohesion principles (REP, CCP, CRP) are heuristics for **reuse/release, common change, and common use**. Review incoming and outgoing static dependencies when evaluating stability, but do not impose a universal numeric threshold or mistake graph counts for a complete cohesion assessment.

## Interaction Styles

| Style             | Static Dependency / Ownership                                                                          | Use When                                                                    |
| ----------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| Direct call       | Caller imports callee's public surface                                                                 | Synchronous capability is needed; boundaries are in one process/build graph |
| Event publication | Publisher owns event vocabulary; subscribers depend on the published contract, not publisher internals | Observers react independently and runtime coupling is acceptable            |
| Orchestrator      | Coordinator imports capabilities of participants; participants need not import each other              | A flow spans several responsibilities                                       |
| Port with adapter | Core owns the needed abstraction; adapter implements it, composition wires them                        | External implementation should be replaceable or isolated                   |

Do not assume an event removes all coupling: payload compatibility, ordering, retry, and ownership still matter, but detailed delivery architecture is outside this skill.

## Resolve Cycles

Inspect actual edges and strongly connected components; a cycle at function/runtime level is not automatically a cycle between **static architectural modules**.

1. Reassign a misplaced responsibility to eliminate the back-edge.
2. Move a genuinely shared abstraction or invariant to the module that owns it, or to a small shared dependency if justified.
3. Invert a static dependency with a consumer-owned port **when** inversion protects an important boundary.
4. Merge modules if the apparent boundary splits one indivisible responsibility.

**Example (static module graph):** `Orders → Notifications → Orders` occurs because `Orders` calls the notification implementation while `Notifications` imports order persistence. One remedy is for `Orders` to publish `OrderPlaced` through an event-publisher port or infrastructure-neutral dispatcher, while `Notifications` consumes the published event contract without importing `Orders` internals. After the change, verify that `Orders` has **no static import of `Notifications`** and `Notifications` does not import order internals; adopting events alone does not eliminate a dependency cycle. Alternatively, use a third-party orchestrator depending on both public interfaces if synchronous coordination is required.

## Boundary Confirmation

Before confirming a consequential boundary, clarify uncertain responsibility, ownership, consumers, or constraints with the human. At the structural decision checkpoint, present **proposed modules, consumers, visibility, important allowed edges, and the trade-off against a plausible merge/split**. Confirm the choice before deriving detailed `DR-xx` constraints or assuming proposed paths are exported. Clarify newly discovered material ambiguities and return changed approved choices for targeted confirmation. An internal-only module needs no invented cross-module API.

## Boundary Review Questions

- Can one module be changed or tested without understanding another module's internals?
- Does the interface reveal implementation representations or allow unauthorized writes?
- Are two modules separated only by pass-through calls?
- Do consumers rely on undocumented initialization order, global state, or hidden data structures?
- Is a shared concern owned by a specific module with clear consumers?
- Is the selected boundary supported by a real visibility or dependency mechanism?
