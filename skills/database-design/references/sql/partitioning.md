# SQL Partitioning

Partitioning splits one logical table into multiple physical partitions. Use it only when workload, data size, or lifecycle operations justify the planning and operational complexity.

## When to Partition

Consider partitioning when one or more conditions are evidenced:

- A very large table has locality or index-size problems that partition pruning can materially improve.
- Most important queries constrain a candidate partition key and can prune most partitions.
- Retention or bulk archival regularly removes whole time ranges or key ranges.
- Bulk loads/maintenance benefit from isolating partitions.

A table larger than physical memory is a PostgreSQL rule of thumb for considering partitioning, not a sufficient condition or mandatory threshold. Small tables, queries that touch most partitions, or high partition counts can become slower or harder to manage. Measure expected workload and keep a non-partitioned design when benefits are unclear.

## Methods

| Method | Typical Use                                                      | Main Trade-off                                                                               |
| ------ | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Range  | Time windows or ordered key ranges                               | Boundary maintenance and queries must filter by the range key to prune.                      |
| List   | A small, stable set of discrete categories                       | Can create too many partitions when values grow without bound (for example, one per tenant). |
| Hash   | Even distribution when no useful natural range/list split exists | Does not align naturally with time-based retention or range queries.                         |

## Partition Key

- Choose keys that align with the highest-value query predicates and lifecycle operations.
- For time retention, use the event/retention time when that same key is queried often.
- Avoid keys that create extreme skew or an unmanageable number of partitions.
- Evaluate future growth and tenant cardinality, not just current counts.

## Constraints and Operations

- In PostgreSQL, a primary key or unique constraint on a partitioned table must include every partition-key column. This can prevent a globally unique business key that omits the partition key.
- Keep partition count moderate. Too many partitions increase planning and per-session metadata overhead, especially when queries touch many partitions.
- Define partition creation cadence, boundary handling, late-arriving data, default-partition policy, and retention/drop workflow.
- Detaching/dropping a whole partition can be substantially cheaper than deleting large volumes row by row, but only if the partition boundaries match the retention policy.
- Partitioning does not replace indexes inside partitions or guarantee query speedups.

## Example

A time-ranged fact table whose primary key includes its partition key:

```sql
CREATE TABLE measurements (
  measured_at timestamptz NOT NULL,
  device_id bigint NOT NULL,
  value numeric NOT NULL,
  PRIMARY KEY (measured_at, device_id)
) PARTITION BY RANGE (measured_at);

CREATE TABLE measurements_2026_11
  PARTITION OF measurements
  FOR VALUES FROM ('2026-11-01 00:00:00+00') TO ('2026-12-01 00:00:00+00');
```

Partitioning is appropriate only if query predicates and retention operations align with `measured_at`; it is not a substitute for workload-driven indexing.

## Output Mapping

Include the `Partitioning` section only when justified. For each table, record method, partition key, granularity/count strategy, query patterns that prune, uniqueness implications, and lifecycle/maintenance policy. Reference the supporting `Access Patterns` IDs.
