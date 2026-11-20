# Configure Project CI

## Inputs and Decisions

Verify the architecture baseline and approved scaffold runtime, applicable services and test harness evidence. Read `config.agenix.json`, approved codebase design, test strategy, stack and applicable conventions. Inspect existing workflows, repository rules, release-unit dependency graph and verified commands, versions, targets, services and permissions. Establish required checks and merge queue behavior from actual repository settings.

Ask the human at the start whether to configure a project-owned pre-commit hook. Reuse a prior explicit decision. If approved, configure the selected existing hook mechanism to run appropriate verified fast checks; document activation, run it locally with a clean example and prove it rejects a controlled violation. Restore the candidate and verify success. Keep required checks in CI independently. Do not install or activate a hook without the decision.

Use [CI/CD and Automation](../../ci-cd-and-automation/SKILL.md) selectively for quality gate ordering, CI configuration and feedback. The approved strategy determines required checks, targets and tools. Use only CI guidance relevant to the approved checks.

## Design and Verify CI

Use [Application CI Guidance](../assets/agenix-application.yml) as the starting point. For a single release unit, configure its verified checks directly. For multiple release units, use the application workflow as the caller and gate, with jobs or local reusable workflows for affected release units and shared checks. A release unit is an independently identifiable application, service, library or tool. A job is a CI execution unit and may run one or several checks. Split files only where it clarifies ownership. Set up the checks selected for the current scaffold; add new checks when their behavior and harnesses exist.

For selective execution, compare the PR head against the merge base of its base and head SHAs so the selection reflects the PR changes. For a merge queue, use the merge-group base and head. For default-branch pushes, use the event's before and after revisions. Fetch the exact revisions or sufficient history before comparing them. Obtain both old and new paths for renames, as well as deleted paths. Map those paths to the approved unit ownership and transitive consumers, including shared configuration, lockfiles, workflows and dependency-graph changes.

Use an existing verified project graph tool or a project-owned change-detection script when it can produce an explicit selection for every required release unit and shared check. Git supplies the changed paths; the graph or mapping determines affected checks. If history, rename information or mapping cannot be established reliably, select all potentially affected checks, or all checks when the affected set is unknown. Detection errors must not produce an empty successful selection. Ensure changes to detection logic and its mapping trigger the checks needed to validate them.

The stable gate runs even when a release unit is unaffected. It verifies detection succeeded, every selected job completed successfully and only jobs proven unnecessary were skipped. Fail for selected skipped, failed, cancelled or missing results, or an incomplete mapping. A reusable workflow runs through `workflow_call` in the caller's run so the gate can evaluate its result. Keep `Agenix Artifacts Gate` as a separate required check. Verify the actual repository ruleset and check names; do not assert one gate covers checks outside its workflow.

Use `pull_request`, default-branch `push` and `merge_group` where required. Avoid workflow-level path filters for required checks. Apply minimum permissions, avoid exposing secrets to untrusted PR code, pin actions to verified full commit SHAs or the approved immutable dependency mechanism, and isolate test services. Set caching, concurrency and timeouts only where appropriate to the project and verify cache invalidation.

Before publication, validate workflow syntax and expressions with available project-appropriate tooling. Exercise detection and gate logic locally using isolated Git histories or equivalent fixtures. Cover a release-unit-only change, a shared dependency and its consumers, shared configuration, a rename across release-unit boundaries, deletion, missing history, and unknown mappings. Check that the gate accepts a proven unaffected skip and rejects detection errors, selected failures, cancellations and unexpected skips. Use the same detection logic and mapping as CI. Verify clean local commands and any approved hook before creating the PR. Report checks that require the hosted runner as pending.

## Publish and Prove Enforcement

Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates) to the exact intentional-failure and restored candidate snapshots and their intended sequential publication. After approval, publish the failure snapshot to the owned scaffold branch and draft PR. Verify the expected assertion causes the required hosted check to fail. Publish the approved restored snapshot and verify required checks pass for its head or proven test-merge revision. Do not treat syntax errors, missing discovery, skipped jobs or unavailable services as the intended failure. Reconcile existing PRs and snapshots on resume.

Record actual results, revisions, check names, permissions, triggers and verified commands in durable non-secret evidence for the final environment record. Report pending checks and blockers. The final instructions step owns final scaffold approval and separate merge authority.
