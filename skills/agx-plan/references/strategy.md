# Select Feature Delivery Strategy

## Inputs and Readiness

Resolve the feature through the merged catalog on the refreshed default branch. Read its Git-owned record and pinned approved specification, applicable contracts, data impact and UI design. Verify the specification phase merged and required checks passed. Read the project scope and targets, applicable codebase and system or client design, test strategy, scoped instructions and existing delivery evidence. Establish actual owned boundaries and available teams or ownership from evidence; do not infer an extra frontend or backend.

Apply [Decide Readiness and Record Progress](../../../references/work-items-and-evidence.md#decide-readiness-and-record-progress) to feature dependencies and applicable overrides. Use [Local Tracker](../../../references/trackers/local.md#read-verify-and-update) for local verification and applicable shared rules for Git-owned feature evidence in remote modes. A blocked feature requires an explicitly scoped human override before permitted work can proceed. Reuse an approved strategy for additions unless a material change requires amendment.

## Determine and Confirm the Approach

Identify the feature's actual delivery boundaries, required contracts, independent checks, shared prerequisites, integration and exposure constraints from the approved sources. Confirm the delivery approach with the human before creating dependent ticket plans. Ask in plain language about the work and trade-offs, not internal enum values. Reuse known preferences and avoid asking for facts already established.

- For one owned scope, propose delivering within that scope and confirm it suits the human's intent. Do not invent another track.
- For a feature spanning frontend and backend, explain the practical choice between delivering complete cross-layer outcomes and separate independently checked tracks using the agreed contract. Ask how the human wants to organize delivery; discuss parallel ownership, dependencies and integration only as relevant. Other multi-boundary scopes follow the same reasoning.
- Use [Flat slicing and quality criteria](../../work-breakdown-planning/SKILL.md#planning-depth) selectively to compare a material choice. A contract-first split needs a usable pinned contract, independently verifiable boundaries and planned real integration. Do not treat mock-backed checks as real integration or impose an artificial dependency between independent tracks.

Ask only for decisions that remain material, such as ambiguous ownership or an unresolved exposure constraint. Explain a recommendation from project evidence and the human's context; retain already approved choices. If the answer does not establish a feasible approach, clarify before proceeding.

## Record and Approve

Map the confirmed meaning to `delivery-strategy.approach` in `docs/features/<feature-id>/feature.agenix.json`: `single-scope` for one owned scope, `vertical-slices` for complete outcomes across boundaries, or `contract-first` for independently delivered tracks coordinated by a shared contract. Write `summary` with the actual boundaries, owners, delivery approach and independent verification. Add pinned `integration-coverage` references when real-boundary checks apply and `exposure-boundary` when applicable. Reuse shared contract pins in `references`. Do not create tickets or task plans here.

Check the selected approach covers the approved outcome, its integration and safe exposure without contradicting approved contracts. Run the installed [artifact validator](../../../scripts/validate-artifacts.py) with `--project-root <absolute-project-root> --stage feature` and assess the strategy's meaning separately.

Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates), presenting the strategy, confirmed choices, evidence, limitations and intended publication. After approval, [publish the candidate](../../../references/git-publication.md#publish-the-approved-candidate) on the feature plan branch and bind approval and evidence to its revision in the phase PR or durable checkpoint. The tickets step owns the complete-set gate and phase merge. Follow the shared session closure rules.
