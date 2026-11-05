# NoSQL Relationships

Choose embedding or references from query patterns, cardinality, lifecycle, growth, consistency, and atomicity. A document database does not provide relational foreign-key enforcement by default.

## Decision Criteria

| Prefer Embedding When                                    | Prefer a Reference When                                            |
| -------------------------------------------------------- | ------------------------------------------------------------------ |
| Data is read with its parent in the same access patterns | Related entity is independently read, updated, or shared           |
| Child cardinality and total size are predictably bounded | Cardinality or size can grow without a reliable bound              |
| Parent and child share lifecycle/ownership               | Records have different lifecycle, retention, or authorization      |
| Single-document atomicity is valuable                    | Independent writes or cross-parent reuse are common                |
| Duplication has low update cost                          | Duplicated values change frequently or must be globally consistent |

- Do not embed by default. Select the model for dominant and important secondary access patterns, including write and lifecycle operations.
- Embed bounded one-to-one and one-to-few values when they are owned by and commonly read with the parent.
- Reference high-cardinality, independently accessed, shared, or unbounded entities. A child collection with `parentId` is often preferable for one-to-many growth.
- If a child is always owned by one parent but is unbounded, store child documents separately and index the parent reference; ownership does not require physical embedding.
- Treat duplication as a consistency decision: identify canonical source, copied fields, acceptable staleness, and update/repair path.

## Relationship Patterns

### One-to-One

- Embed a small dependent value when it shares lifecycle and is usually read with the owner.
- Use a separate document with a unique owner reference when independently accessed or separately secured; enforce one-to-one with a unique index on the owner key.

### One-to-Many

- Embed a bounded child array when the full child set is normally read/updated atomically with the parent and remains within size limits.
- Store children separately with `parentId` when the set can grow, is paginated, or is queried independently. Index the reference for actual parent-to-child queries.

### Many-to-Many

- Use references on both sides or an association collection when both entities have independent lifecycles or the relationship has attributes.
- Embed bounded ID arrays only when one direction dominates, membership changes are controlled, and duplicate/update costs are acceptable. Define reverse lookup.
- Model relationship attributes (`role`, `joinedAt`, `quantity`, status) on an explicit association document rather than parallel arrays.

### Self-Referential and Hierarchical

- Embed a small bounded hierarchy when read as one aggregate and updates fit one-document atomicity.
- Use parent references, ancestor arrays, or materialized paths only after defining traversal/query patterns and update cost. Maintain copied paths when nodes move.

### Polymorphic References

- Prefer a common collection/supertype when target types share identity and lifecycle.
- For heterogeneous references, use an explicit pair such as `{ targetType, targetId }`, validate allowed types, and document application-level referential-integrity checks.
- Never use arbitrary collection names supplied by clients as polymorphic targets.

## Reference Integrity

- Document source of truth, target type, identifier type, requiredness, delete behavior, and orphan-repair policy for every reference.
- Because references are not foreign keys, enforce existence/lifecycle rules in a trusted service, or in a multi-document transaction when atomicity is required and supported.
- Use unique indexes for cardinality that must be enforced (for example, one profile per user).
- Avoid DBRefs as the default; explicit application-level references make access patterns and consistency rules clearer.

## Examples

Bound embedded children:

```javascript
{
  _id: ObjectId("65a000000000000000000001"),
  customerId: ObjectId("65a000000000000000000002"),
  shippingAddress: { city: "Da Nang", countryCode: "VN" },
  items: [
    { productId: ObjectId("65a000000000000000000003"), quantity: 2 }
  ]
}
```

Unbounded children in a separate collection:

```javascript
{
  _id: ObjectId("65a000000000000000000010"),
  orderId: ObjectId("65a000000000000000000001"),
  eventType: "packed",
  occurredAt: ISODate("2026-10-10T08:00:00Z")
}
```

## Output Mapping

In `Relationships`, record cardinality, chosen storage pattern, rationale, source-of-truth/copy policy, indexes, integrity enforcement, delete behavior, and growth bound. Link each pattern to consuming `Access Patterns` IDs.
