# Dependency Rules, Shared Code, and Contracts

## Purpose

Specify what code may depend on, how modules protect internal implementations, how shared code is admitted, and how independently evolving units preserve contract compatibility. A **static dependency** (import, type reference, link, declared build dependency) is different from a **runtime interaction** (HTTP call, message, callback). Import graphs and declared build graphs are also different evidence sources; choose which a rule constrains. Choose the exact relation a rule governs.

## Define the Dependency Model

Record the following when material:

| Dimension            | Required Decision                                                                                                                                     |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Node                 | Module, build package, release unit, or named layer; use unambiguous paths/identifiers                                                                |
| Edge                 | Direct source/type import, declared build dependency, or transitive dependency; name the selected graph. Keep runtime interactions in a separate view |
| Visibility           | Which exports/entry points are public, internal, or restricted                                                                                        |
| Allowed direction    | Allowlists, groups/tags, or explicit forbidden edges                                                                                                  |
| Cycle policy         | Which architectural graph must be acyclic; separately handle cycles within one module if useful                                                       |
| Scope and exceptions | Who may bypass a rule, why, and when the exception will be revisited                                                                                  |

An architecture module may span multiple language packages; tools that only inspect package-level imports cannot automatically prove a higher-level assertion without a package-to-module mapping.

## Rules and Identifiers

For an adopted or proposed design document, assign unique, stable `DR-xx` IDs to cross-module dependency constraints. A Review may cite these rules when reporting violations, but must not treat a suggested new constraint as already binding. Examples:

| ID    | Rule                                                                                                                                            | Static Evidence                               |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| DR-01 | Code outside `Orders` may import only the `Orders` public entry point.                                                                          | Import targets and exported paths             |
| DR-02 | `Orders/Core` must not import from `Orders/Adapters`.                                                                                           | Source import graph                           |
| DR-03 | Architectural modules must not form a directed static cycle.                                                                                    | Strongly connected components of module graph |
| DR-04 | `Client` must not statically import `Server` implementation; shared protocol definitions may be consumed via their published contract artifact. | Build/import dependency graph                 |

Names in examples are illustrative, never required naming conventions. For a non-mechanically-testable policy (e.g., avoiding inappropriate data sharing), define a reviewable criterion and map it honestly to enforcement. Avoid unbounded statements such as "all dependencies must be clean".

## Module Dependency Policy

- **Default:** one module may use another module only through the other's intended public surface. An internal-only module can be consumed only by its declared owner or composition scope.
- List **permitted direct** cross-module dependencies in the Module Catalog when the set is manageable; for an existing codebase, do not treat permission as proof the edge currently exists. For large graphs, use allowed dependency groups and explicit exceptions; define the allowed graph in one canonical place.
- Do not list same-module imports as cross-module dependencies. Distinguish external third-party packages from internal modules; define third-party restrictions only where useful to boundary integrity.
- An orchestrator can depend on several module APIs; participants need not depend on the orchestrator.
- An outbound adapter can import a core-owned port; the core need not import the adapter. Runtime execution may still call the adapter via the port.
- Prefer an acyclic module graph. Detect strongly connected components over the actual static graph; review compiler/build-generated edges and cross-language references separately.

**Example:**

```text
Checkout        ---->  Orders/Public
Orders/Core     ---->  Inventory/Public
Orders/Core     --X->  Inventory/Internal  # forbidden internal import
Orders/Adapter  ---->  Orders/Core/Port    # port is owned by Orders
```

This diagram illustrates **static** dependency direction (the `--X->` edge is prohibited), not the sequence of runtime calls. It is not a claim that a module must always import only toward a single technical layer.

## Layers and Ports

- **Layered:** explicitly specify allowed static edges for each layer. Define any open/closed layer _access path_ separately from static reference direction.
- **Ports and adapters:** the core owns required abstractions and does not import adapter implementation. Concrete adapters depend on those abstractions, with application-level composition or framework configuration resolving implementations.
- **Simple modules:** avoid rules for layers that do not exist.
- **Feature/component modules:** require public-entry access where the language/build system can express it; do not mandate a specific export filename.
- **Slices:** whether slices are top-level use-case grouping or internal to a capability, avoid importing another slice's implementation; give shared invariants one owner and consume them through an intentional surface.
- **Test support:** production sources never import test-only helpers; tests may access their _own_ module internals as allowed by language/test tooling.

