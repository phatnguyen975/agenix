# Dependencies, Order and Status

Used in Step 4 of the Create flow and throughout the Sync flow.

## Dependency Rules

- An edge `A → B` exists only when B cannot start, or cannot be verified, until A is `DONE`.
- A preferred order that is not a hard prerequisite does not create an edge.
- Omit edges implied by transitivity: if `A → B` and `B → C` exist, do not add `A → C`.
- No self-dependency. Every referenced ID must exist.
- A part shared by several Slices belongs to the first Slice that needs it. Later Slices depend on that Slice. Do not create a separate foundation Slice.
- Record the reason for each edge in the dependent Slice's `Depends on` field.

## Cycle Check

Mandatory in Step 4 and at every Sync. The method is a topological sort by in-degree (Kahn's algorithm). It runs in time proportional to the number of Slices plus Dependencies.

1. List every Slice as a node and every Dependency as an edge from prerequisite to dependent.
2. Compute each node's in-degree (number of prerequisites).
3. Repeat: remove every node whose in-degree is 0 (one layer), and lower the in-degree of its dependents by one for each removed prerequisite. Stop when an iteration removes no node.
4. If every node was removed, the graph is a DAG.
5. If nodes remain, a cycle exists. The remaining nodes include every node on a cycle, and also nodes that merely depend on a cycle. To find an actual cycle:
   - Repeatedly discard remaining nodes that no other remaining node depends on.
   - Pick any node left. Step to one of its prerequisites among the nodes left. Repeat until a node appears twice. The nodes between the two appearances form a cycle.
6. Resolve the cycle as below, then repeat from step 1.

Resolving a cycle:

1. Test each edge in the cycle against the Dependency Rules. Delete every edge that is not a hard prerequisite.
2. If a cycle remains, merge the Slices in the cycle into one and Split it again with a different technique. The merged Slice inherits every Dependency that enters or leaves the cycle.
3. In the Sync flow, existing Slices are never merged or changed. Resolve the cycle by changing only new Slices and new edges.
4. If it still cannot be resolved, stop and report the Slices involved to the human.

Do not save the plan while a cycle exists.

## Waves and Execution Order

- A Slice's Wave is 1 when it has no Dependencies; otherwise it is 1 plus the highest Wave among its Dependencies.
- This equals the layer in which step 3 of the Cycle Check removes the Slice.
- Slices in one Wave have no dependency path between them and can be carried out in parallel.
- Within a Wave: Risk-first Slices first when that technique applies, otherwise by ID.

**Example:** edges `S01→S02`, `S01→S03`, `S02→S04`, `S03→S04`.

- _Wave 1:_ S01.
- _Wave 2:_ S02, S03.
- _Wave 3:_ S04.

## Dependency Graph Notation

- Diagram type: Mermaid `flowchart TD`.
- One node per Slice: `S01["S01 · Title"]`. Inside labels, replace double quotes with single quotes and remove line breaks and angle brackets.
- Edge `S01 --> S02` means S01 is a prerequisite of S02.
- One class per node matching its status: `ready`, `blocked`, `inProgress`, `done`. Class definitions are in the template.
- Regenerate the graph from the Slice data whenever a Dependency or status changes.

## Status Model

| Status        | Meaning                                                              |
| ------------- | -------------------------------------------------------------------- |
| `BLOCKED`     | At least one Dependency is not `DONE`.                               |
| `READY`       | Every Dependency is `DONE` (or none exist) and work has not started. |
| `IN-PROGRESS` | Work has started.                                                    |
| `DONE`        | Every acceptance criterion is checked and Verification has passed.   |

**Initial status:** a Slice with no Dependencies is `READY`; every other Slice is `BLOCKED`. No Slice starts as `IN-PROGRESS` or `DONE`.

**Transitions:**

| From          | To            | When                                                               | Set by                                         |
| ------------- | ------------- | ------------------------------------------------------------------ | ---------------------------------------------- |
| `BLOCKED`     | `READY`       | The last Dependency becomes `DONE`.                                | Derived (Sync or the person updating the plan) |
| `READY`       | `BLOCKED`     | Sync adds a Dependency that is not `DONE`.                         | Sync                                           |
| `READY`       | `IN-PROGRESS` | Work begins.                                                       | Whoever does the work                          |
| `IN-PROGRESS` | `DONE`        | Every acceptance criterion is checked and Verification has passed. | Whoever does the work                          |
| `IN-PROGRESS` | `READY`       | Work is stopped before completion.                                 | Whoever does the work                          |

No other transition exists. `DONE` is final.

## Invariants

Check these when reading a plan and report any violation.

- A Slice is `BLOCKED` if and only if at least one Dependency is not `DONE`.
- An `IN-PROGRESS` or `DONE` Slice has every Dependency `DONE`.
- A `DONE` Slice has every acceptance criterion checked.
- The Progress counts equal the number of Slices per status and per Granularity.
- The Dependency Graph edges equal the `Depends on` data, and each node's class equals its status.
- Execution Order equals the Waves computed from the Dependencies.

## Sync Rules

- Derived data (`BLOCKED`, `READY`, Progress, Dependency Graph, Execution Order) is recomputed. `IN-PROGRESS` and `DONE` are never set by Sync.
- Scope additions only append: new Slices take the next IDs, new References take the next `R` IDs, and each Split adds a Slicing Log row with its date.
- Existing Slices keep ID, content, acceptance criteria and Dependencies.
- In the Work Item section, only the parts the added scope requires change (Outcome, Boundary, References). All other text stays as written.
- New Slices may depend on existing Slices.
- A new Slice may become a prerequisite of an existing Slice only if the existing Slice is `READY` or `BLOCKED`. A `READY` Slice that gains an unfinished Dependency becomes `BLOCKED`.
- A defect found after `DONE` is recorded as a new Slice.
