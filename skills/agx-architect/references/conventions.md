# Define Engineering Conventions

## Inputs and Output

Read the approved project scope and language from `config.agenix.json`, the approved `tech-stack.md`, and the applicable approved domain, system, data and UI foundations. Verify their approval and revisions on the architecture branch. Read relevant existing conventions and tool configuration when present. Use the merged PRD or feature records only to resolve a specific policy requirement or conflict.

Create applicable `docs/blueprint/conventions/*.convention.md` files using the [Convention Template](../assets/convention-template.md). These files own cross-cutting engineering rules and intended checks. Reference the foundations for decisions they already own.

## Choose Rule Sets

Start with rules shared across the owned product. Group additional rules by concern and audience when they have meaningfully different scope or enforcement, such as frontend, backend, interface, data, security, testing or operations. A release-unit-specific file is appropriate when its rules differ materially. Describe language or framework-specific rules within the applicable concern. Merge small, related concerns when scope remains clear. Use descriptive lowercase kebab-case filenames and one owner for each rule. Avoid creating empty files.

Identify only applicable decisions. Consider naming and formatting, code clarity and error handling, public boundaries and compatibility, dependency direction, configuration and secrets, data ownership, accessibility, observability, testing and operational behavior. Specify indentation or formatting where useful by adopting the selected tool or established project style. Do not turn conventions into tutorials, feature requirements, design inventories or copies of tool documentation.

## Develop and Confirm Rules

1. Extract approved constraints, existing project decisions, stack-specific practices and relevant risks. Identify where the foundations already own the decision and link to them. Resolve contradictions with the owning baseline before dependent changes.
2. For open material choices, present a concise recommendation and relevant trade-offs to the human. Reuse approved decisions. Batch independent choices for review. For routine choices, prefer the selected language and framework's established conventions and explain any project-specific deviation.
3. Write actionable rules with a clear scope and exceptions where needed. Describe intended enforcement through review, static checks or other suitable verification. Identify ownership when enforcement or responsibility crosses boundaries. Do not claim a command, tool configuration or check exists until verified. Scaffold binds actual paths, tools and commands, and test strategy selects test coverage.
4. Use [Structural Conventions](../../codebase-design/references/conventions.md) for module and dependency rules when needed. Use [API Contract Design](../../api-contract-design/SKILL.md) selectively for applicable shared interface and compatibility rules. Consult [Security Review](../../security-review/SKILL.md) or [Accessibility](../../accessibility/SKILL.md) for a specific relevant concern. Carry only criteria supported by approved requirements and targets.
5. For a new or materially changed architectural decision, apply the [ADR Guide](../../evolutionary-architecture-design/references/adr-guide.md#decide-what-deserves-a-record) and [ADR Template](../../evolutionary-architecture-design/assets/adr-template.md). Link the record from the affected convention and preserve existing decision history.

## Verify and Approve

Check that the set covers applicable shared concerns, every rule has an unambiguous scope, and overlapping files do not conflict. Check alignment with the approved stack and foundations, intended enforcement, exception handling and source links. Read back each file and inspect the complete diff. Remove template instructions and unsupported claims.

Prepare the root documentation map update for the candidate using [Configure Instructions and Scope](../../../references/project-content.md#configure-instructions-and-scope). Include it in the same approval and publication.

Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates) to the related convention files and applicable ADRs together when their prerequisites are approved. Present the proposed rules, material choices, intended checks, evidence and publication actions. [Publish the Approved Candidate](../../../references/git-publication.md#publish-the-approved-candidate) on the architecture branch using the shared publication rules. Record approval and verification evidence against the published revision.
