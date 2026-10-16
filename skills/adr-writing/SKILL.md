---
name: adr-writing
description: Write, review, and maintain Architecture Decision Records (ADRs) — structured documents that capture the reasoning behind a significant technical or architectural decision. Use this skill whenever a decision is hard to reverse, affects system structure, non-functional characteristics (performance, security, scalability, reliability), dependencies, or interfaces, or whenever the user asks to document, record, write up, or explain "why" a technical choice was made — even if they never say the word "ADR". Also use it to update an existing ADR's status, supersede a past decision with a new one, or retroactively document a decision that was made but never written down.
---

# ADR Writing

## Overview

An Architecture Decision Record (ADR) is a short, standalone document that captures one significant technical decision: the problem it responds to, the option chosen, the alternatives that were not chosen and why, and the consequences of going with it. This skill produces ADRs that are consistent, verifiable, and genuinely useful to whoever reads them later — including an agent reading them months from now, trying not to re-decide something that was already settled.

## When to Use

Use this skill for a decision that is **architecturally significant**: it affects the system's structure, a non-functional characteristic (performance, security, scalability, reliability, cost), a dependency, an interface/contract, or the construction technique used to build it — AND it is hard/costly to reverse, had multiple reasonable options, or is likely to be questioned again later. See `references/architectural-significance.md` for the full criteria and worked examples if significance is unclear in a specific case.

This applies regardless of project phase: initial design, mid-sprint, a code review that quietly changes architecture, a post-incident fix, a major refactor, or retroactively documenting a decision that already exists in the code but was never written down.

## When NOT to Use

- The decision is easily reversible, low-impact, or has one obvious answer — writing an ADR for it dilutes the value of the ones that matter.
- The task is to read or summarize existing ADRs rather than write or update one — that's a simpler retrieval task, not this workflow.
- The request is for general design documentation (how a system works) rather than the record of a specific decision (why it was chosen this way).

## Input

| Input                                            | Type        | Required                                           |
| ------------------------------------------------ | ----------- | -------------------------------------------------- |
| Decision title or topic                          | Short text  | Required                                           |
| Context — the problem, constraints, requirements | Text        | Required                                           |
| Chosen option and its rationale                  | Text        | Required                                           |
| Alternatives not chosen, with reasons            | One or more | Required                                           |
| Target directory / existing ADR convention       | Path        | Optional — detect from the repository if not given |
| Fitness-function domain(s), if any apply         | List        | Optional                                           |

If any required input is missing, ask for it or look for it in the repository/conversation before drafting — don't invent context, rationale, or rejected alternatives that weren't actually given or found.

## Output

A single Markdown file following the structure below. The canonical, fully annotated version of this template is `assets/adr-template.md` — use it as the starting point for every draft rather than retyping the structure from memory.

| Section                | Purpose                                                            |
| ---------------------- | ------------------------------------------------------------------ |
| Title                  | `ADR-NNN: <decision>` — names the decision itself, not the problem |
| Status / Date          | A two-line block under the title: current lifecycle state and date |
| Context                | The problem, constraints, and requirements driving the decision    |
| Decision               | The chosen approach and its core rationale                         |
| Alternatives Evaluated | Each option not chosen, with pros, cons, and why it was rejected   |
| Consequences           | Concrete effects of the decision, one per line                     |
| Fitness Functions      | Objective, automatable checks tied to this decision, if any apply  |

**Status values:**

- `Proposed` — drafted and awaiting review; not yet in effect.
- `Accepted` — in effect; this is the current decision.
- `Superseded by ADR-XXX` — replaced by a newer decision; kept for history, no longer in effect.
- `Deprecated` — no longer applies, due to a changed context, without necessarily having a direct replacement.

**Typical flow:** `Proposed` → `Accepted` → (`Superseded` or `Deprecated`). Old ADRs are never deleted — superseding or deprecating one is a status change, not a rewrite.

## Core Principles

