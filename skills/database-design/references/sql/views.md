# SQL Views

Add derived read models only when they solve a stated interface, authorization, or performance requirement. Do not introduce views solely for organizational convenience or to create unnecessary schema layers.

## Decision Criteria

- Use a regular view for a reusable relational projection, stable read contract, or restricted projection of rows and columns.
- Use a materialized view when repeated expensive reads justify storing query results and bounded staleness is acceptable.
- Use a summary table or maintained projection when refresh semantics, incremental maintenance, transactional consistency, or explicit write control exceed what a materialized view can provide.
- Do not use a view merely to hide query complexity, duplicate an existing access pattern, or create an additional abstraction without a clear consumer.
- Do not assume regular views improve query performance. Their underlying query is generally evaluated when accessed, and complex views may make query optimization and performance analysis more difficult.
- Evaluate whether the same requirement is better served by a well-designed query, appropriate indexes, a materialized view, or a maintained projection.
- Record the consuming access patterns, expected query volume, authorization requirements, and freshness contract before introducing a view.
- Prefer the simplest read model that satisfies the requirement. Avoid introducing additional derived models when the underlying tables already provide an adequate interface.

## Regular Views

- A regular view stores a query definition, not its result. Query execution cost is generally paid when the view is read.
- Prefer simple, explicit projections with clearly defined column names and stable output types. Avoid exposing unnecessary source columns or relying on implicit column ordering.
- Document joins, filters, aggregations, grouping behavior, and expected consumers, especially when the view combines multiple source relations.
- Treat views as read interfaces by default. Updatable-view behavior depends on query shape, database-specific rules, and constraints. Design write-through semantics explicitly when required.
- Do not rely on a view as a security boundary unless its owner/invoker semantics, privileges, and underlying row-level security policies have been reviewed.
- PostgreSQL supports `security_invoker` views (PostgreSQL 15+), which execute permission checks and applicable underlying row-level security policies using the invoking user. By default, PostgreSQL views generally access underlying relations using the view owner's privileges, subject to PostgreSQL's security rules. Choose deliberately and test with the actual runtime role.
- Do not assume that filtering rows or excluding columns in a view automatically provides sufficient authorization. Review direct table access, grants, ownership, RLS behavior, and the application's database role.
- Avoid deeply nested views or excessive view dependencies that make query behavior, authorization, and performance difficult to reason about.

## Materialized Views

- A materialized view stores query results rather than executing the underlying query on every read. Its contents can become stale until refreshed.
- Use a materialized view only when the read-performance benefit justifies storage overhead, refresh cost, and additional operational complexity.
- Define the refresh trigger or schedule, maximum acceptable staleness, failure handling, recovery procedure, and whether a full refresh is acceptable.
- Identify whether refreshes may overlap, whether readers can tolerate stale data during refresh, and how refresh failures affect consumers.
- PostgreSQL `REFRESH MATERIALIZED VIEW CONCURRENTLY` allows concurrent reads during refresh, but requires at least one qualifying unique index using only column names and covering all rows. Partial and expression indexes do not qualify. Only one refresh can run against a given materialized view at a time.
- A qualifying unique index must already exist on the materialized view before using `CONCURRENTLY`. The materialized view must also be populated.
- Index the materialized result for its own access patterns. Do not assume indexes on source tables automatically satisfy reads from the materialized view.
- Account for the storage, indexing, refresh duration, and write amplification associated with maintaining materialized results.
- Do not assume PostgreSQL materialized views support automatic incremental refresh. Standard refresh recomputes the stored query result; incremental maintenance requires a separate mechanism or implementation.
- When freshness must be transactionally current, use the base tables or a deliberately maintained summary model with explicitly defined consistency guarantees.
- Ensure consumers understand that materialized results may not reflect the latest committed source data.

## Example

A stable read projection can expose only the fields required by a consumer:

```sql
CREATE VIEW active_customer_summary AS
SELECT id, display_name, created_at
FROM customers
WHERE deleted_at IS NULL;
```

The view provides a reusable read interface without storing query results. Changes to the underlying `customers` table are reflected when the view is queried, subject to the transaction's visibility rules.

For an expensive aggregate that is read frequently, a materialized view may be appropriate:

```sql
CREATE MATERIALIZED VIEW monthly_order_summary AS
SELECT
  DATE_TRUNC('month', created_at) AS order_month,
  COUNT(*) AS order_count,
  SUM(total_amount) AS total_revenue
FROM orders
GROUP BY DATE_TRUNC('month', created_at);
```

A qualifying unique index can support concurrent refresh when its requirements are satisfied:

```sql
CREATE UNIQUE INDEX idx_monthly_order_summary_month
ON monthly_order_summary (order_month);
```

The materialized view does not automatically update when orders changes. Define its refresh schedule, maximum acceptable staleness, and failure handling rather than assuming it is current.

## Output Mapping

In `Views`, record each view's name, kind, purpose/sources and consumers, security semantics, and refresh/freshness contract. Include required indexes and materialized-view refresh/failure details in the final column when applicable. Omit `Views` when no view or materialized view is justified.
