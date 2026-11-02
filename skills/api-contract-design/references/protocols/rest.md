# REST

## Scope

- HTTP APIs organized around resources identified by URIs and manipulated through standard methods.
- Covers resource design, method and status semantics, and updates. Pagination, errors, idempotency, auth, and caching are separate concerns.

## Resource Modeling

- Resource = a noun the consumer cares about, not a table or a class.
- Collection + item pairs: `/orders`, `/orders/{orderId}`.
- Identifiers are opaque, stable, immutable; never reuse an identifier.
- Nest a subresource when its identity or lifecycle is scoped by the parent (`/orders/{orderId}/lines`). Keep paths readable; shallow nesting is a usability heuristic, not an HTTP requirement.
- Model state as a field with a documented set of transitions; model long processes as operation resources.
- Expose representations shaped for consumers; do not serialize storage entities.

## Naming

- Lowercase, hyphen-separated path segments; plural nouns for collections.
- No verbs in paths for CRUD; no file extensions; no trailing-slash variants (pick one, redirect or reject the other).
- Path parameters are resource identifiers only; filters, sorting, and paging are query parameters.
- Query and body property names follow one casing style across the surface.
- One concept, one name, everywhere.

| Good                                      | Bad                                                             | Rule                                                                                                                               |
| ----------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `GET /orders`                             | `GET /getOrders`                                                | No verbs for CRUD                                                                                                                  |
| `GET /orders/{orderId}`                   | `GET /order/list`                                               | Plural collection, identifier selects the item                                                                                     |
| `GET /orders?status=PAID&sort=-createdAt` | `GET /orders/status/PAID`                                       | Filters and sorting are query parameters                                                                                           |
| `/payment-methods`                        | `/paymentMethods`, `/Payment_Methods`                           | Lowercase, hyphen-separated                                                                                                        |
| `/orders/{orderId}/lines`                 | `/orders/{orderId}/lines/{lineId}/discounts/{discountId}/rules` | Prefer shallow nesting; use deeper paths only when parent-scoped identity or lifecycle requires it. At most two levels of nesting. |

## Methods

| Method            | Safe | Idempotent                 | Use                                                                |
| ----------------- | ---- | -------------------------- | ------------------------------------------------------------------ |
| GET               | Yes  | Yes                        | Read; no body semantics                                            |
| HEAD              | Yes  | Yes                        | Headers of GET                                                     |
| OPTIONS           | Yes  | Yes                        | Capabilities, CORS preflight                                       |
| QUERY (RFC 10008) | Yes  | Yes                        | Read with a request body when parameters do not fit a URI          |
| PUT               | No   | Yes                        | Replace or create at a known URI                                   |
| DELETE            | No   | Yes                        | Remove                                                             |
| POST              | No   | No                         | Create in a collection, trigger actions, non-idempotent operations |
| PATCH (RFC 5789)  | No   | No (unless designed to be) | Partial update                                                     |

- Never change state on a safe method.
- Safe methods may be cached, prefetched, and retried by intermediaries; design accordingly.
- QUERY needs support across clients, gateways, caches, and intermediaries. When unavailable, POST on a search resource is an interoperability convention; document that it is application-level read-only, but do not describe POST as an HTTP safe or idempotent method or assume generic cache/retry behavior.
- Do not expose `TRACE` by default; it can reflect sensitive request information. Use it only when explicitly required and reviewed.
- Sensitive data does not go in URIs (URIs are logged); use a body.

**Example:** create with a retry-safe key.

```http
POST /orders HTTP/1.1
Content-Type: application/json
Idempotency-Key: "8e03978e-40d5-43e8-bc93-6894a57f9324"

{"total": {"amount": 1250, "currency": "EUR"}}
```

```http
HTTP/1.1 201 Created
Location: /orders/ord_01HZX
ETag: "1"
Content-Type: application/json

{"id": "ord_01HZX", "status": "PENDING", "total": {"amount": 1250, "currency": "EUR"}}
```

## Status Codes

| Situation                                                       | Status                                  |
| --------------------------------------------------------------- | --------------------------------------- |
| Read or update succeeded with body                              | 200                                     |
| Created                                                         | 201 with `Location` of the new resource |
| Accepted for asynchronous processing                            | 202 with operation resource `Location`  |
| Succeeded, no body                                              | 204                                     |
| Conditional GET unchanged                                       | 304                                     |
| Malformed syntax, invalid parameter                             | 400                                     |
| Missing or invalid credentials                                  | 401 with `WWW-Authenticate`             |
| Authenticated but not permitted                                 | 403                                     |
| Resource does not exist                                         | 404                                     |
| Method not allowed for resource                                 | 405 with `Allow`                        |
| No acceptable representation                                    | 406                                     |
| Conflict with current state (duplicate, version, state machine) | 409                                     |
| Resource permanently gone                                       | 410                                     |
| Precondition failed (`If-Match`, `If-Unmodified-Since`)         | 412                                     |
| Precondition required but missing                               | 428                                     |
| Request body too large                                          | 413                                     |
| Unsupported request media type                                  | 415                                     |
| Semantically invalid content                                    | 422                                     |
| Rate limited                                                    | 429 with `Retry-After`                  |
| Unexpected server fault                                         | 500                                     |
| Bad gateway / upstream failure                                  | 502                                     |
| Overloaded or unavailable                                       | 503 with `Retry-After` when known       |
| Upstream timeout                                                | 504                                     |

