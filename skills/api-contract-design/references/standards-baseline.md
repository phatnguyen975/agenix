# Standards Baseline

## Scope

Use this file only when selecting or verifying a contract format, protocol standard, binding, profile, or draft. Project-pinned versions and compatibility requirements take precedence when still supported and safe. For new contracts, use the baseline below unless the project's toolchain cannot support it; record the fallback, reason, and omitted features in the hand-off report; persist durable project decisions in an ADR or project configuration.

## Version Selection Rules

- Prefer the current published stable specification listed below; do not treat preview, beta, or release-candidate as a stable baseline.
- Confirm parser, validator, generator, gateway, SDK, and runtime support for every feature used. A version label alone does not establish toolchain support.
- Use the supported fallback only when required by a project constraint. State the exact feature omissions and compatibility reason in the hand-off report; pin the selected version in project configuration where applicable.
- For standards that evolve independently (for example, AsyncAPI bindings), pin the document version and each binding version separately.
- Check the authoritative source before pinning a version when network access is available.

## Contract Formats

| Format                 | Baseline               | Fallback                                                | Schema                                                                                                                                                                             | Source                                                       |
| ---------------------- | ---------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| OpenAPI Specification  | 3.2.1                  | 3.1.2                                                   | OAS 3.1/3.2 Schema Object is based on JSON Schema 2020-12 plus the OAS base vocabulary. Features marked 3.2 in the contract reference are unavailable in 3.1.                      | https://spec.openapis.org/oas/latest.html                    |
| AsyncAPI Specification | 3.1.0                  | 3.0.0                                                   | AsyncAPI 3.x has a dedicated Schema Object based on a draft-07 superset. Use a Multi Format Schema Object for other schema languages.                                              | https://www.asyncapi.com/docs/reference/specification/latest |
| Protocol Buffers       | Edition 2026           | Edition 2024; proto3 only for legacy toolchains         | Edition 2026 requires `protoc` 36.0 or later. Edition 2024 requires `protoc` 32.0 or later. Check generated-code/runtime support as well as the compiler.                          | https://protobuf.dev/support/version-support/                |
| GraphQL                | September 2025 edition | October 2021 edition                                    | SDL is the schema language. September 2025 adds OneOf Input Objects and expands `@deprecated` locations; remove those features for the 2021 fallback.                              | https://spec.graphql.org/                                    |
| JSON Schema            | 2020-12                | draft-07 only where required by the host format/tooling | OpenAPI 3.1/3.2 uses its OAS dialect built on 2020-12; AsyncAPI 3.x uses its own draft-07-based Schema Object. Do not transfer keywords between dialects without checking support. | https://json-schema.org/specification                        |

## Protocol and Web Standards

