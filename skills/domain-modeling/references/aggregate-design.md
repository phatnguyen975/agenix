# Aggregate Design

Use when domain behavior needs an explicit **identity and consistency boundary**, especially where invariants, concurrency, or lifecycles matter. An Aggregate is a cluster of domain objects treated as one unit for consistent change, **not** a bounded context, database table, UI screen, or deployed service.

## Aggregate Fundamentals

- An Aggregate has **one Aggregate Root**, an Entity through which external domain operations govern state changes within that boundary. The Aggregate can consist of only its root.
- Internal Entities and Value Objects belong within the root's consistency responsibility. Their presence is justified by domain behavior and invariants, not merely object navigation.
- A **hard invariant** must remain true after each successful state-changing operation in the boundary. Distinguish it from policies that can be completed later.
- Prefer **small, cohesive aggregates**. Larger aggregates increase coupling and may cause unnecessary contention; splitting too far can make a true invariant unenforceable.
- Prefer references to **other aggregates by identity** rather than embedding their independently mutable entities as part of the same object graph.
- Changing **one aggregate instance per atomic transaction** is a strong default guideline, not a rule to impose on every business operation. Exceptions require an explicit consistency and failure rationale.

## Discover the Boundary

1. Extract candidate entities, their identities, and **commands that change business state** from actual scenarios.
2. List required invariants and the exact state each one reads or changes. Separate **hard atomic guarantees** from acceptable delays, policies, and eventually achieved outcomes.
3. Identify the business authority for changing each piece of state. Start with the smallest candidate root that can enforce its invariants.
4. Include child Entities or Value Objects whose state is controlled under the same invariant or lifecycle. Keep independently owned state in another aggregate.
5. For each command, specify permitted outcomes, refusal conditions, and which invariants must be maintained.
6. Exercise concurrency, stale information, cancellation, and partial failure. Reconsider boundary and process ownership if the model cannot uphold its own guarantee.

Record the root and identity, consistency responsibility, internal concepts, invariant sources, references to other aggregates, and lifecycle if it materially constrains behavior. Describe actions, decisions, and outcomes at the bounded-context **Business Behavior** level and link relevant Aggregate invariants to those entries; do not duplicate full action catalogs for each Aggregate.

## Local and Cross-Aggregate Consistency

| Requirement                                    | Important Modeling Decision                                                    |
| ---------------------------------------------- | ------------------------------------------------------------------------------ |
| One root controls all relevant state           | Which invariant must be true atomically?                                       |
| Several independent aggregates participate     | Can a delayed business reaction achieve the goal, or is coordination required? |
| Globally limited resource or unique allocation | Who has the authority to reserve, allocate, or serialize the scarce resource?  |
| Mutable fact belongs to another context        | What freshness, authority, and failure trade-offs does the business accept?    |

**Never claim a global invariant is enforced by "check, then update" alone** when concurrent actions can race. A query is evidence used for a decision, not a transaction guarantee. Do not silently weaken an explicit must-never-break rule into eventual consistency.

**Illustrative local invariant:** If the order total must always equal the sum of its committed line amounts, an `Order` Aggregate can own those lines and enforce that equality on every accepted change.

**Illustrative cross-aggregate invariant:** If no customer may exceed an agreed credit exposure even with concurrent orders, querying current credit before each order is insufficient. Explore **a single authoritative credit-reservation decision** or another justified coordination boundary. The model must explain the business effects of release, cancellation, and refusal; actual technical concurrency mechanisms are outside this skill.

If the business explicitly tolerates temporary divergence, establish what must eventually converge, who owns the response, acceptable timing, and what happens when reconciliation fails. Ask the appropriate human when any material guarantee or exception is unknown; treat it as a working blocker, never a fictional guarantee in the final model.

## References, Ownership, and Coordination

- **Within an aggregate:** Members are governed by the root's rules. Internal objects do not independently break root invariants.
- **Between aggregates:** Reference identities and describe permitted collaborations; do not assume an operation can atomically update all participants.
- **Between bounded contexts:** Each context owns its model and terms. Integration facts, translations, and business-level timing requirements must be explicit; consult `context-mapping.md`.
- **Across a business process:** A policy or process may coordinate multiple distinct decisions. Avoid labeling this coordinator an Aggregate solely because it initiates several actions.

**Warning signs:** An Aggregate that copies an entire object graph, a root that owns unrelated business capabilities, or a Domain Service that mutates several roots to hide an unspecified transaction boundary.

## Lifecycle and State-Dependent Rules

Model states only when they restrict business behavior:

1. Define **business states** and the rules that distinguish them. Avoid technical lifecycle states unless they are business-relevant.
2. Identify allowed commands/transitions, preconditions, refusals, and terminal states where they exist.
3. Distinguish **stored business state** from a derived condition such as `Overdue`, which may follow from time without a dedicated transition.
4. Confirm who or what triggers a change, especially for deadlines and external observations.
5. Check that every transition preserves invariants and that invalid transitions are refused.

**Example:** A `Reservation` might move `Requested → Confirmed → Completed`, with `Canceled` reachable earlier. Whether confirmation after cancellation is refused or a canceled reservation can be reopened requires source-backed rules; the diagram alone cannot establish them.

## Analyze Concurrency and Failure

For a claimed guarantee, test at least the relevant cases:

- **Competing commands:** Two concurrent requests that individually pass an availability check; can they jointly violate capacity or limit?
- **Repeated command/event:** Could repetition grant the same business resource twice, and what business identity makes the outcome unique?
- **Reordered information:** What if an older external fact arrives after a newer one?
- **Stale reads:** Who owns the definitive decision when information has changed since it was observed?
- **Incomplete process:** What does the business do if one context completes while another refuses or becomes unavailable?
- **Changed rules:** What happens to existing aggregates when eligibility or limits change?

These checks challenge the business model; they do **not** prescribe persistence or messaging technology. Resolve material consistency and failure trade-offs with the relevant human before publishing a final invariant or guarantee.

## Aggregate Quality Checks

- Does the root represent a domain concept and control a coherent consistency boundary?
- Is every claimed invariant linked to a requirement and a violating scenario?
- Can the boundary uphold the requirement under concurrency and partial failures?
- Are child objects part of the root's invariants rather than attached for data convenience?
- Are independently owned aggregates referenced by identity where practical?
- Are lifecycles documented only when states genuinely constrain decisions?
- Are eventual outcomes, hard guarantees, and external constraints explicitly distinguished?
- Are material concurrency, cancellation, and failure semantics confirmed before accepting the aggregate design?
