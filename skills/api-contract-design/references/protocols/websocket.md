# WebSocket

## Scope

- Full-duplex message sessions over one connection (RFC 6455), also available over HTTP/2 (RFC 8441) and HTTP/3 (RFC 9220).
- Covers handshake, authentication, message design, reconnect, limits, and close semantics.

## Fit

- Use when both sides send frequent, low-latency messages on one session.
- One-way server updates: use SSE. Request-response only: use REST or gRPC.
- WebSocket gives no HTTP semantics (no status codes per message, no caching); design them explicitly.

## Connection

- HTTP/1.1: use the RFC 6455 Upgrade handshake (`Sec-WebSocket-Key` / `Sec-WebSocket-Accept`, response `101`). HTTP/2 and HTTP/3 use Extended CONNECT (RFC 8441 and RFC 9220); do not expect a `101` response or the HTTP/1.1 key/accept exchange on those transports.
- Always `wss://` (TLS) outside local development.
- Subprotocols: negotiate through `Sec-WebSocket-Protocol`; name and version the application protocol (for example `orders.v1`) and reject unsupported values.
- Extensions such as per-message compression are negotiated through `Sec-WebSocket-Extensions`; decide whether to allow them (compression can expose sensitive data to compression-oracle attacks).
- Validate the `Origin` header on the handshake for browser clients (defends against cross-site WebSocket hijacking).

## Authentication and Authorization

- Browser `WebSocket` cannot set custom headers on the handshake. Options:
  - Cookie-based session, with `Origin` and CSRF checks.
  - Short-lived, single-use ticket obtained over HTTPS and passed once at connect.
  - Authentication message as the first frame, with a short deadline.
- Avoid long-lived tokens in query strings; URLs are logged.
- Authenticate before processing any application message; close on failure.
- Authorize every subscription and every message type, not only the connection.
- Long-lived connections outlive token expiry: define re-authentication (an auth-refresh message) or close with a defined code and let the client reconnect.

## Message Design

- Text frames carry JSON by default; binary frames for Protobuf or other binary payloads. Declare the encoding.
- Envelope fields: `type` (message kind), `id` (message identifier), optional `correlationId` (links a reply to its request), `payload`.
- Define which messages are client-to-server, server-to-client, or both.
- Request-reply over WebSocket: the reply carries the request `id` as `correlationId` and either a result or a typed error.
- Typed error messages: stable `code`, human-readable `message`; no internals.
- Ordering is preserved within one connection; across reconnects it is not.
- Version the protocol through the subprotocol name or an explicit `version` in the first message.

Example envelope (JSON text frames).

```json
{"type": "subscribe", "id": "c-1", "payload": {"orderId": "ord_01HZX"}}
{"type": "subscribed", "correlationId": "c-1", "payload": {"subscriptionId": "sub_9"}}
{"type": "order.updated", "id": "e-42", "seq": 42, "payload": {"orderId": "ord_01HZX", "status": "PAID"}}
{"type": "error", "correlationId": "c-1", "payload": {"code": "FORBIDDEN", "message": "Not allowed to subscribe to this order"}}
```

## Liveness and Reconnect

- Use protocol ping/pong frames or application heartbeats; define interval and timeout.
- Proxies and load balancers close idle connections; set heartbeat below their idle timeout.
- Clients reconnect with exponential backoff and jitter.
- Resume: messages carry a monotonically increasing sequence number or cursor; on reconnect the client sends its last-seen value; the server replays within a documented retention window or signals that a full resync is needed.
- Replayed messages must be safe to process twice (carry identifiers; consumers de-duplicate).

**Example:** resume after reconnect.

```json
{ "type": "resume", "id": "c-2", "payload": { "lastSeq": 42 } }
```

The server replays events with `seq` greater than 42 if they are inside the retention window, otherwise it sends `{"type": "resync-required"}`.

## Flow Control and Limits

- Bound outgoing buffers per connection; define the slow-consumer policy (drop, coalesce, or close).
- Declare maximum message size, maximum frame rate per connection, maximum connections per identity, and maximum subscriptions per connection.
- Reject oversized or malformed messages with close code 1009 or 1007.
- TCP flow control exists, but the WebSocket protocol does not provide an application-level demand/acknowledgement mechanism. Bound application queues and define slow-consumer behavior; do not claim transport flow control prevents unbounded buffering.

## Close Codes

| Code      | Meaning                                                                            |
| --------- | ---------------------------------------------------------------------------------- |
| 1000      | Normal closure                                                                     |
| 1001      | Endpoint going away                                                                |
| 1002      | Protocol error                                                                     |
| 1003      | Unsupported data type                                                              |
| 1007      | Invalid payload data                                                               |
| 1008      | Policy violation (for example authentication or authorization failure, rate limit) |
| 1009      | Message too big                                                                    |
| 1010      | Missing mandatory extension                                                        |
| 1011      | Internal server error                                                              |
| 4000–4999 | Application-defined; document each used code and whether the client may reconnect  |

- 1005, 1006, and 1015 are reserved and never sent in a close frame.
- The close reason is a short string; keep it free of internal detail.

## Evolution

- Additive message types and fields are compatible when clients ignore unknown `type` values and unknown fields.
- Removing or changing a message type or field meaning is breaking: publish a new subprotocol version and run both during migration.

## Contract Mapping

- AsyncAPI: `servers` (protocol `ws`/`wss`), one `channel` per logical endpoint with the WebSockets channel binding, `operations` with `send`/`receive` actions, `messages` with `payload` schemas, `correlationId` for request-reply.
- Document authentication, heartbeat, resume, limits, and application close codes in the relevant AsyncAPI server, channel, operation, or message descriptions, or in linked connection documentation. Define runtime enforcement separately.

## Anti-Patterns

- WebSocket for infrequent request-response calls.
- No heartbeat, no reconnect or resume design.
- Tokens in URLs with long lifetimes.
- Authenticating the connection but not authorizing messages.
- Unbounded send queues and no message size limit.
- Untyped messages with no `type` or version.
- Skipping the `Origin` check for browser clients.

## Checklist

- [ ] Fit justified over SSE and REST.
- [ ] Subprotocol named and versioned.
- [ ] Authentication method, expiry handling, and per-message authorization defined.
- [ ] Envelope, message types, and directions listed.
- [ ] Heartbeat, reconnect, and resume rules defined.
- [ ] Size, rate, connection, and subscription limits declared.
- [ ] Close codes documented.
- [ ] `Origin` validation specified.
