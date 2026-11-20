# Build the Runtime Foundation

## Inputs and Output

Verify the approved architecture phase is merged and the approved `docs/blueprint/codebase-design.md` and its approval evidence are available on the scaffold branch. Read project instructions and `config.agenix.json`, the approved tech stack and applicable conventions for release units, targets, tools, settings and constraints. Consult system design and test strategy only for relevant startup boundaries and smoke-check requirements. Inspect existing files, tool versions and commands before changing them.

Produce the smallest source, toolchain and configuration foundation needed to build and start or load each owned release unit. Preserve existing work. Create only directories and files needed by this step. Planned module and test directories are created when their owning work needs them.

## Implement the Foundation

1. For each release unit, configure the approved language, runtime, package and build tools, dependency manifests and lockfiles as applicable. Verify installed versions and compatibility with approved targets. Identify missing tools or access and pause affected work. Install dependencies only within authorized project and host permissions.
2. Add the minimal entry point or public surface appropriate to the unit. A service may expose a minimal startup or health path, a CLI can provide a basic invocation, and a library can load or export its intended entry. Avoid fabricated business behavior. Reuse real existing code when it fulfills the purpose.
3. Configure applicable formatting, lint, type checking and build tools using approved conventions. Select paths and discovery patterns that include subsequent source additions without creating empty module trees. Do not disable substantive checks merely to pass the initial skeleton.
4. Define application settings required to run the foundation. Provide safe examples such as `.env.example` where applicable, explain required values and defaults, and update ignore rules for private configuration and generated outputs. Keep credentials out of tracked files, command arguments and evidence. Avoid connecting to real production services.
5. If containerization is approved for a release unit, add its container build and standalone run configuration. Specify the application entry point, required settings and image version or pin according to the approved stack. Build and start the resulting container where the environment permits, and verify its service-independent behavior.

Use [Incremental Implementation](../../incremental-implementation/SKILL.md) only when the foundation has dependent changes that benefit from independently verified increments. Use [TDD](../../tdd/SKILL.md) for behavior-bearing helpers under an approved test-first method. Apply only the needed cycle and verification guidance; use the scaffold candidate and evidence rather than a separate tracking artifact.

## Verify and Publish

Run applicable install, format, lint, typecheck, build and service-independent startup or load commands for each unit. Use a meaningful smoke check against the actual entry point to demonstrate it works. A missing service-dependent check remains pending for its owning step. Record the exact command and arguments, working directory, unit, target, relevant environment and actual result. Check expected failures separately from harness failures. Verify applicable configuration and ignore behavior without exposing secrets.

Inspect the complete scoped diff, including manifests, lockfiles and generated files. Confirm approved architecture, target compatibility and that examples contain no credentials. Record actual tool versions and results in durable non-secret step evidence linked to the candidate revision, such as a checkpoint or phase PR. Carry the command details forward for later scaffold steps and final environment documentation.

Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates). Present the candidate, base, checks, remaining service-dependent work and intended commit and push. After approval, [publish the candidate](../../../references/git-publication.md#publish-the-approved-candidate) on the scaffold branch and bind the verification evidence to its published revision. Follow the shared phase and session rules.
