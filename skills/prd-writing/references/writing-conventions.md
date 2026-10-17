# Requirement Writing Conventions

## ID Scheme

Every traceable item is numbered and never renumbered once assigned:

| Prefix   | Used for                    |
| -------- | --------------------------- |
| `G-01`   | Goals                       |
| `UJ-01`  | User Journeys               |
| `FR-01`  | Functional Requirements     |
| `NFR-01` | Non-Functional Requirements |
| `CON-01` | Constraints                 |
| `SC-01`  | Success Metrics             |
| `A-01`   | Assumptions                 |
| `D-01`   | Dependencies                |

## Structural Rules

- **Normative keywords, capitalized**: `MUST`, `MUST NOT`, `SHALL`, `SHOULD`, `MAY`. `MUST` / `SHALL` for mandatory, `SHOULD` only for a genuine recommendation (not a disguised mandatory item), `MAY` for truly optional. Example: `FR-01: The system MUST allow a user to reset their password.`
- **One capability per line.** No chaining multiple capabilities into a single requirement; "and" / "or" joining two separate testable conditions is a sign the line should be split into two IDs.
- **Capability-level granularity.** A requirement describes a capability or behavior area, not every validation rule or error state — that depth belongs to a downstream feature spec, not this document.
- **Traceability annotations.** A functional requirement references the journey(s) it supports; a success metric references the goal(s) it measures. This keeps Goals → Journeys → Requirements → Metrics as one connected chain, not four disconnected lists.
- **Journeys, not acceptance criteria.** Narrative flows using the format in `prd-template.md`, not Given/When/Then test cases.
- **No placeholders in output.** A value that can't be quantified yet is pushed back to the user during elicitation, never written as "TBD".

## Clarity Rules

Correct structure alone doesn't prevent ambiguity — the wording itself has to be unambiguous and testable.

These rules apply to every formal, numbered line: Goals, Functional and Non-Functional Requirements, Constraints, and Success Metrics — the lines that commit to something testable. They do not apply to narrative prose (Executive Summary, Problem Statement, Target Users, journey descriptions), where plain language describing a need or pain point is fine — e.g. "members need a fast way to check in" is acceptable context in Target Users, even though "fast" would be rejected inside NFR-01 itself.

- **Active voice, explicit subject.** "The system MUST send a confirmation email" — not "A confirmation email MUST be sent" (unclear what performs the action).
- **Quantify instead of qualifying.** Replace a subjective adjective with a number, threshold, or concrete condition. A requirement that can't be quantified gets pushed back to the user rather than written as-is.
- **One term per concept, used identically everywhere.** If the document calls something "account" in one place, it isn't called "profile" or "user record" elsewhere. Domain-specific terms are defined once in the Glossary.
- **No dangling scope words** ("etc.", "and so on", "among others") — either enumerate the full list, or state the exact rule that decides inclusion.

### Banned Words and Replacements

| Avoid                                             | Problem                                       | Write instead                                                           |
| ------------------------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------- |
| fast, quick, slow                                 | subjective, unverifiable                      | a quantified threshold, e.g. "within 200ms"                             |
| user-friendly, intuitive, easy to use             | not testable                                  | a concrete, observable behavior, e.g. "completable in 3 steps or fewer" |
| robust, reliable, flexible, scalable (used alone) | vague                                         | a quantified NFR, e.g. "99.9% uptime", "handles 1,000 concurrent users" |
| as appropriate, as needed, if necessary           | defers the actual decision                    | the specific rule or condition that applies                             |
| should (for a mandatory item)                     | understates required strength                 | `MUST`                                                                  |
| and / or joining two requirements                 | hides two separate testable items in one line | split into two separate requirement IDs                                 |
| TBD, to be determined                             | unresolved placeholder                        | resolved during elicitation before the file is written                  |
