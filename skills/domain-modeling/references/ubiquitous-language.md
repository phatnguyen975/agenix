# Ubiquitous Language

Use when discovering or maintaining the shared language of domain experts and modelers, particularly where business terms affect responsibilities, decisions, or boundaries. A **ubiquitous language** is a continually refined, **model-based language within a bounded context**, not a globally enforced dictionary or a list of class names.

## Language Rules

- Use domain experts' own concepts wherever possible. Test proposed definitions in business conversations and concrete scenarios; the language should become precise enough to expose ambiguity in the model.
- Scope meaning to the **bounded context**. The same word may have different meanings across contexts, and related concepts may have different names. Record material translations instead of forcing uniformity.
- Define concepts by business meaning, identity, relationships, and constraints where relevant — not merely by UI fields, database attributes, or synonyms.
- Prefer one **preferred term per meaning** within a context; retain legitimate aliases and distinguish related but non-equivalent terms.
- Reflect the same terminology in business rules, decisions, commands, events, policies, and examples. Naming conventions are secondary to actual business language.
- During discovery, label incomplete meanings **Proposed** or **Unresolved** in working notes; ask the human about material distinctions before publishing. A final model uses only sufficiently confirmed, precise definitions, never an invented meaning that settles a boundary dispute.

## Discover and Define Terms

1. Extract material **nouns** (actors, entities, value concepts, quantities), **verbs** (business actions), **states**, and **occurrences** (candidate domain events) from provided evidence.
2. Describe each term in one or two sentences using business meaning and distinguishing conditions. A definition should help someone decide whether a real example qualifies.
3. Look for synonyms (two names, one concept), overloaded words (one name, several concepts), and near-neighbors (similar but meaningfully different concepts).
4. Ask experts responsible for the context to resolve disputed material meanings as soon as they arise. Preserve the original wording and source in working analysis; put only the confirmed definition in the final glossary.
5. Choose a preferred term and scope. Capture aliases, counterexamples, and cross-context translations when they materially clarify decisions.
6. Update all dependent model elements when a definition changes. Recheck affected scenarios and externally understood terms.

**Definition quality:** For each important term, establish its **bounded-context scope**, preferred name, precise meaning, and any material aliases, contrasts, or translations. Scope can be implicit when the containing model is already unambiguously identified. Avoid large dictionaries of ordinary words or repeated metadata that does not help distinguish business meaning.

## Meaning and Identity Examples

| Term       | Context   | Illustrative Meaning                                      |
| ---------- | --------- | --------------------------------------------------------- |
| Product    | Catalog   | Offering a buyer may select, with commercial descriptions |
| Stock Item | Warehouse | Item type managed for storage and inventory allocation    |
| Customer   | Ordering  | Party that places or owns an order                        |

`Product` and `Stock Item` might refer to related real-world things without being the same domain object. A business identifier connecting them is not proof of shared semantics.

**Synonym or distinction:** If domain experts use `Buyer` and `Customer` interchangeably in Ordering, document one preferred term and the other as an alias. If `Buyer` pays while `Customer` owns the account, they are distinct roles — even if some people fill both roles.

**Definition with a counterexample:** `Active Reservation` might mean "a confirmed hold that has not expired or been canceled". A merely requested hold is **not** active. This is illustrative only; do not adopt the rule without business evidence.

## Naming Domain Behaviors

| Element            | Meaning                                                                            | Example                                |
| ------------------ | ---------------------------------------------------------------------------------- | -------------------------------------- |
| **Command**        | A request to try a business action; success is not guaranteed                      | `ConfirmReservation`                   |
| **Domain Event**   | A business-significant occurrence expressed as an established fact                 | `ReservationConfirmed`                 |
| **State**          | A meaningful condition that may constrain actions                                  | `Confirmed`                            |
| **Policy**         | A conditional business reaction to a known trigger                                 | `When ReservationExpires, ReleaseHold` |
| **Domain Service** | A domain calculation or decision not naturally owned by one entity or value object | `PremiumCalculation`                   |

Imperative commands and past-tense events are useful conventions, **not strict English syntax**; follow the project's business language. A state predicate such as `ReservationIsOverdue` is not automatically an event, and a technical operation such as `UpdateRow` is not usually a domain event. Do not rename established business terminology merely to fit PascalCase.

## Cross-Context Translation

When contexts exchange business meanings:

1. Identify each context's **own term and definition**, including differences in lifecycle, precision, or authority.
2. State which concepts can be translated and what information or meaning may be lost. Do not assume fields with the same name have identical semantics.
3. Decide who interprets incoming meaning; use `context-mapping.md` when a model-protecting translation or a shared published vocabulary is material.
4. Record translation in the dependency description or terminology notes. Internal renames do **not automatically** change published message meaning or external contracts.

**Illustrative translation:** Warehouse's `Available Units` may exclude reserved inventory, while Ordering's `Sellable Quantity` may also consider sales restrictions. Treating these counts as identical would silently move business decisions across contexts.

## Language Quality Checks

- Can an expert distinguish similar concepts and apply the definitions to concrete examples?
- Is each important word unambiguous **within** its context, even if it has different meanings elsewhere?
- Are aliases distinguished from concepts with genuinely different rules or identities?
- Do commands, events, policy names, states, rules, and scenarios use coherent terminology?
- Are important translations evidenced, and have high-impact terminology disputes been resolved before final delivery?
- Has a changed meaning been traced to affected rules, boundaries, processes, and communications?
