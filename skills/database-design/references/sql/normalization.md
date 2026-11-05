# SQL Normalization

Use normalization to make relational facts unambiguous, reduce avoidable redundancy, and prevent insertion, update, and deletion anomalies. Base normalization decisions on functional dependencies, candidate keys, multivalued dependencies, join dependencies, and confirmed business rules rather than targeting a normal form mechanically.

## Process

1. Identify candidate keys and functional dependencies from attribute semantics and confirmed business rules (`X → Y` means `X` functionally determines `Y`).
2. Identify all candidate keys, distinguish superkeys from candidate keys, and classify attributes as prime (belonging to at least one candidate key) or non-prime.
3. Identify applicable multivalued dependencies (`X ↠ Y`) when the domain rules indicate independent multi-valued facts.
4. Test the relation against the relevant normal forms using all candidate keys and applicable dependencies, not only the declared primary key.
5. Decompose only when the decomposition is lossless and its dependency-preservation and constraint-enforcement properties are acceptable.
6. Verify that required business rules remain enforceable through database constraints, triggers, transactions, or explicitly owned application-level validation.
7. Document deliberate exceptions, historical facts, derived data, and any duplicated stored values, including their source of truth and consistency requirements.

## Normal Forms

| Form | Core Condition                                                                                                                                         | Typical Issue                                                                                                                                           | Typical Treatment                                                                                                         |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 1NF  | Each attribute value is atomic with respect to its defined domain; no repeating groups or delimited sets representing independently meaningful values. | `customer.phones = '555-0101,555-0102'` when phone numbers are independently meaningful facts.                                                          | Represent independently meaningful phone numbers as separate rows in a related relation.                                  |
| 2NF  | In 1NF; every non-prime attribute is fully functionally dependent on every candidate key, not merely a proper subset of a candidate key.               | `order_items(order_id, product_id, product_name)` when `(order_id, product_id)` is a candidate key and `product_id → product_name`.                     | Keep product facts with the product; retain event-time product snapshots separately when required by the business domain. |
| 3NF  | For every non-trivial functional dependency `X → A`, `X` is a superkey or `A` is a prime attribute.                                                    | `employee_id → department_id` and `department_id → department_name`, where the department name is a fact about the department rather than the employee. | Represent department facts once and reference the department from employees.                                              |
| BCNF | For every non-trivial functional dependency `X → Y`, `X` is a superkey.                                                                                | A determinant that is not a superkey remains in the relation, even though 3NF is satisfied.                                                             | Decompose when the result is lossless and the loss of dependency preservation, if any, is acceptable.                     |
| 4NF  | For every non-trivial multivalued dependency `X ↠ Y`, `X` is a superkey.                                                                               | Independent employee skills and languages are stored as combinations in one relation.                                                                   | Separate independent multi-valued facts into distinct relations.                                                          |

These are relational properties, not a command to split every compound value into separate tables. Values that form one domain fact and share identity and lifecycle may remain together.

Important interpretation rules:

- 1NF atomicity is relative to the attribute's defined domain and business meaning. A value being technically divisible does not automatically mean it violates 1NF.
- 2NF must be checked against every candidate key, not only the selected primary key. Partial dependencies concern non-prime attributes and proper subsets of candidate keys.
- 3NF is formally defined by its functional dependency condition. The simplified rule of eliminating transitive dependencies is useful for teaching but is not a complete formal definition.
- BCNF is stricter than 3NF. A relation in BCNF is also in 3NF, but a relation in 3NF is not necessarily in BCNF.
- 4NF addresses non-trivial multivalued dependencies, not merely columns that happen to contain multiple values.

## Baseline

