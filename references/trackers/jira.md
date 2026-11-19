# Jira Cloud Tracker

Use this guide when `tracker: jira`. Map a ticket to one configured standard issue type and a task to a configured sub-task type. The feature stays in Git.

## Verify Project and Access

- During configure, verify and record three values in the working configuration. The site URL identifies the Jira site in the browser, the Cloud ID identifies that site at the API gateway, and the project key limits operations to the intended project. An issue key identifies one ticket or subtask within the project.
- Initialize `.agenix/credentials/jira.json` from the packaged empty template only if absent. The developer fills `email` and `api-token` privately in each worktree. Only the helper reads the file. It validates the fixed project-relative location and the credential fields before sending requests and never falls back to environment variables, dotenv or other files.
- Use `jira.py` for approved REST v3 operations. Authenticate over certificate-verified HTTPS using HTTP Basic with the Atlassian account email and its scoped Jira Cloud API token. Append each endpoint path to the gateway base `https://api.atlassian.com/ex/jira/<cloudId>`. For example, read an issue at `https://api.atlassian.com/ex/jira/<cloudId>/rest/api/3/issue/<issueKey>`. Use the configured Jira site URL for browser links only. Use bounded timeouts and sanitized results. Supply the project and operation inputs through the calling step without exposing credential values.

## Setup Mapping Defaults

Configure records known values and reports unresolved mappings as pending. Verify uses the defaults below to select entries from the project's Jira metadata and records their actual IDs.

| Config Field         | Default Selection                                                                                                                                                            |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `issue-types.ticket` | Standard `Story`, then standard `Task` if `Story` is unavailable.                                                                                                            |
| `issue-types.task`   | Native `Subtask` or `Sub-task`. Verify the type can be used under the selected ticket type.                                                                                  |
| `dependency-link`    | The `Blocks` type with `inward` when the dependent sees `is blocked by`.                                                                                                     |
| `status-targets`     | For each issue type, use `To Do`, `In Progress`, `Done`, and an explicit `Cancelled` target. The two issue types may use different IDs.                                      |
| `field-defaults`     | Approved shared values for required create fields that Jira does not fill. Key by `ticket` or `task`, then by Jira field ID or key. Keep issue-specific values in the draft. |

1. Use `discover`, `link-types` and `project-statuses` for the project. Read create metadata for the selected ticket and subtask types. Check that subtasks are enabled and that token scopes and Jira permissions allow browsing and creating issues.
2. Verify that required transitions are available and that a subtask can complete while its parent remains open. Use authorized existing issues or administrator evidence. A status ID identifies a destination. A transition ID identifies an available action on an issue.
3. Ask the human only when a compatible mapping is unclear or a required field needs a decision. Resolve a missing cancellation target before publication.

## Create and Read Issues

1. Resolve the approved Agenix ID, project, issue type, native parent and dependencies. Check existing records and obtain approved values for any required custom fields. For sub-tasks, keep the approved plan snapshot and resulting mappings in parent comments.
2. Supply the approved summary, ADF description, labels and any issue-specific fields in the draft. For a subtask, supply the Jira issue key of its existing parent. The helper resolves project and type from config and sets `fields.parent.key`. Draft fields take precedence over shared field defaults. Keep project, issue type, parent, summary, description and labels in their dedicated inputs.
3. Record the returned key and read back the type, parent, labels, links and current status. Traverse every page for collections. Reconcile a partial or unknown create by exact ID and parent before attempting another write. If search can still be stale and direct reads cannot resolve the outcome, leave the create unresolved.

## Helper Operations

Run the installed entry point with the absolute Git worktree root and private credential path. It reads project identity from `config.agenix.json`.

```bash
python "<plugin-root>/scripts/jira.py" --project-root "<project-root>" --credentials-file ".agenix/credentials/jira.json" <operation> [operation-arguments]
```

| Operation                                      | Arguments and Result                                                                                                                                                                                                                                                                                                   |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `discover`, `link-types`                       | Read project issue types and link types. For `discover --issue-type <id>`, read the create fields for that type.                                                                                                                                                                                                       |
| `project-statuses`                             | Read status names and IDs grouped by issue type for the selected project.                                                                                                                                                                                                                                              |
| `issue`, `children`, `comments`, `transitions` | Pass `--key <issue-key>` to read the issue or its related records.                                                                                                                                                                                                                                                     |
| `create`, `reconcile`                          | Pass `--input <draft-path>` containing `role`, `item`, `summary`, ADF `description` and `labels`. Include `parent` for a task and optional approved native `fields`. Only use `create` for a new approved write. After an uncertain outcome, use `issue` with the returned key or `reconcile` with the original draft. |
| `comment`                                      | Pass `--key <issue-key> --input <draft-path>` containing the ADF checkpoint. After an uncertain write, inspect existing comments first.                                                                                                                                                                                |
| `dependency`                                   | Pass `--key <dependent-key> --prerequisite <prerequisite-key>`. The helper checks for the existing link before writing.                                                                                                                                                                                                |
| `status`                                       | Pass `--key <issue-key> --status <agenix-status>`. Use lowercase status values. Supply `--input <draft-path>` for required native transition fields, and `--transition-id <id>` when selecting an exact transition.                                                                                                    |

Draft paths are project-relative JSON inputs. The calling step owns ADF rendering, the approved definition and write authority. The helper saves a private create receipt under `.agenix/issues/` before sending a new issue. It retains the known native key for direct read-back. An unresolved receipt blocks another create on a search miss. Preserve it and the draft until mappings and evidence are durable.

## Confirm Native State

| Agenix State               | Configured Target for the Issue Type                                                    |
| -------------------------- | --------------------------------------------------------------------------------------- |
| `READY`, `BLOCKED`         | To Do target.                                                                           |
| `IN-PROGRESS`, `IN-REVIEW` | In Progress target.                                                                     |
| `DONE`                     | Successful completion target in the Done category with `status:done`.                   |
| `CANCELLED`                | Explicit cancellation target with `status:cancelled` and approved disposition evidence. |

Treat the names in the table as roles. Use the discovered status IDs. If the issue already has the target status, skip the transition. Otherwise find an available transition to that exact status and supply any required transition fields. Ask the human if no eligible transition exists or several eligible transitions remain ambiguous.

Read back the lifecycle label and exact native target after updates. If either write failed or is uncertain, report the transition as incomplete and reconcile the existing issue. Close tasks when verified under their approved checks. Close the ticket as complete after verified delivery.