## Shared Code Admission

Sharing has distinct levels:

1. **Within one module:** ordinary implementation reuse; keep details private.
2. **Across modules in one release unit:** reuse only stable, genuinely shared capabilities; assign an owner and narrow public surface.
3. **Across release units in one repository:** a reusable package/library or contract with declared consumers and controlled dependency direction.
4. **Across repositories:** published, versioned artifact or protocol/contract; do not presume file-copy sharing.

Admit a shared package when it offers a coherent responsibility **and** the benefits of one source of truth outweigh cross-consumer coordination costs. No universal "two consumers required" test: a carefully justified shared contract may exist before a second concrete consumer; speculative general-purpose utility packages are still discouraged.

**Required shared-code policy:** purpose, owner, permitted content, public surface, consumers, dependency direction, compatibility/release policy (when independent), and change verification. Reuse of small implementation details may be cheaper through intentional duplication if the owners' change paths differ.

**Good example:** `Money` value semantics shared across two packages with one agreed owner and strict public API. **Bad example:** global `common/` where unrelated business helpers, environment variables, and persistence details accumulate without ownership.

## Contracts Across Release Units

A contract may be:

- A **published library/package API** (public exports and compatibility guarantees),
- A **service/protocol contract** (API schema, messages, events, or wire semantics), or
- A **shared interface definition** deliberately published separately from implementations.

Record **owner, consumers, source location, artifact or discovery path, compatibility policy, verification responsibility, and release coordination**. A contract does not always require a separate `contracts/` repository or package. Provider-owned definitions, generated client libraries, or shared schemas are choices conditioned on tooling and governance. Do not move provider internals to a shared package.

**Cross-unit integration policy:** consumers rely only on the published contract, not implementation paths; the provider owns its internals. Runtime connectivity is documented at the boundary level, not as a detailed API design.

## Compatibility and Versioning

- For independently published packages using **Semantic Versioning**, first declare the public API: `MAJOR` for incompatible changes, `MINOR` for backward-compatible additions/deprecations, and `PATCH` for compatible bug fixes. A released version is immutable.
- For `0.y.z` packages, Semantic Versioning treats the public API as unstable; do not present `MAJOR`/`MINOR` guarantees as binding in that phase.
- **Do not automatically apply SemVer to every service protocol or monorepo-internal module.** Use the project's actual protocol compatibility and release strategy; schema compatibility may have different rules for reads/writes or asynchronous consumers.
- Prefer compatible-first evolution of published interfaces: expand support, migrate consumers, remove the old behavior after compatibility is verified (parallel change).
- Shared-repository changes may be atomically committed, but independently deployed/released consumers can still require a compatibility window.
- For consumer-driven contracts, the consumer captures expectations and the provider verifies the same contract; a consumer-only test does not prove provider compatibility. Contract verification is **selected by risk and consumer/provider arrangement**, not universally mandated for every boundary. Consumer-driven contract testing is suitable for independently changing API providers and consumers; published libraries may be better served by public API tests, compatibility checks, and downstream build/tests.

## Decision and Exception Review

A preliminary dependency sketch should state **the graph being constrained**, the intended directions, and any important consumer-facing edge removals. Before adopting a new or tightened rule, inspect existing imports/build references to distinguish a _permitted_ edge from an _observed_ edge. If the rule would invalidate current consumers, classify it as potentially breaking and obtain approval for the exact scope or a staged migration; approval of an abstract principle alone does not authorize deleting an import or contract.

For a proposed exception, present the forbidden edge, reason, affected paths/consumers, owner, and concrete revisit/removal trigger. An exception is not implicit just because an architectural pattern looks inconvenient. A cross-unit integration may be runtime-only; do not require a shared source package solely to represent its protocol.

## Enforcement and Exceptions

- Prefer build/visibility enforcement; then architecture/import graph checks; use documented review policy where automation is infeasible.
- Each rule identifies node mapping and edge kind; enforcement must actually inspect its scope.
- Temporary exceptions specify affected paths, rationale, reviewer/owner, and retirement condition. A grandfathered violation baseline should block new violations while existing ones are removed.
- Avoid exemptions that mask new violations globally; track each exception individually.
