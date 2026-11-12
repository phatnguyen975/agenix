# Tactical Design

Use to model meaningful **business decisions, identities, behaviors, and rules within a bounded context**. Start from scenarios and domain language; do not start by designing class hierarchies. Tactical building blocks are conceptual modeling tools, not obligations to implement objects, events, or services.

## Core Building Blocks

| Element            | Domain Meaning                                                                  | Distinguishing Question                                                      |
| ------------------ | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Entity**         | Concept with identity that remains meaningful as attributes change              | Must the business distinguish this instance from another with equal values?  |
| **Value Object**   | Descriptive concept distinguished by its relevant values                        | Would replacing it with an equal value preserve its business meaning?        |
| **Aggregate**      | Boundary for behavior and invariants that require consistent change             | What state and rules must be controlled atomically?                          |
| **Domain Service** | Cohesive domain operation not naturally belonging to one entity or value object | Does it implement a business decision rather than coordinate technical work? |
| **Domain Event**   | Business-significant fact that has occurred                                     | Is the occurrence meaningful in the context's business language?             |
| **Policy**         | Conditional business reaction                                                   | When a condition/occurrence is recognized, what action follows and why?      |

**Command** denotes business intent; **query** denotes a request for information; **result/refusal** describes the outcome. These are useful descriptions even if the eventual implementation does not use command classes or event buses.

## Entity or Value Object

1. **Identity:** Does the business care which _particular instance_ it is over time, even if its attributes equal another's? If so, model an Entity.
2. **Equality:** If all business-relevant values are equal, are the concepts interchangeable? If yes, a Value Object is a good candidate.
3. **Lifecycle:** Does the concept have independently tracked transitions or decisions? That favors an Entity. Do not invent technical IDs to justify entity status.
4. **Validation:** A Value Object can encapsulate rules such as valid ranges or unit consistency. Prefer conceptual immutability — treat a change as a new value rather than a mutation of the same identity.
5. **Context:** Classify separately inside each bounded context; one real-world thing can be modeled differently elsewhere.

**Example:** `DeliveryAddress` recorded on an order is often a Value Object. A registered `Facility` inspected and managed over time is an Entity. An address string is not inherently either; identity and responsibility determine the model.

## Business Rules, Decisions, and Invariants

Write every material rule in business language with its condition, constraints, exceptions, and authoritative source. Confirm missing or conflicting business outcomes with the responsible human **before** presenting them as rules in a final model. Identify the **authority** for the decision; one business process may involve several steps without creating several contradictory owners.

| Rule Kind                   | Modeling Responsibility                                         | Illustration                                            |
| --------------------------- | --------------------------------------------------------------- | ------------------------------------------------------- |
| **Invariant**               | State consistency enforced by an appropriate aggregate boundary | Confirmed order total equals the sum of confirmed lines |
| **Eligibility / Decision**  | Entity, value object, or domain service owning the rule         | Application may be approved only when eligible          |
| **Process / Reaction Rule** | Policy or explicitly responsible human process                  | After approval, notify the applicant if required        |
| **External Constraint**     | Outside authority plus the receiving context's response         | An external payer may refuse an authorization           |

**Invariant** means a condition required to hold at an aggregate's defined consistency boundary after each successful state-changing operation. A precondition or eligibility check is not always an invariant; a global requirement spanning aggregates is not automatically enforceable locally. See `aggregate-design.md`.

**Example distinction:** "An application needs a valid license to be approved" may be an approval precondition. "Every approved application references an accepted license record" may become an aggregate invariant **if** the owning model can actually guarantee it. Neither should be stated without business evidence.

## Intentions, Occurrences, and Reactions

- **Command / action:** `ApproveApplication` requests a decision. Record the responsible domain concept or context, necessary facts, refusal conditions, and observable outcomes. A command can fail without producing a domain event.
- **Domain event:** `ApplicationApproved` asserts that approval occurred. Record it when this occurrence matters in the model. It is not automatically an event message sent to other contexts.
- **Query / information:** `CheckEligibility` seeks relevant facts or a decision result. A query does not intend to change business state, and it is not automatically a domain service.
- **Policy:** `When ApplicationApproved, if notification is required, notify applicant` expresses a conditional response. A policy may be manual or delayed; it need not always create another command or event.
- **Cross-context message:** Name the business meaning communicated across boundaries and any translation; do not expose an internal event or model wholesale by default. Consult `context-mapping.md`.

**Illustrative trace:**

```text
Intent: Approve Application
Decision Owner: Application
Precondition: Application is eligible [hypothesis until confirmed]
Accepted Outcome: Application approved
Domain Event: ApplicationApproved [only if meaningful]
Refusal: Not eligible [not necessarily a domain event]
Reaction: If notification is required, inform applicant
```

This trace is a working illustration, not an approved requirement. Ask the human to establish material preconditions and refusal behavior before a final design; never carry the bracketed hypothesis into a delivered model.

## Decide Where Behavior Belongs

1. Put behavior that depends on **an entity's own identity, lifecycle, or rules** with that entity or its owning aggregate.
2. Put calculations and validation intrinsic to **a value concept** with the Value Object.
3. Use a **Domain Service** when a real business operation spans concepts and cannot naturally belong to one entity or value object. State its inputs, domain decision, and authority.
4. Model **policies** when behavior is a reaction or process across decisions/contexts; do not hide business policy inside infrastructure or workflow plumbing.
5. Keep **application-level orchestration** (fetching data, calling systems, scheduling, handling transports) outside the domain model. The business process may still be documented in domain terms.

**Domain Service example:** `PremiumCalculation` might apply an organization's rating policy to a risk profile and return a premium. It does not have to change an aggregate, and it should not be created solely because inputs come from multiple entities. If a `Policy` aggregate naturally owns the calculation, place the behavior there instead.

## Select Tactical Depth

| Situation                                               | Model When Useful                                                                                      |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Complex decisions or hard consistency requirements      | Entities/Value Objects, aggregates, invariants, commands, refusals                                     |
| Multi-step or cross-context business journeys           | Events/meaningful outcomes, information needs, policies, collaborators, timing                         |
| State-dependent business restrictions                   | Lifecycle states, allowed/refused transitions                                                          |
| Simple reference data or externally supplied capability | Context purpose, terms, important rules, integration meaning; omit speculative aggregates and services |

Strategic type (`Core`, `Supporting`, `Generic`) helps prioritize **investment**, but does not determine an obligatory tactical checklist. A supporting capability can own a strict invariant; a core capability may not need a lifecycle diagram.

## Tactical Review Checks

- Is every material published rule grounded in confirmed business evidence and assigned an appropriate authority?
- Do entity identity and value equality follow actual business needs, not an ORM or database structure?
- Does the proposed aggregate protect a real consistency rule? If uncertain, consult `aggregate-design.md`.
- Are preconditions, invariants, process reactions, and external constraints distinguishable?
- Are commands intents, events established facts, and refusals outcomes unless the business explicitly treats them as facts?
- Are domain services business decisions, not technical orchestrators or generic helper objects?
- Are optional tactical elements omitted when they would add no domain understanding?
