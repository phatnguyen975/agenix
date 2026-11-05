# NoSQL Views

Use read models when they provide a stable projection or materialize expensive derived data with an explicit freshness contract.

## Standard Views

- A MongoDB view is a read-only aggregation pipeline over a source collection or another view. It stores no result documents and runs the pipeline when queried.
- Use a view for a stable projection, reshaped data contract, or restricted set of fields when authorization has been independently verified.
- A view has no indexes of its own; query performance depends on indexes of underlying collections and pipeline shape.
- Do not treat a view as a replacement for data modeling or as an automatic security boundary.

## On-Demand Materialized Views

- Use a target collection populated by an aggregation pipeline ending in `$merge` or `$out` when expensive derived reads are frequent and bounded staleness is acceptable.
- Define whether refresh is full, incremental, scheduled, event-triggered, or recomputed on demand; define maximum staleness and failure/recovery behavior.
- `$merge` can update/merge results into a target collection. Define the unique key and deletion handling so stale target documents do not remain indefinitely.
- Index the target collection for its own access patterns. Source indexes do not automatically index the materialized result.
- Do not use a materialized view when output must be transactionally current with source writes.

## Modeling Signal

- A hot-path `$lookup` or multi-stage aggregation may indicate a model that does not match the access pattern. Reconsider embedding, an extended reference, subset, or computed pattern before adding pipeline complexity.
- A lookup is not inherently wrong; retain it when normalized source-of-truth, cardinality, and measured workload make it the clearer design.

## Example

An on-demand summary collection can be refreshed from order facts:

```javascript
db.orders.aggregate([
  {
    $group: {
      _id: "$customerId",
      orderCount: { $sum: 1 },
      totalSpent: { $sum: "$totalAmount" },
    },
  },
  {
    $merge: {
      into: "customerOrderSummary",
      on: "_id",
      whenMatched: "replace",
      whenNotMatched: "insert",
    },
  },
]);
```

Define how summaries for customers with no remaining orders are removed and how often the pipeline runs; `$merge` alone does not define the complete refresh lifecycle.

## Output Mapping

In `Views`, record each view/read model's name, kind, source collections, purpose, pipeline summary, consumers, authorization behavior, freshness/staleness, refresh trigger, failure recovery, and target indexes. State `None` or omit the conditional section when no derived read model is justified.
