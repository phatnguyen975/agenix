---
name: domain-modeling
description: Discover, design, review, or evolve a business domain model using Domain-Driven Design (DDD). Use for ubiquitous language, domain terminology, business rules, subdomains, bounded contexts, context mapping, business workflows and events, or tactical domain modeling (entities, value objects, aggregates, invariants, policies, and domain services). Keep the model technology-independent; do not use for database schemas, API contracts, UI, code structure, architecture style, or deployment design.
metadata:
  author: phatnguyen975
  version: 1.0
---

# Domain Modeling

## Purpose and Boundaries

Create a coherent, **business-centered model and ubiquitous language** that domain experts and designers can use to understand decisions, responsibilities, and behavior. Apply DDD selectively:

- **Strategic design:** business capabilities and subdomains (problem space); bounded contexts, their distinct languages, and their relationships (model boundaries).
- **Behavioral discovery:** business intentions, decisions, meaningful events, outcomes, exceptions, information needs, and policies.
- **Tactical design:** entities, value objects, aggregates, invariants, and domain services where identity, behavior, and consistency justify them.

A subdomain is **not** automatically a bounded context. A bounded context is **not** automatically a service, team, repository, database, or deployment unit. Do not prescribe technical schemas, APIs, integration transports, code structure, UI, infrastructure, or technology choices. Business-level interaction and consistency requirements remain in scope.

## Select the Task

Choose one **operation** and a **scope** from the request; do not invent a fourth operation for focused work.

| Operation  | Responsibility                                                                                                                                                                     |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Design** | Discover and design a new model from business evidence, then validate it before delivery.                                                                                          |
| **Evolve** | Read the existing model, identify changed requirements and their impact, update only affected parts, and validate regressions before saving.                                       |
| **Review** | Assess an existing model against business evidence and DDD design criteria. Return actionable findings; change the model only if explicitly requested, following the Evolve rules. |

| Scope          | Deliverable                                                                                                                                                                                                   |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Focused**    | Only the requested decision or model slice, together with relevant dependencies and validation evidence. Do not manufacture a full domain model.                                                              |
| **Full Model** | All in-scope domain elements. For Design/Evolve, use the `assets/domain-model-template.md` when a complete design document is requested. For Review, return findings unless an updated document is requested. |

Respect the user's language, file path, project conventions, and stated scope. When none is specified, use English and `docs/domain-model.md` **only if** a complete design document is requested. Read an existing file before changing it; Review alone never authorizes writes.

## Business Evidence and Human Confirmation

1. **Source business facts.** Use approved requirements, explicit business scenarios, authorized stakeholder/domain-expert decisions, and relevant project artifacts. Cite material rules and decisions. Existing code describes observed behavior, not necessarily intended business policy. Do not invent rules, events, authorities, guarantees, or approvals.
2. **Clarify early and continuously.** At intake, compare inputs for missing scope, conflicting terminology, unowned decisions, and undefined outcomes. Ask the human for **material** gaps before relying on them. During strategic, behavioral, and tactical modeling, ask again when new material uncertainties appear; do not defer all clarification to the last step.
3. **Distinguish a working hypothesis from a final decision.** A provisional model, candidate boundary, or proposed policy may guide **internal discovery** while evidence is incomplete. Label it explicitly in working analysis and identify what must be confirmed. Never silently promote a proposal to a business fact or final deliverable.
4. **Require authoritative confirmation where it matters.** A decision is material if changing it could alter business outcomes, rules/exceptions, core terminology, responsibility/authority, context boundaries with business consequences, hard invariants, cross-context obligations, or required scenarios. Confirm these decisions with the human unless an existing, explicit, authoritative approval already establishes them. Silence, tool output, and AI inference are not approval. Do not ask humans to approve every ordinary modeling choice.
5. **Separate design judgment from business authority.** The agent may choose and justify DDD representations that preserve confirmed business semantics. When alternatives encode different business obligations or ownership, present the trade-off and ask for a human decision.
6. **No unresolved decisions in the final design.** If a material point remains unanswered or conflicting, pause the affected design/evolution, ask precise questions, and do not write or overwrite the final model. Provisional notes can be discussed in conversation if useful; they are not the final `domain-model.md`. Exclude optional, irrelevant detail rather than inventing it; do not use exclusions to conceal an in-scope gap.

## Reference Routing

Use **progressive disclosure** — load only the reference needed for the current modeling decision. For focused tasks, skip unrelated topics. Read `references/model-validation.md` when validating or reviewing a deliverable. Read the `assets/domain-model-template.md` only when authoring or auditing a complete design document.

| Decision or Task                                                                          | Read                                |
| ----------------------------------------------------------------------------------------- | ----------------------------------- |
| Business events, process branches, triggers, and discovery hotspots                       | `references/event-discovery.md`     |
| Term definitions, synonyms, conflicting meanings, and translations                        | `references/ubiquitous-language.md` |
| Business capabilities, subdomains, strategic importance, and context boundaries           | `references/strategic-design.md`    |
| Context relationships, influence, collaborations, and business messages                   | `references/context-mapping.md`     |
| Business rules, behavior, commands, policies, entities/value objects, and domain services | `references/tactical-design.md`     |
| Aggregate roots, invariants, lifecycles, and consistency boundaries                       | `references/aggregate-design.md`    |
| Scenario checks, review findings, confirmation and release gates                          | `references/model-validation.md`    |
| Complete domain-model document structure                                                  | `assets/domain-model-template.md`   |

