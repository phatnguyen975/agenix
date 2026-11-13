# Model Validation

Use to validate a new or evolved business domain model **before** publishing the final design, or to review an existing model. Test both **business correctness** (the model matches authoritative intent) and **internal consistency** (its terms, decisions, boundaries, messages, and examples agree). A well-formed diagram or a passing structural check alone does not establish business validity.

## Evidence and Decision Authority

Identify the stated scope, source requirements, scenario references, relevant human decisions, existing model where applicable, and any prior validation evidence.

- **Authoritative input:** explicit approved requirements and confirmations by the relevant business owner/domain expert for the decision. An existing approval can satisfy confirmation; do not ask for redundant sign-off.
- **Supporting evidence:** operations documents, examples, existing code, logs, current system behavior, and previous model versions. These may describe what happens, not what **should** happen.
- **Agent proposal:** a candidate rule, boundary, policy, or guarantee inferred during modeling. It must never be passed off as authorized business policy.
- **Conflicting sources:** do not arbitrarily pick the most recent file or most detailed implementation. Ask the appropriate human to reconcile material differences before finalizing the affected design.

**Materiality test:** Would a different answer change an in-scope business outcome or exception, key term, responsibility/authority, context boundary with business impact, non-negotiable consistency rule, cross-context obligation, or acceptance scenario? If yes, it is a **material clarification**. Ask as soon as discovered, including during intake — not merely at the end. The agent can select a defensible modeling pattern without human approval when it does not invent or change business meaning.

## Clarification and Confirmation Protocol

1. **Identify the decision:** state the gap or conflicting evidence, the affected scenario/model element, and why it matters.
2. **Ask a concrete question:** include options and consequences if useful; do not quietly adopt a suggested answer. Batch tightly related decisions rather than interrupting for trivial details.
3. **Capture the answer:** record the approved rule, meaning, or responsibility and a traceable source (requirement ID, decision record, meeting reference, or explicit in-conversation human response). Approval cannot be inferred from silence.
4. **Reconcile changes:** update affected terminology, ownership, policies, aggregate guarantees, context exchanges, and scenario expectations; check that old evidence is not treated as current after a superseding decision.
5. **Repeat when necessary:** new material gaps can surface at any modeling step. Working candidates may be explored internally, but final design publication remains blocked until affected decisions are resolved.

**Example:** If `OrderConfirmed` can be reached before a stock-reservation reply, ask: "Is confirmation allowed while reservation is pending, or must stock first be reserved? Which outcome is required if stock is refused?" The chosen answer determines the process, refusal behavior, and possibly context responsibilities. Do not invent a compensation policy.

## Scenario Coverage

Select cases that exercise **distinct business decisions and risks**, proportionate to the requested scope. Do not turn every type into a mandatory diagram.

| Scenario Type                 | What to Check                                                                         |
| ----------------------------- | ------------------------------------------------------------------------------------- |
| **Happy Path**                | Actor, preconditions, decision authority, accepted action, required outcome           |
| **Alternative / Refusal**     | Exceptions, invalid action, reason for refusal, effect on existing state              |
| **Lifecycle / Time**          | Allowed transitions, deadline meaning, expiration or delayed responses                |
| **Consistency / Concurrency** | Competing decisions, repeated actions, stale information, hard invariant preservation |
| **Cross-Context / Failure**   | Model translation, ownership, denied or delayed collaboration, partial completion     |
| **Regression**                | Previously accepted behavior and downstream effects changed by evolution              |

## Walk Through Each Scenario

1. **Source and setup:** requirement or confirmation reference; actor/trigger; starting business state and relevant facts.
2. **Business intention:** action/command or decision and the context that owns it. Do not create a command or aggregate class solely to satisfy a checklist.
3. **Decision and guard:** supported eligibility/preconditions, business rule, invariant, external authority, and where each is enforced or evaluated.
4. **Outcomes:** accepted result, applicable refusal/exception, meaningful business event if established, and any subsequent policy.
5. **Collaboration:** required facts and exchanges; ownership of translations; acceptable information freshness and failure behavior where important.
6. **Consistency:** evaluate concurrent, repeated, or partial operations when a hard business guarantee depends on them. A preliminary query is not by itself an atomic guarantee.
7. **Result:** classify as **Pass**, **Fail**, **Blocked**, or **Not in Scope**, explain evidence and required action. Repeat affected scenarios when a rule, boundary, or answer changes.

