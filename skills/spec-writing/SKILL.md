---
name: spec-writing
description: Creates an implementation-ready specification for one feature, through a structured interview that resolves every ambiguity before anything is written. Use this skill whenever the user asks to write, draft, or create a spec, a feature spec, or a specification for a feature — even when they don't say "spec" explicitly, such as "write up exactly what this feature needs to do before we build it" or "turn this into something an engineer could implement without asking me questions". Do not use it for a system-level or product-level requirements document covering multiple features or a whole product, or for any document outside this feature's own behavior and requirements.
metadata:
  author: phatnguyen975
  version: 1.0
---

# Spec Writing

## Overview

Turns a feature description, an approved PRD, existing implementation notes, or an existing `spec.md` into a complete, implementation-ready specification for one feature — detailed enough that an AI coding agent can build it correctly without asking follow-up questions.

Every requirement in this document is fully atomic and independently testable — a depth an upstream product-level requirements document deliberately stays above.

## When to Use

- A feature is ready to move from "what we've decided to build" into implementation-ready detail, and that detail doesn't exist yet.
- The user hands over a feature description, a PRD excerpt, meeting notes, or a one-pager and wants it turned into something an implementer can build from without further questions.
- Revising an existing spec because behavior, rules, or requirements for the feature changed.

## When Not to Use

- The request is for requirements across a whole system or multiple features at once — that is a product-level document, not this skill.
- The request is for a document outside this feature's own behavior and requirements — if such a document is needed, it is separate; this skill only links to it once it exists.
- The feature is trivial enough that nothing here would add clarity (e.g. "rename this label") — there's no ambiguity worth a structured spec.

## Input

| Input                                                     | Type                         | Required                                                   |
| --------------------------------------------------------- | ---------------------------- | ---------------------------------------------------------- |
| Feature description, PRD excerpt, or implementation notes | Text/document                | Required if no existing spec is provided                   |
| Existing project documentation relevant to this feature   | Files already in the project | Optional, but actively sought out                          |
| Existing `spec.md` (for revision)                         | Markdown file                | Optional — triggers revision mode instead of a fresh draft |

### Existing Project Documentation

Before interrogating the user, actively look for and read whatever of this already exists in the project rather than waiting for it to be pasted in. Exact file names and locations vary by project; look for documents along these lines:

- **Product requirements** — a PRD or similar upstream document covering this feature, if one exists.
- **Architecture or system design documentation** — how the relevant part of the system is currently structured.
- **Prior architectural decision records** — a log of past technical decisions and the reasoning behind them, commonly kept as a numbered series of short documents.
- **Specs for related or adjacent features** — existing specs elsewhere in the project, to pick up the vocabulary, conventions, and format already in use.
- **Repository-level engineering conventions** — a README, contribution guide, or engineering-practices document relevant to this feature.

Anything these already answer clearly is not re-asked — see `references/elicitation-flow.md`, Section 1.

## Output

A single Markdown file following the exact structure in `references/spec-template.md`, written only after every section is fully resolved and the output path has been confirmed with the user.

A project may run this skill once per feature, and again whenever that feature's spec needs revising. Never assume a single fixed location across different features, or a later run for a different feature could collide with an earlier one.

| Case                        | Default path + filename                                                    |
| --------------------------- | -------------------------------------------------------------------------- |
| New or revised feature spec | `docs/features/<feature-slug>/spec.md` (slug = feature name in kebab-case) |

- Always show the proposed path and get explicit confirmation before writing. A user-specified path overrides the default.
- If the target file already exists and revising it wasn't requested, don't overwrite silently — ask how to proceed.
- For a revision, write back to the existing file's path instead of applying the default.

## Core Principles

- **Discover before asking.** Existing project documentation is read and extracted before any question is asked — elicitation targets only genuine gaps, not information that's already written down somewhere.
- **Implementation-ready, not product-level.** Every requirement is atomic and independently testable.
- **Strictly template-scoped.** Only the sections in `references/spec-template.md` belong in the output — no additional topic gets its own content, however related it might seem.
- **Behavior over implementation.** Flows and acceptance criteria describe observable system behavior, not how it's built.
- **Single source of truth per fact.** The same constraint is never stated authoritatively in two places — a rule that's entirely about one state transition lives only in the State Transitions table, not also as a Business Rule. See "Section Boundaries" in `references/writing-conventions.md`.
- **Everything traceable gets a stable ID.** A `Rule` block cross-references the Business Rule it verifies; every Functional Requirement — whether or not a Business Rule backs it — is exercised by at least one scenario. See `references/writing-conventions.md`.
- **Normative language, capitalized** — `MUST`, `MUST NOT`, `SHALL`, `SHOULD`, `MAY`.
- **Zero unresolved ambiguity at output time.** No placeholder, guess, or open question survives into the final file.
- **Executable, testable acceptance criteria.** Every scenario is valid Gherkin, runnable by a Cucumber-compatible test runner exactly as written, with an observable, checkable outcome — not a prose bullet that only looks structured. See `references/gherkin-guidelines.md`.
- **The spec is a living document**, carrying a status/version header and expected to be revised as decisions change.

## Workflow

