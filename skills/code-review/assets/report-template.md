<!-- Complete every section in order. Use `N/A: <reason>` where a section does not apply. Remove this comment from the final report. -->

# Code Review Report: <change title>

## 1. Metadata

| Field             | Value                                                                      |
| ----------------- | -------------------------------------------------------------------------- |
| Review date       | <YYYY-MM-DD>                                                               |
| Review target     | <ref range / commit(s) / working tree / PR diff / pasted diff / file list> |
| Reviewed revision | <base..head / commit / working-tree snapshot / current file state>         |
| Commits           | <count and short list, or N/A with reason>                                 |
| Change size       | <files> files; +<added> / -<removed> lines, or unavailable                 |
| Change assessment | <cohesive / acceptable / split recommended>; <mixed concerns or none>      |
| Report scope      | <all applicable axes / selected focus / partial scope>                     |

## 2. Summary and Verdict

**Verdict:** <Request changes | Approve with comments | Approve>

**Rationale:** <one or two sentences grounded in findings and unresolved material questions>

**Verdict scope:** <verified findings from Completed and Partial axes; state that Partial coverage is incomplete and Failed/Skipped axes are unassessed>

| Axis      | Critical | High | Medium | Low | Total |
| --------- | -------: | ---: | -----: | --: | ----: |
| <axis>    |      <n> |  <n> |    <n> | <n> |   <n> |
| **Total** |      <n> |  <n> |    <n> | <n> |   <n> |

**Top risks** (up to three):

- <finding ID>: <one-line impact>

**Merge-blocking findings:** <Critical/High IDs, or `None`>

**Unresolved material questions:** <Q-IDs, or `None`>

## 3. Scope and Inputs

### 3.1 Reviewed Scope

<Repository/revision, exact changed files or file groups, diff source, excluded binary/generated files, and any scope limitation.>

### 3.2 Inputs

| Input                          | Used                                                             |
| ------------------------------ | ---------------------------------------------------------------- |
| Change description             | <source/text or none>                                            |
| Spec sources                   | <paths/sections or none available>                               |
| Standards sources              | <paths/sections or none found>                                   |
| Tooling-enforced rules skipped | <linters/formatters/compiler/static analysis or none identified> |
| Verification commands          | <documented/user-supplied commands or none available>            |
| Focus                          | <requested axes or all applicable axes>                          |

### 3.3 Axis Status and Coverage

Allowed status values: `Completed`, `Partial`, `Failed`, `Skipped — not applicable`, `Skipped — requested`.

| Axis                      | Status   | Notes                                       |
| ------------------------- | -------- | ------------------------------------------- |
| spec-compliance           | <status> | <reason, files/groups, or spec unavailable> |
| standards-compliance      | <status> | <reason and rules reviewed>                 |
| correctness               | <status> | <reason and files/groups>                   |
| design                    | <status> | <reason and files/groups>                   |
| maintainability           | <status> | <reason and files/groups>                   |
| testing                   | <status> | <reason and files/groups>                   |
| security                  | <status> | <reason and files/groups>                   |
| performance               | <status> | <reason and files/groups>                   |
| dependencies              | <status> | <reason and files/groups>                   |
| compatibility-operability | <status> | <reason and files/groups>                   |
| user-facing               | <status> | <reason and files/groups>                   |

### 3.4 Limitations and Not Verified

- <item, reason, and impact on review confidence; or `None`>

## 4. Verification Results

| Command   | Status                      | Summary                         |
| --------- | --------------------------- | ------------------------------- |
| <command> | <passed / failed / not run> | <key output, or reason not run> |

Do not include commands that were not actually run as if they passed.

## 5. Findings

<Order by severity (Critical, High, Medium, Low), then primary axis. Use one block per root cause and the exact schema below.>

### <ID>: <Title>

| Severity   | Confidence    | Axis           | Location                                                    | Category   |
| ---------- | ------------- | -------------- | ----------------------------------------------------------- | ---------- |
| <severity> | <High/Medium> | <primary axis> | <path:start-end; use path@base:start-end for deleted lines> | <category> |

**Evidence**

<Minimal source excerpt and/or exact spec/rule source + section + observed command output. For security, include the attack path in prose. Redact secrets.>

**Problem and impact**

<What happens, affected actors/data/systems, trigger/preconditions, and concrete impact.>

**Recommendation**

<Specific, actionable fix addressing the root cause.>

**Fix verification**

<Exact regression test/check/invariant/metric that demonstrates resolution.>

**Related**

<Related IDs; `Also flagged by: <axes>`; or `None`>

## 6. Questions

| ID   | Axis   | Location                                                  | Uncertainty                | Needed to Settle It             |
| ---- | ------ | --------------------------------------------------------- | -------------------------- | ------------------------------- |
| Q-01 | <axis> | <path:lines, path@base:lines for deleted content, or n/a> | <what cannot be confirmed> | <specific evidence or decision> |

## 7. Spec Traceability

<N/A if no applicable spec source was available; omit the table and behavior list in that case.>

| Req | Atomic Requirement                                  | Status                                                                    | Evidence                                             |
| --- | --------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------- |
| R1  | <quoted or paraphrased requirement (file, section)> | <Implemented / Partial / Missing / Incorrect / Not verifiable / Violated> | <changed path:lines, test, or reason not verifiable> |

**Behavior not covered by the spec:**

- <path:lines>: <description; not automatically a finding>

## 8. Out-of-scope Observations

- <path:lines>: <pre-existing/out-of-axis observation; suggested axis; whether that axis was run; or `None`>

## 9. Positive Observations

- <path:lines>: <notable good practice; or `None`>

## 10. Remediation Order

1. <finding ID>: <why first; prerequisites/dependencies; or `N/A: no findings`>
