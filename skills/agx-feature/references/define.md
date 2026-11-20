# Define the Feature Catalog

**Input.** An approved product PRD merged on the refreshed default branch, its verified delivery evidence and the existing catalog, if any.

**Outputs.** The index at `docs/features/catalog.agenix.json` and one `docs/features/<feature-id>/feature.agenix.json` per feature. Publish the index and records together in Git in every tracker mode.

## 1. Establish the Baseline

Verify the PRD merge and required checks before deriving features. Use the owned `docs/feature` branch and phase PR under the shared publication rules. On resume, reconcile the existing catalog, records and PR before allocating IDs or writing. Serialize ID allocation against the refreshed baseline and any approved reservations. If ownership or pending allocations conflict, resolve them before assigning IDs.

## 2. Identify and Bound Features

A feature delivers a coherent, observable outcome for a user, operator or consuming system. It has a clear beneficiary, a bounded behavior and a scenario that demonstrates the outcome through the relevant product boundary. It can be verified and made available once its prerequisites are met.

1. Map the merged PRD's in-scope journeys and obligations to candidate outcomes. Treat PRD headings and user stories as source material. Keep a story as one feature if it meets the quality bar. Combine fragments when they only provide value together, and split broad areas when they contain distinct outcomes.
2. Formulate each candidate as a demonstrable result with clear exclusions. For example, commerce can contain guest checkout and order tracking if each has its own outcome. Product creation can stand alone if it lets a merchant publish a usable listing. Group it with other operations when the approved outcome requires managing the listing lifecycle. Include the layers the outcome needs for this product, whether the public boundary is a UI, API, CLI or library. Route isolated implementation work to later delivery planning.
3. Refine any candidate that still lacks a bounded delivery scope. Ask the human about unresolved scope, priorities or trade-offs that affect feature boundaries. Route changes to approved PRD obligations through the owning amendment workflow.

### Use Flat Slicing When Needed

