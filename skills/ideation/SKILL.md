---
name: ideation
description: Refine a raw idea into a sharp, actionable concept through divergent-then-convergent thinking — generate several real variations, evaluate them against value/feasibility/differentiation, surface hidden assumptions, and converge on one direction with explicit trade-offs. Use when an idea is still vague, before committing to a spec or plan, or when the user asks to "ideate", "refine this idea", or "brainstorm directions".
metadata:
  author: phatnguyen975
  version: 1.0
---

# Ideation

## Overview

A concept-refinement primitive — opens a raw idea up into real alternatives, then narrows it down to one direction with its trade-offs made explicit.

- Raw ideas usually get built before anyone checks whether they're worth building, or whether a better direction exists.
- Opens the idea up first (several genuinely different directions), then narrows it down (evaluate, pick, make trade-offs explicit).
- Applies equally to a vague early-stage concept, a feature inside an existing codebase, or a process/workflow idea — not just product ideas. The framework stays the same; the output adapts to the kind of idea it is.
- Produces one deliverable — a concept one-pager: problem statement, chosen direction, tiered assumptions, MVP scope, an explicit "not doing" list.
- Saved only after the human confirms where — never assumed, never auto-written.

## When to Use

Trigger phrases: "help me refine this idea", "ideate on [concept]", "brainstorm directions for X". Typical situations:

- The request is still an idea, not a decided direction — e.g. "we should do something about X" with no concrete shape yet.
- Before committing to a spec or plan, where more than one genuinely different approach exists and picking the wrong one would be costly to walk back later.

## When NOT to Use

- **The direction is already chosen.** Pinning down how to build an already-decided plan is a separate concern from deciding what to build.
- **The idea is already narrow and well-defined** — a one-line fix, a clearly-scoped small task.
- **Explicit time pressure, exploration not wanted.** Respect it — but name, in the normal response, whatever assumption is being carried forward unexamined.

## Input & Invocation

```
ideation
<the raw idea, in plain language>
```

- The idea is whatever was described with the invocation, or the task already in front of you.
- Flag briefly that you're opening it up before narrowing, so the person can redirect if they'd rather proceed directly — then go straight into Workflow.

## Output

One concept doc — a markdown one-pager. Ask where to save it (a sensible default like `docs/ideas/<slug>.md` if nothing in the project suggests otherwise); write it only after the human confirms.

```markdown
# <Idea Name>

## Problem Statement

<one-sentence "How Might We" framing — a reframe, not a rephrase>

## Recommended Direction

<the chosen direction and why — 2–3 paragraphs max>

## Key Assumptions to Validate

### Must Be True (Dealbreakers)

- [ ] <assumption — how to test it>

### Should Be True (Important)

- [ ] <assumption — how to test it>

### Might Be True (Nice to Have)

- [ ] <assumption>

## MVP Scope

<the minimum version that tests the riskiest assumption — one job done well, what's in, what's out. For a process/workflow idea, this is a zero-cost experiment to try, not a build>

## Not Doing

- <thing> — <reason>

## Open Questions

- <question that needs answering before building>
```

- "Not Doing" carries the most weight here — focus means explicit no's, not just a list of yeses.
- Every assumption needs a way to check it, not just a statement that it's unvalidated — its tier (Must/Should/Might) decides how urgently.
- "Building" above means whatever "doing" means for this idea — code, a process change, or an experiment to run.

## Core Principles

1. **Simplest version that solves the real problem** — not the most feature-complete one.
2. **Start from the person and their problem**, work back to the solution and the technology — not the reverse.
3. **Say no to far more than you say yes to.** Focus beats breadth — this is exactly what "Not Doing" exists to make explicit.
4. **Breadth, then depth.** Divergent phase generates real variation; convergent phase actually narrows, doesn't just rubber-stamp the first idea.
5. **"How it's usually done" isn't a reason on its own.** Challenge convention explicitly.
6. **Aim past the stated ask.** A faster horse is still a horse — look for the direction the person hasn't thought to ask for yet, not just a better version of the obvious one.
7. **Unseen parts deserve the same rigor as visible ones.** Scoping decisions and trade-offs nobody will notice still deserve the same care as the parts everyone sees.
8. **Honest, not agreeable.** A weak idea stays weak if nobody says so, specifically and kindly.
9. **Have opinions, not just options.** State a lean and why — "I'd push you toward A" teaches as much as the options themselves. A neutral list of alternatives is a menu, not a thinking partner.
10. **Name assumptions before committing**, not after, and sort them by how much they matter — not every assumption deserves the same urgency.

## Tone

Direct, thoughtful, slightly provocative — a sharp thinking partner, not a facilitator reading from a script. "That's interesting, but what if..." energy — push one step further, without being exhausting.

## Workflow

A default flow, not a rigid script — adapt to what the person says. This is a conversation, not a form to fill in. Exactly three phases — resist adding more. Full example: `references/worked-examples.md`.

**Phase 1 — Open It Up (Divergent)**

