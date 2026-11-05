# SQL Conventions

Naming, identifiers, types, and null semantics. Apply project conventions first. Examples use PostgreSQL 18; other relational engines may differ in types, defaults, null handling, and feature support.

## Naming

- Use one consistent convention. Default to lowercase `snake_case`, unquoted identifiers, concise domain terms, and no reserved words.
- Respect the selected engine's identifier limits. PostgreSQL identifiers are limited to 63 bytes by default; do not depend on silent truncation.
- Use singular or plural table names consistently. Default to plural nouns for entity tables; name associative tables after the domain concept when one exists (`enrollments`) or combine entity names when it does not (`student_courses`).
- Do not use reserved words (`user`, `order`, `group` are reserved in PostgreSQL).
- Use singular column names. Prefer `id` for a table's primary key and `<referenced_entity>_id` for a foreign key. Prefix role names when referencing the same table more than once (`billing_address_id`, `shipping_address_id`).
- Use clear boolean names (`is_active`, `has_access`), `_at` suffix for timestamps, `_date` suffix for calendar dates, and consistent actor names (`created_by`, `updated_by`).

| Object            | Pattern                 | Example                             |
| ----------------- | ----------------------- | ----------------------------------- |
| Primary key       | `pk_<table>`            | `pk_orders`                         |
| Unique constraint | `uq_<table>_<columns>`  | `uq_users_email`                    |
| Foreign key       | `fk_<table>_<column>`   | `fk_orders_customer_id`             |
| Check constraint  | `ck_<table>_<rule>`     | `ck_order_items_quantity_positive`  |
| Index             | `idx_<table>_<columns>` | `idx_orders_customer_id_created_at` |
| Trigger           | `trg_<table>_<purpose>` | `trg_orders_status_transition`      |

## Identifiers

- Prefer an immutable primary key that is stable and compact.
- PostgreSQL default: `bigint GENERATED ALWAYS AS IDENTITY` for database-generated sequential identifiers. Identity values can have gaps and are not gap-free business numbers.
- Use UUID when identifiers must be generated independently, across services, or before database insertion. PostgreSQL 18 provides `uuidv7()`; its time ordering can improve index locality compared with random UUIDs. Do not use any identifier as an authorization secret.
- Do not use legacy `serial` or `bigserial` when identity columns are available.
- Keep a stable natural key as an alternate unique constraint when domain semantics require it. A composite primary key is valid when it is the true stable identity; do not introduce a surrogate only because the natural key has multiple columns.
- Associative tables commonly use a composite primary key of their foreign keys when a pair can occur only once. Add a discriminator or validity period when repeated relationships are allowed.

## Data Types

Choose the narrowest type that correctly represents the domain without creating brittle limits. Length, range, precision, and scale limits must come from requirements, not guesswork.

| Meaning                     | PostgreSQL Example                                                                         | Avoid                                                                                                                            |
| --------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| Variable text               | `text`                                                                                     | Fixed-width `char(n)` without a domain reason                                                                                    |
| Whole number                | `smallint`, `integer`, `bigint` by range                                                   | Storing numbers as text                                                                                                          |
| Exact decimal / money       | `numeric(p,s)` or integer minor units plus currency code                                   | `real`, `double precision` for exact arithmetic; avoid `money` when explicit currency, scale, or portable semantics are required |
| Approximate measurement     | `double precision` where measurement tolerance permits                                     | Exact arithmetic expectations                                                                                                    |
| Boolean                     | `boolean`                                                                                  | Text flags such as `'yes'` / `'no'`                                                                                              |
| Instant in time             | `timestamptz`                                                                              | `timestamp` (without time zone), `timetz`                                                                                        |
| Calendar date               | `date`                                                                                     | Midnight timestamps when no time semantics exist                                                                                 |
| Local wall-clock time       | `time` plus an IANA timezone where schedule semantics require it                           | Treating a recurring local schedule as a fixed UTC instant                                                                       |
| Duration                    | Numeric quantity with unit, or `interval` where calendar arithmetic semantics are intended | Assuming all months/days have a fixed number of seconds                                                                          |
| Binary                      | `bytea` for bounded payloads                                                               | Large file/blob storage without a size and access justification                                                                  |
| Variable structured payload | `jsonb` for genuinely variable/non-relational data                                         | Hiding stable relational facts in JSON                                                                                           |
| Range                       | A suitable range type (`tstzrange`, `daterange`, `int4range`)                              | Manually maintained interval boundaries without an overlap policy                                                                |
| Network address             | `inet` / `cidr`                                                                            | Unvalidated text                                                                                                                 |

