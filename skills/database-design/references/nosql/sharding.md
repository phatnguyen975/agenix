# NoSQL Sharding

Treat sharding as a scale and distribution decision supported by workload evidence, not as a default architecture choice.

## Sharding Decision

Consider sharding only when a replica set and appropriate indexes cannot meet documented storage, throughput, working-set, or write-distribution requirements, or when horizontal distribution is a stated requirement.

Before selecting a shard key, define:

- Dominant query predicates and whether requests can target a narrow shard range.
- Cardinality and frequency distribution of candidate values, including tenant skew.
- Write rate and whether values are monotonic or concentrated in a small range.
- Expected collection growth, chunk distribution, resharding/migration path, and operational capability.
- Required unique constraints and whether they are compatible with the shard key.

## Shard Key Selection

- Prefer a stable key with sufficient cardinality and reasonably balanced value frequency, while retaining useful query targeting.
- High cardinality alone does not guarantee uniform distribution; inspect hot values and tenant/data skew.
- Monotonically increasing keys can concentrate inserts at the active range boundary in range-based sharding. Hashed sharding can distribute inserts but may weaken range targeting and ordering locality.
- Choose a compound key when it better balances distribution and query patterns; field order determines routing and range behavior.
- Avoid changing a shard key as a casual schema revision. Treat it as a high-impact lifecycle and migration decision.

## Strategies

| Strategy | Properties                                                                     | Use When                                                       |
| -------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| Ranged   | Range queries on the key stay local. Risk of hot spots                         | Range queries on the key are core and values are spread evenly |
| Hashed   | Even distribution, including for monotonic values. No range queries on the key | Monotonic or low-entropy key with equality lookups             |
| Compound | Raises cardinality (`tenantId` plus a high-cardinality field)                  | A single field has too few distinct values                     |

## Unique Index Constraints

- In a sharded collection, a unique index generally must include the full shard key as a prefix. A unique index that omits the shard key cannot enforce global uniqueness across shards.
- If `_id` is not the shard key, the `_id` uniqueness constraint is enforced per shard, not necessarily across the whole sharded cluster. Ensure IDs are globally unique by generation or use a compatible uniqueness design.
- Unique hashed indexes are not supported. Verify all unique-index and shard-key restrictions for the actual server version before committing the model.
- A per-tenant unique key often takes the form `{ tenantId: 1, businessKey: 1 }`, but it is valid for cluster-wide enforcement only when compatible with the collection's shard key.
- Time-series collections have a separate, restricted shard-key contract. Only the `metaField`, its subfields, and (deprecated since MongoDB 8.0) the `timeField` are eligible; zone sharding and sharding administration commands are unsupported. Avoid `timeField` shard keys and verify target-version restrictions before selecting a sharded time-series design.

## Example

For a tenant-scoped workload, a candidate compound key might combine tenant routing with a high-cardinality tenant-local identifier:

```javascript
// Illustrative candidate only; validate distribution and query targeting first.
const candidateShardKey = { tenantId: 1, accountId: 1 };
```

If one tenant dominates writes, this key may still concentrate traffic. A hashed or alternative compound key changes range-query targeting and uniqueness constraints; compare candidates against actual distributions.

## Output Mapping

Include `Sharding` only for an approved sharded topology. State why sharding is needed and summarize rejected key alternatives, then record the chosen key/strategy, query targeting/distribution risk, and unique-index compatibility. Omit the section when sharding is not in scope.
