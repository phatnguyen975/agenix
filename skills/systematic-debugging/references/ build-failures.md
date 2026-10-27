# Build, CI, and Dependency Failures

## Read the first error

Later errors often cascade from the first one. Fix or explain the first error, rerun, then read the next.

## Classify

| Kind                         | Typical signs                                  | First checks                                                                                                              |
| ---------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Syntax or type error         | Points to a file and line                      | Recent edits; compiler or type-checker version                                                                            |
| Missing or unresolved module | Import or path error                           | Name, path, and letter case; generated files; skipped install or build step; build ordering                               |
| Configuration                | Missing or wrong setting                       | Environment variables; path assumptions; configuration files in effect                                                    |
| Dependency resolution        | Version conflict, unresolved package           | Lockfile against manifest; transitive version changes; registry or network failure; platform-specific packages            |
| Toolchain mismatch           | Works with another compiler or runtime version | Versions in use against versions the project expects                                                                      |
| Stale or corrupted artifacts | Passes after a clean build                     | Caches; generated code; build output directories                                                                          |
| CI-only                      | Passes locally                                 | Operating system and architecture; working directory; permissions; missing secrets; parallelism; time and resource limits |

## Method

1. Reproduce with the exact command and environment of the failing build (same image, container, or versions where possible).
2. Compare a clean build with an incremental build.
3. Diff what changed between the last passing build and the first failing build: lockfile, manifest, configuration, toolchain version, CI definition, base image.
4. Bisect dependency versions or commits (`isolation.md`).
5. For network or registry errors, repeat the build with `scripts/repeat-run.py` before concluding.

## Rules

- Clear caches and generated files in a controlled way and record what was cleared.
- Do not delete lockfiles or state blindly.
- Do not pin versions, skip steps, or disable lint and type rules as the fix without a confirmed root cause.
- Do not edit generated files; fix the generator or its input.
