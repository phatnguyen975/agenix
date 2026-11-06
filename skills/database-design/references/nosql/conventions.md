# NoSQL Conventions

Define consistent naming, identifier, data type, and value representation conventions for document-oriented databases. Examples use MongoDB and BSON; map logical concepts to the target database's native types without assuming identical storage representations.

## Naming

- Follow existing project conventions first. If none exist, establish one convention and apply it consistently. Examples use `camelCase` for field names and plural collection names.
- Use stable, descriptive, domain-oriented names. Avoid ambiguous names such as `data`, `value`, `info`, or `type` unless their meaning is clear from context.
- Avoid punctuation or naming patterns that conflict with the database's query language, field-path syntax, or operators. Avoid `.` and leading `$` in field names.
- Use predicate-style names for boolean fields (`isActive`, `hasConsent`, `canRetry`).
- Use semantic names for date and time fields, distinguish calendar dates from timestamps (`createdAt`, `updatedAt`, `expiresAt`, `birthDate`).
- Include measurement units in field names when they are not otherwise explicit (`durationSeconds`, `weightGrams`, `distanceMeters`).
- Use explicit names for identifiers and references (`customerId`, `orderId`, `lineItemIds`).
- Use singular names for embedded objects (`shippingAddress`) and plural names for arrays or collections (`lineItems`).
- Use consistent suffixes and prefixes for fields representing the same semantic category.
- Avoid encoding mutable business meaning, environment names, or implementation details into field names.
- Do not use dynamic field names to represent variable attributes. Use a consistent attribute structure instead.

## Identifiers

- Use a stable identifier for each entity that requires independent identification.
- Prefer the target database's native identifier type when it satisfies uniqueness, generation, and interoperability requirements.
- Choose identifier formats based on system requirements:
  - Database-generated identifiers when database-local generation is sufficient.
  - UUIDs when identifiers must be generated independently across services or systems.
  - Natural identifiers only when they are stable, unique, compact, and safe to expose.
- Do not use mutable business attributes such as names, email addresses, or phone numbers as primary identifiers.
- Do not use identifiers as authorization secrets or security credentials.
- Keep the identifier type and representation consistent across documents and references belonging to the same entity.
- Do not silently mix strings, numbers, binary values, or native identifier types for the same logical identifier.
- Define a consistent identifier generation and serialization format across application components.
- Avoid exposing internal database identifiers when their representation reveals sensitive or unnecessary implementation details.

## Data Types

| Domain Meaning     | Prefer Type                                      | Convention                                                                                                                  |
| ------------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Text               | String (`string`)                                | Define normalization, case sensitivity, and encoding where relevant.                                                        |
| Whole number       | Integer (`int32` or `int64`)                     | Choose according to expected value range.                                                                                   |
| Approximate number | Floating-point (`double`)                        | Use only when approximation is acceptable.                                                                                  |
| Exact decimal      | Decimal (`decimal128`)                           | Use for decimal arithmetic requiring exact decimal representation.                                                          |
| Money              | Integer minor units plus currency code (`int64`) | Store monetary amounts as integer minor units (e.g. cents, đồng where applicable) to avoid floating-point precision errors. |
| Boolean            | Boolean (`bool`)                                 | Use actual boolean values, not strings or magic numbers.                                                                    |
| Instant            | Date/time instant (`date`)                       | Represent an unambiguous point in time, preferably UTC.                                                                     |
| Calendar date      | Date-only (`string` or explicit components)      | Use canonical `YYYY-MM-DD` representation when using strings.                                                               |
| Enumerated value   | Enum or string (`string`)                        | Use stable, descriptive values rather than positional numbers.                                                              |
| Nested structure   | Object (`object`)                                | Represent structured, related values as nested objects.                                                                     |
| Ordered collection | Array (`array`)                                  | Keep element types consistent within the same logical array.                                                                |
| Binary content     | Binary (`binData`)                               | Use only for appropriately sized binary values.                                                                             |
| Null value         | Null (`null`)                                    | Use only when explicit null has defined semantics.                                                                          |
| Identifier         | Identifier (`objectId`, `string`, or `binData`)  | Use one consistent representation for each logical identifier.                                                              |
| Geospatial value   | Geographic geometry (GeoJSON)                    | Use the target database's supported geospatial representation.                                                              |

## Value Semantics and Consistency

- Keep the logical type and representation of each field consistent across documents in the same collection.
- Distinguish missing fields, explicit null values, empty strings, empty arrays, and empty objects. They have different meanings and should not be treated as interchangeable.
- Use missing fields for optional values that have not been provided or are not applicable, according to the domain convention.
- Use explicit null only when it has a defined semantic meaning.
- Use empty strings, arrays, and objects only when they represent valid domain states.
- Avoid magic values such as `-1`, `"N/A"`, `"unknown"`, or `"null"` to represent missing data.
- Use consistent formatting for dates, identifiers, currency codes, phone numbers, and other standardized values.
- Do not mix formatted display values with machine-readable values in the same field.
- Avoid storing the same logical value in multiple incompatible representations.
- Define field-level naming and representation conventions consistently across collections.

## Example

```javascript
const invoice = {
  _id: ObjectId("65a000000000000000000001"),
  customerId: ObjectId("65a000000000000000000002"),
  fullName: "Nguyen Van A",
  isActive: true,
  birthDate: "2000-05-20",
  createdAt: ISODate("2026-11-04T08:30:00Z"),
  totalAmount: Decimal128("1250.50"),
  currencyCode: "VND",
  tags: ["premium", "verified"],
  shippingAddress: {
    city: "Ho Chi Minh City",
    countryCode: "VN",
  },
};
```

## Output Mapping

- `Design Summary`: identify the target DBMS/version and source requirements.
- `Collections > <database.collection_name>`: apply project naming/identifier/date-time/money/document-bound conventions consistently; list each field path, BSON type, requiredness, validation rule, and meaning.
