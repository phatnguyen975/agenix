# Payload Conventions

## Scope

- Data-level conventions for any payload: HTTP bodies, GraphQL values, message data, and stream events.
- Project conventions override these defaults; when the project has none, apply them and record the choice.

## Naming

- One casing style per API surface for properties (`camelCase` or `snake_case`), applied everywhere including query parameters and headers where applicable.
- One concept, one name; the same field means the same thing in every operation.
- Names describe meaning, not storage (`customerId`, not `cust_fk`).
- Booleans are positive (`enabled`, not `disabled`); when more than two states are plausible, use an enum.
- Avoid abbreviations except universally understood ones (`id`, `url`).
- Units are in the field name or the schema description (`timeoutSeconds`, `sizeBytes`).

| Good             | Bad        | Rule                 |
| ---------------- | ---------- | -------------------- |
| `customerId`     | `cust_fk`  | Meaning, not storage |
| `enabled`        | `disabled` | Positive boolean     |
| `timeoutSeconds` | `timeout`  | Unit in the name     |

## Identifiers

- Opaque, stable, immutable strings; consumers never parse them.
- Identifiers are unique within their resource type and never reused after deletion.
- UUIDs: choose an appropriate version (for example v4 random or v7 time-ordered); use the canonical textual form. Do not expose UUID version as a security control.
- Sequential integer keys exposed to consumers invite enumeration; if used, authorize every access by object.
- Identifiers are JSON strings, even when numeric inside.
- Cross-resource references use the identifier plus, when helpful, a link.

## Time

- Instants: RFC 3339 `date-time` in UTC with `Z` (`2026-03-01T09:30:00Z`).
- Dates without time: `date` (`2026-03-01`); times without date: `time`.
- Durations: ISO 8601 (`PT15M`) or an integer with the unit in the name; pick one per surface.
- Time zones: IANA names (`Europe/Paris`) in a separate field when local time matters.
- Name fields by meaning: `createdAt`, `expiresAt`, `startDate`.
- Binary protocols use native timestamp types.

| Concept       | Good                                  | Bad                                               |
| ------------- | ------------------------------------- | ------------------------------------------------- |
| Instant       | `"2026-03-01T09:30:00Z"`              | `"03/01/2026 9:30"`, `1772357400` (unit unstated) |
| Date          | `"2026-03-01"`                        | `"1 March"`                                       |
| Duration      | `"PT15M"` or `"timeoutSeconds": 900`  | `"15"`                                            |
| Money         | `{"amount": 1250, "currency": "EUR"}` | `12.5`                                            |
| Large integer | `"9007199254740993"`                  | `9007199254740993`                                |
| Enum          | `"PAID"`                              | `2`                                               |
| Identifier    | `"ord_01HZX"`                         | `42` (sequential, guessable)                      |

## Numbers and Money

- Money: integer amount in minor units plus ISO 4217 currency code, or a decimal string plus currency code; never binary floating point.
- For JSON consumers that may parse numbers as IEEE 754 doubles, represent integers beyond 2⁵³ − 1 as strings to preserve precision. ProtoJSON maps 64-bit integers to strings for this reason.
- Percentages, ratios, and rates: state the scale (0–1 or 0–100) in the description.
- Quantities carry units; use SI units unless the domain dictates otherwise.
- State meaningful numeric bounds and precision where required by the domain, security, or resource constraints; do not invent arbitrary limits.

## Enums

- Use enums for closed sets that change rarely; use a reference resource for sets that change often.
- Values are stable strings in one casing style (`UPPER_SNAKE_CASE` or lowercase), not numeric codes.
- Declare whether new values may be added; consumers handle unknown values safely.
- Include an explicit "unknown" or "unspecified" value only where the format requires a zero value.

## Null, Absent, Empty

- Absent: not provided (request) or not applicable (response).
- `null`: explicitly no value; in JSON Merge Patch it clears the field.
- Empty string or array: a value that is empty.
- Define the meaning of each for every optional field; do not use `null` and absent interchangeably.
- Responses return the same fields on every call; omit only fields documented as conditional.
- Do not use sentinel values (`-1`, `""`) for missing data.

Example with JSON Merge Patch semantics:

| Request body     | Effect                         |
| ---------------- | ------------------------------ |
| `{"note": null}` | Clears `note`                  |
| `{}`             | Changes nothing                |
| `{"note": ""}`   | Sets `note` to an empty string |

## Text and Locale

- UTF-8 everywhere; lengths are measured in characters (code points) in JSON Schema and bytes in some binary limits; state which.
- Language tags: BCP 47 (`en-US`); country codes: ISO 3166-1 alpha-2; currency codes: ISO 4217.
- Free text fields have maximum lengths and a trimming policy.
- Decide where localization occurs. Prefer stable machine-readable codes and locale-neutral values; when the API returns localized text, document locale negotiation and `Content-Language`.

## Structure

- Prefer object envelopes for extensible JSON responses. A top-level scalar or array is not inherently invalid; use one only when it is the clearest stable representation and the project permits it.
- Collections are wrapped in a named property (`items`) with sibling metadata (`nextCursor`).
- Group related fields into nested objects (`address`, `money`) instead of prefixes.
- Limit nesting depth and total size; state both.
- For response payloads, document whether consumers must tolerate unknown fields; open response objects usually improve forward compatibility. For request payloads, reject or ignore unknown fields deliberately and consistently; closed write schemas are often safer against mass assignment.
- No behavior-changing flags hidden in boolean fields; model modes explicitly.

## Binary Data

- Small binary values in JSON: base64 (RFC 4648) with `contentEncoding`.
- Large or streamed binary: separate upload or download operation, not embedded in JSON.
- Declare media type and maximum size for every binary field.

## Anti-Patterns

- Floating-point money; local time without zone; epoch numbers without unit.
- Numeric enum codes as the public contract.
- Mixed casing; synonyms for the same concept.
- Nullable-by-default fields; `null` meaning three different things.
- Bare-array responses.
- Exposing internal enum names, table names, or error codes.

## Checklist

- [ ] One casing style; consistent names for repeated concepts.
- [ ] Identifiers are opaque strings.
- [ ] Time, duration, money, and large integers follow the rules.
- [ ] Enum policy for unknown values is stated.
- [ ] Null, absent, and empty are defined for optional fields.
- [ ] Top-level payload shape is intentional; prefer object envelopes when extensibility or sibling metadata is needed, and use arrays/scalars only when they are a clear, stable fit for the project.
- [ ] Sizes and nesting are bounded.
