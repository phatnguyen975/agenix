# Elicitation Flow

A single round of questions produces a thin, generic PRD. Run a structured, persistent interview until every section in `prd-template.md` has concrete, specific content. The rules below are grouped by where they apply during that interview.

## 1. Interview Order

- **Skip what's already answered.** Only interrogate the gaps and vague points found while mapping the input against the template. Never re-ask what the input material already states clearly.
- **Follow the template's dependency order:** Problem → Goals → Target Users → Journeys → Scope → Functional / Non-Functional Requirements → Constraints → Data → Success Metrics → Assumptions → Dependencies → Glossary. Each later section depends on decisions already locked earlier — journeys need known users, requirements need known journeys, metrics need known goals — so asking out of order produces answers that have to be redone.
- **Root-cause check on Problem Statement and Goals.** Before accepting a stated problem or goal as final, ask one follow-up along the lines of "why does that matter?" or "what happens if this isn't addressed?" to confirm it's the actual driver, not a symptom or a restated feature request. Stop as soon as the answer stops changing the scope of the PRD — usually one or two levels deep, not an exhaustive chain.

## 2. Question Sequence Per Gap — Open Before Closed

For each remaining gap, move through these stages in order:

1. **Open.** Ask one open-ended question in the user's own words — "What should happen when a check-in fails?" — so they can volunteer context the interview didn't anticipate.
2. **Probing.** If the answer comes back vague or partial, sharpen it along whichever of these dimensions is actually missing, rather than a generic "can you clarify?": **Who** (actor), **What** (capability), **When** (trigger/timing), **Where** (context/channel), **Why** (goal), **How** (mechanism/condition).
3. **Closed.** If a concrete decision is still unresolved after probing, close with 2-4 suggested options grounded in the input material or common patterns for that type of system, plus an explicit "something else" option — e.g. "Expected traffic — (a) under 100 req/s, (b) 100-1,000 req/s, (c) over 1,000 req/s, (d) something else?" This gives the user a concrete answer to react to instead of a blank page, without skipping the chance for them to say something unexpected first.

One question at a time throughout — each answer shapes the next question; never dump a checklist on the user at once.

## 3. Wording

- **Ask about the concrete present, not a hypothetical future.** Prefer "what happens today when X?" or "how do you currently handle Y?" over "would you want X?" or "do you think X is a good idea?" — a question about an imagined future tends to produce an optimistic, unreliable answer rather than a usable decision.
- **Keep questions and options neutral.** Don't phrase a question so it implies the expected answer (not "don't you think this should be fast?"). Order suggested options along a neutral axis — magnitude, chronology — not by which one seems preferable.

## 4. Convergence

- **No vague answer is final.** A generic response ("make it fast", "for all users") goes back through the probing/closed stages in Section 2.
- **Follow-up cap.** After at most two follow-ups on the same point, stop repeating the question. Propose a concrete working decision drawn from context and ask for a yes/no confirmation instead. This guarantees the interview converges rather than looping.
- **"I don't know" triggers the same fallback** — a proposed working decision to confirm, never a blank.

## 5. Prioritization

- **Force a real trade-off for each journey's Priority.** Don't accept a default "High" for everything. Once two or more journeys are captured, ask a forced-choice question across them — "If only one of these could ship first, which is it?" — so Priority reflects an actual decision, not an unconsidered label.

## 6. Throughout

- **Contradictions are surfaced immediately** — not carried silently into the draft (e.g. a stated goal that conflicts with a declared Out-of-Scope item).
- **Answers are reflected back for confirmation** before moving to the next section ("So the primary user is X, and Y is explicitly out of scope — confirm?"), catching misunderstandings early rather than at final review.
- **Drafting starts only once every section is concrete.** The output step never runs against a partially-answered interview.
