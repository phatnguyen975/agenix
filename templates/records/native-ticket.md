<!--
Render the issue body for a GitHub ticket or the equivalent Jira description. Use the
tracker title "<agenix-id>: <title>". Set scope, priority and status in native labels as
required by the selected tracker. Use the approved definition and stable labels below.
Remove authoring comments and placeholders before publishing. Keep label names in
English and use the project's approved documentation language for prose.
-->

## Outcome

<!--
Write the bounded outcome approved for the ticket. State what changes for its consumers
and what is in scope.
-->

<Approved ticket outcome>

## Details

<!--
Use one value per label. Feature is the Agenix feature ID. Feature Reference is the
project-relative feature record path at its full approved revision. Type follows the
project work-type convention. Use lowercase scope and priority values that match the
native labels. Owner is the approved responsibility.
-->

- **Feature:** <feature-id>
- **Feature Reference:** `<project-relative feature record path>` at `<approved revision>`
- **Type:** <work type>
- **Scope:** <lowercase scope>
- **Priority:** <lowercase priority>
- **Owner:** <approved owner>

<!--
Include Origin only for applicable additive work. Use the source finding, amendment or
preceding item as an artifact or evidence reference. This is provenance.
-->

- **Origin:** <source reference>

## Dependencies

<!--
List only ticket IDs from the owning feature. Use one bullet per ID. Replace the list
with the standalone text "None" when empty. Verify corresponding native links where
supported.
-->

- <ticket-id>

## References

<!--
List pinned spec, contract, data or UI targets required by this ticket. For each entry,
use a project-relative path with an optional anchor or an HTTPS URL, followed by the
approved revision. Add the parenthesized Acceptance suffix where the target supplies
criteria. Select at least one acceptance ID across all entries. Use comma-separated IDs.
Omit the suffix when it does not apply.
-->

- `<target>` at `<approved revision>` _(Acceptance: <acceptance-id>[, <acceptance-id>])_

<!--
Keep later approval, task mappings, results and PR references in checkpoint comments.
Add native tasks under this issue after the task plan is approved. On Jira, render each
heading as its fixed label paragraph and use ADF paragraphs, lists and links for body
content.
-->
