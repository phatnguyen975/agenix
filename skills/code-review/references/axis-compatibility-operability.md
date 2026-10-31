# Axis: compatibility-operability

## Purpose

Verify that the change can be released and operated safely: consumers remain compatible or have a migration path, persisted data transitions safely, configuration is valid, and new failure modes are observable and recoverable.

## Method

1. Identify consumers and runtime versions affected: API callers, event/message consumers, stored-data readers/writers, CLI users, operators, and adjacent service versions.
2. Evaluate the transition, not only the final state. Consider rolling deployments, mixed versions, retries, rollback, and partially completed rollout.
3. Walk only the checklist areas touched by the change.
4. Distinguish a design/code defect from missing operational evidence. Record unknowns as Not verifiable or Questions, not assumed successes.

## Checklist

### Compatibility and Contracts

- Do public APIs, schemas, file formats, events/messages, CLI behavior, configuration keys, and documented output remain compatible?
- If breaking behavior is intentional, is it versioned or announced with a deprecation and migration path appropriate to the project?
- Are observable defaults, limits, ordering, error semantics, timing, and side effects treated as part of the contract where consumers rely on them?
- Can old/new application versions, readers, and writers coexist during a rolling deployment?
- Are generated clients, SDKs, downstream consumers, and integration contracts updated as needed?

### Data and Migrations

- Is the migration safe at production-scale volume and contention (lock duration, table rewrite, batching, transaction size, replication lag)?
- Is rollback or forward recovery defined? Is irreversibility explicit and accepted?
- Does the release order preserve correctness at each intermediate stage?
- Do breaking schema changes use an expand/migrate/contract sequence where mixed versions must coexist?
- Are backfills restartable, idempotent, observable, rate-limited, and safe under partial completion?
- Is destructive cleanup separated until all consumers have stopped relying on the old representation?

### Configuration and Release

- Are new settings documented, parsed, validated at startup or deploy time, and given safe defaults?
- Do feature flags have an explicit default, owner, rollout/disable strategy, and removal plan where needed?
- Are infrastructure/deployment changes compatible with existing environments and applied in a safe order?
- Are resource limits, secrets/config sources, and environment-specific behavior explicit without embedding secrets?
- Can the release be rolled back without losing data or leaving incompatible state?

### Observability and Operations

- Are logs sufficient to diagnose new behavior without recording secrets or unnecessary personal data?
- Are metrics, traces, health checks, alerts, and dashboards added or adjusted for new failure modes and saturation points?
- Are error messages actionable for operators and appropriate for end users?
- Are new jobs, schedules, queues, dependencies, runbooks, on-call actions, and recovery procedures documented?
- Can operators detect a stuck migration, growing backlog, partial rollout, or degraded dependency?

## Severity Guidance

- Breaking consumed contract without a safe transition, likely irreversible data loss, or production-blocking migration — Critical or High.
- No viable rollback/recovery, unsafe default, or incompatible deployment sequence — High or Medium by impact.
- Missing observability for a material new failure mode — Medium.
- Missing operational documentation with limited impact — Low or Medium.

## Boundaries

- Security-event auditing, secret exposure, and sensitive log content belong to security.
- Interface shape and architectural ownership belong to design; compatibility over time belongs here.
- Runtime efficiency belongs to performance.
- Functional errors in state transitions belong to correctness.
