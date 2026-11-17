# Closing (Phase 8)

## Evidence Table Rules

- One row per claim; the columns are Claim, Command, Output, Assessment. The assessment states whether the evidence supports or contradicts the claim, not whether the command exited zero. A red pre-fix test supports the claim that the bug reproduces; retain its actual failure/exit code in Output.
- For post-change claims, use fresh command output captured after the final change. The pre-fix symptom and guard-red rows intentionally use the recorded pre-fix output.
- Show the exit code or the pass/fail summary line; trim long output to the lines that prove the claim.
- Redact secrets and personal data.
- A check that was not run is listed with the assessment `not run` and the reason; an unverifiable claim is removed or labeled unverified.
- Include rows for the original symptom before any fix; the guard red before and green after when a root-cause fix is applied (state its hierarchy level); the original feedback loop after the change; test suites compared with the baseline; applicable build, lint, and type-check commands; and cleanup of temporary instrumentation. For Mitigated and Unresolved sessions, report the original loop's actual result and mark inapplicable checks as `not applicable` with a reason rather than inventing a red/green result.

## Status

| Status     | Meaning                                                                                                                                                    |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Resolved   | Root cause fixed; guard seen red then green; verification passed                                                                                           |
| Mitigated  | Impact reduced by a labeled, reversible mitigation; the mitigation-specific check passes; the root cause or original failure remains explicitly documented |
| Unresolved | Diagnosis or repair is incomplete; record confirmed causes separately from hypotheses, blockers and missing evidence                                       |

## Commit Message Draft

Provide only when requested or required by the caller.

- Follow the project's commit convention (discovered in Phase 0).
- First line: what was fixed.
- Body: symptom, confirmed root cause (the hypothesis that held), fix, and the regression guard.
- No secrets. Do not commit unless the human asks.

## Follow-ups

Each item is a concrete action or finding. Categories:

- Hardening proposals ([Hardening](hardening.md)).
- Areas left without a regression guard.
- Observability gaps.
- Architectural findings (for example, no test seam exists, or repeated failures in one component).

## Close Message

```markdown
## Close

- **Status:** <Resolved, Mitigated, or Unresolved>
- **Root cause:** <one sentence, or "not found">
- **Fix:** <what changed, or "none">
- **Evidence:** <the evidence table, delivered above this message>
- **Follow-ups:** <the list of follow-ups, or "none identified">
- **Report:** <the path written, or "not written" with the reason>
```
