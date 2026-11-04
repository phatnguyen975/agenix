# AsyncAPI Contract

## Scope

- Authoring rules for AsyncAPI documents describing WebSocket and Messaging APIs.
- Baseline 3.1.0 (minor release; changing `asyncapi: 3.0.0` to `3.1.0` keeps existing documents valid); fallback 3.0.0.
- Payload schemas follow the schema-modeling rules for the AsyncAPI Schema Object.

## Version Rules

- `asyncapi: 3.1.0` for new documents; keep the project's version otherwise.
- AsyncAPI 3 separates channels, operations, and messages; channels are reusable across documents.
- `info.version` is the contract version, not the AsyncAPI version.
- Version 2.x documents use a different structure (`publish`/`subscribe` on channels); do not mix structures.

## Document Structure

| Field                | Required | Use                                                                                                                                 |
| -------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `asyncapi`           | Yes      | Specification version                                                                                                               |
| `id`                 | No       | Application identifier (URI recommended)                                                                                            |
| `info`               | Yes      | `title`, `version` required; optional consumer-facing `description`, `termsOfService`, `contact`, `license`, `tags`, `externalDocs` |
| `servers`            | No       | Named connection targets                                                                                                            |
| `defaultContentType` | No       | Content type used when a message omits `contentType`                                                                                |
| `channels`           | No       | Named addressable message destinations                                                                                              |
| `operations`         | No       | Send and receive operations on channels                                                                                             |
| `components`         | No       | Reusable objects                                                                                                                    |

## Servers

- Fields: `host` (required), `protocol` (required), `protocolVersion`, `pathname`, `title`, `summary`, `description`, `variables`, `security`, `tags`, `externalDocs`, `bindings`.
- `host` carries host and optional port; `pathname` carries the path (in version 3 the version 2 `url` is split).
- Protocol values name the transport (for example `kafka`, `amqp`, `mqtt`, `ws`, `wss`, `nats`).
- One server entry per environment or broker.

## Channels

- Fields:
  | Field                                                     | Meaning                                                                                                                           |
  | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
  | `address`                                                 | Optional string or `null`; topic, queue, or path; may contain `{parameters}`. If absent or `null`, the address is unknown/dynamic |
  | `messages`                                                | Map of messages allowed on the channel                                                                                            |
  | `servers`                                                 | Restricts the channel to listed servers                                                                                           |
  | `parameters`                                              | Variables used in `address`                                                                                                       |
  | `title`, `summary`, `description`, `tags`, `externalDocs` | Documentation                                                                                                                     |
  | `bindings`                                                | Protocol-specific settings                                                                                                        |
- A channel describes where messages travel, not who sends them. `address` is optional in AsyncAPI 3.1; include a concrete address when known and use `null` (or omit it) only when it is genuinely unknown or resolved dynamically at runtime.
- `parameters` declare address variables with `description`, `enum`, `default`, `examples`, `location`.
- Name channel keys in `camelCase`; the `address` holds the real name.

```yaml
channels:
  telemetry:
    address: fleet/{deviceId}/telemetry
    parameters:
      deviceId: { description: Device identifier. }
    messages:
      telemetry: { $ref: "#/components/messages/Telemetry" }
```

## Operations

