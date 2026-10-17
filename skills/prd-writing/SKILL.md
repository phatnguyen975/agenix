---
name: prd-writing
description: Creates a system-level or feature-level Product Requirements Document (PRD) from a raw idea, concept description, or existing proposal, through a structured interview that resolves every ambiguity before anything is written. Use this skill whenever the user asks to write, draft, or create a PRD, a product requirements document, or a requirements document for a new system or a new feature being added to an existing system — even when they don't say "PRD" explicitly, such as "help me define what this system needs to do", "turn this idea into formal requirements", or "write up what we need before we start building this". Do not use it for low-level technical specs, API/schema design, or fully detailed feature-level acceptance criteria — that level of detail belongs to a separate feature-spec step.
---

# PRD Writing

## Overview

Turns a concept, raw idea, system description, or existing proposal into a complete `PRD.md`. The PRD sits between a project proposal (why this should be done at all) and a feature spec (the detailed, implementation-ready breakdown). It defines what the system or feature must do and why, at system/product level — not how it will be built, and not broken down to feature-spec granularity.

## When to Use

- Starting a new system or product and formal requirements don't exist yet.
- Adding a significant new feature or capability to an existing system and its scope, requirements, and success criteria need to be defined before design or implementation work starts.
- The user hands over a raw idea, a meeting summary, a one-pager, or an existing proposal document and wants it turned into structured requirements.
- Revising an existing PRD because scope, goals, or requirements changed.

## When Not to Use

- The user wants a pitch-level business case or go/no-go justification, not requirements — that's a proposal, a step before this skill, not this skill.
- The user wants implementation-ready detail: API contracts, database schema, fully decomposed acceptance criteria, edge-case enumeration, or architecture decisions — that's feature-spec or design-doc work, a step after this skill, not this skill.
- The request is for a small, single, unambiguous change with no real scope or requirements question (e.g. "rename this button") — there is nothing here worth a structured requirements document.

## Input

| Input                                     | Type          | Required                                                           |
| ----------------------------------------- | ------------- | ------------------------------------------------------------------ |
| Concept, raw idea, or problem description | Text          | Required if no document is provided                                |
| Existing proposal, spec, or notes         | Document/text | Optional — supplies answers that reduce how much needs to be asked |
| Existing `PRD.md` (for revision)          | Markdown file | Optional — triggers revision mode instead of a fresh draft         |

At least one of the first two must be present. Anything the input already answers clearly is not re-asked — see `references/elicitation-flow.md`, Section 1.

## Output

A single Markdown file following the exact structure in `references/prd-template.md`, written only after every section is fully resolved and the output path has been confirmed with the user.

A project may run this skill more than once — once for the initial system PRD, again for each new feature added later. Never assume a single fixed `PRD.md` name for every run, or a later run will silently overwrite the original.

| Case                                    | Default path + filename                                                                                  |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| New system (first PRD for a system)     | `docs/prds/PRD.md`                                                                                       |
| New feature added to an existing system | `docs/prds/PRD-<feature-slug>.md` (slug = feature name in kebab-case, e.g. `PRD-notification-center.md`) |

- Always show the proposed path and filename and get explicit confirmation before writing. A user-specified path or filename overrides the default.
- If the target file already exists and revising it wasn't requested, do not overwrite it silently — propose the feature-slug variant, or ask how to proceed.
- `docs/prds/` is the default root for every PRD this skill produces, so system-level and feature-level PRDs stay grouped and distinguishable.
- These defaults apply to a fresh draft only. When revising an existing `PRD.md`, write back to its current path — don't apply the defaults above or ask again, unless the user asks to move or rename the file.

## Core Principles

- **Problem-first, not solution-first.** Open with the user/business problem and why it matters, before any capability description.
- **System-level, not implementation-level.** Architecture, API design, and acceptance-criteria-level detail stay out — they belong downstream.
- **Capability-level, not task-level.** Requirements describe what the system must support, not a fully decomposed, atomic requirement set.
- **Everything traceable gets a stable ID**, and cross-references its origin: a requirement points to the journey it supports, a metric points to the goal it measures. See `references/writing-conventions.md`.
- **Normative language, capitalized** — `MUST`, `MUST NOT`, `SHALL`, `SHOULD`, `MAY` — so requirement strength is scannable at a glance.
- **Zero unresolved ambiguity at output time.** No placeholder, guess, or open question survives into the final file.
- **User-journey driven**, not a flat, unprioritized feature list.
- **Explicit scope boundary.** What is not being built is stated as clearly as what is.
- **Success is measurable before build starts.** Every metric has a target, not just a direction.
- **Assumptions and dependencies are written down, not implied.**
- **The PRD is a living document**, carrying a status/version header and expected to be revised as decisions change.

