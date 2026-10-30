# Design Rules: Relational Stores

These are default design checks, not a substitute for the actual database engine's documentation. Project conventions and documented engine behavior take precedence. Do not infer that a feature (partial index, online index build, deferrable constraint, generated column, JSON operator, or lock mode) exists or behaves the same across engines.

## 1. Model from requirements and access patterns

- Start with sourced entities, attributes, cardinality, optionality, ownership, lifecycle, and operations. Do not create a table solely because a UI has a component or because a name appears in prose.
- Match existing types and key conventions for the same meaning. If conventions conflict, surface the conflict rather than inventing a new convention.
- Model each relationship with explicit cardinality and optionality. For many-to-many relationships, normally use an association table with foreign keys and an appropriate uniqueness rule. Use another design only when requirements and access patterns justify it.
- Keep attribute meaning stable. Avoid using a single generic column to hold different semantic kinds without an explicit, validated model.

## 2. Normalization and deliberate denormalization

- Use 3NF as the default for new relational entities unless a project standard or a demonstrated workload requires otherwise:
  - **1NF:** represent each attribute as a value with the engine's documented domain/type; avoid repeating groups and delimited lists that need independent filtering, integrity, or updates.
  - **2NF:** 1NF, and non-key attributes depend on the whole candidate key, not only part of a composite key.
  - **3NF:** 2NF, and non-key attributes do not depend transitively on another non-key attribute.
- Treat normalization as a default, not an absolute law. Denormalize only for a named `AP-xx` or a clear integrity/workload need. Record source of truth, update/repair mechanism, consistency window, and write amplification in Design Decisions.
- Do not store values that can be derived unless a source-backed access, snapshot, audit, or historical-consistency requirement justifies persistence.

## 3. Field and type definition

Every added or materially changed field needs:

- exact name/path and semantic meaning;
- database data type, precision/length/domain where meaningful;
- nullable/required semantics;
- default or generation rule, including whether the default is database- or application-generated;
- validation/constraints;
- treatment of existing rows and invalid legacy values.

**Rules:**

- Allow `NULL` only when “no value” is a valid business state. Do not equate NULL, empty string, zero, missing, and “unknown”; document the distinction required by the feature and engine.
- For amounts, counters, identifiers, timestamps, and measurements, select types based on domain and project convention; do not guess precision, timezone, or overflow behavior. Preserve original units/currency where relevant.
- Store one lifecycle in a single constrained status/state field rather than a collection of overlapping booleans. Keep its allowed values canonical in Section 7 of the Data Impact Document.
- Use a stable representation for enumerated values, time, money, identifiers, and audit metadata across related entities. If existing representations differ, document the discrepancy and ask when it changes correctness or interoperability.
- A default does not automatically backfill existing rows or make a change operationally safe. Confirm the engine/version's behavior and deployment sequence.

## 4. Keys and relationships

- Every entity needs a primary key or the project's explicitly documented equivalent. Follow the existing key strategy (surrogate, natural, composite, generated) and verify uniqueness, stability, and mutability.
- For each foreign key, specify the referenced candidate key and explicit `ON DELETE` / `ON UPDATE` behavior where supported and relevant. Derive cascade, restrict, set-null, or set-default behavior from requirements; never choose one silently.
- Assess nullability of all foreign-key columns and whether partial/null relationships are valid.
- Check whether referencing-side indexes are needed for joins, parent deletes/updates, and known queries; a foreign-key declaration does not guarantee that an index is created on the referencing columns in every engine.
- If a relationship cannot or should not be a database foreign key (cross-store boundary, polymorphic relation, legacy limitation), state the reason and the alternative integrity mechanism.
- Business uniqueness should be enforced by a unique constraint/index when the engine and model can express the requirement. Specify scope, columns, predicate, case/collation semantics, and null behavior as applicable.
- Use check/domain/enum constraints for closed value sets and row-local ranges when supported. Do not assume a row-level `CHECK` enforces cross-row or cross-table invariants; use the engine's appropriate supported mechanism and concurrency design.

## 5. Constraints and invariants

For every invariant, name:

1. the source and exact condition;
2. its scope (single field/row, multiple rows, entities, tenant, or system-wide);
3. enforcement point: database, application, both, or external process;
4. behavior on violation and whether any write can partially succeed;
5. concurrency/race considerations if the invariant depends on a read followed by a write.

