<!--
Render as a readable tracker or PR comment. Keep the fixed English labels so the tracker
adapter can extract fields. Write narrative content in the project's approved
documentation language. Use the exact approved or observed values. Omit inapplicable
sections, optional rows and authoring comments. Keep Git-owned checkpoints in their JSON
records.
-->

## Checkpoint

<!--
Checkpoint ID is stable within the owning record. Use the exact phase and step, UTC
timestamps ending in Z, and the Agenix item ID for item steps. Omit Item for an itemless
step. Outcome states the actual result. Next Action appears only when work remains. Use
one evidence reference per bullet under References. Write None if the reference list is
empty.
-->

- **Checkpoint ID:** <checkpoint-id>
- **Phase:** <phase>
- **Step:** <step>
- **Item:** <Agenix item ID>
- **Recorded At:** <RFC 3339 UTC timestamp>
- **Outcome:** <observed outcome>
- **Next Action:** <outstanding action>

### References

<!--
Use a project-relative path or durable HTTPS URL. Add the full commit for
snapshot-specific Git evidence. Include the checkpoint ID when selecting one inside a
JSON record.
-->

- `<target>` [at `<evidence commit>`] [_(Checkpoint: <checkpoint-id>)_]

## Candidate

<!--
For Git approval or review, record the intended parent commit and candidate tree.
Include Target Base Commit when review depends on it. For remote definition publication,
include Baseline Commit and preserve the approved definitions in Task Plan or Ticket
Plan. Both forms can appear for a mixed batch. Use full Git object IDs.
-->

- **Base Commit:** <intended parent commit>
- **Tree:** <candidate tree>
- **Target Base Commit:** <target base commit>
- **Baseline Commit:** <prerequisite Git revision>

## Task Plan

<!--
Use for a parent ticket approving native child creation. Include each exact approved
task definition, using the native task body sections under its full Agenix ID and title.
Keep the task's identity, parent, dependencies, references, acceptance and verification
unchanged. Publish the parent checkpoint before creating children.
-->

### <task-id>: <title>

<Approved task definition>

## Ticket Plan

<!--
Include the approved native ticket definitions when recording a batch approval here. Use
the native ticket sections under each full Agenix ID and title. Preserve the
authoritative feature plan and record later native mappings separately.
-->

### <ticket-id>: <title>

<Approved ticket definition>

## Decision

<!--
Kind is artifact, review, feature-acceptance, merge, exposure, manual-confirmation,
cancellation or override. Result is approved, changes-requested, passed or failed as
applicable. Use human-in-session or a verified native identity for Actor. Record the
actual confirmation. Record each authorized action and its exact target. State PR and
head for merge. State operation, target and revision or artifact for exposure. For
manual confirmation include the applicable acceptance IDs or check IDs. Record findings
and accepted risks under the outcome or evidence references.
-->

- **Kind:** <decision kind>
- **Result:** <decision result>
- **Actor:** <human-in-session or verified native identity>
- **At:** <RFC 3339 UTC timestamp>
- **Confirmation:** <actual confirmation>
- **Authorized Action:** <action> — <exact target>
- **PR:** #<number> — <PR URL>
- **Head Commit:** <full approved PR head>
- **Operation:** <operation-id>
- **Target:** <approved exposure target>
- **Revision:** <approved revision>
- **Artifact:** <approved artifact reference>
- **Acceptance:** <comma-separated acceptance IDs>
- **Checks:** <comma-separated check IDs>

## Verification

<!--
Repeat the Check heading and fields for each receipt. Result is passed, failed, pending,
skipped or unavailable. Use the checked Revision or Tree. Include Item and its
Acceptance IDs for work-item checks. Keep level and mode when applicable. Require an
evidence pointer for a completed check and Detail for pending, skipped or unavailable.
Record actual outcomes even when an exception applies.
-->

### Check: <check-id>

- **Item:** <Agenix item ID>
- **Acceptance:** <comma-separated acceptance IDs or None>
- **Result:** <observed result>
- **At:** <RFC 3339 UTC timestamp>
- **Environment:** <verified environment>
- **Revision:** <checked Git commit>
- **Tree:** <checked candidate tree>
- **Check Level:** <applicable level>
- **Mode:** <applicable mode>
- **Evidence:** <durable evidence reference>
- **Detail:** <explanation>

## Publication

<!--
Record the actual published head and PR when available. Add Merge Commit only after
verification. List each verified native mapping with the Agenix ID, native issue number
or Jira key and numeric ID, and URL. On post-merge repair use References to preserve
both PRs, revisions and check results.
-->

- **Head Commit:** <published Git commit>
- **PR:** #<number> — <PR URL>
- **Merge Commit:** <verified merge commit>
- **Native Mapping:** <Agenix item ID> — <native identifiers and URL>

## Disposition

<!--
Use for an approved cancellation or override. Always record the affected item and
reason. For cancellation, record replacement references when applicable. For override
use allow-work or accept-incomplete and record the reviewed revision, exact waived
conditions, permitted work and consumer scope. Keep the actual human decision in
Decision.
-->

- **Item:** <Agenix item ID>
- **Reason:** <reason>
- **Replacement:** <replacement reference>
- **Action:** <allow-work or accept-incomplete>
- **Revision:** <reviewed commit>
- **Waived Condition:** <exact waived condition>
- **Permitted Work:** <authorized scope>
- **Consumer Scope:** <consumers covered by the override>
