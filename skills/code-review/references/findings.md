# Findings

Defines the shared finding schema, severity, confidence, exclusions, IDs, and verdict. Every sub-agent and the main agent must use the same contract.

## Severity

Severity reflects the **credible impact and likelihood in the changed context**, not the axis, author's intent, or OWASP category number.

| Severity | Meaning                                                                                                          | Typical Examples                                                                                                                                           |
| -------- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Critical | Must be fixed before merge/release; severe impact is readily reachable or the change breaks a critical invariant | Remotely exploitable compromise; broad privileged access; major data loss/corruption; core operation unusable; severe production secret exposure           |
| High     | Should be fixed before merge; plausible, material impact under realistic conditions                              | Significant authorization/data exposure; common-path defect; unsafe migration; important contract break; missing tests for security/data-critical behavior |
| Medium   | Should be fixed; may be deferred with an owner, reason, and tracking item                                        | Edge-case defect with bounded impact; material maintainability/performance gap; partial test gap; moderate rule deviation                                  |
| Low      | Optional improvement with limited impact                                                                         | Small hygiene or readability improvement with a concrete rationale                                                                                         |

Do not inflate severity to make a finding visible. Do not downgrade a confirmed high-impact defect to be polite. When uncertain between adjacent levels, choose the lower level and explain the uncertainty.

## Confidence

| Confidence | Meaning                                                                               | Handling                                                                   |
| ---------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| High       | Directly verified in changed code, applicable documents, or actual command output     | Report as a finding                                                        |
| Medium     | Strong technical reasoning, but one material context element is unverified            | Report as a finding and state the verification gap in Evidence/Limitations |
| Low        | Plausible suspicion, ambiguous requirement, or missing evidence prevents confirmation | Put under Questions, not Findings                                          |

Severity and confidence are independent. A potentially Critical issue with Low confidence is a Question until verified.

## Finding Schema

Each finding must contain all fields below. Use `N/A: <reason>` only when a field truly cannot apply.

| Field              | Required content                                                                                                                                                                                                                                                                                  |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID                 | Axis prefix and sequential number, e.g. `COR-01`; assigned by the main agent after deduplication                                                                                                                                                                                                  |
| Title              | Concise, defect-oriented statement of the problem; avoid vague wording such as "Improve security"                                                                                                                                                                                                 |
| Axis               | One primary owning axis                                                                                                                                                                                                                                                                           |
| Severity           | Critical, High, Medium, or Low                                                                                                                                                                                                                                                                    |
| Confidence         | High or Medium; Low belongs in Questions                                                                                                                                                                                                                                                          |
| Location           | Exact path and line range: `path:start-end` resolves against the reviewed snapshot (head/working tree). For deleted lines that no longer exist there, use `path@base:start-end` and label it as deleted. For multiple distinct sites, list each exact anchor; do not use an ambiguous prose range |
| Category           | Relevant axis checklist item or exact documented rule                                                                                                                                                                                                                                             |
| Evidence           | Minimal code/config/test/command excerpt and, where relevant, exact spec/rule source and section. Redact secrets. Evidence must establish the behavior, not merely show a suspicious name                                                                                                         |
| Problem and impact | What happens, who/what is affected, conditions required, and concrete impact; quantify when supported                                                                                                                                                                                             |
| Recommendation     | Smallest actionable change that addresses the root cause; state constraints and avoid speculative rewrites                                                                                                                                                                                        |
| Fix verification   | Specific test, command, invariant, query/metric, or observable behavior that would prove resolution                                                                                                                                                                                               |
| Related            | Related finding IDs and/or `Also flagged by: <axis names>`; use `None` when empty                                                                                                                                                                                                                 |

For security findings, Evidence or Problem and impact must describe the attack path in prose: attacker, controlled input/capability, vulnerable behavior, and resulting impact. Do not include working exploit payloads or code.

For multiple locations caused by one root cause, list every confirmed affected location in the same finding. A deleted-line finding must use a base-side anchor (`path@base:start-end`) and identify the deleted diff hunk; do not invent a head-side line number. Avoid combining independent causes merely because they share a file.

Example (illustrative; language-neutral pseudocode):

