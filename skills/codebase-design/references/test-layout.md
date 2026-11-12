# Test Layout

## Purpose

Decide **where tests and test support belong** so production module boundaries remain understandable and test code can be located, built, and changed with its owner. Choosing exact coverage percentages, test tools, or the project's entire quality strategy is out of scope.

## Start from the Boundary

For each release unit or module, determine its real public consumers, external integrations, and framework packaging constraints. Record tests at the **lowest owning scope** that exercises the behavior without leaking unrelated module internals. Tests can be colocated with source or in a mirrored tree; a project may use both when the scopes differ.

## Test Types and Scope

| Type             | What It Exercises                                                                                      | Typical Ownership                           |
| ---------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------- |
| Unit             | Small behavior unit with controlled collaborators; may be a function, class, or cohesive module        | Owning module                               |
| Component/Module | A complete module through its public surface, including its internal collaborators                     | Owning module                               |
| Integration      | Real interaction across an adapter, datastore, framework boundary, or several modules                  | Boundary owner or release unit              |
| Contract         | Compatibility assertions at independently evolving consumer/provider or published interface boundaries | Contract owner and affected parties         |
| End-to-End       | User-visible or system flow through real public entry points                                           | Whole release unit or cross-unit test owner |

Names vary across ecosystems. Define the intended scope in the design rather than assuming `unit`, `integration`, or `e2e` means exactly the same setup everywhere. Component/module tests are useful where unit tests would otherwise depend on private implementation details.

## Placement Strategies

### Colocated Tests

```text
orders/
├── api/                    # module's production public surface
├── internal/               # implementation
└── tests/                  # tests owned by orders, if allowed by tooling
```

- Prefer when tests should move with the module and the test tooling/build can exclude test artifacts from production.
- A language may instead favor `foo.test`, `foo_spec`, or `__tests__` in the source tree; follow existing idiom.
- Do not let a sibling module import another module's private test helpers.

### Separate Test Trees

```text
src/orders/                 # production module

tests/orders/               # mirrors owning module

tests/integration/          # tests spanning declared modules

tests/e2e/                  # application-level scenarios
```

- Prefer when build/package boundaries or language tooling require production/test separation.
- Keep a deterministic module-to-test mapping; use the actual paths, not these placeholders.
- Group cross-unit tests at the scope of the scenario rather than forcing them into one participant's internal test folder.

**Hybrid example:** colocated module tests, application-level `tests/integration/`, and a repository-owned cross-service verification suite. Such a hybrid is valid if ownership and run stages are explicit.

## Mapping Rules

In the design document:

1. Map every **substantive** module or reusable package to its primary test location, or state why its behavior is tested through a larger boundary. Avoid manufacturing an empty test directory for a purely declarative module.
2. Record integration tests at the point that owns each meaningful external adapter.
3. State where application/end-to-end tests live **when applicable**; a library with no executable user flow need not have end-to-end tests.
4. For independently evolving contracts, identify the verification approach and which participants are responsible. In consumer-driven contract testing, consumer expectations and provider verification form one workflow; a generated contract file alone is insufficient. Not every internal function or package needs consumer-driven contract files.
5. Record packaging and execution constraints: tests must not leak into shipping artifacts unintentionally, and slow/external tests should have an intentional CI stage.

## Test Boundaries by Organization

| Design                  | Primary Test Seam                                            | Complementary Tests                                             |
| ----------------------- | ------------------------------------------------------------ | --------------------------------------------------------------- |
| Simple module           | Public function/module entry when present                    | Unit tests for nontrivial internals when useful                 |
| Layered                 | Stable application/domain behavior, isolated when meaningful | Adapter and framework integration tests                         |
| Ports and adapters      | Core behavior through ports                                  | Real adapter integration tests; inbound-adapter interface tests |
| Vertical slices         | Slice's own request/use-case entry                           | Tests of shared invariants without duplicated setup             |
| Pipes and filters       | Independent transformation stages                            | Pipeline composition and error-flow integration tests           |
| Presentation separation | State transitions/presentation logic                         | Rendering, input, and accessibility integration tests           |
| Published library       | Public package API                                           | Consumer compatibility tests and downstream builds as needed    |

This table helps choose test **locations and seams**, not a universally required suite for each pattern.

## Fixtures and Test Doubles

Use a test double only where it improves test isolation or determinism. The Meszaros vocabulary is:

- **Dummy:** required value never used.
- **Stub:** supplies predetermined responses.
- **Spy:** records interactions for later assertion.
- **Mock:** verifies specified interaction expectations.
- **Fake:** functional simplification such as an in-memory repository.

**Example:** a module with an outbound `Payments` port may use an in-memory fake for module tests, while its real payment adapter has integration tests. Test the real integration independently; a fake does not prove protocol compatibility.

Placement and ownership:

- Keep local fixtures and builders beside the tests using them; extract shared test support only for repeated, stable needs. Where test frameworks cannot access private code without violating module visibility, prefer public-boundary tests or narrowly scoped same-module test access.
- Scope reusable fakes to the **owner of the interface** or an explicit test-support package; avoid a sprawling global testing utilities module.
- A consumer test may implement its own double against a published interface. Do not require all doubles to be distributed by the provider.
- Test-support imports must never flow into production code. Where tests need private internals, allow them only within their owning module and actual test tooling's visibility mechanism.
- Make shared fixtures deterministic; isolate mutable state, time, environment, external endpoints, and file system paths so tests can run in parallel where supported.

## Execution and Feedback

Record which test groups run locally, pre-submit/PR CI, merge/mainline, or on demand. Place cheap deterministic tests early and expensive environment-dependent tests later. For migration, run relevant characterization/regression tests before and after each boundary move.

In Design, specify intended test locations and run stages. In Review, distinguish observed test locations and executed results from proposed improvements; absent or unrun suites are not passing evidence. A test layout document must **not** claim coverage or passing status without execution evidence.
