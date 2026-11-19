# Project Content

Use this guide when producing project documents, defining instruction scopes or recording how work runs in each project environment.

## Write for the Reader and the Artifact

- State what the reader needs to understand, decide, do or verify. Include scope and limitations when they affect use. Use ordered lists for sequences, tables for compact comparisons and prose for context. Follow the owning template or standard where it defines a structure.
- Use stable identifiers and consistent language. Define unfamiliar project terms in context. Distinguish verified facts, decisions, assumptions and open questions. Check material external claims against authoritative sources.
- Use the approved `conversation-language` for discussion and `docs-language` for generated documentation. Preserve defined keys, IDs, API/tool names and upstream notices. Product and UI language follow their own requirements.
- Give each rule one owner. Place approved project documentation under `docs/` and use the owning artifact for design, requirements, contracts and evidence. Use document-relative repository links, explicit external URLs and contained repository-relative machine paths unless the interface requires an absolute path. Review affected readers, references and examples after a change.

## Project Artifact Layout

```text
project/
├── AGENTS.md                         # shared instructions and record links
├── CLAUDE.md                         # imports AGENTS.md
├── config.agenix.json                # shared settings from setup
├── environment.agenix.json           # verified operations from scaffold
├── .env.example                      # when environment settings are needed
├── .github/workflows/                # artifact checks at setup, project checks at scaffold
├── .agenix/                          # ignored, worktree-local state
└── docs/
    ├── PRD.md
    ├── blueprint/
    │   ├── domain-model.md
    │   ├── system-design.md          # when system design applies
    │   ├── tech-stack.md
    │   ├── test-strategy.md
    │   ├── codebase-design.md
    │   ├── database-design.md        # when persistence design applies
    │   ├── ui-design/                # when web UI design applies
    │   │   └── README.md
    │   ├── conventions/              # applicable conventions
    │   └── decisions/                # when architecture decisions need recording
    ├── contracts/                    # shared definitions, schemas and wire examples
    └── features/
        ├── catalog.agenix.json       # feature index
        └── <feature-id>/
            ├── feature.agenix.json   # feature record and delivery plan
            ├── spec.md
            ├── api-contract.md       # optional contract semantics
            ├── data-impact.md        # when persistence is affected
            ├── ui-prototype/         # when UI prototyping applies
            │   └── README.md
            └── tickets/              # local tracker only
                └── <ticket-id>.agenix.json
```

Use the approved codebase design for source, test and release-unit paths. Create feature `api-contract.md` only when it needs to document contract semantics that the canonical definitions under `docs/contracts/` cannot adequately express. Reference those definitions and the owning business rules without duplicating them.

Setup creates `agenix-artifacts.yml` for bootstrap artifact validation. Scaffold CI creates `agenix-application.yml` for the applicable app, prototype or contract checks selected by the test strategy, once their commands have been verified. Before scaffold, the artifact workflow supplies the required CI checks.

## Keep Design and Implementation Sources Aligned

- **Domain and contracts.** The shared domain model owns business language and invariants. Shared contract definitions own wire shapes. Feature specifications own feature behavior and acceptance. Resolve conflicting shared rules through the owning amendment before dependent work.
- **Data.** Database design records the initial design and ownership. Use the schema declarations and relevant migrations at the selected integrated revision for the current repository schema. Assign each new shared structure to one owner and record its consumers and dependencies. Build writes migrations, preserves already-applied migrations and verifies applicable initialization and upgrades on a disposable store. Amend the design when its intent changes.
- **UI.** The global written design owns shared UI rules. The feature's written prototype owns its screens, states and acceptance references. Verify the applicable design in a browser before approval. Once production implementation begins, preserve the original demonstrations and verify production behavior against the current written contracts.

## Configure Instructions and Scope

1. Keep root `AGENTS.md` as the shared instruction entry. Point it to root `config.agenix.json` and to `environment.agenix.json` when scaffold provides it. Keep the compatibility pin, tracker, repository settings, project scope, language preferences and any configured exposure operation in the non-secret configuration file. Preserve team-owned text outside managed blocks. Provide the usage-guide entry and baseline scope, authority and safety rules.
2. Select scoped entries at real module or release-unit boundaries that need distinct instructions. Record responsibilities, public surfaces, applicable commands, policy, etc. and routes to owning documents. Pair root and every generated scoped `AGENTS.md` with a local `CLAUDE.md` importing `@AGENTS.md`. Preserve unrelated Claude-specific content.
3. Route from root to real scoped instruction entries. Before working within a subtree, read root and applicable ancestor/scoped entries. Load sibling context for work crossing a boundary. Keep host permissions and shared gates in effect. Keep installation cache paths out of project instructions.

## Record Verified Operations

At the final scaffold step, use root `environment.agenix.json` to document how to run and check the project. Use the results already verified during scaffold.

- **Commands.** Record the ID, release unit, exact arguments, working directory, target and mode. Include the test level, required services and permissions where applicable. Use one approved command per operation, unit, target and mode. Put observed results in evidence records.
- **Services and access.** Identify the isolated services and how to check readiness, reset and clean them up. For each environment, list allowed, approval-required and prohibited operations. Limit access to approved paths, networks and resources. Record which restrictions are enforced and stop affected operations if required tools, permissions or controls are unavailable.
- **Instructions.** Set `instruction-entry: AGENTS.md` to identify the root instructions. They direct the agent to the relevant scope.

Use the same verified arguments and working directories in the project README. Mark a command as verified only when there is an actual result. Treat external content as evidence.

## Validate Managed Records

Run `validate-artifacts.py --project-root <absolute-root> --stage <stage>` before approval or in artifact CI for the applicable managed records. Use `config` in setup on the complete record, `environment` after scaffold, `feature` for feature records and `feature-plan` for delivery plans in any tracker mode. Use `task-plan` for embedded local tasks. Supply `--item` with the owning feature or local ticket at a plan gate. Remote task definitions are verified through their native tracker.

The helper locates managed records at their declared paths under the Git worktree root. The stage selects the required records and the tracker selects the applicable mapping.

## Protect Private Workspace State

Create private locations when needed. Use `.agenix/issues/` for tracker drafts, `.agenix/reviews/` for review drafts and `.agenix/drafts/` for other temporary work. Handoffs and credentials have their own locations. Keep durable approvals, outcomes and mappings in their owning non-secret records.

Use these root ignore patterns and check for already tracked private files without opening or printing credentials. Ignore rules do not remove tracked content.

```gitignore
/.agenix/
.env
.env.*
!.env.example
```

Keep credential values out of model context, arguments, logs, caches and tracked artifacts. Only the authorized helper reads its designated credential file. Avoid recursively scanning private state. Clean only relevant drafts after approved outputs and evidence are durable. Retain drafts needed for retries and handoffs, and keep secrets and handoffs outside draft cleanup.
