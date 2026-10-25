# Test Levels

How to treat levels in the TDD loop. How the applicable set is determined is in `SKILL.md`, Phase 0.

## Applicable levels

The applicable levels are the levels the project runs during implementation.

- **In the set:** normal flow (test list → RED → GREEN → REFACTOR) with the focused run.
- **Outside the set:** no tests, no items, not run in the loop. Leave existing tests at these levels unchanged; if the change may alter behavior they verify, report it in the exit summary.
- For behavior observable only at an outside level, record it under "Not Tested" with the reason, for the user to decide.
- Show the applicable levels and their source in the review view.

| Situation found                                                                                              | Applicable levels                                       |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| Project documents say only unit tests run during implementation                                              | unit                                                    |
| Project documents say integration tests also run locally before a change is finished                         | unit, integration                                       |
| Integration or end-to-end tests run only in CI, and the user gave no instruction                             | unit                                                    |
| The user asks for an additional level for part of the work (e.g. one end-to-end test for a critical journey) | the documented set, plus that level for the named items |
| No rule found and no instruction                                                                             | ask the user; propose unit as the minimum               |

## Level definitions

**Levels are defined by scope and dependencies:**

| Level       | Scope                                                                                                                  | Dependencies                                                                                   |
| ----------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Unit        | One unit of behavior through its public interface, real in-process collaborators are allowed                           | No I/O, network, or external process                                                           |
| Integration | The code plus a real adapter of one boundary (database, file system, queue, in-process HTTP)                           | Local and hermetic                                                                             |
| Contract    | The project's assumptions about an external provider or consumer (request and response shapes, status and error codes) | Doubles of the provider, checked against the provider's schema, documentation, or real samples |
| End-to-end  | The whole system through its outermost interface                                                                       | Real wiring                                                                                    |

**Notes:**

- A unit may use real collaborators in the same process. Double only what crosses a system boundary (see `writing-good-tests.md`).
- A fake used at unit level is trustworthy when contract tests confirm it behaves like the real provider.
- Acceptance testing is defined by purpose (stakeholder acceptance), not by scope. Classify an automated acceptance test by its scope and dependencies.

## Mapping project vocabulary to levels

Map by scope and dependencies, never by name alone.

| Term a project may use                                                                                      | Level                                                                                                               |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Component test, module test, unit test                                                                      | Unit                                                                                                                |
| Component integration test, repository test, adapter test, service test with a real database                | Integration                                                                                                         |
| Consumer-driven contract test, schema test, API conformance test against provider documentation             | Contract                                                                                                            |
| System test, UI test, browser test, journey test, automated acceptance test through the outermost interface | End-to-end                                                                                                          |
| An "API test" or "service test"                                                                             | Decide by dependencies: real boundary adapter → integration; whole system → end-to-end; doubled provider → contract |

## Assigning a level to an item

- Choose the lowest applicable level at which the behavior is observable through a stable seam and dependencies can be real or hermetic.
- Move up only when the behavior emerges from connecting components across a boundary.
- Assign exactly one level per item.

| Signal                                                                                                                        | Level       |
| ----------------------------------------------------------------------------------------------------------------------------- | ----------- |
| Business rule, calculation, validation, branching, state change                                                               | Unit        |
| Query semantics, persistence round trip, serialization format, transaction or constraint behavior, mapping of boundary errors | Integration |
| Shape of a request or response exchanged with another system, status or error codes                                           | Contract    |
| A critical journey that only works when every component is connected                                                          | End-to-end  |

Example (feature "save an order"):

| Behavior                                                                 | Level                                                                      |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| An order with no items is rejected                                       | Unit                                                                       |
| The saved order can be read back with the same items                     | Integration                                                                |
| The payment provider's decline response is mapped to a "declined" result | Contract (or unit with a double, once a contract test confirms the double) |
| A customer completes checkout through the interface                      | End-to-end                                                                 |

Only levels in the applicable set are used. A behavior whose natural level is outside the set goes to "Not Tested".

## What to test and what not to test

| Level       | Test                                                                                                                                                                   | Do not test                                                                                                                               |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Unit        | Business rules, branching, validation, calculations, state transitions, error paths, boundary values                                                                   | Framework or library internals; getters, constructors, or forwarding without logic; private methods; call order or internal collaborators |
| Integration | Round trips across the boundary (persistence and queries, serialization, payload shape); constraints and transactions; mapping of boundary errors (timeout, rejection) | Business-rule permutations already covered at unit level; third-party service behavior                                                    |
| Contract    | Request and response schema; status and error codes; required fields; that doubles behave like the real provider                                                       | The provider's business logic; data permutations                                                                                          |
| End-to-end  | Critical business journeys; acceptance criteria observable only with the whole system connected                                                                        | Edge cases; validation matrices; anything verifiable at a lower level                                                                     |
