# Design Rules: NoSQL Stores

NoSQL is not one data model. Distinguish at least document, key-value, wide-column, graph, time-series, and other specialized stores. These defaults directly cover document and key-value/wide-column modeling; for other types, consult the actual product's current official documentation and project conventions. Never assume relational joins, global transactions, uniqueness, index coverage, consistency, or conditional-write behavior without checking the engine and configuration.

**Design from requirements and access patterns first.** List every important read, create, update, delete, uniqueness check, ordering/pagination path, and event/replay path before choosing a document shape or key/index. Record access patterns as `AP-xx` and link each proposed key/index to the patterns it supports.

## 1. Document stores

### Embedding versus referencing

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

These are workload-dependent choices, not absolute rules. Compare read/write frequency, atomicity needs, size/growth, independent access, duplication, latency, and repair complexity. Record meaningful alternatives in Section 9.

### Document shape and data integrity

- Define field paths, scalar/object/array/reference representation, cardinality, optionality, and the distinction between missing, null, empty, and default values.
- Avoid unbounded arrays and indefinitely growing embedded event/history lists. If an array is embedded, state the expected bound or retention mechanism and what happens when the bound is reached.
- Do not duplicate a canonical fact across documents without a named source of truth, propagation/update mechanism, failure handling, consistency window, and reconciliation strategy.
- If data is duplicated as a historical snapshot, identify it as a snapshot and do not silently treat it as the current source of truth.
- Use schema validation when supported and useful. Specify the validation level, behavior for old/unknown fields, and rollout implications; do not assume validation automatically exists in a flexible-schema database.
- Add a schema/document version only when it supports an actual compatibility, migration, or reader/writer requirement. Specify how older versions are read, migrated, or retired; a version field alone is not a migration plan.
- Treat embedded-document updates and multi-document updates according to the actual engine's atomicity and transaction guarantees. Do not imply that a multi-document operation is atomic by default.
- Specify unique indexes, partial/sparse semantics, array/multikey behavior, and missing/null-field behavior from the actual engine docs. Unique constraints can behave differently for absent or null fields.
- Identify the exact keys and options of every index and the AP it supports. An index may not serve a query the way expected because of array, compound-key, collation, partial, or engine-specific rules.
- Consider document-size limits, write amplification, hot-document contention, index cardinality, and the impact of unbounded nested structures.

### Document lifecycle and data hygiene

- State whether removal is physical deletion, a logical deleted/archived marker, or archival elsewhere. Specify how references and duplicated copies are handled.
- For TTL/expiry, identify the field, time basis, expected expiry delay/semantics from official product docs, and whether expiry is suitable for business/legal retention. Do not treat eventual TTL cleanup as an exact-time business action without evidence.
- For updates, define field-absence behavior and how old documents lacking a newly added field are interpreted.
- For lifecycle state, use one canonical field and explicit allowed values/transitions where appropriate. Use atomic conditional updates/version checks when the engine supports them and the business rule needs conflict detection.

## 2. Key-value and wide-column stores

### Model from key design and workload

- List the exact primary key for every item/row: partition key plus sort/range key where the engine has those concepts. Specify type, encoding, uniqueness scope, and composite-key delimiter/escaping rules if relevant.
- Map each AP to a key condition, filter, ordering, and result set before designing keys. State whether a query requires a secondary index, multiple queries, fan-out, scan, or a materialized/duplicated representation.
- Choose partition keys that distribute load and storage appropriately for the actual workload. High cardinality can help but does not by itself prevent hot keys; test skew, bursts, tenant/celebrity keys, and write concentration.
- Design sort/range keys around required grouping, ordering, prefix, and range queries. If composite keys encode hierarchy or multiple item types, define the grammar and avoid ambiguous or colliding encodings.
- For each secondary index, name the AP and specify partition/sort keys, projected attributes, sparse/condition behavior, consistency semantics, write cost, and migration/backfill implications where the store supports those options.
- Do not assume an index supports arbitrary filters or joins. Many key-value/wide-column products distinguish key conditions from post-read filtering; record the read-amplification risk of any scan/fan-out/post-filter path.
- State how the key design evolves if requirements add a new access pattern. Do not prematurely create a global access path “for flexibility” without a named requirement.

### Integrity, updates, and consistency

- State whether uniqueness is enforced by the primary key, a supported unique index, a conditional write, or application coordination. Never claim global uniqueness when only per-partition uniqueness is guaranteed.
- Model atomicity at the actual granularity (item, partition, batch, transaction, or other documented unit). Cross-item or cross-table atomicity varies by product and operation.
- For read-modify-write logic, specify the concurrency strategy: conditional expression, version attribute/compare-and-swap, supported transaction/lock, or another justified mechanism. Include how conflicts and bounded retries are handled.
- Define idempotency for retries, event replay, at-least-once delivery, and client resubmission. Use deterministic keys/conditional writes or a deduplication record when requirements need it; do not assume a write API is idempotent merely because it has a key.
- For denormalized copies/materialized views, state the canonical source, propagation mechanism, consistency lag, failed-propagation handling, repair/reconciliation, and deletion behavior.
- Consider TTL/retention, data size limits, hot partitions, item-size/row-size limits, index write amplification, capacity/throttling, and pagination limits from official docs for the selected engine.
- Key changes often change item identity or placement. Treat them as potentially breaking migrations: define backfill/copy, dual-read/write or cutover if needed, compatibility, verification, rollback, and old-key retirement.

## 3. Specialized stores and limits

For graph, time-series, search, vector, object, or event-stream stores, do not apply relational normalization or key-value assumptions mechanically. Identify the actual model and query semantics, then consult the product's official modeling, consistency, indexing, lifecycle, partitioning, and migration guidance. If those semantics cannot be established from available evidence, record the unknown and ask before proposing a structural change.

## Official references

- [MongoDB schema design process](https://www.mongodb.com/docs/manual/data-modeling/schema-design-process/) — workload, relationships, patterns, and indexes.
- [MongoDB embedding](https://www.mongodb.com/docs/manual/data-modeling/embedding/) and [referencing](https://www.mongodb.com/docs/manual/data-modeling/referencing/) — trade-offs for related data.
- [MongoDB unbounded-array anti-pattern](https://www.mongodb.com/docs/manual/data-modeling/design-antipatterns/unbounded-arrays/) — size, growth, and reference alternatives.
- [MongoDB schema validation and unique indexes](https://www.mongodb.com/docs/manual/core/schema-validation/) — product-specific validation options.
- [DynamoDB partition-key design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) and [sort-key design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-sort-keys.html) — examples of key/access-pattern coupling.
- [DynamoDB concurrent-update strategies](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BestPractices_ImplementingVersionControl.html) and [condition expressions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html) — examples of conditional writes and conflict handling.