## Workflow

1. **Intake.** Read whatever is provided (idea, proposal, existing PRD). Map what's already known against `references/prd-template.md`; list every remaining gap. If the input includes an existing `PRD.md`, this is a **revision**, not a fresh draft — continue at step 2 but only for what the requested change actually affects (new or changed goals, journeys, requirements, etc.); everything untouched by the change is carried over as-is, not re-interrogated.
2. **Interrogate.** Resolve every open gap using the structured interview in `references/elicitation-flow.md`. Do not proceed until every section this case needs — the full template for a fresh draft, or just the affected parts for a revision — has concrete content.
3. **Draft or update.**
   - _Fresh draft_: populate the template fully, at system/product-level depth, applying `references/writing-conventions.md`. Select the section subset for this case using the applicability table in `references/prd-template.md`.
   - _Revision_: edit the existing file in place — add new IDs following the next sequential number in their prefix (never renumber existing ones), update affected sections, bump the version, and set `Status` back to `Draft` until the revision is reviewed.
4. **Self-check.** Run the checklist in "Verification" below against the draft or the updated file before showing it.
5. **Confirm output location.** For a fresh draft, propose the file name and path per "Output" above and get explicit confirmation before writing. For a revision, write back to the existing file's path unless the user asks to move it.

## Anti-Patterns to Avoid

- Solution-first framing — opening with "what to build" instead of "why".
- Vague, unquantified requirements ("the system should be fast").
- Leaving an open question or placeholder in the final document.
- Missing or deferred success metrics.
- No scope boundary, or one that's implied rather than stated.
- Feature-spec depth: fully atomic requirements, exhaustive acceptance criteria, edge-case enumeration.
- Implementation detail inside the PRD: API specs, database schema, code-level design.
- A requirement with no link back to a goal or journey.
- A static document that's never revisited as decisions change.
- Accepting a vague answer during the interview and moving on anyway.

## Common Rationalizations to Reject

These are tempting shortcuts during this workflow — each one defeats the point of the skill:

- _"The idea already sounds clear enough, I can skip the interview."_ → Skip only what the input explicitly answers, never based on a general impression that the idea "feels" clear.
- _"This detail is minor, I'll just pick something reasonable."_ → Minor or not, an unresolved decision goes through the follow-up cap (propose a working decision, get it confirmed) — it is never silently assumed.
- _"I'll write 'should be fast' and the user can fix the number later."_ → An unquantified requirement doesn't get written; it gets resolved through elicitation first.
- _"The user seems busy, I'll shorten the interview."_ → Shorten the questions, not the coverage — every section still gets resolved; only already-answered ones are skipped.
- _"This is basically a feature, so I'll add full acceptance criteria to be extra helpful."_ → Stay at capability level. Acceptance-criteria detail is explicitly out of scope for this document.
- _"A `PRD.md` already exists here, I'll just overwrite it — it's probably the same thing."_ → Never overwrite without explicit confirmation; propose the feature-slug filename instead.
- _"I can't find a good number for this metric, I'll leave it qualitative."_ → Push for a concrete target through the same follow-up cap used for any other unresolved point; a metric with no target doesn't go in the file.
- _"Offering multiple-choice options right away is faster than asking open-ended first."_ → Faster isn't the goal here — an open question first can surface something the suggested options wouldn't have covered. Closed options are the last stage of the sequence, not the first.
- _"Every journey the user described sounds important, I'll mark them all High."_ → Priority is a forced trade-off, not a default. If everything is unranked, ask the trade-off question before writing a Priority value.

## Verification

Before presenting the final file, confirm all of the following:

- [ ] Every section required for this system type (per the applicability table in `prd-template.md`) is present and non-empty.
- [ ] No placeholder, "TBD", or bracketed instruction text remains anywhere.
- [ ] Every requirement uses `MUST` / `MUST NOT` / `SHALL` / `SHOULD` / `MAY`, capitalized, with no banned vague word from `writing-conventions.md` in any Goal, Requirement, Constraint, or Metric line (narrative sections are exempt — see that file).
- [ ] Every Functional Requirement references at least one journey ID; every Success Metric references at least one goal ID.
- [ ] Every ID prefix (`G`, `UJ`, `FR`, `NFR`, `CON`, `SC`, `A`, `D`) is used correctly, sequential within its own prefix, with no duplicates.
- [ ] Out of Scope is explicit and substantive, not a token line.
- [ ] If two or more journeys exist, Priority values are not all the same by default — a trade-off was actually asked and answered.
- [ ] No implementation-level or technology-specific detail is present.
- [ ] The metadata header has Status, Date — v1 (or current version), and Owner, all filled in.
- [ ] The output path and filename were confirmed with the user before the file was written.
