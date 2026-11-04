# gRPC

## Scope

- Typed RPC over HTTP/2 described by Protobuf service definitions.
- Covers service and method design, errors, deadlines, retries, streaming, and operational endpoints.

## Service Design

- One service per cohesive capability; avoid one service holding unrelated methods.
- Package carries the major version: `company.domain.v1`.
- Service names are nouns ending in `Service`; method names are verbs in `PascalCase` (`GetOrder`, `CreateOrder`).
- Resource-oriented services use standard methods (`Get`, `List`, `Create`, `Update`, `Delete`) before custom methods.
- Keep the service surface small; each method has one clear purpose.

| Good                                                                | Bad                                                                                                     |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `package company.orders.v1;`                                        | `package orders;` (no version)                                                                          |
| `service OrderService`                                              | `service Orders`, `service OrderAPI`                                                                    |
| `rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse)` | `rpc createOrder(Order) returns (Order)` (generic model obscures the method-specific write/read shapes) |

## Method Shapes

| Shape                   | Use                                                                       |
| ----------------------- | ------------------------------------------------------------------------- |
| Unary                   | Single request, single response; default                                  |
| Server streaming        | One request, a sequence of responses (feeds, large result sets, progress) |
| Client streaming        | A sequence of requests, one response (uploads, aggregation)               |
| Bidirectional streaming | Independent request and response sequences on one call                    |

- Choose unary unless streaming has a concrete benefit.
- Large payloads: stream chunks instead of one oversized message.

## Messages

- Prefer method-specific request and response messages named `<Method>Request` and `<Method>Response`. Reuse a type only when the directions have genuinely identical semantics and constraints, such as a symmetric bidirectional-stream frame. In Protobuf Edition 2026, keep service-specific messages local unless another `.proto` file must import them; export only reusable top-level message/enum types.
- Use a method-specific empty message or `google.protobuf.Empty` for a genuinely empty side, according to project conventions and evolution needs; do not add empty placeholders without a semantic reason.
- Reuse a message across methods only when its meaning, presence rules, constraints, and compatibility expectations are genuinely identical. Do not reuse merely because fields happen to match today. Do not use bare scalars as request or response.
- Standard list requests: `page_size`, `page_token`; responses: `next_page_token`.
- Partial updates: an explicit `google.protobuf.FieldMask` (`update_mask`) in the request.
- Retry-safe creates: a client-generated `request_id` or idempotency key backed by defined server-side deduplication, scope, retention, and replay behavior.
- Field constraints use Protovalidate annotations when the project uses them.
- Use well-known types (`Timestamp`, `Duration`) for time values.

## Errors

- Canonical status codes: `OK`, `CANCELLED`, `UNKNOWN`, `INVALID_ARGUMENT`, `DEADLINE_EXCEEDED`, `NOT_FOUND`, `ALREADY_EXISTS`, `PERMISSION_DENIED`, `RESOURCE_EXHAUSTED`, `FAILED_PRECONDITION`, `ABORTED`, `OUT_OF_RANGE`, `UNIMPLEMENTED`, `INTERNAL`, `UNAVAILABLE`, `DATA_LOSS`, `UNAUTHENTICATED`.
- Return the most specific code; `UNKNOWN` and `INTERNAL` mean server fault.
- `INVALID_ARGUMENT` for arguments invalid regardless of system state; `FAILED_PRECONDITION` for state-dependent rejection; `OUT_OF_RANGE` for bounds that depend on current state.
- `UNAUTHENTICATED` for missing or invalid credentials; `PERMISSION_DENIED` for authenticated callers without permission.
- Structured details travel in `google.rpc.Status.details` (for example `ErrorInfo`, `BadRequest`, `RetryInfo`, `QuotaFailure`); machine-readable `reason` and `domain` in `ErrorInfo`.
- Document each method's possible codes in comments.

**Example:** status with structured details (text format).

```
code: FAILED_PRECONDITION
message: "Insufficient stock for sku ABC-1"
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "INSUFFICIENT_STOCK"
    domain: "inventory.example.com"
    metadata { key: "sku" value: "ABC-1" }
  }
}
```

## Deadlines and Retries

