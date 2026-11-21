# Commit Convention

A project's own commit convention (lint config, contributing docs, consistent `git log` pattern) takes precedence over the defaults below. The [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/#specification) defines the message structure; the length and style guidelines here are defaults, not requirements of that specification.

## 1. Format

```
<type>[(scope)][!]: <description>

[body]

[footer(s)]
```

## 2. Types

| Type                                          | Use When                                  | SemVer |
| --------------------------------------------- | ----------------------------------------- | ------ |
| `feat`                                        | A feature is added                        | MINOR  |
| `fix`                                         | A bug is fixed                            | PATCH  |
| `refactor`                                    | Code structure changes, behavior does not | —      |
| `perf`                                        | Performance improves                      | —      |
| `docs`                                        | Documentation only                        | —      |
| `test`                                        | Tests added or changed                    | —      |
| `build`                                       | Build system or dependencies              | —      |
| `ci`                                          | CI configuration                          | —      |
| `style`                                       | Formatting only, no logic change          | —      |
| `chore`                                       | Remaining maintenance                     | —      |
| `revert`                                      | A previous commit is reverted             | —      |
| any type + `!` or a `BREAKING CHANGE:` footer | Backward-incompatible change              | MAJOR  |

These are Conventional Commit defaults, not universal versioning rules. The SemVer column describes stable `1.0.0+` releases; inspect actual consumer impact and project policy, especially for `0.y.z` and pre-releases. Other types have no implicit bump under Conventional Commits. If the project defines a different set of types, use the project's set.

## 3. Format Rules

| Part            | Rule                                                                                                                                                                                                            |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Type            | Lowercase                                                                                                                                                                                                       |
| Scope           | Optional lowercase noun (kebab-case) naming the affected area; reuse scopes already present in `git log`; omit when unsure                                                                                      |
| Description     | Imperative mood ("add", not "added"/"adds"); lowercase first letter; no trailing period                                                                                                                         |
| Header length   | Target ≤ 50 characters; hard limit 72, including `type(scope):`                                                                                                                                                 |
| Body            | Separated from the header by one blank line; wrapped at 72 columns; explains **what** and **why**, with implementation details only when needed to assess the change                                            |
| Footer          | Separated from the body by one blank line; trailer-like format (`Token: value` or `Token #value`); tokens use `-` instead of spaces, except the standard special tokens `BREAKING CHANGE` and `BREAKING-CHANGE` |
| Breaking change | `!` before the colon and/or a `BREAKING CHANGE: <description>` footer (uppercase)                                                                                                                               |
| Issue reference | `Refs: #123`; use the platform's closing keyword only when the commit fully resolves the issue                                                                                                                  |
| Language        | English unless the project uses another language                                                                                                                                                                |

