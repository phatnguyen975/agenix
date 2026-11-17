# Domain Guidance

Select the section matching the requested outcome. Each route describes inputs, query choices, interpretation and how the result supports the task. [Command Selection](commands.md) owns invocation shapes and version notes.

## Orientation

**Input:** An unfamiliar module, directory or task question, plus the intended project/worktree.

Use `files` for indexed layout, `explore` for a focused structural question, or `context` for a task-oriented evidence package. Use status/coverage information to understand omissions. Query one relevant module before expanding to adjacent boundaries.

Return a map of important symbols, dependencies and source locations that guides the next inspection. Explain behavior only after reading its source and relevant contracts. Ranking, exclusions and parser support limit the map; it is not an architectural or business summary by itself.

## Debugging

**Input:** A symptom, entry point, suspect symbol or proposed connection. Preserve actual failure evidence separately from the graph.

Start with `explore` around the identified flow. Use `node` for source and `callers`/`callees` for unresolved one-hop questions. A `query` can first resolve an ambiguous name. Distinguish parser-derived and heuristic relationships where the result exposes that distinction; do not invent confidence labels if it does not.

Use the path to form a hypothesis and identify a reproduction or observation that would test it. Static paths do not establish which path executed, its ordering or its root cause. Framework callbacks and cross-language edges depend on actual version/language support; check the returned evidence rather than assuming complete resolution.

## Refactoring

**Input:** Exact target definition, proposed change and affected scope.

Resolve the definition with `query`/`node`, then use `impact` with a depth appropriate to the question. Inspect candidate callers and public boundaries, reading source when needed. Use `explore` for relationships that a symbol-centered blast radius does not explain.

The output is a bounded candidate impact set, not an automatic edit list or safety guarantee. Account for limits, external consumers, generated references, reflection, dynamic dispatch and changed/deleted definitions absent from the current index. A rename proposal still requires its normal compatibility checks and tests.

## Change Review

**Input:** A specified base/candidate diff or changed-file list, including relevant renames/deletions, and the index representing the candidate.

Map changed definitions through `query`/`node`; investigate important risks with bounded `impact`, and use `affected` on the changed-file set for candidate test files. For a deleted definition, the candidate graph may no longer contain it; use available base/source evidence and disclose the gap rather than treating an empty result as no impact.

Contribute grounded risk findings and proposed verification to the existing review. `affected` does not establish runtime coverage or that a test asserts the changed behavior. Inspect relevant tests and retain required regression, integration and manual checks. This route neither fixes code nor creates a separate approval.

## Architecture and Patterns

**Input:** The expected structural rule and a declared module/symbol scope.

Use `files` to bound the indexed area, `query` to locate candidate symbols by name/kind, and `explore`/`node` to inspect their relationships and source. A limited search result is not a full inventory. Establish the expected set through available source/index evidence before making an all-symbols claim.

Return specific observations and candidate outliers against the rule. Missing inheritance, implementation or route edges can reflect parser/resolution gaps as well as real inconsistency; verify relevant source before concluding a violation. Static relationships do not alone establish deployment topology, architectural intent or stylistic conformance.

## Code Hygiene

**Input:** A bounded area and a question about potentially unused or colliding symbols.

Use `query` for candidates, then `callers` and `node` for evidence about a definition. Compare full symbol identities and public/exported roles rather than equating a shared name with a collision.

Zero indexed callers suggests investigation, not deletion. Entry points, framework hooks, external consumers, references outside the indexed language/scope and reflective use may not appear. Keep findings explicitly provisional until the relevant consumers and source have been checked.

## Entry-to-Sink Mapping

**Input:** An entry point and the operation or boundary of interest, such as a persistence call.

Use `explore` to locate plausible static connections and `callees`/`node` to inspect unresolved steps. Identify the source locations that require deeper reasoning and distinguish actual returned paths from hypotheses connecting them.

This is structural reachability, not a taint or security analysis: a call path does not prove that a particular value reaches a sink, bypasses validation or is exploitable. Security findings need their actual data propagation, controls and verification evidence.

## Test Impact

**Input:** The intended changed-file set and approved verification obligations for the candidate.

Use `affected` with the correct project, traversal depth and test-file detection/filter. Inspect its results as dependency-linked test candidates, including relevant provider/client boundaries not represented in one graph. A custom filter can exclude tests as well as locate them.

Use candidates to prioritize investigation or targeted runs within the caller's existing test strategy. Empty output is not permission to run no tests; a short result is not authority to replace the required suite. Record graph coverage, limits and any uncertainty in proposed test selection. No test is executed by this query.
