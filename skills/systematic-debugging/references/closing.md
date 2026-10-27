# Closing (Phase 8)

## Evidence table rules

- One row per claim; the columns are Claim, Command, Output, Verdict.
- For post-change claims, use fresh command output captured after the final change. The pre-fix symptom and guard-red rows intentionally use the recorded pre-fix output.
- Show the exit code or the pass/fail summary line; trim long output to the lines that prove the claim.
- Redact secrets and personal data.
- A check that was not run is listed with the verdict `not run` and the reason; an unverifiable claim is removed or labeled unverified.
- Include rows for the original symptom before any fix; the guard red before and green after when a root-cause fix is applied (state its hierarchy level); the original feedback loop after the change; test suites compared with the baseline; applicable build, lint, and type-check commands; and cleanup of temporary instrumentation. For Mitigated and Unresolved sessions, report the original loop's actual result and mark inapplicable checks as `not run` with a reason rather than inventing a red/green result.

## Status

| Status     | Meaning                                                                                                                                                    |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Resolved   | Root cause fixed; guard seen red then green; verification passed                                                                                           |
| Mitigated  | Impact reduced by a labeled, reversible mitigation; the mitigation-specific check passes; the root cause or original failure remains explicitly documented |
| Unresolved | No root cause confirmed; the investigation log shows what was tested, ruled out, and what evidence remains missing                                         |

## Commit message draft

- Follow the project's commit convention (discovered in Phase 0).
- First line: what was fixed.
- Body: symptom, confirmed root cause (the hypothesis that held), fix, and the regression guard.
- No secrets. Do not commit unless the human asks.

## Follow-ups

Each item is a concrete action or finding. Categories:

- Hardening proposals (`hardening.md`).
- Areas left without a regression guard.
- Observability gaps.
- Architectural findings (for example, no test seam exists, or repeated failures in one component).

## Close message

```markdown
## Close

- **Status:** <Resolved, Mitigated, or Unresolved>
- **Root cause:** <one sentence, or "not found">
- **Fix:** <what changed, or "none">
- **Evidence:** <the evidence table, delivered above this message>
- **Follow-ups:** <the list of follow-ups, or "none identified">
- **Report:** <the path written, or "not written" with the reason>
```
