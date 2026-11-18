# Baseline and Reconciliation

## Evidence by Role

| Question                                                   | Evidence                                                                                                                                                                                      |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| What is the structure at the selected repository revision? | Toolchain-owned schema declarations, versioned migrations, or a verified schema snapshot produced from that history.                                                                          |
| Why does the shared model behave this way?                 | Approved design decisions, business invariants, data ownership, and lifecycle rules.                                                                                                          |
| What is proposed, and what has integrated?                 | The feature analysis records intent. Verify integration from the selected repository revision and actual migration artifacts. Use version history to trace provenance when links are missing. |
| Which migration has applied in a specific environment?     | Environment-specific migration status or authorized observation, with its scope and provenance.                                                                                               |

Pin the compared revision or snapshot. If executable schema does not yet exist, use the approved design and label it as a design baseline. If both schema declarations and migrations exist, identify which defines intent and how the project confirms they agree. Inspect affected structures and relevant history. Use a trusted replay or snapshot result when structure cannot be determined reliably from inspection. Trace stale or inconsistent evidence to the affected decision rather than resolving material disagreements by preference.

## Parallel Changes

- Compare known pending changes and the latest available integration baseline for the affected objects. Check competing creation, renamed or removed objects, incompatible keys or constraints, backfill assumptions, and intermediate application/schema compatibility.
- Assign shared prerequisites to a single owning change. Record dependent changes, intended order or dependency, and what proves the prerequisite integrated. A proposal or branch-local result is insufficient evidence of integration.
- If a later baseline changes the assumptions, compare the proposed result again and revise the affected analysis. Use the toolchain's ordering, dependency, and history rules. A clean text merge is insufficient evidence that migrations compose.
- Keep a reference to the actual migration path or revision when it exists. Early analysis describes planned outcomes instead. For shared design changes, identify the governing decision and owner for scoped amendment.

## Verification Handoff

Define what implementation should verify on the selected integration candidate: relevant migration history, ordering and dependencies, the resulting schema, and supported versions. Use an empty disposable store to establish clean initialization where applicable. Use a representative prior state with data to test upgrades, constraints, backfills, or recovery. An empty-store replay alone cannot prove existing-data compatibility.

**References:** [Flyway versioned migrations](https://documentation.red-gate.com/flyway/flyway-concepts/migrations/versioned-migrations) and [Django migration dependencies](https://docs.djangoproject.com/en/5.2/topics/migrations/#dependencies) illustrate different ordering models. Verify the actual toolchain's rules.
