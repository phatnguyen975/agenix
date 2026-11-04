# Versioning and Compatibility

## Scope

- Evolving contracts without breaking consumers; classification of changes; deprecation lifecycle.

## Compatibility Model

- **Backward compatibility:** consumers written against the old contract keep working with the new provider.
- **Forward compatibility:** old providers tolerate messages from new consumers (tolerant reader: ignore unknown fields).
- **Hyrum's Law:** with enough users, every observable behavior is depended on, including field order, timing, and error text; treat observable changes as potentially breaking.
- In message-based systems both directions matter, because producers and consumers deploy independently.
- Every consumer-visible behavior is part of the contract.

## Change Classification

| Class    | Rule                                                 |
| -------- | ---------------------------------------------------- |
| Additive | Existing consumers keep working without changes      |
| Breaking | Some correct existing consumer can fail or misbehave |

**Additive:**

- New optional request field, parameter, header.
- New response field (when consumers ignore unknown fields).
- New operation, endpoint, event type, channel, RPC, or type.
- New enum value or union member on output when the contract states that consumers must tolerate unknown values.
- Relaxing request validation.
- Documentation-only changes.

**Breaking:**

- Removing or renaming any operation, field, parameter, enum value, event type, channel, or RPC.
- Making an optional request field or parameter required; adding a required field.
- Changing a field's type, format, units, meaning, or default value.
- Tightening request validation (shorter limits, new patterns).
- Changing response guarantees (non-null to nullable; removing documented values; reducing precision).
- Changing status codes, error codes, or error types consumers handle.
- Changing authentication, scopes, or required permissions.
- Changing pagination, ordering, or identifier formats.
- Changing delivery or ordering guarantees; changing message keys.
- Adding an enum value or union member, unless the contract states that consumers must tolerate unknown values.
- Renaming an `operationId` or another identifier that generated code depends on.
- Changing a protobuf field number or reusing a removed number or name.

When classification is uncertain, treat the change as breaking. Breaking changes need explicit user approval, a migration path, and a deprecation period.

| Change                                                               | Class    |
| -------------------------------------------------------------------- | -------- |
| Add optional request field `description`                             | Additive |
| Add response field `owner`                                           | Additive |
| Remove response field `status`                                       | Breaking |
| Make optional request field `status` required                        | Breaking |
| Reduce request `name` maxLength from 200 to 100                      | Breaking |
| Add enum value `DELETED` with no tolerance statement in the contract | Breaking |
| Rename `operationId` `listProjects` to `listAllProjects`             | Breaking |
| Add operation `archiveProject`                                       | Additive |

## Versioning Strategies

| Strategy                          | Use                                                               |
| --------------------------------- | ----------------------------------------------------------------- |
| Major version in URI path (`/v2`) | HTTP APIs with uncontrolled consumers; visible and cache-friendly |
| Version in media type or header   | When URIs must stay stable; requires client discipline            |
| Version-less evolution            | GraphQL; additive changes plus deprecation                        |
| Versioned package                 | gRPC (`package company.domain.v1`)                                |
| Versioned message type or channel | Messaging, WebSocket subprotocol, webhooks                        |

- Use one strategy per surface; only major versions appear in identifiers.
- `info.version` follows semantic versioning: major for breaking, minor for additive, patch for corrections.
- Prefer additive evolution; introduce a new major version only for unavoidable breaking changes.
- Limit concurrently supported majors (typically two) and publish the support window.
- Opt-in behavior changes use new fields or parameters, not silent changes.

**Example:** `/v1/orders` becomes `/v2/orders` for a breaking change; `info.version` moves from `1.4.0` to `2.0.0`. An additive change keeps `/v1` and moves `info.version` from `1.4.0` to `1.5.0`.

## Deprecation and Sunset

- **Lifecycle:** announce, mark deprecated, monitor usage, set sunset date, remove.
- **Contract markers:** `deprecated: true` (OpenAPI), `@deprecated(reason: ...)` (GraphQL), `[deprecated = true]` (Protobuf); where a format has no flag, state it in the description.
- Name the replacement and the sunset date in the description.
- HTTP runtime signals:
  - `Deprecation: @<unix-timestamp>` (RFC 9745; the value is a date item, for example `@1688169599`).
  - `Sunset: <HTTP-date>` (RFC 8594).
  - `Link` headers with relation `deprecation` (RFC 9745) and `sunset` (RFC 8594) pointing to documentation.
- Track usage per deprecated element; remove only after the sunset date, and extend when active consumers remain.
- Provide a migration guide and run old and new versions in parallel during the sunset period.

```http
Deprecation: @1788220800
Sunset: Tue, 01 Dec 2026 00:00:00 GMT
Link: <https://example.com/docs/migrate-v2>; rel="deprecation"; type="text/html"
```

## Per-Format Rules

- **OpenAPI:** compare documents; changes to `required`, types, enums, status codes, parameters, and security are the main breaking vectors; new optional properties are additive.
- **JSON payloads:** closed request schemas make new client fields rejected by old servers; response schemas stay open.
- **Protobuf:**
  - Never renumber or reuse fields; `reserved` removed numbers and names.
  - Adding fields and enum values is compatible.
  - Changing a type incompatibly, moving fields into or out of a `oneof`, and renaming a package, service, or RPC are breaking.
  - `buf breaking` is a common automated check.
- **GraphQL:** add freely; deprecate before removing; changing nullability, argument requirements, or types is breaking in the directions listed in the GraphQL SDL reference.
- **AsyncAPI and messaging:** schema compatibility modes (backward, forward, full) per channel; breaking changes publish a new message type version or channel; keep old versions until all consumers migrate.
- **Webhooks:** pin a payload version per subscription; additive changes are unannounced; breaking changes follow the migration window.

## Update Procedure

1. Read the current contract, project compatibility policy, relevant descriptions, and linked documentation.
2. Apply the requested change.
3. Diff old and new contracts; list every difference.
4. Classify each difference (additive or breaking) using this reference.
5. For each breaking difference: present options (additive alternative, new version, opt-in field), obtain approval, add migration and deprecation information.
6. Record classification in the hand-off; update deprecation markers, affected element descriptions, and migration documentation where needed.

## Anti-Patterns

- Silent behavior changes under the same version.
- Removing fields without deprecation.
- New required request fields in a minor release.
- Version numbers in every identifier (`v1.2.3` in URIs).
- Supporting unlimited old versions indefinitely.
- Reusing removed names or numbers for new meaning.
- Deprecation without replacement, date, or usage tracking.

## Checklist

- [ ] Every change is classified; uncertain ones are treated as breaking.
- [ ] Breaking changes have approval, migration path, and deprecation signals.
- [ ] One versioning strategy per surface; only major versions in identifiers.
- [ ] `info.version` change matches the change class.
- [ ] Deprecated elements carry replacement and sunset date.
- [ ] Format-specific rules (reserved fields, nullability, schema compatibility) applied.
