# Elicitation Flow

A single round of questions produces a thin, generic spec. Run a structured, persistent interview until every section in `spec-template.md` has concrete, specific content.

## 1. Interview Order

- **Skip what's already answered** by the input or by the project documentation gathered during Intake — only interrogate real gaps.
- **Follow the template's dependency order:** Context → Scope → Actors & Flow → Business Rules → Functional Requirements → State Transitions (if applicable) → Non-Functional Requirements → Technical Constraints → Acceptance Criteria. Everything that defines _what the feature does_ (rules, requirements, states) is locked before moving to _quality attributes and constraints_. Acceptance criteria are elicited last of all, because they formalize the flow, rules, and requirements already locked earlier as concrete examples — writing them any earlier means redoing them.
- **Root-cause check on Context**, when there's no upstream document to draw from: confirm why this feature is needed before detailing its behavior — one "why does that matter?" follow-up, not an exhaustive chain.

## 2. Non-Functional Requirements Coverage

When the interview reaches Non-Functional Requirements, walk through each category below for this feature — include it as an `NFR-xxx` if it applies, skip it if it genuinely doesn't, but don't skip it by default:

- **Performance** — latency/throughput for this feature's specific operations under stated load.
- **Reliability** — behavior on failure: error handling, retries, idempotency, partial-failure recovery.
- **Concurrency** — two actors acting on the same resource at the same time.
- **Security** — authorization checks, input validation boundaries, or rate-limiting specific to this feature's actions.
- **Compatibility** — backward compatibility with existing behavior or consumers, especially when adding to a system already in production.
- **Accessibility** — a behavioral requirement only (e.g. "operable via keyboard/screen reader"), never a visual design detail.
- **Observability** — logging or audit trail, only if this feature is operationally or compliance-sensitive.

## 3. Question Sequence Per Gap — Open Before Closed

For each remaining gap, move through these stages in order:

1. **Open.** Ask one open-ended question in the user's own words.
2. **Probing.** If the answer is vague or partial, sharpen it along whichever of these is actually missing: **Who** (actor), **What** (capability), **When** (trigger/timing), **Where** (context/channel), **Why** (goal), **How** (mechanism/condition).
3. **Closed.** If still unresolved, close with 2-4 concrete suggested options grounded in the input or common patterns, plus "something else".

One question at a time throughout — each answer shapes the next question; never dump a checklist on the user at once.

## 4. Wording

- **Ask about the concrete present or the already-agreed design, not a hypothetical future** — "what should happen when X fails today?" rather than "would you want X to fail gracefully?"
- **Keep questions and options neutral** — no phrasing that implies the expected answer.

## 5. Convergence

- **No vague answer is final** — it goes back through probing/closed.
- **Follow-up cap.** After at most two follow-ups on the same point, stop asking, propose a concrete working decision, and ask for yes/no confirmation instead. This guarantees the interview converges rather than looping.
- **"I don't know" triggers the same fallback** — a proposed decision to confirm, never a blank.

## 6. Throughout

- **Contradictions are surfaced immediately** — not carried silently into the draft.
- **Answers are reflected back for confirmation** before moving to the next section, catching misunderstandings early rather than at final review.
- **Drafting starts only once every section is concrete.** The output step never runs against a partially-answered interview.