When a candidate combines multiple outcomes or leaves its boundary too broad, apply [Flat planning](../../work-breakdown-planning/SKILL.md#planning-depth) and the [Slice Quality Bar](../../work-breakdown-planning/SKILL.md#slice-quality-bar) as a one-level method for refining the catalog. Use [workflow steps, operation boundaries or rule variations](../../work-breakdown-planning/references/slicing-techniques.md#default-tier-techniques-that-perform-the-cut) when the resulting slice delivers a meaningful outcome. Check coverage after each proposed cut. Keep the output at feature level in the Agenix records below. Skip the standalone slice plan, decomposition log and ticket or task planning.

## 3. Map Coverage, Dependencies and Priority

- Map each owned functional requirement and in-scope journey to the features that fulfill it. When several features contribute, explain the distinct responsibilities in the approval review. Resolve uncovered obligations and duplicate ownership. Keep shared quality requirements in the PRD until architecture assigns checks. Record provisional responsibility where a feature owns a concrete quality contribution.
- Apply [Dependency Rules](../../work-breakdown-planning/references/dependency-and-status.md#dependency-rules) and the [Cycle Check](../../work-breakdown-planning/references/dependency-and-status.md#cycle-check). Record a direct feature edge when the dependent feature needs a usable outcome of another feature for verification or safe delivery. Explain what it needs and why in the approval review. Priority, preferred order and shared infrastructure alone do not establish an edge. Resolve missing targets, self-edges, duplicates and cycles across the full catalog. If two outcomes must ship together, recheck their boundaries or resolve the prerequisite before approval.
- Set initial readiness from [Decide Readiness and Record Progress](../../../references/work-items-and-evidence.md#decide-readiness-and-record-progress). An unfinished feature dependency yields `BLOCKED` unless covered by an approved override. Use merged completion evidence when evaluating existing prerequisites.

### Rank and Order the Catalog

1. Reuse the project's approved priority labels and their order. Start from the PRD's release scope, explicit commitments and measurable goals. Assess each feature's contribution to those goals, the impact of deferring it and any confirmed deadline or obligation. Explain the basis for the proposed priority in the approval review. If the project has no priority scale, propose a small ordered scale and include it in the same review. Ask the human to resolve material conflicts that prevent ranking.
2. Order the full catalog with prerequisites before their dependents. At each position, choose the highest-priority feature among those whose prerequisite entries have already been placed. Break ties by ascending numeric feature ID. Apply the same order to the review list and the catalog's `features` array. A lower-priority prerequisite can appear before a higher-priority dependent while keeping its own priority. Preserve IDs when the order changes and use delivery evidence to determine readiness separately.

## 4. Write and Validate Records

Use the [catalog schema](../assets/feature-catalog.schema.json) and shared [feature schema](../../../templates/records/feature.schema.json). Preserve approved records and historical IDs. Assign new positive IDs sequentially above all prior IDs, including cancelled items, with at least three digits. Use a new ID for an added outcome or approved replacement and obtain human approval for cancellation.

The catalog holds `schema-version: 1`, `kind: "catalog"` and `features`, a list of unique `{id, path}` entries. Match each ID to its canonical path and the record inside it.

| Feature Field              | Value at Definition                                                                                                                                                                                         |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `schema-version`, `kind`   | `1` and `"feature"`.                                                                                                                                                                                        |
| `id`, `title`              | The allocated ID and a concise name for the capability.                                                                                                                                                     |
| `outcome`                  | A bounded statement of what the beneficiary can do or observe, including scope qualifiers that distinguish this feature from others.                                                                        |
| `priority`                 | A nonempty label from the approved priority scale above.                                                                                                                                                    |
| `depends-on`               | Direct prerequisite feature IDs, or an empty list.                                                                                                                                                          |
| `requirements`, `journeys` | Lists of `{target, revision}` references. Use the real PRD heading anchor and the verified Git revision containing it. Require at least one requirement. Use an empty journey list when no journey applies. |
| `status`                   | `READY` or `BLOCKED` based on dependency evidence.                                                                                                                                                          |
| `quality-allocations`      | Where applicable, list `{requirement-ref, responsibility}` entries. Pin each PRD quality requirement as above and state the feature's contribution.                                                         |
| `origin-ref`               | Include when additive work has a known source finding, amendment or predecessor.                                                                                                                            |

Leave `references`, `delivery-strategy` and `tickets` to their owning workflows. Include `approval-ref`, `checkpoint-refs` or `checkpoints` only as applicable evidence exists, following [Record Fields and Ownership](../../../references/work-items-and-evidence.md#record-fields-and-ownership). Keep feature acceptance and finalization evidence for their owning workflows.

Run the installed [artifact validator](../../../scripts/validate-artifacts.py) with `--project-root <absolute-project-root> --stage feature`. Read back the catalog and records. Review semantic coverage, scope, priority rationale, dependency justification, initial readiness and catalog order separately from the validator result.

## 5. Approve, Publish and Verify Delivery

1. Prepare the root documentation map update using [Configure Instructions and Scope](../../../references/project-content.md#configure-instructions-and-scope). Include it in the same approval and publication.
2. Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates). Present the catalog and records together with the PRD revision, coverage, boundaries, priority rationale, dependency rationale, catalog order and initial statuses. Include validation results and intended publication.
3. [Publish the Approved Candidate](../../../references/git-publication.md#publish-the-approved-candidate) through the catalog phase PR and [Bind Review and CI](../../../references/git-publication.md#bind-review-and-ci-to-the-candidate) to its final head. Reconcile existing publication on resume.
4. Follow [Merge the Approved Head](../../../references/git-publication.md#merge-the-approved-head) and [Verify Delivery](../../../references/git-publication.md#verify-delivery-and-recover-from-a-failed-check). Wait for human merge or separate authority for the exact head. Report the catalog path, PR, merge revision and actual check results when complete. After the matching human `END`, suggest `agx-architect domain` only if eligible for the approved scope.
