<!--
Render the body for a GitHub sub-issue or Jira sub-task. Set the native title to
"<agenix-id>: <title>" and attach it to the approved native parent. Native labels and
state carry lifecycle status. Use the exact approved definition from the parent
task-plan checkpoint. Remove authoring comments and placeholders. Keep labels in English
and write narrative content in the approved documentation language.
-->

## Outcome

<!-- State the observable outcome approved for this task. -->

<Approved task outcome>

## Details

<!-- Use the Agenix parent ticket ID and verify it matches the native relationship. -->

- **Parent Ticket:** <ticket-id>

<!--
Include Origin only for applicable additive work. Use the source finding, amendment or
preceding item as an artifact or evidence reference. Keep dependency IDs in
Dependencies.
-->

- **Origin:** <source reference>

## Dependencies

<!--
Use one bullet per sibling task ID. Replace the list with the standalone text "None"
when empty.
-->

- <task-id>

## References

<!--
Optional. Omit the entire section when the parent already supplies the required
references. Otherwise use one pinned target per line and narrow the parent's scope.
-->

- `<target>` at `<approved revision>`

## Acceptance

<!--
Keep at least one observable criterion. Give each a distinct task-local ID. Every
criterion must cover one or more IDs selected by the ticket. List covered IDs separated
by commas and keep the Covers label literal.
-->

- **<task acceptance ID>:** <observable criterion> _(Covers: <ticket-covered acceptance ID>[, <ticket-covered acceptance ID>])_

## Verification

<!--
Method is test-first, test-after or manual. Checks are distinct approved check IDs
separated by commas. Automated methods require at least one check. Use the exact value
"None" only for manual tasks with no applicable automated checks. For test-after and
manual include Exception Reason. Include Manual Procedure, Expected Result and
Responsible Verifier only for manual. Manual tasks require human confirmation and
cannot be prerequisites for other tasks. Copy the approved values. Derive check
levels from the check definitions.
-->

- **Method:** <test-first, test-after or manual>
- **Checks:** <check IDs or None>
- **Exception Reason:** <approved reason>
- **Manual Procedure:** <approved procedure>
- **Expected Result:** <observable expected result>
- **Responsible Verifier:** <person or role responsible for confirming the result>

<!--
Keep actual results, human confirmations and revision evidence in checkpoints. On Jira,
render section labels as standalone ADF paragraphs and preserve the approved field
wording and lists.
-->