- Start with a normalized relational model. 3NF is a common practical target, not an unconditional quality score or mandatory stopping point.
- BCNF may remove additional redundancy, but a BCNF decomposition can fail to preserve every original functional dependency. Prefer a lossless, dependency-preserving design when a rule must remain directly enforceable; a 3NF design may be the better trade-off.
- Apply 4NF when independent multi-valued facts create redundant combinations or update anomalies.
- Prefer decompositions that are both lossless and dependency-preserving.
- A decomposition is lossless when joining its resulting relations reconstructs exactly the original relation without introducing spurious tuples.
- A decomposition is dependency-preserving when the original functional dependencies can be enforced by checking the resulting relations individually, without requiring joins.
- Losslessness is a correctness requirement for decomposition. Dependency preservation is a strong design preference, particularly when business rules must be enforced directly.
- When dependency preservation cannot be achieved, explicitly evaluate whether the affected rules can be enforced through database mechanisms or reliable application-level validation.
- Do not label a normalized decomposition as denormalization. Record any dependency that cannot be enforced by a local constraint and define its enforcement explicitly.
- Do not assume a functional dependency merely because current sample data happens to satisfy it. Dependencies must be supported by business rules and hold for every valid database state.
- Do not normalize solely to increase the normal-form level. Evaluate query patterns, integrity requirements, write behavior, and operational complexity.

## Denormalization

Use denormalization only when an identified access pattern cannot meet its performance or operational requirements with the normalized model, appropriate indexes, and reasonable query design. The benefit must justify the additional write, storage, and consistency complexity.

For each duplicated or maintained derived value, record:

- The stored field or table and its source of truth.
- The reason and supporting access pattern (`AP-nn`).
- The update mechanism and which writes maintain it.
- The write paths that can affect the duplicated representation, including create, update, delete, correction, and import operations.
- The consistency model: same transaction/immediate or eventual.
- The consistency window, when eventual consistency is used.
- The failure handling, retry, repair, and reconciliation approach.
- The behavior on deletion, correction, and historical changes.

Prefer a derived expression that does not create stored redundancy when it meets the workload. Where a materialized value is necessary, choose an appropriate generated column, materialized view, summary structure, or mirrored field based on the derivation:

- Use a generated/computed column for supported deterministic row-local expressions.
- Use a materialized view or summary structure for suitable cross-row or aggregate derivations.
- Use an explicitly maintained mirrored field or summary table only when the workload justifies its consistency and maintenance costs.

What NOT to do:

- Do not treat generated columns as a general replacement for cross-row calculations or queries involving other tables.
- Do not duplicate parent data merely to avoid an ordinary indexed join.
- Do not classify an event-time snapshot as denormalization when it represents a distinct immutable or historically significant business fact, such as the unit price agreed upon on an order line. Such values describe the historical state of a business event rather than necessarily duplicating the current state of another entity.

## Example

Assume the following functional dependencies:

- `order_id → customer_id, placed_at`
- `product_id → product_name`

The product name is determined by product identity, not by the order or order line. Storing the current `product_name` in every order line would repeat the same product fact and create potential update anomalies.

Keep product identity and current product information in `products`, and reference it from `order_items`. Store a purchase-time product description separately only when it is an intentional historical snapshot.

```sql
CREATE TABLE orders (
  id bigint PRIMARY KEY,
  customer_id bigint NOT NULL,
  placed_at timestamp NOT NULL
);

CREATE TABLE products (
  id bigint PRIMARY KEY,
  product_name text NOT NULL
);

CREATE TABLE order_items (
  order_id bigint NOT NULL REFERENCES orders(id),
  product_id bigint NOT NULL REFERENCES products(id),
  quantity integer NOT NULL CHECK (quantity > 0),
  unit_price_at_purchase numeric(14, 2) NOT NULL CHECK (unit_price_at_purchase >= 0),
  PRIMARY KEY (order_id, product_id)
);
```

The example assumes that a product can occur at most once per order. If the business domain allows multiple separate lines for the same product in one order, use an `order_item_id` or another appropriate line identifier instead of `(order_id, product_id)` as the primary key.

`unit_price_at_purchase` is not accidental duplication when the domain requires the price agreed upon at the time of purchase. It is a distinct historical business fact and must not automatically change when the product's current price changes. If product descriptions must remain historically accurate, store an order-time description snapshot in `order_items` or an appropriate immutable snapshot relation.

## Output Mapping

- `Normalization`: summarize the normal form justified by the model's functional dependencies and any deliberate trade-off.
- `Denormalization`: document genuine stored duplication or maintained derived data, with source, synchronization, consistency window, and `AP-nn`; omit this conditional section when none exists.
- `Business Rules`: retain the rule that defines any derived value and its enforcement owner.
