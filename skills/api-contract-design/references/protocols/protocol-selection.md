# Protocol Selection

## Scope

- Chooses the protocol for each interaction (one consumer-to-provider exchange pattern).
- Candidates: REST, GraphQL, gRPC, WebSocket, SSE, Messaging. Webhooks are an HTTP pattern covered by the webhook concern.

## Selection Order

1. Project rules: existing contracts, ADRs, style guide, platform constraints. A rule decides; stop.
2. Hard constraints: browser reach, network intermediaries, consumer control, latency, delivery guarantees.
3. Criteria below; choose the simplest protocol that satisfies them.
4. More than one viable option and no project rule: ask the user to confirm.

## Criteria

| Criterion              | Question                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| Interaction model      | Request-response, server push, bidirectional session, or decoupled asynchronous messages? |
| Consumer control       | Are consumers external and uncontrolled, or internal and coordinated?                     |
| Client types           | Browsers, mobile, services, devices?                                                      |
| Coupling               | Must the provider know the consumer, and must the consumer be online?                     |
| Latency and throughput | Interactive latency, high fan-out, or bulk throughput?                                    |
| Data shape             | Fixed resource shapes, or client-selected fields across a graph?                          |
| Caching                | Is HTTP caching valuable?                                                                 |
| Delivery guarantee     | At-most-once, at-least-once, ordering, replay?                                            |
| Session lifetime       | Short request, long-lived stream, or durable subscription?                                |
| Evolution              | Can all consumers be updated together?                                                    |
| Operational maturity   | Are tooling, observability, and gateways available for the protocol?                      |

## Protocol Profiles

| Protocol  | Fits                                                                               | Limits                                                                                                                                |
| --------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| REST      | Resource-oriented CRUD, public APIs, cacheable reads, broad client reach           | Over-fetching and chatty access for graph-shaped reads; no native streaming                                                           |
| GraphQL   | Client-shaped reads across related data, many client types with differing needs    | Harder HTTP caching; needs cost controls and field-level authorization; transport for subscriptions is outside the core specification |
| gRPC      | Internal service-to-service calls, strict typed contracts, streaming, low overhead | Browsers need a gRPC-Web layer or gateway; less human-debuggable                                                                      |
| WebSocket | Low-latency bidirectional sessions (collaboration, chat, live control)             | Own authentication, reconnect, backpressure, and scaling design; no HTTP caching                                                      |
| SSE       | One-way server-to-client streams over HTTP (notifications, progress, feeds)        | One direction only; native browser `EventSource` is GET-only without custom headers                                                   |
| Messaging | Decoupled, durable, asynchronous workflows and event distribution                  | Eventual consistency; requires delivery, ordering, and idempotency design                                                             |

## Decision Rules

- Public or third-party consumers, resource model, cacheable reads → REST.
- Many client types needing different projections of related data, with a team able to operate cost controls → GraphQL.
- Internal calls between services with typed contracts or streaming RPC → gRPC.
- Server pushes updates and the client sends requests separately → SSE.
- Client and server both send frequent messages on one session → WebSocket.
- Producer must not depend on consumer availability, or fan-out to many consumers, or replay needed → Messaging.
- Provider notifies external HTTP consumers of events: webhooks (HTTP callbacks) with a subscription API.
- Work longer than a request: asynchronous operation pattern over the chosen protocol.
- Prefer the protocol the consumer already speaks when two options satisfy every criterion.

**Worked examples:**

| Scenario                                                                     | Decision                        | Deciding Criteria                                      |
| ---------------------------------------------------------------------------- | ------------------------------- | ------------------------------------------------------ |
| Mobile app and partner systems create and read orders                        | REST                            | External consumers, resource model, cacheable reads    |
| Dashboard shows live stock levels; users only watch                          | SSE                             | One-way push over HTTP, automatic resume               |
| Whiteboard where every client sends and receives strokes                     | WebSocket                       | Frequent messages in both directions on one session    |
| Billing tells shipping an invoice was paid; shipping may be offline          | Messaging                       | Decoupled, durable, consumer availability not required |
| Checkout calls pricing thousands of times per second; both internal          | gRPC                            | Typed contract, low overhead, coordinated consumers    |
| Web and mobile clients need different fields from products, reviews, sellers | GraphQL                         | Client-shaped reads across related data                |
| Partner wants a push when a payment settles                                  | Webhook plus a subscription API | External HTTP consumer notified of events              |

## Hybrid Patterns

- REST for commands and reads, SSE or WebSocket for live updates.
- gRPC between internal services, REST or GraphQL at the edge.
- REST command that emits an event to Messaging for downstream consumers.
- REST plus webhooks for external event delivery.
- Each interaction keeps one contract; a hybrid system has one contract per format.

## Decision Record

Summarize the selected protocol and material trade-offs in the hand-off. Persist durable, cross-project architecture decisions in an ADR; do not duplicate the rationale in the consumer contract.

## Anti-Patterns

- Selecting by familiarity or fashion without checking criteria.
- WebSocket for one-way updates that SSE serves.
- GraphQL or gRPC for a public CRUD API without the matching consumer need.
- Messaging for a call that needs an immediate answer.
- One protocol for all interactions regardless of interaction model.
- Exposing internal gRPC contracts directly to uncontrolled browsers.

## Checklist

- [ ] Project rules checked before criteria.
- [ ] Each interaction has one selected protocol and named alternatives.
- [ ] Browser, network, and intermediary constraints verified for the choice.
- [ ] User confirmed the choice when no rule existed and options were viable.
