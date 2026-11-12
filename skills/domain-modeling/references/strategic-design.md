# Strategic Design

Use when identifying business capabilities and subdomains, assessing strategic importance, or defining bounded contexts. These are separate decisions: subdomains describe the business problem space; bounded contexts bound coherent solution models. Consult `ubiquitous-language.md` when meanings are ambiguous; use `context-mapping.md` when dependencies need classification.

## Domain, Subdomain, and Bounded Context

| Concept             | Meaning                                                                               | Primary Question                                     |
| ------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **Domain**          | The business subject area and associated knowledge, goals, and rules                  | What business problem is being addressed?            |
| **Subdomain**       | A cohesive part of that business problem, with related capabilities and expertise     | What business responsibility or outcome is distinct? |
| **Bounded Context** | An explicit boundary inside which a domain model and ubiquitous language are coherent | Where does this meaning and set of rules apply?      |

A subdomain can require multiple bounded contexts; a bounded context can model parts of multiple subdomains. Neither the application boundary nor a team boundary proves a bounded context. Existing teams and systems may provide evidence about ownership and change, but they are not definitions of the model boundaries.

## Discover Subdomains

1. Identify business outcomes and capabilities from requirements, scenarios, and stakeholder language. Ask what business value or obligation is served, not which screen, database, or service implements it.
2. Group decisions and activities that serve the same goal and rely on related expertise. Use business rules and change drivers to test cohesion.
3. Separate capabilities when they have substantially different objectives, policies, stakeholders, or change pressures. Do not split by noun, CRUD entity, or technical layer alone.
4. Record each candidate's purpose, scope, key decisions, and evidence. Map material requirements to candidates; mark genuine overlaps explicitly.
5. Test contested boundaries with the responsible domain experts. Explore alternatives as **working hypotheses**, but clarify material ownership or semantic differences before finalizing the context model.

**Illustrative example:** `Pricing` determines applicable prices; `Order Fulfillment` coordinates delivering committed orders; `Customer Support` handles inquiries and exceptions. They are possible subdomains of a retailer, not prescribed bounded contexts or services.

## Classify Strategic Importance

| Type           | Decision Criterion                                                                | Practical Consequence                                          |
| -------------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Core**       | Creates or sustains business differentiation or is central to strategic advantage | Invest modeling effort where evolving rules deliver that value |
| **Supporting** | Required by the business but not a key differentiator; may be business-specific   | Model its real rules, avoiding unnecessary complexity          |
| **Generic**    | Addresses a widely recurring problem with broadly reusable approaches             | Consider reuse while retaining required business controls      |

**Classification is relative to the organization and can change.** A complex system is not automatically core; a straightforward activity may be strategically important. Generic does not mean trivial or that local business constraints can be ignored. Supporting does not mean "custom-built by definition". Build/buy decisions are separate.

**Classification procedure:**

1. Identify goals, differentiators, constraints, and where the organization intends to innovate.
2. For each subdomain, explain why it is core or, if not, whether the business need is specialized supporting work or broadly generic.
3. Record the supporting business evidence and who can confirm the classification.
4. If strategic evidence is missing, use **Undetermined** only during working discovery. Ask for business goals and prioritization when classification is needed for the final model; do not fabricate a Core/Supporting/Generic label from complexity, technology, or vendor availability. If strategic classification is explicitly outside a focused task, omit it rather than leaving a speculative classification.

**Contextual example:** A retailer may classify a proprietary recommendation strategy as Core, internal returns coordination as Supporting, and routine authentication as Generic. A security product company may classify authentication differently.

## Find Bounded-Context Boundaries

Start with responsibilities, decisions, and **context-specific meanings**, then evaluate candidate boundaries against concrete scenarios.

| Signal                  | Investigate                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------ |
| **Language**            | Does a term mean materially different things, or do experts disagree about its definition? |
| **Rules and Authority** | Which business decisions belong together, and who can change or approve them?              |
| **Model and Lifecycle** | Does the same apparent concept have different behavior, states, or identity?               |
| **Change**              | Can one model evolve without constantly coordinating changes to another?                   |
| **Collaboration Cost**  | Would a split create excessive translation, orchestration, or coordination?                |

A single homonym is **not sufficient** to justify two contexts, and a shared business noun is **not sufficient** to merge them. A context may contain multiple related concepts and may serve several subdomains while maintaining a coherent language.

**Boundary procedure:**

1. Describe each candidate context in one business-purpose sentence. State what it owns and explicitly excludes.
2. Define its essential terminology, decisions, business rules, and typical scenarios.
3. Record which subdomains the context serves. Explain meaningful splits or overlaps; do not force a one-to-one map.
4. Walk an end-to-end scenario, noting information it needs from other contexts and where ownership would become unclear.
5. Compare alternatives when a boundary would cause significant shared change, duplicated decisions, or cross-boundary consistency needs.
6. Refine using `context-mapping.md` and `model-validation.md`; confirm material semantic, ownership, and boundary consequences with responsible humans before delivering the design.

**Example:** In `Catalog`, `Product` could mean a sellable commercial offering, including descriptions and availability for selection. In `Warehouse`, the related concept might be a `Stock Item`, with storage and allocation rules. Separate models are useful when their rules and lifecycles genuinely differ; a translation or identifier may connect them without creating one shared `Product` entity.

## External Systems and Coverage

- An external provider, user, or organization may be a **collaborator** without being an in-scope bounded context. Do not create a fake local bounded context just because the business uses an outside service.
- If the external party's model is a significant integration dependency, represent its **external model boundary** distinctly in the context map; do not assert its internal rules or a team relationship without evidence.
- A generic subdomain may be fulfilled by an external provider without a locally modeled context. Record the business capability and responsible collaboration instead.
- Ensure each in-scope capability is covered by one or more bounded contexts or explicitly delegated/excluded. A context should not silently own contradictory definitions from different subdomains.

## Strategic Checks

- Are subdomains framed as business problems rather than modules, tables, or services?
- Is each published classification supported by this business's confirmed goals? Are temporary Undetermined classifications resolved before a full final design?
- Are context purpose, owned decisions, exclusions, and language coherent?
- Is subdomain-to-context coverage explicit, including one-to-many or many-to-one arrangements?
- Do proposed boundaries make known business scenarios and consistency needs easier to reason about, rather than simply mirror the organization chart?
- Are external collaborators separated from contexts whose models are actually in scope?
- Have material boundary and strategic-classification gaps been resolved with authoritative human input before finalizing?
