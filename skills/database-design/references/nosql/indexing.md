# NoSQL Indexing

Design indexes based on explicit access patterns, query predicates, sorting, uniqueness requirements, and database capabilities. Examples use MongoDB; adapt index types and behavior to the target database.

## Index Candidates

- Identify query patterns before proposing indexes. Record collection, filter predicates, sort order, projection, and expected result cardinality.
- Create indexes when they materially support frequent queries, selective filters, sorting, range queries, uniqueness constraints, geospatial operations, or retention policies.
- Consider query frequency, selectivity, read/write ratio, and collection size when evaluating index necessity.
- Do not index every field or reference automatically. Each index adds storage, memory, and write-maintenance costs.
- A collection scan may be appropriate for small collections or queries returning a large fraction of documents.
- Consider range-based pagination with stable sort keys instead of deep `skip` pagination on large datasets.
- Index fields used in MongoDB `$lookup` operations on the foreign collection when they support the join predicates.

## Compound Indexes

- Design compound indexes around specific query patterns. Field order determines which filters and sorts the index can support.
- Use Equality-Sort-Range (ESR) as a starting heuristic: equality fields first, followed by sort fields, then range fields.
- Consider Equality-Range-Sort (ERS) when a selective range predicate is more beneficial than index-provided sorting.
- Follow the leftmost-prefix principle. An index on `{ tenantId: 1, status: 1, createdAt: -1 }` generally supports queries beginning with `tenantId`, but not queries filtering on `status` alone.
- Consider sort direction and collation compatibility when designing compound indexes.
- Avoid redundant prefix indexes unless uniqueness, partial filters, collation, or measured workload justifies them.

## Specialized Indexes

| Index         | Use When                                     | Considerations                                                                     |
| ------------- | -------------------------------------------- | ---------------------------------------------------------------------------------- |
| Unique        | Enforcing uniqueness of one or more fields   | Define uniqueness scope, null/missing behavior, and collation.                     |
| Partial       | Indexing only documents matching a condition | Queries must imply the partial filter for index eligibility.                       |
| Sparse        | Excluding documents without indexed fields   | Understand missing-field and uniqueness behavior.                                  |
| Multikey      | Querying array elements in MongoDB           | A compound multikey index cannot index multiple array fields in the same document. |
| TTL           | Automatically expiring documents             | MongoDB TTL deletion is asynchronous, not an exact-time scheduler.                 |
| Geospatial    | Geographic and spatial queries               | MongoDB GeoJSON `2dsphere` coordinates use `[longitude, latitude]`.                |
| Text / Search | Full-text search and relevance ranking       | Distinguish MongoDB text indexes from MongoDB Search or external search engines.   |
| Hash          | Equality-based lookups                       | Does not support ordered or range queries through the hashed key.                  |
| Vector        | Similarity search over embeddings            | Define vector dimensions, distance metric, and filtering requirements.             |

- Verify that the target database supports the selected index type and its specific restrictions.
- For MongoDB time-series collections, do not assume ordinary collection behavior: there is no default `_id` index, unique indexes are unsupported, and some secondary index types have `metaField` restrictions. Check the target MongoDB version.

## Index Examples

Tenant-scoped filtering and sorting:

```javascript
db.orders.createIndex(
  { tenantId: 1, status: 1, createdAt: -1 },
  { name: "ix_orders_tenant_status_created" },
);
```

Active-only uniqueness:

```javascript
db.users.createIndex(
  { tenantId: 1, emailNormalized: 1 },
  {
    unique: true,
    partialFilterExpression: { isDeleted: false },
    name: "uq_users_tenant_email_active",
  },
);
```

## Verification Criteria

For each index, document:

- Index name and target collection.
- Indexed fields, key order, and direction.
- Index type and options (unique, partial, sparse, TTL, collation).
- Associated access-pattern ID (`AP-nn`).
- Query frequency, selectivity, and expected result cardinality.
- Expected filtering and sorting benefits.
- Storage and write-maintenance impact.
- Verification status.

Distinguish:

- **Proposed:** Justified by documented access patterns but not yet tested.
- **Verified:** Evaluated using execution plans, query statistics, or representative benchmarks.
- **Not needed:** No documented requirement justifies an additional index.

For MongoDB, use `explain("executionStats")` to examine documents examined, keys examined, returned documents, and sort behavior. Do not claim an index is optimal based solely on its field composition.

## Output Mapping

- `Access Patterns`: define the query shape and the `AP-nn` served by each index.
- `Indexes`: record key order, options, uniqueness/partial/TTL semantics, and workload rationale. State `None` when no secondary index beyond required defaults is justified.