- Every client call sets a deadline; servers check and propagate the remaining deadline to downstream calls.
- A missing deadline means unbounded waiting; never rely on defaults.
- Retry only idempotent methods, or methods protected by a `request_id`/idempotency key with defined server-side deduplication and replay semantics.
- `UNAVAILABLE` is retryable.
- `DEADLINE_EXCEEDED` and `RESOURCE_EXHAUSTED` are retried only for idempotent methods, with backoff; for `RESOURCE_EXHAUSTED`, wait at least the server-provided retry delay.
- Retry policy through service configuration: `maxAttempts`, `initialBackoff`, `maxBackoff`, `backoffMultiplier`, `retryableStatusCodes`; use retry throttling to prevent retry storms.
- Exponential backoff with jitter; bounded attempts.

**Example:** client service configuration (JSON) with a deadline and a retry policy.

```json
{
  "methodConfig": [
    {
      "name": [
        { "service": "company.orders.v1.OrderService", "method": "GetOrder" }
      ],
      "timeout": "2s",
      "retryPolicy": {
        "maxAttempts": 3,
        "initialBackoff": "0.1s",
        "maxBackoff": "1s",
        "backoffMultiplier": 2,
        "retryableStatusCodes": ["UNAVAILABLE"]
      }
    }
  ]
}
```

## Streaming

- gRPC streaming has transport flow control, but applications must still bound queues and define slow-consumer behavior; do not buffer unboundedly on either side.
- Define message ordering, completion, and cancellation semantics in comments.
- Long-lived streams: define maximum duration, keepalive, and resume strategy (a cursor or last-processed identifier in the request).
- Set maximum send and receive message sizes explicitly on clients, servers, gateways, and proxies. Defaults vary by implementation and version; never rely on a generic default.

## Metadata and Security

- Credentials travel in call metadata (`authorization`) over TLS; mutual TLS for service-to-service identity.
- Per-method authorization; carry caller identity from credentials, never from request fields.
- Define which metadata keys are part of the contract (trace context, tenant, locale).
- Browsers cannot call native gRPC directly; if browser access is required, define gRPC-Web or a gateway as a distinct consumer-facing surface and document its endpoint, authentication, and compatibility behavior in the relevant API documentation.
- Server reflection: enable by explicit policy per environment.

## Operations

- Implement `grpc.health.v1.Health` (`Check`, `Watch`) when the deployment platform uses the standard gRPC health protocol; document service names and serving-state semantics.
- Return `UNIMPLEMENTED` for methods a server does not support.
- Graceful shutdown: refuse new calls, drain in-flight calls within a deadline.

## Evolution

- Never renumber or reuse field numbers; `reserved` removed numbers and names.
- Adding fields, methods, and services is additive; removing or changing types is breaking.
- Breaking change: new package version (`v2`) served alongside `v1`.
- Deprecate with `[deprecated = true]` and a comment naming the replacement.

## Contract Mapping

- `.proto` file: edition declaration, versioned package, services, request/response messages, enums, comments.
- Protobuf does not define runtime authentication, rate limiting, deadlines, retry policy, or gateway exposure. Document consumer-facing behavior on the relevant service/RPC or in linked gRPC/API documentation, and enforce it in the service or gateway.
- Use HTTP annotations (`google.api.http`) only when a compatible transcoding gateway is part of the supported surface; document the generated HTTP mapping alongside that surface.

## Anti-Patterns

- Reusing a generic message across methods when their semantics, presence rules, or constraints differ.
- `google.protobuf.Empty` as response of a method that may later return data.
- Calls without deadlines.
- Retrying non-idempotent methods without a functioning deduplication mechanism.
- Business errors encoded in successful responses.
- Using `OK` with an error field instead of status codes.
- Large messages instead of streaming.
- Reflection and verbose error details exposed publicly.

## Checklist

- [ ] Package is versioned; services and methods follow naming rules.
- [ ] Request/response types are method-specific where their semantics differ; any reuse has identical meaning, presence rules, constraints, and compatibility expectations.
- [ ] Lists use `page_size` and `page_token`; updates use field masks.
- [ ] Possible status codes are documented per method.
- [ ] Deadline and retry guidance is recorded.
- [ ] Streaming methods define ordering, completion, cancellation, and limits.
- [ ] Health checking is specified for deployed services.