1. **Intake.** Read whatever is provided directly (feature description, PRD, existing spec, notes), and actively locate and read the project documentation described under "Existing Project Documentation" above — don't wait for it to be handed over. Extract everything these already answer, tracking each document consulted as a candidate for References. Map what's known against `references/spec-template.md`; list what's still genuinely missing. If the input includes an existing `spec.md`, this is a revision — interrogate only what the requested change actually affects; everything untouched is carried over as-is.
2. **Interrogate.** Resolve every open gap using `references/elicitation-flow.md`. Do not proceed until every section this case needs has concrete content.
3. **Draft or update.**
   - _Fresh draft_: populate the full template, applying `references/writing-conventions.md` and `references/gherkin-guidelines.md`.
   - _Revision_: edit the existing file in place — append new IDs at the next sequential number in their prefix (never renumber existing ones), update affected sections, bump the version, set `Status` back to `Draft` until reviewed.
4. **Self-check.** Run the checklist in "Verification" below against the draft or the updated file before showing it.
5. **Confirm output location.** Propose the file name and path per "Output" above and get explicit confirmation before writing. For a revision, write back to the existing file's path.

## Anti-Patterns to Avoid

- Writing content for a topic with no section in the template.
- Vague, unquantified requirements ("the system should handle errors gracefully").
- Acceptance criteria as unstructured prose instead of concrete scenarios.
- One scenario asserting multiple unrelated behaviors.
- Leaking automation or implementation mechanics into acceptance criteria (selectors, "click", "scroll to", raw HTTP/SQL).
- A functional requirement that clearly implements a Business Rule but doesn't reference it.
- Leaving an open question or placeholder in the final document.
- Over-specifying beyond what the feature actually needs.

## Common Rationalizations to Reject

- _"This feature seems simple, I can skip most of the interview."_ → Simple or not, every template section still gets resolved; only already-answered ones are skipped.
- _"I happen to know some details outside this feature's own behavior and requirements, I'll note them here too."_ → Not this document's job, even briefly. If relevant, it belongs in a separate document and gets linked from References, not described here.
- _"I'll write the acceptance criteria as a readable paragraph instead of full Gherkin — it says the same thing."_ → A paragraph isn't executable; it can't be run by a test tool or checked step by step. Acceptance criteria are always real Gherkin.
- _"This requirement is basically obvious, I don't need to quantify it."_ → Obvious to the person who wrote it, not verifiable by the person who reads it later. Quantify or resolve it through elicitation first.
- _"A `spec.md` already exists here, I'll just overwrite it — it's probably for the same change."_ → Never overwrite without explicit confirmation.
- _"I can't pin down this detail, I'll leave it broad so it stays flexible."_ → Push for a concrete decision through the same follow-up cap used for any other unresolved point; "flexible" is not a resolved requirement.
- _"This FR has no Business Rule behind it, so it doesn't need a scenario."_ → Every `FR` still needs at least one scenario verifying it somewhere — as part of an existing scenario it naturally fits into, or, if it doesn't fit anywhere else, its own `Scenario` directly under `Feature`. Either way, it doesn't go unverified.
- _"This state-transition rule reads naturally as a Business Rule too, I'll write it in both places."_ → If it's entirely about one specific transition — valid or not, and what happens either way — it belongs only in State Transitions; restating it as a `BR` duplicates the same fact in two places that can drift out of sync.

## Verification

Before presenting the final file, confirm all of the following:

- [ ] Every section required for this spec is present and non-empty; no section exists for a topic outside the template.
- [ ] No placeholder, "TBD", or bracketed instruction text remains anywhere.
- [ ] Every requirement uses `MUST` / `MUST NOT` / `SHALL` / `SHOULD` / `MAY`, capitalized, with no banned vague word from `writing-conventions.md`.
- [ ] Every `FR-xxx` that implements a specific Business Rule references it; none reference a `BR-xxx` that doesn't exist.
- [ ] Every `FR-xxx` is exercised by at least one Acceptance Criteria scenario — as part of a scenario under the `Rule` for the `BR` it implements, as an added assertion in another scenario that naturally covers it, or, when neither fits, its own `Scenario` directly under `Feature`, outside any `Rule` block.
- [ ] No `BR-xxx` merely restates a rule already fully captured by the State Transitions table.
- [ ] Every `Rule` block in Acceptance Criteria maps to a `BR-xxx`; every `Scenario` / `Scenario Outline` carries a sequential `@AC-xxx` tag.
- [ ] Every scenario follows `gherkin-guidelines.md`: strict Given/When/Then order, observable `Then` outcomes, domain-level language with no automation mechanics, 3-5 steps typical (10 as the outer limit), and is valid Gherkin a Cucumber-compatible runner could execute as written.
- [ ] If this feature has NFRs, they were checked against the category list in `elicitation-flow.md`, Section 2 — not just whatever came to mind first.
- [ ] Out of Scope is explicit and substantive, not a token line.
- [ ] References lists only documents actually consulted or actually needed for implementation, each with why it's there.
- [ ] The metadata header has Status, Date — v1 (or current version), and Owner, all filled in.
- [ ] The output path and filename were confirmed with the user before the file was written.