**Release-commit exception:** The release commit and its corresponding PR title `chore(release): <version>`, as defined in [release naming](release.md#5-tag-and-naming), are an intentional exception to the imperative-mood and lowercase-first-character guidelines above. In this format, `<version>` is a version literal rather than a prose description. Use this exception only for release-metadata commits and their corresponding PR titles; all other headers must follow the normal description rules.

## 4. Examples

**Good:**

```
fix(session): reject expired tokens on refresh
```

```
feat(search): add prefix matching to the query parser

Allow queries such as "auth*" so users can find related terms without
typing them in full.

Refs: #214
```

```
refactor!: drop support for the legacy configuration format

BREAKING CHANGE: configuration files in the v1 format are no longer read.
Convert them before upgrading.
```

**Bad:**

| Message                                    | Problem                                                  |
| ------------------------------------------ | -------------------------------------------------------- |
| `fix` / `update` / `wip` / `misc`          | No type/description pairing; says nothing                |
| `feat: Added new feature.`                 | Past tense, capitalized, trailing period, no information |
| `Fix: login bug`                           | Type not lowercase; description vague                    |
| `feat: add search, fix login, update docs` | Three changes in one commit                              |

## 5. Revert Format

```
revert: <header of the reverted commit>

Refs: <sha>[, <sha>]
```

## 6. Atomic Commit Rules

- One logical change per commit. Separate unrelated intents; a shared logical change can include implementation, tests and necessary documentation.
- Keep unrelated refactoring, formatting, features, fixes and dependency updates separate. Do not split a tightly coupled change merely because it touches several file types.
- A bug fix and its regression test belong in the same commit.
- Keep each commit independently buildable and testable where practical. Run the applicable project verification before committing; if a required check cannot run, report that limitation rather than claiming it passed.
- Size: target about 100 changed lines; around 300 is usually reviewable. Above 300, assess whether the change can be split; above 1000, normally split unless the changes are tightly coupled or project policy differs.
- Commit messages are written for developers. Changelog entries are written for consumers (see `release.md`).

## 7. Staging and Pre-Commit Checks

1. Confirm commit authority/cadence, then inspect `git status`, `git diff` and `git diff --staged`. Identify existing staged work before changing the index.
2. Stage **explicit paths**. Do not use `git add .`, `git add -A`, or `git commit -a` unless every changed file has been matched to the intended change.
3. Read `git diff --staged` and confirm the intended commit includes exactly the authorized change. Explicit add paths do not exclude unrelated entries already staged. If every change in selected paths is in scope, `git commit --only -m "<header>" -m "<body>" -- <paths>` can commit their working contents while preserving other staged entries; inspect the selected working diff, not just the index. For mixed hunks in the same file, use a reviewed selective patch/index operation that preserves excluded content, or resolve the specific ownership gap before committing. See Git's [commit options](https://git-scm.com/docs/git-commit#_options) for path-only semantics.
4. Confirm the diff contains no secrets, credentials, private environment values, build output, or unintended large files. Placeholder-only templates such as `.env.example` may be committed when the project expects them and the diff contains no secrets.
5. Run the project's verify commands (test, lint, typecheck, build) appropriate to the change. Verification must represent the proposed commit: unstaged or excluded changes can hide a missing dependency or fix. For a partial commit, inspect that distinction and use an isolated candidate checkout when necessary rather than treating tests on the combined dirty tree as proof. If no verify command can be found, do not invent one: state that verification was not possible.
6. Verify the effective identity as described in [Identity and Attribution](#9-identity-and-attribution), then commit with hooks enabled. If a hook fails, inspect its effects, fix the cause, re-stage only intended content and reverify affected behavior before retrying. If a successful hook changes the candidate, inspect and verify the resulting change before publication; do not assume the earlier test result still applies.
7. Read `git show --stat HEAD`, inspect the resulting commit and run `git status` to confirm exactly what was committed and that excluded staged/unstaged contents remain intact.

## 8. Amend and Fixup

Only within commit/rewrite authority, after checking [Command Policy](command-policy.md#4-bounded-local-corrections):

- **Current HEAD:** for an agent-authored commit in this session with reliable evidence it has never been published, `git commit --amend --no-edit` incorporates exactly the intended index; use a supplied message to correct the message. Preserve unrelated staged work first.
- **Earlier unpublished commit:** use `git commit --fixup=<sha>` only with the intended correction staged. Autosquash with `git rebase -i --autosquash <base>` only when every rewritten commit is agent-authored in this session and confirmed unpublished, and the base is verified. For unattended execution set `GIT_SEQUENCE_EDITOR` to a known no-op using the active shell's syntax, scoped to this operation; do not change persistent editor settings.
- **Published, other-authored or uncertain:** add a new commit. Missing upstream configuration is not evidence that a commit is unpublished. Never amend/rebase a published commit or use force push to repair it.

If ownership, publication status, the index or the rewrite range is uncertain, use an additive correction within authority rather than guessing.

## 9. Identity and Attribution

When the human authorizes the agent to commit, use the human's intended Git identity as the commit author and add `Co-authored-by: <agent name> <agent email>` for the agent performing the commit. Use the attribution identity provided by the host or project; if it is unavailable or ambiguous, ask the human for it rather than inventing one. Add separate trailers for other contributors when applicable.

Before committing, inspect the effective author and committer with `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` in the target worktree. If the intended human author is unclear or the effective author does not match, stop and ask the human to correct the configuration or environment. Do not set or override Git identity yourself. After committing, inspect the author, committer and trailers before publication; stop and report a mismatch. Do not rewrite published history. Never add `Signed-off-by` on the human's behalf.

## 10. Repository Hygiene

| Item                  | Rule                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.gitignore`          | Inspect the project's existing ignore policy. Propose a separate `chore:` change only when required by the project and after selecting patterns appropriate to its build output, dependencies, local environment files, keys/certificates, and editor artifacts                                                                                                                                                                                                                             |
| Generated files       | Commit only when the project requires it (for example lockfiles, migrations)                                                                                                                                                                                                                                                                                                                                                                                                                |
| Secrets               | If a secret appears in a proposed diff, stop and do not commit it; tell the user. If it is in an agent-authored commit proven never pushed, correct the local commit only after verifying no pre-existing user-staged state would be changed; remove the secret from versioned changes without deleting a user-owned local file. If publication status is uncertain, ask. If pushed, tell the user to revoke/rotate it and remove it in a follow-up commit; never rewrite published history |
| Large or binary files | Do not commit unless the project's convention allows it                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Identity              | Do not change `user.name`, `user.email`, or the commit author                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Message content       | No secrets, personal machine paths, or pasted long logs                                                                                                                                                                                                                                                                                                                                                                                                                                     |
