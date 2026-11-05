# Caching and Conditional Requests

## Scope

- Contract-level HTTP caching, cache validation, and lost-update prevention. For RPC/message retries, read `idempotency-retries-concurrency.md` instead.
- Caching is an HTTP behavior; GraphQL or POST-based reads need an explicit application or persisted-query cache design.

## Cache Policy

- Prefer GET for broadly cacheable resource reads. A safe method is not automatically cacheable in every context; the response still needs an applicable cache policy.
- Choose policy per response and data classification:
  | Directive         | Meaning and Use                                                                                                                                 |
  | ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
  | `max-age=N`       | Freshness lifetime for private caches.                                                                                                          |
  | `s-maxage=N`      | Freshness lifetime for shared caches; takes precedence over `max-age` for shared caches.                                                        |
  | `public`          | Explicitly permits shared-cache storage in cases where it would otherwise be restricted; use only when representation is safe for shared reuse. |
  | `private`         | Prevents shared-cache storage; a private cache may store the response.                                                                          |
  | `no-cache`        | Storage is allowed, but reuse requires successful revalidation. It does not mean "do not store".                                                |
  | `no-store`        | Instructs caches not to store the response; use for sensitive responses where appropriate.                                                      |
  | `must-revalidate` | A stale response must not be reused without successful validation.                                                                              |
- `stale-while-revalidate` and `stale-if-error` are extensions defined by RFC 5861; use only where stale responses are acceptable and the cache supports them.
- Authenticated or user-specific data must not leak through a shared cache. Prefer `private` or `no-store`; only use shared caching with an explicit, reviewed cache-key and authorization design.
- Define freshness, stale behavior, invalidation expectations, and cacheability per operation. Do not assume a gateway's default policy.

**Examples:**

```http
# Public reference data that may be five minutes stale
Cache-Control: public, max-age=300

# User-specific data may be stored only in a private cache and must revalidate
Cache-Control: private, no-cache
ETag: "v4"

# Sensitive response
Cache-Control: no-store
```

## Validators and Revalidation

- Prefer an `ETag` when the server can provide a representation validator. `Last-Modified` is useful when timestamp-based validation is sufficient; its resolution and clock behavior may be less precise.
- Clients revalidate with `If-None-Match` or `If-Modified-Since`. If the selected representation is unchanged, return `304 Not Modified` with no message body and the applicable cache metadata.
- Use a strong ETag when byte-for-byte representation identity matters. Weak ETags (`W/`) are suitable for semantic cache revalidation but cannot satisfy strong comparison required by `If-Match`.
- Validators identify a selected representation; account for negotiated variants and any content coding that changes the representation.

```http
GET /orders/ord_123 HTTP/1.1
If-None-Match: "order-v4"

HTTP/1.1 304 Not Modified
ETag: "order-v4"
Cache-Control: private, max-age=60
```

## Conditional Writes and Concurrency

- Use conditional requests to prevent lost updates when two consumers may modify the same resource.
- Return an ETag with a representation. Require `If-Match` on updates when stale writes must be rejected; use a strong validator.
- Return `412 Precondition Failed` when the validator does not match. Return `428 Precondition Required` when the server requires a precondition and it is missing.
- `If-None-Match: *` can express create-only semantics where an existing resource must not be overwritten.
- Document whether the server requires preconditions, which representation/version the validator covers, and the client's conflict-recovery action (refetch, merge, or ask the user).

```http
GET /orders/ord_123

HTTP/1.1 200 OK
ETag: "order-v4"

PATCH /orders/ord_123
If-Match: "order-v4"
Content-Type: application/merge-patch+json

{"note": "Gift wrap"}

HTTP/1.1 412 Precondition Failed
Content-Type: application/problem+json
```

## Representation Variants

- Use `Vary` for request headers that select the representation, commonly `Accept` and `Accept-Language`.
- Do not add `Authorization` to `Vary` as a substitute for safe cache directives or correct authorization. Shared caching of authenticated responses needs explicit policy and cache-key design.
- When reflecting a request `Origin` in CORS responses, include `Vary: Origin` so caches do not reuse one origin's CORS response for another.
- `Content-Encoding` and negotiated media types can affect validators and cache variants; document the supported behavior when clients depend on it.

## Protocol Mapping

- **OpenAPI:** declare `ETag`, `Last-Modified`, `Cache-Control`, `Vary`, and applicable request validators; model `304`, `412`, and `428` where the operation can return them. Describe cache policy per operation/response.
- **GraphQL:** cache at the operation/field or persisted-query layer; define authorization-aware cache keys and invalidation. POST requests are not generically cacheable by HTTP intermediaries.
- **gRPC / AsyncAPI / WebSocket / SSE:** define application-level caches separately. HTTP cache directives do not automatically describe broker retention, stream replay, or in-memory response caching.

## Anti-Patterns

- Assuming every GET response is public or safe for shared caching.
- Using `no-cache` when the intent is to prohibit storage; use `no-store` for that intent.
- Using weak ETags for `If-Match` lost-update protection.
- Returning a body with `304 Not Modified`.
- Treating `Vary: Authorization` as access control.
- Using `Last-Modified` as a high-precision concurrency token.

## Checklist

- [ ] Cacheability and freshness are defined per relevant response.
- [ ] User-specific and sensitive data cannot be reused by a shared cache.
- [ ] Validators and 304 behavior are specified where revalidation is supported.
- [ ] Conditional writes, strong ETags, 412, and 428 are defined where concurrency requires them.
- [ ] Negotiated variants and `Vary` fields are correct.
