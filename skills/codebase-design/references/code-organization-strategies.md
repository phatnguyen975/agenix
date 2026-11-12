# Code Organization Strategies and Structure Patterns

## Purpose and Scope

Choose **how code is grouped within each affected release unit** and **how each architectural module is structured internally**. A multi-unit repository may use different languages, frameworks, and patterns in different units. These are separate, composable decisions. Repository layout, build targets, release units, modules, and runtime deployment boundaries are not interchangeable; use `repository-layout.md` and `module-design.md` for their definitions and ownership.

- **Primary organization:** the dominant way developers locate code — by capability/feature, component, technical layer, or use case/operation.
- **Module-internal pattern:** an optional way to separate responsibilities within a module — simple, layered, ports and adapters, vertical slices, pipes and filters, or presentation-state separation.
- **Boundary:** the intended public surface and permitted static dependencies, not merely a directory name. Implement visibility using the project's language, package/build system, and feasible checks.

These options **overlap** — a capability may be packaged as a component, contain operation slices, and use ports for external integrations. Respect framework-required paths and existing successful conventions; do not impose one universal directory tree.

## Selection Procedure

1. **Identify constraints and change drivers.** Inspect framework/build requirements, current paths and imports, consumers, ownership, changes that usually occur together, external dependency volatility, and testing needs. Clarify material gaps or conflicts with the human before choosing a target organization; do not substitute guesses for design inputs.
2. **Choose the simplest viable primary grouping.** Compare an existing or minimal structure against alternatives using change locality, cohesion, public-consumer needs, navigation cost, and coordination cost — not folder counts or arbitrary complexity scores.
3. **Add internal separation only where it protects a decision.** Select a pattern for an identifiable use case, invariant, I/O boundary, transformation sequence, or UI-state concern. Different modules and operations may use different patterns.
4. **Specify the real boundary.** Identify owned paths, authorized consumers, intended public surface (or `Internal only`), allowed **static** imports, and the compiler/build/visibility or review mechanism that can maintain those rules. If a rule cannot be enforced, state the gap; a diagram is not enforcement.
5. **Present consequential trade-offs.** Show a representative proposed tree, important dependency edges, the strongest practical alternative, and costs introduced by abstraction. Submit material, previously unapproved choices to the `SKILL.md` **Decision Checkpoint** before treating them as adopted.

| Observed Driver                                           | Consider                                   | Countercheck                                              |
| --------------------------------------------------------- | ------------------------------------------ | --------------------------------------------------------- |
| Capabilities evolve or are owned independently            | Feature/capability grouping                | Are shared invariants and consumers owned?                |
| Consumers need a small protected entry point              | Component-oriented boundary                | Can visibility be enforced without excess wrappers?       |
| Technical roles/framework roots dominate a small codebase | Layer-first or simple grouping             | Does one feature change scatter across global layers?     |
| Operations change independently with different complexity | Use-case-first grouping or internal slices | Will shared rules be duplicated?                          |
| Core behavior must be isolated from external I/O          | Core separation or ports and adapters      | Is the additional interface useful?                       |
| Processing has distinct input/output stages               | Pipes and filters                          | Are order and state dependencies explicit?                |
| UI has nontrivial presentation state                      | Presentation-state separation              | Does the framework already provide a sufficient boundary? |

## Primary Organization Strategies

### Package by Feature or Capability

Group implementation by a coherent product responsibility (for example, `orders/` or `notifications/`) so related changes stay local. A feature folder **does not automatically enforce** a public interface; define the module boundary and cross-feature imports separately.

- **Prefer when:** business capabilities have recognizable owners/consumers or technical-layer-first navigation scatters a change.
- **Reconsider when:** features cannot own shared invariants, require pervasive cross-feature internals, or are artificially split by endpoint.
- **Combine with:** a simple module, internal technical layers, operation slices, or a component-style public surface.

### Package by Component

Encapsulate a cohesive capability — including its application logic and private persistence details — **behind a deliberately limited consumer-facing interface**. Compared with mere feature grouping, the defining decision is which internals consumers cannot access; this is **not** a claim that component and feature organization are mutually exclusive.

- **Prefer when:** several consumers must depend on a stable responsibility rather than its controller, repository, or implementation classes.
- **Reconsider when:** the component is a pass-through facade, its public interface is sprawling, or its boundary is only a folder convention with no feasible check.
- **Enforce when possible:** language visibility/package exports or build boundaries first; otherwise architecture/import checks or explicit review with a documented limitation.

