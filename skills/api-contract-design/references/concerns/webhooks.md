# Webhooks

## Scope

- HTTP callbacks sent by a provider to consumer-hosted endpoints when events occur.
- Header names and signature scheme follow the Standard Webhooks convention when the project has no other rule; confirm field names against that specification before use.

## Event Design

- Event type names: `resource.action`, lowercase, past tense for facts (`invoice.paid`); stable once published.
- Payload envelope fields: `id` (unique event identifier, stable across redelivery), `type`, `createdAt` (RFC 3339), `apiVersion` or schema version, `data` (the resource or change).
- Alternative: CloudEvents structured or binary HTTP mode, when the project uses CloudEvents.
- Thin payloads (identifiers, consumers fetch current state) reduce exposure and ordering problems; fat payloads (full state) save a round trip. Choose per event type and document it.
- No ordering guarantee unless documented; include an aggregate sequence/version when consumers must detect gaps or discard stale events. A timestamp alone does not establish a total order.
- Publish a catalogue of event types with schemas.

| Event Type        | Payload Kind           | Schema       |
| ----------------- | ---------------------- | ------------ |
| `order.paid`      | Fat (full order)       | `OrderEvent` |
| `order.cancelled` | Thin (identifier only) | `OrderRef`   |

## Subscription Management

- A normal authenticated API: create, list, get, update, delete subscriptions.
- Subscription fields: endpoint URL (HTTPS), event types (filter), status, signing secret (returned once at creation, rotatable), optional description.
- Validate endpoint URLs (HTTPS, no internal or link-local targets, no credentials in URL).
- Optional endpoint verification: send a test event or challenge before enabling.
- Provide operations to send a test event, list delivery attempts, and redeliver an event.
- Secret rotation: accept signatures from old and new secrets during an overlap period.

## Delivery

- **Semantics:** at least once; duplicates occur.
- **Success:** any 2xx unless the provider contract defines a narrower acknowledgement. A 2xx means the receiver accepted responsibility for processing, not necessarily that the business action completed. Anything else, including timeouts and connection errors, is a failed delivery attempt.
- **Retries:** exponential backoff with jitter over a documented horizon (for example hours to days), then mark the delivery failed.
- Provider sends `POST` with `Content-Type: application/json`, a bounded payload size, and a short timeout.
- Disable endpoints that fail continuously beyond a threshold; notify the subscriber; allow re-enable and replay.
- Delivery attempts are logged and visible to subscribers (status, response code, time).
- Do not follow redirects blindly; treat 3xx as failure unless documented.
- Rate-limit outbound deliveries per subscriber; isolate slow endpoints so they do not delay others.

## Security

- Sign every delivery. Standard Webhooks scheme:
  - `webhook-id`: message identifier.
  - `webhook-timestamp`: Unix seconds.
  - `webhook-signature`: one or more space-separated signatures such as `v1,<base64 HMAC-SHA256>`.
  - Signed content: `<id>.<timestamp>.<raw body>`, using the endpoint secret.
- Consumers verify the exact raw body bytes before parsing or re-serializing JSON, compare signatures in constant time, and reject timestamps outside the documented tolerance window. Define how multiple signatures are handled during secret rotation.
- HTTPS only; secrets are per subscription, high entropy, stored securely.
- Optionally publish source IP ranges or support mutual TLS as additional controls, not as replacements for signatures.
- SSRF controls on every registered URL (see API security).
- Payloads contain the minimum personal data; sensitive data is fetched through authenticated APIs.

```http
POST /hooks/orders HTTP/1.1
Content-Type: application/json
webhook-id: msg_2KWPBgLlAfxdpx2AI54pPJ85f4W
webhook-timestamp: 1772357400
webhook-signature: v1,<base64-hmac-sha256>

{"id": "evt_01HZY", "type": "order.paid", "createdAt": "2026-03-01T09:30:00Z", "apiVersion": "2026-03-01", "data": {"id": "ord_01HZX", "status": "PAID"}}
```

Verification procedure for the consumer:

1. Keep the raw body bytes unchanged.
2. Build the signed content: `<webhook-id>.<webhook-timestamp>.<raw body>`.
3. Compute HMAC-SHA256 with the endpoint secret; encode as base64.
4. Compare to each `v1,` signature in the header using a constant-time comparison.
5. Reject the delivery when the timestamp is outside the tolerance window.

## Versioning

- Include the payload version in each event or pin a version per subscription.
- Additive changes (new fields, new event types) are compatible; consumers ignore unknown fields and event types.
- Breaking changes require a new version and a migration window with both versions delivered.

## Consumer Rules

- Verify the signature before parsing the body.
- Respond with 2xx quickly; process asynchronously after acknowledging.
- De-duplicate by event `id`; handle out-of-order delivery using timestamps or versions.
- Treat unknown event types as ignorable.
- Reconcile periodically through the provider's list API for missed events.

## Contract Mapping

- OpenAPI `webhooks`: one entry per event type; each is a path item with a `post` operation, request body schema (envelope + `data`), documented signature headers as header parameters, and 2xx and error responses expected from the consumer.
- OpenAPI `callbacks`: for callback URLs supplied per request, with runtime expressions for the URL.
- Subscription management lives in `paths` as ordinary operations.
- Under AsyncAPI-based projects, model webhooks as `send` operations over an `http` channel.
- Document the signing scheme and its status where it affects consumer verification, and describe delivery retry behavior at the webhook operation or in linked integration documentation. Keep delivery-log retention policy internal unless it affects consumer obligations.

## Anti-Patterns

- Unsigned webhooks; static shared secrets across all subscribers.
- Signing the parsed rather than the raw body.
- No replay protection; no timestamp.
- Assuming exactly-once or ordered delivery.
- Long synchronous processing in the receiver.
- Unbounded retries; no endpoint disablement.
- Registering arbitrary URLs without validation.

## Checklist

- [ ] Event catalogue with schemas and stable names.
- [ ] Subscription API with secret handling and rotation.
- [ ] Delivery semantics, timeout, retry horizon, and disablement defined.
- [ ] Signature scheme and replay window defined.
- [ ] Duplicate and ordering behavior documented.
- [ ] URL validation (SSRF) defined.
- [ ] Versioning and compatibility rules defined.
