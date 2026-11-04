# Schema Modeling (OpenAPI and AsyncAPI)

## Scope

- How to express field types, constraints, and structure inside schemas of OpenAPI and AsyncAPI documents.
- The project owns the physical file layout: contracts may be monolithic or modular. Do not prescribe splitting or merging files.
- Keep one logical definition for each schema and resolve references according to the host format and project tooling. Inline definitions, local references, and external references are all valid when the project supports them.
- Protobuf and GraphQL SDL have native type systems and use their own language-level composition or import mechanisms.

## Dialects

| Host                | Dialect                                                                                                  | Notes                                                                                                |
| ------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| OpenAPI 3.1 and 3.2 | OAS dialect: JSON Schema 2020-12 vocabularies plus the OAS base vocabulary                               | Adds `discriminator`, `xml`, `externalDocs`, `example`; `jsonSchemaDialect` can override the default |
| AsyncAPI 3.x        | AsyncAPI Schema Object: JSON Schema draft-07 superset plus `discriminator`, `externalDocs`, `deprecated` | Other formats through the Multi Format Schema Object                                                 |

- Keyword differences that matter:

| Topic                   | 2020-12 (OpenAPI)       | draft-07 (AsyncAPI)                                                       |
| ----------------------- | ----------------------- | ------------------------------------------------------------------------- |
| Reusable definitions    | `$defs`                 | `definitions`                                                             |
| Tuple arrays            | `prefixItems` + `items` | array-form `items`                                                        |
| Keywords next to `$ref` | Allowed                 | Do not rely on siblings; wrap in `allOf` when needed for interoperability |
| `unevaluatedProperties` | Available               | Not available                                                             |

- Use only keywords the host dialect defines.

## Types and Constraints

| Need                     | Keywords                                                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| Type                     | `type`: `string`, `number`, `integer`, `boolean`, `array`, `object`, `null`                                              |
| Fixed set                | `enum`, `const`                                                                                                          |
| String size and shape    | `minLength`, `maxLength`, `pattern`, `format`                                                                            |
| Numeric range            | `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum` (numbers in draft-06+), `multipleOf`                        |
| Array                    | `items`, `minItems`, `maxItems`, `uniqueItems`                                                                           |
| Object                   | `properties`, `required`, `additionalProperties`, `minProperties`, `maxProperties`, `patternProperties`, `propertyNames` |
| Binary or encoded string | `contentMediaType`, `contentEncoding` (`format: binary` is not used in 3.1+)                                             |
| Documentation            | `title`, `description`, `default`, `examples`, `deprecated`                                                              |
| Access                   | `readOnly`, `writeOnly`                                                                                                  |

- `format` is generally an annotation unless the selected validator is configured to assert it; do not rely on it as a security control. Add explicit bounds and application validation for security-sensitive values.
- Common formats: `date-time`, `date`, `time`, `duration`, `email`, `uri`, `uuid`; OpenAPI also documents `int32`, `int64`, `float`, `double`.
- Bound consumer-controlled strings, arrays, maps, and numeric inputs where domain, security, or resource limits require it. Encode meaningful finite limits in the schema when supported; do not invent arbitrary caps.
- `integer` with `format: int64`: values above 2⁵³ − 1 lose precision in consumers that use IEEE 754 doubles; transmit such identifiers and counters as strings.
- `pattern` is an unanchored regular expression; anchor it (`^...$`) and keep it ECMA-262-compatible.

```yaml
name: { type: string, minLength: 1, maxLength: 200 }
tags:
  {
    type: array,
    items: { type: string, maxLength: 50 },
    maxItems: 20,
    uniqueItems: true,
  }
price:
  {
    type: integer,
    minimum: 0,
    maximum: 999999999999,
    description: Minor units.,
  }
code: { type: string, pattern: "^[A-Z]{3}$" }
```

## Objects and Properties

- Give every consumer-facing property a type and a meaningful description; express applicable constraints in the schema.
- `required` lists properties that must be present; it does not mean non-null.
- Closed objects (`additionalProperties: false`, or `unevaluatedProperties: false` in 2020-12) for request bodies when unknown input must be rejected.
- Response objects stay open so producers can add fields; consumers ignore unknown fields.
- Dictionary-like data: `additionalProperties` with a value schema plus `maxProperties`.
- Property names follow one casing style across the whole contract.

