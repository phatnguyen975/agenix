# NoSQL Design Patterns

Apply a pattern only when a documented access pattern or domain constraint justifies its read/write and consistency trade-offs. Do not use patterns as defaults.

## Computed Pattern

- **Problem:** A frequently requested value requires repeated expensive computation.
- **Use when:** Reads dominate writes, the computation is repeatable, and bounded staleness or write-time maintenance is acceptable.
- **Model:** Store the derived value on the owning document or in a projection. Update atomically with the source write where practical, or recompute using a defined job.
- **Required contract:** Identify the source of truth, update path, reconciliation process, and acceptable drift/staleness.
- **Trade-off:** extra write cost, possible staleness.
- **Avoid when:** The value must always be exact but cannot be updated atomically, or is cheap to calculate.
- **Example:** `products.reviewCount`, `orders.totalAmount`.

## Bucket Pattern

- **Problem:** A high-volume stream produces many small records with time-window access.
- **Use when:** Records are append-heavy, commonly queried by time window, and bucket grouping reduces document/index overhead.
- **Model:** Group a bounded set of measurements by stable dimensions and time window. Define maximum count/size, closure, late-arrival handling, and update contention.
- **Trade-off:** more complex updates.
- **Avoid when:** Records need independent updates, arbitrary per-record access dominates, or unbounded bucket growth is possible. For pure time-series measurements, evaluate native time-series collections first.
- **Example:** `{ deviceId, hourStart, count: 3600, readings: [{ t, v }, ...] }`.

## Subset Pattern

- **Problem:** A large related set is often only partially needed with the parent.
- **Use when:** Most reads need a small, predictable subset while the full set is queried separately.
- **Model:** Embed the hot/recent subset on the parent and retain the complete set in a separate collection. Identify canonical ownership and synchronization.
- **Avoid when:** The subset cannot be maintained consistently or the parent document can grow without bound.

## Extended Reference Pattern

- **Problem:** Reads need a few related display fields but a lookup is too expensive or too frequent.
- **Use when:** A small set of stable attributes is repeatedly read with the referencing document.
- **Model:** Store the target identifier plus selected copied fields. Define source of truth, update propagation, staleness, and reconciliation.
- **Avoid when:** Copied fields change frequently or must be immediately consistent.
- **Example:** `orders.customer = { _id, name }`.

## Attribute Pattern

- **Problem:** Records share a core structure but have a variable set of attributes that must be queried.
- **Use when:** Dynamic attributes are numerous/variable and users query across them.
- **Model:** Use an array of `{ name, value }` entries with controlled value types and indexes appropriate to the query. Prefer typed top-level fields for stable, frequently queried attributes.
- **Avoid when:** Dynamic field names are not queried or a fixed schema is adequate.
- **Example:** `attributes: [{ name: "material", value: "steel" }, { name: "weightGrams", value: 850 }]`.

## Polymorphic Pattern

- **Problem:** Several document variants share identity, lifecycle, and common access patterns.
- **Use when:** Queries span variants or variants share relationships.
- **Model:** One collection with a required discriminator and variant-specific fields. Validate variants explicitly, for example using `$jsonSchema` with `oneOf`.
- **Avoid when:** Variants have unrelated lifecycles, access rules, or query patterns.
- **Example:** `vehicles` with `type: "car" | "truck"` and type-specific fields.

## Outlier Pattern

- **Problem:** A small number of documents have much larger arrays/sets than typical records.
- **Use when:** Most documents are bounded but exceptional records would exceed the intended document bound.
- **Model:** Keep the common portion in the primary document and move overflow entries to a separate collection keyed by parent ID.
- **Avoid when:** The model is unbounded for most records; use a separate child collection directly.

## Tree Modeling

- **Problem:** Hierarchical reads need more than a simple parent lookup.
- **Options:** Parent reference for frequent parent/child traversal; materialized path or ancestor IDs for frequent subtree/ancestor queries; bounded embedding for small fixed trees.
- **Required contract:** Define subtree queries, move frequency, consistency/update cost, maximum depth, and cycle prevention.
- **Avoid when:** The query pattern does not justify maintaining duplicated paths or arrays.

## Example

Subset and extended-reference examples identify which values are copied and where the source remains authoritative:

```javascript
const customerView = {
  _id: ObjectId("65a000000000000000000001"),
  customerId: ObjectId("65a000000000000000000002"),
  customerSummary: { displayName: "Example Customer", tier: "gold" },
  recentOrders: [
    {
      orderId: ObjectId("65a000000000000000000010"),
      placedAt: ISODate("2026-10-20T10:00:00Z"),
    },
  ],
};
```

The customer record remains the source of truth for `displayName` and `tier`; the embedded summary needs an explicit propagation or staleness policy. `recentOrders` must have a fixed retention/count bound.

## Output Mapping

For every applied pattern, record the triggering access pattern, source of truth, read/write trade-off, consistency/staleness contract, size/cardinality bound, maintenance, and repair strategy. Omit `Design Patterns` when plain embedding/reference is sufficient.
