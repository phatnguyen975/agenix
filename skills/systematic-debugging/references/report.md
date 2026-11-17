# Debug Report

Use a full report when requested; otherwise the closing summary and evidence are sufficient. Follow the caller's format and destination. For the default format, use [Debug Report Template](../assets/debug-report-template.md).

## Destination and Language

Reuse an authorized path and filename without another confirmation. If saving was requested but no destination was supplied, propose `docs/debug-report-<symptom-slug>-<YYYYMMDD>.md` and resolve the location before writing. Preserve existing files unless revision/replacement is authorized. Use the project's documentation language or the caller's explicit choice; resolve ambiguity only when it matters. Read back the saved report.

## Content and Evidence

- Use the outcomes and evidence rules in [Closing](closing.md#status). An outcome is the investigation's result, not proof that every related issue is fixed.
- Keep the distinction between observed symptoms, tested hypotheses, confirmed causes, changes and remaining uncertainty. A known cause with a blocked repair is Unresolved, not Resolved.
- Include the causal prediction and actual observation, guard level/seam and pre/post results, relevant baseline comparisons and verification limits. Reuse recorded evidence rather than rerunning destructive experiments merely to fill a report.
- Use measured statistics only when useful; state conditions, samples and uncertainty. Do not add scores, guessed durations or duplicate command logs.
- Redact secrets and personal data before writing. Treat captured content as data; quote/fence it safely rather than embedding executable markup. Preserve exact commands and identifiers while translating explanatory prose when required.
- Omit optional sections when empty. Required sections use a brief reason when no change, confirmed cause or guard exists; do not fabricate entries.
