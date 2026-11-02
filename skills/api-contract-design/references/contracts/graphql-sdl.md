# GraphQL SDL Contract

## Contents

- Scope
- File Rules
- Type System Elements
- Directives
- Descriptions
- Value Constraints
- Compatibility Rules
- Anti-Patterns
- Checklist
- Sources

## Scope

- Authoring rules for GraphQL schemas in SDL, specification edition September 2025 (fallback October 2021).
- Design decisions (naming, nullability, pagination, errors) follow the GraphQL protocol reference.

## File Rules

- Header notes as a leading comment block (SDL comments start with `#`).
- One schema document per API surface; split into multiple files only when tooling merges them; use `extend` to compose.
- Order: directive definitions, scalars, enums, interfaces, input types, object types, unions, then `Query`, `Mutation`, `Subscription`.
- `schema { query: Query mutation: Mutation subscription: Subscription }` only when root type names deviate from the defaults.

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

| Directive                     | Use                                                                                                              |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `@deprecated(reason: String)` | Mark fields, enum values, arguments, and input fields as deprecated; always give a reason naming the replacement |
| `@specifiedBy(url: String!)`  | Link a custom scalar to its specification                                                                        |
| `@oneOf`                      | Input object where exactly one field must be provided (September 2025 edition)                                   |
| `@skip`, `@include`           | Execution directives for operations, not used in SDL                                                             |
| Custom directives             | Allowed; define them explicitly, list locations, and record them in the header notes                             |

```graphql
type Order {
  id: ID!
  legacyCode: String @deprecated(reason: "Use id.")
}
scalar DateTime @specifiedBy(url: "https://www.rfc-editor.org/rfc/rfc3339")
```

## Descriptions

- Every type, field, argument, enum value, and directive has a description (block strings `"""..."""`).
- Descriptions state meaning, units, bounds, nullability reasons, and authorization requirements.
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
- Authentication, rate limits, cost limits, and subscription transport are not expressible: record them in the header notes.

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
- [ ] Descriptions on all elements.
- [ ] Nullability explicit and justified.
- [ ] `@deprecated` carries a reason and a replacement.
- [ ] Constraints expressed by scalars, input shapes, or descriptions.
- [ ] Header notes present, including what SDL cannot express.

## Sources

- GraphQL specification, September 2025 edition (https://spec.graphql.org/September2025/); September 2025 edition announcement.
- Relay Cursor Connections specification.
