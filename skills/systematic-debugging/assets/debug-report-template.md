# Debug Report Template

Adapt to caller output. Replace placeholders with actual evidence. Outcome definitions belong to the closing reference; do not invent a final outcome when the investigation is still awaiting a required decision. Keep optional measurements and follow-ups only when useful.

```markdown
# Debug Report: <Symptom or Area>

> **Outcome:** <Resolved / Mitigated / Unresolved>
> **Date:** <YYYY-MM-DD>
> **Candidate:** <source revision or identifiable working state>

## Summary

<What failed, what was established, what changed and what remains. Distinguish
an effective mitigation from root-cause repair. Mention the main blocker if unresolved.>

## Symptom and Context

- **Expected:** <observable behavior and its authoritative source>
- **Actual:** <exact error, wrong value or measured regression; redact sensitive data>
- **Impact:** <observed affected users/data/operations, or unknown>
- **Reproduction:** <command or observation steps, inputs and relevant environment>
- **Scope:** <authorized investigation/repair and preserved pre-existing work>

## Diagnosis

<Repeat only for confirmed causes. If none are confirmed, say so.>

### <Confirmed Cause Identifier>

- **Cause and Location:** <defect, file/function/config/data; exact anchor where available>
- **Mechanism:** <how it produces the symptom>
- **Origin or Trigger:** <verified introduction/condition, or explicitly unknown>
- **Confirmation:** <experiment, prediction and actual observation; cite evidence below>

| Hypothesis        | Prediction           | Experiment            | Observation     | Conclusion                           |
| ----------------- | -------------------- | --------------------- | --------------- | ------------------------------------ |
| <candidate cause> | <falsifiable result> | <single-factor probe> | <actual result> | <confirmed / refuted / inconclusive> |

<Keep material experiments and ruled-out alternatives, not a transcript.
For unresolved work, identify the missing evidence or blocked experiment.>

## Changes

<State no changes when appropriate. Identify repair versus mitigation,
retained changes versus reverted attempts, authorization for consequential
choices and any unresolved restoration state.>

- **<Path / Setting>:** <actual change and why it addresses the cause or reduces impact>

## Regression Guard

<If no guard applies or could run, state why and the resulting protection gap.
For mitigation, name its specific effectiveness check and the remaining original failure.>

- **Level and Seam:** <chosen hierarchy level, location and rationale>
- **Assertion:** <specific intended behavior>
- **Before:** <observed failure for the right reason>
- **After:** <observed result on the final candidate>

## Verification

<Include original symptom, guard pre/post, final original loop, relevant suite
baseline comparison, applicable build/lint/type checks and cleanup. Distinguish
a deliberately failing pre-fix check from evidence contradicting a claim.
Missing evidence is not a pass. Include measured before/after statistics here
when useful, with workload, sample counts, conditions and uncertainty.>

| Claim / Candidate | Command or Observation                           | Actual Output     | Assessment                                                         |
| ----------------- | ------------------------------------------------ | ----------------- | ------------------------------------------------------------------ |
| <one fact>        | <exact executed command or recorded manual step> | <redacted result> | <supported / contradicted / not run / not applicable, with reason> |

## Follow-ups

<Omit when empty. Include unresolved causes/repairs, guard gaps, external
handling limits and separately proposed hardening where applicable.>

- **<Remaining Issue>:** <next action or decision, and owner when known>
```
