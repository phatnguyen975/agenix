# Command Selection

Use this reference to choose a CLI operation, then consult `codegraph help <command>` for the installed command's arguments, flags and defaults. This is a task-oriented map, not a duplicate CLI manual.

Invocation shapes below were checked against local CodeGraph **1.6.2** help. Other versions require interface verification; version metadata for this skill is separate from the external tool version. Upstream background: [versioned CLI reference](https://github.com/colbymchenry/codegraph/blob/v1.6.2/README.md#cli-reference). Installed help takes precedence when syntax differs from a documentation example.

## Query Selection

| Command Shape                                                        | Use it For                                                           | Important Interpretation                                                               |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `codegraph status "<root>" --json`                                   | Index statistics/availability at an explicit root                    | Statistics do not prove candidate alignment or full language coverage                  |
| `codegraph files --path "<root>" --filter "<directory>"`             | Indexed file layout in a bounded area                                | Indexed layout is not a complete filesystem inventory                                  |
| `codegraph query "<name>" --path "<root>" --json`                    | Name-based symbol discovery; optionally filter kind/count using help | Resolve all relevant definitions, not just the first ranked match                      |
| `codegraph explore "<question with symbol or file>" --path "<root>"` | Structural context and paths around a focused question               | Ranked context may omit paths or source outside its bounds                             |
| `codegraph context "<task>" --path "<root>"`                         | A task-oriented package of symbols, relationships and code           | Select when gathering task context rather than only tracing a specific connection      |
| `codegraph node "<symbol>" --path "<root>" --file "<relative-file>"` | Source/trail for a disambiguated definition                          | Check the returned definition actually matches; a narrowing hint is not proof          |
| `codegraph node --file "<relative-file>" --path "<root>"`            | File source/line context and dependents                              | Use ordinary file reads when the indexed view is unnecessary or insufficient           |
| `codegraph callers "<symbol>" --path "<root>" --json`                | Incoming one-hop call relationships                                  | Count/definition limits can truncate the result                                        |
| `codegraph callees "<symbol>" --path "<root>" --json`                | Outgoing one-hop call relationships                                  | Edges are not a runtime sequence or data propagation trace                             |
| `codegraph impact "<symbol>" --path "<root>" --json`                 | Bounded transitive impact                                            | In 1.6.2 default depth is 2; specify/record relevant depth for deeper questions        |
| `codegraph affected "<relative-file>" --path "<root>" --json`        | Tests linked through indexed file dependencies                       | In 1.6.2 default depth is 5; detection/filter rules and graph gaps affect completeness |

## Inputs and Output Handling

For symbol commands, inspect returned identities and paths. `callers`, `callees` and `impact` in 1.6.2 accept `--file` to narrow definitions; a no-match hint can still return other definitions with a note. Treat warnings as part of the result.

Inspect relationship kinds rather than treating every returned item as a function call: caller results can include a file-level `imports` relationship as well as `calls`. Source returned from disk and graph edges can have different freshness; current source text does not prove that the indexed relationships have caught up. In 1.6.2, `status --json` exposes pending file changes, index state and worktree mismatch information; inspect available indicators alongside relevant source alignment.

For `affected`, pass the explicitly selected changed-file list as separate arguments or via its `--stdin` option with one path per line. Preserve paths containing spaces. Establish the intended comparison first, including how additions, deletions and renames are represented. The skill does not prescribe a shell pipeline or silently choose the diff baseline.

Structured-output flags vary: `query`, `callers`, `callees`, `impact`, `affected`, `files` and `status` expose `--json` in 1.6.2; `context` uses `--format json`. `explore` and `node` do not expose `--json` in that help. Do not attach flags by analogy.

Use result limits to keep retrieval useful, but report their effect and widen a query when a pending conclusion requires it. Missing coverage and stale edges cannot be corrected by merely raising a limit. Resolve index readiness/freshness through the caller's approved environment process; do not mutate source or index state without the appropriate authority.