- Fields: `action` (`send` or `receive`, required), `channel` (reference, required), `title`, `summary`, `description`, `security`, `tags`, `externalDocs`, `bindings`, `traits`, `messages` (subset of the channel's messages), `reply`.
- `send`: the described application sends messages to the channel. `receive`: the application receives messages from the channel. Perspective is always the described application.
- `reply` (request-reply): `address` (`location` runtime expression, `description`), `channel`, `messages`; or reference a reusable reply in `components.replies`.
- Each operation lists the messages it uses explicitly.

```yaml
operations:
  publishTelemetry: # the described application produces messages
    action: send
    channel: { $ref: "#/channels/telemetry" }
  onTelemetry: # the described application consumes messages
    action: receive
    channel: { $ref: "#/channels/telemetry" }
  requestQuote: # request-reply
    action: send
    channel: { $ref: "#/channels/quoteRequests" }
    reply:
      address: { location: $message.header#/replyTo }
      channel: { $ref: "#/channels/quoteReplies" }
```

An application normally uses one action per channel; the second operation above shows the consumer's view.

## Messages

- Fields: `headers`, `payload`, `correlationId`, `contentType`, `name`, `title`, `summary`, `description`, `tags`, `externalDocs`, `bindings`, `examples`, `traits`.
- `payload` and `headers` use the AsyncAPI Schema Object or a Multi Format Schema Object (`schemaFormat` + `schema`) for other formats such as Avro, OpenAPI Schema, or JSON Schema draft-07.
- `correlationId`: `location` as a runtime expression (for example `$message.header#/correlationId`) and `description`.
- Examples: `name`, `summary`, `headers`, `payload`; provide at least one representative example per message.
- One message per message type; shared envelope fields live in a reusable `headers` schema.

```yaml
components:
  messages:
    OrderPlaced:
      name: OrderPlaced
      contentType: application/json
      headers: { $ref: "#/components/schemas/Envelope" }
      payload: { $ref: "#/components/schemas/Order" }
      examples:
        - name: pending
          payload: { id: ord_01HZX, status: PENDING }
```

## Components and Traits

- Component maps:
  - Definitions: `schemas`, `servers`, `channels`, `operations`, `messages`, `securitySchemes`, `serverVariables`, `parameters`, `correlationIds`, `replies`, `replyAddresses`, `externalDocs`, `tags`.
  - Traits: `operationTraits`, `messageTraits`.
  - Bindings: `serverBindings`, `channelBindings`, `operationBindings`, `messageBindings`.
- Component keys match `^[a-zA-Z0-9\.\-_]+$`.
- Traits add shared fields to operations or messages; a trait property must not override the same property on the target object.
- Use `$ref` where the AsyncAPI object type supports Reference Objects. AsyncAPI 3 security arrays contain Security Scheme Objects or Reference Objects; this differs from OpenAPI's Security Requirement Object map.

## Security Schemes

- Types: `userPassword`, `apiKey`, `X509`, `symmetricEncryption`, `asymmetricEncryption`, `httpApiKey`, `http`, `oauth2`, `openIdConnect`, `plain`, `scramSha256`, `scramSha512`, `gssapi`.
- Declare in `components.securitySchemes`; apply through `servers[*].security` and `operations[*].security`.
- `servers[*].security` and `operations[*].security` are arrays of Security Scheme Objects or Reference Objects. Reference a component with `- $ref: "#/components/securitySchemes/bearer"`; do not use OpenAPI's `{ schemeName: [scopes] }` Security Requirement Object shape here.
- Entries within one security array are alternatives (OR): satisfying one is sufficient for that array. If both server-level and operation-level security are present, the applicable server requirement and operation requirement must both be satisfied (AND across the two levels). Do not repeat the same scheme at both levels unless the duplication is intentional.
- For OAuth2, the scheme defines `flows[*].availableScopes` and its `scopes` field. Document consumer-relevant scope requirements in the relevant operation description or linked security documentation when the format cannot express per-operation scope selection.

## Bindings

- Bindings add protocol-specific settings at server, channel, operation, and message level: for example Kafka (topic configuration, key schema, group), AMQP (exchange, queue, delivery mode), MQTT (QoS, retain), WebSockets (method, query, headers), HTTP.
- Every binding object has `bindingVersion`; pin it.
- Confirm field lists in the AsyncAPI bindings repository for the chosen protocol and version.
- Use bindings only for settings that change broker or connection behavior; keep business semantics in descriptions and schemas.

## Authoring Rules

- Use `info.description` for a concise consumer-facing application overview when useful. Put delivery, ordering, retention, security, and reply semantics on the relevant server, operation, channel, or message.
- Define messages and schemas in `components`; reference them from channels and operations.
- Every application message has a stable name and representative example. When it carries a payload, define its schema and effective content type (explicit `contentType` or `defaultContentType`). Add header schemas and correlation data only when used.
- State delivery guarantee, ordering scope, retention, and dead-letter policy in channel descriptions.
- State idempotency expectations for consumers in operation descriptions.
- Do not embed credentials or real broker hosts.

## Anti-Patterns

- Describing the same message in several channels instead of referencing one component.
- `send`/`receive` from the wrong perspective.
- Payload-bearing messages without a representative example, payload schema, or effective content type.
- Putting business rules only in bindings.
- Mixing AsyncAPI 2.x and 3.x structures.
- Open payload schemas on consumed messages where strictness is required.

## Checklist

- [ ] `asyncapi` version is baseline or recorded fallback.
- [ ] Application overview is concise; channel and operation semantics are documented at the relevant objects.
- [ ] Each channel has messages and a delivery description; include `address` when known, or explicitly use `null`/omit it only for a genuinely dynamic or unknown address.
- [ ] Each operation has `action`, `channel`, and explicit `messages`.
- [ ] Each message has a stable name and example; payload schema and effective content type are defined when it carries a payload; correlation is defined where replies require it.
- [ ] Bindings pinned with `bindingVersion`.
- [ ] Security schemes declared and applied.
