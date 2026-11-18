# Design Rules: Relational Stores

These are defaults, not substitutes for project conventions or the selected database's documentation. Verify engine/version-specific behavior before relying on an index, constraint, type, lock, or online operation.

## 1. Model and Normalize

- Start from sourced entities, attributes, cardinality, optionality, ownership, lifecycle, and operations.
- Model relationships explicitly. Use an association table for many-to-many relations unless requirements justify another design.
- Preserve sound existing normalization. Analyze functional dependencies and update anomalies when adding or duplicating facts.
- Denormalize only for a named access pattern or clear domain need. Record source of truth, update/repair mechanism, consistency window, and write cost.
- Do not persist derived values without an access, snapshot, audit, or history requirement.

## 2. Fields and Types

For every added/changed field, define name/path, meaning, type/precision, nullability, default/generation, constraints, and existing-data treatment.

- Distinguish null, empty, zero, missing, and unknown.
- Choose money, time, identifier, and measurement types from domain needs and project conventions; do not guess precision, timezone, or units.
- For a lifecycle, identify the canonical state representation and check allowed values and transitions.
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

- Start from named access patterns: predicates, joins, ordering, pagination, projections, scale, and scan tolerance.
- Reuse an index only after checking ordered keys, expression/collation, predicate, included columns, and engine semantics.
- For common B-tree patterns, equality columns often precede sort/range columns; verify the actual engine and query.
- A leading-prefix index may be redundant, but uniqueness, predicates, ordering, included columns, type, or workload may justify both.
- Every new index names the operation or invariant it supports and justifies write, storage, maintenance, and build cost.
- Define unique, partial, expression, covering, and specialized index options precisely and verify support.
- Consider update/delete/FK checks as well as reads. Do not claim plan validation without inspecting a plan.

## 6. Change Safety

- Classify compatibility with existing data, consumers, and old/new app versions.
- Audit data before adding non-null, unique, restrictive, or type constraints.
- Apply [rollout and recovery checks](change-classification.md#2-breaking-changes-expand--migrate--contract) when the change affects existing data or supported versions.
- Consider transaction duration, table rewrites, replication lag, and deployment order.
- For changes across stores, use a documented alternative such as outbox/saga/compensation when one transaction cannot cover them.

## Official References

- [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes-intro.html)
- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
