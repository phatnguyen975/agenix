# gRPC

## Contents

- Scope
- Service Design
- Method Shapes
- Messages
- Errors
- Deadlines and Retries
- Streaming
- Metadata and Security
- Operations
- Evolution
- Contract Mapping
- Anti-Patterns
- Checklist
- Sources

## Scope

- Typed RPC over HTTP/2 described by Protobuf service definitions.
- Covers service and method design, errors, deadlines, retries, streaming, and operational endpoints.

## Service Design

- One service per cohesive capability; avoid one service holding unrelated methods.
- Package carries the major version: `company.domain.v1`.
- Service names are nouns ending in `Service`; method names are verbs in `PascalCase` (`GetOrder`, `CreateOrder`).
- Resource-oriented services use standard methods (`Get`, `List`, `Create`, `Update`, `Delete`) before custom methods.
- Keep the service surface small; each method has one clear purpose.

| Good                                                                | Bad                                                                   |
| ------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `package company.orders.v1;`                                        | `package orders;` (no version)                                        |
| `service OrderService`                                              | `service Orders`, `service OrderAPI`                                  |
| `rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse)` | `rpc createOrder(Order) returns (Order)` (shared message, wrong case) |

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

- Every method has its own request and response messages, named `<Method>Request` and `<Method>Response`.
- Define them even when empty, so fields can be added later.
- Do not reuse one message across methods; do not use bare scalars as request or response.
- Use `google.protobuf.Empty` only where the project style guide requires it.
- Standard list requests: `page_size`, `page_token`; responses: `next_page_token`.
- Partial updates: an explicit `google.protobuf.FieldMask` (`update_mask`) in the request.
- Retry-safe creates: a client-generated `request_id` field.
- Field constraints use Protovalidate annotations when the project uses them.
- Use well-known types (`Timestamp`, `Duration`) for time values.

## Errors

- Canonical status codes: `OK`, `CANCELLED`, `UNKNOWN`, `INVALID_ARGUMENT`, `DEADLINE_EXCEEDED`, `NOT_FOUND`, `ALREADY_EXISTS`, `PERMISSION_DENIED`, `RESOURCE_EXHAUSTED`, `FAILED_PRECONDITION`, `ABORTED`, `OUT_OF_RANGE`, `UNIMPLEMENTED`, `INTERNAL`, `UNAVAILABLE`, `DATA_LOSS`, `UNAUTHENTICATED`.
- Return the most specific code; `UNKNOWN` and `INTERNAL` mean server fault.
- `INVALID_ARGUMENT` for arguments invalid regardless of system state; `FAILED_PRECONDITION` for state-dependent rejection; `OUT_OF_RANGE` for bounds that depend on current state.
- `UNAUTHENTICATED` for missing or invalid credentials; `PERMISSION_DENIED` for authenticated callers without permission.
- Structured details travel in `google.rpc.Status.details` (for example `ErrorInfo`, `BadRequest`, `RetryInfo`, `QuotaFailure`); machine-readable `reason` and `domain` in `ErrorInfo`.
- Document each method's possible codes in comments.

Example: status with structured details (text format).

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
- Retry only idempotent methods, or methods protected by a `request_id`.
- `UNAVAILABLE` is retryable.
- `DEADLINE_EXCEEDED` and `RESOURCE_EXHAUSTED` are retried only for idempotent methods, with backoff; for `RESOURCE_EXHAUSTED`, wait at least the server-provided retry delay.
- Retry policy through service configuration: `maxAttempts`, `initialBackoff`, `maxBackoff`, `backoffMultiplier`, `retryableStatusCodes`; use retry throttling to prevent retry storms.
- Exponential backoff with jitter; bounded attempts.

Example: client service configuration (JSON) with a deadline and a retry policy.

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

- Flow control is built in; do not buffer unboundedly on either side.
- Define message ordering, completion, and cancellation semantics in comments.
- Long-lived streams: define maximum duration, keepalive, and resume strategy (a cursor or last-processed identifier in the request).
- Set maximum message sizes explicitly; implementations apply default limits (commonly a few megabytes on receive).

## Metadata and Security

- Credentials travel in call metadata (`authorization`) over TLS; mutual TLS for service-to-service identity.
- Per-method authorization; carry caller identity from credentials, never from request fields.
- Define which metadata keys are part of the contract (trace context, tenant, locale).
- Browsers cannot call native gRPC; if browser access is required, use a gRPC-Web layer or a gateway and state it in the header notes.
- Server reflection: enable by explicit policy per environment.

## Operations

- Implement the standard health checking service (`grpc.health.v1.Health`: `Check`, `Watch`) for load balancers and orchestrators.
- Return `UNIMPLEMENTED` for methods a server does not support.
- Graceful shutdown: refuse new calls, drain in-flight calls within a deadline.

## Evolution

- Never renumber or reuse field numbers; `reserved` removed numbers and names.
- Adding fields, methods, and services is additive; removing or changing types is breaking.
- Breaking change: new package version (`v2`) served alongside `v1`.
- Deprecate with `[deprecated = true]` and a comment naming the replacement.

## Contract Mapping

- `.proto` file: edition declaration, versioned package, services, request/response messages, enums, comments.
- Authentication, rate limits, retry guidance, and browser access are not expressible in Protobuf: record them in the header notes.
- Optional REST exposure through HTTP annotations (`google.api.http`) when a transcoding gateway is used; record the mapping in the header notes.

## Anti-Patterns

- One message type shared by many methods.
- `google.protobuf.Empty` as response of a method that may later return data.
- Calls without deadlines.
- Retrying non-idempotent methods without a `request_id`.
- Business errors encoded in successful responses.
- Using `OK` with an error field instead of status codes.
- Large messages instead of streaming.
- Reflection and verbose error details exposed publicly.

## Checklist

- [ ] Package is versioned; services and methods follow naming rules.
- [ ] Each method has unique request and response messages.
- [ ] Lists use `page_size` and `page_token`; updates use field masks.
- [ ] Possible status codes are documented per method.
- [ ] Deadline and retry guidance is recorded.
- [ ] Streaming methods define ordering, completion, cancellation, and limits.
- [ ] Health checking is specified for deployed services.

## Sources

- gRPC documentation: status codes, deadlines, retry, health checking, metadata, authentication (https://grpc.io/docs/).
- Protocol Buffers style guide (https://protobuf.dev/programming-guides/style/).
- Google API Improvement Proposals (standard methods, pagination, field masks, errors).
