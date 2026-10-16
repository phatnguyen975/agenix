# Fitness Functions — Full Guidance

Read this file when an ADR's decision seems to warrant automated verification and the concrete checks need to be worked out. SKILL.md's domain table is enough to decide whether a fitness function is worth adding at all.

## Definition

A fitness function is any mechanism that provides an **objective integrity assessment of an architectural characteristic**. Two things follow directly from that:

- The characteristic being protected must be named — not "performance" in the abstract, but the specific property this decision is meant to protect.
- The assessment must be objective: a measurable check, not a subjective judgment call. "This doesn't look maintainable" is not a fitness function; "no module in the domain layer imports from the infrastructure layer" is.

Making that assessment objective and automatable in practice requires a third element: a concrete threshold that decides pass or fail. Operationally, each fitness function has three parts:

1. **Protected characteristic** — the property being safeguarded.
2. **Automated guard** — the mechanism that checks it.
3. **Failure threshold** — the exact condition that fails the check.

## Trigger / Cadence

Fitness functions can also be classified by when they run: **triggered** (run on demand, e.g. a CI job on every pull request) vs. **continual** (run constantly, e.g. production monitoring and alerting). This matters because it determines how the guard gets implemented — a triggered check is typically a test or a CI step; a continual check is typically a dashboard, alert rule, or health check. State the trigger/cadence explicitly whenever it isn't obvious from the guard description itself.

## When to Add One

Not every ADR needs a fitness function. Add one only when the decision's outcome can and should be verified automatically — i.e., there's a real property at stake that could silently regress without a check in place. If no domain below applies, mark the section "N/A" rather than inventing a check for the sake of completeness.

## Common Domains

| Domain                       | Protected characteristic (example)          | Automated guard (example)                   |
| ---------------------------- | ------------------------------------------- | ------------------------------------------- |
| Performance                  | Latency/throughput budget                   | CI benchmark, load test                     |
| Security                     | No known vulnerable dependencies            | Dependency/CVE scan in CI                   |
| Scalability & Reliability    | Survives N replicas / node failure          | Load test, chaos/failover test              |
| Maintainability              | Module coupling boundary, coverage floor    | Architecture test, lint rule, coverage gate |
| Observability                | Key metrics/alerts exist for this component | Dashboard/alert existence check             |
| Compliance / Data governance | Data classification & retention applied     | Policy-as-code check                        |
| Cost                         | Infra spend within budget                   | Cost-estimation check in CI/CD              |

A given ADR picks only the domain(s) it actually affects — most ADRs touch one or two, not all seven. The specific guard and threshold for a given ADR are always decided at write time, based on what the decision is actually protecting — this table is a starting point for the conversation, not a fixed menu.
