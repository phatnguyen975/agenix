# Finalize Project Instructions and Environment

## Inputs and Outputs

Verify the approved architecture and scaffold branch, candidate revisions, CI results, commands and service evidence. Read project instructions, `config.agenix.json`, approved codebase design, test strategy, applicable conventions and the scoped instruction inventory. Reconcile prior scaffold approvals, operations, tool versions, targets, permissions and unresolved results. Recheck any evidence affected by subsequent changes.

Produce root `environment.agenix.json` using the [Environment Schema](../assets/environment.schema.json), update root and applicable scoped instructions using the shared [Root Instructions](../../../templates/instructions/root-agents.md) and [Scoped Instructions](../../../templates/instructions/scoped-agents.md), and prepare the project root README. Preserve team-owned content and existing valid decisions.

## 1. Record Verified Operations and Permissions

Apply [Record Verified Operations](../../../references/project-content.md#record-verified-operations). Populate release units, commands, services, permissions and evidence from actual scaffold results. Record exact argument vectors, working directories, targets, modes and check levels. Resolve IDs and references. Separate project configuration values from credentials. Record permissions by environment and boundary, with `verified` only when supported by actual evidence. General tool usage and scope guardrails belong in instructions and remain subject to host permissions.

Run [Artifact Validator](../../../scripts/validate-artifacts.py) with `--project-root <absolute-project-root> --stage environment`. Resolve errors without weakening schema or assertions. Validate each check and service reference against the recorded commands.

## 2. Finalize Instruction Routing

Apply [Configure Instructions and Scope](../../../references/project-content.md#configure-instructions-and-scope). Render the root managed region with the approved scope, documentation map and verified environment link. Preserve unrelated content. Use the approved scope inventory to create or update scoped `AGENTS.md` files at actual module or release-unit boundaries. Link each to its parent, applicable approved designs, conventions and operations. Link actual children and route from the root index. Pair each generated instruction entry with the [Claude Adapter](../../../templates/instructions/claude-adapter.md). Verify paths, links and operation IDs against the candidate.

Review baseline guardrails for scope, untrusted content, credentials, least privilege, verification and destructive operations. Add only project-specific, approved environment controls and distinguish technically verified enforcement from instruction-only rules. Keep host permissions authoritative.

## 3. Prepare the Project README

Ask the human about the intended audience, presentation style and desired content. Propose a concise structure grounded in project context and reuse prior decisions. Use [Grilling](../../grilling/SKILL.md) for multiple interdependent open choices, without creating a separate interview artifact. Confirm material choices before drafting.

Write or update the root README for its intended readers. Describe the project and owned scope, prerequisites, setup, run and verification steps, relevant services, and links to the applicable documentation and contribution information. Use the same verified arguments and working directories as the environment record. Mark unavailable capabilities accurately and preserve unrelated content.

## 4. Verify, Approve and Deliver

Verify a clean checkout using the approved install, startup, build and test operations for all applicable units and targets. Verify required service readiness, isolation and cleanup. Reuse only evidence still valid for the final candidate. Check README commands, environment IDs, scoped instructions, adapters, links, effective ignores and permissions against the actual project. Record actual results and blockers without exposing secrets.

As the final scaffold step, inspect the complete scaffold candidate and its prerequisites. Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates) to the environment record, instructions, README and any other changed outputs. Present the candidate, verified operations, effective controls, CI evidence, limitations and intended publication. [Publish the Approved Candidate](../../../references/git-publication.md#publish-the-approved-candidate), ready the existing scaffold PR and [Bind Review and CI](../../../references/git-publication.md#bind-review-and-ci-to-the-candidate) to its final head.

Follow [Merge the Approved Head](../../../references/git-publication.md#merge-the-approved-head) and [Verify Delivery](../../../references/git-publication.md#verify-delivery-and-recover-from-a-failed-check). Wait for human merge or separate authority to merge the exact head. Report completion only after the merge and required post-merge checks. Follow the shared session closure rule.
