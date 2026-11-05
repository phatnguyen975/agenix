# SQL Constraints

Map confirmed business invariants to reliable relational mechanisms. Examples use PostgreSQL; verify equivalent capabilities and syntax in the selected engine or version.

## Mechanism Selection

| Rule                           | Primary Mechanism                                                                                            | Limits / Decision Point                                                           |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| Mandatory scalar attribute     | `NOT NULL`                                                                                                   | A `CHECK` alone does not reject NULL/UNKNOWN results.                             |
| Value or same-row relationship | `CHECK`                                                                                                      | Use only deterministic row-local expressions.                                     |
| Uniqueness                     | `PRIMARY KEY`, `UNIQUE`, or unique partial index                                                             | Define the business scope and NULL semantics.                                     |
| Referential integrity          | `FOREIGN KEY`                                                                                                | The referenced key must be unique.                                                |
| Non-overlapping periods        | Exclusion or temporal constraint                                                                             | Select range semantics and concurrency-safe period identity.                      |
| State transition               | Conditional update or trigger                                                                                | A row check cannot compare `OLD` with `NEW`.                                      |
| Cross-row invariant            | Suitable declarative constraint; otherwise transaction-safe locking/serialization or application enforcement | A trigger that merely reads other rows may race unless concurrency is controlled. |
| Derivation                     | Query/view or row-local generated column; maintained summary only when justified                             | A generated column cannot aggregate other rows.                                   |
| Authorization                  | Database privileges and row-level security where appropriate, plus application authorization                 | A data-shape constraint is not an authorization check.                            |

Use the strongest reliable declarative mechanism available. Where the DBMS cannot enforce the rule, name the application-owned enforcement point and explain how concurrent requests cannot violate it.

## Primary Key and Unique

- Give each table one declared primary key. It is unique and non-null and creates a unique index.
- Treat identifiers as immutable. Never use identity/sequence values as gap-free business numbering.
- Add unique constraints for stable business keys, scoped correctly (for example, `(tenant_id, email)`).
- Use a partial unique index when uniqueness applies only to a subset, such as active rows.
- Specify whether multiple NULLs are distinct or equal; confirm the selected DBMS behavior.

## Foreign Key

- Represent relational references with foreign keys wherever possible. The referenced columns must be a primary/unique key supported by the engine.
- Choose deletion behavior from domain ownership and retention: `NO ACTION`/`RESTRICT` to prevent invalid orphaning, `CASCADE` only for true dependents, `SET NULL` only for optional relationships, and `SET DEFAULT` only with a valid designated parent.
- In PostgreSQL, `NO ACTION` can be deferred when the constraint is deferrable; `RESTRICT` is checked immediately.
- Keep referenced identifiers immutable where possible. State non-default update behavior only when the domain requires it.
- For composite foreign keys, define the intended NULL matching behavior. PostgreSQL's default `MATCH SIMPLE` permits a row to escape the check when any referencing column is NULL; `MATCH FULL` requires all referencing columns to be NULL or all to match.
- Index the referencing side only when joins, child lookup, or parent deletion/key update cost justifies it (`indexing.md`). PostgreSQL does not create that index automatically.

## Check Constraints

- Use for same-row ranges, allowed values, format, and cross-column consistency (for example, `quantity > 0`, `end_at > start_at`, or `status IN ('draft', 'paid', 'shipped')`).
- Do not query other tables, inspect other rows, or rely on volatile/time-dependent expressions inside a PostgreSQL `CHECK`.
- A `CHECK` expression that evaluates to NULL is not a violation. Pair it with `NOT NULL` when absence is forbidden.
- Do not reference a mutable user-defined function whose behavior can change without revalidating stored rows.

## Temporal and Exclusion Constraints

Use an overlap rule when the domain prohibits two records from occupying the same resource/time range.

PostgreSQL examples:

```sql
ALTER TABLE reservations
  ADD CONSTRAINT no_room_time_overlap
  EXCLUDE USING gist (room_id WITH =, during WITH &&);
```

For scalar equality plus range overlap, the required operator class may need `btree_gist`; list the extension only when the selected definition requires it.

PostgreSQL 18 also supports temporal keys such as:

```sql
PRIMARY KEY (room_id, during WITHOUT OVERLAPS)
FOREIGN KEY (room_id, PERIOD during) REFERENCES room_availability (room_id, PERIOD valid_during)
```

Use these only when their semantics match the domain and the target version supports them. Define half-open/inclusive interval boundaries, timezone basis, open-ended periods, and allowed gaps/overlaps.

## Deferrable Constraints

- Use deferred checking only when a valid transaction temporarily violates a relationship while completing a multi-statement change (for example, a circular reference or coordinated key swap).
- PostgreSQL supports deferrability for primary key, unique, foreign key, and exclusion constraints; `CHECK` and `NOT NULL` are not deferrable.
- Do not use deferral to conceal an invalid intermediate/final model.

## Triggers and Cross-Row Rules

- Use triggers only when a declarative constraint cannot express a confirmed rule and the trigger can preserve correctness under concurrent writes.
- Define trigger timing, events, affected rows, lock/serialization strategy, and error behavior.
- A deferred constraint trigger can validate a rule at transaction end, but a trigger that reads a changing set of rows still needs a concurrency strategy (for example, locking a stable parent row or serializable transactions).
- Keep trigger logic deterministic and local. Never perform external side effects from a trigger; use an application/outbox workflow for those.

## Generated Columns

- Use a generated column only for a deterministic expression over columns in the same row. It cannot aggregate across records or query another table.
- PostgreSQL 18 supports stored and virtual generated columns; virtual is the default. Choose based on read/write cost, storage, expression restrictions, and target DBMS capability.
- PostgreSQL generation expressions require immutable functions. Virtual generated columns have additional restrictions on user-defined functions/types.
- Do not assume a generated column replaces a cross-row summary or that every engine supports the same indexing/replication behavior.

## Output Mapping

- `Tables > Table-Level Constraints`: every primary, unique, foreign-key, check, exclusion, or temporal constraint with name, columns, rule, and referential action.
- `Business Rules`: map each `BR-nn` to its authoritative constraint, trigger, transaction-safe application path, or authorization mechanism.
- In the `Design Summary` table, use the `Required Extensions and Capabilities` property to list extensions only when the chosen definition depends on them.
