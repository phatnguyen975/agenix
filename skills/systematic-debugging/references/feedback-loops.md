# Feedback Loops (Phase 1)

A feedback loop is a single command that reproduces the symptom and returns a pass/fail verdict. Every later phase runs it, so its quality sets the speed and reliability of the whole investigation.

## Required properties

- **Red on the exact symptom:** the same error text or wrong behavior as reported, not a nearby failure.
- **One command, agent-runnable:** no human step and no manual setup between runs.
- **Fast:** seconds, not minutes; every hypothesis costs one run.
- **Deterministic:** the same verdict on every run. For non-deterministic failures, a pinned reproduction rate instead (see `nondeterministic-failures.md`).
- **Sharp:** asserts the specific symptom, not a vague condition such as "does not crash".

## Construction options

Try in order; use the first that fits.

| Option                                  | Fits when                                                       | Notes                                                                       |
| --------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Failing automated test                  | A test level reaches the faulty code                            | Can become the regression test in Phase 4                                   |
| Command-line or API call with a fixture | The failure is observable through a public interface            | Store inputs (files, payloads) in a fixture so every call is identical      |
| Headless UI script                      | The failure is visible only in a user interface                 | Drive the UI with an automation tool; assert on specific text or state      |
| Captured trace replay                   | Production input, logs, network capture, or a crash dump exists | Replay the captured input against the current code                          |
| Temporary harness                       | The faulty code is hard to reach                                | A small script that calls the suspect code directly with the failing input  |
| Property or fuzz test                   | The failure depends on unusual inputs                           | Generate inputs until the failure appears; keep the failing seed and input  |
| Differential comparison                 | A known-good version or reference implementation exists         | Run the same input through both; compare outputs                            |
| Bisection harness                       | The failure appeared between two known states                   | A feedback loop that returns pass or fail per revision (see `isolation.md`) |
| Human-in-the-loop                       | None of the above is possible                                   | `reproduction-fallbacks.md`                                                 |

## Tighten

- **Faster:** narrow to the smallest test target or fixture, cache setup, skip unrelated steps.
- **Sharper:** assert the specific message, value, or state change.
- **More deterministic:** pin time, seed randomness, isolate filesystem, network, and ports, fix test data.

## Verify before moving on

1. Run the feedback loop and confirm it returns red.
2. Compare the failure text or behavior with the reported symptom.
3. If it passes, do not immediately infer an environment mismatch. Check that the assertion captures the exact symptom, the inputs/state and version match, and the failure is not intermittent. If relevant conditions still differ or are unknown, read `environment-failures.md` and ask for the smallest missing detail.
4. Record the command and its result; Phases 5 and 7 rerun it.

## Pitfalls

- Building an elaborate harness before trying a simple command.
- Starting to fix while the feedback loop is still incomplete.
- A feedback loop that fails for unrelated reasons (setup error, missing dependency) and is mistaken for the symptom.
