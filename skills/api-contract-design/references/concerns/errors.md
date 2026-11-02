# Errors

## Contents

- Scope
- Principles
- HTTP: Problem Details
- Validation Errors
- Status Selection
- Cross-Protocol Mapping
- Per-Protocol Rules
- Anti-Patterns
- Checklist
- Sources

## Scope

- Error model design for every protocol; one model per protocol, consistent within the contract.

## Principles

- Errors are part of the contract: every operation lists its error cases.
- Clients branch on stable machine-readable identifiers, never on human text.
- Messages help the caller fix the problem and reveal no internals (stack traces, SQL, hostnames, library names).
- The same condition produces the same error everywhere.
- Distinguish: invalid input, authentication, authorization, not found, conflict, precondition, rate limit, unavailable, internal.
- Do not reveal whether protected objects exist beyond the documented 403/404 policy.

## HTTP: Problem Details

- Media type `application/problem+json` (RFC 9457).
- Standard members:
  - `type`: URI reference identifying the problem type; defaults to `about:blank` when omitted; stable identifier, dereferencing is optional.
  - `title`: short summary of the type; the same for every occurrence of that type.
  - `status`: the HTTP status code (advisory; must agree with the actual response).
  - `detail`: explanation specific to this occurrence; for humans, not for parsing.
  - `instance`: URI reference identifying this occurrence (for example a request or trace identifier).
- Extension members are allowed; add a stable `code` for branching and domain fields for context. Clients ignore unknown extension members.
- Multiple problems in one response: one problem object whose extension member (for example `errors`) lists the individual problems; choose the status that best fits the whole.
- Define one shared Problem schema in the contract and reuse it in every error response.
- The draft RateLimit specification defines problem types for quota and capacity conditions (see the rate-limiting concern); other types use project URIs under a domain the project controls.
- Set `Content-Language` when `title` and `detail` are localized.

```http
HTTP/1.1 404 Not Found
Content-Type: application/problem+json

{
  "type": "https://example.com/problems/order-not-found",
  "title": "Order not found",
  "status": 404,
  "detail": "No order with identifier ord_01HZX.",
  "instance": "/requests/9f2c",
  "code": "ORDER_NOT_FOUND"
}
```

## Validation Errors

- Return all detected field errors at once, not one at a time.
- Each entry: location (JSON Pointer, RFC 6901, such as `/items/0/quantity`; or parameter name and location), stable `code`, short `detail`.
- Status: 400 for syntactic problems and invalid parameters; 422 for well-formed content that violates semantic rules. Choose one convention per API.

```json
{
  "type": "https://example.com/problems/validation-error",
  "title": "Request validation failed",
  "status": 422,
  "errors": [
    {
      "pointer": "/total/amount",
      "code": "OUT_OF_RANGE",
      "detail": "Must be 0 or greater."
    },
    {
      "pointer": "/note",
      "code": "TOO_LONG",
      "detail": "Maximum length is 500."
    }
  ]
}
```

## Status Selection

| Condition                                    | HTTP                        |
| -------------------------------------------- | --------------------------- |
| Malformed request, invalid parameter         | 400                         |
| Missing or invalid credentials               | 401 with `WWW-Authenticate` |
| Authenticated, not allowed                   | 403                         |
| Not found or hidden by policy                | 404                         |
| State conflict, duplicate, concurrent change | 409                         |
| Precondition failed                          | 412                         |
| Precondition required                        | 428                         |
| Semantic validation failure                  | 422                         |
| Rate limited                                 | 429                         |
| Server fault                                 | 500                         |
| Dependency failure                           | 502                         |
| Overload or maintenance                      | 503                         |
| Dependency timeout                           | 504                         |

## Cross-Protocol Mapping

| Condition                         | HTTP      | gRPC                  | GraphQL (`extensions.code`)      |
| --------------------------------- | --------- | --------------------- | -------------------------------- |
| Invalid argument                  | 400 / 422 | `INVALID_ARGUMENT`    | `BAD_USER_INPUT` or project code |
| Unauthenticated                   | 401       | `UNAUTHENTICATED`     | `UNAUTHENTICATED`                |
| Forbidden                         | 403       | `PERMISSION_DENIED`   | `FORBIDDEN`                      |
| Not found                         | 404       | `NOT_FOUND`           | `NOT_FOUND`                      |
| Already exists                    | 409       | `ALREADY_EXISTS`      | `CONFLICT`                       |
| Aborted / concurrent conflict     | 409       | `ABORTED`             | `CONFLICT`                       |
| State precondition not met        | 400       | `FAILED_PRECONDITION` | `PRECONDITION_FAILED`            |
| Resource exhausted / rate limited | 429       | `RESOURCE_EXHAUSTED`  | `RATE_LIMITED`                   |
| Cancelled by client               | 499       | `CANCELLED`           | —                                |
| Internal error                    | 500       | `INTERNAL`            | `INTERNAL_SERVER_ERROR`          |
| Not implemented                   | 501       | `UNIMPLEMENTED`       | —                                |
| Unavailable                       | 503       | `UNAVAILABLE`         | `SERVICE_UNAVAILABLE`            |
| Deadline exceeded                 | 504       | `DEADLINE_EXCEEDED`   | `TIMEOUT`                        |

- The HTTP column for gRPC follows the canonical gRPC-to-HTTP mapping used by gateways.
- GraphQL has no standard codes; the listed names are conventions; define the project's own set and document it.

## Per-Protocol Rules

- **REST**: Problem Details on every non-2xx response; document statuses per operation.
- **GraphQL**: user-correctable domain errors as typed payload fields; protocol-level failures in `errors` with `extensions.code`; never leak resolver internals.
- **gRPC**: canonical status codes with `google.rpc.Status` details (`ErrorInfo` with `reason` and `domain`, `BadRequest` with field violations, `RetryInfo`).
- **WebSocket**: typed error messages with `code` and `correlationId`; close codes for connection-level faults.
- **SSE**: a dedicated `error` event type with `code` and `message`; end the stream only for unrecoverable errors; failures before the stream starts use HTTP statuses.
- **Messaging**: processing failures go to retry then dead-letter with failure reason attached; reply messages carry a typed error body; consumers never throw away messages silently.
- **Webhooks**: consumers signal failure with non-2xx; providers retry per policy; provider-side errors appear in delivery logs.

Examples:

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer error="invalid_token", error_description="The access token expired"
```

```
event: error
data: {"code": "STREAM_EXPIRED", "message": "Stream duration limit reached; reconnect."}
```

## Anti-Patterns

- 200 with an error body; the same status for every failure.
- Clients required to parse `detail` or `message`.
- Different error shapes across operations.
- Stack traces and internal identifiers in responses.
- Distinct error timing or text that lets attackers enumerate accounts.
- Undocumented error codes.

## Checklist

- [ ] One error schema per protocol, reused everywhere.
- [ ] Every operation lists error cases with status or code.
- [ ] Stable `type` or `code` values are catalogued in the contract.
- [ ] Validation errors report all violations with locations.
- [ ] No internal detail in error text.
- [ ] 403/404 policy stated and consistent.

## Sources

- RFC 9457 (Problem Details), RFC 9110 (status codes), RFC 6901, RFC 6585.
- gRPC status codes and `google.rpc` error model; Google API Improvement Proposals (errors).
- GraphQL specification, Response (errors).
