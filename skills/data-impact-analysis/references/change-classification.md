# Change Classification and Rollout Safety

Classify each DMC by compatibility with existing data, applications, and consumers. `Additive` and `Breaking` describe compatibility risk, not implementation effort.

## 1. Classification

| Class    | Criteria                                                                                                               | Typical examples                                                                                                                            |
| -------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Additive | Existing valid data and supported old readers/writers remain compatible through rollout.                               | Optional field, independent entity, compatible index, rule limited to new data.                                                             |
| Breaking | Existing data, readers/writers, consumers, or an intermediate rollout can fail or change meaning without coordination. | Rename/remove, incompatible type or key change, required field without safe backfill, tighter constraint, changed deletion/state semantics. |

Before classifying, check:

- Current values: null, missing, duplicate, invalid, and historical data.
- Old/new application compatibility at each rollout stage.
- Consumers: features, jobs, reports, integrations, events, and external clients.
- Engine/version behavior: locks, index builds, consistency, throughput, atomicity.
- Rollback limits and the irreversible point.

Unknown compatibility is not evidence of safety. Record the uncertainty and block the decision when material.

## 2. Breaking Changes: Expand → Migrate → Contract

Use this pattern when it fits the change and technology. Otherwise justify an alternative staged rollout.

1. **Expand:** add the target structure while retaining compatibility with the old one. Define dual-write or another divergence-prevention mechanism where needed.
2. **Migrate:** backfill with a deterministic, repeatable rule. Define batching, checkpoints, invalid/duplicate handling, validation, cutover, consistency window, and recovery.
3. **Contract:** remove the old structure only after verifying that supported versions and consumers no longer use it. Define removal evidence and failure response.

For each stage, state:

- Coexisting model/application versions.
- Data visibility, consistency, and dual-write risk.
- Backfill and completion checks.
- Retry, idempotency, rollback, and recovery.
- DMC dependencies and operational hazards.

Do not write migration commands or scripts. Specify the required behavior for a later implementation task.

## 3. Existing Data and Backfill

- Nullable fields may still need reader/writer coordination.
- Defaults do not necessarily rewrite existing records; verify engine behavior.
- Required fields and stricter constraints need a safe default, deterministic backfill/cleanup, or staged enforcement.
- Check duplicates before adding uniqueness; never invent which record wins.
- For type/encoding changes, define invalid-value handling and pre-cutover validation.
- For key/partition changes, preserve identity and define copy/dual-write, lookup, verification, cutover, rollback, and retirement.
- If no backfill is needed, explain why current data remains valid.

## 4. Indexes and Constraints

Neither is automatically low-risk. Verify engine/version support, locking, online build behavior, resource cost, existing-data validity, and failure recovery. Reflect the result in classification and rollout notes.

## 5. Dependencies and Ordering

- List prerequisites; avoid dependency cycles.
- Keep DMCs reviewable without leaving an invalid intermediate model.
- Order changes to shared structures so every intermediate state is coherent.
- Reuse an applied DMC only after verifying semantic equivalence in the current model.
- Before reversing an applied DMC, inspect later consumers and plan a safe deprecation/rollout.

## References

- [Martin Fowler — Parallel Change](https://martinfowler.com/bliki/ParallelChange.html)
- [AWS DMS — Data Validation](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Validating.html)
- [PostgreSQL — CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html)
