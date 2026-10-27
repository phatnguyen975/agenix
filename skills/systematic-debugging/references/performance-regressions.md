# Performance Regressions

## Define before measuring

- **Metric:** latency percentile, throughput, memory, CPU, startup time, size.
- **Workload:** fixed input and size.
- **Environment:** hardware, background load, tool and dependency versions.
- **Budget or baseline:** the known-good value and an acceptable margin.

## Measure

- For steady-state metrics, warm up and discard initial runs. For startup/cold-start metrics, define and measure cold-start conditions instead of discarding the behavior being measured.
- Repeat enough runs (ten or more is typical) to report the median and spread (minimum and maximum, or percentiles); use a larger sample when variance or the decision threshold requires it.
- Keep conditions identical before and after, and isolate the machine from other load.
- The feedback loop returns red when the metric exceeds the budget by more than the measured noise.

## Locate

- Profile (CPU, memory and allocation, I/O, locks and contention) instead of guessing.
- Differential profile: profile the known-good and the current version and compare.
- Bisect history with the benchmark as the feedback loop and the threshold as the verdict (`isolation.md`).

## Hypothesis classes

- Algorithmic complexity growth.
- Repeated work: missing or invalidated cache, N+1 queries, redundant I/O.
- Allocation and garbage-collection pressure.
- Lock contention or serialization.
- Configuration: pool sizes, timeouts, debug flags.
- Dependency version change.
- Data growth.

## Fix and guard

- Change only the measured hotspot, then measure again with the same method and report before and after with the spread.
- Guard level 3: a benchmark with a threshold set above the measured noise.
- A deterministic alternative: assert an operation count (queries, allocations, calls) that stays bounded.

## Avoid

- Optimizing without a profile.
- Micro-optimizing outside the hotspot.
- Changing several things at once.
- Comparing measurements taken under different conditions.
- Trusting a single run.