- **Detect convention before imposing one.** Scan the repository for an existing ADR setup — a `docs/adr/` or `docs/adrs/` folder, an `.adr-dir` file, a different numbering/heading style — before defaulting to `docs/adrs/ADR-NNN-<slug>.md`. If something different already exists, follow it (or ask, if it's ambiguous) instead of overriding it.
- **Write as Proposed, confirm before Accepted.** Create the file with `Status: Proposed` and surface its path for the human to open and review — never skip straight to `Accepted` without that explicit approval first. Clear intent from the user is not the same as them having reviewed the actual written draft.
- **One ADR, one decision.** Never bundle unrelated decisions into a single file.
- **Never edit an Accepted decision.** To change course, write a new ADR and mark the old one `Superseded by ADR-XXX`. History stays intact; nothing gets silently rewritten or deleted.
- **Alternatives must be real.** Every option in `Alternatives Evaluated` has to be one that was genuinely on the table — not a strawman added to make the chosen option look better by comparison.
- **Keep it short.** A reader should get through an ADR in a few minutes. If a draft is running long, that's usually a sign it's documenting more than one decision.
- **Maintain the index.** If the project keeps an ADR index (e.g. `docs/adrs/README.md`), update it with every new or changed ADR so it stays a reliable table of contents.

## Workflow

1. **Assess significance.** Check the decision against "When to Use" above. If it doesn't clearly qualify, say so and ask whether an ADR is really wanted, rather than writing one by default.
2. **Detect the repository's convention.** Look for an existing ADR directory, index, or numbering style. Use it if found; otherwise, the default is `docs/adrs/ADR-NNN-<slug>.md`.
3. **Gather the missing inputs.** Confirm the problem/context, the chosen option and its rationale, and at least one genuinely considered alternative. Ask rather than assume anything not already stated or evident in the repository.
4. **Compute the file name.** If the default convention applies, run the helper script to get the next number and a slug — it only prints a suggestion, it never writes anything:
   - Linux/macOS: `scripts/next-adr.sh "<title>" [adr-directory]`
   - Windows: `scripts/next-adr.ps1 -Title "<title>" [-Directory <adr-directory>]`

   Pick the script based on the environment the command will actually run in (the human's OS, or the OS of the machine executing the command) — not the skill's own platform. Both scripts implement identical logic and produce identical output for the same input, so either is safe to use once the right one is chosen. They match the `ADR-NNN-<slug>.md` pattern specifically; if step 2 found a different existing convention, follow that project's own numbering/naming pattern by hand instead of using either script.

5. **Draft the ADR** from `assets/adr-template.md`:
   - Title the decision itself, not the question.
   - Write Context objectively — the situation as it stood, without presupposing the outcome.
   - State the Decision and its rationale in one clear statement.
   - Fill in Alternatives Evaluated with real options, each with pros, cons, and a specific rejection reason.
   - List Consequences as concrete, checkable effects — not vague optimism.
6. **Decide on Fitness Functions.** Check whether any domain in `references/fitness-functions.md` genuinely applies to this decision. If one does, define the protected characteristic, automated guard, and failure threshold. If none applies, mark the section "N/A" rather than forcing one in.
7. **Write the file as Proposed and surface it for review.** Create the file at the computed path with `Status: Proposed`, add it to the ADR index with that status if the project keeps one, then print the file path so the human can open and check it. Writing happens now — the `Proposed` status itself signals the draft isn't final yet.
8. **Promote to Accepted only on explicit approval.** If the human approves, update just the `Status` line (in the file, and in the index if present) from `Proposed` to `Accepted`. If they request changes instead, revise the file in place, keep `Status: Proposed`, and surface the path again. Never change the status to `Accepted` without this explicit, separate approval step.

## Anti-Patterns

- Writing an ADR for a decision that's trivial, obvious, or cheaply reversed.
- Padding Alternatives Evaluated with options that were never seriously considered.
- Editing an Accepted ADR's Decision instead of superseding it with a new one.
- Deleting or silently rewriting a past ADR.
- Writing consequences as vague reassurance ("this will improve things") instead of specific, checkable effects.
- Adding a Fitness Function with no objective threshold ("should be fast").
- Setting `Status: Accepted` at write time, instead of `Proposed`, and skipping the human's review of the written draft.
- Imposing this skill's default path/structure on a repository that already has its own established ADR convention.

## Best Practices

- Title the ADR as the decision made ("Use X for Y"), not the question asked ("Should we use X?").
- Write Context and Decision in the present tense, as the reasoning stood at decision time.
- Prefer a small number of genuinely distinct alternatives over an exhaustive list of weak ones.
- Make failure thresholds specific enough that a machine, not a person, can judge pass or fail.
- When unsure whether a consequence belongs, ask: "would a reader be able to tell whether this actually happened?" If not, it's too vague to include.

## Common Rationalizations to Reject

- _"This is a small decision, an ADR is overkill."_ — Size isn't the test; reversibility and impact are. A one-line decision that's hard to reverse still qualifies.
- _"The reasoning is obvious, no need to list alternatives."_ — If it were truly obvious, there would be no decision to record. Write down what made it non-obvious.
- _"I'll just edit the old ADR's Decision to reflect the new choice."_ — This breaks the immutability principle. Write a new ADR and supersede the old one.
- _"The user clearly wants this, I'll mark it Accepted right away."_ — Clear intent is not the same as a reviewed draft. Write it as `Proposed`, surface the path, and wait for explicit approval before promoting it to `Accepted`.
- _"No convention was found, so the default always applies."_ — The default only applies after checking; a quick scan costs little and avoids fragmenting a project's documentation into two inconsistent styles.
- _"There's no obvious metric, so skip Fitness Functions."_ — First check whether a domain genuinely applies; only skip the section when none does, not because defining a threshold takes extra thought.

## Verification

Before presenting a draft, check it against this list:

- [ ] The decision meets the significance criteria — it wasn't written out of habit or because it was asked for by name.
- [ ] The repository's existing convention was checked before defaulting to `docs/adrs/`.
- [ ] The title names the decision, not the problem or the question.
- [ ] Status and Date are present and accurate.
- [ ] Context states the problem objectively, without presupposing the decision.
- [ ] Decision states the chosen approach and its core rationale in one clear statement.
- [ ] At least one genuine alternative is listed, each with pros, cons, and a specific rejection reason.
- [ ] Every consequence is concrete and checkable, not a vague platitude.
- [ ] Fitness Functions are either justified (characteristic + guard + threshold) or explicitly marked "N/A".
- [ ] The file was written with `Status: Proposed` and its path was surfaced for review, rather than skipping confirmation.
- [ ] `Status` was changed to `Accepted` only after the human's explicit approval of the written draft.
- [ ] The ADR index was updated, if the project keeps one — at write time with `Proposed`, and again if the status later changes.