**Illustrative working trace:**

```text
Scenario: Confirm Order Requiring Stock
Evidence: REQ-12
Ordering: ConfirmOrder → accept or refuse
Warehouse: ReserveStock → reserved or refused
Unresolved decision: Can Ordering confirm before reservation succeeds?
Result: Blocked until the responsible business owner clarifies the timing rule
Action: Ask owner; do not publish the design or infer an eventual policy
```

The scenario is illustrative only. A working `Blocked` trace belongs in analysis or a review report, **never** in the final domain model.

## Semantic Review

| Dimension                  | Typical Defect                                                                  |
| -------------------------- | ------------------------------------------------------------------------------- |
| **Authority and Evidence** | Unapproved rule presented as business fact, conflicting source ignored          |
| **Language**               | Important term contradicts its context definition or another cited scenario     |
| **Responsibility**         | No owner for a decision; two incompatible authorities for one outcome           |
| **Strategic Coverage**     | Business capability omitted, or subdomain confused with a service/context       |
| **Context Map**            | Influence mistaken for message direction or an unsupported relationship pattern |
| **Tactical Model**         | Aggregate/entity/service selected to mirror implementation rather than rules    |
| **Consistency**            | Global guarantee asserted without an authoritative decision or viable boundary  |
| **Behavior**               | Missing or invented refusal, exception, deadline, event, or reaction            |
| **Evolution**              | Updated rule contradicts unaffected terms, messages, or regression scenarios    |

For domain-specific corrections, load only the relevant guide: `ubiquitous-language.md`, `event-discovery.md`, `strategic-design.md`, `context-mapping.md`, `tactical-design.md`, or `aggregate-design.md`.

## Final Design Release Gate

Release a final model for the agreed scope only when **all** applicable gates pass:

1. **Business authorization:** all material in-scope ambiguities and conflicting evidence have been resolved by an appropriate human or explicit prior approved requirement; important decisions have traceable confirmation.
2. **Model correctness:** required capabilities, rules, ownership, meanings, and boundaries reflect that authority. Proposed modeling choices do not smuggle in new business policies.
3. **Scenario acceptance:** required in-scope scenarios **Pass**; no material **Fail** or **Blocked** result remains. Nonapplicable cases are explicitly outside scope rather than silently assumed to pass.
4. **Consistency:** known cross-context exchanges reconcile with both sides; actual hard guarantees survive relevant concurrency/failure reasoning; optional patterns are not added for completeness.
5. **Completeness of meaning:** the delivered model represents agreed business semantics with no unresolved material question, pending approval, tentative rule, or fictitious example. Keep the working validation record separate from the business model and retain traceability to authoritative sources where important.

**If a gate fails:** clarify the missing decision or correct the evidenced model defect, then rerun affected checks. Do **not** publish an incomplete final design or overwrite an accepted model with an unconfirmed change. Keep provisional hypotheses separate from finalized business claims. If a preview is requested, identify its provisional nature and limits; never present it as the completed design.

**Acceptance is scoped, not permanent:** a new or changed business rule can affect previous design decisions. Evolution rechecks those parts and regression scenarios; unrelated confirmed material remains intact.

## Review and Evolution Results

- **Review-only:** return findings ordered by impact. For each give **location → finding → supporting evidence → impact/severity → correction or decision needed**. A review may identify unresolved issues; its findings do not establish that the assessed model is correct. Do not edit without authorization.
- **Evolve:** inspect the original, establish changed business intent, trace impact, confirm material decisions, test affected and regression scenarios, then update the file only after the release gate passes. If blocked, leave the existing file untouched and request clarification.
- **Focused:** validate the requested slice and its material dependencies. Do not treat the entire domain as accepted merely because one aggregate or terminology change passes.

At handoff, briefly communicate the checked scope, major evidence, scenario results, and meaningful limitations **separately from the domain model**. Validation results and review findings describe the assessment, not the business design itself.
