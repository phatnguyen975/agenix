# Database Design: <System or Feature Name>

<!-- Authoring contract: Replace every <...> placeholder and remove every authoring comment. Use confirmed requirements and project conventions. Mark non-blocking unknowns 'Not specified' only in the affected field. Omit any section, subsection, table, or row that has no applicable content. Repeat the Collection block once per collection and the row pattern once per item. -->

<!-- Use this template for a standalone full document design. When adapting an applicable section to a caller's format, follow that format. MongoDB notation is illustrative. Use an em dash for an inapplicable cell in an otherwise relevant row. -->

## Design Summary

| Property            | Value                                                                                          |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| System / Feature    | <System or feature name>                                                                       |
| Scope               | <In-scope and out-of-scope items>                                                              |
| DBMS / Version      | <Selected document DBMS and target version; topology and compatibility settings when relevant> |
| Source Requirements | <Requirement IDs or source document paths>                                                     |
| Required Features   | <Only non-default features required by this design, with version>                              |

### Design Intent

<Briefly state the data problem and the key modeling decisions>

## Access Patterns

<!-- Repeat one row per materially distinct operation. Keep only fields that affect document shape, query, index, or atomicity decisions. -->

| ID    | Operation          | Mode         | Collections                   | Predicate / Order                             | Result / Consistency / Atomicity                                     |
| ----- | ------------------ | ------------ | ----------------------------- | --------------------------------------------- | -------------------------------------------------------------------- |
| AP-01 | <Domain operation> | <Read/Write> | <Collections read or changed> | <Filters, tenant scope, sort, and pagination> | <Result shape and freshness; for writes, the required atomic effect> |

## Business Rules

<!-- Repeat one row per confirmed invariant. Identify the authoritative mechanism; distinguish database validation from application and transaction enforcement. -->

| ID    | Rule                                       | Enforcement                                                                                  | Source                       |
| ----- | ------------------------------------------ | -------------------------------------------------------------------------------------------- | ---------------------------- |
| BR-01 | <Precise business invariant and its scope> | <Validator/unique index/conditional write/transaction/application rule and failure behavior> | <Requirement or decision ID> |

## Entity Model

<!-- Use a logical ER diagram or a relationship table. For Mermaid, use an identifying edge only when parent identity is part of child identity. A document reference has its own enforcement policy. -->

```mermaid
erDiagram
    EntityA ||..o{ EntityB : "relationship verb"
```

### Entity Definitions

| Entity        | Meaning          | Logical Identifier          | Key Scope / Lifecycle                      |
| ------------- | ---------------- | --------------------------- | ------------------------------------------ |
| <Entity name> | <Domain meaning> | <Stable logical identifier> | <Business-key scope and lifecycle summary> |

## Relationships

<!-- Repeat one row per relationship. State the chosen embed/reference strategy, ownership, and growth/integrity implications. -->

| Relationship         | Cardinality / Optionality                           | Mapping                                              | Growth / Integrity                                                  |
| -------------------- | --------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------- |
| <EntityA to EntityB> | <A-to-B and B-to-A cardinality; mandatory/optional> | <Embed at parent.field / reference collection.field> | <Bounded growth, independent lifecycle, and orphan/integrity owner> |

## Collections

<!-- REPEAT BLOCK: Copy the complete collection block below once for every collection. Replace its heading with the exact database and collection name. Keep each collection's fields, example document, and validation together. -->

### <database.collection_name>

<Purpose, represented aggregate, identifier type and generation, worst-case expected document size and array growth bounds. Compare against the selected engine and collection type limits>

| Field Path   | Type          | Required | Rule / Meaning                                       |
| ------------ | ------------- | -------- | ---------------------------------------------------- |
| <field.path> | <Engine type> | <Yes/No> | <Allowed values, bounds, business meaning, or BR-nn> |

#### Example Document

<!-- Provide one realistic, internally consistent document with synthetic data that matches the field types, requiredness, bounds and validation rules. For MongoDB, label Extended JSON or shell syntax explicitly. For other engines, use their supported representation. -->

**Example representation:** <State the selected encoding or shell notation. MongoDB shell notation is illustrated below>.

```javascript
{
  _id: ObjectId("<24-hex-character-example-id>"),
  <fieldName>: "<representative value>"
}
```

#### Validation

<Shape and value rules, enforcement mode and invalid-write behavior. State target-version requirements, collection-type limits and trusted write-path controls for rules the engine cannot enforce>

## Indexes

<!-- Include Indexes only for justified query, uniqueness, or lifecycle requirements. -->

| Index        | Collection        | Keys / Type                                                                  | Options                                      | Supports         | Reason                                                      |
| ------------ | ----------------- | ---------------------------------------------------------------------------- | -------------------------------------------- | ---------------- | ----------------------------------------------------------- |
| <index_name> | <collection_name> | <fieldA: 1, fieldB: -1; or a text/2dsphere/hashed/wildcard index definition> | <Unique/Partial/Sparse/TTL/Collation/Hidden> | <AP-nn or BR-nn> | <Query shape, uniqueness scope, or lifecycle justification> |

