# Design the Feature Web UI

## Applicability and Inputs

Use this step when the feature includes an owned web UI. If it does not, report the basis for omission without creating an artifact.

Read the approved feature record and behavior specification on the feature specification branch, including actors, acceptance, flows and states. Verify that applicable API and data outputs are approved before relying on them; read their relevant contracts, wire examples and data constraints. Read the approved global `docs/blueprint/ui-design/README.md` and token source, applicable system or client design, tech stack, conventions and test strategy for shared rules and supported targets. Inspect affected existing feature UI contracts and production screens where a flow crosses their boundaries. Follow applicable scoped project instructions.

Verify scaffold merge and required checks on the refreshed default branch. Apply [Decide Readiness and Record Progress](../../../references/work-items-and-evidence.md#decide-readiness-and-record-progress) to feature dependencies and applicable overrides; use [Local Tracker](../../../references/trackers/local.md#read-verify-and-update) for local status verification and the applicable shared rules for Git-owned feature evidence in remote modes. A blocked feature requires an explicitly scoped human override before permitted work can proceed. Resolve material conflicts through the owning amendment route and confirm consequential unresolved design decisions with the human before dependent work.

## Define the Feature Design

Create `docs/features/<feature-id>/ui-prototype/`:

```text
ui-prototype/
├── README.md
├── index.html
├── styles.css
├── app.js
├── assets/         # when visual assets are needed
└── data/           # when scenario fixtures are needed
```

Use the [UI Prototype Template](../assets/ui-prototype-template.md) for the README. It owns feature-specific screens, flows, states and interaction criteria, with stable acceptance references. Inherit the global design and link its authoritative rules and tokens; describe feature-specific applications without creating a competing design system. Identify affected existing screens and cross-feature handoffs without redefining their owners' behavior. Ask for confirmation when a material feature-specific decision remains open. Amend shared foundations through their owner if the approved direction must change.

Apply [Frontend Design](../../frontend-design/SKILL.md) selectively to resolve or critique feature-specific visual and interaction choices within the approved global direction. Use [UI/UX Pro Max](../../ui-ux-pro-max/SKILL.md) focused searches only for unresolved flow, state or component questions; evaluate suggestions against approved requirements and do not persist another design system. Consult [UI Styling](../../ui-styling/SKILL.md) only for applicable token, responsive or interaction techniques supported by the selected stack; do not impose its framework on the lightweight prototype.

## Build and Verify the Prototype

Implement the feature demonstration in lightweight HTML, CSS and JavaScript. Add files only where needed. Select deterministic scenarios that cover the feature's relevant acceptance, screens, transitions and applicable loading, empty, error, success and recovery states. Provide start, selection, reset and replay instructions; use synthetic data. Reference canonical wire examples for API payloads, keeping scenario state and transformed display fixtures in `data/` where needed. Label simulated external or cross-feature interactions and do not invent production behavior or claim real integration.

Replay every selected scenario in a real browser before the design gate. Check the approved viewport and browser targets, responsive layout, navigation, keyboard and focus, relevant themes and languages, and visible states. Compare rendered results with the README, spec and shared design; correct discrepancies. Use [Playwright CLI](../../playwright-cli/SKILL.md) when selected and available, or another approved browser tool that provides equivalent evidence. Use [Accessibility](../../accessibility/SKILL.md) for targeted checks; distinguish automated findings from manual evidence and do not claim full conformance from automation alone. Record actual coverage, results and limitations.

The demonstration is design-time evidence, not production code or a production regression suite. During implementation, build the actual frontend using its approved stack and verify affected behavior against the written contract and applicable scenarios. Contract-based mocks or synthetic data may exercise the real client path before the provider is ready; real integration remains required where specified. Prototype-only reset and replay controls do not belong in production UI unless independently required. Preserve the initial approved prototype as historical evidence; once implementation begins, amend the written UI contract using production evidence rather than synchronizing historical prototype code.

## Approve and Publish

Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates) to the README and demonstration together. Present the feature screens, flows, shared touchpoints, acceptance coverage, rendered scenarios, browser evidence, limitations and intended publication. Obtain human review of the rendered UI and material design decisions. After approval, publish the approved prototype and record its actual revision in the README through an approved mechanical update; do not embed a commit's own SHA in that commit. Bind the approved README in the feature record as described in the skill entry point.

[Publish the Approved Candidate](../../../references/git-publication.md#publish-the-approved-candidate) on the feature specification branch and bind approval and verification evidence to its revision in the phase PR or a durable checkpoint. Reconcile existing work on resume. If this is the final applicable specification step, verify the complete specification set, acceptance coverage, references, amendments and applicable evidence; obtain separate merge authority and verify the merge and required checks. Otherwise leave the phase open for the remaining applicable steps. Follow the shared session closure rules.
