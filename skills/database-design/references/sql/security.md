# SQL Security

Model data access, least privilege, sensitive attributes, and database-enforced boundaries. Tenant isolation is covered in `multi-tenancy.md`.

## Threat and Trust Boundaries

- Identify which actors and application components may read, insert, update, delete, administer, export, or decrypt each data category.
- Identify trust boundaries between clients, application services, background workers, integrations, administrators, and the database.
- Treat application input, tenant identifiers supplied by clients, background jobs, and integration payloads as untrusted until authenticated, validated, and authorized.
- Separate database-enforceable controls from application, infrastructure, and operational controls. Do not claim that a schema alone provides end-to-end security.

## Roles and Privileges

- Define roles by responsibility, such as schema owner/migration role, application writer, application reader, reporting reader, and narrowly scoped worker roles.
- The runtime application role must not be a superuser, object owner, or role with privilege escalation unless a documented requirement demands it.
- Grant only required schema, table, sequence, and column privileges. Revoke broad defaults where relevant; avoid granting write access to reporting or history consumers.
- Specify which role owns migrations and objects. Object ownership and role membership can bypass ordinary grants.
- Use row-level security only when row predicates are a required database boundary; define policies for every command and account for owner, superuser, and `BYPASSRLS` behavior. Consider `FORCE ROW LEVEL SECURITY` where table-owner enforcement is required.

## Sensitive Data

- Classify columns from supplied policy or domain requirements. If classification is unknown, mark it `Not specified` rather than inventing a label.
- Store the minimum data needed for the stated purpose. Do not add sensitive attributes merely because they may be useful later.
- Never store plaintext passwords. Passwords require a dedicated adaptive password-hashing scheme in the authentication layer; a fast general-purpose hash is insufficient.
- Use application-side or database-supported encryption only when threat model, query needs, key ownership, and rotation are defined. Encryption changes equality, ordering, search, indexing, and operational capabilities; document those consequences.
- Do not describe hashing, tokenization, masking, or pseudonymization as encryption or guaranteed anonymization.
- Masking views can provide a restricted projection, but do not treat obscured values as a substitute for correct privileges.
- TLS, disk encryption, backups, secrets management, and key custody are deployment controls. Mention them only as explicit dependencies, not as schema features.

## Example

A reporting role receives read access without ownership or write privileges:

```sql
CREATE ROLE reporting_reader NOLOGIN;

GRANT USAGE ON SCHEMA app TO reporting_reader;

GRANT SELECT ON app.orders, app.order_items TO reporting_reader;

REVOKE INSERT, UPDATE, DELETE ON app.orders, app.order_items FROM reporting_reader;
```

Role membership, object ownership, default privileges, and row-level policies must be reviewed together; this fragment is not a complete deployment security configuration.

## Output Mapping

In `Security and Data Protection`, map each actor/role to permitted operations and objects; list sensitive columns with confirmed classification and protection; identify row-level policies and trusted context source; and record security assumptions that require application or infrastructure enforcement.
