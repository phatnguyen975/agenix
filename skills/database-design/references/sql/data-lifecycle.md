# SQL Data Lifecycle

Design audit metadata, change history, deletion, retention, and archival only when required by the domain, operations, or applicable policy.

## Audit Metadata

- Add `created_at` when creation time is meaningful. Use `timestamptz` for an instant; use a date type for a calendar date.
- Add `updated_at` only when consumers need the last-modified instant. State whether the application or a database trigger maintains it; a default alone does not update it.
- Add actor identifiers only when attribution is required. Reference an actor table when referential integrity and actor lifecycle make that useful; otherwise document the identifier contract.
- Do not add the same audit columns mechanically to immutable facts, pure junction tables, or fixed reference data.

## Change History

Choose the smallest mechanism that preserves the required history semantics.

| Mechanism                      | Model                                                                                                          | Use When                                                                               |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Current row plus history table | Copy the relevant values into an append-only history relation with operation, effective/change time, and actor | Audit trail is required while current-state reads should remain simple                 |
| Versioned rows                 | Store validity intervals and prevent overlapping versions for the same business key                            | Users query what was valid at a point in business time                                 |
| Event log                      | Append domain events with stable event identity and event time                                                 | Events are business facts, replay/integration matters, or a temporal audit is required |
| Generic audit record           | Store entity type, identifier, operation, changed fields/payload, actor, and time                              | Uniform audit is more important than strongly typed history queries                    |

- Distinguish **valid time** (when a fact is true in the domain) from **transaction time** (when the system recorded it).
- Define whether history records before/after values, full snapshots or deltas, actor identity, reason, and correlation/request ID.
- Protect append-only history with privileges and controlled write paths. A trigger or application convention alone is not an immutability guarantee if writers can update/delete the history table.
- Do not use a generic JSON audit log when history fields need frequent joins, constraints, or selective querying.

## Deletion and Retention

| Strategy      | Model                                                                       | Consequences to Specify                                                                       |
| ------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Hard delete   | Physically delete the row                                                   | Foreign-key action, dependent records, audit obligations, and recoverability                  |
| Soft delete   | Nullable deletion marker or explicit lifecycle state                        | Active-row uniqueness, default filtering, child behavior, restore semantics, and purge policy |
| Archive       | Move or copy data to a separately governed store/table                      | Atomicity, query access, schema evolution, restore path, and retention                        |
| Anonymization | Irreversibly transform personal attributes while preserving permitted facts | All copies, history, exports, backups, and re-identification risk                             |

- Derive retention periods and deletion obligations from confirmed requirements or applicable policy. Mark unknown periods `Not specified`; never invent a legal retention period.
- Soft deletion does not remove foreign-key references or automatically hide rows. Define which queries exclude deleted records and whether children remain visible.
- A uniqueness rule for active records may require a partial unique index, for example `UNIQUE (email) WHERE deleted_at IS NULL` in PostgreSQL.
- Anonymization must cover history, archives, JSON payloads, derived tables, and downstream copies within the stated scope. Do not claim that pseudonymization is anonymization.
- Prefer partition detach/drop for eligible high-volume time-based retention only when partitioning already matches the workload and retention boundary. It is not a universal replacement for deletion.
- Distinguish logical deletion from physical erasure in backups and replicas; state any operational delay as an explicit requirement or limitation.

## Example

Active-only business-key uniqueness for soft-deleted accounts:

```sql
CREATE UNIQUE INDEX uq_accounts_email_active
  ON accounts (tenant_id, email_normalized)
  WHERE deleted_at IS NULL;
```

The query contract must also define whether ordinary reads exclude deleted rows and how restoring a row handles a key that has since been reused.

## Output Mapping

In `Data Lifecycle`, record audit fields and their maintenance owner; history mechanism and semantics; deletion/restore behavior; retention trigger and period; archival/purge mechanism; and source requirement for each affected entity/table. Use `Not specified` only for material non-blocking unknowns. If a legally or contractually required retention rule is unresolved, stop and clarify before finalizing; omit non-applicable rows and empty subsections.
