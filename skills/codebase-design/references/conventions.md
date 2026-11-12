# Structural Conventions

## Purpose and Selection

Specify conventions that maintain module boundaries, code discoverability, and safe integration. **Do not duplicate** formatter rules, feature-level business logic, complete security policies, or tutorials on framework APIs. Select each area **only** if it changes a structural decision; naming and public-surface guidance are relevant whenever modules exist, and some topics below are conditional.

For every selected convention, state **scope, required behavior, exceptions, owner, and check**. A Review distinguishes existing adopted conventions from recommended new ones; a proposed `CV-xx` rule is not evidence of a violation until adopted. Use stable `CV-xx` rule IDs in a design document. Prefer established language/framework conventions over arbitrary universal naming styles.

| Area                      | Include When                                                          |
| ------------------------- | --------------------------------------------------------------------- |
| Naming and placement      | Always, but only for structural units and boundary files              |
| Public interfaces         | Other modules or external consumers require access                    |
| Errors across boundaries  | A module exposes failure behavior to consumers                        |
| Dependency composition    | Implementations are selected or injected at a boundary                |
| Configuration             | Modules receive environment-dependent or externally supplied settings |
| Logging and observability | Boundary logging/correlation affects multiple modules                 |
| State ownership           | Mutable state is shared beyond a single local scope                   |
| Assets and generated code | Such resources are part of the codebase and ownership is ambiguous    |

## Naming and Placement

- Use established product/domain vocabulary for capabilities; use technical names (`adapters`, `tests`, `src`) for genuine technical roles, not as substitutes for capability ownership.
- State one convention for **module names**, paths, public exports, and test names, respecting case sensitivity and existing framework tooling. Do not prescribe a universal singular/plural or file-case style.
- Define the placement of entry points, composition roots, contract definitions, and generated output **only when they exist**. State where initialization and import-time side effects are allowed if they affect module consumers.
- Avoid catch-all names (`misc`, `helpers`, `common`) _when_ they conceal unrelated responsibilities; a framework-standard `common` directory can be acceptable with a bounded, named purpose.
- Keep public paths stable where consumers depend on them; file renames can be breaking even when exported types stay equivalent.

**Example:** `orders/api` exposes `placeOrder`; `orders/internal/storage` is not an import target for `checkout`. The exact path form follows project idioms.

## Public Interface Surface

- Record the public-entry mechanism: language visibility modifiers, package exports, manifest entrypoints, declared APIs, or boundary checks.
- Default to the smallest useful surface. Internal support code stays private; third-party SDK types should not become contract types accidentally.
- Consider compatibility of **symbols, paths, errors, behavior, and types**. An additive export is not necessarily behaviorally backward-compatible.
- Mark external/public, intra-repository/public, and internal-only surfaces distinctly if the project has all three.
- Use `DR-xx` for forbidden imports and `CV-xx` for naming/maintenance practices; do not duplicate constraints in both locations.

## Error Boundaries

- Define error _categories_ that consumers can react to, not the complete exception hierarchy. Typical distinction: invalid input, rejected business operation, unavailable dependency, unexpected defect.
- Choose the project's language-idiomatic representation (exceptions, errors, result values). Translate technology-specific failures into a stable module-facing vocabulary when they cross boundaries.
- Handle failure at the layer that can decide on recovery; do not swallow exceptions. Avoid unconditional "log exactly once": logging ownership depends on whether a failure is recovered, returned, or observed at an outer boundary.
- Boundary adapters map internal failures to the contract's response semantics; the core need not depend on transport-specific error classes.

**Example:** an adapter catches `ProviderTimeout` and exposes `PaymentUnavailable` to its owning module; only the caller with a retry/fallback decision acts on it. Detailed retry policy is outside this skill.

## Dependency Composition

- When dependency injection is useful, identify a composition location that knows concrete implementations (usually application startup or a framework composition mechanism).
- An independently published library generally exposes a construction/configuration API rather than requiring a global application composition root of its own.
- Distinguish **compile-time ownership** of a port from **runtime control flow** through it. Core code may call a port without importing its concrete adapter.
- Prefer explicit, testable initialization and avoid import-time I/O or global state mutations across module boundaries unless the framework requires them. Prevent uncontrolled service locators and hidden global construction when they obscure dependencies; do not outlaw framework-provided dependency injection solely because it lacks an explicit handwritten `main` function.
- Test-only assembly may instantiate adapters independently for tests.

```text
Application composition → concrete email adapter → notification-owned port
Notifications core → notification-owned port
```

## Configuration Ownership

- Separate deployment-variable configuration and secrets from code; do not commit secrets.
- Give each configuration key/section a responsible module; define how validated settings reach that module through constructors, configuration providers, or framework-approved mechanisms.
- Prefer one coherent validation boundary; do not require every library to read environment variables or require all settings to be immutable if the runtime legitimately supports dynamic configuration.
- Identify generated/default config locations only when needed for navigation; keep environment-specific values outside the module's public API unless consumers truly need them.

## Logging and Observability Boundaries

- Decide ownership of log emission at module and application boundaries; prefer structured context if the project's observability system supports it.
- Pass correlation context across relevant entry/adaptor boundaries, without coupling core rules to one vendor SDK.
- Keep secrets, tokens, and sensitive personal data out of emitted logs; use approved redaction/masking policy.
- Do not mandate one universal level taxonomy or exact logging library without project constraints. Avoid duplicate noisy logs of the same propagated failure; legitimate multi-layer observability can exist.

## State Ownership

- For shared mutable state, name the owning module and the public operations allowed to update it; avoid write access from unrelated modules.
- Specify local versus module-scoped versus process-wide lifetime only where it changes dependency or ownership rules.
- Use state propagation mechanisms that fit the runtime/framework. Cross-unit state synchronization and data consistency policy belong to system/domain architecture, not this skill.
- For UI modules, separate rendering from state mutation when the complexity warrants it; avoid mandatory global state stores.

## Assets and Generated Sources

- Place assets with their owning module when feasible; a shared asset package needs an explicit consumer set and owner.
- Identify source-of-truth versus generated outputs, whether generated files are checked in, and which checks prevent stale generation; do not edit generated output as authoritative source.
- Give templates and localization resources an explicit owning capability where they affect that capability's behavior.
- Do not assume every image/font/resource must be accessed through a programmatic public API; static asset bundlers and frameworks have legitimate access mechanisms.

## Rule Examples

| ID    | Rule                                                                                                     | Verification                                            |
| ----- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| CV-03 | Module directories use the project's established capability vocabulary and casing.                       | New-module review and path naming checks when supported |
| CV-04 | Public module error surfaces expose documented module-facing error categories, not vendor error objects. | Public API inspection, compatibility tests, review      |
| CV-05 | Environment settings are validated before creation of modules that require them.                         | Startup test or integration test                        |
| CV-06 | Changes to shared generated contracts modify the source of truth and regenerate derived artifacts.       | Generated-file consistency check in CI                  |

These IDs are illustrative. In a real document allocate IDs once across all convention areas, including shared-code policy.
