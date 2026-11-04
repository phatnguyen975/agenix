# Idempotency, Retries, Concurrency

## Scope

- Making operations safe to retry and safe under concurrent writers.
- `Idempotency-Key` is an IETF Internet-Draft (`draft-ietf-httpapi-idempotency-key-header-08`), not an RFC; its name is widely used by existing APIs. When adopting the draft syntax, identify its status in the relevant parameter/header description or linked consumer documentation and verify the current revision.

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
- Apply keys where callers may retry a non-idempotent side effect and a natural unique constraint is insufficient. Do not add keys mechanically to every POST/PATCH or require them on naturally idempotent operations.

## Server Behavior

- Look up the key scoped by caller identity and operation (composite lookup key), never by the raw client key alone.
- Validate the key against the published format before using it.
- Atomically claim the key before performing side effects (insert-if-absent); prevent two concurrent requests from both executing.
- Store the request fingerprint (checksum of the payload or of selected fields) with the key.
- Outcomes (the IETF draft describes 409 for a concurrent request, 422 for key reuse with a different payload, and recommends 400 when a required key is missing; these are draft recommendations, not universal HTTP requirements):
  | Situation                                      | Behavior                                                                                                                                                                                                      |
  | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | First request                                  | Process normally; store the result under the key                                                                                                                                                              |
  | Retry after a completed, deterministic outcome | Replay the stored status and response for that outcome; do not turn a transient or uncertain infrastructure failure into a final cached result                                                                |
  | Retry while the original is in flight          | A documented policy: 409 Conflict, wait for the first result, or return an operation reference (for example 202); choose one. Revision -08 of the current IETF draft describes 409 for concurrent processing. |
  | Same key, different payload                    | Reject with a stable client error; revision -08 of the current IETF draft describes 422.                                                                                                                      |
  | Key required but missing                       | 400 with a pointer to documentation                                                                                                                                                                           |
- Retention covers the documented client retry horizon plus reasonable network/queue delay. State the expiry behavior; after expiry, the same key may be treated as a new operation only if documented. Persist the key and result durably enough to survive the failures the API claims to handle.
- Define which outcomes are replayed. Persist completed deterministic results; for unknown outcomes (for example a timeout after a downstream side effect) reconcile or retain an in-progress/unknown state rather than blindly executing again. Do not replay transient infrastructure failures as a final business result unless explicitly intended.
- In-flight claims need lease/recovery semantics so a crashed worker does not block a key forever; recovery must not permit duplicate side effects after an uncertain commit.

**Example:** sequence for `POST /orders` with key `K`.

| Step | Request                                | Response                                                |
| ---- | -------------------------------------- | ------------------------------------------------------- |
| 1    | `K`, payload `P`                       | `201`, order `A` created                                |
| 2    | `K`, payload `P` (retry after timeout) | `201`, the stored result for order `A`; no second order |
| 3    | `K` while step 1 is still running      | `409`                                                   |
| 4    | `K`, payload `P2`                      | `422`                                                   |
| 5    | no key, key required                   | `400`                                                   |

## Non-HTTP Protocols

- **gRPC:** a client-generated `request_id` field in the request message; apply the same scope, fingerprint, retention, atomic-claim, and replay rules.
- **GraphQL:** use a purpose-defined idempotency key in the mutation input. A Relay-style `clientMutationId` is a correlation convention and does not provide idempotency unless the server explicitly defines it that way.
- **WebSocket:** give retryable client commands a stable identifier and define server-side de-duplication; make replayed server messages safe to process twice when the protocol supports resume.
- **SSE:** use event IDs for stream resume; clients handle replayed events idempotently or de-duplicate them by event ID. SSE is server-to-client, so client commands use a separate HTTP operation.
- **Messaging:** when delivery or replay can produce duplicates, give messages stable IDs; consumers record processed identifiers transactionally or apply version-checked upserts.
- **Webhooks:** deliveries carry a stable event `id`; consumers de-duplicate.

## Retries

- Retry only idempotent operations, or non-idempotent ones protected by a key.
- Retryable HTTP outcomes include connection failures, 408, 429 (honor `Retry-After`), 502, 503 (honor `Retry-After`), and 504. Retry 500 only when the operation is idempotent or protected by a functioning idempotency mechanism.
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

- **OpenAPI:** define `Idempotency-Key` only on operations that support it. When adopting draft `-08`, model its wire value as a Structured Field String (including the surrounding quotes) and label the field as an Internet-Draft convention, not an RFC; specify key format, scope, fingerprint, and retention. Declare the applicable 400, 409, and 422 outcomes. For optimistic concurrency, define `ETag`, `If-Match`, and applicable 412/428 responses.
- **Protobuf:** `request_id` and `etag`/`version` fields documented in comments.
- **AsyncAPI:** message `id` header and consumer de-duplication note in the operation description.
- Identify the draft status where the field is defined or in linked consumer documentation; do not imply draft syntax is a finalized RFC.

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
- [ ] Duplicate-capable message channels and webhook deliveries have stable identifiers and a consumer de-duplication strategy.
- [ ] Draft status of `Idempotency-Key` is noted.
