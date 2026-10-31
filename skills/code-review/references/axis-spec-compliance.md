# Axis: spec-compliance

## Purpose

Verify that the change satisfies the applicable, explicit requirements and non-goals without silently inventing product behavior.

## Method

1. Identify authoritative Spec sources supplied by the user or clearly associated with the change. Record source path, section, version/commit, and precedence when sources conflict.
2. Extract atomic, testable requirements: behaviors, acceptance criteria, constraints (including security, performance, compatibility, and operational constraints), and explicit non-goals. Assign stable IDs `R1`, `R2`, etc.
3. Map each requirement to changed code, relevant unchanged code, and tests. Do not infer a requirement from implementation, a commit message alone, or a function name.
4. Trace acceptance criteria and examples through the implementation, including boundary values, error behavior, permissions, and state transitions.
5. Classify each requirement using the status vocabulary below.
6. Identify behavior that is explicitly outside scope or contradicts a stated non-goal. Do not call every undocumented behavior "scope creep"; when the spec is silent, list it as uncovered behavior or ask a Question if its acceptability matters.
7. If a requirement is ambiguous or authoritative sources conflict, record a Question. Report a finding only for a demonstrable conflict with an unambiguous requirement.
8. Quote the smallest useful spec excerpt for every finding and identify its source and section.

## Status Vocabulary

- **Implemented:** all stated conditions are satisfied by the implementation.
- **Partial:** at least one stated condition or case is missing, while some are implemented.
- **Missing:** no implementation for the requirement is present in the reviewed change or its relevant context.
- **Incorrect:** implementation exists but contradicts the requirement.
- **Not verifiable:** code review cannot establish the requirement (for example, a production business metric or external operational property).
- **Violated:** use only for an explicit non-goal that the change contradicts.

## Axis Extras

Return a traceability table in the result:

| Req | Atomic Requirement                                  | Status                                                                    | Evidence                                             |
| --- | --------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------- |
| R1  | <quoted or paraphrased requirement (file, section)> | <Implemented / Partial / Missing / Incorrect / Not verifiable / Violated> | <changed path:lines, test, or reason not verifiable> |

Also list behavior not covered by the spec with `path:lines`. This list is descriptive, not automatically a finding.

## Severity Guidance

- Missing/incorrect core requirement or explicit non-goal affecting safety, data, access, or a public contract — Critical or High.
- Material requirement partially met — High or Medium according to impact and likelihood.
- Minor acceptance gap — Medium or Low.
- Unspecified behavior — not a finding unless it clearly exceeds explicit scope or conflicts with a stated constraint/non-goal.

## Boundaries

- General logic defects not tied to a requirement belong to correctness.
- Project rule violations belong to standards-compliance.
- Missing tests belong to testing; keep the requirement's implementation status here.
- Do not infer requirements from code or reviewer preference.
