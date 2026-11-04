# Authentication and Authorization

## Scope

- Establishing who the caller is (authentication) and what the caller may do (authorization) for every protocol.
- OAuth 2.1 is an IETF draft; current normative guidance is RFC 9700.

## Principles

- Deny by default; the effective authentication and authorization policy must be clear for every operation. Use inherited defaults where the contract format supports them; mark intentional public exceptions explicitly.
- Authenticate at the boundary, authorize at the resource.
- Derive caller identity, tenant, and roles from verified credentials, never from request fields.
- Least privilege: narrow scopes, short lifetimes, per-purpose credentials.
- Use established standards; do not design custom authentication schemes.

## Authentication Mechanisms

| Caller                                 | Mechanism                                                                                        |
| -------------------------------------- | ------------------------------------------------------------------------------------------------ |
| User in a browser or mobile app        | OAuth 2.0 Authorization Code with PKCE (RFC 7636); OpenID Connect for identity                   |
| Service-to-service, no user            | Client credentials grant, or mutual TLS workload identity                                        |
| Input-constrained device               | Device authorization grant (RFC 8628)                                                            |
| First-party browser session            | Session cookie: `Secure`, `HttpOnly`, `SameSite`, CSRF protection for state-changing requests    |
| Third-party integration by application | API key identifying the application, combined with an authorization mechanism for sensitive data |

- Do not use the implicit grant or the resource owner password credentials grant in new designs (RFC 9700).
- API keys identify applications, not users; they travel in headers (never URLs), rotate, are scoped, and are stored hashed.
- Sender-constrained tokens (DPoP, RFC 9449; mutual TLS bound tokens, RFC 8705) reduce token theft impact for high-risk APIs.
- Advanced flows: Pushed Authorization Requests (RFC 9126), Resource Indicators (RFC 8707), authorization server metadata (RFC 8414), protected resource metadata (RFC 9728).

## Token Rules

- Bearer tokens (RFC 6750) travel in the `Authorization` header.
- JWT access tokens: validate the signature with an explicit algorithm allowlist; validate issuer, audience, expiry, not-before, token purpose/type, and profile-required claims; reject `none` and algorithm/key confusion (RFC 8725, RFC 9068).
- Opaque tokens: validate through introspection (RFC 7662) with caching bounded by token lifetime.
- Access tokens are short-lived; refresh tokens rotate and are revocable.
- Audience restriction: a token is accepted only by the resource it was issued for.
- Tokens never appear in URLs, logs, or error messages.

**Example:** claims checked for a JWT access token.

```json
{
  "iss": "https://auth.example.com",
  "aud": "https://api.example.com",
  "sub": "user_123",
  "exp": 2000000000,
  "scope": "orders:read",
  "tenant": "t_42"
}
```

Accept only when the signature algorithm is allowlisted, `iss` is the expected issuer, `aud` names this API, `exp` is in the future, and `scope` covers the operation.

## Authorization Model

- Layers, all required where applicable:
  1. **Operation level:** may this caller invoke this operation?
  2. **Object level:** may this caller access this specific object? (check on every object access, including list filtering)
  3. **Property level:** may this caller read or write this field?
  4. **Tenant boundary:** every query and mutation is scoped to the caller's tenant.
  5. **State and business rules:** is the action allowed in the object's current state?
- Model choice: scopes for coarse client permissions; roles for user-level grouping; attributes or relationships for object-level rules. State which are used and how they combine.
- Scope names follow one pattern (`resource:action`) and are documented per operation.
- Central policy evaluation; do not scatter checks inconsistently.
- Authorization applies to list results, search, counts, exports, and subscriptions as well as direct reads.

**Example:** checks for `GET /orders/{orderId}`.

| Layer     | Check                                                                 |
| --------- | --------------------------------------------------------------------- |
| Operation | Token scope includes `orders:read`                                    |
| Object    | `order.ownerId` equals the caller, or the caller holds a support role |
| Property  | `internalReference` returned only with `orders:admin`                 |
| Tenant    | Query is filtered by the tenant in the token                          |
| State     | Not applicable to reads                                               |

| Good Scope Names                              | Bad                      |
| --------------------------------------------- | ------------------------ |
| `orders:read`, `orders:write`, `orders:admin` | `admin`, `all`, `scope1` |

## Responses

- 401 with `WWW-Authenticate` challenge (for bearer tokens, include an `error` such as `invalid_token`) for missing or invalid credentials.
- 403 for authenticated callers lacking permission.
- 404 instead of 403 only under a documented policy to hide object existence, applied consistently.
- Failed authentication responses are uniform to avoid account enumeration.

## Per-Protocol Rules

- **REST:** `Authorization` header; per-operation scopes in the contract.
- **GraphQL:** authenticate the HTTP request; authorize per field or per resolver in the domain layer; authorize subscriptions at subscribe time and per event.
- **gRPC:** credentials in call metadata over TLS; mutual TLS between services; per-method authorization.
- **WebSocket:** authenticate during or immediately after the handshake; authorize per subscription and message; handle token expiry on long-lived connections.
- **SSE:** cookie or fetch-based client with `Authorization`; re-check on long streams.
- **Messaging:** broker-level authentication; per-channel publish and subscribe permissions; message-level claims for end-to-end identity.
- **Webhooks:** payload signatures verify the sender; subscription APIs require normal authentication.

## Contract Mapping

- **OpenAPI:** declare `components.securitySchemes`; apply default `security` at the root when appropriate and override at operation level only when needed; use `security: []` for intentionally public operations; document relevant 401 and 403 responses.
- **AsyncAPI:** declare `components.securitySchemes`; `servers[*].security` and `operations[*].security` are arrays of Security Scheme Objects or Reference Objects (for example `- $ref: "#/components/securitySchemes/bearer"`). Entries within one array are alternatives (OR); when both server and operation security apply, each level must be satisfied (AND across levels). Unlike OpenAPI, AsyncAPI does not use the scheme-name-to-scopes map syntax in these arrays.
- Protobuf and GraphQL SDL do not define a common first-class authentication model. Document gRPC authentication and metadata requirements in service/RPC comments or linked transport documentation; document GraphQL authentication at the HTTP/WebSocket transport layer. Describe consumer-visible permission requirements where useful, but comments and descriptions do not enforce authorization. Define and test runtime policy separately.

## Anti-Patterns

- Trusting client-provided user, tenant, or role fields.
- Checking authentication but not object-level authorization.
- Long-lived bearer tokens; tokens in URLs.
- API keys as user identity.
- Custom signature or token schemes.
- Accepting any JWT algorithm; skipping `aud` validation.
- Different error text for unknown user versus wrong password.

## Checklist

- [ ] Effective authentication and permissions are clear for every operation; inherited defaults and explicit public exceptions are documented.
- [ ] Object-, property-, and tenant-level checks defined.
- [ ] Token validation rules (algorithm, issuer, audience, expiry) stated.
- [ ] Flows follow RFC 9700 (no implicit or password grants).
- [ ] 401, 403, and 404 policy defined.
- [ ] Long-lived connections have an expiry strategy.
- [ ] Draft OAuth 2.1 references are labeled when used.
