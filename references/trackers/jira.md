# Jira Cloud Tracker

Use this guide when `tracker: jira`. Map a ticket to one configured standard issue type and a task to a configured sub-task type. The feature stays in Git.

## Verify Project and Access

- Discover the site URL, cloud ID, project key, issue type IDs and required fields. Verify the dependency link type ID and direction, allowed transitions and exact target status IDs per issue type. Confirm sub-tasks can complete while the parent stays open and that an approved cancellation transition is available. Resolve incompatible automation or unsupported fields before publication.
- Initialize `.agenix/credentials/jira.json` from the packaged empty template only if absent. The developer fills `email` and `api-token` privately in each worktree. Only the helper reads the file. It validates the fixed project-relative location and the credential fields before sending requests and never falls back to environment variables, dotenv or other files.
- Use `jira.py` for approved REST v3 operations. Authenticate over certificate-verified HTTPS using HTTP Basic with the Atlassian account email and its scoped Jira Cloud API token. Append each endpoint path to the gateway base `https://api.atlassian.com/ex/jira/<cloudId>`. For example, read an issue at `https://api.atlassian.com/ex/jira/<cloudId>/rest/api/3/issue/<issueKey>`. Use the configured Jira site URL for browser links only. Use bounded timeouts and sanitized results. Supply the project and operation inputs through the calling step without exposing credential values.

## Create and Read Issues

1. Resolve the approved Agenix ID, project, issue type, native parent and dependencies. Check existing records and obtain approved values for any required custom fields. For sub-tasks, keep the approved plan snapshot and resulting mappings in parent comments.
2. Create issues or sub-tasks with the verified project and type. Set a sub-task's parent using `fields.parent.key`. Convert the approved description and comments to Atlassian Document Format using supported paragraphs, lists and links. Preserve canonical IDs and acceptance references in the converted content.
3. Record the returned key and read back the type, parent, labels, links and current status. Traverse every page for collections. Reconcile a partial or unknown create by exact ID and parent before attempting another write. If search can still be stale and direct reads cannot resolve the outcome, leave the create unresolved.

## Helper Operations

Run the installed entry point with the absolute Git worktree root and the declared private credential path.

```bash
python "<plugin-root>/scripts/jira.py" --project-root "<project-root>" --credentials-file ".agenix/credentials/jira.json" <operation> <arguments>
```

| Operation                                      | Arguments and Result                                                                                                                                                                                                                                                                                                   |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `discover`, `link-types`                       | Read project issue types and link types. For `discover --issue-type <id>`, read the create fields for that type.                                                                                                                                                                                                       |
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
