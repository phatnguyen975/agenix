# Authentication and Authorization

## Contents

- Scope
- Principles
- Authentication Mechanisms
- Token Rules
- Authorization Model
- Responses
- Per-Protocol Rules
- Contract Mapping
- Anti-Patterns
- Checklist
- Sources

## Scope

- Establishing who the caller is (authentication) and what the caller may do (authorization) for every protocol.
- OAuth 2.1 is an IETF draft; current normative guidance is RFC 9700.

## Principles

- Deny by default; every operation declares its required authentication and permissions, including operations deliberately public.
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
- JWT access tokens: validate signature with an allowlisted algorithm (reject `none`), `iss`, `aud`, `exp`, `nbf`, and scopes (RFC 8725, RFC 9068).
- Opaque tokens: validate through introspection (RFC 7662) with caching bounded by token lifetime.
- Access tokens are short-lived; refresh tokens rotate and are revocable.
- Audience restriction: a token is accepted only by the resource it was issued for.
- Tokens never appear in URLs, logs, or error messages.

Example claims checked for a JWT access token:

```json
{
  "iss": "https://auth.example.com",
  "aud": "https://api.example.com",
  "sub": "user_123",
  "exp": 1772361000,
  "scope": "orders:read",
  "tenant": "t_42"
}
```

Accept only when the signature algorithm is allowlisted, `iss` is the expected issuer, `aud` names this API, `exp` is in the future, and `scope` covers the operation.

## Authorization Model

- Layers, all required where applicable:
  1. Operation level: may this caller invoke this operation?
  2. Object level: may this caller access this specific object? (check on every object access, including list filtering)
  3. Property level: may this caller read or write this field?
  4. Tenant boundary: every query and mutation is scoped to the caller's tenant.
  5. State and business rules: is the action allowed in the object's current state?
- Model choice: scopes for coarse client permissions; roles for user-level grouping; attributes or relationships for object-level rules. State which are used and how they combine.
- Scope names follow one pattern (`resource:action`) and are documented per operation.
- Central policy evaluation; do not scatter checks inconsistently.
- Authorization applies to list results, search, counts, exports, and subscriptions as well as direct reads.

Example: checks for `GET /orders/{orderId}`.

| Layer     | Check                                                                 |
| --------- | --------------------------------------------------------------------- |
| Operation | Token scope includes `orders:read`                                    |
| Object    | `order.ownerId` equals the caller, or the caller holds a support role |
| Property  | `internalReference` returned only with `orders:admin`                 |
| Tenant    | Query is filtered by the tenant in the token                          |
| State     | Not applicable to reads                                               |

| Good scope names                              | Bad                      |
| --------------------------------------------- | ------------------------ |
| `orders:read`, `orders:write`, `orders:admin` | `admin`, `all`, `scope1` |

## Responses

- 401 with `WWW-Authenticate` challenge (for bearer tokens, include an `error` such as `invalid_token`) for missing or invalid credentials.
- 403 for authenticated callers lacking permission.
- 404 instead of 403 only under a documented policy to hide object existence, applied consistently.
- Failed authentication responses are uniform to avoid account enumeration.

## Per-Protocol Rules

- **REST**: `Authorization` header; per-operation scopes in the contract.
- **GraphQL**: authenticate the HTTP request; authorize per field or per resolver in the domain layer; authorize subscriptions at subscribe time and per event.
- **gRPC**: credentials in call metadata over TLS; mutual TLS between services; per-method authorization.
- **WebSocket**: authenticate during or immediately after the handshake; authorize per subscription and message; handle token expiry on long-lived connections.
- **SSE**: cookie or fetch-based client with `Authorization`; re-check on long streams.
- **Messaging**: broker-level authentication; per-channel publish and subscribe permissions; message-level claims for end-to-end identity.
- **Webhooks**: payload signatures verify the sender; subscription APIs require normal authentication.

## Contract Mapping

- OpenAPI: `components.securitySchemes` (`http` bearer, `apiKey`, `oauth2` flows with scopes, `openIdConnect`, `mutualTLS`); root and per-operation `security`; `security: []` for public operations; 401 and 403 responses.
- AsyncAPI: `components.securitySchemes`; `servers[*].security`; `operations[*].security`.
- Protobuf and GraphQL SDL cannot express authentication: record mechanism, scopes, and per-operation permissions in comments and header notes.

## Anti-Patterns

- Trusting client-provided user, tenant, or role fields.
- Checking authentication but not object-level authorization.
- Long-lived bearer tokens; tokens in URLs.
- API keys as user identity.
- Custom signature or token schemes.
- Accepting any JWT algorithm; skipping `aud` validation.
- Different error text for unknown user versus wrong password.

## Checklist

- [ ] Every operation declares required authentication and permissions.
- [ ] Object-, property-, and tenant-level checks defined.
- [ ] Token validation rules (algorithm, issuer, audience, expiry) stated.
- [ ] Flows follow RFC 9700 (no implicit or password grants).
- [ ] 401, 403, and 404 policy defined.
- [ ] Long-lived connections have an expiry strategy.
- [ ] Draft OAuth 2.1 references are labeled when used.

## Sources

- RFC 6749, 6750, 7636, 7662, 8414, 8628, 8705, 8707, 8725, 9068, 9126, 9449, 9700, 9728.
- OpenID Connect Core 1.0.
- OWASP API Security Top 10 (2023): API1, API2, API3, API5.
