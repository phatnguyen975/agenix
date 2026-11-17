# Requirement Writing Conventions

Write a usable product contract: necessary, clear, consistent, feasible, traceable and verifiable. The [NASA requirements checklist, Appendix C](https://www.nasa.gov/reference/system-engineering-handbook-appendix/) is a useful quality reference, not a requirement to adopt NASA's lifecycle or claim standards compliance. A PRD is not automatically a complete engineering requirements specification.

## IDs and Traceability

| Prefix   | Item                       |
| -------- | -------------------------- |
| `G-01`   | Goal                       |
| `UJ-01`  | User journey               |
| `FR-01`  | Functional requirement     |
| `NFR-01` | Non-functional requirement |
| `CON-01` | Constraint                 |
| `SC-01`  | Success metric             |
| `A-01`   | Assumption                 |
| `D-01`   | Dependency                 |

Allocate unique sequential IDs per prefix within the document. On revision retain existing IDs, never recycle retired IDs and use the next unused number for additions; gaps are valid. Identify the source document as well when referring to inherited IDs so two PRDs' `FR-01` entries cannot be confused.

Journeys support goals; functional requirements normally support journeys; success metrics measure goals. Cross-cutting obligations can reference a goal or constraint directly with a short rationale rather than inventing a user journey. Link quality requirements to the relevant need/source. Check both directions: no unexplained requirement, uncovered in-scope journey, or goal without a success measure. Traceability is a set of justified relationships, not a mandatory linear chain.

## Requirement Strength and Structure

Use the project's normative convention consistently. By default use capitalized `MUST` / `MUST NOT` for mandatory obligations, `SHOULD` / `SHOULD NOT` for genuine recommendations and `MAY` for optional capability. `SHALL` is equivalent to `MUST` if the project uses it; do not imply different strengths. These meanings follow [RFC 2119, Sections 1-5](https://www.rfc-editor.org/rfc/rfc2119.html#section-1); [RFC 8174, Section 2](https://www.rfc-editor.org/rfc/rfc8174.html#section-2) clarifies uppercase usage. This is an adopted document convention, not a claim that a PRD is an Internet protocol standard.

Define the chosen meanings in the generated PRD, for example in Glossary. Goals, metrics and descriptive context need not be forced into normative sentences. A recommendation needs an understandable exception/trade-off; an optional capability must not conceal a mandatory dependency.

Write each requirement as an explicit subject, obligation, observable behavior and relevant condition. Keep one cohesive obligation per ID. Split independently changeable obligations, but do not split a condition from its outcome merely because it contains "and" or "or". Requirements should be individually assessable at PRD depth without expanding into exhaustive downstream test cases.

## Clarity and Verification

- Use active voice, consistent domain terms and bounded actor/state scope. Define ambiguous terms once; distinguish user goals from system obligations.
- Replace vague qualifiers with observable criteria. Verification can use test, demonstration, inspection or analysis; not every valid requirement needs a number. A privacy rule such as "The system MUST prevent one tenant from reading another tenant's records" is categorical, not a latency target.
- For numerical qualities, specify the unit, population, operating conditions and measurement window/percentile where relevant. A latency target without workload or a reliability percentage without a service boundary is incomplete.
- Do not invent targets, feasibility evidence, legal obligations or benchmark claims. Distinguish measured baselines, agreed targets and hypotheses. A new capability has no historical baseline; it does not automatically have a baseline of zero.
- Avoid unbounded lists such as "etc." and subjective terms such as "fast", "intuitive" or "robust" when they replace a criterion. Evaluate meaning rather than banning substrings in identifiers, quotations or explanatory context.
- Keep rationale, evidence and verification notes distinct from the obligation. Reference a constraint once rather than creating competing versions of it across sections.
- Describe required outcomes rather than selecting architecture or a technology by default. Retain a mandated external interface, compatibility condition or implementation constraint when genuinely applicable, stating its authority and rationale.

## Scope and Revision Quality

Keep important exception, denial, recovery and misuse outcomes when they affect product expectations. Avoid exhaustive field validation, API/schema definitions and implementation tasks. PRD-level acceptance/success criteria are appropriate; complete executable scenario suites are outside this document's default depth.

In a feature PRD, identify inherited obligations and the delta. In a revision, assess affected journeys, metrics, assumptions, dependencies and incoming/outgoing references; preserve unrelated wording and IDs. Do not silently reinterpret a previously approved requirement or inherit approval for changed content. Follow project revision metadata conventions and distinguish AI checks from the responsible human's approval.

Use accepted assumptions only for real empirical uncertainty, with impact and validation responsibility. Missing policy choices and mandatory acceptance thresholds cannot be disguised as assumptions. If the required decision cannot be made, report the blocker rather than delivering an apparently complete final document.
