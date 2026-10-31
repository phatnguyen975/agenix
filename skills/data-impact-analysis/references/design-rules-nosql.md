# Design Rules: NoSQL Stores

NoSQL is not one data model. Distinguish document, key-value, wide-column, graph, time-series, search, and event-stream stores. The rules below cover document and key-value/wide-column stores; verify other models against the selected product's documentation.

**Start from requirements and access patterns.** List reads, writes, lookups, uniqueness checks, ordering/pagination, and event/replay paths before choosing the model. Assign `AP-xx` IDs and link keys/indexes to them.

## 1. Document Stores

### Embedding or Referencing

Embedding related data may fit when most of the following are true:

- The related data is usually read with its parent and is not independently queried or owned.
- Cardinality is one-to-one or one-to-few, or the nested collection has an explicit upper bound.
- Data changes together and the datastore's atomicity guarantees for one document meet the requirement.
- Duplication of values is limited or the duplicated data is intentionally a snapshot.

Use references/separate documents or collections when one or more of the following apply:

- The related data is independently queried, updated, authorized, retained, or deleted.
- Relationship cardinality is large, unbounded, or grows with time/users/events.
- Many-to-many relationships require independent lookup or membership management.
- Embedding would cause hot-document contention, large rewrites, document-size risk, or costly duplication.
- Data requires different access control, lifecycle, retention, or ownership boundaries.

Compare workload, atomicity, size/growth, ownership, access, duplication, and repair cost. Record material alternatives.

### Shape and Integrity

- Define field paths, scalar/object/array/reference shape, cardinality, optionality, and missing/null/empty/default semantics.
- Bound embedded arrays or define retention. Avoid unbounded event/history arrays.
- For duplicated facts, name the source of truth, propagation, failure handling, consistency window, and reconciliation.
- Label historical snapshots; do not treat them as current truth.
- Use schema validation when supported; define level, old/unknown-field behavior, and rollout.
- Add a schema version only for a real compatibility/migration need; specify version handling.
- State atomicity at the actual document/operation scope. Do not assume multi-document atomicity.
- Define unique/partial/sparse/multikey behavior and missing/null semantics from product docs.
- Assess size limits, hot documents, index cardinality, and write amplification.

### Lifecycle and Retention

- Specify physical delete, soft delete, archive, and effects on references/copies.
- For TTL, state field, time basis, documented expiry delay, and whether eventual cleanup meets the requirement.
- Define how old documents without a new field are read.
- Use conditional updates/version checks for lifecycle concurrency when supported and required.

## 2. Key-Value and Wide-Column Stores

### Keys and Workload

- Define the full primary key: partition plus sort/range key where applicable; include type, encoding, uniqueness scope, and composite-key grammar.
- Map each AP to key conditions, filters, ordering, and result shape. State when a secondary index, fan-out, scan, or materialized copy is needed.
- Assess hot keys and skew; high cardinality alone does not prevent hot partitions.
- Design sort keys for grouping, prefix, range, and ordering needs. Avoid ambiguous composite encodings.
- For each secondary index, define keys, projection, sparse/condition rules, consistency, cost, and backfill where supported.
- Distinguish key conditions from post-read filters; record scan/fan-out/read-amplification risk.
- State the risk if future requirements add access patterns.

### Integrity and Consistency

- State how uniqueness is enforced and its scope; never claim global uniqueness from partition-scoped guarantees.
- Define atomicity at the documented item/partition/batch/transaction scope.
- For read-modify-write, define conditional write/version/transaction strategy and conflict/retry behavior.
- Define idempotency for retries, replay, at-least-once delivery, and resubmission.
- For duplicated/materialized data, state canonical source, propagation, lag, failure handling, repair, and deletion behavior.
- Assess TTL, size limits, hot partitions, throttling, capacity, and pagination.
- Treat key changes as potentially breaking: define identity preservation, copy/dual-write, cutover, verification, rollback, and retirement.

## 3. Specialized Stores

For graph, time-series, vector, search, object, or event-stream stores:

- Do not apply relational or key-value assumptions mechanically.
- Verify model, query, consistency, indexing, partitioning, lifecycle, and migration semantics using project guidance and official product documentation.
- Record unknowns and ask when they affect correctness.

## Official References

- [MongoDB Schema Design](https://www.mongodb.com/docs/manual/data-modeling/schema-design-process/)
- [MongoDB Embedding](https://www.mongodb.com/docs/manual/data-modeling/embedding/) and [Referencing](https://www.mongodb.com/docs/manual/data-modeling/referencing/)
- [MongoDB Unbounded Arrays](https://www.mongodb.com/docs/manual/data-modeling/design-antipatterns/unbounded-arrays/)
- [MongoDB Schema Validation](https://www.mongodb.com/docs/manual/core/schema-validation/)
- [MongoDB Unique Indexes](https://www.mongodb.com/docs/manual/core/index-unique/)
- [DynamoDB Partition Keys](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) and [Sort Keys](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-sort-keys.html)
- [DynamoDB Version Control](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BestPractices_ImplementingVersionControl.html) and [Condition Expressions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html)
