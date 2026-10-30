# Change Classification and Rollout Safety

Classify each DMC by its actual compatibility and deployment consequences. `Additive` and `Breaking` describe a change's compatibility risk; they are not synonyms for “easy” and “hard”, and neither label alone proves a rollout is safe.

## 1. Classification criteria

| Classification | Default criteria                                                                                                                                            | Examples (verify actual behavior)                                                                                                                                                                                                                                    |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Additive       | Existing valid data and supported old readers/writers continue to work during the intended rollout; the change does not silently tighten existing behavior. | New optional field; new entity not required by old code; new index that does not invalidate existing operations; new optional rule whose scope is only new data.                                                                                                     |
| Breaking       | Existing data, existing readers/writers, consumers, or a supported intermediate rollout can fail or change meaning unless coordinated.                      | Rename/remove; incompatible type/encoding change; new required value without a safe default/backfill; changed key/identity; tighter constraint violated by current data; changed deletion/state semantics; removing or changing an index/key that consumers require. |

Before classifying, answer:

1. What happens to current records/items, including null, missing, duplicate, malformed, and historical values?
2. Can the old application version read and write the proposed/intermediate model? Can the new version operate before the backfill/cutover finishes?
3. What do other features, jobs, reports, integrations, events, and external consumers depend on?
4. What are the actual datastore/version's lock, index-build, consistency, throughput, and atomicity behaviors?
5. Is rollback possible after writes use the new representation? If not, identify the irreversible point.

If a critical compatibility fact is unknown, state the uncertainty and do not call the change safe merely because it looks additive on paper.

## 2. Breaking changes: expand → migrate → contract

Use this rollout pattern when it fits the actual change and technology. Some changes require a different strategy; justify it if expand/migrate/contract is not applicable.

1. **Expand:** add the new structure while preserving the old one. Keep both readers/writers compatible where required. Define how new writes populate both representations, or otherwise prevent divergence.
2. **Migrate:** backfill old data using a deterministic, repeatable rule; define batching, checkpoints, duplicate/invalid-value handling, validation/reconciliation, and failure recovery. Switch readers/writers in a controlled order, with feature flags or a documented cutover when appropriate. State the consistency window.
3. **Contract:** remove the old structure only after proving relevant consumers and supported application versions no longer use it. Define the evidence/criteria for removal and how to recover if the check fails.

For every phase, state:

- model and application versions that may coexist;
- data visibility/consistency guarantees and any dual-write risk;
- backfill rule and how completion/correctness are verified;
- retry, idempotency, rollback, and recovery behavior;
- dependencies/order relative to other DMCs;
- operational hazards such as locks, table rewrites, index build duration, replication lag, throttling, item-size limits, or hot partitions when relevant.

Do not prescribe specific SQL or migration commands in this skill. Record the required structural and rollout behavior for a later implementation task.

## 3. Existing data, defaults, and backfill

- A new nullable field may still require reader compatibility and application deployment coordination.
- A default does not necessarily rewrite existing records or guarantee every writer provides the expected value. Verify the engine's behavior.
- A new required field or stricter constraint needs either a valid default, an explicit backfill/cleanup rule, or a staged transition before enforcement.
- For uniqueness, check existing duplicates and specify how conflicts are resolved. Do not invent which record wins.
- For type/encoding changes, define handling of invalid, out-of-range, precision-losing, or ambiguous values and how data is validated before cutover.
- For key/partition changes, specify identity preservation, old-to-new lookup, copying/dual-write, verification, traffic cutover, and retirement of old keys.
- If no backfill is needed, state why existing data remains valid and what confirms that claim.

## 4. Indexes and constraints can have rollout risk

An index or constraint is not automatically low-risk. Check the selected product/version for online/concurrent build support, locking, resource use, uniqueness validation, consistency behavior, and failure recovery. Adding an index may be compatible but expensive; adding a constraint can fail because existing data violates it. Reflect these facts in the classification rationale and migration/rollout notes.

## 5. Dependencies and ordering

- List DMC dependencies explicitly. A prerequisite must be applied first; do not create circular dependencies.
- Keep DMCs independently reviewable, but do not split a change into artificial pieces that leave the model invalid between steps.
- A shared table/collection can be affected by several DMCs. State their order and ensure intermediate models are coherent.
- Reuse an already confirmed/applied DMC only after verifying the current model contains the equivalent structure. If the definition changed, treat it as a new/materially changed DMC requiring approval.
- When a previously approved change is later rejected, inspect subsequent consumers before removing it. Reversal may require a new rollout plan rather than a blind deletion.
