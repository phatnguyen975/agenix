# NoSQL Security

Design authorization boundaries, least-privilege access, sensitive-field handling, and trusted write paths. Tenant isolation is covered in `multi-tenancy.md`.

## Trust Boundaries

- Identify actors and services that can read, insert, update, delete, administer, export, or decrypt each data category.
- Treat client-supplied identifiers, tenant context, filters, update operators, and integration payloads as untrusted until validated and authorized.
- Use fixed, allowlisted update shapes; do not pass arbitrary client-supplied query/update documents directly to the database.
- Separate controls enforced by the database from controls enforced by the application, infrastructure, and operations.

## Roles and Privileges

- Define separate least-privilege roles for application runtime, read-only/reporting, background workers, migrations, and administration as needed.
- The runtime role must not have cluster/database administration or user-management privileges unless explicitly required.
- Grant only necessary database/collection actions. Avoid broad built-in roles when narrower custom roles satisfy the use case.
- MongoDB RBAC controls resources and actions; it does not provide automatic row-level filtering by tenant or per-document business authorization.
- Keep credentials and encryption keys outside the data model. Specify rotation and secret ownership as deployment dependencies when they affect the design.

## Sensitive Fields

- Classify sensitive fields using supplied policy. If absent, mark classification `Not specified`; do not infer legal categories or retention obligations.
- Minimize collection of personal/sensitive data and avoid copying it into denormalized snapshots unless required.
- Never store plaintext passwords. Store adaptive password hashes produced by a dedicated authentication-layer scheme; do not use a fast general-purpose hash.
- Consider client-side field-level encryption or queryable encryption only when the threat model and query requirements justify the complexity. Identify which fields can be queried, indexed, sorted, or aggregated under the selected encryption mode. MongoDB time-series collections do not support client-side field-level encryption; keep fields requiring that capability in a supported collection or choose another protection design.
- Encryption at rest, TLS, key management, backups, and secret rotation are deployment controls. Record dependencies without presenting them as document-schema capabilities.
- Define masking/redaction for logs, analytics, exports, and error payloads. A view or application projection is not a substitute for authorization.

## Example

A trusted application derives the tenant predicate from the authenticated principal and combines it with the requested object identity:

```javascript
const tenantId = authenticatedPrincipal.tenantId;
const invoice = await invoices.findOne({
  _id: requestedInvoiceId,
  tenantId,
});
```

The client must not be allowed to replace `tenantId` or provide an arbitrary database filter. Database RBAC still controls which collections and operations the service credential can access.

## Output Mapping

In `Security and Data Protection`, map actors to database roles/actions and application authorization rules; list sensitive fields and protection; identify tenant-context trust source; document encryption/query trade-offs, audit requirements, and deployment dependencies. Put document-level decisions in `Security and Data Protection > Application Authorization` and tenant-specific model decisions in `Tenant Isolation`.
