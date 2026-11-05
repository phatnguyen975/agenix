# SQL Multi-Tenancy

Choose an isolation model only when a system serves multiple tenants. Separate logical data ownership from operational and security isolation.

## Models

| Model                          | Isolation Characteristics                                                                                       | Cost / Limitation                                                                            | Use When                                                                                                                                     |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Database per tenant            | Distinct database namespace; a dedicated instance/cluster provides a stronger resource and operational boundary | More provisioning, migration, backup, monitoring, and cross-tenant reporting work            | Few tenants or strong isolation/customization is required; choose dedicated infrastructure when the threat or residency boundary requires it |
| Schema per tenant              | Separate namespaces and grants in one database                                                                  | Catalog growth and schema-wide migration management; shared instance resources               | Moderate tenant count with controlled structural variation                                                                                   |
| Shared tables with `tenant_id` | Logical row-level separation                                                                                    | Every access path must enforce tenant scope; noisy-neighbor and operational isolation remain | Many small tenants with a uniform schema                                                                                                     |

No model is automatically compliant or secure. Confirm the threat model, tenant count/growth, customization, data residency, recovery, and cross-tenant reporting requirements.

## Shared Table Integrity

- Every tenant-owned table has `tenant_id NOT NULL` using the tenant key's type.
- Business uniqueness is tenant-scoped where appropriate (`UNIQUE (tenant_id, email)`). Do not make a business key global unless the domain says so.
- Prevent cross-tenant references with composite foreign keys: parent `(tenant_id, id)` must be unique; child `(tenant_id, parent_id)` references it.
- Include `tenant_id` in indexes when access patterns consistently scope by tenant and the prefix improves those patterns. Do not force it into every index without checking actual query shapes.
- Define how tenant deletion, export, legal hold, and archival operate across owned tables.

## Row-Level Security

- PostgreSQL row-level security (RLS) can provide defense in depth for shared tables. Define policies for both row visibility (`USING`) and allowed new row values (`WITH CHECK`).
- Table owners normally bypass RLS; superusers and roles with `BYPASSRLS` bypass it regardless. `FORCE ROW LEVEL SECURITY` subjects the owner to policies but does not constrain superusers or bypass roles.
- The application role should not own tenant tables and should not have `BYPASSRLS`.
- If a pooled connection uses a custom setting (for example, `current_setting('app.tenant_id', true)`) to identify the tenant, set it transaction-locally and contain it safely. The value must come from trusted authentication middleware, never directly from an untrusted request field.
- A custom PostgreSQL setting is mutable by a role that can execute SQL; it is application context, not an unforgeable credential. RLS based on such a setting protects against omitted tenant predicates, but does not by itself contain arbitrary SQL execution or a compromised application role that can change the setting. Include this limitation in the threat model.
- Where the threat model includes arbitrary SQL under the shared runtime identity, do not present a caller-set custom setting as the sole tenant security boundary. Evaluate per-tenant database identities or stronger physical isolation, and restrict the ordinary role's access to trusted database entry points where feasible.
- Cross-tenant support/reporting should use a separately authorized and audited path, not casually grant bypass to the ordinary application role.
- RLS does not replace application-level authorization, secure tenant identity propagation, or correct composite foreign keys.

## Example

A tenant-scoped reference uses a composite key so a child cannot point to another tenant's parent:

```sql
CREATE TABLE projects (
  tenant_id uuid NOT NULL,
  id bigint NOT NULL,
  PRIMARY KEY (tenant_id, id)
);

CREATE TABLE tasks (
  tenant_id uuid NOT NULL,
  id bigint NOT NULL,
  project_id bigint NOT NULL,
  PRIMARY KEY (tenant_id, id),
  FOREIGN KEY (tenant_id, project_id) REFERENCES projects (tenant_id, id)
);
```

The tenant identifier must be supplied from a trusted authenticated context, not accepted as authority from an untrusted request field.

## Output Mapping

- `Tenant Isolation`: selected isolation model, tenant-owned tables, key scope, relationship restrictions, and explicitly authorized cross-tenant operations.
- `Security and Data Protection > Row-Level Security`: policy behavior, source of trusted tenant context, and owner/bypass/custom-setting limitations.