1. Restate the idea as a crisp "How Might We" question — this should _reframe_ the problem, not just rephrase the ask (e.g. "add real-time collaboration" reframes to "let people work simultaneously without chaos"). Forces clarity on what's actually being solved.
2. Ask a handful of sharpening questions (not more than ~5): who's this for, what does success look like, real constraints (time, tech, resources, etc.), what's been tried before, why now. Don't move on until target user and success criteria are clear.
3. Generate a handful of genuinely different variations (roughly 5–8) using 2–3 lenses that fit what's actually uncertain about the idea — inversion, removing a constraint, a different audience, combining with something adjacent, radical simplification, radical scale, an expert's obvious-but-invisible angle. Give each variation a one-line bet — why it might work — not just a label. Full lens set and deeper frameworks (SCAMPER, Jobs-to-Be-Done, First Principles, Pre-mortem, and more): `references/ideation-techniques.md`.
4. Push past the literal ask — look for the direction nobody thought to request yet, not just a faster version of the obvious one.
5. Working inside an existing project? Check existing constraints, patterns, and architecture first — ground variations in what's actually there, and reference specific files and patterns when relevant.
6. Not a product idea? The same framework applies to a process or workflow idea — variations become process changes or zero-cost experiments, not features.

**Phase 2 — Narrow It Down (Convergent)**

1. Cluster what resonated into 2–3 genuinely distinct directions, not variations on one theme.
2. Evaluate each against: **User value** (who benefits and how much?), **Feasibility** (what it costs to build?), **Differentiation** (what makes it genuinely different?). Full evaluation rubric: `references/evaluation-criteria.md`. Inside an existing codebase, ground feasibility in what's actually there (specific files, existing patterns), not abstract estimates.
3. Name the hidden assumptions per direction, sorted by how much they matter: what must be true or the idea fails outright, what should be true or the approach needs adjusting, what might be true but isn't worth validating yet. A pre-mortem ("imagine this already failed — why?") is a good way to surface the first tier. This is where most ideation fails if skipped.
4. Push back on weak directions specifically and kindly — don't just validate whatever resonated.
5. State a lean. Say which direction you'd push toward and why — not just a neutral comparison table.

**Phase 3 — Sharpen and Ship**

1. Produce the concept doc (Output above) for the chosen direction. Scope the MVP around the single riskiest assumption, not a feature list — one job, done well.
2. Confirm with the human before saving anywhere.

## Anti-Patterns

| Anti-Pattern                                                       | Fix                                                                                |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| A large pile of shallow variations (20+)                           | A handful of considered ones (5–8) beats many shallow ones                         |
| Agreeing with every direction the person likes                     | Push back on weak ones, specifically and kindly                                    |
| Skipping "who is this for"                                         | Every direction starts with a person and their problem                             |
| Converging without naming assumptions                              | Name what's being bet on before committing, tiered by how much it matters          |
| Producing a direction with no "Not Doing" list                     | Make the trade-offs explicit, every time                                           |
| Variations listed as bare bullets with no reason                   | Each one needs a stated bet, not just a label                                      |
| Running every lens or framework mechanically                       | Pick what fits the idea, not all of them                                           |
| Jumping straight to the concept doc, skipping divergent/convergent | Both phases matter — speed isn't the point                                         |
| Ignoring existing project patterns when ideating inside one        | Ground variations in what's actually there                                         |
| Adding extra phases or steps beyond the three                      | Three phases, each doing one thing well — resist scope creep in the process itself |

## Best Practices

- Ground variations in real constraints once they're known, not before.
- Make "Not Doing" as concrete as "Doing" — vague trade-offs aren't trade-offs.
- Give each assumption a concrete way to check it, and sort it by tier before deciding how urgently to validate it.
- Keep sharpening questions to a handful — more becomes an interrogation, not a conversation.
- Reference specific existing patterns or files when ideating inside a project, not generic advice.
- Scope the MVP around the single riskiest assumption, not a wishlist of features.

## Common Rationalizations to Reject

| Rationalization                                                | Why it's wrong                                                                                              |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| "More variations is always better."                            | Shallow breadth crowds out real evaluation — a handful of considered directions beats twenty bullet points. |
| "This direction sounds good, no need to push back."            | Agreement isn't evaluation — a weak idea needs specific pushback, not validation.                           |
| "We'll figure out the assumptions later."                      | Later is usually after the thing's already built on them. Name them, and their tier, before committing.     |
| "This idea is simple enough to skip the divergent phase."      | Simple-seeming ideas still have a "who" and a "why now" worth checking once.                                |
| "The existing codebase doesn't matter for a new feature idea." | It's both a constraint and a source of patterns worth reusing — check it first.                             |
| "One more phase would make this more thorough."                | Three phases, each doing one thing well — add steps and the process stops being usable.                     |
| "Everyone could use this, so the value is obvious."            | If no specific person can be named, the value isn't established yet — that's a red flag, not a strength.    |

## Verification

Before presenting the concept doc:

- [ ] The "How Might We" problem statement reframes the problem, not just rephrases the ask.
- [ ] Target user and success criteria are defined, not assumed.
- [ ] More than one direction was actually explored, not just the first idea, and each variation had a stated bet.
- [ ] A lean was stated for the recommended direction, not just a neutral comparison.
- [ ] Assumptions are tiered (Must/Should/Might be true), not a flat list.
- [ ] MVP Scope targets the riskiest assumption — one job done well, not a feature checklist.
- [ ] "Not Doing" makes trade-offs explicit, not just a wish list of what's included.
- [ ] Output is the concept doc itself, not just conversation.
- [ ] The human confirmed the direction and save location before anything is written.