```text
shop/
├── orders/
│   ├── public/           # intended Orders consumer surface
│   └── internal/         # order rules and persistence implementation
└── checkout/             # imports Orders public surface, not internal/
```

`public/` and `internal/` are illustrative roles, **not required directory names**. They alone do not restrict imports.

### Package by Layer

Group by technical role, such as `presentation/`, `application/`, and `persistence/`. Layer-first placement and **layered dependency policy** are different decisions: the first describes locations; the second defines which edges are permitted.

- **Prefer when:** code is small and cohesive, technical workflows dominate, or the framework mandates layer-shaped roots.
- **Reconsider when:** routine capability changes touch many unrelated global directories or ownership and public boundaries become implicit.
- **Alternative:** preserve framework roots but establish capability modules and imports across them; do not infer a single architectural module from a top-level folder.

### Package by Use Case or Operation

Group entry points and operation-specific code around requests or workflows (`place-order/`, `cancel-order/`) when **the operation is the main axis of change**. This is vertical-slice organization used as the primary grouping, rather than only inside a capability directory.

- **Prefer when:** operations evolve independently and benefit from different implementation approaches.
- **Reconsider when:** operations repeatedly modify shared invariants or need tightly coordinated changes; group them under a capability and give shared rules one owner.
- **Boundary:** an operation folder is not automatically an independent module, public contract, or release unit. State ownership and allowed cross-operation imports explicitly.

```text
operations/
├── place-order/          # handler, validation, operation-specific coordination
└── cancel-order/         # distinct operation; may use a simpler implementation
orders-core/              # shared invariants, only if independently justified
```

A feature/capability boundary and use-case-first organization can coexist — an `orders/` capability may own both operation folders and the shared order invariants.

## Module-Internal Structure Patterns

### Simple Module

Keep a cohesive responsibility in a few files or one directory; expose only what real consumers need. **Use when** there is no independently changing concern worth isolating. **Reconsider** if implementation details leak to consumers, testing repeatedly requires external systems, or distinct changes repeatedly collide.

**Example:** `date-formatting/` may expose one formatter and keep parsing helpers private; it needs no mandatory `domain/application/infrastructure` trio.

### Layered

Separate technical roles and specify allowed **static import edges**. In conventional layered access, a **closed** layer must be traversed rather than bypassed; an **open** layer permits defined bypasses. Neither term alone establishes the actual source-import graph or guarantees that domain logic is independent of storage.

- **Use when:** technical roles are meaningful, help navigation, and separate concerns without excessive forwarding.
- **Reconsider when:** layers are mostly pass-through, or core behavior depends on concrete infrastructure that ought to be replaceable.
- **Define separately:** allowed access between layers, static import direction, and runtime call flow. Dependency inversion may deliberately make concrete adapters import an abstraction owned by the core.

```text
# Static imports in an application that combines layers with inversion:
delivery     ---->  application       # calls application entry points
application  ---->  domain            # uses domain behavior
storage      ---->  application/port  # implements core-owned persistence port
composition  ---->  delivery, application, storage
application  --X->  storage           # prohibited concrete-adapter import
```

These are illustrative **source dependencies**, not the sequence of runtime calls. A conventional downward three-layer design without inversion is another valid choice if its trade-offs are accepted.

### Ports and Adapters (Hexagonal)

Define core interactions as **purposeful ports** and translate technologies at adapters. Driving/inbound adapters invoke core entry points; driven/outbound adapters satisfy capabilities required by the core. The core does not statically import concrete adapters; composition connects implementations at the application boundary.

- **Use when:** independent core testing, varied entry mechanisms, or volatile external integrations justify the extra seams.
- **Reconsider when:** wrappers merely rename SDK operations and create no useful isolation.
- **Avoid mandated shapes:** an inbound port may be the application's existing public API/use-case entry, not a separately declared interface. Outbound ports should describe meaningful core needs, not every external call. Framework-native wiring is acceptable.

```text
orders/
├── core/                 # use cases; owns payment port when needed
├── inbound/              # translates request to a core operation
└── outbound/             # payment adapter imports core port
# application composition connects inbound, core, and outbound
```

