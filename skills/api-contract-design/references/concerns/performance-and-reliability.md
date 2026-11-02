# Performance and Reliability

## Contents

- Scope
- Caching
- Payload Efficiency
- Timeouts and Deadlines
- Resilience
- Observability
- Service Objectives
- Contract Mapping
- Anti-Patterns
- Checklist
- Sources

## Scope

- Contract-level decisions that determine latency, load, and failure behavior: caching, payload size, timeouts, resilience, and observability fields.

## Caching

- Only safe methods are cacheable in practice; design cacheable reads as GET.
- `Cache-Control` directives:

| Directive                                             | Use                                               |
| ----------------------------------------------------- | ------------------------------------------------- |
| `max-age`, `s-maxage`                                 | Freshness lifetime; `s-maxage` for shared caches  |
| `private`                                             | User-specific data                                |
| `no-store`                                            | Sensitive data                                    |
| `no-cache`                                            | Cache may store, but must revalidate before reuse |
| `stale-while-revalidate`, `stale-if-error` (RFC 5861) | Acceptable staleness windows                      |

- Validators: `ETag` (and `Last-Modified`); clients revalidate with `If-None-Match` or `If-Modified-Since`; servers return 304 with no body.
- `Vary` lists the request headers that change the representation (`Accept`, `Accept-Language`, `Authorization` for per-user caching rules).
- Declare cache behavior in the contract for every cacheable operation.
- GraphQL and POST-based reads need explicit cache design (persisted operations over GET, application-level caching).
- Authorization applies before cache use; shared caches never serve one user's private data to another.

| Response                                         | Header                                             |
| ------------------------------------------------ | -------------------------------------------------- |
| Public catalog, tolerates 5 minutes of staleness | `Cache-Control: public, max-age=300`               |
| User-specific resource, must revalidate          | `Cache-Control: private, no-cache` and `ETag: "4"` |
| Sensitive data                                   | `Cache-Control: no-store`                          |

```http
GET /orders/ord_1 HTTP/1.1
If-None-Match: "4"

HTTP/1.1 304 Not Modified
ETag: "4"
```

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

- Propagate W3C Trace Context (`traceparent`, `tracestate`) across HTTP, gRPC metadata, and message headers.
- Return or log a request identifier; include it in error responses (`instance` or an extension member).
- Contracts declare which correlation headers are accepted and returned.
- Standard signals per operation: request rate, error rate, latency distribution (rate, errors, duration).
- Logs contain identifiers and outcomes, not payloads or secrets.

```http
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
```

## Service Objectives

- State per operation or per API: availability target, latency percentiles (for example p50, p95, p99), and error budget basis.
- Distinguish targets from guarantees; document what clients can rely on.
- Publish maintenance and deprecation windows.

| Operation      | Objective                                            |
| -------------- | ---------------------------------------------------- |
| `GET /orders`  | p95 latency under 300 ms; 99.9% monthly availability |
| `POST /orders` | p99 latency under 2 s; 99.9% monthly availability    |

## Contract Mapping

- OpenAPI: response headers `Cache-Control`, `ETag`, `Last-Modified`, `Vary`, `Retry-After`; request headers `If-None-Match`, `If-Modified-Since`, `traceparent`; 304 response; descriptions with duration and objective statements.
- Protobuf: deadline and idempotency notes in RPC comments; health service definition when deployed.
- AsyncAPI: message headers for trace context; channel descriptions for latency and retention expectations.
- Header notes: service objectives and non-expressible reliability rules.

## Anti-Patterns

- No timeouts; unlimited retries; per-layer retries.
- Caching responses that contain user-specific data in shared caches.
- Large unbounded responses; N+1 call patterns.
- Health endpoints that leak internals or always return OK.
- Objectives stated as guarantees.
- Dropping trace context at protocol boundaries.

## Checklist

- [ ] Cacheability and validators defined for each read.
- [ ] Payload maximums and pagination defined.
- [ ] Timeout or deadline and expected duration stated per operation.
- [ ] Degraded behavior documented.
- [ ] Trace context and request identifier propagation defined.
- [ ] Objectives stated with percentiles.

## Sources

- RFC 9111 (HTTP Caching), RFC 9110 (conditional requests, content coding), RFC 5861.
- W3C Trace Context.
- gRPC documentation: deadlines, health checking, retry.
