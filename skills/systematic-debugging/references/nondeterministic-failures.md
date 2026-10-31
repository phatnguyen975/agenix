# Non-Deterministic Failures

**Goal:** turn "sometimes" into a measured reproduction rate, then treat the failure as deterministic.

## Measure

- Run: `python scripts/repeat-run.py --runs N [--parallel K] --timeout S -- COMMAND`.
- Each execution passes when the command exits 0; any failed or timed-out run makes the overall command fail. Use `--stop-on-fail` only when an early stop fits the investigation, and use `--json` when machine-readable results help.
- Manual fallback: run the command N times in a shell loop and count non-zero exits.
- Reproduction rate = failed or timed-out executions divided by total executions actually started. Choose a bounded run/time budget and increase N enough to observe multiple failures when practical. If `--stop-on-fail` prevents later runs from starting, report the actual execution count, not the planned count. If no failures occur, report "not reproduced in N runs"; do not treat that as proof the failure is gone.

## Raise the rate

- Repeat; run in parallel; add CPU or I/O load; shrink timing windows; randomize order; vary data size; run on constrained resources.
- Add temporary delays at suspected race points.
- Use data-race detectors or thread sanitizers where the platform provides them.
- Capture the seed and inputs of every failing run. `repeat-run.py` sets `REPEAT_RUN_INDEX` for each invocation (zero-based); captured output is not redacted, so inspect and redact it before sharing or including it in the report.

## Cause classes

| Class                          | Signs                                                            |
| ------------------------------ | ---------------------------------------------------------------- |
| Timing, races, async ordering  | Passes alone, fails under load; depends on speed                 |
| Shared state, order dependence | Fails only after certain tests or only in the full suite         |
| Environment                    | Depends on time, timezone, locale, resource limits, ports, files |
| Randomness                     | Unseeded random values, hash ordering, unordered collections     |
| External dependency            | Network or service variability                                   |

## Pin determinism

- Seed randomness and log the seed.
- Use a fixed or fake clock.
- Use per-run temporary directories and ephemeral ports (`REPEAT_RUN_INDEX` is set for each run by `repeat-run.py`).
- Isolate or reset shared state.
- Stub external services at the boundary.
- Sort unordered output before comparing.

## Condition-based waiting

Replace arbitrary delays with waiting for the condition that matters.

- Poll for the condition (state reached, event received, file present, response available) at a short interval, with a timeout that fails with a message naming the condition.
- Read fresh state on every poll; do not reuse a value captured before the polling started.
- An arbitrary delay is justified only when testing time-based behavior itself: wait for the triggering condition first, then delay for a documented duration derived from the known interval.
- Increasing delays, retries, or timeouts is not a fix.

## Test-order pollution

**Symptom:** a test fails only after other tests ran.

- Remove any pollution already present before the run; the script refuses to start when pollution is already present and never deletes pollution. A previous suite run often left it.
- Start with a clean pollution target. Find the polluter: `python scripts/find-polluter.py --pollution-path PATH --glob 'TEST-GLOB' -- RUNNER {test}`. For state that is not a file or directory, use `--check-command`, whose command exits 0 while the state is clean and non-zero when pollution is present.
- The helper stops at the first candidate after which pollution is detected. The runner's exit code is reported but does not determine pollution, and the helper never deletes pollution; remove the initial pollution yourself before running.
- Manual fallback: run candidate tests one at a time and check the state after each.
- Alternative: bisect by order. Run the first half of candidates followed by the failing test, then recurse into the half that reproduces the failure. Use the runner's ordering options and record the failing order or seed.
- Fix the state leak or reset it in setup/teardown; reordering tests alone hides the defect.

## Guard (level 4)

- Measure the failure rate p before the fix.
- For an estimated pre-fix failure rate `0 < p < 1`, choose N so a clean result is unlikely by chance: the probability of N clean, independent runs is approximately (1 − p)^N, so use N ≥ ln(0.05) / ln(1 − p). Examples: p = 0.5 → N = 5; p = 0.1 → N = 29; p = 0.01 → N = 299. The estimate assumes independent runs and a reasonably stable rate; correlated or changing conditions weaken it. If p = 0 because the failure was not observed, the formula cannot establish a useful N: gather more evidence or improve reproduction. If every observed run fails (p = 1), report that observed rate and a bounded run count; the formula is unnecessary.
- Report the observed rate and N before and after the change, along with the method and conditions.
- A clean result lowers the chance of a remaining failure but does not prove it impossible. Use it with root-cause evidence and other applicable checks.
