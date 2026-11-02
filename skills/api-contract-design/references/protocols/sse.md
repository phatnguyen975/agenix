# Server-Sent Events (SSE)

## Scope

- One-way server-to-client event streams over HTTP, using the `text/event-stream` media type defined in the WHATWG HTML Standard.
- Covers stream format, event design, resume, authentication, and limits.

## Fit

- Use for notifications, progress, live feeds, and long-running operation updates.
- The client sends commands through separate HTTP requests; the stream carries server events only.
- For bidirectional low-latency exchange, use WebSocket.

## Stream Format

- Response `Content-Type: text/event-stream`, UTF-8, status 200.
- Each event is a block of `field: value` lines ended by a blank line.
- Fields: `event` (event type name), `data` (payload; multiple `data` lines are joined with newlines), `id` (event identifier), `retry` (reconnection delay in milliseconds).
- Lines beginning with `:` are comments; use them as keep-alive heartbeats.
- Send `Cache-Control: no-cache`; make sure proxies and compression layers do not buffer the stream.
- HTTP 204 tells the client to stop reconnecting; other non-200 responses or a wrong content type fail the connection.

Example stream (each event ends with a blank line; lines starting with `:` are comments).

```
: heartbeat

id: 41
event: order.updated
data: {"orderId": "ord_01HZX", "status": "PAID"}

retry: 5000

```

## Event Design

- `event` names the event type (`order.updated`); omit it only when a single type exists.
- `data` holds one JSON object per event; declare its schema per event type.
- `id` is unique and ordered within the stream scope so clients can resume.
- Keep events small; send identifiers and let clients fetch large state over REST when needed.
- Define a terminal event or closure convention for finite streams.
- Define whether events are ordered, and whether duplicates can occur after reconnect.

## Resume and Reconnect

- On reconnect the client sends the `Last-Event-ID` request header with the last received `id`.
- The server replays events after that `id` within a documented retention window; if the window is exceeded, send a resync-required event or reject with a documented status.
- Set `retry` to control client reconnect delay; add server-side jitter guidance to avoid reconnect storms.
- Replayed events must be safe to process twice.

**Example:** reconnect request after the connection dropped.

```http
GET /orders/ord_01HZX/events HTTP/1.1
Accept: text/event-stream
Last-Event-ID: 41
```

The server sends the events that follow `41`, then continues live.

## Authentication and Transport

- Native browser `EventSource` supports `GET` only and no custom request headers; authenticate with cookies, or use a fetch-based client that can send `Authorization`.
- Avoid long-lived credentials in query strings.
- Authorize the stream at connect time and re-check when permissions change or credentials expire; close the stream on revocation.
- HTTP/1.1 browsers limit concurrent connections per origin; HTTP/2 multiplexing relaxes this. Count open streams per client in your limits.

## Limits and Lifecycle

- Declare maximum stream duration; close politely and let clients reconnect so load can rebalance.
- Declare maximum concurrent streams per identity and per tenant.
- Heartbeat interval below the shortest idle timeout of any intermediary.
- Slow clients: bound per-connection queues; drop or close.

## Contract Mapping

- OpenAPI 3.2: a `get` operation whose 200 response has `content: text/event-stream` with `itemSchema` describing one event (`event`, `data`, `id`, `retry` properties); `data` can use `contentMediaType` and `contentSchema` for its JSON structure.
- Under OpenAPI 3.1 there is no `itemSchema`: describe the event format in the description and keep schemas in `components`.
- Document `Last-Event-ID` as a request header parameter.
- Retention window, heartbeat, and limits go in the operation description and header notes.

## Anti-Patterns

- SSE for traffic that needs client-to-server messages on the same channel.
- No event ids, so resume is impossible.
- Unbounded replay or unbounded per-client buffers.
- Credentials in query strings with long lifetimes.
- Proxy buffering left enabled, delaying events.
- One endless stream per client without duration limits.

## Checklist

- [ ] Event types and their `data` schemas are listed.
- [ ] `id` semantics and replay window are defined.
- [ ] Heartbeat and `retry` values are defined.
- [ ] Authentication works for the intended client (cookie or fetch-based).
- [ ] Stream duration and concurrency limits are declared.
- [ ] Contract uses `itemSchema` (3.2) or documents the format (3.1).