- For case-insensitive uniqueness, use unique index on `lower(<column>)`, or the `citext` type (extension).
- For timestamps representing instants, use `timestamptz`; PostgreSQL stores an instant and renders it in the session timezone. UTC is the interchange convention, not a preserved source timezone.
- Store a calendar date as `date`. For local schedules, retain the local time and IANA timezone identifier so daylight-saving transitions are not lost.
- For money, store the currency explicitly when more than one currency is possible. Define rounding and scale from the domain. Never add unlike currencies without an explicit conversion rule.
- Use `numeric` for exact decimal quantities. Floating point is appropriate only when approximation is acceptable.
- Use standard code sets where the domain calls for them: ISO 4217 currency, ISO 3166-1 country, BCP 47 language tags, E.164 phone numbers, and ISO 8601 interchange formats. Validate the business semantics as well as superficial string shape.
- PostgreSQL character data uses the database encoding; UTF-8 is the preferred default for interoperable applications.

## Enumerations

- Use a closed enum or check constraint only for a small, stable set whose values change through controlled schema releases.
- Use a lookup table when values are data-managed, carry attributes, have their own lifecycle, or are shared across domains.
- Represent a mutually exclusive lifecycle with one status field rather than contradictory booleans (`is_paid`, `is_shipped`). Model independent facts as separate fields.

## Nullability and Defaults

- Use `NOT NULL` when absence is not a valid domain state. For nullable fields, state what `NULL` means.
- Do not use sentinel values (`0`, `'N/A'`, `'9999-12-31'`) to represent absence.
- Do not treat an empty string as `NULL`. Reject empty strings only when the domain requires it.
- Use a default only when the value is a true domain default or a technical default such as a generated identifier or creation instant. A default must not conceal missing input.
- PostgreSQL unique constraints treat NULL values as distinct by default; PostgreSQL 15+ supports `NULLS NOT DISTINCT` when nulls should compare equal. Confirm the chosen engine's semantics.
- `created_at timestamptz NOT NULL DEFAULT now()` is a PostgreSQL example. `now()` represents transaction start time; use a different clock only when the domain requires statement or wall-clock time.

## Example

A money amount and an event instant use types that express their domain semantics:

```sql
CREATE TABLE invoices (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  invoice_number text NOT NULL UNIQUE,
  issued_on date NOT NULL,
  total_amount numeric(14, 2) NOT NULL CHECK (total_amount >= 0),
  currency_code text NOT NULL CHECK (currency_code ~ '^[A-Z]{3}$'),
  created_at timestamptz NOT NULL DEFAULT now()
);
```

The precision, scale, currency set, and identifier strategy must come from the actual domain contract; the values above are illustrative. The regular expression checks only the three-letter uppercase shape, not membership in the ISO 4217 set. Use a reference table or explicit allowlist when authoritative currency validation is required.

## Output Mapping

- `Design Summary`: concise naming, identifier, time, money, and type conventions that affect the model.
- `Tables`: each column's type, nullability, default/generation behavior, meaning, units, and NULL semantics.
- Example:

| Column       | Type          | Null | Default  | Description                              |
| ------------ | ------------- | ---- | -------- | ---------------------------------------- |
| `id`         | `bigint`      | No   | identity | Primary key                              |
| `email`      | `text`        | No   | —        | Login address, unique case-insensitively |
| `created_at` | `timestamptz` | No   | `now()`  | Creation instant (UTC)                   |
