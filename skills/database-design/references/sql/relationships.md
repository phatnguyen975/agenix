# SQL Relationships

Translate logical relationships into relational keys and constraints. Index design is covered in `indexing.md`; referential actions and constraint details are in `constraints.md`.

## Foreign Key Placement

- For a one-to-many relationship, place the foreign key on the many/child side.
- A mandatory relationship requires a non-null foreign key. An optional relationship permits `NULL`; define its meaning.
- A foreign key references a primary key or eligible unique key. Use a composite foreign key when the relationship is scoped by tenant or another parent key.
- A reference between relational tables should normally be represented by a foreign key, not only by a similarly named column.
- Choose `ON DELETE` behavior from ownership and lifecycle rules. Do not default every relationship to cascade. Choose `ON UPDATE` deliberately; immutable surrogate keys commonly use `NO ACTION`.
- A foreign key does not automatically create an index on its referencing columns in PostgreSQL. Evaluate the child-side index from joins, child lookup patterns, and the cost of parent deletes/updates (`indexing.md`).

## One-to-Many

The child holds one foreign key to the parent. Record whether the relationship is mandatory and whether the child can outlive the parent.

- Owned child that must be deleted with the parent: `ON DELETE CASCADE` may be appropriate.
- Independent child: `RESTRICT` / `NO ACTION`, archival, or nullable `SET NULL` may fit the domain.
- Do not use `SET NULL` on a mandatory foreign key.

## One-to-One

- Use a unique foreign key in the dependent table, or a shared primary key when the child identity is the parent identity.
- A foreign key alone enforces at most one child per parent when unique, but cannot always enforce mandatory participation on both sides. Merge the tables or design a reliable deferred/transactional enforcement strategy when that invariant is real.
- Keep the tables separate only when lifecycle, access, size, ownership, or sensitivity differs.

## Many-to-Many

- Use an associative/junction table with one foreign key to each side.
- Use a composite primary key when each pair can occur once. Add a surrogate or discriminator and a suitable unique constraint when the same pair may recur over time.
- Add the reverse lookup index only when the access pattern needs it; the primary-key index serves the leading key prefix, not every lookup direction.
- If the relationship has attributes or lifecycle, model it as a first-class entity (for example, `enrollments` with `grade` and `enrolled_at`).

## Dependent Entities

A dependent row has an explicit owner foreign key. The owner's key may participate in the child's primary key, but an independent child key is also valid. Use cascade only when deletion of the owner must delete the dependent and any retained-history requirements permit it.

## Multiple Relationships Between the Same Tables

Create one foreign key per domain relationship and name it by role (`billing_address_id`, `shipping_address_id`). Do not overload one foreign key to mean different relationships.

## Self-Referencing Relationships

- A tree commonly uses a nullable `parent_id` referencing the same table.
- A graph with several parents commonly uses a junction table.
- Define root behavior, cycle policy, maximum depth if bounded, and common traversal direction.
- A self-referencing foreign key prevents dangling parents but does not prevent cycles. Enforce acyclicity with a safe write strategy (for example, recursive validation under appropriate locking) or a carefully designed trigger.

| Pattern           | Structure                             | Strength                              | Cost / Constraint                 | Use When                                   |
| ----------------- | ------------------------------------- | ------------------------------------- | --------------------------------- | ------------------------------------------ |
| Adjacency list    | `parent_id`                           | Simple inserts and moves              | Recursive traversal for subtrees  | Default for mutable hierarchies            |
| Materialized path | `path` or PostgreSQL `ltree`          | Efficient path/prefix subtree queries | Moves rewrite descendant paths    | Read-heavy hierarchy with infrequent moves |
| Closure table     | `(ancestor_id, descendant_id, depth)` | Ancestor and descendant joins         | Additional rows and complex moves | Frequent arbitrary-depth traversal         |

## Polymorphic References

Avoid an unconstrained `target_type + target_id` pair when referential integrity matters. Alternatives include one nullable foreign key per target plus a check that exactly one is populated, or a shared supertype table referenced by one foreign key. Choose based on domain semantics, not convenience alone.

## Example

A many-to-many relationship with relationship attributes is an associative entity:

```sql
CREATE TABLE enrollments (
  student_id bigint NOT NULL REFERENCES students(id),
  course_id bigint NOT NULL REFERENCES courses(id),
  enrolled_at timestamptz NOT NULL,
  status text NOT NULL,
  PRIMARY KEY (student_id, course_id)
);
```

If a student can enroll in the same course more than once over time, the key must include the enrollment identity or period rather than assuming one pair is unique forever.

## Output Mapping

- `Entity Model` and `Relationships`: each relationship with cardinality, optionality, and ownership.
- `Tables > Table-Level Constraints`: every foreign key with referenced table/columns, nullability, and deletion behavior.
- `Indexes`: only the referencing-side indexes justified by workload or parent-side maintenance; map them to `Access Patterns` IDs.
