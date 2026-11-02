# Messaging

## Contents

- Scope
- Message Types
- Channels and Naming
- Envelope
- Delivery and Ordering
- Consumer Design
- Failure Handling
- Schema Evolution
- Security and Operations
- Contract Mapping
- Anti-Patterns
- Checklist
- Sources

## Scope

- Asynchronous, brokered communication: queues, publish-subscribe topics, and logs, over protocols such as AMQP, MQTT, Kafka, and NATS.
- Covers message design, delivery semantics, ordering, consumers, failure handling, and schema evolution. Broker-specific tuning is out of scope.

## Message Types

| Type    | Meaning                                     | Naming                        |
| ------- | ------------------------------------------- | ----------------------------- |
| Event   | Fact that already happened                  | Past tense: `order.placed`    |
| Command | Request that one consumer perform an action | Imperative: `payment.capture` |
| Reply   | Response to a command or request            | Correlated to the request     |

- Events are owned by the producer; they describe state, not instructions to consumers.
- A command targets one logical consumer; an event may have zero to many.
- Event payload strategy: notification (identifiers only, consumers fetch state) or state transfer (full state); choose per event and document it.

## Channels and Naming

- One channel per message type or per aggregate stream; do not mix unrelated types on one channel unless consumers filter by type.
- Hierarchical, lowercase, dot- or slash-separated names that include domain and entity: `orders.order.placed`.
- Declare channel kind: queue (competing consumers), topic (fan-out), or log (replayable stream).
- Names are part of the contract; renaming is breaking.

| Good                                 | Bad                  | Rule                                                         |
| ------------------------------------ | -------------------- | ------------------------------------------------------------ |
| `orders.order.placed`                | `OrderTopic1`        | Domain, entity, event; lowercase                             |
| `payments.invoice.paid`              | `invoice-events-all` | One message type per channel unless consumers filter by type |
| `shipping.label.requested` (command) | `shipping.label`     | Commands are imperative, events past tense                   |

## Envelope

- Use a standard envelope for every message. CloudEvents 1.0.2 required attributes: `id`, `source`, `specversion`, `type`; optional: `datacontenttype`, `dataschema`, `subject`, `time`.
- `source` + `id` uniquely identify an event; `id` is stable across redelivery.
- `type` names the message type and carries version information when versioned by type (`com.example.order.placed.v1`).
- Metadata that routes or traces belongs in headers or attributes; the business payload in `data`.
- Propagate trace context (W3C `traceparent`, `tracestate`) in message headers.
- Declare content type and serialization (JSON, Avro, Protobuf) per message.

Example: CloudEvents 1.0.2 structured JSON.

```json
{
  "specversion": "1.0",
  "id": "evt_01HZY",
  "source": "/orders-service",
  "type": "com.example.order.placed.v1",
  "time": "2026-03-01T09:30:00Z",
  "datacontenttype": "application/json",
  "subject": "ord_01HZX",
  "data": { "orderId": "ord_01HZX" }
}
```

## Delivery and Ordering

- Delivery guarantees: at-most-once, at-least-once. Exactly-once effect is achieved by at-least-once delivery plus idempotent consumers, not by the transport alone.
- Design for at-least-once: duplicates and redelivery occur.
- Ordering exists only within an ordering scope (a partition, a queue, a session). Choose the ordering key (usually the aggregate identifier) so related messages share a scope.
- No global ordering; do not rely on cross-key order.
- State the delivery guarantee and ordering scope of every channel in the contract.
- Retention and replay: log-based channels declare retention; queues declare time-to-live.

## Consumer Design

- Consumers are idempotent: record processed message `id` (inbox/dedup store) or make the effect naturally idempotent (upsert with version check).
- Acknowledge after the effect is durably applied.
- Competing consumers share a queue or consumer group; fan-out consumers each get their own subscription.
- Bound prefetch and concurrency to apply backpressure.
- Messages that cannot be processed are not retried forever; see failure handling.
- Request-reply: the request carries `replyTo` (destination) and `correlationId`; the reply echoes `correlationId`; define timeouts.

## Failure Handling

- Transient failures: retry with exponential backoff and jitter, bounded attempts.
- Poison messages: after the retry limit, route to a dead-letter channel with failure reason and original headers; alert and provide a replay path.
- Define the visibility of failure to producers (usually none; use reply events when a result is needed).
- Producer side: publish atomically with state change using a transactional outbox when a database write and a publish must agree.
- Large payloads: store the payload externally and send a reference (claim-check) with size and integrity data.

Example: headers added when routing to a dead-letter channel (names are a project convention).

```
x-failure-reason: schema-validation-failed
x-original-channel: orders.order.placed
x-attempts: 5
```

## Schema Evolution

- Every message type has a schema; reference it from the contract and the envelope (`dataschema` or schema identifier).
- Compatible changes: add optional fields with defaults, add new message types. Consumers ignore unknown fields.
- Breaking changes: removing or renaming fields, changing types or meaning, changing required status. Publish a new message type version and run both until consumers migrate.
- When a schema registry exists, set compatibility mode per channel (backward, forward, or full) and enforce it in CI.
- Never reuse a field identifier or number in binary formats.

## Security and Operations

- Authenticate producers and consumers at the broker; authorize per channel (publish and subscribe permissions).
- Encrypt in transit; encrypt sensitive fields end to end when brokers are not trusted.
- Minimize personal and secret data in messages; messages persist and replicate.
- Validate payloads against the schema on consumption; treat messages as untrusted input.
- Declare size limits, rate limits, and quotas per producer.
- Monitor lag, dead-letter volume, redelivery rate, and processing latency.

## Contract Mapping

- AsyncAPI elements:
  - `servers`: broker host, protocol, security.
  - `channels`: address, messages, bindings.
  - `operations`: `send` for producing, `receive` for consuming.
  - `messages`: headers, payload, `correlationId`, `contentType`.
  - Protocol bindings: broker-specific settings.
- Delivery guarantee, ordering key, retention, dead-letter policy, and idempotency expectations go into message and channel descriptions and the header notes.

## Anti-Patterns

- Treating messaging as synchronous RPC.
- Assuming exactly-once delivery or global ordering.
- Non-idempotent consumers.
- Unbounded retries; no dead-letter handling.
- Events that carry commands ("please do X") or leak internal table structure.
- Changing message formats in place.
- Dual writes (database and broker) without an outbox or equivalent.
- One catch-all topic for all types.

## Checklist

- [ ] Each message is classified as event, command, or reply.
- [ ] Channel kind, delivery guarantee, ordering scope, and retention are stated.
- [ ] Envelope attributes and content type are defined.
- [ ] Consumer idempotency strategy is defined.
- [ ] Retry, dead-letter, and replay behavior are defined.
- [ ] Schema compatibility rule is stated per channel.
- [ ] Producer and consumer permissions are defined.

## Sources

- CloudEvents specification 1.0.2.
- AsyncAPI specification and protocol bindings.
- OASIS MQTT and AMQP specifications; documentation of the chosen broker for delivery semantics.
- W3C Trace Context.
