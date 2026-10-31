# Design Rules: Relational Stores

These are defaults, not substitutes for project conventions or the selected database's documentation. Verify engine/version-specific behavior before relying on an index, constraint, type, lock, or online operation.

## 1. Model and Normalize

- Start from sourced entities, attributes, cardinality, optionality, ownership, lifecycle, and operations.
- Model relationships explicitly. Use an association table for many-to-many relations unless requirements justify another design.
- **Use 3NF by default:** atomic attributes (1NF), full-key dependency (2NF), and no transitive non-key dependency (3NF).
- Denormalize only for a named `AP-xx` or clear integrity/workload need. Record source of truth, update/repair mechanism, consistency window, and write cost.
- Do not persist derived values without an access, snapshot, audit, or history requirement.

## 2. Fields and Types

For every added/changed field, define name/path, meaning, type/precision, nullability, default/generation, constraints, and existing-data treatment.

- Distinguish null, empty, zero, missing, and unknown.
- Choose money, time, identifier, and measurement types from domain needs and project conventions; do not guess precision, timezone, or units.
- Use one canonical status field for a lifecycle, not overlapping booleans. Define allowed values in Section 7.
- A default does not necessarily backfill existing rows; verify engine behavior.

## 3. Keys and Relationships

- Follow the existing primary-key strategy; verify uniqueness, stability, and mutability.
- For foreign keys, identify the target key and relevant delete/update behavior. Derive cascade/restrict/set-null behavior from requirements.
- Check FK nullability and whether referencing-side indexes are needed; engines differ on automatic index creation.
- If a DB foreign key is unsuitable (cross-store, polymorphic, legacy), state the reason and alternative integrity mechanism.
- Define business uniqueness scope, columns, predicate, collation/case, and null behavior.
- Use check/domain/enum constraints for supported row-local rules. Do not assume a row-level check enforces cross-row invariants.

## 4. Constraints and Concurrency

For every invariant, state source, condition, scope, enforcement point, violation behavior, and race/concurrency implications.

Prefer database enforcement where reliable. Check current data before tightening constraints. A read-before-write check can race; define isolation, locking, conditional writes, or a unique constraint as appropriate.

## 5. Index Design

- Start from named `AP-xx` patterns: predicates, joins, ordering, pagination, projections, scale, and scan tolerance.
- Reuse an index only after checking ordered keys, expression/collation, predicate, included columns, and engine semantics.
- For common B-tree patterns, equality columns often precede sort/range columns; verify the actual engine and query.
- A leading-prefix index may be redundant, but uniqueness, predicates, ordering, included columns, type, or workload may justify both.
- Every new index names its AP and justifies write, storage, maintenance, and build cost.
- Define unique, partial, expression, covering, and specialized index options precisely and verify support.
- Consider update/delete/FK checks as well as reads. Do not claim plan validation without inspecting a plan.

## 6. Change Safety

- Classify compatibility with existing data, consumers, and old/new app versions.
- Audit data before adding non-null, unique, restrictive, or type constraints.
- For breaking changes, plan expand/migrate/contract when suitable; state version compatibility, locks/build behavior, rollback limits, and irreversible points.
- Consider transaction duration, table rewrites, replication lag, and deployment order.
- For changes across stores, use a documented alternative such as outbox/saga/compensation when one transaction cannot cover them.

## 7. Anti-Patterns

| Pattern                                      | Better default                                                                                         |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Delimited lists                              | Child/association table when values need independent access or integrity.                              |
| Numbered columns (`item1`, `item2`)          | Child table or bounded structured value.                                                               |
| EAV for known attributes                     | Typed columns; use EAV only for genuinely open-ended attributes with explicit query/validation design. |
| Polymorphic IDs across unrelated tables      | Explicit associations or documented application integrity.                                             |
| Table/column per year or category            | Value/partitioning design supported by workload and engine.                                            |
| Multiple booleans for one lifecycle          | One status field and transition rules.                                                                 |
| Duplicated derived columns without ownership | Normalize or define source of truth, propagation, and repair.                                          |

## Official References

- [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes-intro.html)
- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
