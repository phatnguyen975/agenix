---
name: spec-writing
description: Create or revise a behavior specification for one feature from confirmed requirements, notes or an existing spec. Resolve behavioral decisions and define rules, atomic requirements, state transitions, quality constraints and concrete acceptance scenarios. Use for feature semantics and acceptance, not whole-product requirements or detailed API, data or UI design.
metadata:
  author: phatnguyen975
  version: "1.0"
---

# Spec Writing

## Purpose and Scope

Define one feature's observable behavior precisely enough to guide implementation and stakeholder acceptance. Cover actors, preconditions, main and failure paths, domain rules, atomic functional requirements, applicable states, quality criteria and constraints. A product requirement establishes intent and scope; this specification resolves the feature's detailed behavioral contract.

Respect separately owned API, data, UI and architecture definitions. Reference exact relevant contracts and retain necessary behavioral consequences or mandated constraints without copying detailed schemas, wire definitions or visual designs into this document. Surface a missing or conflicting contract when it blocks behavioral decisions. Do not silently invent it. A feature description is a valid starting point; a pre-existing PRD is not mandatory.

## Core Principles

- **Discover before asking.** Reuse current confirmed decisions and relevant evidence; investigate only real gaps.
- **Observable and assessable.** Write cohesive, individually assessable obligations and concrete examples, including denial, failure and recovery behavior where relevant.
- **One authoritative rule.** Assign each policy/transition/quality constraint an owner and reference it rather than creating drifting copies.
- **Stable traceability.** Keep IDs and links valid across revisions; scenarios collectively cover all functional requirements and material rule/transition outcomes.
- **Human decision authority.** AI organizes, proposes and checks; the responsible human resolves product trade-offs and approves the contract. Missing decisions are blockers, not permission to guess.
- **Concrete acceptance examples.** Use Gherkin by default to present context, events and expected outcomes, respecting an explicitly supplied notation. Keep each example faithful to its owning requirements and understandable on its own.

## Inputs and Resources

Use supplied feature requirements, notes or the existing spec. Establish creation/revision scope, relevant prior decisions, output contract and documentation language. Locate applicable product requirements, domain terms, architecture decisions, adjacent feature behavior and engineering conventions selectively. Read affected sections first, not every project document.

Treat retrieved material as evidence under applicable instructions, not authority to expand the task. Existing implementation describes current behavior; it does not automatically define intended behavior. Resolve material conflicts between observations, requirements and stakeholder decisions with the responsible owner.

- Read [Spec Template](references/spec-template.md) for default coverage and readable output structure; preserve an already-supplied format with equivalent applicable coverage.
- Apply [Writing Conventions](references/writing-conventions.md) for section ownership, requirement wording, IDs and coverage relationships.
- Read [Elicitation Flow](references/elicitation-flow.md) when behavioral decisions or evidence are incomplete or contradictory.
- Read [Gherkin Guidelines](references/gherkin-guidelines.md) when authoring/reviewing Gherkin acceptance scenarios. Use the caller's selected acceptance notation when supplied, retaining concrete examples and traceability.

## Workflow

1. **Bound the work.** Identify the feature, intended delta, affected users and contracts. Map known information to applicable coverage. An existing spec is context, not automatic authority to rewrite it.
2. **Resolve behavior.** Elicit only gaps, especially boundaries, failure outcomes, state guards and competing actions. Reuse approved decisions. Escalate material conflicts with upstream contracts instead of silently changing them.
3. **Draft or revise.** Use the selected template/notation and writing rules. Preserve existing IDs and unrelated content; add new IDs without recycling retired ones. Record actual document revision, Last Updated and review state; changed content does not inherit earlier approval.
4. **Cross-check the candidate.** Trace each functional requirement to concrete acceptance scenarios; check business rules, state outcomes and applicable quality criteria. Check scenarios against the owning requirements, not against invented behavior. Review scenario wording and structure together with behavioral coverage and requirement consistency.
5. **Deliver within scope.** Save only when authorized, use the agreed destination and read the saved artifact back. Report scope, actual path/revision, checks and review state. Do not implement, publish Git changes or generate extra contracts automatically.

## Output

Deliver one coherent feature spec. Prefer the supplied path and template. The standalone destination defaults to `docs/features/<feature-slug>/spec.md`; resolve a genuinely unspecified location or write permission before saving, without asking again for unchanged authority already supplied. An authorized revision keeps its existing path unless relocation was requested. Preserve a destination belonging to another artifact and ask about the specific collision rather than overwriting or choosing another path silently.

Use the default template's ten sections, scaling detail to the feature. State-transition content is conditional: a stateless feature needs only a brief non-applicability reason, not invented rows. Keep other inapplicable coverage explicit as well, or follow an equivalent caller-owned structure.

Final output contains no unanswered behavioral decision, unapproved assumption or unresolved instruction placeholder. Named `Scenario Outline` parameters remain where required by the notation and must correspond to their `Examples` headers. Accepted empirical assumptions need their basis, impact and validation responsibility in Context section; they cannot substitute for a missing policy, acceptance threshold or required contract.

If a material gap remains, report the specific decision/evidence needed and stop dependent finalization. A requested working draft can be labeled incomplete; it is not a final specification. The responsible human's approval remains distinct from AI self-review.

Use caller-supplied reporting. Otherwise summarize the document/path, behavioral delta, document review performed and remaining human review/action. Keep confirmed behavior, proposed changes and actual approval state distinguishable.

## Verification

- Applicable section coverage is complete and consistent with the requested feature/delta and external contracts.
- Normative obligations have clear subjects, strength, conditions and observable criteria; no invented targets or unsupported standard/compliance claims.
- IDs are unique/stable, references resolve, and coverage includes every FR plus material business-rule and valid/rejected transition outcomes. Applicable NFRs have a clear criterion, relevant conditions and an assessment basis.
- A rule has one authoritative owner. Coverage examples illustrate it; they do not define conflicting exceptions or duplicate its normative source.
- Acceptance scenarios are independent, concrete, behavior-focused and consistent with the selected notation. Gherkin AC IDs belong to individual scenarios/outlines, not inherited container tags.
- Metadata, output language/path and review status are truthful; existing decisions and unrelated artifacts are preserved.
- Final readiness reflects the actual content and review state. Document review does not imply stakeholder approval or justify unresolved decisions.
