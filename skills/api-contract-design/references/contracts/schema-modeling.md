# Schema Modeling (OpenAPI and AsyncAPI)

## Contents

- Scope
- Dialects
- Types and Constraints
- Objects and Properties
- Composition
- Nullability and Presence
- Read and Write Variants
- Reuse
- Examples
- Anti-Patterns
- Checklist
- Sources

## Scope

- How to express field types, constraints, and structure inside schemas of OpenAPI and AsyncAPI documents.
- Schemas live inside the contract; no standalone schema file is created.
- Protobuf and GraphQL SDL have native type systems and use their own references.

## Dialects

| Host                | Dialect                                                                                                  | Notes                                                                                                |
| ------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| OpenAPI 3.1 and 3.2 | OAS dialect: JSON Schema 2020-12 vocabularies plus the OAS base vocabulary                               | Adds `discriminator`, `xml`, `externalDocs`, `example`; `jsonSchemaDialect` can override the default |
| AsyncAPI 3.x        | AsyncAPI Schema Object: JSON Schema draft-07 superset plus `discriminator`, `externalDocs`, `deprecated` | Other formats through Multi Format Schema Object                                                     |

- Keyword differences that matter:

| Topic                   | 2020-12 (OpenAPI)       | draft-07 (AsyncAPI)      |
| ----------------------- | ----------------------- | ------------------------ |
| Reusable definitions    | `$defs`                 | `definitions`            |
| Tuple arrays            | `prefixItems` + `items` | array-form `items`       |
| Keywords next to `$ref` | Allowed                 | Ignored; wrap in `allOf` |
| `unevaluatedProperties` | Available               | Not available            |

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

- `format` is an annotation unless the validator asserts it; do not rely on it for security-relevant validation, and pair it with `pattern` or length bounds where needed.
- Common formats: `date-time`, `date`, `time`, `duration`, `email`, `uri`, `uuid`; OpenAPI also documents `int32`, `int64`, `float`, `double`.
- Every string has `maxLength`; every array has `maxItems`; every number has a range or a documented reason for none.
- `integer` with `format: int64`: values above 2^53 − 1 lose precision in consumers that use IEEE 754 doubles; transmit such identifiers and counters as strings.
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

- List every property with a type, description, and constraints.
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

- Define each schema once in `components.schemas`; reference with `$ref`.
- Extract shared value objects (`Money`, `Address`, `Problem`, `PageInfo`).
- Name schemas `PascalCase` and by meaning, not by operation.
- Do not duplicate a schema between OpenAPI and AsyncAPI documents when a shared definition is not possible; keep both aligned and note the pairing in the descriptions.

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
- [ ] Every property has type, description, and bounds.
- [ ] `required`, nullability, and optionality are consistent.
- [ ] Request objects are closed or the openness is intentional.
- [ ] Read-only and write-only fields are marked; privileged fields are absent from writes.
- [ ] Shared schemas are defined once.
- [ ] Examples validate.

## Sources

- JSON Schema 2020-12 Core and Validation specifications (https://json-schema.org/specification).
- OpenAPI Specification, Schema Object; AsyncAPI Specification, Schema Object and Multi Format Schema Object.