## Modeling Workflow

This is a **default order, not a rigid waterfall**. Discovering behavior may change language, subdomains, boundaries, or aggregate candidates. Revisit affected decisions, obtain new confirmation as needed, and revalidate. Apply only relevant steps for focused work.

### 1. Intake and Clarify

- Identify the business goal, scope, exclusions, actors, source-of-truth inputs, required scenarios, and intended output.
- For Evolve/Review, read the existing model and change request; identify what is already confirmed and what might be outdated or affected.
- Compare sources, identify material omissions or contradictions, and ask human questions before making affected design decisions. Batch related questions with their implications. Continue with independent, evidenced work while waiting if safe; do not finalize affected content.

### 2. Discover Language and Behavior

- Build and test essential business terms using `references/ubiquitous-language.md`.
- When decisions or processes matter, use `references/event-discovery.md` to examine commands/actions, meaningful occurrences, required information, alternative/refusal paths, and unresolved hotspots.
- Discuss material disputed meanings and business outcomes with the human. A glossary-only task need not invent an event timeline.

### 3. Model Subdomains and Bounded Contexts

- Use `references/strategic-design.md` to identify distinct business capabilities and, when strategy is known, their Core/Supporting/Generic classification.
- Define bounded-context responsibilities, language, decision ownership, and subdomain coverage. Test candidate boundaries with real scenarios; confirm material ownership and semantic disputes.

### 4. Map Material Relationships

- Use `references/context-mapping.md` for genuine business dependencies, influence, translations, and cross-boundary interactions.
- Distinguish upstream/downstream **model influence** from message direction. Do not invent context-pair edges or apply patterns without a supported reason.

### 5. Model Rules and Consistency

- Within relevant contexts, use `references/tactical-design.md` for confirmed business rules and behavior (actions, triggers, decision owners, outcomes), then policies, identities, and domain services as justified.
- Use `references/aggregate-design.md` when actual invariants, lifecycle restrictions, or concurrent decisions require a consistency boundary. Choose tactical depth from domain complexity and scenarios, not solely from subdomain type.
- Clarify unknown refusal behavior, timing, authority, and required consistency with the human before treating them as design requirements.

### 6. Validate and Deliver

- Apply `references/model-validation.md` to the requested scope and its relevant dependencies. Check evidence, confirmed decisions, normal/alternative/refusal scenarios, terminology, ownership, consistency, and cross-context semantics where applicable.
- Resolve failures and material blockers, obtain any missing human decisions, update the model, and rerun affected checks. Only release a final design after all release gates pass; otherwise ask for the missing decisions and stop without creating or overwriting the final artifact.
- For a full Design/Evolve deliverable, populate the `assets/domain-model-template.md` **after** validation, with no unresolved questions, provisional claims, instructional placeholders. For focused work, deliver the requested model slice without inventing a full document. For Review, report findings and limitations; do not edit the model without permission.

## Operation-Specific Checks

- **Design:** Verify that each in-scope requirement and business scenario maps to an appropriate decision, context, or explicitly confirmed external responsibility. Do not let the template dictate unsupported tactical elements.
- **Evolve:** Trace changed requirements through terminology → rules and behavior → context ownership and relationships → cross-boundary business messages → affected aggregates and invariants → regression scenarios, as applicable. Preserve unaffected, evidence-backed material. Do not overwrite the existing final model with an unconfirmed change; leave it unchanged until the applicable release gates pass.
- **Review:** Distinguish confirmed defects, unverifiable claims, and optional improvements. Report location, finding, evidence, impact/severity, and recommended correction or human decision. An assessment can finish with blockers; that does **not** validate the assessed design. If corrections are requested, use the Evolve workflow and its release gate.

## Final Quality Gates

A final model, whether focused or full, must satisfy the applicable checks:

- **Authority:** No material unresolved or conflicting business fact or decision within scope; material business decisions have explicit human confirmation or traceable prior approval.
- **Semantics:** Terminology and business rules agree across requirements, examples, and relevant contexts; contextual differences and translations are explicit.
- **Coverage:** Material in-scope capabilities and scenarios have owned business behavior and supported results; exclusions are intentional and confirmed.
- **Boundaries:** Subdomains, bounded contexts, ownership, and important dependencies are coherent and do not conflate domain design with deployment architecture.
- **Behavior and Consistency:** Events are facts, commands are intentions, refusals are not manufactured events; claimed invariants and cross-context guarantees are supportable under relevant failure/concurrency cases.
- **Validation:** Required scenarios pass; there are no material `Fail` or `Blocked` outcomes in the agreed scope. Review findings never substitute for acceptance.
- **Artifact:** No unfilled `<...>` instructions, open questions, pending approvals, invented content, or provisional decisions appear in the delivered model.
