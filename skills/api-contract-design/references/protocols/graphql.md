# GraphQL

## Contents

- Scope
- Schema Design
- Types and Naming
- Nullability
- Queries and Pagination
- Mutations
- Subscriptions
- Errors
- Transport
- Security and Cost
- Evolution
- Contract Mapping
- Anti-Patterns
- Checklist
- Sources

## Scope

- GraphQL APIs described by a schema in SDL, edition September 2025.
- Covers schema, operation design, errors, transport, cost control, and evolution.

## Schema Design

- Design the schema from consumer use cases, not from storage tables.
- One schema serves many clients; do not model screens.
- Expose a graph of domain types connected by fields; root types: `Query`, `Mutation`, optional `Subscription`.
- Use interfaces and unions for polymorphism; keep hierarchies shallow.
- Global object identification: an `id: ID!` that is unique across the schema for refetchable objects (Relay `Node` interface pattern).
- Document every type, field, argument, and enum value with a description.
- Prefer domain-specific scalars (`DateTime`, `URL`) with `@specifiedBy(url:)` pointing to their specification over untyped strings.

## Types and Naming

- Types, interfaces, unions, inputs: `PascalCase`. Fields and arguments: `camelCase`. Enum values: `SCREAMING_SNAKE_CASE`.
- Input types end with `Input`; mutation payload types end with `Payload`.
- Mutations are verb-first: `createOrder`, `cancelOrder`.
- Enums for closed sets; document whether new values may be added.
- Input objects model mutually exclusive choices with `@oneOf` (September 2025 edition).

## Nullability

- A field that errors resolves to `null`; if the field is non-null, the null propagates to the nearest nullable parent.
- Make a field non-null only when it is guaranteed under every failure mode of its resolver; otherwise nullable.
- List elements and list fields have independent nullability; decide each.
- Required input arguments and fields are non-null; optional ones are nullable with defaults declared.

```graphql
type Order {
  id: ID! # always present
  note: String # optional data
  customer: Customer # resolver may fail: nullable
  lines(first: Int = 20): OrderLineConnection! # container is always returned
}
```

## Queries and Pagination

- Lists that can grow use connections (Relay Cursor Connections): `edges { cursor node }`, `pageInfo { hasNextPage hasPreviousPage startCursor endCursor }`, arguments `first`, `after`, `last`, `before`.
- Cap `first`/`last` with a documented maximum; require one of them.
- Cursors are opaque.
- Filtering and ordering use typed input arguments, not free-form strings.
- Avoid root fields that return unbounded lists.

## Mutations

- One `input` argument of an input type; one payload type.
- Payload returns the changed object(s) and domain-level user errors as typed fields; reserve top-level `errors` for unexpected failures.
- Mutations execute serially at the root; make each mutation self-contained.
- Retried mutations need an idempotency mechanism (a client-supplied identifier field in the input).

```graphql
input CancelOrderInput {
  orderId: ID!
  reason: String
}
type CancelOrderPayload {
  order: Order
  userErrors: [UserError!]! # domain errors the caller can fix
}
type Mutation {
  cancelOrder(input: CancelOrderInput!): CancelOrderPayload!
}
```

## Subscriptions

- Subscriptions deliver events for a subject; define the event payload type and filter arguments.
- The transport for subscriptions is not defined by the core specification; choose a documented transport (WebSocket-based or SSE-based) and state it in the header notes.
- Authorize at subscribe time and per event; enforce limits on concurrent subscriptions per identity.

## Errors

- Response fields: `data`, `errors`, optional `extensions`. Each error has `message`, optional `locations`, `path`, `extensions`.
- Partial success is normal: `data` may contain nulls alongside `errors`.
- Put a stable machine-readable `code` in `extensions`; clients branch on it, never on `message`.
- Request-level failures (syntax, validation) return no `data`.
- Do not leak stack traces, resolver names, or internal identifiers.

```json
{
  "data": { "order": null },
  "errors": [
    {
      "message": "Order not found",
      "path": ["order"],
      "extensions": { "code": "NOT_FOUND" }
    }
  ]
}
```

## Transport

- HTTP: single endpoint; `POST` with JSON body `query`, `operationName`, `variables`, `extensions`; `GET` only for queries.
- GraphQL over HTTP (draft): response media type `application/graphql-response+json`; state which variant the server supports.
- Persisted operations: clients send an identifier instead of query text; the server allowlists known operations.
- HTTP status carries transport and request-level failures; resolver errors travel in the body.

## Security and Cost

- Enforce query depth limits, complexity or cost limits, and operation size limits.
- Limit batching and aliasing per request.
- Introspection: enable or disable by an explicit policy per environment and audience.
- Authorize in the domain layer for every field that returns protected data, not only at the root.
- Rate limit by cost, not only by request count.
- Timeouts on resolvers and on the whole operation.

## Evolution

- Version-less evolution: add fields and types freely; never change the meaning or type of an existing field.
- Deprecate with `@deprecated(reason: "...")`; the September 2025 edition supports deprecating more schema elements, including arguments and input fields.
- Remove only after observed usage reaches zero or a published sunset date passes.
- Adding an enum value or union member can break strict clients; announce it.

## Contract Mapping

- SDL file with descriptions, directives, and the header notes as a leading comment.
- Authentication, rate limits, and subscription transport are not expressible in SDL: record them in the header notes.
- Schema Coordinates (`Type.field`) reference schema elements precisely in change notes (September 2025 edition).

## Anti-Patterns

- Mirroring database tables as types.
- Unbounded list fields; connections without a page-size cap.
- Mutations that take many scalar arguments instead of one input object.
- Everything non-null.
- Generic `JSON` or `Any` scalars for structured data.
- Schema per client or per screen.
- Exposing introspection and verbose errors in production without a policy.

## Checklist

- [ ] Every type, field, argument, enum value has a description.
- [ ] Nullability reflects resolver failure modes.
- [ ] Every list is a bounded connection or has a documented cap.
- [ ] Every mutation has one input type and one payload type.
- [ ] Depth, cost, batching, and introspection policies are stated.
- [ ] Error `extensions.code` values are listed.
- [ ] Subscription transport is documented when subscriptions exist.

## Sources

- GraphQL specification, September 2025 edition (https://spec.graphql.org/September2025/).
- GraphQL over HTTP specification (draft).
- Relay Cursor Connections specification; Relay Global Object Identification.
