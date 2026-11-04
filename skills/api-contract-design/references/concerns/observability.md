# API Observability

## Scope

- Consumer-visible correlation and operational signals that must cross API boundaries. Internal telemetry implementation and dashboard design are out of scope.
- Keep observability metadata distinct from business data, authentication identity, and idempotency keys.

## Correlation and Trace Context

- Propagate W3C Trace Context (`traceparent`, and `tracestate` when used) across HTTP, gRPC metadata, and message headers. Validate syntax and apply trust policy at ingress; do not blindly trust caller-supplied trace metadata.
- A trace ID identifies a distributed trace, not a user, tenant, authorization token, or durable business operation. Never use it as a security or idempotency key.
- Use a server-generated request/correlation identifier for support diagnostics when a trace may not exist. Define whether the identifier is accepted from clients, returned in headers, or exposed in errors.
- Keep correlation values opaque and bounded. If the server accepts an incoming request ID, validate its length/character set and decide whether to replace it or preserve it in a separate client-correlation field.

**Example:**

```http
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
X-Request-Id: req_01J2K8M4
```

`X-Request-Id` is an illustrative project convention, not a standardized field. Choose one name or use the project's existing convention.

## Logs and Audit Events

- Define which identifiers are available for support correlation: request ID, trace ID, operation/RPC name, resource ID, message/event ID, and outcome.
- Logs should record outcome, latency, and safe identifiers—not credentials, access tokens, complete request bodies, or sensitive response fields.
- Audit events are a separate business/security record. Specify actor, action, target, result, timestamp, and relevant authorization context; do not assume request logs satisfy audit requirements.
- If the API exposes an audit/event feed, define its access controls, retention, ordering, and tamper-evidence expectations as part of that event contract.

## Metrics

- Use bounded dimensions such as operation name, status class, protocol, and dependency name. Do not label metrics with unbounded user IDs, request IDs, raw URLs, search terms, or arbitrary error messages.
- Define service-level indicators that consumers or operators need: request rate, error rate, latency distribution, saturation/concurrency, dependency failure, stream disconnects, and message processing lag where applicable.
- State objectives as targets with a measurement window and percentile, not unconditional guarantees. Link to the project SLO policy instead of duplicating internal dashboards in the API contract.
- Do not expose detailed internal metrics publicly unless the API product intentionally provides them.

## Streams and Messaging

- For long-lived streams, define connection/session identifiers, reconnect correlation, resume cursor/sequence, replay window, and how the client detects a gap.
- For messaging, propagate trace context in message headers using the chosen transport binding; state whether a producer trace continues into consumer processing or a new trace is linked.
- Webhooks should carry a stable event ID for delivery de-duplication. Do not use a trace ID as the event's stable identity.

## Contract Mapping

- **OpenAPI:** document accepted/returned correlation headers; add response request-reference fields only when consumers need them. Do not model standard tracing headers as authentication.
- **Protobuf/gRPC:** define metadata conventions and any request ID fields in RPC comments or an API profile; metadata is not part of the Protobuf message unless the application needs it as data.
- **AsyncAPI:** define trace headers and message/event identifiers in message headers; document propagation behavior at the operation/channel level.
- **GraphQL:** expose a request reference in response extensions only when consumers need it; keep tracing identifiers out of domain object fields by default.
- **SSE/WebSocket:** define connection and event correlation separately; reconnect/resume identifiers must have explicit replay semantics.

## Privacy and Cardinality

- Treat trace and request identifiers as potentially sensitive metadata; apply retention, access, and redaction controls.
- Never include secrets or personal data in baggage, trace state, message headers, URLs, metric labels, or error text.
- Propagate only fields that have a clear consumer or operational need; remove or redact untrusted metadata at trust boundaries.

## Anti-Patterns

- Treating trace IDs as authorization or idempotency tokens.
- Logging full payloads by default.
- High-cardinality metric labels containing IDs or arbitrary input.
- Treating operational logs as an audit trail without integrity and retention guarantees.
- Dropping trace context at protocol boundaries or trusting it without validation.

## Checklist

- [ ] Correlation and trace propagation are defined at relevant protocol boundaries.
- [ ] Request IDs, event IDs, and trace IDs have distinct purposes.
- [ ] Logs and audit events have explicit content and privacy rules.
- [ ] Metrics use bounded dimensions and meaningful SLIs.
- [ ] Stream replay and message processing can be correlated without exposing secrets.
