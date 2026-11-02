# API Security

## Contents

- Scope
- Threat Modeling
- OWASP API Top 10 (2023) Controls
- Input and Output Handling
- Transport and Browser Controls
- Sensitive Data
- Protocol-Specific Threats
- Contract Mapping
- Anti-Patterns
- Checklist
- Sources

## Scope

- Security design decisions that belong in the contract and its design notes; authentication and authorization mechanics are in their own concern.

## Threat Modeling

1. Identify assets: data, functions, credentials.
2. Identify actors: legitimate consumers, malicious consumers, insiders, compromised services.
3. Identify trust boundaries and entry points: every operation, stream, channel, and callback.
4. Enumerate threats per entry point (STRIDE: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege).
5. Assign controls (contract-level or design-note) and note residual risk.

- Depth scales with exposure: public and partner APIs and sensitive data get the full pass.

## OWASP API Top 10 (2023) Controls

| Risk                                                 | Design control                                                                                       |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| API1 Broken Object Level Authorization               | Object-level check on every access path; non-guessable identifiers are not a control                 |
| API2 Broken Authentication                           | Standard flows, short-lived tokens, rate limits on authentication endpoints                          |
| API3 Broken Object Property Level Authorization      | Explicit response schemas; allowlisted writable fields; no automatic entity serialization or binding |
| API4 Unrestricted Resource Consumption               | Bounds on page size, payload, rate, concurrency, cost, timeouts                                      |
| API5 Broken Function Level Authorization             | Per-operation permissions; admin operations separated and declared                                   |
| API6 Unrestricted Access to Sensitive Business Flows | Per-flow limits, abuse detection, step-up verification for flows such as purchase and signup         |
| API7 Server-Side Request Forgery                     | Allowlist destinations for any server-fetched URL; block internal ranges; no unvalidated redirects   |
| API8 Security Misconfiguration                       | Explicit CORS, no debug endpoints, disabled verbose errors, controlled reflection and introspection  |
| API9 Improper Inventory Management                   | Every version and operation documented; deprecated versions sunset; no undocumented endpoints        |
| API10 Unsafe Consumption of APIs                     | Validate upstream responses, enforce timeouts and TLS, treat third-party data as untrusted           |

## Input and Output Handling

- Validate every input against the contract schema: type, bounds, format, allowed values; reject unknown fields on writes.
- Enforce `Content-Type`; reject unsupported types with 415.
- Request size, nesting depth, and array length limits are declared and enforced.
- Parameterize all queries; never build queries from raw input (SQL, NoSQL, LDAP, command, template injection).
- Return only fields in the response schema; build responses from explicit view models.
- Normalize and validate identifiers and paths before use (path traversal).
- Server-fetched URLs (webhooks, imports, previews): allowlist schemes and hosts, resolve and block private and link-local ranges after DNS resolution, limit redirects, set timeouts and size limits.
- File uploads: validate type and size, scan content, store outside executable paths, never trust the supplied filename.

| Server-fetched URL                             | Decision                           |
| ---------------------------------------------- | ---------------------------------- |
| `https://hooks.partner.example/orders`         | Accept: HTTPS, public host         |
| `http://hooks.partner.example/orders`          | Reject: not HTTPS                  |
| `https://localhost:8080/`                      | Reject: loopback                   |
| `https://10.0.0.5/`                            | Reject: private range              |
| `https://169.254.169.254/`                     | Reject: link-local                 |
| Public name that resolves to a private address | Reject: check the resolved address |

| Unsafe                                                       | Safe                                                                   |
| ------------------------------------------------------------ | ---------------------------------------------------------------------- |
| Body `{"name": "x", "role": "admin"}` is bound to the entity | Write schema lists `name` only; `role` is rejected as an unknown field |

## Transport and Browser Controls

- TLS for all traffic (1.2 minimum; prefer 1.3); no mixed plaintext endpoints.
- CORS: explicit allowed origins, methods, and headers; never combine wildcard origins with credentials.
- Sensitive responses: `Cache-Control: no-store`.
- `X-Content-Type-Options: nosniff` on responses.
- State-changing requests authenticated by cookies need CSRF defenses (SameSite, tokens, or Origin checks).

```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Credentials: true
Vary: Origin
```

## Sensitive Data

- Classify fields (public, internal, confidential, secret) and mark them in the contract (`writeOnly`, descriptions).
- Return the minimum; mask or omit secrets; never return stored credentials.
- No secrets, tokens, or personal data in URLs, query strings, or error messages (URLs are logged and cached).
- Redact logs and traces; log identifiers, not payloads.
- Encrypt sensitive data at rest and, where brokers or intermediaries are not trusted, end to end.
- Define retention and deletion for personal data exposed through the API.

## Protocol-Specific Threats

| Protocol  | Threats                                                                                 | Controls                                                                        |
| --------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| REST      | Mass assignment, enumeration, verb tampering                                            | Closed write schemas, object-level authz, method allowlist                      |
| GraphQL   | Deep or costly queries, alias and batch abuse, introspection leakage, field suggestions | Depth and cost limits, batching limits, introspection policy, field-level authz |
| gRPC      | Reflection exposure, oversized messages, metadata abuse                                 | Reflection policy, message limits, per-method authz, mTLS                       |
| WebSocket | Cross-site hijacking, message flooding, unauthorized subscriptions                      | `Origin` validation, per-connection rate limits, per-message authz              |
| SSE       | Connection exhaustion, stale authorization                                              | Stream limits, periodic re-authorization                                        |
| Messaging | Poison messages, unauthorized publish, replay, unsigned events                          | Channel ACLs, schema validation, de-duplication, signing where needed           |
| Webhooks  | SSRF through callback URLs, forged deliveries, replay                                   | URL validation, signatures, timestamp window                                    |

## Contract Mapping

- Schemas: `maxLength`, `maxItems`, ranges, `additionalProperties: false` on writes, `readOnly`/`writeOnly`.
- Responses: 401, 403, 413, 415, 429 declared.
- Security schemes and per-operation `security` declared.
- Threat-model outcomes and non-expressible controls recorded in the header notes.

## Anti-Patterns

- Security by obscurity (unguessable ids as the only control).
- Serializing entities directly; binding request bodies directly to entities.
- Wildcard CORS with credentials.
- Verbose errors and public debug or reflection endpoints.
- Unbounded inputs and outputs.
- Treating internal callers as trusted.
- Fetching caller-supplied URLs without validation.

## Checklist

- [ ] Entry points and trust boundaries listed.
- [ ] Each OWASP risk has a control or a recorded reason it does not apply.
- [ ] All inputs bounded and validated by schema; writes reject unknown fields.
- [ ] Server-side URL fetching is validated.
- [ ] CORS, cache, and transport policies stated.
- [ ] Sensitive fields classified; no secrets in URLs or errors.
- [ ] Protocol-specific threats addressed.

## Sources

- OWASP API Security Top 10, 2023 edition (https://owasp.org/API-Security/).
- RFC 9700, RFC 8725; RFC 9110 (CORS-related headers via the Fetch Standard).
- Protocol references: RFC 6455 (Origin), gRPC and GraphQL security documentation.
