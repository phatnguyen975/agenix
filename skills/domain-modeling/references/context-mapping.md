# Context Mapping

Use to explain **how bounded contexts influence or collaborate with one another**, and how their distinct domain models remain coherent. A context map is not an API diagram, message broker diagram, or a rule that every pair of contexts must communicate. Identify actual business dependencies before choosing patterns.

## Relationship Direction and Dependency

| Relationship            | Business Meaning                                                                  | Representation          |
| ----------------------- | --------------------------------------------------------------------------------- | ----------------------- |
| **Upstream/Downstream** | Upstream choices about a model or contract affect downstream integration          | `Upstream → Downstream` |
| **Mutually Dependent**  | The parties must coordinate important model/delivery decisions                    | `A ↔ B`                 |
| **Independent**         | No material model dependency is identified or integration is deliberately avoided | No connecting edge      |

**Arrow direction expresses influence, not message travel.** For example, `Ordering` may send a stock availability query to `Warehouse`, while `Warehouse` remains upstream because its stock model and contract constrain Ordering. An interaction can contain multiple dependencies with different directions: describe them explicitly rather than assign one artificial global direction.

A context map also reflects **organizational relationships**. Do not infer a partnership, negotiated customer/supplier relationship, or shared ownership merely from an API call.

## Context-Mapping Patterns

| Pattern                           | Applies To                                | What It Means                                                                                       |
| --------------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **Partnership**                   | Mutually dependent parties                | Both coordinate plans and changes to achieve a common outcome                                       |
| **Shared Kernel**                 | Mutually dependent models                 | A deliberately small, shared model portion has joint ownership and change discipline                |
| **Customer/Supplier Development** | Upstream supplier and downstream customer | Upstream gives downstream needs genuine planning influence                                          |
| **Conformist**                    | Downstream model                          | Downstream adopts upstream concepts because translation or negotiation is not justified or feasible |
| **Anti-Corruption Layer (ACL)**   | Downstream model                          | Downstream translates a foreign model into its own, protecting local language and rules             |
| **Open Host Service (OHS)**       | Upstream integration boundary             | An established, explicit service/protocol is offered for integration with multiple clients          |
| **Published Language (PL)**       | Interchange boundary                      | An explicitly defined shared exchange language separates external communication from private models |
| **Separate Ways**                 | Deliberately independent parties          | Avoid integration where its business cost outweighs the benefit                                     |
| **Big Ball of Mud (BBOM)**        | Existing poorly bounded model             | Descriptive legacy condition to contain or improve, not a desirable integration design              |

**Patterns are not nine mutually exclusive labels.** They characterize different dimensions. For example, an upstream may use `OHS + PL` while a downstream uses an `ACL`; `Shared Kernel` can coexist with close coordination. Do not combine contradictory downstream choices such as `Conformist` and `ACL` **for the same model translation** without identifying separate interfaces or use cases. `BBOM` describes an observed model condition, not an automatic relationship between two clean contexts.

## Select the Relationship

1. **Name the dependency:** Which specific decision, terminology, process, or exchange makes one context depend on another? Which parties are responsible?
2. **Determine influence:** Identify whose concepts and changes constrain whom; distinguish this from the direction of individual commands, queries, and notifications. Treat uncertain direction as a working hypothesis; ask humans when its business/organizational consequences are material.
3. **Choose collaboration patterns where justified:** `Partnership` or `Customer/Supplier Development` requires evidence about coordination and real influence. `Shared Kernel` needs explicit joint ownership of a small common model; merely using a shared library is insufficient.
4. **Choose the downstream model stance:** If its model is protected by translation, describe `ACL`. If it deliberately adopts the upstream language, describe `Conformist`. Do not force either without evidence.
5. **Describe upstream publication only when warranted:** Use `OHS` for an established integration offering, `PL` for an agreed exchange vocabulary. Distinguish a modeling recommendation from an existing collaboration; clarify material obligations before finalizing it.
6. **Record deliberate non-integration only when relevant:** Omit unrelated pairs; document `Separate Ways` where not integrating is a meaningful decision.
7. **Validate with scenarios:** Check ownership, translated meaning, failure behavior, and whether the selected pattern reflects actual stakeholder relationships.

## Business Messages across Boundaries

Model **business interactions**, not transport, payload, API endpoint, or queue details.

| Kind                   | Business Meaning                                                    | Example              |
| ---------------------- | ------------------------------------------------------------------- | -------------------- |
| **Command**            | Request that a collaborator attempt an action, which may be refused | `ReserveStock`       |
| **Query**              | Request information without intentionally changing business state   | `CheckAvailability`  |
| **Event Notification** | Communicate that a business-significant fact occurred               | `OrderPlaced`        |
| **Result / Reply**     | Answer a command or query when its meaning matters                  | `AvailabilityResult` |

A **domain event** describes an occurrence in a context's internal domain model. A published **integration event / event notification** represents a fact communicated outside its boundary. They may align, but need not share internal names, detail, timing, or contract. A query response is not automatically a domain event.

For each confirmed, material business message:

1. Identify its kind and business meaning: a **Command** requests an action, a **Query** requests information, an **Event Notification** reports a fact, and a **Result/Reply** returns a meaningful outcome. A refusal is an outcome unless the business explicitly recognizes and communicates it as a fact.
2. Identify the **sender and recipient**, including external systems when relevant. State **Inbound** or **Outbound** relative to the context being examined; an action initiated inside a context is not automatically a cross-boundary message.
3. Identify the required **request/reply or accepted/refused semantics**, when supported by business evidence. Do not infer delivery, synchronization, or transport guarantees from a domain-level exchange.
4. Identify **translation and decision ownership** where the participants use different meanings. A notification or query response does not transfer business authority by itself.
5. Cross-check **both sides** whenever the sender and recipient are in-scope bounded contexts. Names may differ across the boundary, but their documented meanings, directions, and expected outcomes must reconcile.

External systems can participate without a modeled internal context. A Shared Kernel denotes jointly owned model elements, not a message. A direct user action is not automatically a context-to-context exchange. Do not invent messages simply because a relationship exists.

## Example: Downstream Query to Upstream

**Illustrative domain choice:** `Warehouse` defines available stock; `Ordering` uses a different concept, sellable availability, and must translate Warehouse's meaning.

| Context Relationship | Influence          | Patterns       | Business Dependency                                                    |
| -------------------- | ------------------ | -------------- | ---------------------------------------------------------------------- |
| Warehouse → Ordering | Warehouse upstream | ACL (Ordering) | Ordering consults stock availability but applies its own selling rules |

```text
Ordering → Warehouse: CheckAvailability (Query)
Warehouse → Ordering: AvailabilityResult (Reply)
Ordering: Translate available stock into sellable availability
```

The **message query goes downstream-to-upstream**, despite the upstream model influence going the other way. `OHS` or `PL` should be recorded only if evidenced or explicitly proposed; this example does not prescribe networking, timing, or schema choices.

## Mapping and Review Checks

- Does each mapped dependency have a business reason, known parties, and an appropriate scope?
- Are arrow direction, collaboration posture, and message direction kept distinct?
- Does each final pattern represent a justified design arrangement, without asserting unconfirmed partnerships, contract authority, or shared ownership?
- Are distinct context meanings and translations explained without collapsing the models?
- Do the sender's and recipient's accounts of each cross-context business message agree on direction, meaning, and material response?
- Are independent contexts shown without invented edges or mandatory `Separate Ways` rows?
- Are external providers or legacy boundaries explicitly distinguished from locally owned bounded contexts?
- Have material translations, failure obligations, and collaboration responsibilities been clarified with humans before final delivery?
