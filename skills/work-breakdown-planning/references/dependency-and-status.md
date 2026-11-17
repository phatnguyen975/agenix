# Dependencies, Order and Status

Read when constructing/updating dependencies or standalone statuses. Graph rules apply across output formats. The four-state model, Sxx notation and derived tables below belong to the standalone [Slice Plan Template](../assets/slice-plan-template.md); a caller-owned format uses its own lifecycle/completion resolver. Status text is not execution evidence.

## Dependency Rules

- An edge `A → B` exists only when B cannot start, or cannot be verified, until A meets the owning prerequisite-completion rule (`DONE` in the standalone model).
- A preferred order that is not a hard prerequisite does not create an edge.
- Prefer omitting edges implied by transitivity unless the direct edge captures a distinct contract obligation: for example, `A → B` and `B → C` already enforce A before C.
- No self-dependency. Every referenced ID must exist.
- Give shared work one owner: usually the first Slice that needs it. A separate prerequisite is valid when it has an independently verifiable contract; later Slices depend on that contract, not on mere shared file ownership.
- Record the reason for each edge in the dependent Slice's `Depends on` field.

## Cycle Check

Mandatory in Step 4 and at every Sync. The method is a topological sort by in-degree (Kahn's algorithm). With adjacency lists and in-degree tracking its traversal is `O(V+E)`. Sorting for deterministic display may add overhead.

1. List every Slice as a node and every Dependency as an edge from prerequisite to dependent.
2. Compute each node's in-degree (number of prerequisites).
3. Repeat: remove every node whose in-degree is 0 (one layer), and lower the in-degree of its dependents by one for each removed prerequisite. Stop when an iteration removes no node.
4. If every node was removed, the graph is a DAG.
5. If nodes remain, a cycle exists. The remaining nodes include every node on a cycle, and also nodes that merely depend on a cycle. To find an actual cycle:
   - Repeatedly discard remaining nodes that no other remaining node depends on.
   - Pick any node left. Step to one of its prerequisites among the nodes left. Repeat until a node appears twice. The nodes between the two appearances form a cycle.
6. Resolve the cycle as below, then repeat from step 1.

Resolving a cycle:

1. Test each edge against the Dependency Rules. Correct unsupported edges in the proposed work. Existing approved edges require an explicit amendment decision.
2. For new, unapproved work, if a cycle remains, merge the Slices in the cycle into one and Split it again with a different technique. The merged Slice inherits every Dependency that enters or leaves the cycle.
3. In the Sync flow, existing Slices are never merged or changed. Resolve the cycle by changing only new Slices and new edges.
4. If it still cannot be resolved, stop and report the Slices involved to the human.

Do not save the plan while a cycle exists.

## Waves and Execution Order

- A Slice's Wave is 1 when it has no Dependencies; otherwise it is 1 plus the highest Wave among its Dependencies.
- This equals the layer in which step 3 of the Cycle Check removes the Slice.
- Slices in one Wave have no dependency path between them and are candidates for parallel execution. Check shared files/resources, ownership and external prerequisites before scheduling; graph independence alone does not grant concurrency.
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

**Initial status for new work:** `READY` when every prerequisite is already `DONE` (or none exist), otherwise `BLOCKED`. Preserve existing completion evidence; planning does not set `IN-PROGRESS` or `DONE`.

**Transitions:**

| From          | To            | When                                                               | Set by                                         |
| ------------- | ------------- | ------------------------------------------------------------------ | ---------------------------------------------- |
| `BLOCKED`     | `READY`       | The last Dependency becomes `DONE`.                                | Derived (Sync or the person updating the plan) |
| `READY`       | `BLOCKED`     | An explicitly authorized correction makes a prerequisite unmet.    | Owner of the authorized correction             |
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
- A newly discovered prerequisite of an existing Slice requires an explicit amendment decision, not ordinary Sync. Preserve the definition and report affected readiness until its owner resolves the correction.
- A defect found after `DONE` is recorded as a new Slice.

## Evidence and Limits

Sync reconciles recorded facts; it does not run product verification, certify completion or grant delivery authority. If a completed item's evidence is stale or contradicted, report the conflict and block dependent readiness under the owning rules. Retain history and obtain a disposition rather than silently trusting `DONE` or rewriting it. External prerequisites and resource availability must be recorded alongside the graph; `READY` in this standalone model describes dependency readiness only.
