# Answer Resolution

Use this reference when replies are vague, partial or delegated. Judge whether the answer supports the decision at hand, rather than policing particular words or demanding unnecessary precision.

## Recognize a Usable Answer

- A specific choice, accepted recommendation or deliberate range can resolve a question. "Probably email" may be concrete enough if it clearly expresses the user's choice; hedging alone does not invalidate it.
- "Sounds good" can accept an unambiguous concrete proposal. It cannot resolve several incompatible options or unanswered questions at once.
- "Follow our standard" is usable when the applicable standard is identified, available and resolves this choice. An unspecified "best practice" is not a concrete policy.
- A partial reply resolves only the questions it actually answers. Conflicting replies require clarification of the affected choice, not a restart of settled topics.
- Preserve the answer's qualifiers and scope in the summary. Selecting part of a suggested option does not accept its other details. Do not silently add exceptions, actors or permissions from convention; if an omitted detail materially affects the decision, keep that detail open or clarify it before claiming resolution.
- "You decide" delegates the specified choice within existing authority. Choose a defensible option, record the delegation and rationale, and retain any required external approval. If evidence or authority is insufficient, report the remaining gap.

## Follow Up Proportionately

Ask one targeted follow-up when needed, using the user's terms and explaining the consequence of ambiguity. Offer a few meaningful alternatives if that helps; avoid a false binary. Accept the answer once it is actionable, including intentional flexibility.

If it remains unresolved, do not turn repeated questioning into pressure or silently select a material default. Explain the impact, keep it open and pause dependent work. Other independent questions can still proceed. If the user asks to stop, summarize immediately rather than requiring another answer.

## Example

**Question:** "When two users edit the same record, may the later save overwrite the earlier one, or must we detect and resolve the conflict?"

**User:** "Use the standard approach."

**Follow-up:** "Is there an existing conflict policy we should follow? Otherwise, are lost concurrent edits acceptable for these records? Overwriting is simpler; detecting conflicts adds a recovery step but avoids silent loss."

**User:** "Lost edits are not acceptable. Detect the conflict and ask the editor to reconcile."

**Decision:** Detect concurrent-edit conflicts and require reconciliation, based on the user's no-silent-loss requirement. This resolves the product policy, not the implementation mechanism; technical details still follow applicable constraints and evidence.
