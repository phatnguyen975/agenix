# PRD Writing Evaluation

## Purpose and Scope

Evaluate evidence-aware elicitation, complete final PRDs, product/feature boundaries and scoped revisions. These are development-only cases, independent of runtime resources.

## Files and Execution Status

| Resource                         | Role                                                   | Status                                                  |
| -------------------------------- | ------------------------------------------------------ | ------------------------------------------------------- |
| [scenarios.json](scenarios.json) | Three semantic cases with permitted inputs and rubrics | Fresh-context model-assisted execution                  |
| Runner / grader                  | Submit cases and assess results                        | No checked-in runner, automated grader or CI job        |
| Structural checks                | Metadata, links, template and JSON                     | Maintainer checks; no duplicate per-skill static script |

The conversation format is local, not an upstream runner contract.

## Coverage

| Layer                  | Cases / Evidence                                   | Limits                                        |
| ---------------------- | -------------------------------------------------- | --------------------------------------------- |
| Missing prerequisites  | `missing-targets-no-fabrication`                   | Initial response, not a full interview        |
| Caller composition     | `caller-owned-scoped-revision`                     | Supplied excerpt and chat output              |
| Standalone delivery    | `ready-feature-save`                               | One real isolated feature PRD write/read-back |
| Structural consistency | Fourteen sections, metadata, IDs, routes and UTF-8 | Does not establish product correctness        |

No host discovery/non-trigger suite, full product PRD, prolonged multi-turn elicitation, collision/write failure, repeated-run reliability or installed-host compatibility is established. Cases exercise explicit skill loading. No executable coverage percentage applies to an instruction-only capability.

## Execution

Use a fresh context per case. Supply only the skill, raw inputs and permitted resources; hide grading criteria. For the save case, provide an empty disposable root and authorize only the named PRD and parent directories. Keep other cases read-only. No network, Git publication, credentials, dependency installation or product execution is permitted. Model-service authority is separate from candidate tool authority.

Capture actual responses and inspect saved artifacts. Later interview turns, if added, must follow real preceding replies; do not fabricate stakeholder decisions. Scenario requests summarize the evaluated input contracts; receipts identify actual execution and limitations.

## Assessment

Require every expected behavior, no prohibited behavior and the semantic quality criterion. Use deterministic assertions for the exact destination, permitted file set, section sequence and ID/reference integrity. Use semantic assessment for faithful product scope, actionable blockers, non-numeric verifiability, realistic measurement context and absence of invented choices. Keyword matching alone cannot establish these properties.

Distinguish infrastructure failure, unrun cases, uncertain judgment and behavioral failure. Coordinator/model-assisted review is not human product approval. Preserve failure dispositions rather than retrying until green.

## CI and Reproducibility

No runner/provider or CI gate is selected. Static checks need no LLM/API key. Behavioral execution requires an inference backend; hosted inference may incur credentials/costs and local inference needs compute. Model grading adds variability.

Record candidate identity, model/settings, permissions, harness and rubric. Compare under matching conditions and measure variation before adopting model results as gates; cross-model results are separate targets.

## Results and Limitations

Keep concise receipts with the reviewed change at the maintainer-selected evidence location; retain raw material only when needed to reproduce a failure. This material does not depend on temporary planning documents.

Runs use host-provided independent subagent contexts with inherited settings, not independently pinned model/settings. Three isolated cases passed coordinator semantic assessment; saved-output assertions confirmed the sole authorized file, fourteen sections and twelve unique/resolving IDs. The initial assertion missed IDs defined in journey headings; it was corrected to include both definition forms. Final wording synchronized the already-required target-readiness rule across resources and received static review, not a model replay. This is single-run evidence, not stakeholder validation, broad system coverage or a reliable CI gate. Keep development material out of runtime packaging; package contents are not verified here.

The later terminology/principles/presentation review changed template metadata and multi-field entries to explicit lists/headings, with real ordered journey steps. Source checks verified fourteen sections, distinct field markers and valid resource anchors; the earlier model cases were not replayed against this layout. No rendered HTML/browser visual check is claimed. ID integrity checks must recognize both heading and bullet definitions rather than assume a single markup form.

The human selected product and feature as the supported document scopes. Terminology was synchronized without changing requirement subjects such as "The system MUST". This follow-up received static checks; prior model runs are not a replay of the final wording.
