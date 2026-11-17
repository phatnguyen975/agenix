# Test Levels

Use this guide to select the scope needed to establish a behavior and distinguish it from where a check executes. Follow the caller's selected strategy and project vocabulary; test categories are not universally standardized.

## Applicable Checks

Include checks required by the behavior, selected strategy and affected boundaries. Record fast local cycle commands separately from broader final/CI checks. A check executed only in CI remains relevant; unavailable service/environment access is a verification gap, not permission to claim a unit double proves the real integration.

- Choose the smallest scope that exposes the behavior without replacing the collaborator responsible for it.
- Use a permitted dedicated environment for real boundaries; do not access shared/production data or credentials implicitly.
- If the required seam, tool or environment is unavailable, record the blocked check and resolve the prerequisite before dependent completion. Do not silently change the strategy.
- Outside the authorized edit scope, identify relevant regression needs and preserve existing tests. Do not widen writes just because another level is relevant.

## Level Definitions

These working categories distinguish scope and dependencies; adapt labels to the project.

| Level       | Scope                                                                                                                  | Dependencies                                                                                                                                                       |
| ----------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Unit        | One unit of behavior through its public interface, real in-process collaborators are allowed                           | No I/O, network, or external process                                                                                                                               |
| Integration | The code plus a real adapter of one boundary (database, file system, queue, in-process HTTP)                           | Real components/adapters in controlled environments; isolate data and cleanup                                                                                      |
| Contract    | The project's assumptions about an external provider or consumer (request and response shapes, status and error codes) | Consumer/provider verification against an explicit shared contract, including the real provider when needed; schemas/samples alone prove only their checked subset |
| End-to-end  | The whole system through its outermost interface                                                                       | Real wiring                                                                                                                                                        |

**Notes:**

- A unit may use real in-process collaborators. Choose isolation/doubles for the test purpose and project style; see [Writing Good Tests](writing-good-tests.md#test-doubles).
- A fake provides evidence only for modeled behavior. Shared conformance checks with the real implementation strengthen confidence; a canned response matching a schema does not establish provider behavior.
- Contract verification is also a purpose that can overlap integration scope; it is not defined by the use of doubles.
- Acceptance testing is defined by purpose (stakeholder acceptance), not by scope. Classify an automated acceptance test by its scope and dependencies.

## Mapping Project Vocabulary to Levels

Map by scope and dependencies, never by name alone.

| Term a Project May Use                                                                                      | Level                                                                                                                                                   |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Component test, module test, unit test                                                                      | Often unit; verify actual scope/dependencies                                                                                                            |
| Component integration test, repository test, adapter test, service test with a real database                | Integration                                                                                                                                             |
| Consumer/provider contract verification; schema or documented-shape checks                                  | Contract verification for the checked interaction; schema/document checks cover only their declared subset                                              |
| System test, UI test, browser test, journey test, automated acceptance test through the outermost interface | End-to-end only for whole-system wiring; isolated browser/component tests may have smaller scope                                                        |
| An "API test" or "service test"                                                                             | Decide by dependencies: real boundary adapter → integration; whole system → end-to-end; doubled provider alone does not establish contract verification |

## Assigning a Level to an Item

- Choose the lowest applicable level at which the behavior is observable through a stable seam and dependencies can be real or hermetic.
- Move up only when the behavior emerges from connecting components across a boundary.
- Record a primary scope/category per item; the same acceptance criterion can require complementary tests at several scopes for different risks.

| Signal                                                                                                                        | Level       |
| ----------------------------------------------------------------------------------------------------------------------------- | ----------- |
| Business rule, calculation, validation, branching, state change                                                               | Unit        |
| Query semantics, persistence round trip, serialization format, transaction or constraint behavior, mapping of boundary errors | Integration |
| Shape of a request or response exchanged with another system, status or error codes                                           | Contract    |
| A critical journey that only works when every component is connected                                                          | End-to-end  |

Example (feature "save an order"):

| Behavior                                                                 | Level                                                                                                          |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| An order with no items is rejected                                       | Unit                                                                                                           |
| The saved order can be read back with the same items                     | Integration                                                                                                    |
| The payment provider's decline response is mapped to a "declined" result | Unit/adapter behavior for mapping; separate contract verification establishes the provider response assumption |
| A customer completes checkout through the interface                      | End-to-end                                                                                                     |

Record unavailable relevant checks under "Not Tested" with reason and required disposition; do not erase them from coverage because execution is deferred to CI.

## What to Test and What Not to Test

| Level       | Test                                                                                                                                                                   | Do Not Test                                                                                                                                                              |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Unit        | Business rules, branching, validation, calculations, state transitions, error paths, boundary values                                                                   | Framework or library internals; getters, constructors, or forwarding without logic; incidental private structure or interaction order unrelated to a behavioral contract |
| Integration | Round trips across the boundary (persistence and queries, serialization, payload shape); constraints and transactions; mapping of boundary errors (timeout, rejection) | Business-rule permutations already covered at unit level; third-party service behavior                                                                                   |
| Contract    | Request and response schema; status and error codes; required fields; that doubles behave like the real provider                                                       | The provider's business logic; data permutations                                                                                                                         |
| End-to-end  | Critical business journeys; acceptance criteria observable only with the whole system connected                                                                        | Avoid duplicating lower-level matrices; retain edge/failure cases that emerge only from real wiring                                                                      |
