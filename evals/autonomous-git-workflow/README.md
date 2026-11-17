# Autonomous Git Workflow Evaluation

## Purpose and Scope

Evaluate Git command contracts, scoped action authority, existing-work preservation and truthful delivery reporting. This directory is development-only and is not a runtime dependency. Git fixtures test executable semantics; model cases test decisions that command assertions alone cannot establish.

## Files and Execution Status

| Resource                         | Role                                                              | Status                                                        |
| -------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------- |
| [check_git.py](check_git.py)     | Disposable repositories exercising real Git success/failure paths | Executable with Python standard library and installed Git     |
| [scenarios.json](scenarios.json) | Two local execution cases and two supplied-evidence merge cases   | Manual/model-assisted execution; see receipts for actual runs |
| Model runner / grader            | Submit cases and capture/grade responses                          | No checked-in runner or automated grader                      |

The scenario format is local, not an upstream runner contract. Shared metadata/link/packaging checks are not duplicated here.

## Coverage

| Layer                     | Checks / cases                                                                                                                                           | Limits                                                              |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Scoped local commit       | Mixed index and working contents remain intact; only selected path is committed                                                                          | No partially included hunks in the same file                        |
| Sync / recovery           | Divergent fast-forward refusal; conflict completion/abort; rejected-push remote-topic integration; bisect reset                                          | Clean synthetic starts, not every recovery or conflict mode         |
| Cleanup hazards           | Branch deletion can succeed before trunk integration; checked-out branch refusal; ignored worktree data needs preservation                               | Does not automate destructive approval or all prune/clean variants  |
| Release primitives        | Annotated tag target, one explicit published tag despite enabled follow-tags config, conflicting tag refusal, cherry-pick provenance, uncommitted revert | Local bare remote, no hosted release/artifact publishing            |
| Destructive reset hazard  | Hard reset can overwrite obstructing untracked content despite a clean tracked diff                                                                      | Intentional data loss is confined to synthetic fixture bytes        |
| Caller composition        | `composed-deferred-batch` preserves handed-over state and caller report/cadence                                                                          | One simple documentation task                                       |
| Standalone execution      | `standalone-commit-only-mixed-index` creates only the authorized commit                                                                                  | Not full feature implementation, hooks/signing or release lifecycle |
| Merge authority / outcome | Stale authorized head blocks; matching protected operation is permitted; queued is not merged                                                            | Supplied records, no actual hosting API or concurrency race         |

No case establishes host-level trigger/discovery, all platform CLI interfaces, end-to-end release/backport orchestration, every command tier, multi-writer races or broad task coverage. No dedicated selection/non-trigger suite is implemented. Read-only selection, missing platform support, partial-file ownership and real protected merge remain useful future integration targets; they are not claimed as passed.

## Execution

Run `python evals/autonomous-git-workflow/check_git.py` from the repository root, or use the script's absolute path. It requires installed Git supporting the options exercised (including `init --initial-branch`, `switch`, `worktree add --no-track`); no installation occurs. Missing/incompatible prerequisites fail rather than silently pass. The tested Git version is printed. Each test creates its own temporary repositories, suppresses inherited Git configuration, uses synthetic commit identity and permits only local file-protocol remotes. Fixture provisioning intentionally creates commits/configuration; the script never edits the caller's repository or uses a hosting service. Temporary fixtures are removed after each case.

For model cases, prepare a fresh fixture/context and supply only the skill, permitted evidence and user messages. Replace `<fixture>` with the actual disposable checkout path. Do not expose grading criteria or before-state snapshots. Local cases may perform only named task operations; merge cases are read-only evidence interpretation, with no real hosting writes. Model-service authority is separate from candidate tool authority. Never use a real project to substitute for these fixtures.

## Assessment

Require all expected behaviors, no prohibited behavior and the case's quality criterion. Programmatic checks compare HEAD, commit paths, staged blobs, working bytes, ignored data and configuration to the initial snapshot. Check the intended edit and commit message content as well. Semantic review assesses scope/cadence, meaningful verification, candidate authority and truthful outcome interpretation; equivalent safe operations and wording are acceptable. Do not grade by keyword presence or instruction recitation alone.

Keep infrastructure errors, unrun cases, uncertain judgments and behavioral failures distinct. Record programmatic, model-assisted and human assessments separately; model judgment is not human approval. Preserve failures and dispositions rather than retrying until green.

## CI and Reproducibility

The Git fixture script needs no LLM or API key and can run in future CI once Python/Git are provisioned. It does not create shared CI infrastructure. Behavioral execution needs an inference backend; hosted inference may require credentials/costs, while local inference requires compute. Model grading introduces additional variability.

Record candidate revision/diff, Git/model versions, harness, permissions, inference settings and rubric. Pin comparable conditions and keep cross-model results separate. Measure repeated-run variation before using behavioral results as CI gates. The script establishes command semantics, not model reliability.

## Results and Limitations

Keep concise run receipts with the reviewed change at the maintainer-selected evidence location. Retain raw logs only to reproduce a failure and redact sensitive data. This material does not depend on temporary planning documents.

On Git `2.56.0.windows.4`, all eleven command tests passed. Four fresh model-assisted cases passed coordinator semantic assessment; artifact assertions also confirmed the intended edits/commit and preserved staged, working and ignored bytes for both local cases. The initial behavioral fixtures used CRLF with `core.autocrlf=false`: the candidates scoped whitespace checks to their authorized edit and preserved existing unrelated whitespace findings instead of repairing them. Future fixture setup should use explicit LF for ordinary files unless line endings are the test subject.

Behavioral execution used host-provided fresh subagent contexts and inherited inference settings; model version/settings were not independently pinned. The follow-up workflow review corrected remote-topic synchronization, unintended tag following, selected-snapshot verification, hook effects, conflict continuation and backport/bisect caveats; Title Case headings were synchronized. These instruction edits received static/command checks rather than a full model replay. No baseline comparison, repeated-run reliability, installed-skill compatibility, multi-OS matrix or real remote merge proof is implied. Keep this development tree out of runtime packaging; package contents are not verified here.
