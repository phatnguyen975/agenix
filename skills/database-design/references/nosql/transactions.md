# NoSQL Transactions

Prefer single-document atomic writes when the aggregate and invariant fit one document. Use multi-document transactions only when a business operation truly requires cross-document atomicity.

## Atomicity Boundaries

- MongoDB writes are atomic at the single-document level, including updates to multiple fields and embedded values in that document.
- Design an aggregate boundary around data that must be read/updated together and whose growth remains bounded.
- Use a multi-document transaction when multiple documents/collections must commit or abort together and a schema redesign cannot reasonably place the invariant in one document.
- Do not confuse atomic commit or snapshot reads with serializable predicate enforcement. Concurrent transactions can read the same condition and update disjoint documents; a transaction alone does not guarantee that every cross-document invariant is preserved.
- For a cross-document invariant, identify a conflict protocol: a unique index where expressible, a shared guard/aggregate document that every competing writer updates conditionally in the same transaction, or a model that moves the invariant into one atomic document. All writers must follow the same protocol.
- Do not use transactions to compensate for an unnecessarily fragmented model. Document transaction scope, contention, and operational cost.
- MongoDB time-series collections cannot be written to within multi-document transactions, although reads are supported. A transaction workflow must not include a time-series write; use a separate supported workflow or choose a regular collection when atomic transactional writes are required.

## Concurrency Control

| Situation                              | Candidate Mechanism                                                                                                                    | Required Contract                                                                       |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| State mutation within one document     | Conditional atomic update with expected state in filter                                                                                | Treat no match as conflict or invalid transition                                        |
| Counter/balance bounded by a predicate | Atomic `$inc` with predicate in update filter                                                                                          | Ensure predicate and update are one operation                                           |
| Rare conflicts or long user editing    | Version field and conditional update                                                                                                   | Zero matched documents signals stale version                                            |
| Unique business key                    | Unique index                                                                                                                           | Handle duplicate-key error; never check-then-insert                                     |
| Cross-document invariant               | Unique constraint where possible; otherwise a shared write-conflict anchor/guard document updated conditionally inside the transaction | Snapshot reads alone are insufficient; all competing writers must use the same protocol |

Example conditional state transition:

```javascript
db.orders.updateOne(
  { _id: orderId, status: "pending", version: expectedVersion },
  { $set: { status: "paid" }, $inc: { version: 1 } },
);
```

Example shared guard for a minimum-coverage invariant; this conditional update must be part of the same transaction as the member change, and every writer must update the same guard. If `matchedCount` is zero, abort the transaction and do not apply the member change:

```javascript
db.teamRoster.updateOne(
  { _id: teamId, onCallCount: { $gt: 1 } },
  { $inc: { onCallCount: -1 } },
);
```

- Single-document atomicity does not mean every business invariant is automatically protected. Include all required predicate conditions in the update filter.
- Make all writers follow the same invariant protocol. A read in one service followed by an unconditional write in another can bypass application-level rules.

## Read and Write Concern

- Choose read and write concern from durability, staleness, causal ordering, and latency requirements; state the required guarantee.
- `majority` write concern waits for majority acknowledgement and is the usual durability choice for critical committed data, subject to deployment replication configuration.
- `local` reads may include data later rolled back; `majority` reads return majority-committed data; snapshot reads provide a consistent snapshot in supported transaction contexts.
- Causally consistent sessions with appropriate majority read/write concern can provide read-your-own-writes and related causal guarantees across operations.
- State visibility separately from durability. A majority read does not guarantee that no newer write exists.

## Retry and Idempotency

- Drivers may label transaction failures `TransientTransactionError` or commits `UnknownTransactionCommitResult`. Retry the whole transaction for transient transaction errors; retry the commit for an unknown commit result according to driver guidance. Do not blindly replay the transaction body after an uncertain commit.
- Make transaction bodies safe to retry: avoid external side effects inside them; use an outbox or idempotent follow-up after commit.
- Give client-retryable commands a stable operation/request ID with a unique constraint. `$inc` and other non-idempotent updates must not be replayed without deduplication.
- Bound retries and define the client-visible conflict/timeout outcome.

## Output Mapping

In `Transactions and Concurrency`, record each write pattern's collections/documents, invariant, single- versus multi-document atomicity, read/write concern, concurrency control, expected contention, retry semantics, idempotency key, and failure behavior. Explicitly mark time-series writes as outside multi-document transactions.