```yaml
OrderCreate: # request: closed, unknown input is rejected
  type: object
  properties: { total: { $ref: "#/components/schemas/Money" } }
  required: [total]
  unevaluatedProperties: false
Order: # response: open, fields may be added later
  type: object
  properties:
    { id: { type: string }, total: { $ref: "#/components/schemas/Money" } }
  required: [id, total]
```

## Composition

- `allOf`: combine a base and an extension; avoid inheritance deeper than two levels.
- `oneOf`: exactly one alternative; pair with `discriminator` (`propertyName`, `mapping`) so consumers can select the branch.
- `anyOf`: at least one alternative; avoid for polymorphic payloads because matching is ambiguous.
- `not`: exclusion rules; use sparingly.
- `if`/`then`/`else`: conditional requirements when the host dialect supports them.
- With `allOf` and closed objects, use `unevaluatedProperties: false` (2020-12); `additionalProperties: false` inside each branch rejects the other branch's fields.

```yaml
Pet:
  oneOf:
    - { $ref: "#/components/schemas/Cat" }
    - { $ref: "#/components/schemas/Dog" }
  discriminator:
    propertyName: kind
    mapping:
      { cat: "#/components/schemas/Cat", dog: "#/components/schemas/Dog" }
Cat:
  type: object
  properties: { kind: { const: cat } }
  required: [kind]
```

## Nullability and Presence

- Required and non-null: in `required`, no `null` in `type`.
- Required and nullable: in `required`, `type: [string, "null"]`.
- Optional: not in `required`.
- Use type arrays for nullability in 3.1+ and AsyncAPI; the `nullable` keyword belongs to OpenAPI 3.0 only.
- Define what absence, `null`, and empty mean for every optional field (see payload conventions).

| Intent                | Schema                                                    |
| --------------------- | --------------------------------------------------------- |
| Required, never null  | `required: [name]` and `name: { type: string }`           |
| Required, may be null | `required: [note]` and `note: { type: [string, "null"] }` |
| Optional              | property not listed in `required`                         |

## Read and Write Variants

- `readOnly: true`: server-generated, never sent by clients (`id`, `createdAt`).
- `writeOnly: true`: accepted from clients, never returned (`password`, secrets).
- When create, update, and read shapes differ materially, use separate component schemas (`OrderCreate`, `OrderUpdate`, `Order`) instead of conditional keywords.
- Server-managed and privileged fields (roles, ownership, tenant) are absent from write schemas to prevent mass assignment.

```yaml
User:
  type: object
  properties:
    id: { type: string, readOnly: true }
    email: { type: string, maxLength: 320 }
    password: { type: string, minLength: 12, maxLength: 128, writeOnly: true }
```

## Reuse

- Prefer a shared schema when the meaning and constraints are genuinely identical; similarly named fields with different meaning should remain separate.
- Define each schema once in `components.schemas`; reference with `$ref`.
- Extract shared value objects (`Money`, `Address`, `Problem`, `PageInfo`).
- Name schemas `PascalCase` and by meaning, not by operation.
- Reuse must not erase operation-specific rules: create, update, read, and event payloads often have different writable or required fields.
- Use the project's existing component or reference layout. Do not duplicate a schema merely to avoid a supported reference, and do not force a separate schema file when the project keeps contracts together.

## Examples

- Provide `examples` per schema and per media type; examples validate against their schema.
- Use realistic but fictional values; no real personal data or secrets.
- Show edge shapes: empty arrays, optional fields omitted, nullable fields null.

## Anti-Patterns

- `type: object` with no properties for structured data.
- Unbounded strings, arrays, and maps.
- Optional meaning "may be null" and vice versa.
- Enums mirroring internal numeric codes.
- `oneOf` without discriminator for payloads that need branch selection.
- `format` used as the only validation of important inputs.
- `additionalProperties: true` on request schemas by default.

## Checklist

- [ ] Only keywords of the host dialect are used.
- [ ] Every property has a type and meaningful description; applicable domain and resource bounds are explicit.
- [ ] `required`, nullability, and optionality are consistent.
- [ ] Request objects are closed or the openness is intentional.
- [ ] Read-only and write-only fields are marked; privileged fields are absent from writes.
- [ ] Shared schemas are defined once.
- [ ] Examples validate.
