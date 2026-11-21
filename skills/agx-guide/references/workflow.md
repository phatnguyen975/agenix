# Agenix Workflow Guide

## How to Use Agenix

Agenix provides human-directed workflows for defining a product, preparing its architecture and implementation environment, and delivering features through review. Each workflow step owns its inputs, outputs and verification. Invoke a specific step with its ID when required; the notation below is the skill input, not necessarily a shell command. The host may display or invoke skills differently.

The typical order is `setup → prd → feature → architect → scaffold → spec → plan → build → review → ship`. Applicability depends on project scope and the feature. For example, a web UI step is omitted when there is no owned web UI; follow the selected step's actual prerequisites rather than assuming every listed step applies.

## Workflow Map

| Workflow                                  | Invocation and Purpose                                                                                                       | Main Result                                                               |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [Setup](../../agx-setup/SKILL.md)         | `agx-setup configure`, then `verify`: prepare and verify project settings; `verify` also supports joining an existing setup. | Shared config, instructions and artifact checks.                          |
| [PRD](../../agx-prd/SKILL.md)             | `agx-prd define`: agree on the product's requirements and measurable outcomes.                                               | Approved product requirements.                                            |
| [Feature](../../agx-feature/SKILL.md)     | `agx-feature define`: define bounded outcomes, priority and feature dependencies.                                            | Feature catalog and records.                                              |
| [Architect](../../agx-architect/SKILL.md) | `agx-architect <step>`: establish the applicable product blueprint.                                                          | Approved shared models, design decisions, conventions and test strategy.  |
| [Scaffold](../../agx-scaffold/SKILL.md)   | `agx-scaffold <step>`: establish the runnable and verifiable foundation.                                                     | Project structure, setup, checks and instructions.                        |
| [Spec](../../agx-spec/SKILL.md)           | `agx-spec <feature-id> <step>`: define the feature's behavior and applicable contracts.                                      | Approved feature specification and applicable API, data and UI artifacts. |
| [Plan](../../agx-plan/SKILL.md)           | `agx-plan <feature-id> <step>`: agree on delivery boundaries and ticket set.                                                 | Approved strategy and ticket mappings.                                    |
| [Build](../../agx-build/SKILL.md)         | `agx-build <ticket-id> <step>`: prepare and execute ticket tasks.                                                            | Approved tasks, implementation and verification evidence.                 |
| [Review](../../agx-review/SKILL.md)       | `agx-review <ticket-id> assess`: assess the candidate and evidence.                                                          | Review report and durable decision.                                       |
| [Ship](../../agx-ship/SKILL.md)           | `agx-ship <ticket-id> run` or `agx-ship <feature-id> run`: verify and publish the appropriate delivery.                      | Verified ticket delivery or feature completion.                           |

Feature IDs use `FEAT-NNN`; ticket IDs use `FEAT-NNN-TNN`. Replace examples with actual allocated IDs. Tasks belong to a ticket. Details and numbering rules are in [Work Items and Evidence](../../../references/work-items-and-evidence.md#identify-and-plan-work).

For a new project, start by invoking `agx-setup configure`. Review its candidate and end that step, then invoke `agx-setup verify` and complete its required publication. Once setup is merged and verified, proceed through `agx-prd define` and `agx-feature define`, followed by the applicable architecture and scaffold steps. After those foundations are merged, `agx-spec FEAT-001 behavior` is an example for an actual allocated feature ID. Confirm each prerequisite and human gate; the example does not imply a particular project already has that ID or has completed prior steps.

## Steps Within the Main Workflows

| Workflow  | Steps and Purpose                                                                                                                                                                                                                                           |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Architect | `domain`: business model; `system`: applicable system design; `stack`: technology selection; `data`: applicable persistence design; `ui`: applicable shared web design; `conventions`: engineering rules; `tests`: test strategy and blueprint consistency. |
| Scaffold  | `structure`: codebase layout; `runtime`: runnable foundation; `services`: applicable services and initial persistence prerequisites; `tests`: verification harnesses; `ci`: CI and optional hook; `instructions`: final project guidance and delivery.      |
| Spec      | `behavior`: requirements and acceptance; `api`: applicable interfaces; `data`: persistence impact; `ui`: feature web UI design and prototype.                                                                                                               |
| Plan      | `strategy`: delivery boundaries; `tickets`: verifiable delivery set and dependencies.                                                                                                                                                                       |
| Build     | `plan`: task definitions and verification; `run`: implement approved tasks.                                                                                                                                                                                 |

Each phase's linked skill entry owns its routing and prerequisites. Do not infer that a step is applicable solely because it appears in this list. The final applicable step verifies and publishes the complete phase output where required.

## Human Decisions and Sessions

For a valid workflow step, the AI emits `BEGIN`; subsequent work in the open step uses `DURING`. The human sends the matching `END` to close it. These markers are session-local and do not grant publication authority. An authorized handoff can carry an open step's state to another session. The human explicitly invokes the next step after closure. See [Session Markers and Handoff](../../../references/workflow-control.md#session-markers-and-handoff).

For example, after `agx-setup configure` completes its authorized actions, the human closes it with `END AGX-SETUP configure`; only then can the human invoke the next step in that session.

For a gated artifact, the AI presents the candidate, evidence and intended writes. Human approval authorizes the stated commit and push; it is not merge or exposure authority. Merge requires a separate decision for the exact PR and head. Exposure, if requested after feature completion, requires separate authority for the exact operation and target. See [Artifact Gates](../../../references/workflow-control.md#artifact-gates) and [Git Publication](../../../references/git-publication.md).

## Ticket and Feature Delivery

The ticket's build plan, implementation, review and fixes share one owned ticket branch. Review findings covered by an unfinished approved task return to build run; new obligations or fixes covered only by closed tasks return to build plan. Review the changed candidate again. Ticket ship creates or updates the implementation PR, checks CI and obtains separate merge authority.

Feature ship is separate: it checks the merged ticket set and required real-boundary acceptance on the integrated baseline, then publishes the feature completion record through its own PR. Mock-backed checks do not prove real integration. A required post-merge ticket failure uses linked repair evidence before the original ticket can close. See [Ticket Delivery](../../agx-ship/references/ticket.md) and [Feature Finalization](../../agx-ship/references/feature.md).

## Tracking and Recovery

Features and their specifications remain in Git in every mode. In local mode, tickets and their embedded tasks are Git records. GitHub mode uses issues and sub-issues; Jira mode uses issues and sub-tasks. The selected tracker owns ticket/task state, while durable checkpoints preserve decisions and evidence. See [Local](../../../references/trackers/local.md), [GitHub](../../../references/trackers/github.md), or [Jira](../../../references/trackers/jira.md) as applicable.

For new work, amendments, cancellation, overrides or an interrupted write, follow [Handle Changes and Exceptions](../../../references/work-items-and-evidence.md#handle-changes-and-exceptions). Reconcile existing records and publication state before retrying. A declared status alone does not establish verified completion. Ask for the item ID and inspect available read-only evidence before suggesting a project-specific next step.
