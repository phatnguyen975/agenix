# Configure Project Setup

## Inputs and Result

Use the owned Git worktree, a verified GitHub default branch with a commit, access to the installed plugin and any confirmed project settings. Prepare the setup candidate locally and hand it to `verify`.

## 1. Confirm Project Settings

1. Check for an existing setup candidate. Route a developer joining merged setup to `verify`. Use the amendment route for approved settings that need to change.
2. Resolve the installed validator and [Config Schema](../assets/config.schema.json). Verify the compatible helper distribution from its HTTPS source and full immutable commit. Confirm the pin supplies the matching helper and schema assets and is retrievable under the intended CI runner access model.
3. Reuse explicit decisions and group unresolved choices in one request. Use the current conversation language until the project preference is confirmed.

| Source                                | Values                                                                                                                                                                                                                                                  |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Git, GitHub and installation evidence | Derive `github-repo`, `default-branch`, `plugin.repository` and `plugin.revision`. Ask if identity, provenance or access is unclear.                                                                                                                    |
| Human decisions                       | Confirm `tracker`, `project-scope` and `targets`. Confirm `conversation-language` and `docs-language` independently. Propose the current conversation language and English for documentation if useful. Record proposed values only after confirmation. |
| Plugin conventions                    | Set `kind` to `config` and `schema-version` to `1`. Use the packaged paths and formats. Include `exposure` only when an approved binding already exists.                                                                                                |
| Jira identity                         | Confirm the site URL, Cloud ID and project key from supplied or verified evidence. Ask only for values that cannot be established.                                                                                                                      |

## 2. Prepare the Local Candidate

### All Tracker Modes

1. Establish or resume the owned setup worktree. Apply [Protect Private Workspace State](../../../references/project-content.md#protect-private-workspace-state). Preserve existing ignore rules and verify that private paths are excluded and `.env.example` remains eligible. Check tracked paths without opening private files. Report an already tracked private path as a blocker.
2. Write root `config.agenix.json` with the confirmed values. For `local` and `github`, prepare the full record. For `jira`, include the verified identity and any already verified mappings. Omit unresolved API-dependent fields and list them as pending in the step summary.
3. Apply [Configure Instructions and Scope](../../../references/project-content.md#configure-instructions-and-scope). Render the managed [Root Instructions](../../../templates/instructions/root-agents.md) and [Claude Adapter](../../../templates/instructions/claude-adapter.md) (if applicable, ask human before rendering). Preserve team text, resolve conflicting markers and link only artifacts that exist. Render documentation in the approved documentation language.
4. Render the [Artifact CI Template](../assets/agenix-artifacts.yml) as `.github/workflows/agenix-artifacts.yml`. Replace the three quoted placeholder scalars as a whole. Encode the approved plugin source and pin as JSON-quoted strings, which are valid YAML scalars. For `<default-branch-pattern>`, first escape GitHub Actions branch glob metacharacters with backslashes, then JSON-quote the resulting pattern. Check that the values match the config and that no placeholder remains.

### Jira Only

Apply [Verify Project and Access](../../../references/trackers/jira.md#verify-project-and-access). Confirm that `.agenix/credentials/jira.json` is contained, ignored and untracked. Create the [empty template](../assets/jira-credentials.json) exclusively if the file is absent. Preserve any existing file without reading it. Give the developer the path for private entry of the email and scoped API token. Jira API reads belong to `verify`.

## 3. Report and Close

Review the local edits for scope, reference paths, effective ignores and unresolved placeholders. Keep configuration validation, commit, push and PR publication for `verify`.

Report the worktree and branch, the prepared files, known settings and any blockers. For Jira, include the credential path and the pending mapping fields. Tell the human to close the step, fill any missing private credentials and invoke `agx-setup verify` in the same worktree.
