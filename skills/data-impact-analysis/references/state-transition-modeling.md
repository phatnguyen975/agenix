# State Transition Modeling

Applies to persisted entities whose state is created/changed by the feature or whose transition validity governs an operation. The transition table is canonical; the Mermaid diagram must match it.

## 1. Define States from Evidence

1. Identify the state field/path and source requirements.
2. List only supported states. Identify initial and terminal states and how records enter an initial state.
3. Classify each relevant event as a state transition, same-state action, or out of scope.
4. For an existing lifecycle, model only what this feature defines; do not redesign unrelated transitions.
5. Ask at Gate 0 when an unknown state, guard, actor, owner, or terminal policy affects correctness.

## 2. Current-State Representation

- Use one canonical state field/path, not overlapping booleans.
- Define allowed values and enforcement in Section 7; reference the DMC if the field/rule changes.
- If state is derived, explain the derivation and do not invent a persisted status field.
- Define behavior for missing, null, legacy, and future values.

## 3. Transition Table

For each transition, specify:

- From/to states and event/operation (`OP-xx`).
- Guard/precondition and actor/role where specified.
- Fields written, cleared, required, and related side effects.
- Supporting source IDs.

Also define invalid-transition behavior, enforcement point, concurrency control, conflict/retry behavior, and history/audit choice. Use append-only history when traceability requires it; otherwise explain why current state or last-changed metadata is sufficient.

Do not assume a concurrency feature or transaction the selected store does not support.

## 4. Sanity Checks

- Initial states are sourced and reachable through creation/import.
- Intended non-terminal states have a defined path or documented waiting/timeout policy.
- Terminal states are truly final; reopening requires an explicit transition.
- Every relevant event is modeled or marked as not changing state.
- Guards, actors, data effects, enforcement, and concurrency are defined.
- State values match the constraint/validator, including legacy/future-value policy.
- Diagram and table contain the same supported states/transitions.
- State-changing operations describe transaction and conflict behavior in Section 4.

These checks are diagnostic, not permission to invent missing transitions. Ask or flag the gap.

## 5. Mermaid

Use `stateDiagram-v2` in a fenced `mermaid` block. Use stable state identifiers and readable labels. Split independent lifecycles into separate diagrams. Validate syntax with a renderer when available.

**Reference:** [Mermaid State Diagrams](https://mermaid.js.org/syntax/stateDiagram.html).
