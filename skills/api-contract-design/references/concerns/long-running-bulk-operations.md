# Long-Running and Bulk Operations

## Contents

- Scope
- Long-Running Operations
- Bulk Operations
- File Transfer
- Per-Protocol Mapping
- Contract Mapping
- Anti-Patterns
- Checklist
- Sources

## Scope

- Work that outlasts a request time budget, requests that carry many items, and transfer of large files.

## Long-Running Operations

- Trigger: the operation cannot reliably finish within the request timeout.
- HTTP pattern:
  - Start: `POST` returns `202 Accepted` with a `Location` header to an operation resource, and optionally `Retry-After`.
  - Operation resource: `id`, `status` (`pending`, `running`, `succeeded`, `failed`, `cancelled`), optional progress, `createdAt`, `updatedAt`, `expiresAt`, and either `result` (or a link to it) or `error` (Problem Details).
  - Poll: `GET` on the operation; the response may carry `Retry-After` to pace polling.
  - Cancel: `DELETE` on the operation or a documented cancellation action; define what already-completed work remains.
  - Finished operations stay available for a documented retention period, then return 404 or 410.
- Starting operations is idempotent through an idempotency key; repeated starts return the same operation.
- Completion notification options: polling, webhook callback, SSE or WebSocket events, or a message on a channel.
- Define timeouts for the operation itself and what happens at expiry.
- Authorize operation access to the caller that started it (and administrators).

```http
POST /exports HTTP/1.1
Idempotency-Key: "5b1f0f1e-7c1a-4a43-9c0e-2f6f7b9d1a11"

HTTP/1.1 202 Accepted
Location: /operations/op_77
Retry-After: 5
```

```json
{
  "id": "op_77",
  "status": "running",
  "progress": 0.4,
  "createdAt": "2026-03-01T09:30:00Z",
  "expiresAt": "2026-03-02T09:30:00Z"
}
```

```json
{
  "id": "op_77",
  "status": "succeeded",
  "result": {
    "downloadUrl": "https://files.example.com/exports/op_77",
    "expiresAt": "2026-03-01T10:30:00Z"
  }
}
```

## Bulk Operations

- Provide a bulk operation only when per-item calls are too costly; otherwise keep single-item operations.
- Decide and document atomicity: all-or-nothing (transaction) or partial success.
- Partial success:
  - Return per-item results in request order, each with `status`, an identifier or index, and an error (Problem Details) when failed.
  - The overall status reflects the batch: 200 with item errors, or 207 Multi-Status where the project already uses it.
- Limit item count and total size; reject larger batches with 413 or 400 and a stable error code.
- Idempotency applies to the batch (batch-level key) and to items (client-supplied item identifiers).
- Validate all items before applying when atomic; report all validation errors.
- Large batches run as long-running operations.
- Bulk reads: fetch many resources by identifier list, bounded in count.

```json
{
  "items": [
    { "clientId": "a1", "sku": "ABC-1", "quantity": 2 },
    { "clientId": "a2", "sku": "", "quantity": 1 }
  ]
}
```

```json
{
  "results": [
    { "clientId": "a1", "status": "created", "id": "ord_1" },
    {
      "clientId": "a2",
      "status": "failed",
      "error": {
        "type": "https://example.com/problems/validation-error",
        "title": "Invalid item",
        "status": 422
      }
    }
  ]
}
```

## File Transfer

- Small files: `multipart/form-data` or a binary body with an explicit `Content-Type`, with size limits (413) and type validation (415).
- Large files: two-step upload (request an upload target, then upload directly), or a resumable upload protocol; define expiry of upload targets.
- Downloads: support range requests (`Range`, `206 Partial Content`) for large files; set `Content-Type` and `Content-Disposition`.
- Exports: model as a long-running operation producing a time-limited download link.
- Validate content type and content, scan for malware, store outside executable paths, and never trust client-supplied filenames.
- Integrity: provide checksums where corruption matters.

## Per-Protocol Mapping

| Protocol        | Long-running                                                                                             | Bulk                                         |
| --------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| REST            | 202 + operation resource                                                                                 | Batch endpoint or batch resource             |
| GraphQL         | Mutation returns operation identifier; poll through a query or subscribe                                 | Mutation with list input, bounded            |
| gRPC            | Long-running operation resource (`google.longrunning.Operation` pattern) or server streaming of progress | Batch methods with repeated items; streaming |
| WebSocket / SSE | Progress events on a stream; final event with result                                                     | Not applicable                               |
| Messaging       | Command message, then progress and completion events correlated by identifier                            | Batched messages with per-item outcomes      |

## Contract Mapping

- OpenAPI: `202` response with `Location` header; operation schema in `components`; `GET`/`DELETE` operation paths; bulk request and per-item result schemas with `maxItems`; multipart `encoding`; `206` and `Range` for downloads.
- Protobuf: operation messages or the long-running operation pattern; `repeated` items with documented maximum.
- AsyncAPI: command, progress, and completion messages with `correlationId`.
- Header notes: retention of operation resources, batch limits, atomicity.

## Anti-Patterns

- Holding connections open for minutes instead of 202 + operation.
- No expiry for operation resources or upload targets.
- Bulk endpoints without item and size limits.
- Ambiguous atomicity; results not mapped to request items.
- Returning 200 with no per-item outcome.
- Unauthenticated download links with unlimited lifetime.

## Checklist

- [ ] Operation lifecycle, statuses, polling, cancel, and retention defined.
- [ ] Start is idempotent.
- [ ] Bulk limits, atomicity, and per-item results defined.
- [ ] File size, type, expiry, and integrity rules defined.
- [ ] Completion notification mechanism chosen and documented.

## Sources

- RFC 9110 (202, 206, Range, 413, 415), RFC 9457 (error results).
- Google API Improvement Proposals (long-running operations, batch methods).
- gRPC `google.longrunning` operations.