```markdown
### COR-01: Pagination omits the final item

| Severity | Confidence | Axis        | Location           | Category        |
| -------- | ---------- | ----------- | ------------------ | --------------- |
| High     | High       | correctness | src/list.ext:42-47 | Boundary values |

**Evidence**

`end = start + page_size - 1; items = all[start:end]` — the slice end is exclusive, so the final item is excluded.

**Problem and impact**

Every full page returns one fewer item than requested; records can be skipped by consumers.

**Recommendation**

Set the exclusive slice end to `start + page_size` and retain the existing upper-bound clamp.

**Fix verification**

A regression test with 10 records and page size 5 returns two complete pages of 5 records without overlap or omission.

**Related**

None
```

## Ownership and Deduplication

- Each finding has exactly one **primary Axis**, chosen by the axis that owns the root defect and remediation.
- Report one finding per root cause. If several axes identify the same defect and same remediation, keep the best-evidenced version and note the other axes as `Also flagged by`.
- Keep separate findings when the root causes or required remediations differ, even if locations overlap.
- An out-of-axis observation is not a finding for the current agent. Route it to the owning axis or list it in Out-of-scope Observations.
- The main agent verifies every finding and may ask the owning axis to substantiate it; it must not create an unsupported finding from an aggregation hunch.

## ID Prefixes

| Axis                      | Prefix |
| ------------------------- | ------ |
| spec-compliance           | SPC    |
| standards-compliance      | STD    |
| correctness               | COR    |
| design                    | DES    |
| maintainability           | MNT    |
| testing                   | TST    |
| security                  | SEC    |
| performance               | PRF    |
| dependencies              | DEP    |
| compatibility-operability | CMP    |
| user-facing               | UXF    |

The main agent assigns IDs sequentially by primary axis only after findings have been verified, deduplicated, and ordered. Re-number after any finding is dropped or merged. Update every `Related` reference. Question IDs use `Q-01`, `Q-02`, etc.

## Exclusions

Do not report:

- Pre-existing problems that the change does not introduce, touch, expose, or materially affect.
- Issues already enforced by configured compiler/linter/formatter/static-analysis tooling, unless the change disables or bypasses that enforcement.
- Personal preference, speculative future needs, or style polish without a documented rule or concrete engineering impact.
- Behavior explicitly allowed by an authoritative requirement or project rule.
- A theoretical vulnerability without a credible attacker-controlled path and impact.
- Unchanged code outside the review boundary, except as evidence/context for a changed defect.
- A missing test as a duplicate production-code defect; report the production defect on its owning axis and the test gap only when it is a distinct testing finding.

## Calibration Rules

- Apply severity consistently across axes: equal impact and likelihood receive equal severity.
- A hard documented-rule violation is High when it protects security, correctness, privacy, or an architecture boundary; otherwise Medium unless impact warrants a different level.
- Advisory-rule deviation is normally Low unless a concrete material impact is established.
- Raise severity for broad exposure, irreversible effects, security/data-integrity risk, or many affected users; lower it for contained, reversible impact.
- Do not use severity as a proxy for confidence or for the importance of the axis.

## Verdict

| Verdict               | Condition                                                                    |
| --------------------- | ---------------------------------------------------------------------------- |
| Request changes       | At least one Critical or High finding remains                                |
| Approve with comments | No Critical/High findings remain, but one or more Medium/Low findings remain |
| Approve               | No findings remain                                                           |

The verdict/counts include verified findings returned by `Completed` and `Partial` axes. A `Partial` axis contributes its substantiated findings, but an absence of findings does not imply full coverage. `Failed` and skipped axes are not assessed. Always disclose every non-Completed status and its scope. Questions do not change the finding count/verdict, but material unresolved Questions must be called out in the rationale/limitations.

## Question Entries

Use Questions for confidence-Low concerns, unresolved spec/source conflicts, or details needed to determine applicability. Each entry states:

- ID (`Q-01`, sequential)
- Axis
- Location (`path:line`, range, or `n/a`)
- Uncertainty (what is uncertain and why it cannot be confirmed)
- Needed to Settle It (exact information, evidence, or decision needed to resolve it)

Do not use Questions to hide a finding that is already supported by evidence.
