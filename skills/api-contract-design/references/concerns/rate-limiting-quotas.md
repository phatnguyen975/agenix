# Rate Limiting and Quotas

## Contents

- Scope
- Concepts
- Limit Design
- HTTP Signaling
- Per-Protocol Rules
- Client Guidance
- Contract Mapping
- Anti-Patterns
- Checklist
- Sources

## Scope

- Protecting capacity and fairness, and telling clients how to behave under limits.
- `RateLimit` and `RateLimit-Policy` fields are an IETF draft (`draft-ietf-httpapi-ratelimit-headers`); label them in the header notes.

## Concepts

| Term              | Meaning                                                     |
| ----------------- | ----------------------------------------------------------- |
| Rate limit        | Maximum requests (or cost) per time window                  |
| Quota             | Allocation over a long period, usually tied to a plan       |
| Concurrency limit | Maximum simultaneous requests, streams, or connections      |
| Payload limit     | Maximum request or message size                             |
| Cost limit        | Budget of weighted units where operations differ in expense |

## Limit Design

- Choose limit keys: client application, user, tenant, operation, or a combination; IP address alone is weak (shared and spoofable) and is used as a supplement.
- Separate limits for authentication endpoints and expensive operations.
- Provide both burst and sustained limits (short and long windows).
- Weight operations by cost when cost varies widely (search, export, GraphQL complexity).
- Common limiting approaches: fixed window, sliding window, token bucket, leaky bucket, concurrency limits; choose by fairness and burst needs and document the observable behavior.
- Limits are documented per operation or per tier; undocumented limits become surprise failures.
- Distinguish client faults (429) from server overload (503).

## HTTP Signaling

- 429 Too Many Requests for client-attributable limits (RFC 6585); 503 Service Unavailable for server overload; both may carry `Retry-After` (seconds or HTTP-date, RFC 9110).
- Draft fields (Structured Field Lists):
  - `RateLimit-Policy: "burst";q=100;w=60,"daily";q=1000;w=86400`: policy name, `q` quota (required), `qu` quota unit (`requests`, `content-bytes`, `concurrent-requests`), `w` window in seconds, `pk` partition key.
  - `RateLimit: "default";r=50;t=30`: policy name, `r` remaining quota (required), `t` seconds until the effective window ends, `pk` partition key.
- The fields may be sent on any response, not only 429.
- Remaining quota is a hint, not a guarantee; servers may throttle earlier.
- With both `Retry-After` and `RateLimit`, `Retry-After` takes precedence; do not point it earlier than the effective window end.
- Add jitter to reset times so throttled clients do not return simultaneously.
- Draft problem types for errors: `https://iana.org/assignments/http-problem-types#quota-exceeded` (429), `#temporary-reduced-capacity` (503), `#abnormal-usage-detected` (429), with a `violated-policies` extension member listing policy names.
- Legacy `X-RateLimit-Limit`, `-Remaining`, `-Reset` headers have inconsistent semantics across vendors; use them only when the project already does, and document their units.
- Do not expose operational capacity details to untrusted callers beyond what clients need.
- Every limit is enforced server-side regardless of the headers published.

```http
HTTP/1.1 200 OK
RateLimit-Policy: "default";q=600;w=60
RateLimit: "default";r=599;t=60
```

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/problem+json
Retry-After: 30
RateLimit-Policy: "burst";q=100;w=60
RateLimit: "burst";r=0;t=30

{
  "type": "https://iana.org/assignments/http-problem-types#quota-exceeded",
  "title": "Quota exceeded",
  "status": 429,
  "violated-policies": ["burst"]
}
```

## Per-Protocol Rules

- **REST**: 429 or 503 with the signaling above.
- **GraphQL**: cost or complexity budgets per operation; depth limits; per-identity request rate; report remaining budget in `extensions`.
- **gRPC**: `RESOURCE_EXHAUSTED` with `RetryInfo` (retry delay) and `QuotaFailure` details; `UNAVAILABLE` for overload.
- **WebSocket**: per-connection message rate, maximum connections and subscriptions per identity; close with 1008 or an application code, and document whether reconnect is allowed.
- **SSE**: maximum concurrent streams per identity; 429 on connect.
- **Messaging**: producer quotas and maximum message size at the broker; consumer prefetch and concurrency limits; overflow policy.
- **Webhooks**: outbound delivery rate per subscriber and backoff on failing endpoints.

## Client Guidance

- Honor `Retry-After`; otherwise exponential backoff with jitter.
- Pre-emptively slow down when remaining quota is low.
- Treat malformed or absent `RateLimit` fields as no information.
- Cap how long a client will wait on a server-provided delay.
- Never retry immediately in a loop.

## Contract Mapping

- OpenAPI: `429` and `503` responses with `Retry-After`, `RateLimit`, `RateLimit-Policy` header definitions in `components.headers`; Problem Details schema with `violated-policies`.
- Protobuf and GraphQL SDL: describe limits in comments and header notes; gRPC lists `RESOURCE_EXHAUSTED` per method.
- AsyncAPI: limits in channel and server descriptions and binding settings.
- Header notes: the limits policy and the draft status of the fields.

## Anti-Patterns

- No limits on public or expensive operations.
- Limits only by IP.
- 200 responses with throttling text; 429 without `Retry-After` guidance.
- Fixed reset times that synchronize all clients.
- Publishing limits that the server does not enforce, or enforcing unpublished limits.
- Client retry loops without delay.

## Checklist

- [ ] Limit keys, windows, and costs defined per operation or tier.
- [ ] Overload (503) and client limit (429) distinguished.
- [ ] Response headers and error shape defined.
- [ ] Streams, connections, and subscriptions have concurrency limits.
- [ ] Client backoff guidance documented.
- [ ] Draft header status noted.

## Sources

- RFC 6585 (429), RFC 9110 (`Retry-After`), RFC 9651 (Structured Fields).
- `draft-ietf-httpapi-ratelimit-headers`.
- gRPC status codes and `google.rpc` error details.
