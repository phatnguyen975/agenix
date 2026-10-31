# Axis: testing

## Purpose

Verify that tests exercise the changed behavior and would detect meaningful regressions, including boundary and failure cases.

## Method

1. Read relevant tests first to understand intended behavior and existing coverage.
2. Inventory production behaviors, branches, state transitions, and failure paths added or changed. Map each material behavior to at least one suitable test or explicit verification method.
3. Assess whether the tests prove behavior at the correct level: unit, integration, contract, end-to-end, property-based, or other project-appropriate level.
4. Perform a **reasoning-only sensitivity check**: mentally invert/remove important conditions, operations, or boundary handling and ask whether a test would fail. Do not mutate source or tests to run mutation experiments.
5. For a bug fix, verify that a regression test would fail against the pre-fix behavior and pass with the fix.
6. Use actual verification outputs and available coverage reports. Coverage percentage is a signal, not proof of test quality.

## Checklist

### Presence and Level

- Are tests present for new or changed behavior, added in the same change where practical?
- Is each behavior tested at the level that proves it? Are contracts between components/services verified where unit tests cannot prove them?
- Are boundaries, invalid inputs, permission cases, concurrency, retries, partial failure, and cancellation covered when relevant?
- Does a bug fix include a regression test for the root cause?

### Validity and Sensitivity

- Do tests assert externally meaningful behavior rather than implementation details?
- Would a realistic defect in the code cause the test to fail?
- Would a harmless internal refactor leave the test passing?
- Are assertions specific and informative, with names describing scenario and expected outcome?
- Are important branches, conditions, and error paths sensitive to incorrect behavior?

### Reliability and Maintainability

- Are tests deterministic and independent of uncontrolled time, randomness, network, execution order, or leftover state?
- Are fixtures isolated and free of shared mutable state that leaks between tests?
- Is setup proportionate, with no excessive mocking that bypasses the behavior being tested?
- Are tests focused, comprehensible, and maintainable like production code?
- Were tests deleted, skipped, weakened, or made conditional in a way that hides a regression?

### Verification Evidence

- Do recorded test/build/lint/manual verification results correspond to the actual changed files and commands run?
- For user-visible behavior, is an appropriate visual/interaction check documented when static tests cannot establish it?
- For performance claims, is there comparable before/after measurement under a stated workload?

## Severity Guidance

- No effective tests for new core, security-sensitive, or data-affecting behavior — High; Critical only when a proven severe failure is otherwise unmitigated.
- Missing regression test for a confirmed bug fix — High.
- Tests that cannot detect the asserted defect, or tests removed/weakened to hide a failure — High.
- Material edge/error/concurrency coverage gap — Medium.
- Flaky, order-dependent, or brittle test with realistic maintenance cost — Medium.
- Minor naming/duplication in tests — Low.

## Boundaries

- Production-code defects belong to their owning axis; here, report only that tests would not catch them.
- Documented test-file rules belong to standards-compliance.
- Do not infer test success when commands were not run.
