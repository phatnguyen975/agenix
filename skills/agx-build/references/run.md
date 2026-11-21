# Execute Ticket Tasks

## Inputs and Readiness

Resolve the ticket from the merged feature plan, verify ownership, merged dependency evidence and applicable approvals. Read the approved task plan and checkpoints from the owned ticket branch or native tracker, including the parent snapshot and verified child mappings for remote mode. Read pinned ticket references and acceptance, scoped instructions, applicable UI/data contracts and conventions, test strategy, `environment.agenix.json`, relevant code and existing test harnesses. Preserve unrelated work and reconcile prior partial execution before resuming.

Apply [Decide Readiness and Record Progress](../../../references/work-items-and-evidence.md#decide-readiness-and-record-progress) and the configured [Local](../../../references/trackers/local.md#read-verify-and-update), [GitHub](../../../references/trackers/github.md#confirm-state-and-closure) or [Jira](../../../references/trackers/jira.md#confirm-native-state) tracker rules. Verify prerequisite evidence rather than trusting status alone. Use actual approved commands and services; run applicable baseline checks and report pre-existing failures and unavailable checks. Stop affected work when evidence cannot support verification.

## Implement and Verify Each Task

Use [Incremental Implementation](../../incremental-implementation/SKILL.md) to coordinate the approved batch. Select the lowest numeric ID among approved, non-cancelled tasks whose prerequisites are satisfied. Repeat as dependencies clear. Record ticket and task `IN-PROGRESS` when work starts. Verified provisional results can unblock dependent tasks only within the same active run; they do not establish durable completion. Preserve existing definitions and use additive planning for newly discovered obligations.

For each task, execute its approved method and checks under [Specify Verification and Assess Evidence](../../../references/work-items-and-evidence.md#specify-verification-and-assess-evidence):

- **Test-first:** use [TDD](../../tdd/SKILL.md) for behavior-focused Red, Green and Refactor cycles. Record an intended assertion failure and subsequent pass; harness or setup failure is not Red. Do not manufacture a failure for existing behavior.
- **Test-after:** implement against the agreed expected results, then add and run the approved automated checks. Use focused test-design guidance when needed; do not claim test-first evidence.
- **Manual:** perform applicable automated checks and prepare the approved procedure and expected result. Record human-only judgment as pending until the responsible human confirms it in review; do not report the task complete.

After each task, inspect the changed code for a worthwhile in-scope simplification. Use [Code Simplification](../../code-simplification/SKILL.md) only when relevant behavior has passing coverage and a concrete improvement exists. Preserve behavior and rerun affected checks; do not force a refactor or expand scope.

For an owned persistence change, use the approved data impact and task scope to determine whether a migration is needed:

1. Compare the pinned analysis with the latest integrated schema declarations and relevant migration history. Check the owning prerequisite, overlapping parallel changes and toolchain ordering; reassess affected assumptions if the baseline has moved. Stop affected work when the approved intent no longer fits.
2. When needed, create the migration in the approved toolchain's project-native location, using its identifiers and ordering rules. Implement the approved schema, data conversion and rollout intent; split steps when compatibility or rollout requires it. Preserve migrations already applied to shared environments and use a new forward migration for corrections. Provide and test a down operation only when required and safe; otherwise record recovery and irreversible effects.
3. Run applicable initialization on an empty disposable store and upgrades from a representative prior state with data. Verify resulting structures, constraints, backfills, supported reader/writer compatibility and recovery as applicable. Record actual migration paths or revisions, commands, candidate and results in the owning evidence. Do not claim a migration is applied in any environment without evidence from that environment.

## UI and Test Routes

Apply only routes relevant to the affected work and the project's approved stack and tool versions:

- [UI Styling](../../ui-styling/SKILL.md): use selected token, theming, responsive or accessible component techniques for applicable Tailwind or shadcn/ui work.
- [React Composition Patterns](../../vercel-composition-patterns/SKILL.md): consult relevant rules for React component APIs, composition or state boundaries. [React Best Practices](../../vercel-react-best-practices/SKILL.md): consult affected React/Next.js rendering, fetching or bundle guidance. Do not impose patterns or unsupported version-specific APIs.
- [Vitest](../../vitest/SKILL.md) for the selected compatible runner and [React Testing](../../react-testing/SKILL.md) for relevant React component or hook tests. Use them with either automated method while honoring its order. Derive assertions from approved behavior and verify examples against installed versions.
- For affected web UI, inspect and interact with the actual rendered implementation in a browser at applicable targets and states before presenting the batch. Use [Playwright CLI](../../playwright-cli/SKILL.md) when selected and available, or an approved equivalent. Apply [Accessibility](../../accessibility/SKILL.md) for relevant semantics, keyboard, focus and targeted automated checks. Record actual evidence and gaps; automation alone does not establish full conformance.

Implement the written feature UI contract and inherited global rules. Use contract-based mocks or synthetic data at the client boundary when approved, without presenting mock evidence as real integration. Verify required real integration separately when available. Historical prototype code is design evidence, not production code or a regression suite; do not add prototype-only replay controls to the product.

## Approve and Publish the Batch

Run required local checks and affected regressions on each eligible increment and on the combined candidate. Check acceptance, cross-task interaction, exposure isolation and the complete diff. Record commands, results, environment, candidate and evidence; distinguish failures, pending PR checks and manual judgments. Resolve affected failures or report the blocker. A partial handoff for contract review requires explicit approval and states its limits; new obligations return to task planning.

Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates) to the checked batch and intended publication. After approval, [publish the candidate](../../../references/git-publication.md#publish-the-approved-candidate) on the owned ticket branch, verify the actual revision and push, and record durable evidence on the owning ticket or tracker checkpoint. Mark a task `DONE` only when its approved checks, committed implementation and durable evidence satisfy the shared completion rules. A published manual task awaiting human judgment is `IN-REVIEW`. Keep manual judgments and PR-dependent checks pending at their owning stages; do not create the implementation PR here. Report the published revision, completed and pending tasks, checks and blockers. Follow the shared session closure rules.