- Use the most specific status; never return 200 with an error body.
- 404 versus 403 for objects the caller may not see: choose one policy, document it, apply it consistently.
- Document each defined success response and each known, consumer-relevant error response; use ranges or a default response intentionally rather than claiming to enumerate every infrastructure failure.

## Updates

- PUT is full replacement; omitted fields are reset; idempotent.
- PATCH with JSON Merge Patch (RFC 7396): send changed fields; `null` removes a field; arrays are replaced whole; cannot set a field to `null` as a value.
- PATCH with JSON Patch (RFC 6902): ordered operations (`add`, `remove`, `replace`, `move`, `copy`, `test`); use for array element edits and guarded updates.
- Pick one PATCH format per resource and declare its media type (`application/merge-patch+json`, `application/json-patch+json`).
- Protect against lost updates with `ETag` and `If-Match`.
- Only fields marked writable are accepted; server-managed fields (`id`, timestamps, owner) are read-only.

**Example:** JSON Merge Patch (`Content-Type: application/merge-patch+json`).

| Stored Resource                      | Request Body                        | Resulting Resource                      |
| ------------------------------------ | ----------------------------------- | --------------------------------------- |
| `{"note": "gift", "giftWrap": true}` | `{"note": null, "giftWrap": false}` | `{"giftWrap": false}`                   |
| `{"tags": ["a", "b"]}`               | `{"tags": ["c"]}`                   | `{"tags": ["c"]}` (arrays are replaced) |

## Requests and Responses

- JSON (`application/json`) unless a consumer need requires another type; declare each media type per operation.
- Prefer an object envelope when the response needs pagination metadata, links, or room for future sibling fields. A top-level array or scalar is valid when it is the clearest stable representation and fits the project's conventions.
- Create returns the created representation (or its identifier) and `Location`.
- Declare `Content-Type` on requests with bodies and `Accept` handling for responses; unsupported types return 415 or 406.
- Link relations (`Link` header, RFC 8288) for pagination and related resources; hypermedia controls are optional.
- Use `HEAD` and conditional requests (`ETag`, `If-None-Match`) for cache validation.

**Example:** object envelope when collection metadata or future extensibility is needed.

| Avoid               | Prefer                                             |
| ------------------- | -------------------------------------------------- |
| `[{"id": "ord_1"}]` | `{"items": [{"id": "ord_1"}], "nextCursor": null}` |

## Relationships and Actions

- Reference related resources by identifier or link; embed only when consumers nearly always need them, and bound the depth.
- Many-to-many links: a collection resource or a relationship subresource (`PUT/DELETE /groups/{id}/members/{userId}`).
- State transitions and commands that are not CRUD: a subresource noun for the action or a transition resource (`POST /orders/{id}/cancellation`); choose one style and apply it everywhere.
- Bulk and long-running work follow the long-running and bulk concern.

| Need                                   | Style                                                       |
| -------------------------------------- | ----------------------------------------------------------- |
| Cancel an order                        | `POST /orders/{orderId}/cancellation` (transition resource) |
| Add a member to a group                | `PUT /groups/{groupId}/members/{userId}`                    |
| Remove a member                        | `DELETE /groups/{groupId}/members/{userId}`                 |
| Search with a large or sensitive query | `QUERY /orders/search` with a body                          |

## Contract Mapping

- **OpenAPI:** `paths` (one path item per resource URI), `operationId` per operation, `parameters`, `requestBody`, `responses` for each status above, `components` for shared schemas, parameters, and responses.
- OpenAPI `query` operations require 3.2. Under 3.1, POST may model a body-bearing search for compatibility, but HTTP still classifies POST as unsafe and non-idempotent by default; do not promise safe-method caching or generic intermediary retries.
- Define default `security` at the API root when appropriate. Each operation inherits it unless it overrides it; use `security: []` to intentionally remove inherited security, or `[{}]` / an empty requirement object when anonymous access is one allowed alternative. Keep the effective policy clear without duplicating root-level requirements on every operation.

## Anti-Patterns

- RPC-style paths (`/getUser`, `/doPayment`) for CRUD.
- GET with side effects; POST for everything.
- 200 with `{"error": ...}`; one status for all failures.
- Exposing database identifiers that are sequential and guessable without authorization checks.
- Deep nesting (`/a/{id}/b/{id}/c/{id}/d`).
- Boolean query flags that hide behavior changes.
- Changing the meaning of a status code or field between versions.

## Checklist

- [ ] Every resource is a noun with a stable identifier.
- [ ] Method safety and idempotency match RFC 9110 semantics.
- [ ] Each operation documents its defined success response and known consumer-relevant error responses.
- [ ] Create returns 201 and `Location`; async returns 202 and an operation resource.
- [ ] One PATCH format per resource, with declared media type.
- [ ] Writable and read-only fields are distinguished.
- [ ] No sensitive data in URIs.
