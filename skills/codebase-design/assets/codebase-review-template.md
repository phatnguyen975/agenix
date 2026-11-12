<!--
OUTPUT TEMPLATE — Full Codebase Review

Use only when a full, persistent structural review report is explicitly
requested. This is an evidence-backed snapshot, not a target design approval.

Filling Rules
1. Keep the five numbered sections. Text inside <...> describes the
   information to supply; replace it with actual evidence-based content.
   Remove instructional comments and unneeded sample rows.
2. Repeat assessments, findings, recommendations, and checks for the actual
   number of items. A single example row or record is not a fixed count.
   Omit optional summaries when they duplicate a short set of detailed records.
3. State the examined scope and its limits. Distinguish Observed evidence from
   inferred risks and Proposed recommendations. Mark unrun checks as Not Run;
   never equate absence of findings with whole-repository health.
4. Use G-xx IDs unique within this report. Cross-report matching uses issue
   identity, paths, and rules, not the same G number. Severity describes harm;
   priority describes action order; confidence describes quality of evidence.
5. Review recommendations are Proposed and do not authorize source edits.
   Detailed target design, executable migration steps, and approval belong to
   the Design Path. For an inapplicable required section use
   'Not applicable — <Why this section does not apply>' rather than an empty table.
-->

# Codebase Review: <Project Name>

## 1. Review Overview

<!-- Specify review type (focused, full, periodic), date/revision if known,
     requested scope, source-of-truth rules, inaccessible/unexamined areas,
     and prior review used for comparison (when available). -->

- **Type and Objective:** <Focused, Full, or Periodic review and its objective>.
- **Scope:** <Included repositories, release units, modules, and explicit exclusions>.
- **Date / Code Revision:** <Review date and commit or revision; identify unverified values>.
- **Applicable Design / Rules:** <Applicable approved design, rules, and project instructions, or None>.
- **Coverage:** <Areas fully inspected, partially inspected, or not inspected>.
- **Previous Review:** <Comparable earlier report path or Not available>.

**Executive Summary:** <Concise assessment of confirmed structural health, major risks, and review limits>

## 2. Current-State Assessment

<!-- Repeat one assessment per meaningful architectural area or release unit.
     Include observed layout, module/public boundaries, dependency graph,
     shared ownership, test seams, and enforcement only where relevant. Prefer
     direct evidence (paths, imports, manifests, executed checks) to inference.
     This is a current-state description, not an unapproved target structure. -->

### <Reviewed release unit or structural area>

- **Observed Structure:** <Observed layout, module surfaces, and dependency edges with source locations>.
- **Assessment:** <Observed strengths, substantiated risks, and limits of the evidence>.
- **Evidence / Limits:** <Supporting paths, manifests, checks actually run, and evidence gaps>.

## 3. Findings

<!-- Repeat one G record for each established violation, evidenced risk, or
     improvement opportunity. If there are no substantiated findings, state:
     'No findings established within the examined scope' and keep the
     limitations in Section 5. Do not manufacture findings to fill the form.
     Use the optional compact index for longer reports (e.g., several findings);
     omit it when detailed entries are already easy to scan. -->

| Finding                | Severity   | Confidence   |
| ---------------------- | ---------- | ------------ |
| G-01 — <Finding title> | <Severity> | <Confidence> |

### G-01 — <Concise observed issue or improvement opportunity>

- **Type / Severity / Confidence:** <Violation, Risk, or Opportunity>; <Critical, High, Medium, or Low>; <Verified, Likely, or Unverified>.
- **Observation and Evidence:** <Specific paths or imports, violated rule if any, and actual check output>.
- **Expected Boundary / Authority:** <Applicable adopted DR/CV rule or project authority, or No binding rule>.
- **Impact / Affected Consumers:** <Likely or observed consequences and affected consumers>.
- **Assessment Basis:** <Why the impact and evidence support these classifications>.
- **Recommended Direction:** <Smallest justified improvement and its main trade-off>.
- **Verification Gap:** <Additional evidence needed, or None>.

## 4. Recommendations and Improvement Plan

<!-- Repeat one item for each recommended improvement, ordered by action
     priority rather than finding severity. One action may address several
     findings; a finding may require several actions. This is an assessment
     backlog, NOT an executable migration sequence or implementation approval.
     Note the owner only if known and the decision required to proceed. -->

1. **<Now, Next, Later, or existing priority label> — <Short recommended improvement>**
   - **Addresses:** <Related finding IDs or cross-cutting risk>.
   - **Action / Expected Benefit:** <Proposed improvement and expected structural benefit>.
   - **Trade-Off / Dependencies:** <Expected costs, blockers, prerequisites, and interactions>.
   - **Owner / Decision Needed:** <Owner or Unassigned, and design or approval required before execution>.

<!-- Include this comparison only when an accessible prior report covers
     comparable scope. Match findings by issue identity and evidence, not G ID. -->

**Change Since Previous Review:** <New, continuing, resolved, or unverified issues with supporting evidence>

## 5. Verification and Limitations

<!-- Include one row per executed, unrun, or blocked structural check relevant
     to the assessment. Keep coverage and evidence concise; if full details are
     long, replace that row with a keyed record. Do not present a planned tool
     as an actual executed result. -->

| Check   | Result   | Scope   | Source         |
| ------- | -------- | ------- | -------------- |
| <Check> | <Result> | <Scope> | <Evidence ref> |

- **Blind Spots:** <Dynamic or generated edges, unknown consumers, and uninspected areas>.
- **Follow-Up Evidence:** <Specific additional inspections or evidence needed to verify tentative findings, or None>.
- **Follow-Up Trigger:** <Requested follow-up condition or interval, or Not set>.
