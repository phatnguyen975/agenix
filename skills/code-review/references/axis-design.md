# Axis: design

## Purpose

Verify that the change fits the system: responsibilities are cohesive, boundaries and dependency directions are sound, interfaces are appropriate, and the abstraction reduces rather than relocates complexity.

## Method

1. Understand the module/service around the change, its dependents, its dependencies, and the architectural constraints that apply.
2. Evaluate the overall shape before individual lines: whether the change belongs in this module, a shared library, a service boundary, or a different layer.
3. Check dependency direction, ownership, boundaries, and data flow against documented architecture and established structure.
4. Inspect the public and internal interfaces being introduced or modified.
5. For each substantive structural issue, recommend a concrete remedy from the list below or explain a better context-specific alternative.
6. Consider whether the added abstraction or capability is justified by current requirements and real use cases.

## Checklist

### Fit and Responsibility

- Does the change follow established architecture, or is a new pattern justified by a concrete requirement?
- Does it integrate without special cases, hidden coupling, or knowledge of unrelated modules?
- Does functionality belong in the module/service that owns the concept?
- Does the change improve or worsen architectural drift?
- Are orchestration, domain behavior, persistence, transport, and presentation concerns separated where the project architecture expects it?

### Boundaries and Dependency Direction

- Are module, service, package, and domain boundaries respected?
- Do dependencies flow toward stable abstractions or intended owners rather than creating cycles or reverse dependencies?
- Is feature-specific behavior leaking into shared/general-purpose modules?
- Is there a canonical helper or service that should be reused instead of creating a near-duplicate?
- Are cross-service calls and shared data ownership explicit?

### Abstraction and Complexity

- Is the abstraction level appropriate: neither speculative nor tightly coupled?
- Does a refactor remove concepts/branches/layers, or merely move the same complexity elsewhere?
- Does a wrapper, adapter, factory, registry, or configuration option add meaningful isolation or only indirection?
- Can the unit be understood and tested without unnecessarily heavy setup?
- Are extension points justified by real variation rather than hypothetical future needs?

### Interfaces and Data Models

- Are interfaces minimal, cohesive, consistent, and difficult to misuse?
- Are type and data boundaries explicit? Are casts, escape-hatch types, and silent fallbacks hiding an unclear invariant?
- Does each unit have a coherent responsibility and reason to change?
- Are persistence-level constraints (uniqueness, nullability, foreign keys, checks, relationships) enforced at the authoritative data boundary where appropriate?
- Are ownership, lifecycle, and error semantics clear across component boundaries?

## Structural Remedies

Name a concrete move when recommending a structural fix. Candidate moves:

- Replace repeated conditional branching with a typed model, strategy, or explicit dispatcher where behavior truly varies by type/state.
- Collapse duplicate flows into one cohesive path.
- Separate orchestration from domain/business logic.
- Move feature-specific logic to the module that owns the concept.
- Reuse the canonical helper or service.
- Make a type/data boundary explicit so downstream branching disappears.
- Remove a pass-through wrapper that adds no useful contract.
- Extract a cohesive helper or split an oversized module by responsibility.
- Introduce an adapter/port only when it creates a real boundary or test seam.

Prefer the remedy that removes moving parts over one that spreads complexity across more files.

## Severity Guidance

- Broken architecture boundary, circular dependency, or ownership ambiguity that creates material correctness/security risk — High.
- Feature logic in shared code, unjustified abstraction, or complexity merely relocated — Medium; High when materially damaging.
- Minor coupling or unjustified pattern — Low or Medium according to concrete cost.

## Boundaries

- Line/function readability, naming, and local code smells belong to maintainability.
- Public contract compatibility over time belongs to compatibility-operability.
- Dependency provenance and lockfile hygiene belong to dependencies; dependency direction belongs here.
- Individual-unit overengineering belongs to maintainability when no architectural boundary is involved.
