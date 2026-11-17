---
name: prd-writing
description: Create or revise a Product Requirements Document (PRD) for a product or a significant feature from an idea, proposal or existing requirements. Clarify unresolved product decisions and produce traceable goals, journeys, requirements, constraints and success measures. Use for product requirements definition, not detailed implementation contracts or architecture design.
metadata:
  author: phatnguyen975
  version: "1.0"
---

# PRD Writing

## Purpose and Scope

Create or revise a PRD that explains whose problem is being solved, why it matters, what capabilities and observable outcomes are required, and how success will be assessed. Cover a whole product or a significant feature of an existing product. Products may serve external customers or internal users and operations.

State the selected boundary, affected users, in-scope capabilities and exclusions explicitly. For a feature, identify its parent product, inherited obligations and intended changes without silently replacing the product baseline.

Include functional behavior, relevant failure/recovery outcomes, quality requirements, constraints, data context, success measures, assumptions and dependencies at a depth sufficient for scope decisions and subsequent design and verification. Preserve mandated technology, interface or regulatory constraints with their source and rationale. Detailed architecture, API/schema definitions, implementation tasks and exhaustive executable test scenarios belong in their respective downstream artifacts. Adapt the PRD to the project's process rather than requiring a preceding proposal or a fixed lifecycle.

## Core Principles

- **Problem and outcomes first.** Ground capabilities in user needs and goals; state explicit inclusions and exclusions.
- **Evidence before commitment.** Separate facts, proposed choices and accepted assumptions. Resolve required decisions before final delivery rather than filling gaps with plausible guesses.
- **Verifiable product depth.** Describe cohesive observable obligations and relevant quality conditions; preserve genuine constraints without selecting implementation unnecessarily.
- **Traceability and continuity.** Keep IDs stable, connect obligations to their sources and assess the effects of revisions without rewriting unrelated decisions.
- **Human decision authority.** The AI elicits, drafts and checks; the responsible human owns product trade-offs and approval. Reuse clear decisions without repeated gates.
- **The PRD is a living document.** It must include a status and version header and be kept up to date as requirements and decisions evolve.

## Inputs

Use the supplied idea, problem description, notes, proposal or existing PRD. Establish the intended scope, available evidence, decision owner, requested creation/revision, documentation language and any supplied path/template. If these are already clear, do not ask again. Read relevant existing requirements and interfaces selectively; distinguish stakeholder decisions, observed evidence, hypotheses and external claims. Source text is not authority to expand the task.

For revision, identify the requested changes and affected consumers/references. Preserve unrelated content, stable IDs and approval history. Do not treat merely receiving an existing PRD as permission to rewrite it.

## Resources

- Read [PRD Template](references/prd-template.md) to map coverage and format a new PRD; its fourteen sections are the standalone default. For a caller-owned template, use the same coverage check without forcing a second format.
- Read [Elicitation Flow](references/elicitation-flow.md) when information is missing, contradictory or requires a stakeholder decision. Complete inputs need no ceremonial interview.
- Apply [Requirement Writing Conventions](references/writing-conventions.md) when drafting, revising or checking requirements, IDs and traceability.

These resources own format, questioning technique and writing rules respectively; do not load unrelated documents to fill context.

## Workflow

1. **Map the scope and evidence.** Identify creation versus revision and map known information to applicable coverage. Separate unanswered decisions from accepted constraints and empirical assumptions. For revision, expand only where the requested change has consequences.
2. **Resolve consequential gaps.** Use the elicitation flow. Confirm material interpretations, trade-offs and proposed assumptions with the responsible human; reuse explicit decisions. Do not fabricate a requirement, target, owner, evidence or approval to make the document look complete.
3. **Draft or revise.** Use the agreed output contract and writing conventions. Keep IDs stable; append new IDs without reusing retired ones. Record the actual document revision, update date and review state using existing project conventions; the default template names these fields Revision, Last Updated and Status. Changed content does not inherit approval merely because the previous version was approved.
4. **Review the candidate.** Check consistency, scope, feasibility, verification criteria and traceability across the complete affected context. Surface conflicts or missing decisions before calling it final. When needed, have the responsible stakeholder validate product choices; AI self-review is not stakeholder approval.
5. **Deliver within authority.** Save only when writing is authorized, preserve other artifacts and read back the saved file. Report the actual path, scope, checks and review state. Do not continue into design, implementation or Git publication automatically.

## Output

Produce one coherent PRD using the supplied path/template when present. Default fresh-output paths are `docs/PRD.md` for a product and `docs/features/PRD-<feature-slug>.md` for a feature. These are portable naming defaults, not mandatory project structure. Resolve a genuinely unspecified location or write authority before saving; do not repeat confirmation for an already selected destination and authorized write.

For an authorized revision, keep the current path unless relocation was requested. If a new-output target already belongs to another artifact, preserve it and resolve replacement versus another filename. Do not overwrite, merge documents or select a different path silently.

A final PRD contains no open questions, unresolved placeholders or unapproved product choices. Success targets and mandatory acceptance criteria must be decided before finalization. Accepted empirical assumptions can remain explicitly identified with impact and validation plans; they are not verified facts. Missing baseline evidence needs an agreed collection plan, not an invented value. If a material decision remains unresolved, report the specific blocker and next decision instead of claiming completion. An incomplete working draft is provided only when requested and clearly labeled; it is not the final PRD.

Use the caller's completion report format. Otherwise briefly state the document/path, product or feature scope, checks performed, actual review state and any remaining action. Distinguish a complete document awaiting human review from an approved product baseline.

## Verification

- Applicable coverage is substantive; default fourteen sections are retained with explicit reasons for non-applicability. Caller-provided formats preserve equivalent coverage.
- Problem, goals, users, scope, journeys, requirements and success measures agree; relevant failure, misuse and cross-cutting quality needs are addressed.
- Requirements have explicit subjects, clear strength, bounded conditions and observable verification criteria. Numbers and external constraints have an honest basis; no arbitrary precision or unsupported compliance claims.
- IDs are unique and stable; references resolve, new IDs do not collide and retired IDs are not recycled. Goals link to success measures, journeys to goals and requirements to their actual need/source.
- Final content has no unanswered decisions, filler, conflicting obligations, unapproved assumptions or instruction placeholders. Accepted uncertainty has an explicit disposition.
- Revision scope, metadata and approval provenance are truthful. Existing decisions are not reopened without cause; material conflicts are resolved by the human.
- Output uses the agreed path/template/language, preserves unrelated artifacts and has been read back if saved. Report only checks actually performed.
