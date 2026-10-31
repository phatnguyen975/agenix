# Axis: correctness

## Purpose

Verify that the changed code produces the intended behavior, preserves invariants, and handles boundary conditions, failures, and concurrency correctly.

## Method

1. Establish intended behavior from applicable specs, public contracts, caller expectations, and surrounding code. Do not treat the implementation itself as proof of intent.
2. For each changed function, state transition, or data flow, trace the normal path and each relevant failure path.
3. Exercise input boundaries: absent, null, empty, minimum, maximum, just inside/outside limits, duplicates, malformed encodings, unexpected but representable types, and invalid state.
4. Inspect callers/callees when signatures, return values, ordering, side effects, exceptions, or timing semantics change.
5. For asynchronous or concurrent code, reason about interleavings, cancellation, duplicate completion, timeout, partial completion, and ordering explicitly.
6. For refactors, compare observable behavior: result, state, side effects, ordering, exceptions, and externally relied-upon timing/ordering contracts.
7. For bug fixes, verify the root cause is addressed and inspect analogous paths for the same defect.

## Checklist

### Logic and Data

- Do branches, loops, recursion, state machines, and termination conditions behave correctly, including off-by-one and unreachable-state cases?
- Are arithmetic, overflow, rounding, precision, units, integer conversions, and division-by-zero handled safely?
- Are time zones, daylight-saving transitions, calendar boundaries, locale, Unicode, and encoding handled correctly where relevant?
- Are absent/null values, empty collections, duplicates, and malformed-but-parseable values handled intentionally?
- Does correctness depend on unspecified ordering, iteration order, concurrent completion order, or unstable identifiers?
- Are parsing, serialization, normalization, and round trips lossless enough for the contract?

### Errors and External Systems

- Are errors propagated or translated intentionally rather than swallowed or replaced with success-like defaults?
- Do fallbacks preserve a valid invariant, or do they conceal a failure or invalid state?
- Are external calls bounded by timeouts/cancellation, and are partial failures handled?
- Are retries bounded, appropriately backed off, and limited to operations that are idempotent or made safe to repeat?
- Are return values, status codes, and error variants checked rather than assumed?

### State and Resources

- Are invariants maintained across transitions and failures midway through an operation?
- Are files, streams, transactions, locks, connections, handles, subscriptions, and temporary resources released on every path?
- Are multi-step writes atomic or recoverable through transactions, idempotency, checkpoints, or compensation?
- Can a cancelled or timed-out operation leave stale state or continue an unintended side effect?

### Concurrency and Asynchronous Flow

- Is shared mutable state protected using the correct synchronization model?
- Are check-then-act operations atomic where an invariant depends on them?
- Can work run twice, out of order, after cancellation, or never complete?
- Are lock acquisition and release paths balanced, with a consistent lock order?
- Can shared state or coordination be removed by redesigning the flow?

## Severity Guidance

- Wrong result, unauthorized state transition, data loss/corruption, or core operation failure in normal use — Critical or High.
- Race condition/deadlock with a realistic trigger — High or Critical by impact and likelihood.
- Edge-case failure — Medium; High when data, permissions, or irreversible actions are at risk.
- Contained unhandled error — Medium or Low according to user impact.

## Boundaries

- Deviation from an explicit requirement belongs to spec-compliance; record the requirement status there.
- Test adequacy belongs to testing.
- Security validation of untrusted input, authorization, and exploit paths belongs to security; ordinary input-domain behavior belongs here.
- Runtime cost belongs to performance.
