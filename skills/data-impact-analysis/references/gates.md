# Gate Question Formats

Gates are the only planned workflow points where the skill asks the user to resolve decisions or approve changes. Write gate messages in the user's language.

## Rules for every gate

- Batch the questions for that gate into one round.
- Ask only for facts or decisions that materially change the data design and cannot responsibly be derived from the available evidence.
- State the source and decision affected. Show data consequences: structure, integrity, existing data, consumers, compatibility, consistency, or rollout.
- Recommend an option when there is a defensible recommendation based on requirements, project conventions, or referenced design rules. Give a one-line reason. Do not manufacture a recommended answer for a missing required document or unresolved source-of-truth conflict.
- Keep options mutually distinguishable and allow a concise reply by letter or ID.
- If the user authorizes an assumption, restate it, its impact, and residual risk. Do not label it a confirmed fact.
- A gate answer changes only the decision dimensions the user names; if it invalidates earlier decisions, revisit their dependencies.

## Gate 0 — Clarification

Use for missing required inputs, multiple candidate documents, conflicts between specs/model/code, and design-blocking unknowns such as relationship cardinality, optionality, ownership, deletion, retention, state transitions, tenant isolation, uniqueness, or consistency.

Format:

```text
Clarification needed (<n> questions). Reply with one choice per question, or provide the missing reference.

Q1. <Decision topic> (Source: <SRC-ID or source location>)
Why it matters: <The exact design decision this controls>
  a) <Option>: <consequence for model/data/consumers>
  b) <Option>: <consequence for model/data/consumers>
Recommended: <letter>, because <source-backed reason>.
```

For conflicts, cite both sources and say what each states. Do not recommend one side merely because it is easier to implement. For a missing required file or unresolved source-of-truth conflict, ask for the correct input or an explicit authority decision; do not offer an unsupported guess.

A user may say “use your recommendation” only for questions where a defensible recommendation was provided. The skill may proceed with an explicit user-approved assumption for a non-blocking unknown, but cannot waive the absence of the existing System Data Model Document or present an unresolved conflict as settled.

## Gate 1 — Confirm Data Model Changes

Present only new or materially changed DMCs. Each DMC uses the canonical DMC format in `assets/data-impact-template.md` with an additional `Alternatives considered` note for this gate. Include dependencies and classification rationale. For changes involving lifecycle state, include the actual proposed state list and transition table or the complete relevant excerpt, not a vague summary.

Format:

```text
<n> Data Model Changes proposed (<m> Breaking).
The System Data Model Document will be changed only for DMCs you explicitly confirm.

<Summary table and detail blocks for the proposed DMCs>

Recommended: <IDs to accept, with source-backed reasons>. <For each Breaking DMC, state the risk and why the change is necessary, or show the safer additive alternative.>
Reply per DMC: `DMC-01 accept` | `DMC-01 modify: <specific change>` | `DMC-01 reject`; `accept all` is also allowed.
```

Rules:

- Approval is explicit and per DMC. One approved DMC does not approve the rest unless the user says `accept all`.
- A changed DMC is revalidated against requirements, design rules, dependencies, and migration safety; a materially changed definition requires confirmation again.
- If rejection leaves a requirement unmet, state exactly what remains unmet and ask how to proceed. Do not silently invent a substitute DMC.
- Existing DMCs that are already synchronized and semantically unchanged are not resubmitted; verify they are present in the current model before treating them as effective.

## Gate 2 — Confirm output location

Skip this gate only when the user already specified an exact output path and filename. Otherwise propose the default path and ask for a clear decision. If the target exists, never overwrite without explicit confirmation.

```text
Where should the Data Impact Document be saved?
  a) docs/features/<feature-slug>/data-impact.md (recommended)
  b) Another path/name: reply with the exact path
Feature slug: <slug>. Reply `a` or provide a path.

<If the target already exists:>
A file already exists at <path>.
  c) Replace it with this verified document
  d) Save under another path/name
```

## After a gate

Record the answer in the Draft and update affected requirements, source dispositions, DMCs, dependencies, flow diagrams, state diagrams, and cross-references. If the user provides new evidence that conflicts with prior evidence, preserve the discrepancy and resolve it rather than overwriting provenance.
