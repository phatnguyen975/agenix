# Incremental Change Patterns

Use when **an existing running system** must change safely while continuing to serve users. Patterns structure migrations; they are not architecture styles and do not justify the migration by themselves.

## Choose by Change Boundary

| Change Situation                          | Candidate Pattern     | Principal Risk                               |
| ----------------------------------------- | --------------------- | -------------------------------------------- |
| Replace exposed functionality gradually   | Strangler Fig         | Misrouting, split data ownership             |
| Replace a deeply used internal dependency | Branch By Abstraction | Abstraction grows into permanent indirection |
| Evolve an incompatible published contract | Parallel Change       | Legacy consumer never migrates               |
| Separate deploy from feature release      | Feature Toggle        | Stale flags, behavior explosion              |
| Compare old/new behavior before cutover   | Parallel Run          | Duplicate side effects, false comparisons    |
| Integrate incompatible domain semantics   | Anti-Corruption Layer | Leakage and translation divergence           |

## Patterns

### Strangler Fig

- **Mechanism:** route a selected slice at a stable entry boundary to old or new implementation; move slices gradually; retire the old path when dependencies and data ownership are migrated.
- **Fit:** replaceable externally accessible capabilities and a high-risk big-bang cutover.
- **Design obligations:** routing ownership, traffic selection, data synchronization, rollback, observability, security, old-path retirement.
- **Example:** first send order-history reads to a new query path while writes remain authoritative in legacy storage; reconcile results and lag before switching more traffic. Never describe dual writes as safe without an explicit consistency and recovery plan.

### Branch by Abstraction

- **Mechanism:** introduce a stable seam around an internal dependency; migrate callers behind it; implement old and new providers; switch and remove old dependency.
- **Fit:** replacing an internal persistence/integration library or subsystem where a boundary router cannot intercept calls.
- **Watch:** back-and-forth changes in callers, contract mismatch and excessive permanent abstraction.

### Parallel Change (Expand, Migrate, Contract)

- **Mechanism:** add a compatible new contract/schema **while retaining old support**; migrate producers and consumers; verify no old consumers remain; remove old compatibility.
- **Fit:** database and API/event evolution across staggered deployments.
- **Example:** add `customerReference` while preserving `customerId`; update consumers; observe legacy usage; delete `customerId` only after compatibility and rollback requirements are met. A database migration may need read/write precedence and backfill/reconciliation design.

### Feature Toggles

**Mechanism:** choose runtime behavior without a fresh deployment. Consider release, experiment, operations and permissioning toggles as different lifetimes and risk profiles. State owner, intended lifecycle, security implications and removal condition. **Do not treat toggles as substitutes for authorization.** Limit simultaneous combinations and make fail-safe behavior explicit.

### Parallel Run

- **Mechanism:** process equivalent inputs through old and new paths, compare results, and keep a designated authoritative path until validated.
- **Precondition:** isolate external effects, irreversible actions and notifications; comparison rules handle nondeterminism, timing and allowed differences.
- **Done when:** representative cases and exceptions pass agreed criteria; cutover and rollback plans exist.

### Anti-Corruption Layer

- **Mechanism:** translate external/legacy data and semantics into the owning model's terms.
- **Fit:** integration when meanings differ and must stay separate. It may be permanent at an external integration boundary or temporary during migration.
- **Watch:** hidden business rules, unclear ownership, model/version drift and transformation loss.

## Migration Design Record

For **each significant step**, record in System Design §4.3:

1. **Scope and driver:** what changes, why, and the baseline/target elements.
2. **Compatibility and data:** producer/consumer compatibility; source of truth; backfill, duplication, synchronization and reconciliation.
3. **Rollout/cutover:** order of steps, selection strategy, safe pause points and reversible vs irreversible operations.
4. **Verification and feedback:** meaningful metrics, difference checks, contract tests, failure rehearsal and owner role.
5. **Rollback or forward recovery:** state that must be preserved, and what happens if the previous binary cannot read a migrated schema.
6. **Retirement:** proof that old consumers, paths, data copies and toggles are no longer needed.

**Example phased plan:** (1) add compatibility adapter; (2) mirror read-only requests and compare outcomes; (3) route a small agreed share to the new implementation; (4) monitor and expand; (5) deprecate the old path after contract and data checks. Each phase remains releasable; rollback capability may decrease after a destructive data migration, so explicitly gate it.

## Data and Contract Migration Hazards

- **Authority:** specify which path is the system of record at every phase. Dual writes across independently failing stores require conflict, ordering, replay and reconciliation rules; they are not a default migration tactic.
- **Backward and forward compatibility:** state the actual consumer/producers and their supported overlap. An expand/migrate/contract schema approach may require old readers to tolerate the new representation and new readers to understand the old representation during rollout.
- **Rollback boundary:** separate traffic rollback, binary rollback and _data_ rollback. After a destructive transformation, prefer an explicitly designed forward-recovery procedure over promising an impossible revert.
- **Completion evidence:** include old-path traffic and dependency measurements, state reconciliation, contract checks and actual retirement of temporary adapters, flags and copied data. "All tests pass" alone does not show legacy consumers have gone away.

**Failure example:** shifting writes to a new datastore but leaving an old background worker with direct legacy writes creates two authorities. Pause the cutover until the worker is migrated or fenced, then prove that the legacy write path is inactive before retirement.

## Selection Rules

- Do not add an incremental-change pattern merely for architectural fashion. Trace to a justified change and its risks.
- Do not silently add a new durable data owner or transactional dependency during migration.
- Human Gate C applies before breaking contracts, destructive data moves and changes lacking easy rollback.
- Combine patterns when boundaries differ (e.g. Strangler Fig outside, Parallel Change for data, Anti-Corruption Layer for semantics); distinguish their responsibilities.
