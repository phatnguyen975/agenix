# Collections: Pagination, Filtering, Sorting, Search

## Scope

- Operations that return lists or searchable sets, on any protocol.

## Pagination

- Every list is bounded: declare a default page size and a maximum; reject or clamp larger requests, and state which.
- Cursor (keyset) pagination is the default for large or changing datasets: stable under inserts and deletes, cost independent of depth.
  - **Request:** `limit`, `cursor`.
  - **Response:** `items` and `nextCursor` (absent or `null` when no more data).
  - Cursors are opaque, tied to the sort order and filters they were issued for, and may expire; an invalid or expired cursor returns 400 with a stable error code.
  - Sorting must be deterministic: include a unique tie-breaker (identifier) in the order.
- Offset pagination (`offset`, `limit`) only for small, stable datasets; deep offsets are slow and drift under concurrent writes.
- Totals are optional and costly: provide `totalCount` only on request or as an approximate value, and document it.
- HTTP `Link` header (RFC 8288) with `rel="next"` and `rel="prev"` may complement body cursors.
- Do not change paging semantics between pages of one traversal.

```http
GET /orders?limit=2&cursor=eyJpZCI6Im9yZF8wMiJ9 HTTP/1.1
```

```json
{
  "items": [{ "id": "ord_03" }, { "id": "ord_04" }],
  "nextCursor": "eyJpZCI6Im9yZF8wNCJ9"
}
```

Last page: `"nextCursor": null`. Invalid or expired cursor: `400` with problem type `https://example.com/problems/invalid-cursor`.

## Filtering

- Define filterable fields explicitly; every filter has a field, type, operator set, and effect.
- **Simple filters:** one query parameter per field (`status=active`); multiple values as repeated parameters or comma-separated, one convention per API.
- **Ranges:** paired parameters (`createdAfter`, `createdBefore`) or operator syntax (`created[gte]`); one convention per API.
- **Rich filters:** a documented expression language in one `filter` parameter; state grammar, allowed fields, operators, maximum length and complexity.
- Unknown filter fields or operators return 400; they are never silently ignored.
- Filters that cannot be served efficiently (no supporting index) are not offered.
- Filters combine with AND unless the grammar defines OR.

## Sorting

- Declare sortable fields (allowlist), direction syntax (`sort=-createdAt,name` where `-` means descending, or explicit `orderBy`), and the default order.
- Unknown sort fields return 400.
- Always append a unique tie-breaker so paging is deterministic.
- Limit the number of sort keys.

## Search

- Search (relevance-ranked text matching) differs from filtering (exact predicates); expose search as its own parameter (`q`) or operation.
- Document matched fields, normalization (case, accents), operators, minimum query length, and ranking behavior.
- Relevance-sorted results use cursor pagination with a score and identifier as the cursor basis.
- Queries too large or too sensitive for URIs may use QUERY (RFC 10008) when the ecosystem supports it. Otherwise use POST to a search resource as an application convention; POST remains unsafe/non-idempotent under HTTP semantics, so do not assume generic safe-method caching or retries.
- Facets and counts are optional, bounded, and documented as approximate when they are.

| Intent                  | Request                                                                            |
| ----------------------- | ---------------------------------------------------------------------------------- |
| Two statuses            | `GET /orders?status=PAID&status=SHIPPED`                                           |
| Created in a range      | `GET /orders?createdAfter=2026-03-01T00:00:00Z&createdBefore=2026-04-01T00:00:00Z` |
| Newest first, then name | `GET /orders?sort=-createdAt,name`                                                 |
| Only some fields        | `GET /orders?fields=id,status`                                                     |
| Text search             | `GET /orders?q=gift%20card`                                                        |
| Unknown filter          | `GET /orders?colour=red` returns `400`                                             |

## Field Selection and Expansion

- **Sparse fieldsets:** `fields=id,name,status` limit returned properties; unknown fields return 400.
- **Expansion:** `expand=customer` embeds related resources; bound depth and count.
- gRPC uses `google.protobuf.FieldMask` for read and update masks; GraphQL selects fields in the query.
- Defaults return the documented standard representation, not "everything".

## Per-Protocol Mapping

| Protocol        | Paging                                                               | Filter and Sort                              | Contract                                                                 |
| --------------- | -------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------ |
| REST            | `limit` + `cursor` query parameters; `items` + `nextCursor` response | Query parameters or `filter`/`sort`          | OpenAPI parameters with `minimum`, `maximum`, `default`; response schema |
| GraphQL         | Connections with `first`/`after`, `last`/`before`, `pageInfo`        | Typed input arguments                        | SDL arguments and connection types                                       |
| gRPC            | `page_size`, `page_token`, `next_page_token`                         | `filter`, `order_by` strings or typed fields | Request and response messages                                            |
| WebSocket / SSE | Replay from a cursor or last event identifier; snapshot then deltas  | Subscription filters                         | Message and event schemas                                                |
| Messaging       | Consumer offsets; replay windows                                     | Topic and header filtering                   | AsyncAPI channels and bindings                                           |

## Anti-Patterns

- Unbounded lists; unlimited page sizes.
- Offset paging over large mutable tables.
- Unstable ordering without a tie-breaker.
- Cursors that expose internals or can be forged to reach other tenants' data.
- Filtering on any column; ignoring unknown filters silently.
- Changing the default sort order.
- Computing exact totals on every request.

## Checklist

- [ ] Default and maximum page size declared.
- [ ] Cursor semantics, expiry, and invalid-cursor error defined.
- [ ] Sort allowlist, default order, and tie-breaker defined.
- [ ] Filterable fields, operators, and error behavior for unknown names defined.
- [ ] Search semantics documented separately from filters.
- [ ] Authorization applied before pagination, filtering, and counting.
