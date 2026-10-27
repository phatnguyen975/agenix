# Regression Guards (Phase 4)

The regression guard hierarchy is in `SKILL.md`. This file covers how to build a guard and confirm it fails for the right reason.

## Choosing the test seam

- Too low (mocks that remove the faulty collaborator): the guard passes while the bug exists.
- Too high (full end-to-end for a unit-level defect): the guard is slow and flaky.
- Start from the root cause: choose the lowest level that still exercises the defective code with the real inputs and state of the failure.
- Reuse the project's test framework, location, naming, fixtures, and conventions found in Phase 0.
- When Level 1 has no feasible test seam (for example, the behavior cannot be isolated without removing the faulty collaborator), record why and consider the next feasible level in the hierarchy. Prefer the strongest available option; use Level 5 only when stronger levels are not feasible.

## Writing the guard

- Name it after the behavior ("rejects an empty cart"), not the ticket.
- Keep it minimal: the minimal reproduction and nothing else.
- Assert the correct behavior for the symptom (expected value or message), not merely "no error".
- Make it deterministic: pin time, randomness, ordering, and network.
- Test public behavior, not implementation details.
- Make it independent: it creates its own state and cleans up after itself.

## Confirming red for the right reason

1. Run the guard on the current, unfixed code.
2. The failure text or behavior must match the symptom.
3. Setup errors, import or compile errors, and missing fixtures are wrong reds: repair the guard and rerun.
4. When the guard passes instead, it does not exercise the defect (often a mock replaced the faulty code): rebuild it one level up, with the real collaborators.
5. Keep the failing output for the evidence table and the report.

## Other levels

| Level                 | Build notes                                                                                                                                                       |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2 Reproduction script | Commit it where the project keeps scripts or checks; non-zero exit on failure; usage in a header comment                                                          |
| 3 Benchmark           | Threshold from the measured baseline with a margin above measurement noise (several runs, compare medians); document the method; see `performance-regressions.md` |
| 4 Repeated-run check  | Use `scripts/repeat-run.py`; choose the run count as described in `nondeterministic-failures.md`                                                                  |
| 5 Manual verification | Record steps, expected result, and captured evidence; flag it as unguarded in the evidence table and the report                                                   |

## After green

Run the guard and the original feedback loop. When the guard was never seen red, perform the revert-fix check from Phase 7.

## Do not

- Weaken, skip, or delete a failing check to get green.
- Widen a tolerance until the check passes.
- Update a snapshot or golden file without confirming the new output is correct behavior.
