# Axis: performance

## Purpose

Verify that the change does not introduce an unreasonable runtime cost, resource bottleneck, or scalability regression for the workload the system is designed to serve.

## Method

1. Establish the workload and budgets from product/service SLOs, specifications, production telemetry, architecture docs, or representative benchmarks: data volume, request/concurrency rates, latency percentiles, throughput, payload sizes, memory/CPU, and client-device constraints.
2. If no target or workload is documented, state the assumption and reason about cost growth and resource bounds. Do not substitute a universal latency, bundle-size, or capacity target.
3. Identify changed hot paths: request/job loops, data access, startup, serialization, network calls, memory retention, rendering, and critical resource loading.
4. Quantify likely cost where possible: query/call/allocation count per unit, asymptotic growth, payload size, queue depth, memory retention, or before/after measurement.
5. Prefer production telemetry, representative benchmarks, query plans, profilers, and existing budgets over intuition. A lab benchmark must state environment, data shape, concurrency, and measurement method.
6. Recommend optimization only when the path is material to the workload or violates an explicit budget. Do not recommend caching, indexing, memoization, or concurrency merely because the mechanism exists.
7. Keep security-exploitable resource exhaustion with a plausible attacker-controlled path under security; report ordinary capacity/performance regressions here.

## Checklist

### Algorithms and CPU

- Does time/space complexity grow acceptably with input and expected concurrency? Are nested scans, repeated work, sorting, serialization, or parsing on hot paths bounded?
- Is invariant work performed once rather than repeated per item/request?
- Are large objects, copies, intermediate collections, regexes, or expensive conversions created on hot paths unnecessarily?
- Are batching, streaming, incremental processing, or early termination appropriate for large inputs?
- Is expensive CPU work placed on an appropriate worker/job/thread rather than blocking a latency-sensitive request or UI thread?

### Database and Data Access

- Are there N+1 query/API patterns or repeated round trips that grow with the number of records?
- Are list/search/export operations bounded through pagination, streaming, explicit limits, or an intentional bulk-processing design?
- Are only necessary columns/fields fetched on hot paths where payload and row width matter?
- Are bulk operations used where per-item calls add material overhead?
- Do indexes match actual filter, join, and sort predicates and the database engine's index semantics?
- For materially changed queries, is there a representative query-plan/measurement comparison where available? Are scans, sorts, misestimates, spills, and row counts understood in the context of table size and selectivity? Remember that tools such as `EXPLAIN ANALYZE` execute the statement; do not run them against production or side-effecting statements without explicit authorization and a safe test environment.
- Are indexes justified by the measured/query-plan benefit and balanced against write amplification, storage, maintenance, and duplicate/overlapping indexes?
- Are database-specific techniques (composite, partial, expression, covering, full-text, trigram, partitioning) used only when supported and appropriate for that engine/version/query shape?
- Are slow-query telemetry and useful query labels available where the project operates a database service?

### Connections, I/O, and Concurrency

- Are network, filesystem, database, and remote-service operations awaited/handled without blocking event loops or UI threads?
- Are independent operations parallelized only when safe, with bounded concurrency and backpressure?
- Are queue depth, worker/thread pools, connection acquisition, and external service limits bounded?
- Is pool capacity calculated against total replicas/processes/instances and the downstream service's limits, including autoscaling/serverless concurrency?
- Are pools reused at the appropriate application/process boundary rather than created per request? Are acquisition and operation timeouts configured?
- Are long transactions, leaked resources, missing awaits, and exhausted pools diagnosed before simply increasing pool sizes?
- Are large request/response bodies streamed or chunked where doing so reduces peak memory and latency?
- Are compression and protocol choices appropriate for payload size, CPU, client, and deployment constraints?

### API and Service Latency

- Does the change preserve service SLOs under representative load, including tail latency (p95/p99 where used by the project)?
- Are request handlers free of unnecessary CPU-heavy work, serial remote calls, unbounded fan-out, and synchronous waits?
- Are deadlines propagated across nested calls, with cancellation and bounded retries that do not amplify load?
- Are load shedding, admission control, circuit breakers, or queue limits used where needed for overload behavior?
- Is time-to-first-byte (TTFB) measured and decomposed into connection setup, server work, and response generation when relevant? TTFB is diagnostic, not a Core Web Vital and has no universal threshold.
- Are edge/CDN, keep-alive, HTTP versions, preconnect, or redirect changes supported by an evidenced latency need rather than applied as blanket rules?

### Caching

- Is the cached operation measured or otherwise shown to be expensive enough to justify cache complexity and an extra hop?
- Is the read/write ratio and cache layer appropriate for the workload?
- Does the key include every result-varying dimension (tenant, identity, authorization, locale, feature flags, query inputs, schema/version)? Could one user's result be served to another?
- Is freshness/staleness explicitly bounded, and is invalidation behavior coherent? TTL, event invalidation, and versioned keys may be combined when intentionally designed.
- Are hot-key stampedes and cache outages handled through coalescing, locking, stale serving, or bounded fallback where appropriate?
- Are negative results bounded so newly created resources become visible within an acceptable interval? Are transient origin failures kept from poisoning the cache?
- Are eviction policy, entry size, memory ceiling, and hit/miss/eviction telemetry defined?
- Is stale data unacceptable for the domain (for example, authorization, balances, inventory commitment) and therefore not cached or revalidated at the decision boundary?
- Is write-behind used only with explicit durability, replay, ordering, and recovery guarantees?

### Memory and Resource Lifecycle

- Are caches, queues, buffers, collections, sessions, and retained histories bounded?
- Are listeners, timers, subscriptions, streams, file handles, native resources, and references released when their owner ends?
- Can closures, event listeners, global registries, thread-local values, or long-lived tasks retain request/user objects?
- Are large payloads processed without unnecessary copies or simultaneous in-memory representations?

