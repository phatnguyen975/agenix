# State Transition Modeling

Use when a change creates or alters a persisted lifecycle, or when transition validity governs an operation. When useful, show the rules in a transition table. If a diagram is also included, keep it consistent with the rules.

## 1. Define States from Evidence

1. Identify the state field/path and source requirements.
2. List only supported states. Identify initial and terminal states and how records enter an initial state.
3. Classify each relevant event as a state transition, same-state action, or out of scope.
4. For an existing lifecycle, model only what this feature defines; do not redesign unrelated transitions.
5. Clarify any unknown state, guard, actor, owner, or terminal policy that affects correctness.

## 2. Current-State Representation

- Identify where state is owned and how it is represented. Keep independent state dimensions distinct.
- Define allowed values and enforcement, and link the proposed change if the representation or rule changes.
- If state is derived, explain the derivation and do not invent a persisted status field.
- Define behavior for missing, null, legacy, and future values.

## 3. Transition Table

For each transition, specify:

- From/to states and triggering event or operation.
- Guard/precondition and actor/role where specified.
- Fields written, cleared, required, and related side effects.
- Supporting requirement IDs or source locations.

Also define invalid-transition behavior, enforcement point, concurrency control, conflict/retry behavior, and history/audit choice. Use append-only history when traceability requires it; otherwise explain why current state or last-changed metadata is sufficient.

Do not assume a concurrency feature or transaction the selected store does not support.

## 4. Sanity Checks

- Initial states are sourced and reachable through creation/import.
- Intended non-terminal states have a defined path or documented waiting/timeout policy.
- Terminal states are truly final; reopening requires an explicit transition.
- Every relevant event is modeled or marked as not changing state.
- Guards, actors, data effects, enforcement, and concurrency are defined.
- State values match the constraint/validator, including legacy/future-value policy.
- If both are included, the diagram and table describe the same states and transitions.
- State-changing operations describe their transaction boundary, conflict behavior, and effects.

These checks are diagnostic, not permission to invent missing transitions. Ask or flag the gap.

## 5. Mermaid

When a diagram helps and the output supports Mermaid, use `stateDiagram-v2` in a fenced `mermaid` block. Use stable state identifiers and readable labels. Separate independent lifecycles. Verify rendered output when a renderer is available.

**Reference:** [Mermaid State Diagrams](https://mermaid.js.org/syntax/stateDiagram.html).
