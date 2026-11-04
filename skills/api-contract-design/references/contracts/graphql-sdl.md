# GraphQL SDL Contract

## Scope

- Authoring rules for GraphQL schemas in SDL, specification edition September 2025 (fallback October 2021).
- Design decisions (naming, nullability, pagination, errors) follow the GraphQL protocol reference.

## File Rules

- Use GraphQL description strings on public schema elements when their names are not self-descriptive or when consumers need semantics, constraints, units, or usage guidance. Schema descriptions are supported by both listed editions and are available through `__Schema.description`. Include an explicit `schema` definition when a schema-level description is needed, even when using conventional root type names. If no schema description is needed and root names are conventional, the definition may be omitted. Do not rely on `#` comments being exposed by introspection or documentation tooling.
- Preserve the project layout. A schema may be maintained in one SDL document or composed from multiple documents by the project toolchain. Use `extend` only where the composition process supports it.
- Order: directive definitions, scalars, enums, interfaces, input types, object types, unions, then `Query`, `Mutation`, `Subscription`.

## Type System Elements

| Element              | Syntax notes                                                                                    |
| -------------------- | ----------------------------------------------------------------------------------------------- |
| Scalar               | `scalar DateTime @specifiedBy(url: "...")`; built-ins `Int`, `Float`, `String`, `Boolean`, `ID` |
| Object               | `type Order implements Node { ... }`; interfaces may implement interfaces                       |
| Interface            | `interface Node { id: ID! }`                                                                    |
| Union                | `union SearchResult = Order \| Customer`                                                        |
| Enum                 | `enum OrderStatus { PENDING SHIPPED }`                                                          |
| Input object         | `input CreateOrderInput { ... }`; fields cannot be object types                                 |
| Directive definition | `directive @name(arg: Type) on LOCATION \| LOCATION`                                            |
| Extension            | `extend type Query { ... }`                                                                     |

- Non-null `!` and list `[Type!]!` wrappers are explicit on every field and argument.
- Arguments may have default values; document them.
- Interfaces declare the fields all implementers share; implementers repeat them.
- Root `Query` fields are the entry points; keep them few and resource-oriented.

## Directives

| Directive                     | Use                                                                                                                                             |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `@deprecated(reason: String)` | Mark fields, enum values, arguments, and input fields as deprecated; always give a reason naming the replacement                                |
| `@specifiedBy(url: String!)`  | Link a custom scalar to its specification                                                                                                       |
| `@oneOf`                      | Input object where exactly one field must be provided (September 2025 edition; remove for October 2021 fallback)                                |
| `@skip`, `@include`           | Execution directives for operations, not used in SDL                                                                                            |
| Custom directives             | Allowed; define them explicitly, list locations, and document their consumer-visible semantics where applied; ensure runtime enforcement exists |

```graphql
type Order {
  id: ID!
  legacyCode: String @deprecated(reason: "Use id.")
}
scalar DateTime @specifiedBy(url: "https://www.rfc-editor.org/rfc/rfc3339")
```

## Descriptions

- Describe public types, fields, arguments, enum values, and directives when their names are not self-descriptive or when additional semantics help consumers; use block strings (`"""..."""`) for longer descriptions.
- Descriptions state meaning, units, bounds, nullability reasons, and authorization requirements when relevant.
- Descriptions are Markdown-capable by convention; keep them plain and short.
- September 2025 edition allows descriptions on executable documents (operations, fragments, variables); this is for operation files, not the schema.

## Value Constraints

- The language has no native min, max, or pattern constraint syntax.
- Options, in order of preference:
  1. Dedicated custom scalars (`EmailAddress`, `PositiveInt`) with `@specifiedBy`.
  2. Input types shaped so invalid states cannot be expressed (`@oneOf`, enums).
  3. Custom constraint directives defined by the project.
  4. Description text for bounds the server enforces.
- State every enforced bound in the description so consumers can rely on it.
- Authentication, rate limits, query-cost limits, and subscription transport are not standardized by SDL. Describe transport and API-wide operational policies in accompanying API documentation; enforce them in the runtime. Document field-specific authorization intent where useful, but do not imply SDL descriptions or custom directives enforce it.

```graphql
"""
A valid e-mail address (RFC 5322 addr-spec); the server rejects other values.
"""
scalar EmailAddress @specifiedBy(url: "https://www.rfc-editor.org/rfc/rfc5322")

"""
Exactly one field must be provided.
"""
input OrderLookup @oneOf {
  id: ID
  externalReference: String
}
```

## Compatibility Rules

- Nullability and list shape are part of the public contract. Evaluate output and input positions separately; resolver failures can cause null propagation up to the nearest nullable parent.
- New enum values and union members are not unconditionally safe: clients with exhaustive switches may fail. Document the unknown-value policy and coordinate rollout.
- Compatible: add types, fields, enum values (see caveat), optional arguments with defaults, optional input fields; deprecate.
- Breaking:
  - Remove or rename types, fields, arguments, or enum values.
  - Change a type.
  - Output field: non-null to nullable is breaking (the reverse is compatible).
  - Argument or input field: nullable to non-null is breaking (the reverse is compatible).
  - Add a required argument or required input field.
  - Change a default value.
- Adding enum values and union members can break strict clients; announce them.
- Deprecate first; remove after usage ends.

## Anti-Patterns

- Missing descriptions.
- Arguments or fields without a deliberate nullability.
- `JSON` or `Any` scalars for structured data.
- Removing fields without a deprecation period.
- Enforced constraints that exist only in code.
- Custom directives without definitions.

## Checklist

- [ ] SDL parses; every type referenced is defined.
- [ ] Public elements have useful descriptions where needed; descriptions do not merely restate self-descriptive names.
- [ ] Nullability explicit and justified.
- [ ] `@deprecated` carries a reason and a replacement.
- [ ] Constraints expressed by scalars, input shapes, or descriptions.
- [ ] Public schema elements have useful descriptions; transport, security, and operational policies are documented in the appropriate accompanying documentation when they cannot be represented in SDL.
