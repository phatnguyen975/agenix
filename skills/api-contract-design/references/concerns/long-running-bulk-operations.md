# Long-Running and Bulk Operations

## Scope

- Work that outlasts a request time budget, requests that carry many items, and asynchronous import/export jobs.
- For HTTP media negotiation and byte-level upload/download behavior, use `content-negotiation-and-file-transfer.md`.

## Long-Running Operations

- **Trigger:** the operation cannot reliably finish within the request timeout.
- **HTTP pattern:**
  - **Start:** `POST` returns `202 Accepted` with a `Location` header to an operation resource, and optionally `Retry-After`.
  - **Operation resource:** `id`, `status` (`pending`, `running`, `succeeded`, `failed`, `cancelled`), optional progress, `createdAt`, `updatedAt`, `expiresAt`, and either `result` (or a link to it) or `error` (Problem Details).
  - **Poll:** `GET` on the operation; the response may carry `Retry-After` to pace polling.
  - **Cancel:** `DELETE` on the operation or a documented cancellation action; define what already-completed work remains.
  - Finished operations stay available for a documented retention period, then return 404 or 410.
- When clients may retry a start after an ambiguous outcome, define duplicate suppression (for example, an idempotency key or client operation ID). Repeating the same logical start within the retention window must not create a second job.
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
- When a batch may be retried after an ambiguous outcome, define duplicate suppression at batch level. For partial retries or item-level replay, use stable client item identifiers and define whether already-processed items are skipped, replayed, or returned unchanged.
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

- Model an export as a long-running operation whose result becomes a downloadable artifact; define when it is ready, how it is authorized, and when its access expires.
- Model an import as a job with explicit upload association, validation, processing, partial-failure, and completion semantics.
- Define whether the artifact remains available after the operation resource expires and how consumers discover that state.
- Delegate media types, multipart, byte ranges, resumable transfer, integrity, content validation, and file security to `content-negotiation-and-file-transfer.md`.

## Per-Protocol Mapping

| Protocol        | Long-running                                                                                             | Bulk                                         |
| --------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| REST            | 202 + operation resource                                                                                 | Batch endpoint or batch resource             |
| GraphQL         | Mutation returns operation identifier; poll through a query or subscribe                                 | Mutation with list input, bounded            |
| gRPC            | Long-running operation resource (`google.longrunning.Operation` pattern) or server streaming of progress | Batch methods with repeated items; streaming |
| WebSocket / SSE | Progress events on a stream; final event with result                                                     | Not applicable                               |
| Messaging       | Command message, then progress and completion events correlated by identifier                            | Batched messages with per-item outcomes      |

## Contract Mapping

- **OpenAPI:** `202` response with `Location` header; operation schema in `components`; `GET`/`DELETE` operation paths; bulk request and per-item result schemas with `maxItems`; artifact links and expiry in the operation result.
- **Protobuf:** operation messages or the long-running operation pattern; `repeated` items with documented maximum.
- **AsyncAPI:** command, progress, and completion messages with `correlationId`.
- Put consumer-visible operation-resource retention, batch limits, and atomicity guarantees in the relevant operation/resource descriptions and schema constraints. Keep internal cleanup and storage policy in operational documentation unless it affects consumers.

## Anti-Patterns

- Holding connections open for minutes instead of 202 + operation.
- No expiry for operation resources or upload targets.
- Bulk endpoints without item and size limits.
- Ambiguous atomicity; results not mapped to request items.
- Returning 200 with no per-item outcome.
- Unauthenticated download links with unlimited lifetime.

## Checklist

- [ ] Operation lifecycle, statuses, polling, cancel, and retention defined.
- [ ] Duplicate-start behavior is defined when clients may retry after an ambiguous outcome.
- [ ] Bulk limits, atomicity, and per-item results defined.
- [ ] Import/export artifact association, readiness, authorization, and access expiry defined when applicable.
- [ ] Completion notification mechanism chosen and documented.