### Client-side and Browser Performance

- **Core Web Vitals:** when applicable, assess field data at the 75th percentile, segmented by page/group and device class. Current good thresholds are LCP ≤ 2.5 s, INP ≤ 200 ms, and CLS ≤ 0.1. The needs-improvement/poor boundaries are LCP 4.0 s, INP 500 ms, and CLS 0.25. Do not assume a single lab run proves field performance.
- **JavaScript:** does the initial route load only necessary code? Are route/feature chunks, lazy loading, tree shaking, and dependency output formats appropriate? Use the project's performance budget; a 200 KB compressed initial bundle is only an external heuristic, not a universal limit.
- **Main thread:** browser tasks exceeding 50 ms are long tasks. Do they block input/rendering? Can work be chunked, deferred (for example, via idle scheduling where supported), or moved to a worker? Use `scheduler.yield()`, `scheduler.postTask()`, or other scheduling APIs only when supported, feature-detected, and paired with an acceptable fallback. Do not prescribe framework-specific memoization without profiling.
- **Third-party code:** are scripts, SDKs, widgets, and embeds necessary, sized, loaded at the right priority, and isolated from critical interaction paths?
- **CSS and rendering:** is there avoidable render-blocking CSS, forced synchronous layout/layout thrashing, expensive paint, excessive re-rendering, or unvirtualized long lists? Prefer compositor-friendly animation properties when appropriate, but verify actual rendering cost.
- **Images and media:** are formats, quality, responsive sources, dimensions/aspect ratios, decoding, and loading priority appropriate? Make the primary LCP image discoverable early and give it appropriate fetch priority where supported; lazy-load below-the-fold content, but do not lazy-load the primary LCP image. Use modern formats with suitable fallbacks where required.
- **Fonts:** avoid unnecessary families/weights; prefer efficient formats such as WOFF2 where supported, subset only when justified, preload only critical fonts, and use font-display/fallback metrics to limit blocking and layout shift. Do not require WOFF2-only or fixed family/weight counts where compatibility/product needs differ.
- **Network and caching:** use content-hashed asset caching and appropriate API/document cache headers. Preconnect/fetch-priority hints only for known critical resources. Never weaken privacy or freshness requirements to improve cacheability.
- **Page lifecycle:** avoid legacy `unload` handlers when back/forward cache eligibility matters. Do not remove `Cache-Control: no-store` from sensitive pages solely to improve bfcache; evaluate current browser behavior and privacy requirements.
- **Measurement:** use field RUM/CrUX where available, attribution for slow interactions, representative lower-end devices, browser performance traces, bundle analysis, and CI budgets where the project has them. State when visual/runtime evidence is unavailable.

### Infrastructure and Capacity

- Are CPU, memory, file descriptors, connections, disk, queue, and downstream limits appropriate for expected concurrency and payloads?
- Are autoscaling signals and limits aligned with the actual bottleneck and downstream capacity?
- Are health/readiness checks, CDN/edge placement, compression, and caching appropriate to the system's topology and user distribution?
- Does the change increase cold-start, startup, image size, container footprint, or deployment artifact size materially?

## Common Findings

| Pattern                              | Impact                               | Fix                                            |
| ------------------------------------ | ------------------------------------ | ---------------------------------------------- |
| N+1 queries                          | Database load grows with result size | Join, eager load, or batch                     |
| Unbounded query or list              | Memory exhaustion, timeouts          | Paginate and limit                             |
| Missing index for the query shape    | Slow reads as data grows             | Index the filter and sort columns              |
| Index added without reading the plan | Write cost with no read gain         | Check the plan before and after                |
| Redundant or unused indexes          | Slower writes, wasted storage        | Audit usage stats, drop what nothing reads     |
| Connection pool per request          | Connection exhaustion under load     | One pool per process; proxy for serverless     |
| Cache key missing the viewer         | One user's data served to another    | Include tenant, user, locale, permissions      |
| Unbounded cache                      | Memory growth                        | Eviction policy and ceiling                    |
| Cache stampede on a hot key          | Origin overload at expiry            | Coalesce, lock, or serve stale                 |
| Layout thrashing                     | Dropped frames                       | Batch reads, then writes                       |
| Unoptimized images                   | Slow loading, wasted bandwidth       | Modern formats, responsive sizes, lazy loading |
| Large bundles                        | Slow loading and interaction         | Split, remove unused code, audit dependencies  |
| Blocking the main thread             | Unresponsive interface               | Chunk or offload                               |
| Listener or timer leaks              | Growing memory                       | Release on teardown                            |

## Severity Guidance

- Likely to exhaust a critical resource or breach an explicit SLO/budget at expected scale — High or Critical by impact.
- Material growth problem at an expected or clearly foreseeable workload — Medium or High.
- Measured but modest regression on a hot path — Low or Medium.
- Unmeasured micro-optimization, off-hot-path cost, or speculative scaling concern — do not report.

## Boundaries

- Attacker-exploitable resource exhaustion belongs to security when a plausible attack path exists; ordinary capacity regression belongs here.
- Cache-key authorization leaks belong to security; report once under security if exploitable.
- Stale-cache behavior that violates functional invariants belongs to correctness; latency/capacity cost belongs here.
- Operational dashboards/alerts/runbooks belong to compatibility-operability.

## References

- [Web Vitals — Core Web Vitals](https://web.dev/articles/vitals)
- [Chrome: Long tasks](https://web.dev/articles/optimize-long-tasks) and [Scheduler.yield()](https://developer.chrome.com/blog/use-scheduler-yield)
- [MDN: Scheduler.yield()](https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/yield)
- [PostgreSQL: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) and [Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
