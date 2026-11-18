# Data Impact

<!-- Use this template for a full standalone report. Follow the caller's
     format when supplied. Replace placeholders and remove authoring comments.
     Link requirements and evidence where used. Add detail only where it
     changes a decision or verification obligation. -->

## Scope and Baseline

- **Change and Scope:** <Feature or change, relevant requirements, owned stores and affected consumers>
- **Baseline:** <Revision, snapshot, or approved design reference and the evidence that describes affected structures>
- **Limits:** <Unexamined consumers, uncertain evidence, or material discrepancies, when applicable>

## Data Impact

<!-- Combine actions that share data, enforcement, and failure semantics.
     Link exact structures and existing keys where applicable. Include new read
     or write behavior even if no structural change is needed. -->

| Requirement / Source       | Operation and Data                                                      | Disposition                                                                     |
| -------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| <Stable ID or source link> | <Read, write, derive, or retain; affected structure and access pattern> | <Supported as-is, proposed change linked below, or unresolved with consequence> |

<!-- Describe relevant constraints, lifecycle, tenancy, retention, consistency,
     or failure behavior when a table cell is insufficient. Use a transition
     table or diagram when it materially improves understanding. -->

## Model Changes and Rollout

<!-- Use this section for structural changes, existing-data conversion, or a
     change that needs coordinated rollout. Otherwise omit it.
     Repeat the following record only for material changes. Group changes that
     must roll out together. -->

### <Change ID or title>

- **Before and After:** <Exact affected object and proposed shape or semantics, with reason>
- **Consumers and Compatibility:** <Affected readers and writers, existing data, and compatibility of supported versions>
- **Owner and Prerequisites:** <Owning change, dependencies, and evidence needed before reliance>
- **Rollout and Recovery:** <Applicable stages, backfill or existing-data treatment, cutover, safe recovery, and irreversible point>
- **Decision and Integration:** <Proposed, approved, or blocked. Link the decision or evidence needed. Cite integration evidence separately when available>

## Verification and Open Decisions

- **Checks and Evidence:** <Required checks and expected results. Separately link actual executed evidence and implementation artifacts when available>
- **Open Decisions:** <Decision, consequence, and evidence or answer needed, when applicable>
