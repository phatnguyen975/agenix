# Idempotency, Retries, Concurrency

## Contents

- Scope
- Method Semantics
- Idempotency Keys
- Server Behavior
- Non-HTTP Protocols
- Retries
- Optimistic Concurrency
- Contract Mapping
- Anti-Patterns
- Checklist
- Sources

## Scope

- Making operations safe to retry and safe under concurrent writers.
- `Idempotency-Key` is an IETF draft (`draft-ietf-httpapi-idempotency-key-header`); label it in the header notes. Its header name is widely used by existing APIs.

## Method Semantics

- HTTP (RFC 9110): GET, HEAD, OPTIONS, PUT, DELETE are idempotent; POST and PATCH are not by default.
- Idempotent means repeating the request has the same intended effect on the server as one request; responses may differ.
- Design PUT and DELETE to be idempotent; design POST and PATCH that clients may retry to be made idempotent with a key or a natural unique constraint.
- Safe methods change no state.

## Idempotency Keys

- The client generates a unique value per logical operation and sends it with every retry of that operation.
- HTTP header: `Idempotency-Key`; value is a Structured Field String, quoted: `Idempotency-Key: "8e03978e-40d5-43e8-bc93-6894a57f9324"`.
- Use a UUID or another high-entropy random value; low-entropy keys let attackers guess other clients' keys.
- A key must not be reused with a different request payload.
- The provider publishes: which operations require a key, the key format, and the expiry policy.
- Apply keys to non-idempotent operations (POST, PATCH); do not require them on naturally idempotent methods.

## Server Behavior

- Look up the key scoped by caller identity and operation (composite lookup key), never by the raw client key alone.
- Validate the key against the published format before using it.
- Atomically claim the key before performing side effects (insert-if-absent); prevent two concurrent requests from both executing.
- Store the request fingerprint (checksum of the payload or of selected fields) with the key.
- Outcomes:

| Situation                             | Behavior                                                             |
| ------------------------------------- | -------------------------------------------------------------------- |
| First request                         | Process normally; store the result under the key                     |
| Retry after completion                | Return the stored result, success or error, with the original status |
| Retry while the original is in flight | 409 Conflict                                                         |
| Same key, different payload           | 422                                                                  |
| Key required but missing              | 400 with a pointer to documentation                                  |

- Retention covers at least the longest period over which clients retry; delete expired keys.
- Store results for failed operations too when the failure is deterministic; do not store transient infrastructure failures as final results.
- The in-flight claim has a timeout so a crashed request does not block the key forever.

Example sequence for `POST /orders` with key `K`:

| Step | Request                                | Response                                                |
| ---- | -------------------------------------- | ------------------------------------------------------- |
| 1    | `K`, payload `P`                       | `201`, order `A` created                                |
| 2    | `K`, payload `P` (retry after timeout) | `201`, the stored result for order `A`; no second order |
| 3    | `K` while step 1 is still running      | `409`                                                   |
| 4    | `K`, payload `P2`                      | `422`                                                   |
| 5    | no key, key required                   | `400`                                                   |

## Non-HTTP Protocols

- gRPC: a client-generated `request_id` field in the request message; same server rules.
- GraphQL: a client-supplied identifier in the mutation input.
- WebSocket and SSE: message `id` for client commands; server de-duplicates; replay safe by identifier.
- Messaging: every message has a stable `id`; consumers record processed identifiers (inbox) or apply version-checked upserts.
- Webhooks: deliveries carry a stable event `id`; consumers de-duplicate.

## Retries

- Retry only idempotent operations, or non-idempotent ones protected by a key.
- Retryable HTTP outcomes: connection failures, 408, 429 (honor `Retry-After`), 502, 503 (honor `Retry-After`), 504; 500 only for idempotent operations.
- Do not retry 4xx other than 408, 429, and, for conflicts, after correcting the request.
- gRPC: `UNAVAILABLE`; `DEADLINE_EXCEEDED` and `RESOURCE_EXHAUSTED` only when safe and with backoff.
- Exponential backoff with jitter, capped attempts, capped total time.
- Overall retry budget per client to avoid retry storms; retries at only one layer of the call chain.
- Providers state which operations are safe to retry and the expected behavior on timeout.

## Optimistic Concurrency

- Resources that concurrent clients update expose a version: HTTP `ETag` (strong validator) or a `version` field.
- Updates send the version: `If-Match` with the `ETag`.
- Mismatch returns 412 Precondition Failed; resources requiring preconditions return 428 when the header is absent.
- Create-only semantics: `If-None-Match: *`.
- Non-HTTP protocols carry the expected version in the request message and return a conflict error (`ABORTED` in gRPC).
- Last-write-wins is allowed only when documented and acceptable for the resource.
- Prefer optimistic concurrency over locks; avoid long-lived locks across requests.

```http
GET /orders/ord_1            ->  200, ETag: "3"
PATCH /orders/ord_1          If-Match: "3"  ->  200, ETag: "4"
PATCH /orders/ord_1          If-Match: "3"  ->  412 Precondition Failed
```

## Contract Mapping

- OpenAPI: `Idempotency-Key` as a header parameter (string, format and length bounds) on each operation that supports it; responses 400, 409, 422 declared; `ETag` response header and `If-Match` request header; 412 and 428 responses.
- Protobuf: `request_id` and `etag`/`version` fields documented in comments.
- AsyncAPI: message `id` header and consumer de-duplication note in the operation description.
- Header notes: record the draft status of `Idempotency-Key`.

## Anti-Patterns

- Retrying non-idempotent calls without a key.
- Keys scoped globally (cross-client collisions and leaks).
- Executing before the key is claimed; check-then-act races.
- Returning a new result for a repeated key.
- No expiry policy.
- Lost updates because writes carry no version.
- Retrying at every layer, multiplying load.

## Checklist

- [ ] Every non-idempotent operation clients may retry has a key or unique-constraint strategy.
- [ ] Key format, scope, retention, and outcomes are documented.
- [ ] Retry guidance (statuses, backoff, limits) is documented.
- [ ] Concurrent updates use `ETag`/`If-Match` or a version field.
- [ ] Consumers of messages and webhooks de-duplicate by identifier.
- [ ] Draft status of `Idempotency-Key` is noted.

## Sources

- RFC 9110 (method semantics, conditional requests), RFC 6585 (428).
- `draft-ietf-httpapi-idempotency-key-header`.
- gRPC retry and status documentation; Google API Improvement Proposals (request identification, retries).
