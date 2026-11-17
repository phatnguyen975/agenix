# Diagnosis (Phase 3)

A failure can originate in bad data, a missing operation, an invalid assumption, configuration or an interaction between components. Trace the observed divergence backward to candidate causes, then test causality; not every failure is state corruption.

## Backward Tracing

1. Find the immediate cause: the code that directly produces the wrong value or behavior.
2. Ask what called it and where the wrong value came from; inspect each caller's input.
3. Continue upward until the first point where the state is wrong although its inputs were correct. That point is a candidate defect boundary, not proof until a discriminating experiment confirms it.
4. Fix at the defect, never at the symptom.

When tracing by reading is impractical, add instrumentation before the failing operation (not after it fails). Capture only allowlisted fields containing relevant, redacted inputs and environment details plus the needed call context; never dump all environment variables or raw payloads. Use an output channel that stays visible in the run (some runners capture or suppress standard logging).

## Differential Analysis

- Find a working example: another call site, an earlier version, another environment, or a reference implementation.
- Read the complete relevant path, including its dependencies when needed; do not preload unrelated implementation.
- List every difference, however small, and do not assume one cannot matter.
- Test the differences as hypotheses, one at a time.

## Hypotheses

**Format:** "If CAUSE, then OBSERVATION when EXPERIMENT."

- **Falsifiable:** some result must be able to refute it.
- **Distinct:** hypotheses differ in their predictions, not in wording.
- **Ranked:** by likelihood and cost to test; run cheap, likely ones first.
- **Count:** one when evidence is direct; otherwise a small ranked set of plausible explanations. Never invent hypotheses to meet a count.

## Experiments

- Write the prediction before the run.
- Change exactly one variable; use the smallest change or probe.
- Record hypothesis, prediction, experiment, and result (confirmed, refuted, inconclusive) in the investigation log.
- Inconclusive is not confirmation: refine the experiment.
- After one hypothesis set is fully refuted, regenerate a distinct set from the new evidence. If two consecutive sets are fully refuted, stop routine hypothesis generation and ask the human to reassess the assumptions, scope, and missing evidence (G7). Do not continue generating sets indefinitely.

## Confirming a Root Cause

- An experiment's prediction held, and toggling the suspected cause toggles the symptom in the minimal reproduction: introducing the cause reproduces the failure, removing it eliminates it.
- The cause explains every observed symptom; a leftover symptom points to another cause.
- Plausibility is not confirmation.

## Instrumentation Rules

- Order of preference: debugger or REPL, then targeted logs. Log only allowlisted fields needed to test the hypothesis; redact secrets and personal data and never dump the full environment or payload.
- Tag every debug log with a unique prefix (for example `[DEBUG-` plus a short identifier) so one search finds all of them in Phase 6.
- Keep secrets and personal data out of logs.
- Instrumentation must not change behavior; for timing-sensitive failures prefer non-intrusive tools.

## Root Cause Outside the Codebase

When evidence points to a third-party service, infrastructure, or platform:

- Record the external cause in the Root-Cause Statement with the observed evidence; distinguish it from any local defect that has not been proved.
- Work only on the controllable boundary. Add or change handling (for example validation, bounded retries/backoff, clear errors, or observability) when the evidence shows it is appropriate.
- Do not claim to have fixed the external service or platform. Phases 4–7 verify the local handling, not the provider itself.

## Pitfalls

- Anchoring on the first idea; testing only for supporting evidence.
- Blaming the most recent change without verifying it (`bisect`).
- Stacking several changes in one experiment.
- Declaring the cause unknown before isolation and backward tracing are complete. When the cause is still unknown after both, say so and state which evidence is missing.
