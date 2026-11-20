# Prepare Development and Test Services

## Applicability and Inputs

Use this step when the approved stack and test strategy require service integration or owned persistence initialization. If neither applies, report the reason and leave the worktree unchanged.

Verify the architecture phase is merged and the approved structure and runtime candidates, revisions and evidence are available on the scaffold branch. Read the project instructions, `config.agenix.json`, approved codebase design, tech stack and test strategy. Read applicable system and database designs and ADRs for service ownership, selected versions, topology, migration toolchain and shared persistence prerequisites. Inspect the runtime configuration and existing service definitions before editing. Resolve material gaps or conflicts through the owning decision before dependent changes.

## Configure Services

1. Identify only dependencies needed by approved local development or test workflows. Respect the selected engine, version, provider and environment. Where local containers are selected, configure project-owned Compose or an equivalent orchestration file to connect the application and its dependencies. Reuse the runtime image, entry point and settings. For a managed dependency, use only an approved isolated environment and its documented access mechanism.
2. Place service-specific configuration in appropriate project-owned locations from the approved codebase design and toolchain conventions. Configure the minimum required settings, startup ordering and readiness checks. Pin or constrain images and verify their compatibility with the selected stack. Avoid copying vendor defaults without purpose. Create only paths and files needed now.
3. Define safe non-secret example settings and isolated identities for development and tests. Keep credentials out of tracked files, logs and command arguments. Protect persistent and shared resources from disposable test reset or cleanup. Specify readiness, seed, reset and cleanup operations where applicable. Keep test fixtures separate from required reference data.
4. Integrate service-dependent application startup using the existing runtime settings. Preserve the service-independent checks and avoid duplicating application build or runtime configuration.

## Establish Persistence Prerequisites

For each owned store requiring a migration harness, use the approved migration toolchain, its naming and ordering rules, and its project-native configuration and paths. Derive the initial schema from the approved database design. Implement only structures required to start the runtime, prove the harness or provide approved shared prerequisites for parallel work. Do not pre-create feature-specific structures or empty migrations. Include required reference data separately from disposable test fixtures.

Apply initial migrations to an empty disposable store and verify the resulting structures and a repeat invocation according to the toolchain's semantics. When a supported previous state exists, verify the applicable upgrade using representative disposable data. Provide and verify a down migration only when required and safe; otherwise document recovery and irreversible effects. Preserve migrations already applied to shared environments and use a new forward migration for corrections.

Use [Incremental Implementation](../../incremental-implementation/SKILL.md) when dependent setup changes benefit from verified increments. Use [TDD](../../tdd/SKILL.md) for behavior-bearing helpers under an approved test-first method. Keep results in the scaffold evidence.

## Verify and Publish

Verify configuration, service startup, readiness, isolation, seed/reset/cleanup where applicable, and the application path that depends on the services. Exercise the actual migration commands and failure cases that can be safely reproduced in disposable resources. Report inaccessible tools or services and stop affected work rather than claiming success. Ensure cleanup targets only resources created or explicitly authorized for the check.

Record each verified command and arguments, working directory, unit or service, target, environment, permissions and actual result in durable non-secret evidence bound to the candidate. Record service identity, isolation and migration paths or revisions. Carry this evidence forward for the final environment record.

Review the scoped diff and settings, including example values and ignore rules. Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates), presenting the candidate, checks, limitations and intended publication. [Publish the Approved Candidate](../../../references/git-publication.md#publish-the-approved-candidate) on the scaffold branch and bind the evidence to its published revision. Follow the shared phase and session rules.
