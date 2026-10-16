# Architectural Significance — Full Criteria

Read this file when the significance of a decision is genuinely unclear, or when asked to justify why a decision does or doesn't warrant an ADR. SKILL.md's "When to Use" section is enough for the common case.

## Formal Definition

An ADR documents an **architecturally significant** decision — a decision that affects at least one of:

| Category                       | What it covers                                                                              | Example                                                                                      |
| ------------------------------ | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Structure                      | Architecture style, code-organization pattern, how the system is decomposed into components | Monolith vs. microservices; sync vs. event-driven service communication                      |
| Non-functional characteristics | Quality attributes: performance, security, scalability, reliability, cost                   | Choosing a caching strategy to meet a latency target                                         |
| Dependencies                   | Coupling between components, or reliance on an external system, library, or vendor          | Relational vs. NoSQL database; adopting a third-party auth provider                          |
| Interfaces                     | Contracts between components or systems, including published/external APIs                  | Public API versioning strategy; authentication/authorization contract shared across services |
| Construction techniques        | Implementation approach, platform, or framework used to build the system                    | Adopting a new build/deployment platform                                                     |

This definition is independent of project phase. A decision that touches one or more of these categories qualifies regardless of whether it happens during initial design, mid-sprint, in code review, after an incident, during a refactor, or retroactively (documenting a past decision that was never written down).

## Secondary Heuristics

Not every decision that touches a category above is worth the overhead of an ADR. These heuristics help filter for the ones that are:

- Hard or costly to reverse
- Several reasonable options existed — a real trade-off, not an obvious call
- Unconventional — deviates from the project's established pattern
- Long-lasting or wide-reaching consequences
- Took real time or debate to settle
- Likely to be questioned again later

A decision meeting the formal definition AND at least one heuristic is a strong candidate. A decision meeting the formal definition but none of the heuristics (e.g. a structural choice with an obvious, cheap, easily-reversed answer) usually isn't worth documenting.

## Worked Examples

| Decision                                                                                      | Category                               | Why it qualifies                                                                       |
| --------------------------------------------------------------------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------------- |
| Architecture style (monolith vs. microservices, layered vs. hexagonal, sync vs. event-driven) | Structure                              | Reshapes the system's whole structure; reversing it means rewriting, not refactoring   |
| Database paradigm (relational vs. NoSQL, SQL vs. document vs. graph)                          | Structure & Dependencies               | Migrating a data model later is expensive and risky                                    |
| Authentication/authorization architecture (session vs. token, RBAC vs. ABAC, SSO provider)    | Interfaces & Non-functional (security) | Security-critical and cross-cutting; changing it later touches every integration point |
| Component extraction (pulling a service out of a monolith, defining a bounded context)        | Structure                              | Affects team ownership, deployment topology, and API contracts going forward           |
| Major trade-off (consistency vs. availability, latency vs. throughput, build vs. buy)         | Non-functional characteristics         | A foundational trade-off that ripples through every downstream decision                |