Prefer database-enforced integrity for invariants the database can express reliably, but do not claim it is fully enforced when application-only logic or cross-store checks remain. Check whether adding a constraint could fail against existing data before classifying it or selecting a rollout.

## 6. Index design

- Start from the explicit read and write access patterns (`AP-xx`). For each pattern, record predicates, join keys, ordering, pagination, projected values where relevant, expected cardinality/frequency, and whether a full scan is acceptable.
- Reuse an existing index when it supports the required predicates and order. A similar index name is not proof of suitability; inspect the ordered keys, expression/collation, predicate, included columns, and engine semantics.
- For common B-tree composite patterns, equality predicates on leading columns commonly precede ordering/range needs, but the effective order depends on the engine, query operators, sort direction, collation, and planner behavior. Check official engine documentation; do not apply a fixed universal recipe.
- An index whose leading key prefix matches another index may be redundant, but uniqueness, different predicates, ordering, included columns, index type, and actual workload can justify both. State the reasoning rather than using a blanket redundancy rule.
- Each new index must name the AP it serves and justify its write, storage, maintenance, and build cost. Consider read selectivity and write amplification. Do not add an index “just in case.”
- For unique, partial/filtered, expression, covering/include, functional, or specialized indexes, state the full definition and confirm engine support. Include predicate and uniqueness semantics.
- Consider indexes used by updates/deletes, foreign-key checks, pagination, and ordering, not just `SELECT` filters.
- Document when plan/performance validation has not been run; a model-level assessment is not proof of runtime performance.

## 7. Change safety and concurrency

- Classify changes according to compatibility with existing data, old/new application versions, and consumers—not merely whether a statement is syntactically additive.
- Before adding non-null constraints, uniqueness, tighter checks, or type restrictions, identify and validate existing data. Give a deterministic backfill/cleanup rule or mark the decision blocked.
- For breaking changes, design expand → migrate → contract steps and specify which app/model versions are compatible at each step, rollback limits, and the point at which rollback is no longer safe.
- Consider engine-specific table locks, index-build blocking, rewrite behavior, transaction duration, replication lag, and deployment order. Never promise an online/non-blocking operation without confirming the exact engine/version/operation.
- For read-modify-write business rules, state the isolation/locking/conditional-write strategy and conflict behavior. A read-before-write check alone may race; database uniqueness and other constraints can still report conflicts under concurrency.
- Multi-table changes require a transaction or a documented alternative such as an outbox/saga/compensation strategy when atomicity cannot span the affected systems.

## 8. Anti-patterns to challenge

| Pattern                                           | Default concern                                             | Better default / exception handling                                                                                     |
| ------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Delimited lists in one column                     | Hard to validate, join, update, and index individual values | Association/child table when values have independent meaning; arrays/JSON only when access/integrity needs support them |
| Numbered columns such as `item1`, `item2`         | Repeating group and inflexible cardinality                  | Child/association table or a bounded structured value justified by requirements                                         |
| EAV for a known stable set of attributes          | Weak typing and awkward constraints/querying                | Normal columns; EAV only for genuinely open-ended attributes with explicit query and validation design                  |
| Polymorphic ID pointing at different tables       | No single enforceable FK and ambiguous ownership            | Explicit association tables, a shared parent model, or a documented application integrity contract                      |
| One table/column per year or category             | Schema proliferation and duplicated logic                   | A value/partitioning strategy supported by the actual engine and workload                                               |
| Several booleans representing one lifecycle       | Invalid combinations and unclear transitions                | One state field plus explicit transition rules                                                                          |
| Duplicate derived columns without ownership rules | Drift and repair complexity                                 | Normalize or define a source of truth, consistency mechanism, and reconciliation path                                   |

## Official references

- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) — examples of unique, foreign-key, check, and referential actions; engine-specific behavior.
- [PostgreSQL multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html) — leading-column behavior for B-tree and other supported index types.
- [PostgreSQL index overview](https://www.postgresql.org/docs/current/indexes-intro.html) — index selection and maintenance costs.
- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) — example of engine-specific concurrency and serialization behavior.
