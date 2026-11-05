# SQL Transactions

Define atomic write boundaries, concurrency protection, isolation, and retry behavior from business invariants and access patterns.

## Transaction Boundaries

- Group the smallest set of writes that must commit or roll back together to preserve one business operation.
- For each write access pattern, list participating tables, invariant, transaction boundary, and externally visible side effects.
- Keep transactions short. Do not wait for user input, remote API calls, message delivery, or other unbounded external work while holding database locks.
- Use an outbox or another durable handoff when a committed database change must trigger an external message; publish after commit and make consumers idempotent.

## Isolation and Anomalies

Choose isolation based on the anomaly the invariant must prevent, not on a generic preference for stronger isolation.

| PostgreSQL Level         | Relevant Behavior                                                                                                                           | Design Guidance                                                                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Read Committed (default) | Each statement sees a snapshot as of that statement. A transaction can observe different committed states across statements.                | Suitable when constraints, atomic statements, or explicit locks protect the invariant.                                                               |
| Repeatable Read          | Uses a transaction-wide snapshot; conflicting concurrent updates can cause serialization failures. It can still permit write-skew patterns. | Useful for stable multi-statement reads; do not assume it protects every cross-row invariant.                                                        |
| Serializable             | Detects executions that cannot be placed in a serial order and aborts a transaction when necessary.                                         | Use for invariants spanning rows/predicates when constraints or explicit locking do not provide a simpler safe design. Retry serialization failures. |

- PostgreSQL maps Read Uncommitted to Read Committed.
- State the invariant and possible anomaly explicitly (lost update, write skew, duplicate creation, overselling, stale decision) before selecting a mechanism.
- Prefer declarative constraints and atomic statements over read-then-write application checks.

## Concurrency Mechanisms

| Invariant / Workload                           | Candidate Mechanism                                                   | Required Behavior                                                                       |
| ---------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Single-row balance/counter bound               | Atomic conditional `UPDATE` plus `CHECK` constraint                   | A rejected update is handled as a conflict/business outcome                             |
| Read-modify-write on known rows                | `SELECT ... FOR UPDATE` or an atomic update                           | Lock only the rows required; define lock order                                          |
| Shared read where conflicting writes must wait | Appropriate row-level lock, such as `FOR SHARE`                       | Identify which updates/deletes must be blocked                                          |
| Work queue                                     | `FOR UPDATE SKIP LOCKED`                                              | Claim work transactionally; tolerate duplicate delivery with idempotent processing      |
| Fail-fast contention                           | `NOWAIT` or bounded lock timeout                                      | Return a defined retry/conflict response                                                |
| Optimistic concurrency                         | Version column and conditional update                                 | Zero rows updated means stale version/conflict                                          |
| Concurrent unique-key creation                 | Unique constraint plus `INSERT ... ON CONFLICT` or equivalent         | Never rely on check-then-insert alone                                                   |
| Cross-row predicate invariant                  | Constraint where expressible, explicit lock protocol, or Serializable | Every writer must follow the same protocol; otherwise use a database-enforced invariant |

- Acquire multiple locks in a consistent order to reduce deadlocks.
- A trigger that queries other rows does not automatically make a cross-row rule concurrency-safe. Require suitable locking, a declarative constraint, or Serializable execution.
- Sequence/identity values can have gaps. Use a serialized counter only when a gap-free number is an explicit requirement and accept its contention cost.

## Retry and Idempotency

- Treat PostgreSQL serialization failures (`40001`) and deadlocks (`40P01`) as transaction-level failures. Retry the entire transaction in a fresh transaction, with bounded attempts and backoff, or return a defined conflict.
- Never retry only the failed statement when earlier reads/writes inform the decision.
- Make retryable operations idempotent. Use a stable request/operation identifier with a unique constraint when clients may repeat submissions.
- Do not perform irreversible external side effects before commit. Use an outbox, idempotency key, or compensating workflow where required.

## Example

Protect a single-row withdrawal with one conditional statement rather than a separate read followed by a write:

```sql
UPDATE accounts
SET balance = balance - $1
WHERE id = $2 AND balance >= $1
RETURNING id, balance;
```

No returned row means the account was absent or the balance predicate failed; the application must distinguish those outcomes only if the domain requires it. A transfer between two accounts needs a transaction and a consistent lock order.

## Output Mapping

In `Transactions and Concurrency`, record each write access pattern's invariant, tables, transaction boundary, isolation level, concurrency mechanism, lock ordering, conflict response, retry policy, idempotency strategy, and external handoff. Use `Not applicable` for read-only patterns.