| Standard                                                             | Use                                                                                                                        | Source                                                                                                                                                                                                                              |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RFC 9110 — HTTP Semantics                                            | Method semantics, status codes, request/response fields, safe and idempotent properties                                    | https://www.rfc-editor.org/rfc/rfc9110.html                                                                                                                                                                                         |
| RFC 9111 — HTTP Caching                                              | Cache keys, freshness, validation, shared/private cache behavior                                                           | https://www.rfc-editor.org/rfc/rfc9111.html                                                                                                                                                                                         |
| RFC 10008 — HTTP QUERY Method                                        | Safe, idempotent request method with a query body; use only when clients, intermediaries, gateways, and tooling support it | https://www.rfc-editor.org/rfc/rfc10008.html                                                                                                                                                                                        |
| RFC 9457 — Problem Details for HTTP APIs                             | Standard HTTP error representation (`application/problem+json`)                                                            | https://www.rfc-editor.org/rfc/rfc9457.html                                                                                                                                                                                         |
| RFC 9745 — Deprecation; RFC 8594 — Sunset                            | Lifecycle signaling; they are separate fields with separate semantics                                                      | https://www.rfc-editor.org/rfc/rfc9745.html ; https://www.rfc-editor.org/rfc/rfc8594.html                                                                                                                                           |
| RFC 8288 — Web Linking                                               | `Link` header and relation types                                                                                           | https://www.rfc-editor.org/rfc/rfc8288.html                                                                                                                                                                                         |
| RFC 5789 — PATCH; RFC 7396 — JSON Merge Patch; RFC 6902 — JSON Patch | Partial update method and patch document formats                                                                           | https://www.rfc-editor.org/rfc/rfc5789.html ; https://www.rfc-editor.org/rfc/rfc7396.html ; https://www.rfc-editor.org/rfc/rfc6902.html                                                                                             |
| RFC 6585 — Additional HTTP Status Codes                              | Includes 428 and 429                                                                                                       | https://www.rfc-editor.org/rfc/rfc6585.html                                                                                                                                                                                         |
| RFC 9651 — Structured Field Values for HTTP                          | Structured syntax for HTTP fields where adopted                                                                            | https://www.rfc-editor.org/rfc/rfc9651.html                                                                                                                                                                                         |
| RFC 3339; RFC 9562; RFC 8259; RFC 6901; RFC 4648                     | Timestamps; UUIDs; JSON; JSON Pointer; Base64                                                                              | https://www.rfc-editor.org/rfc/rfc3339.html ; https://www.rfc-editor.org/rfc/rfc9562.html ; https://www.rfc-editor.org/rfc/rfc8259.html ; https://www.rfc-editor.org/rfc/rfc6901.html ; https://www.rfc-editor.org/rfc/rfc4648.html |
| RFC 6455; RFC 8441; RFC 9220                                         | WebSocket over HTTP/1.1 Upgrade, HTTP/2 Extended CONNECT, and HTTP/3 Extended CONNECT                                      | https://www.rfc-editor.org/rfc/rfc6455.html ; https://www.rfc-editor.org/rfc/rfc8441.html ; https://www.rfc-editor.org/rfc/rfc9220.html                                                                                             |
| WHATWG HTML Living Standard — Server-sent events                     | Browser EventSource and SSE wire format                                                                                    | https://html.spec.whatwg.org/multipage/server-sent-events.html                                                                                                                                                                      |
| WHATWG Fetch Standard                                                | Browser CORS processing and fetch behavior                                                                                 | https://fetch.spec.whatwg.org/                                                                                                                                                                                                      |
| RFC 9325 — Recommendations for Secure Use of TLS and DTLS            | TLS deployment guidance; use current security guidance for protocol/cipher configuration                                   | https://www.rfc-editor.org/rfc/rfc9325.html                                                                                                                                                                                         |
| gRPC documentation                                                   | Status codes, deadlines, health checking, retries, and gRPC-Web distinctions                                               | https://grpc.io/docs/                                                                                                                                                                                                               |
| W3C Trace Context                                                    | `traceparent` and `tracestate` propagation                                                                                 | https://www.w3.org/TR/trace-context/                                                                                                                                                                                                |

## Security Standards

| Standard                               | Use                                                                                                            | Source                                                                                                                                                                                |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RFC 6749 and RFC 6750                  | OAuth 2.0 framework and bearer-token usage; apply current security BCPs                                        | https://www.rfc-editor.org/rfc/rfc6749.html ; https://www.rfc-editor.org/rfc/rfc6750.html                                                                                             |
| RFC 9700                               | OAuth 2.0 Security Best Current Practice; current normative security guidance                                  | https://www.rfc-editor.org/rfc/rfc9700.html                                                                                                                                           |
| RFC 7636; RFC 8628                     | PKCE; OAuth device authorization grant                                                                         | https://www.rfc-editor.org/rfc/rfc7636.html ; https://www.rfc-editor.org/rfc/rfc8628.html                                                                                             |
| RFC 8725; RFC 9068                     | JWT Best Current Practices; JWT profile for access tokens                                                      | https://www.rfc-editor.org/rfc/rfc8725.html ; https://www.rfc-editor.org/rfc/rfc9068.html                                                                                             |
| RFC 7662; RFC 9449; RFC 8705           | OAuth token introspection; DPoP; OAuth mTLS client authentication and certificate-bound tokens                 | https://www.rfc-editor.org/rfc/rfc7662.html ; https://www.rfc-editor.org/rfc/rfc9449.html ; https://www.rfc-editor.org/rfc/rfc8705.html                                               |
| RFC 9126; RFC 8707; RFC 8414; RFC 9728 | Pushed Authorization Requests; Resource Indicators; authorization server metadata; protected resource metadata | https://www.rfc-editor.org/rfc/rfc9126.html ; https://www.rfc-editor.org/rfc/rfc8707.html ; https://www.rfc-editor.org/rfc/rfc8414.html ; https://www.rfc-editor.org/rfc/rfc9728.html |
| OpenID Connect Core 1.0                | Identity layer on top of OAuth 2.0; do not treat OAuth alone as an authentication protocol                     | https://openid.net/specs/openid-connect-core-1_0.html                                                                                                                                 |
| OWASP API Security Top 10 — 2023       | API-specific risk taxonomy; not interchangeable with the general web application Top 10                        | https://owasp.org/API-Security/                                                                                                                                                       |
| OWASP Top 10 — 2025                    | General web application risk taxonomy; not a replacement for the API-specific Top 10                           | https://top10.owasp.org/2025/                                                                                                                                                         |

