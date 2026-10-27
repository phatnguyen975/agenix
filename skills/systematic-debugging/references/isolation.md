# Isolation (Phase 2)

**Goal:** the smallest failing scenario and a narrowed location. Each technique answers one question: where, how small, since when.

## Localize (where)

1. List the layers or components the failing path crosses (for example client → API → service → data store, or build → test → package → deploy).
2. Observe at every boundary in one run: what enters, what leaves, which configuration and environment values arrive, and the relevant state.
3. The faulty component is the first boundary where actual output differs from expected output.
4. When boundaries are many, binary-search the pipeline: check the middle stage first, then the half that contains the divergence.
5. **Tools:** debugger, existing logs, tracing, network inspection, temporary tagged logs.

## Reduce (how small)

Delta-debugging approach:

1. List what can be removed: input data, request fields, configuration entries, callers, steps, dependencies, test setup.
2. Remove half (or one item) at a time and run the feedback loop.
3. Keep the removal if the feedback loop stays red; undo it if the feedback loop turns green.
4. Stop when every remaining element is necessary: removing any one makes the failure disappear.
5. Record the result as the minimal reproduction; Phase 4 turns it into the regression guard.

Keep a copy of the full scenario; Phases 5 and 7 rerun it.

## Bisect (since when)

| Dimension                            | Method                                                                                                                                                 |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| History                              | Version-control bisection with the feedback loop as the test (for example `git bisect run COMMAND`; other version-control systems offer an equivalent) |
| Input                                | Halve the input until the smallest failing slice remains                                                                                               |
| Configuration or dependency versions | Halve the differences between the working and failing states                                                                                           |
| Test order                           | See `nondeterministic-failures.md`                                                                                                                     |

History bisection details:

- Verify first that the feedback loop passes on the known-good revision and fails on the known-bad one.
- Exit code 0 marks a revision good, 125 skips an untestable revision, other codes from 1 to 127 mark it bad, and codes above 127 abort. A missing command that returns 127 is treated as a bad revision, not as a setup error; verify that the runner starts successfully before invoking the bisect, or every tested revision may be mislabeled bad.
- Skip revisions that do not build.
- A flaky feedback loop gives wrong verdicts: pin its reproduction rate first (`nondeterministic-failures.md`).
- Cache builds and narrow the test target when builds are slow.

The first bad revision or smallest differing setting shows what changed; Phase 3 explains why.

## Exit

- Minimal reproduction recorded.
- Location or range narrowed.
- Independent failures found along the way are recorded as separate root causes.
