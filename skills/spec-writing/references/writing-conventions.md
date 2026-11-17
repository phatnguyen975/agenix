# Requirement Writing Conventions

## IDs and Coverage

Use the existing project's scheme when supplied; defaults are `BR-001`, `FR-001`, `NFR-001` and `AC-001`. Allocate unique IDs per kind within the document. Preserve existing IDs through revisions, append new IDs and do not reuse retired ones; gaps are valid. Qualify external IDs with their owning document.

For Gherkin, the authoritative AC ID is a unique `@AC-001` tag on a `Scenario` or `Scenario Outline`. Outline rows are cases of that outline, not separate AC IDs. A coverage table references those IDs rather than defining a second independent AC inventory. A caller-selected notation retains equally stable acceptance references.

Every FR is illustrated by at least one concrete acceptance scenario; one cohesive scenario may cover several related FRs. Identify that relationship explicitly using the Acceptance Criteria coverage table or an equivalent supplied mapping. Do not split a meaningful example merely to create one scenario per FR. Every BR has relevant acceptance examples; each Gherkin `Rule` names the BR it illustrates. Requirements without a BR still need scenarios and a clear source in scope/flow or an external contract. Cross-cutting scenarios can reference other applicable rules without duplicating them.

State coverage includes relevant successful transitions, failed guards/rejected events and their consequences. Reference rows by unambiguous state/event/guard when no row IDs exist. For NFRs, specify relevant conditions, a threshold or observable criterion and an assessment basis, such as measurement, inspection or analysis. Concrete examples can illustrate a quality concern, but must not replace its full criterion or conditions.

## Section Ownership

| Content                                                           | Authoritative Location                       |
| ----------------------------------------------------------------- | -------------------------------------------- |
| Purpose and inherited decisions                                   | Context, with exact upstream references      |
| Included/excluded capabilities                                    | Scope                                        |
| Actor responsibilities, prerequisites and main sequence           | Actors and Flow                              |
| Domain policy governing behavior                                  | Business Rules                               |
| One cohesive, individually assessable system obligation           | Functional Requirements                      |
| State/event/guard validity and direct success/rejection effects   | State Transitions                            |
| Verifiable quality criteria under stated conditions               | Non-Functional Requirements                  |
| Mandated technology, compatibility or implementation restriction  | Technical Constraints, with source/rationale |
| Concrete examples and their coverage links                        | Acceptance Criteria                          |
| Consulted/required external artifacts and exact relevant sections | References                                   |

A BR can govern one or several flows; it need not apply everywhere to qualify as a domain policy. If a policy is entirely captured by one transition row, keep it there and reference it instead of restating it as a BR. An FR can require support for the operation and reference its transition policy without repeating its guards and effects. Wider policies remain BRs referenced by relevant rows. Derived examples are useful repetition, not a second normative owner.

Security, accessibility and reliability concerns can impose both functional obligations and quality criteria. Classify by what the statement requires, not merely its category name. Keep wire/schema/visual detail in the owning external artifact and reference the behavioral consequence here. Do not invent a reference to a file that does not exist; a blocking missing contract remains explicit.

## Requirement Wording

Follow the project's normative convention; by default use `MUST` / `MUST NOT` for mandatory obligations, `SHOULD` / `SHOULD NOT` for recommendations and `MAY` for optional capability. `SHALL` is equivalent to `MUST` when used. The meanings are adapted from [RFC 2119, Sections 1-5](https://www.rfc-editor.org/rfc/rfc2119.html#section-1) and [RFC 8174, Section 2](https://www.rfc-editor.org/rfc/rfc8174.html#section-2); define the convention briefly in Context when using it.

- State an explicit subject, obligation, condition and observable result. Each requirement has one cohesive assessable intent; split independently changeable obligations, not every sentence containing "and" or "or".
- Use stable domain terms and explicit actor/state scope. Replace vague qualifiers with concrete conditions or observable criteria. Not every valid requirement is numerical: an authorization prohibition can be categorical.
- Numerical targets need units, workload/population, percentile and window where relevant. Do not invent precision, feasibility evidence or thresholds.
- Keep rationale, normative text and assessment notes distinguishable. Avoid unbounded "etc." lists and unobservable outcomes such as "it works". Judge meaning rather than banning substrings in identifiers or narrative.
- Retain consequential failure and recovery behavior without selecting unnecessary implementation mechanics. External interfaces can be legitimate observable boundaries; reference detailed contracts rather than reproducing them.
- Revisions preserve unrelated content, IDs and prior decisions. Update actual Revision/Last Updated and review provenance under the project's convention; changed content does not inherit approval.

## Final Readiness

Complete the feature's behavioral decisions before final delivery. No unresolved instruction placeholder or unapproved assumption may masquerade as a requirement. Review the document for behavioral consistency, coverage, clear ownership, correct references and the selected presentation format. Keep the written agreement and stakeholder approval state distinct.
