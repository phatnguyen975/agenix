# NoSQL Data Lifecycle

Model audit metadata, revisions, deletion, retention, and archival from explicit domain and operational requirements.

## Audit Metadata

- Add `createdAt` when creation time is meaningful and `updatedAt` when consumers need last-modified time. Store instants as BSON `date` values.
- State which trusted write path maintains each value. A field default does not automatically maintain timestamps on every update; upserts and replacement updates need deliberate handling.
- Add actor identifiers (`createdBy`, `updatedBy`) only when attribution is required. Define whether they are references, external subject IDs, or immutable snapshots.
- Do not add audit fields mechanically to immutable facts or collections where they provide no useful semantics.

## Change History

| Mechanism                  | Model                                                          | Use When                                                                           |
| -------------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Bounded embedded revisions | Append a small, bounded revision array to the current document | Few revisions are read with the document and size stays bounded                    |
| History collection         | Append revision documents keyed by entity ID and revision/time | History is large, unbounded, independently queried, or retained separately         |
| Domain event collection    | Append immutable business events                               | Events are domain facts needed for replay, integration, or temporal reconstruction |

- Define full snapshot versus delta, revision identity/order, actor, reason, and effective time.
- A history collection is not append-only merely because the application intends it to be. Restrict database privileges and define retention/immutability controls.
- Avoid embedding an unbounded revision array in the current document.

## Deletion and Retention

| Strategy      | Model                                             | Consequences to Specify                                                                        |
| ------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Hard delete   | Delete document(s)                                | Referencing-document cleanup, recovery, audit, and transaction needs                           |
| Soft delete   | Explicit state or `isDeleted`/`deletedAt`         | Active filters, restore behavior, uniqueness, child visibility, and final purge                |
| Archive       | Copy/move to archive collection or external store | Idempotency, consistency during move, schema compatibility, restore path, access and retention |
| Anonymization | Irreversibly transform personal fields            | Embedded/history/archive copies, exports, backups, and re-identification risk                  |

- Derive retention periods from confirmed requirements or policy. Use `Not specified` rather than inventing a period.
- For active-only uniqueness, use a partial unique index with an explicit active-state predicate (for example `{ isDeleted: false }`) and define behavior for legacy documents missing the flag.
- TTL indexes delete asynchronously after expiry; they are not exact-time schedulers or a guaranteed legal-erasure workflow.
- TTL applies to a date field and has index-shape restrictions; verify the target version and collection type. Time-series collections can use collection-level `expireAfterSeconds` retention options.
- Time-series collections do not support schema validation or change streams, cannot be written to inside multi-document transactions (reads are supported), and have a 4 MiB per-document limit. Do not design their ingestion/integration workflow as though these capabilities exist.
- Time-series collections have constrained update semantics: updates can only match/modify the `metaField` and must use supported update operators. Treat measurements as append-oriented facts; use a regular collection when arbitrary measurement correction is required.
- Set `timeField`, `metaField`, and bucketing/granularity options at collection creation; do not assume these can be freely changed later. MongoDB buckets are bounded by both measurement count and bucket size, so avoid designing custom documents that approach the collection's document limit.
- Use an idempotent scheduled process when deletion requires conditions, cross-collection cleanup, archival, or auditable completion.
- Distinguish logical deletion, primary deletion, replica propagation, and backup expiry; state the operational scope of any erasure guarantee.

## Time-Series Collection Design

- Use a time-series collection for append-heavy measurements/events queried by time ranges and grouped by stable metadata dimensions.
- Define `timeField`, optional `metaField`, expected time precision, late/out-of-order arrival behavior, metadata cardinality, and retention window.
- Keep metadata stable and compact; avoid frequently changing values in metadata when that fragments bucket grouping.
- Use an ordinary collection instead when strict schema validation, change-stream integration, arbitrary measurement updates, or multi-document transactional writes to the measurement record are required.

## Example

A partial unique index can preserve active-only uniqueness, while TTL is suitable for expiring temporary sessions (not exact-time deletion guarantees):

```javascript
db.users.createIndex(
  { tenantId: 1, emailNormalized: 1 },
  { unique: true, partialFilterExpression: { isDeleted: false } },
);

db.sessions.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });
```

The expiry worker removes expired documents asynchronously; business workflows must not depend on removal at the exact expiry instant.

## Output Mapping

Per collection, record audit fields and maintenance owner; revision/event approach; delete/restore behavior; retention period and trigger; TTL/job/archive mechanism; time-series options/limitations; and copies that must be anonymized or erased. Omit non-applicable sections explicitly.
