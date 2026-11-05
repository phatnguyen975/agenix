# NoSQL Multi-Tenancy

Choose tenant isolation, database/collection boundaries, tenant-aware uniqueness, and authorization from isolation requirements, scale, operations, and query patterns.

## Isolation Models

| Model                              | Isolation                                                              | Trade-offs                                                                                                                                              |
| ---------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Shared collections with `tenantId` | Logical separation in every document                                   | Low operational overhead; every read/write path must enforce tenant scope                                                                               |
| Database per tenant                | Database namespace and privilege boundary                              | Stronger logical separation/customization; higher provisioning, connection, index, and operations cost                                                  |
| Dedicated cluster per tenant       | Separate deployment and resource/operational boundary                  | Highest cost and operational overhead; use for strong isolation, residency, or resource-control requirements                                            |
| Collection per tenant (avoid)      | Separate collection namespace per tenant in one database               | MongoDB documentation advises against this pattern at scale because namespace, index, and operational overhead grow; use only for a justified exception |
| Hybrid                             | Shared model for most tenants, isolated resources for selected tenants | Flexible but requires explicit routing and lifecycle policy                                                                                             |

- A separate database or collection does not automatically provide complete security; roles, administrative access, backups, and application routing still matter.
- Select the model from isolation requirements, tenant count/size skew, noisy-neighbor risk, customization, migration, and operational limits.

## Shared Collection Rules

- Every tenant-owned document carries a non-null tenant identifier with one consistent BSON type.
- Derive tenant identity from trusted authentication/session context; never trust a tenant ID supplied only by the request body or query parameters.
- Include tenant scope in every tenant-owned read, update, delete, and uniqueness invariant. Centralize enforcement and test negative cross-tenant cases.
- Use compound unique indexes such as `{ tenantId: 1, externalKey: 1 }` when uniqueness is per tenant. Use a global unique index only when global uniqueness is explicitly required and shard restrictions permit it.
- Include `tenantId` in a compound index when it supports a real tenant-scoped query, sort, or uniqueness rule. Do not force it to lead every index without considering query shapes.
- For references between tenant-owned documents, enforce same-tenant ownership in the trusted write path or transaction. A reference alone does not prove tenant equality.

## Authorization and Operations

- MongoDB RBAC grants actions on database/collection or cluster resources; it does not provide automatic row-level tenant predicates. Shared-collection tenant isolation therefore requires a trusted application boundary or physical isolation.
- Do not expose broad administrative credentials to application code. Use least-privilege roles and separate migration/operations identities.
- Define tenant onboarding, suspension, export, deletion, retention, backup/restore, and migration behavior.
- If tenants can move between shared and isolated models, define routing metadata and a consistency-safe migration procedure.

## Sharding Considerations

- A tenant key may help targeted routing for tenant-scoped workloads, but tenant skew or monotonic keys can create hotspots depending on shard-key design.
- Validate shard-key cardinality, value frequency, write distribution, query targeting, and tenant size skew before choosing a key (`sharding.md`).
- Unique indexes on a sharded collection generally must have the shard key as a prefix. Align tenant-scoped uniqueness with the actual shard key and target server restrictions.

## Example

A shared-collection document and per-tenant key make scope explicit:

```javascript
{
  _id: ObjectId("65a000000000000000000001"),
  tenantId: ObjectId("65a000000000000000000099"),
  externalKey: "INV-1042",
  status: "open"
}

db.invoices.createIndex(
  { tenantId: 1, externalKey: 1 },
  { unique: true }
);
```

Every access path must derive the tenant ID from authenticated server context and include it in the predicate; the index does not authorize access.

## Output Mapping

In `Tenant Isolation`, record the isolation model, tenant identifier source/type, scope enforcement point, unique constraints, tenant-aware references, index rationale, administrative roles, lifecycle operations, and sharding implications. Identify cross-tenant access tests. Record database roles and application authorization separately in `Security and Data Protection`.
