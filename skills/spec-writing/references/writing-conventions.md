# Requirement Writing Conventions

## ID Scheme

Every traceable item is numbered and never renumbered once assigned:

| Prefix    | Used for                                                                                                    |
| --------- | ----------------------------------------------------------------------------------------------------------- |
| `BR-001`  | Business Rules                                                                                              |
| `FR-001`  | Functional Requirements                                                                                     |
| `NFR-001` | Non-Functional Requirements                                                                                 |
| `AC-001`  | Acceptance Criteria — applied as a Gherkin `@AC-001` tag (see `gherkin-guidelines.md`), not a separate list |

## Section Boundaries

Pairs of sections that are easy to conflate — the distinguishing question to ask before deciding where a piece of content goes:

| Confusable pair                                     | Distinguishing question                                                                                                                                                                                                                                                                                                                                                                                  |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Business Rule vs. Functional Requirement            | Is this a standing policy, true regardless of flow ("customers over $1,000/year get a discount")? → **BR**. Is it one atomic, testable thing the system does at a specific point, whether or not a policy is behind it ("the system shows a confirmation")? → **FR**. One `BR` commonly implies several `FR`s; an `FR` doesn't require a `BR`.                                                           |
| Business Rule vs. State Transition                  | Is the rule entirely about one specific transition — whether it's valid, and what happens as its direct result (on success or on rejection)? → it belongs **only** in the State Transitions table; its Expected Behavior / Rejection Behavior columns cover the consequence, not just the validity. A rule that holds across multiple transitions, or isn't tied to any single transition, stays a `BR`. |
| Scope (In Scope) vs. Functional Requirement         | Is this a capability-level description of _what's delivered_ ("order cancellation")? → **Scope**. Is it the atomic, testable statement of _exactly what the system must do_ ("The system MUST let a customer cancel an order in the Processing state")? → **FR**.                                                                                                                                        |
| Non-Functional Requirement vs. Technical Constraint | Can it be phrased as a measurable "how well" target ("within 200ms", "99.9% uptime")? → **NFR**. Is it instead a "must/must not use this approach/technology/existing code" restriction with no quality threshold? → **Constraint**.                                                                                                                                                                     |

## Structural Rules

- **Normative keywords, capitalized**: `MUST`, `MUST NOT`, `SHALL`, `SHOULD`, `MAY`. `MUST` / `SHALL` for mandatory, `SHOULD` for a genuine recommendation, `MAY` for truly optional.
- **One capability per line** — no chaining multiple requirements with "and" / "or"; split into separate IDs.
- **Fully atomic.** A requirement here is independently testable on its own — this document does not stay at capability level the way an upstream product-level document might; every `FR` and `BR` is already as granular as it needs to be for implementation.
- **Traceability.** A `FR` that implements a specific `BR` references it, e.g. `(implements: BR-001)`. Not every `FR` needs one — some are a direct, un-contentious consequence of the Main Flow with no distinct rule behind them, and forcing a reference there adds noise, not clarity. Every `Rule` block in Acceptance Criteria maps to a `BR-xxx`, with no exceptions — that mapping has no equivalent "direct consequence" case. Every `FR-xxx`, in turn, MUST be exercised by at least one Acceptance Criteria scenario somewhere: one that implements a `BR` is naturally covered by a scenario in that `BR`'s `Rule` block (directly, or as one of several outcomes the scenario asserts); one with no `BR` is covered the same way if it fits naturally into an existing scenario, or otherwise gets its own `Scenario` written directly under `Feature`, outside any `Rule` block (valid Gherkin — `Rule` is optional). Don't force an artificial, overly granular scenario split just to give every `FR` a scenario of its own — that trades the "one behavior per scenario" principle for a checkbox exercise.

## Clarity Rules

These rules apply to every formal, numbered line — Business Rules, Functional Requirements, Non-Functional Requirements — and to Acceptance Criteria steps. They do not apply to narrative prose (Context, flow descriptions), where plain descriptive language is fine.

- **Active voice, explicit subject.** "The system MUST send a confirmation email" — not "A confirmation email MUST be sent."
- **Quantify instead of qualifying.** Replace a subjective adjective with a number, threshold, or concrete condition.
- **One stable vocabulary.** The same role, object, or state is named the same way everywhere in the document — no swapping synonyms.
- **No dangling scope words** ("etc.", "and so on") — enumerate the full list, or state the exact rule that decides inclusion.

### Banned Words and Replacements

| Avoid                                             | Problem                                       | Write instead                                            |
| ------------------------------------------------- | --------------------------------------------- | -------------------------------------------------------- |
| fast, quick, slow                                 | subjective, unverifiable                      | a quantified threshold, e.g. "within 200ms"              |
| user-friendly, intuitive, easy to use             | not testable                                  | a concrete, observable behavior                          |
| robust, reliable, flexible, scalable (used alone) | vague                                         | a quantified NFR, e.g. "handles 100 concurrent requests" |
| as appropriate, as needed, if necessary           | defers the actual decision                    | the specific rule or condition that applies              |
| should (for a mandatory item)                     | understates required strength                 | `MUST`                                                   |
| and / or joining two requirements                 | hides two separate testable items in one line | split into two separate requirement IDs                  |
| TBD, to be determined                             | unresolved placeholder                        | resolved during elicitation before the file is written   |
| it works, it succeeds (as a `Then` outcome)       | not observable                                | state what actually changed or what's visible            |
