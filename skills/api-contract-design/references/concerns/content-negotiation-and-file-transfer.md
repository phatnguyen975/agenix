# Content Negotiation and File Transfer

## Scope

- Choosing representations and transferring binary or large payloads over HTTP APIs. For asynchronous export/import job lifecycle, also read `long-running-bulk-operations.md`.

## Representation Negotiation

- Declare each supported request and response media type. `Content-Type` describes the representation sent; `Accept` describes acceptable response media types.
- Return `415 Unsupported Media Type` when the request representation is unsupported. Return `406 Not Acceptable` when no acceptable response representation can be selected, where the API honors `Accept` strictly.
- Do not imply that `Content-Type` validates the payload; validate the actual format and content.
- Use `Content-Encoding` for representation coding such as gzip or br; `Accept-Encoding` expresses acceptable response codings. Keep media type (`Content-Type`) separate from content coding.
- Emit `Vary: Accept-Encoding` when the selected response representation varies by that header.
- Use one canonical JSON representation unless there is a concrete consumer need for additional media types (for example CSV export or a vendor-specific format).
- When representation selection changes cacheable responses, emit the appropriate `Vary` dimensions (for example `Accept`) and align cache policy with `caching-and-conditional-requests.md`.
- Do not advertise media types that the implementation cannot produce or consume.

## Language Negotiation

- Use `Accept-Language` only when the API intentionally localizes human-readable representation content; identify the selected language with `Content-Language` when applicable.
- Use BCP 47 language tags, document supported languages and the default/fallback behavior, and do not assume every requested language is available.
- Emit `Vary: Accept-Language` when a cacheable representation varies by that request header.
- Keep machine-readable values stable and locale-independent: identifiers, enum values, error codes, timestamps, numeric values, and currency amounts must not change meaning with the selected language.
- Do not localize response content implicitly when consumers require deterministic machine-to-machine representations.

## Request Bodies

- **JSON:** use `application/json`; define maximum body size, nesting depth, and array size.
- **Partial updates:** choose and document one patch format per operation/resource. JSON Merge Patch uses `application/merge-patch+json`; JSON Patch uses `application/json-patch+json`.
- **Multipart:** use `multipart/form-data` with per-part media type and encoding metadata. Specify required parts, maximum part size, and whether duplicate part names are allowed.
- **Binary body:** use a specific media type and bounded size. Do not represent arbitrary binary as an unbounded JSON string.

## Uploads

- Small uploads may use multipart or a raw binary body when payload and timeout limits are practical.
- Large or resumable uploads should use a staged upload target or a documented resumable-upload protocol. Define creation, authorization, expiry, completion/finalization, abort, and cleanup behavior.
- Bind an upload target to the intended resource, caller, permitted method, media type, size, and expiry. Treat pre-signed URLs as bearer credentials: short-lived, least-privilege, and never logged or placed in public examples.
- Define whether an upload is visible before finalization and how incomplete or abandoned uploads are removed.

## Downloads and Ranges

- Set `Content-Type` accurately and use `Content-Disposition` for download presentation. Sanitize filenames and prevent header injection; do not trust caller-supplied filenames.
- For large, seekable representations, support byte ranges only when the origin and intermediaries can serve them correctly. A successful range response uses `206 Partial Content` and `Content-Range`; unsatisfiable ranges use `416 Range Not Satisfiable`.
- Advertise byte-range support with `Accept-Ranges: bytes` when supported. Define whether range requests are supported for dynamically generated files.
- `If-Range` can combine validators with range requests; if the validator no longer matches, send the full representation rather than a partial one.
- Define download URL lifetime, authorization, content disposition, maximum size, and whether the resource can be resumed.

## Integrity and Security

- Validate file size, extension as a user-facing hint, declared media type, file signature or magic bytes, and content according to the file class. The declared media type alone is untrusted.
- Scan or quarantine uploads where malware or active content is a risk. Store files outside executable or web-root paths, and apply least-privilege access.
- Define checksum algorithms and encoding only when integrity verification is required; use a collision-resistant hash such as SHA-256. A checksum is not authenticity proof unless it is protected by a trusted signature or channel.
- Apply quotas per caller or tenant, enforce limits while streaming, and defend against decompression bombs and archive path traversal.
- Avoid embedding large file data in API error responses or logs.

## Contract Mapping

- **OpenAPI:** declare media types under `requestBody.content` and `responses.content`; use multipart `encoding`; represent binary bodies according to the OAS version's schema rules; document 413/415/406, and 206/416/Content-Range where applicable.
- **gRPC:** define chunk size, sequence, total-size, checksum, cancellation, and finalization messages; apply explicit message limits at all hops.
- **Messaging:** prefer an external object reference for large payloads; define object authorization, retention, checksum, and lifecycle.
- **AsyncAPI:** use the selected binding and message content type; do not assume the generic message schema defines broker-specific maximum payload size.

## Anti-Patterns

- Accepting a file based only on filename or `Content-Type`.
- Unbounded multipart or streaming bodies.
- Long-lived pre-signed URLs or URLs leaked into logs and errors.
- Treating a checksum as authentication.
- Range support without stable representation validators.
- Returning file bytes inside ordinary JSON for large transfers.

## Checklist

- [ ] Media types, content codings, and negotiation behavior are documented.
- [ ] Language negotiation, fallback, and cache variation are explicit when localization is supported.
- [ ] Request, part, and response sizes are bounded.
- [ ] Upload authorization, expiry, finalization, and cleanup are defined.
- [ ] Download filename, media type, authorization, and lifetime are defined.
- [ ] Range, partial-content, and validator semantics are correct where supported.
- [ ] Content validation, malware handling, and integrity controls are appropriate to the file type.
