# Change Classification and Rollout Safety

Assess each proposed change against existing data, applications, and consumers. Classify compatibility separately from rollout risk. An additive change may still require a table lock, significant storage, or deployment coordination.

## 1. Classification

| Class      | Criteria                                                                                                                        | Typical Examples                                                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Compatible | Existing valid data and supported readers and writers continue to work through rollout. Assess this for each supported version. | An optional field accepted by existing readers and writers, or an independent table.                                                        |
| Breaking   | Existing data, readers/writers, consumers, or an intermediate rollout can fail or change meaning without coordination.          | Rename/remove, incompatible type or key change, required field without safe backfill, tighter constraint, changed deletion/state semantics. |

Before classifying, check:

- Current values: null, missing, duplicate, invalid, and historical data.
- Old/new application compatibility at each rollout stage.
- Consumers: features, jobs, reports, integrations, events, and external clients.
- Engine/version behavior: locks, index builds, consistency, throughput, atomicity.
- Rollback limits and the irreversible point.

When information is missing, report compatibility as unverified and identify the affected rollout decision.

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
- Change dependencies and operational hazards.

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

- Keep each change reviewable and each intermediate state compatible with supported readers and writers.
- Check ordering, overlaps, and owners using [Parallel Changes](baseline-reconciliation.md#parallel-changes).
- Before reversing an applied change, inspect later consumers and supported deployed versions. Prefer a verified forward correction or recovery plan when reversing the schema would lose data or break those consumers.

## References

- [Martin Fowler — Parallel Change](https://martinfowler.com/bliki/ParallelChange.html)
- [AWS DMS — Data Validation](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Validating.html)
- [PostgreSQL — CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html)