## Design Patterns

<!-- Include Design Patterns only when a named pattern solves a documented access, growth, consistency, or lifecycle problem. -->

| Pattern                                                                                      | Collection / Field | Source of Truth        | Maintenance / Bound                                                          | Supports         |
| -------------------------------------------------------------------------------------------- | ------------------ | ---------------------- | ---------------------------------------------------------------------------- | ---------------- |
| <Computed/Bucket/Subset/Extended Reference/Attribute/Polymorphic/Outlier/Tree/Archive/other> | <Pattern location> | <Authoritative source> | <Update method, staleness, growth bound, and repair/reconciliation approach> | <AP-nn or BR-nn> |

## Transactions and Concurrency

<!-- Include Transactions and Concurrency when writes exist or an explicit read-consistency guarantee affects design. Record the smallest suitable atomic write boundary and any cross-document conflict protocol. -->

| Operation            | Invariant / Atomic Boundary                            | Consistency / Durability                           | Concurrency Control                                                                  | Retry / Failure                                       |
| -------------------- | ------------------------------------------------------ | -------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| <Operation or AP-nn> | <BR-nn and single-document or multi-document boundary> | <Required consistency/durability settings and why> | <Conditional update/version check/unique index/shared conflict document/transaction> | <Retry and idempotency rule; client-visible conflict> |

## Security and Data Protection

<!-- Include only applicable role, sensitive-data, and application-authorization details. If all are inapplicable, omit the entire section. Omit every empty subsection. -->

### Roles and Privileges

| Role        | Principal          | Allowed Scope / Actions                            | Enforcement Boundary                                |
| ----------- | ------------------ | -------------------------------------------------- | --------------------------------------------------- |
| <Role name> | <Service or actor> | <Database/collection and read/write/admin actions> | <Database privileges and application authorization> |

### Sensitive Data

| Collection.Field        | Classification                   | Protection                                     | Query Impact             |
| ----------------------- | -------------------------------- | ---------------------------------------------- | ------------------------ |
| <collection.field.path> | <Project-defined classification> | <Minimize/encrypt/tokenize/mask and key owner> | <Query/index limitation> |

### Application Authorization

<Trusted identity source and object-/tenant-level authorization rules; database RBAC does not automatically filter documents by tenant>

## Data Lifecycle

<!-- Include this section only when at least one collection has applicable lifecycle decisions. -->

| Collection        | History / Audit                                 | Delete / Restore                                       | Retention / Archive                                                                       |
| ----------------- | ----------------------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| <collection_name> | <Required fields/events and trusted maintainer> | <Hard delete/soft delete/archive and restore behavior> | <Confirmed period and TTL/job/archive mechanism; account for TTL's asynchronous deletion> |

## Tenant Isolation

<!-- Include only for multi-tenant systems. -->

| Decision                 | Design                                                               |
| ------------------------ | -------------------------------------------------------------------- |
| Isolation Model          | <Shared collections/database per tenant/dedicated deployment/hybrid> |
| Trusted Tenant Context   | <Authenticated source and identifier type>                           |
| Tenant Keys / References | <Tenant-scoped unique indexes and reference checks>                  |
| Enforcement              | <Application authorization and physical isolation boundary>          |

## Collection Options

<!-- Include only for non-default collection semantics, such as time-series. For time-series, record applicable limits on size, validation, indexes, updates, transactions and sharding for the selected engine/version. -->

| Collection        | Type / Options                                                             | Validation Limitation                                          | Transaction / Index Limitation                                           | Retention                                         |
| ----------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------- |
| <collection_name> | <Time-series: timeField, metaField, granularity; or other special options> | <Applicable validation support or application validation path> | <Only relevant restrictions for this collection type and target version> | <Confirmed retention setting or lifecycle policy> |

## Sharding

<!-- Include only when the approved target topology is sharded. Add one concise rationale above the table stating why sharding is needed and which viable shard-key alternatives were rejected. -->

| Collection        | Shard Key / Strategy                                | Query Targeting / Distribution                              | Unique-Key Compatibility                                            |
| ----------------- | --------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------- |
| <collection_name> | <Shard key fields/order and ranged/hashed strategy> | <AP-nn targeting, cardinality, frequency, and hotspot risk> | <Unique-index prefix compatibility and _id uniqueness implications> |

## Views

<!-- Include only when a stable read interface or derived read model is justified. -->

| Name                      | Kind                                     | Purpose / Sources                                     | Authorization       | Freshness / Refresh                                | Target Indexes                                               |
| ------------------------- | ---------------------------------------- | ----------------------------------------------------- | ------------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| <view_or_projection_name> | <View/On-demand materialized collection> | <Consumers, source collections, and pipeline summary> | <Security boundary> | <Refresh trigger, maximum staleness, and recovery> | <Indexes on a materialized target collection, if applicable> |
