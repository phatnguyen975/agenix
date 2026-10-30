# State Transition Modeling

Applies to any persisted entity with a state or lifecycle, in any datastore. The transition table is the canonical specification; the Mermaid state diagram is a required visual summary that must match it exactly.

## 1. Define the lifecycle from evidence

1. Identify the state field/path and its source requirements. Preserve exact state values and event names where they exist.
2. List the defined states as a closed set only when the inputs establish that set. Identify the initial state(s), terminal state(s), and how a record is created/imported into an initial state.
3. List each specified event/operation and determine whether it changes state, performs a same-state action, or is out of scope. Do not infer an unmentioned transition.
4. For an existing state field, model only states/transitions the feature inputs define. Explicitly note that undocumented existing transitions are not changed by this feature. Do not redesign a prior lifecycle solely to make the graph look complete.
5. If a required state value, transition, guard, actor, ownership, or terminal-state policy is unknown and changes correctness, ask at Gate 0.

## 2. Use one canonical current-state representation

- Store current lifecycle state in one canonical field/path rather than overlapping booleans.
- Specify exact allowed values and validation/enforcement: database/store constraint or validator, application, or both. Link any structural DMC; list allowed values canonically only in Section 7.
- If state is derived from other facts rather than persisted, explain that and do not invent a status column.
- Treat missing state, null state, unknown future values, and legacy values explicitly. Do not decide their meaning implicitly.

## 3. Transition table requirements

Every modeled transition has:

- **From / To:** exact state values, including same-state behavior if meaningful.
- **Event / operation:** source event or `OP-xx`.
- **Guard / precondition:** facts that must be true for the transition to proceed.
- **Data effects:** fields written, cleared, or required; related entity changes; emitted event/outbox/history data.
- **Actor:** user/role/service/process allowed to initiate it, where specified.
- **Source IDs:** evidence supporting the transition and its conditions.

Also state:

- invalid-transition behavior (reject, return an error/result, no unintended data change, compensation if a prior external effect already occurred);
- enforcement point and any limits of application-only checks;
- concurrency control suitable for the actual datastore (atomic conditional write, version compare-and-swap, lock/transaction, or another documented approach);
- conflict and bounded-retry behavior for simultaneous transitions;
- history/audit choice: append-only transition history when traceability requirements need it; otherwise document why current state/last-changed metadata is enough.

Do not prescribe a particular concurrency mechanism if the store's capabilities are unknown. Ask or record the unknown instead of promising atomicity.

## 4. Sanity checks

Evaluate these checks and explain any exception instead of silently forcing a graph change:

- Can the initial state be identified from the requirements and creation/import flow?
- Is every intended reachable state reachable from an initial state, or is an external seed/recovery path documented?
- Does each non-terminal state have an intended outgoing path, or is it intentionally waiting/paused with an explicit event or timeout policy?
- Are terminal states truly final under the feature's business semantics? If reopening is allowed, the state is not terminal for that lifecycle or the reopen transition must be explicit.
- Is every event in the requirements represented by a transition or explicitly marked as not changing state?
- Are guards, actor permissions, and data effects defined for every transition?
- Does the state-value constraint/validator equal the modeled state set, with a documented policy for legacy/future values?
- Does the Mermaid diagram contain exactly the supported states and transitions represented in the table? It must not imply an unlisted transition.
- Does Data Flow for each state-changing OP describe the concurrency mechanism, transaction boundary, and invalid/conflict behavior?

The reachability and outgoing-transition checks are diagnostic heuristics, not permission to invent business behavior. If a graph appears incomplete but the source does not specify the missing edge, ask at Gate 0 or flag the gap.

## 5. Mermaid

Use Mermaid `stateDiagram-v2` in a fenced `mermaid` block. Use stable identifier tokens for states and readable labels where needed. Keep the diagram small enough to review; split independent lifecycles into separate subsections/diagrams. Mermaid syntax must be checked where a renderer is available, but validator success alone does not prove the diagram renders or agrees with the table.

Official syntax: [Mermaid state diagrams](https://mermaid.js.org/syntax/stateDiagram.html).
