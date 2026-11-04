# Performance and Reliability

## Scope

- Contract-level decisions that determine latency, load, and failure behavior: caching, payload size, timeouts, resilience, and observability fields.

## Caching

Caching policy, validators, and conditional request semantics are covered in `caching-and-conditional-requests.md`. Keep cacheability, freshness, authorization variation, and invalidation explicit for each operation; do not infer cacheability from a read-only method alone.

## Payload Efficiency

- Return only what consumers need: sparse fields, bounded expansion, pagination.
- Avoid chatty designs: provide batch reads, composite resources, or expansion where consumers always need related data.
- Avoid N+1 patterns in the contract design (list endpoints that force one call per item); GraphQL servers batch resolvers.
- Compression: support `Accept-Encoding` with `Content-Encoding` (for example gzip); do not compress secrets mixed with attacker-controlled content over the same channel without evaluating compression-oracle risks.
- Large results use streaming, pagination, or asynchronous export; state payload maximums.
- Binary protocols and HTTP/2 reduce overhead; choose them by measured need.

## Timeouts and Deadlines

- Every call has a timeout or deadline on the client; every server enforces its own maximum processing time.
- Deadlines propagate: downstream calls use the remaining time, not a fresh timeout (gRPC deadlines propagate this way).
- Choose timeouts from the operation's service objective; state expected duration and the maximum in the contract.
- Work exceeding the request budget becomes an asynchronous operation.
- Fail fast when a dependency is known unavailable.

## Resilience

- Idempotent retries with backoff and jitter; bounded budgets; retry at one layer.
- Bulkheads and circuit breakers around dependencies; define degraded behavior (stale data, partial results) and signal it in the response.
- Graceful degradation is documented per operation: what the caller sees when a dependency fails.
- Health signaling: liveness (process is running) and readiness (can serve traffic) separated; gRPC uses the standard Health Checking protocol; HTTP uses documented endpoints that expose no sensitive detail.
- Graceful shutdown: stop accepting, drain in-flight work.
- Backpressure: bounded queues; 429/503 or flow control instead of unbounded buffering.

## Observability

Trace propagation, request correlation, structured logs, metrics cardinality, audit events, and stream-specific telemetry are covered in `observability.md`. Preserve trace context across HTTP, RPC, messaging, and callback boundaries; do not put secrets or high-cardinality identifiers in metric labels.

## Service Objectives

- State per operation or per API: availability target, latency percentiles (for example p50, p95, p99), and error budget basis.
- Distinguish targets from guarantees; document what clients can rely on.
- Publish maintenance and deprecation windows.

| Operation      | Objective                                            |
| -------------- | ---------------------------------------------------- |
| `GET /orders`  | p95 latency under 300 ms; 99.9% monthly availability |
| `POST /orders` | p99 latency under 2 s; 99.9% monthly availability    |

## Contract Mapping

- **OpenAPI:** response headers `Retry-After`; request timeout/deadline guidance in descriptions; define objective statements without implying they are protocol guarantees.
- **Protobuf:** deadline and idempotency notes in RPC comments; health service definition when deployed.
- **AsyncAPI:** channel descriptions for latency, retention, and consumer processing expectations.
- Put consumer-visible timeouts, retry obligations, and reliability guarantees in the relevant operation, RPC, channel, or message documentation. Keep internal SLOs and implementation objectives in service-level documentation unless they create an explicit consumer commitment.

## Anti-Patterns

- No timeouts; unlimited retries; per-layer retries.
- Caching responses that contain user-specific data in shared caches.
- Large unbounded responses; N+1 call patterns.
- Health endpoints that leak internals or always return OK.
- Objectives stated as guarantees.
- Dropping trace context at protocol boundaries.

## Checklist

- [ ] Payload maximums and pagination defined.
- [ ] Timeout or deadline and expected duration stated per operation.
- [ ] Degraded behavior documented.
- [ ] Objectives stated with percentiles.
