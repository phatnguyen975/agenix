# NoSQL Validation

Use the selected engine's validation to enforce document shape and field-level value rules. The syntax and modes below describe MongoDB. State which invariants remain application- or transaction-enforced.

## Structural Validation

- For MongoDB collections with a stable document contract, define a `$jsonSchema` validator. For another engine, map the rules to its supported validation or the trusted write path.
- Specify required fields, BSON types, allowed values, numeric bounds, string length/pattern, array bounds, and nested object shape when part of the domain contract.
- Use `additionalProperties: false` only for intentionally closed objects; include `_id` and every allowed field. Keep variable attributes open where intended.
- Set `maxItems` for bounded arrays. If no credible bound exists, reconsider embedding rather than inventing a maximum.
- Use `oneOf` or an explicit discriminator rule for known variants. Avoid rejecting forward-compatible fields without a deliberate versioning policy.

**Example:**

```javascript
db.createCollection("orders", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["tenantId", "status", "createdAt"],
      additionalProperties: false,
      properties: {
        _id: { bsonType: "objectId" },
        tenantId: { bsonType: "objectId" },
        status: { enum: ["pending", "paid", "cancelled"] },
        createdAt: { bsonType: "date" },
        items: {
          bsonType: "array",
          maxItems: 100,
          items: {
            bsonType: "object",
            required: ["productId", "quantity"],
            properties: {
              productId: { bsonType: "objectId" },
              quantity: { bsonType: "int", minimum: 1 },
            },
          },
        },
      },
    },
  },
  validationLevel: "strict",
  validationAction: "error",
});
```

## Validation Modes

See MongoDB's [validation levels](https://www.mongodb.com/docs/manual/core/schema-validation/specify-validation-level/) and [validation actions](https://www.mongodb.com/docs/manual/core/schema-validation/handle-invalid-documents/) for the target version.

| Setting            | Option                       | Design meaning                                                                                             |
| ------------------ | ---------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `validationLevel`  | `strict`                     | Validate all inserts and updates against the rules; preferred for a new collection with a defined contract |
|                    | `moderate`                   | Validate inserts and updates to documents that already satisfy validation; transitional compatibility mode |
|                    | `off`                        | Disable validation; require an explicit reason and compensating controls                                   |
|                    | `constraint` (MongoDB 9.0+)  | Enforce validation so it cannot be bypassed; validation rules cannot be modified while active              |
| `validationAction` | `error`                      | Reject invalid writes                                                                                      |
|                    | `errorAndLog` (MongoDB 8.1+) | Reject invalid writes and log details                                                                      |
|                    | `warn`                       | Accept invalid writes and log; observation/migration mode, not enforcement                                 |

- Before enabling stricter validation on an existing collection, inspect and remediate legacy documents. Changing validation policy does not repair existing records.
- MongoDB 9.0 introduced `constraint`. Existing documents must satisfy validation, and the action must be `error` or `errorAndLog`. To edit the rules, change the level to `strict` first.
- MongoDB time-series collections do not support schema validation. Enforce their shape and value rules in a trusted application write path and record the limitation.

## Cross-Field and Business Rules

- `$jsonSchema` validates fields and structure. Use `$expr` in the validator for supported same-document comparisons, such as `endAt > startAt`.
- Unique values require unique indexes, not schema validation.
- References and target existence are not enforced by a normal reference field; design a race-safe trusted write path when existence or same-tenant membership must hold under concurrent changes. See [Reference Integrity](relationships.md#reference-integrity).
- Previous-state transitions require conditional updates (match the expected current state in the update filter); a validator cannot inspect the prior value.
- Invariants spanning documents require a model that puts the invariant in one document, a transaction with an explicit conflict protocol, or another concurrency-safe mechanism.
- Authorization is not field validation. Enforce permissions using database roles and the application authorization boundary.

## Output Mapping

In each `Collections > <database.collection_name> > Validation` block, record the validator shape, closed/open object policy, validation level/action, same-document rules, and collection-type limitations. Record the intended initial write behavior and failure outcome. In `Business Rules`, identify the enforcement layer and failure behavior for each rule.
