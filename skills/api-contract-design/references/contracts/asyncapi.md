# AsyncAPI Contract

## Contents

- Scope
- Version Rules
- Document Structure
- Servers
- Channels
- Operations
- Messages
- Components and Traits
- Security Schemes
- Bindings
- Authoring Rules
- Anti-Patterns
- Checklist
- Sources

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

| Field                | Required | Use                                                                                                                       |
| -------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| `asyncapi`           | Yes      | Specification version                                                                                                     |
| `id`                 | No       | Application identifier (URI recommended)                                                                                  |
| `info`               | Yes      | `title`, `version` required; `description` (header notes), `termsOfService`, `contact`, `license`, `tags`, `externalDocs` |
| `servers`            | No       | Named connection targets                                                                                                  |
| `defaultContentType` | No       | Content type used when a message omits `contentType`                                                                      |
| `channels`           | No       | Named addressable message destinations                                                                                    |
| `operations`         | No       | Send and receive operations on channels                                                                                   |
| `components`         | No       | Reusable objects                                                                                                          |

## Servers

- Fields: `host` (required), `protocol` (required), `protocolVersion`, `pathname`, `title`, `summary`, `description`, `variables`, `security`, `tags`, `externalDocs`, `bindings`.
- `host` carries host and optional port; `pathname` carries the path (in version 3 the version 2 `url` is split).
- Protocol values name the transport (for example `kafka`, `amqp`, `mqtt`, `ws`, `wss`, `nats`).
- One server entry per environment or broker.

## Channels

- Fields:

| Field                                                     | Meaning                                                                |
| --------------------------------------------------------- | ---------------------------------------------------------------------- |
| `address`                                                 | Topic, queue, or path; may contain `{parameters}`; `null` when dynamic |
| `messages`                                                | Map of messages allowed on the channel                                 |
| `servers`                                                 | Restricts the channel to listed servers                                |
| `parameters`                                              | Variables used in `address`                                            |
| `title`, `summary`, `description`, `tags`, `externalDocs` | Documentation                                                          |
| `bindings`                                                | Protocol-specific settings                                             |

- A channel describes where messages travel, not who sends them.
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
- Examples: `name`, `summary`, `headers`, `payload`; every message has at least one.
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
- Reference components with `$ref`.

## Security Schemes

- Types: `userPassword`, `apiKey`, `X509`, `symmetricEncryption`, `asymmetricEncryption`, `httpApiKey`, `http`, `oauth2`, `openIdConnect`, `plain`, `scramSha256`, `scramSha512`, `gssapi`.
- Declare in `components.securitySchemes`; apply through `servers[*].security` and `operations[*].security`.
- `oauth2` and `openIdConnect` entries list `scopes`.

## Bindings

- Bindings add protocol-specific settings at server, channel, operation, and message level: for example Kafka (topic configuration, key schema, group), AMQP (exchange, queue, delivery mode), MQTT (QoS, retain), WebSockets (method, query, headers), HTTP.
- Every binding object has `bindingVersion`; pin it.
- Confirm field lists in the AsyncAPI bindings repository for the chosen protocol and version.
- Use bindings only for settings that change broker or connection behavior; keep business semantics in descriptions and schemas.

## Authoring Rules

- Header notes go in `info.description` as the first section.
- Define messages and schemas in `components`; reference them from channels and operations.
- Every message has a name, content type, payload schema, and example.
- State delivery guarantee, ordering scope, retention, and dead-letter policy in channel descriptions.
- State idempotency expectations for consumers in operation descriptions.
- Do not embed credentials or real broker hosts.

## Anti-Patterns

- Describing the same message in several channels instead of referencing one component.
- `send`/`receive` from the wrong perspective.
- Messages without examples or content type.
- Putting business rules only in bindings.
- Mixing AsyncAPI 2.x and 3.x structures.
- Open payload schemas on consumed messages where strictness is required.

## Checklist

- [ ] `asyncapi` version is baseline or recorded fallback.
- [ ] Header notes in `info.description`.
- [ ] Each channel has `address`, messages, and a delivery description.
- [ ] Each operation has `action`, `channel`, and explicit `messages`.
- [ ] Each message has payload, content type, correlation (where replies exist), and example.
- [ ] Bindings pinned with `bindingVersion`.
- [ ] Security schemes declared and applied.

## Sources

- AsyncAPI Specification 3.1.0 and 3.0.0 (https://www.asyncapi.com/docs/reference/specification/latest).
- AsyncAPI 3.0.0 and 3.1.0 release notes.
- AsyncAPI bindings repository.