Clean Architecture and Onion Architecture share the principle of protecting application policies from external implementation details. Clean Architecture additionally distinguishes domain-level and use-case-level policies. Apply these distinctions when useful; do not impose fixed layers or directory structures.

### Vertical Slice

Keep **each use case's** entry, validation, and operation-specific coordination together. Use slices inside a capability or as primary use-case grouping as above. Each slice may choose a simple transaction script or richer design; **do not mandate a service/repository abstraction for every request**.

- **Use when:** individual operations evolve mostly independently and implementation complexity differs across them.
- **Reconsider when:** slices duplicate substantive invariants, access each other's internals, or must change together constantly.
- **Share deliberately:** move stable common rules to an explicitly owned capability/core; minimize shared infrastructure abstractions whose only purpose is uniformity.

```text
orders/
├── place-order/          # may coordinate payment through a core-owned port
├── cancel-order/         # may be a small direct operation
└── core/                 # order invariants shared by both, if needed
```

A slice is not automatically a DDD bounded context, build module, or deployable unit.

### Pipes and Filters

Organize a transformation as **stages with explicit input/output contracts**, plus a composition point that defines their order. A stage need not be a separate process or service; this skill concerns **source-code boundaries**, not distributed execution design.

- **Use when:** independently understandable transforms form a useful pipeline and can be tested or reused in isolation.
- **Reconsider when:** stages share mutable state, rely heavily on one another's internals, or only disguise a sequential service method.
- **Define:** stage ownership, required input/preconditions, output/errors, state handling, and ordering constraints. Compatible data types alone do **not** make reordering semantically safe.

```text
importer/
├── stages/               # parse, normalize, validate
└── pipeline/             # parse → normalize → validate, by this policy
```

For example, `validate` might require normalized values; changing the order requires validating semantics, not only matching types.

### Presentation-State Separation

Keep rendering controls separate from presentation state and behavior **when** UI complexity warrants it. Select the variant already supported by the framework instead of treating the following names as equivalent:

- **MVC:** separates model, view, and input/controller responsibilities; exact interaction and dependencies vary by framework.
- **MVP:** a presenter handles input/presentation coordination; **Passive View** delegates nearly all view behavior to the presenter, while **Supervising Controller/Presenter** leaves simple binding in the view.
- **MVVM / Presentation Model:** view binds or synchronizes with view-independent presentation state and operations; clarify who owns state and synchronization.
- **Unidirectional Data Flow:** actions/events trigger controlled state transitions, then updated state drives rendering; a single global store is **not** universally required.

**Use when:** complex UI state, transformations, and interactions are difficult to reason about inside rendering code. **Reconsider when:** a straightforward view or built-in framework idiom is sufficient. Specify state ownership, permitted updates, lifecycle, and boundary to domain/application behavior; adapt folders to the actual framework.

```text
profile/
├── presentation/         # view and interaction adapters
└── state/                # view-independent state transitions, if needed
# events → state update → render (unidirectional example)
```

## Composition and Review Rules

- **Do not pick patterns by labels.** A feature folder can be a component only when its public/private contract is meaningful; a ports folder does not create dependency inversion on its own.
- **Mix patterns by boundary, not by mandate.** A capability may contain vertical slices and one outbound port; it does not need hexagonal folders for every slice.
- **Keep one owner for invariants.** A shared rule must not silently diverge across operations or components. Cross-module collaboration uses intentional public surfaces.
- **Make static dependencies unambiguous.** Identify the source/build graph, public imports, adapter-to-port direction, and actual check. Runtime calls, events, and data flow are different graphs; avoid conflicting policies.
- **Expose the cost of structure.** Include new interfaces, indirection, build complexity, coupling, and consumer migration where relevant. Record an alternative for material decisions; retain an existing working layout absent a demonstrable reason to change it.

**Worked decision:** `Orders` has independently evolving `place-order` and `cancel-order` operations, one owner of order invariants, and a payment provider likely to change. A capability module containing two slices, shared core rules, and **one payment port where isolation is useful** is a reasonable candidate. A global `controllers/services/repositories` split scatters changes; a port per helper over-engineers the boundary. Show `place-order → orders/core`, `payment-adapter → orders/core/payment-port`, and **no** `orders/core → payment-adapter` static import. Treat this as a **proposal**, not an approved or observed tree; apply the Human Gate when required by `SKILL.md`.
