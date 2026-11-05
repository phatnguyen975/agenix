# SQL Modeling Patterns

Use these patterns only when the domain shape or access patterns justify them. Core relationship placement is covered in `relationships.md`.

## Subtype Modeling

| Pattern         | Structure                                                                     | Prefer When                                                                                | Main Trade-off                                                              |
| --------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| Single table    | One relation with a discriminator and nullable subtype attributes             | Subtypes share most attributes and are commonly queried together                           | Sparse columns and subtype-specific constraints                             |
| Class table     | Base relation plus one relation per subtype; subtype PK is also an FK to base | Subtypes have substantial attributes or distinct constraints while shared identity matters | Joins for complete subtype reads; ensure exactly-one subtype where required |
| Concrete tables | One complete relation per concrete subtype                                    | Subtypes are independent and polymorphic queries/references are not needed                 | Duplicated shared columns and difficult cross-subtype uniqueness            |

- Make the discriminator explicit and constrain allowed values.
- For single-table designs, add checks tying subtype-specific columns to the discriminator; distinguish "not applicable" from "unknown".
- For class-table designs, a shared PK/FK guarantees subtype row belongs to a base row, but does not by itself guarantee every base row has exactly one subtype. Add a safe lifecycle/constraint strategy when total participation is required.
- Avoid vendor-specific table inheritance as a substitute for an explicit relationship model.

## Temporal Modeling

- Separate valid time (domain-effective interval) from transaction time (when the database recorded the version).
- Use explicit `valid_from`/`valid_to` or a range type for interval semantics. Define inclusive/exclusive boundaries, open-ended intervals, timezone, and whether zero-length intervals are valid.
- Prevent overlapping periods per business key when overlap is forbidden. PostgreSQL 18 supports temporal `WITHOUT OVERLAPS` constraints for supported range keys; otherwise use an exclusion constraint or a concurrency-safe alternative.
- Do not use an audit timestamp as a substitute for business validity.

## Ordered Child Rows

- Add a `position` attribute only when users define an order independent of business attributes.
- Scope uniqueness to the parent, such as `UNIQUE (parent_id, position)`. Define how reorder operations avoid transient uniqueness conflicts (for example, a deferrable constraint where supported or a two-phase position update).
- If chronology or a domain sequence already determines order, use that attribute instead.

## Semi-Structured Columns

- Use `jsonb` for genuinely variable or externally supplied payloads when the payload is not a substitute for modeled entities.
- Promote fields to typed columns when they participate in identity, referential integrity, frequent filters/joins, sorting, uniqueness, or business invariants.
- Validate the required shape and critical keys; document schema evolution and unknown-field behavior.
- Choose JSONB GIN or expression indexes only for known predicates. Avoid broad indexing of payloads without measured/query-driven need.
- Use arrays only for bounded, value-like collections with no independent identity or relationship lifecycle. Use child tables for entities, unbounded lists, or independently queried members.

## Example

A class-table subtype shares the base identity through a primary-key/foreign-key pair:

```sql
CREATE TABLE payments (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  payment_type text NOT NULL
);

CREATE TABLE card_payments (
  payment_id bigint PRIMARY KEY REFERENCES payments(id),
  card_token_reference text NOT NULL,
  authorization_code text
);
```

This enforces that each card-payment row has a base payment; it does not by itself guarantee that every base payment has exactly one subtype row.

## Output Mapping

In the conditional `Design Patterns` section, record each applied pattern, the entities/tables affected, why alternatives do not fit, the invariants and constraints it requires, and the `AP-nn` access patterns affected. Map detailed columns and constraints in `Tables`; define business rules in `Business Rules`. Omit `Design Patterns` when no specialized pattern applies.
