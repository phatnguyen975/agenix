# Structural Enforcement

## Purpose

Translate important boundary decisions into **checks that detect violations** and governance for constraints that cannot be fully tested automatically. Do not claim a policy is verified when only a reviewer could judge it. The strongest enforcement is often provided by the language/build system; architectural tests and linters supplement it.

## Classes of Enforcement

| Mechanism                          | What It Can Prove                                                                              | Limitation                                                                                        |
| ---------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Compiler/package/module visibility | Illegal imports/exports or undeclared build dependencies fail at source/build time             | Only enforces boundaries expressible in that ecosystem                                            |
| Import/static dependency rules     | Forbidden imports, paths, declared dependencies, layer direction when each is actually scanned | Dynamic imports, reflection, generated code, multi-language references may require extra handling |
| Architecture tests                 | Graph constraints, package ownership, cycles, public/internal boundaries                       | Requires correct module mapping, tool configuration, test input coverage                          |
| CI checks                          | Executes build/tests, validates generated files and graph checks                               | CI itself is a runner, not a unique detection method                                              |
| Ownership/review protection        | Assigns reviewers and, when enabled, requires approval                                         | Does not detect invalid dependency edges automatically                                            |
| Focused review checklist           | Semantic boundaries, naming clarity, inappropriate shared behavior                             | Human judgment; must name owner/review trigger                                                    |

Do not treat an `EN-xx` entry with `CI` as sufficient unless it states the actual check executed by CI.

## Enforcement Selection

1. Identify the rule (`DR-xx` or `CV-xx`) and its **observable violation**.
2. Identify the graph/artifacts the checker reads: static imports, build manifests, public exports, source folders, generated artifacts, or code review changes.
3. Prefer native visibility/build checks when available, then static graph/import checks, then semantic review for parts that cannot be automated.
4. Name the exact tool only after confirming the project's language/version and existing tooling actually support the desired rule; otherwise state a **mechanism class** and a concrete feasibility task, not an invented configuration.
5. Record feedback stage, owner, failure message/action, and limitations. If automation is not currently available, mark the gap rather than claiming compliance.

**Example of a meaningful check:**

```text
DR-01: No module outside Orders may import Orders/internal/**.
EN-01: Static import-boundary check over production and test sources,
       except Orders' own tests; fail PR CI with source and target paths.
```

**Noncheck:** `EN-01: Keep the codebase clean using CI.`

## Rule-Type Matrix

| Constraint                         | First Choice                                              | Additional Safeguard                                                   |
| ---------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------- |
| Public entry points only           | Language/package visibility or export maps                | Forbidden-import check for bypass paths                                |
| Module dependency allowlist        | Build dependency declarations or dependency graph checks  | PR CI report showing offending edge                                    |
| Layer/core direction               | Architecture/static graph checks                          | Module-focused review of semantic responsibilities                     |
| Static module cycles               | Strongly connected component check over full module graph | Baseline for known legacy cycles                                       |
| Cross-unit implementation imports  | Separate released artifact visibility or graph checks     | Compatibility test of published package API or protocol when warranted |
| Shared package ownership           | Repository ownership/review rules                         | Change-impact testing of declared consumers                            |
| Generated source freshness         | Generator reproducibility/diff check                      | Review source-of-truth changes                                         |
| Naming/public errors/config access | Linter/architecture check where expressible               | Semantic review of uncovered behavior                                  |

Use one check for several rules if its coverage is explicit. A single rule can use multiple checks. Neither `DR` nor `CV` IDs imply automation in all ecosystems.

## Define the Graph Precisely

- Map every source/build target to a module; list allowed internal test exceptions.
- Distinguish direct from transitive edges and source-import from build-declaration graphs. A direct-import rule may pass while a transitive forbidden dependency or an undeclared build edge remains; choose and check the intended policy.
- Specify whether to include dynamic imports, code generation, vendored code, type-only imports, dependency injection registrations, and build scripts. Include relevant edges or state blind spots.
- Restrict the graph to intended architectural nodes; unrelated cycles inside a module are not automatically violations of the _inter-module_ cycle policy.
- Report exact source, target, governing rule, and permitted remediation. Never silently skip unmapped code.

## Run Stages

- **Editor/local:** fast import and naming feedback when available.
- **Pre-commit/pre-submit:** relevant quick tests, optional based on project workflow.
- **Pull request CI:** authoritative checks that should block new structural violations.
- **Merge/mainline and scheduled:** comprehensive graph or integration checks when cost justifies them.
- **Code review:** semantic rules that cannot be reduced to a reliable static check.

State whether each check is blocking, advisory, or not yet implemented. An owner is needed to maintain and respond to failures.

## Legacy Violation Baselines

When a repository already violates target rules:

1. Record a **specific, reviewable inventory** of existing violations: exact source/target edges or paths, rule, owner, and planned resolution.
2. Make checks reject **new or expanded** violations, including new instances of existing exception patterns.
3. Shrink the baseline as each migration step closes gaps. Do not grandfather an entire directory or turn off the rule globally.
4. Keep current baseline generation deterministic; review updates instead of automatically accepting new entries.
5. Remove an exception once the code is compliant.

**Example:** `Orders/internal → Payments/internal` can remain temporarily as one enumerated legacy edge while any second bypass fails. An unrestricted `Orders/**` ignore would not enforce this.

## Human Decision Gate vs. Enforcement

A **design checkpoint** approves structural choices before they are adopted; a **review/CI check** detects violations of adopted rules afterward. Do not substitute a passing architecture check for human approval of a new boundary, or label an approved diagram as proof that source imports comply. `CODEOWNERS` may suggest reviewers, but required approval depends on repository protection settings. If an exception changes an approved boundary or affects consumers, obtain decision approval separately from updating its enforcement baseline.

## Verification Requirements

For every numbered rule link at least one `EN-xx` entry specifying check or review mechanism, evidence scope, stage, owner, and status. Use keyed list entries in the design template rather than a wide register table. Verify that:

- Every rule ID resolves to at least one real mechanism or an explicitly documented enforcement gap.
- The check's scanner includes the claimed language, paths, and artifact types.
- A deliberate violating fixture or example causes a failure (negative test); verify this in the real checker when execution is available, otherwise label the test unexecuted.
- A compliant example is accepted (positive test), including declared exceptions; test at least one case outside each exception's exact scope.
- Rule changes update the check and any baseline together.
