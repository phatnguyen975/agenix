# Gate Question Formats

Gates are the planned points for clarification and approval. Write questions in the user's language.

## Rules

- Batch questions for each gate.
- Ask only for facts/decisions that change the data design and cannot be derived safely.
- State source, affected decision, and data/consumer/rollout consequences.
- Recommend an option only when evidence supports it. Do not guess missing inputs or settle source conflicts.
- Keep options distinct and allow short replies.
- Record approved assumptions with their basis and residual risk.

## Gate 0 — Clarification

Use for missing required inputs, multiple candidate documents, source conflicts, or design-blocking unknowns (cardinality, ownership, deletion, retention, lifecycle, tenancy, uniqueness, consistency).

```text
Clarification needed (<n> questions). Reply with one choice per question or provide the missing reference.

Q1. <Decision> (Source: <SRC-ID or location>)
Why it matters: <Decision controlled by the answer>
  a) <Option>: <data/model consequence>
  b) <Option>: <data/model consequence>
Recommended: <letter and evidence-based reason, if available>
```

For conflicts, cite both sources. For a missing required file or unresolved source of truth, ask for the correct input or an authority decision.

A user may approve a non-blocking assumption. The user cannot waive a missing System Data Model Document or make an unresolved conflict a confirmed fact.

## Gate 1 — Confirm Data Model Changes

Present only new/materially changed DMCs. Use the template's DMC structure plus alternatives. Include dependencies, classification, rollout, and lifecycle details when relevant.

```text
<n> Data Model Changes proposed (<m> Breaking).
The System Data Model Document changes only after explicit confirmation.

<Summary table and DMC details>

Recommended: <DMC IDs and reasons; explain each Breaking risk or safer alternative>
Reply per DMC: `DMC-01 accept` | `DMC-01 modify: <change>` | `DMC-01 reject`; `accept all` is also allowed.
```

- Approval is explicit and per DMC.
- Revalidate modified DMCs; materially changed definitions need approval again.
- If rejection leaves a requirement unmet, state it and ask for direction.
- Reuse a prior DMC only after confirming semantic equivalence in the current model.

## Gate 2 — Confirm Output Location

Skip only when the user supplied the exact path and filename. Never overwrite an existing file without explicit confirmation.

```text
Where should the Data Impact Document be saved?
  a) docs/features/<feature-slug>/data-impact.md (recommended)
  b) Another path/name: <exact path>
Feature slug: <slug>

<If the file exists:>
  c) Replace it
  d) Save under another path/name
```

## After a Gate

Record the answer in the Draft and update affected requirements, sources, DMCs, dependencies, diagrams, and references. Preserve provenance when new evidence conflicts with earlier evidence.
