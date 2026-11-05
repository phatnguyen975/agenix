# SQL Indexing

Select indexes for known operations and invariants. Index types and syntax below use PostgreSQL; the selection principles apply broadly, but operator support is engine-specific.

## When to Index

An index is justified when it supports one or more of:

- A recurring access pattern's filter, join, ordering, pagination, or selective projection.
- A business uniqueness rule.
- A lifecycle operation that locates rows to expire, archive, or delete.
- A foreign-key maintenance path where child-side scans during parent delete/key update are costly.

Do not add an index merely because a column exists or appears in a filter. A sequential scan may be correct for a small table, a low-selectivity predicate, or a query returning a large share of rows. Every index adds storage and write/maintenance cost. Primary-key and unique-constraint indexes already exist.

## Index Types

| PostgreSQL Index Type | Typical Use                                                                                                        | Cautions                                                                                  |
| --------------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| B-tree                | Equality, range, ordered retrieval, and many uniqueness constraints                                                | General-purpose default; multicolumn efficiency depends on leading keys.                  |
| Hash                  | Equality on a single key                                                                                           | Narrow use; B-tree is usually more flexible.                                              |
| GiST                  | Range overlap/containment, spatial and other operator-class searches, exclusion constraints                        | Operator class and key order matter.                                                      |
| SP-GiST               | Data with natural partitioning into non-overlapping regions (for example, selected geometric or prefix structures) | Specialized; not a general replacement for B-tree.                                        |
| GIN                   | Multiple components per row such as arrays, JSONB containment/key search, and full-text vectors                    | Write-heavy updates can be more expensive; operator class determines supported operators. |
| BRIN                  | Very large tables where indexed values correlate with physical row order (for example, append-time data)           | Lossy block summaries; unsuitable for random distributions or precise single-row lookup.  |

## Index Forms

- **Unique:** enforce a domain key, not just to influence query plans.
- **Composite:** several ordered key columns for access patterns that constrain/order by the combination.
- **Partial:** indexes only rows satisfying a stable predicate (for example, active records). The query predicate must be compatible with the index predicate for the planner to use it.
- **Expression:** indexes a deterministic expression used by predicates or uniqueness (for example, case-folded email). Keep the query expression and collation semantics consistent.
- **Covering:** PostgreSQL `INCLUDE` stores non-key columns to support possible index-only scans. Use only when a frequent projection justifies the larger index.

## Composite Index Design

- For B-tree indexes, equality conditions on leading columns are generally the strongest starting point; the first range condition limits the portion of the index that can be scanned efficiently.
- Match key order to real filter combinations, sort direction, pagination, and reuse across access patterns. Do not use a rigid universal "equality, sort, range" formula for every query.
- A composite index `(a, b)` can serve patterns using its leading prefix, but a narrower `(a)` index may still be useful when it is materially smaller or better for a workload. Verify before declaring indexes redundant.
- For mixed-direction multi-column sorts, specify the appropriate index ordering.
- PostgreSQL 18 can use B-tree skip scans for some non-leading predicates; do not design around skip scan without workload evidence.

**Example workload:** for a frequent tenant-scoped query filtering by `tenant_id` and `status`, then sorting recent orders, `(tenant_id, status, created_at DESC)` is a candidate. Confirm the actual selectivity, projection, and write cost before finalizing.

## Foreign Key Indexes

- A foreign key does not automatically imply a separate child-side index.
- Consider an index when joins or lookups use the child key, or parent deletion/key updates would otherwise scan many child rows.
- Omit an index when the table is small, the key is not queried, and parent-side maintenance is rare/cheap. Record the reason where omission could otherwise look accidental.
- For composite foreign keys, an existing index may already cover the required leading columns.

## Review Criteria

For each candidate index, record key order, direction, predicate, included columns, operator class/type, and the access pattern or rule it serves. Check:

- Selectivity and expected result size.
- Whether the query constrains the leading keys and can use the intended ordering.
- Insert/update/delete rate and index maintenance cost.
- Existing primary, unique, composite, or partial indexes that overlap.
- Whether an index actually helps the intended pattern on representative data. Do not claim a performance result without measurement.

## Example

An index for a tenant-scoped order list filtered by status and sorted newest first:

```sql
CREATE INDEX ix_orders_tenant_status_created
  ON orders (tenant_id, status, created_at DESC);
```

This is justified only when the corresponding access pattern uses those leading predicates and order. A small table or low-selectivity query may still be faster with a sequential scan.

## Output Mapping

- `Indexes`: one row per non-constraint index with its table, type, keys/expression, predicate, included columns, and supporting `AP-nn`, `BR-nn`, or lifecycle policy.
- `Access Patterns`: define the operation represented by every referenced `AP-nn`.
- `Tables > Table-Level Constraints`: define primary-key and unique constraints; do not duplicate their implicit indexes in `Indexes`.
