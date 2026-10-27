# Hardening

**Purpose:** make the same class of bug harder to reintroduce or quicker to detect. Hardening is a separate change with its own verification, applied only after the human approves it; it is never part of the fix (G5).

## Process

1. Take the path the bad value or state followed from origin to failure (from Phase 3).
2. List the checkpoints on that path.
3. Choose the layers where a check is cheap and meaningful:
   - **Entry validation:** reject invalid input at the boundary where it enters the system.
   - **Business-logic validation:** assert invariants where the data is used.
   - **Environment safeguards:** refuse dangerous operations in contexts where they must not happen (for example, a test touching a real resource).
   - **Diagnostic instrumentation:** capture inputs, state, and call stack at the point of failure so a future failure is quicker to diagnose.
4. Add one layer at a time. In isolated tests, verify each layer can catch the case when upstream layers are bypassed as needed. Never bypass production safeguards or use real destructive resources to test a layer.
5. Repeat the Phase 7 verification and update the evidence table and the report.

## Limits

- Not every bug needs every layer; weigh the cost in noise, duplication, and performance.
- Prefer designs in which invalid states cannot be represented (types, constructors) when the language and project support it.
- Error messages state what was received, what was expected, and where.

## Observability additions

- Structured errors with context.
- Metrics or alerts for the failure signature.
- Tests for every added check.
