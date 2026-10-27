# Test Failures

## First decision: is the test wrong or the code wrong?

1. Read the test name and assertion: what behavior does the test claim?
2. Compare that claim with the specification, the documentation, or the human. When they disagree, ask the human.
3. Check history: did the test or the code change recently (version-control log or blame)?
4. Run the test alone and inside the suite. Different results mean shared state or order dependence: `nondeterministic-failures.md`.
5. Inspect fixtures, mocks, and snapshots: stale test data, mocks that no longer match the real interface, snapshots recorded from buggy behavior.

## Common causes

- A real defect in the code under test.
- A test that encodes outdated behavior after an intended change.
- A stale or over-specified mock, fixture, or snapshot.
- Shared or leaked state; order dependence.
- Dependence on time, locale, timezone, randomness, filesystem, or network.
- Differences between the local and CI environments (`environment-failures.md`).

## Rules

- Read the first failure first; later failures can be consequences.
- Many tests failing at once: group them by error message or top stack frame. One cause often explains a group; each distinct cause is handled as a separate root cause.
- Test is wrong: follow the "Incorrect test or expectation" special case in `SKILL.md`.
- Update snapshots or golden files only after confirming the new output is the correct behavior.
- Never skip, delete, or loosen a test to make it pass.