## Draft Standards

The entries below are not finalized Internet Standards unless explicitly marked otherwise. Draft status, version, and expiry can change. Verify the current draft revision from the IETF Datatracker before adopting exact field names or semantics.

| Draft                                     | Status and Use                                                                                                                                                                               | Source                                                                      |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `Idempotency-Key` HTTP field              | IETF Internet-Draft `draft-ietf-httpapi-idempotency-key-header-08`; not an RFC. Follow its current syntax only when the service implements the documented key lifecycle and replay behavior. | https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ |
| `RateLimit` and `RateLimit-Policy` fields | IETF Internet-Draft `draft-ietf-httpapi-ratelimit-headers-11`; not an RFC, and field semantics or syntax may change in later revisions.                                                      | https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/      |
| OAuth 2.1                                 | IETF Internet-Draft `draft-ietf-oauth-v2-1-17`; not an RFC. Use RFC 9700 for current normative OAuth 2.0 security guidance.                                                                  | https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/                     |
| GraphQL over HTTP                         | GraphQL ecosystem draft describing HTTP transport behavior; check current status and implementation support.                                                                                 | https://graphql.github.io/graphql-over-http/                                |

## Ecosystem Conventions

These conventions are not core protocol standards. Identify them as conventions at the relevant consumer-facing description or in linked protocol documentation only when they affect interoperability; verify project-specific compatibility.

| Convention                       | Use                                                                                                                           | Source                                    |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| CloudEvents 1.0.2                | Portable event envelope and protocol bindings; does not replace AsyncAPI.                                                     | https://github.com/cloudevents/spec       |
| Standard Webhooks                | Webhook headers, signatures, and verification; not an IETF RFC.                                                               | https://www.standardwebhooks.com/         |
| Relay Cursor Connections         | GraphQL connection/edge pagination; optional convention, not core GraphQL.                                                    | https://relay.dev/graphql/connections.htm |
| Google API Improvement Proposals | Resource names, pagination, long-running operations, and errors; adopt only where appropriate.                                | https://google.aip.dev/                   |
| Protovalidate                    | Buf ecosystem validation annotations for Protobuf; requires declared dependency and matching compiler/plugin/runtime support. | https://buf.build/docs/protovalidate/     |

## Confirm Before Pinning

Confirm the current edition or field list against the authoritative source before pinning when any of these can affect interoperability: OpenAPI 3.2 tool support; AsyncAPI binding field lists and `bindingVersion`; Protobuf compiler/runtime and generated-code support; GraphQL specification edition and parser support; WebSocket/SSE transport support; MQTT/AMQP versions; Standard Webhooks; W3C Trace Context level; and Internet-Draft status.

## Protocol and Toolchain Notes

- AsyncAPI binding versions are independent of the AsyncAPI document version. Pin each binding's `bindingVersion` and verify its fields against the binding specification for that transport. Do not assume every broker feature is portable across bindings.
- GraphQL core does not define a transport protocol for subscriptions. Document the selected transport and its authentication, reconnect, replay, and flow-control behavior separately.
- Native gRPC uses HTTP/2 and Protobuf. Browser access usually requires gRPC-Web or a gateway; document that additional surface as a distinct interaction.
- WebSocket handshake details depend on the HTTP version: RFC 6455 Upgrade/101 applies to HTTP/1.1; HTTP/2 and HTTP/3 use Extended CONNECT mechanisms.
- SSE uses the WHATWG EventSource format over HTTP; browser EventSource has client API restrictions that do not apply to arbitrary HTTP clients.
- A contract format's ability to describe a protocol feature does not guarantee support in every parser, gateway, SDK generator, or runtime.

## Anti-Patterns

- Citing a version from memory when an authoritative source is reachable.
- Treating an Internet-Draft as a final RFC or omitting its draft status.
- Mixing format versions inside one project without a recorded reason.
- Adopting an unreleased or unsupported successor version as the baseline.
- Assuming schema dialects or binding fields are interchangeable across host formats and protocols.

## Checklist

- [ ] Version matches the project baseline, or a supported fallback with a recorded reason.
- [ ] Compiler, parser, validator, generator, gateway, and runtime support are verified for features used.
- [ ] Any draft or ecosystem convention that affects consumer interoperability is identified by its correct status at the point of use; project dependencies and versions are pinned where required.
- [ ] Schema dialect matches the host contract format.
- [ ] Binding versions are pinned independently where applicable.
