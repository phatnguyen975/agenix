---
name: api-contract-design
description: Designs, reviews, and evolves technology-neutral API contracts from requirements or existing contract artifacts. Covers interaction modeling, protocol selection, schemas, behavior, security, reliability, compatibility, and validation across synchronous and asynchronous communication patterns. Use whenever a consumer-visible API interaction or contract must be created, reviewed, or changed, regardless of protocol or format. Do not use for API implementation, test generation, database design, or internal architecture with no consumer-visible API effect.
metadata:
  author: phatnguyen975
  version: 1.0
---

# API Contract Design

## Overview

Turn requirements or an existing contract into an explicit, reviewable, machine-readable API contract and a concise design hand-off.

- Design and review consumer-visible behavior: interactions, resource and message models, schemas, constraints, errors, and operational semantics.
- Choose a protocol for each interaction; one product may intentionally expose the same capability through multiple protocols.
- Create or update the contract in the project's established format and layout. The contract is the source of truth; implementation details do not replace it.
- Support synchronous request/response, streaming, callbacks, and asynchronous messaging.

## When to Use

- A feature, story, integration, or change request creates or changes an API operation, RPC, event, message, stream, subscription, or webhook.
- An existing contract needs a correctness, completeness, security, interoperability, or consistency review, whether or not changes are requested.
- A protocol or contract format must be selected for a new interaction.
- An existing contract needs a new capability, deprecation, compatibility correction, or breaking-change proposal.
- A requirement changes a consumer-visible rule such as authentication, authorization, pagination, idempotency, error behavior, rate limits, caching, content negotiation, or versioning.

## When NOT to Use

- Implementing handlers, clients, SDKs, middleware, or infrastructure.
- Writing or generating automated tests.
- Reviewing or debugging an implementation without assessing or changing its contract.
- Designing database schemas, UI behavior, deployment topology, or internal service architecture that has no consumer-visible API effect.

## Input

| Input                                                   | Required | How to use                                                                                                                                                                                                                       |
| ------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Requirement, story, change request, or review objective | Yes      | Source of intended consumer-visible behavior or review criteria. For review-only work, treat the existing contract as the primary artifact.                                                                                      |
| Existing contracts and project conventions              | No       | Discover relevant files, style guides, ADRs, compatibility policy, toolchain versions, and project layout. Existing project decisions take precedence unless they conflict with security, correctness, or explicit requirements. |
| Consumers and trust boundaries                          | No       | Infer from project context where possible; identify human, browser, partner, internal service, broker, and third-party consumers.                                                                                                |
| Constraints                                             | No       | Capture compatibility, latency, throughput, payload size, availability, privacy, residency, regulatory, and toolchain constraints when relevant.                                                                                 |

Ask only when missing information materially changes the contract and cannot be resolved safely from project context. Otherwise make the least-surprising defensible choice, record the assumption in the hand-off, and continue. Never invent domain facts, permissions, limits, guarantees, or business states; mark genuinely unknown items as unresolved.

## Output

1. **Contract artifact(s)** for every distinct interaction and protocol when creation or changes are in scope. Follow the project's established file organization. A project may keep a contract in one file or organize it into multiple files. When no convention exists, choose a clear location such as `docs/api-contracts/`, state the chosen path, and proceed. For review-only work, do not rewrite files unnecessarily; provide actionable findings with severity, evidence, and recommended changes.
2. **Hand-off report** with artifact paths, format versions, protocol decisions where relevant, unresolved assumptions, notable design choices, changes and compatibility classification, validation performed, warnings, review findings, and approvals still required.

Do not include secrets, production credentials, internal hostnames, or sensitive personal data in examples or consumer-facing descriptions. Start from the matching template in `assets/` when supported, but remove its guide comments and unused illustrative coverage sections before delivery.

## Core Principles

1. **Contract first:** define consumer-visible behavior before implementation; implementations conform to the contract.
2. **Consumer-centered modeling:** model business concepts and use cases, not database tables, ORM entities, or internal class names.
3. **Protocol per interaction:** choose based on interaction shape, consumer capabilities, latency, streaming, delivery, and operational constraints.
4. **Project-compatible organization:** preserve the project's file layout and tooling; do not require either a monolithic contract or a particular split-file structure.
5. **Single logical source of truth:** define a schema or behavior once within the contract set and reference it consistently.
6. **Explicit semantics:** specify method safety, side effects, idempotency, concurrency, ordering, delivery, retry, timeout, cancellation, and error behavior where applicable.
7. **Secure by default:** authenticate callers where required; authorize every operation and every object/property/tenant boundary; default to deny. Public access must be intentional and explicit.
8. **Bound resources:** define applicable limits for collection size, input size, nesting, query cost, concurrency, rate, stream duration, timeouts, and retries.
9. **Stable evolution:** prefer additive changes; classify every change; breaking changes require explicit approval and a migration path.
10. **Precise schemas:** state type, requiredness, nullability/presence, format, bounds, unknown-field policy, and examples where the format supports them.
11. **Standards discipline:** distinguish specifications, RFCs/BCPs, drafts, profiles, bindings, and ecosystem conventions. Never promote a draft or convention to a standard.
12. **Validation honesty:** report exactly which parsers, linters, schema validators, compatibility checkers, and manual checks ran. A successful YAML parse is not proof of OpenAPI or AsyncAPI conformance.

## Routing

Read only the references required by the interaction and triggered concerns. Do not load every reference by default. A referenced file does not need to be loaded transitively unless its own content is needed.

**Routing rules**

- Load the relevant protocol reference, contract reference, and baseline concerns; load only concern files triggered by the interaction or requirements.
- Read `references/protocols/protocol-selection.md` only when the protocol choice is open or needs review. Do not revisit an explicit, still-valid project decision without a reason.
- Read `references/standards-baseline.md` only when a version, draft, binding, profile, or current standards claim needs selection or verification. Project-pinned versions and toolchain constraints take precedence when still supported and safe.
- Load a template only when creating or substantially restructuring a contract. For review-only tasks, inspect the existing artifact and its configured validators first.

**Table A — interaction → protocol, contract, template**

| Interaction                             | Protocol                            | Contract                                                                      | Template                |
| --------------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------- | ----------------------- |
| Resource-oriented HTTP API (REST-style) | `references/protocols/rest.md`      | `references/contracts/openapi.md`, `references/contracts/schema-modeling.md`  | `assets/openapi.yaml`   |
| Server-Sent Events (SSE)                | `references/protocols/sse.md`       | `references/contracts/openapi.md`, `references/contracts/schema-modeling.md`  | `assets/openapi.yaml`   |
| Webhook / Callback                      | `references/concerns/webhooks.md`   | `references/contracts/openapi.md`, `references/contracts/schema-modeling.md`  | `assets/openapi.yaml`   |
| WebSocket                               | `references/protocols/websocket.md` | `references/contracts/asyncapi.md`, `references/contracts/schema-modeling.md` | `assets/asyncapi.yaml`  |
| Broker / Message-driven                 | `references/protocols/messaging.md` | `references/contracts/asyncapi.md`, `references/contracts/schema-modeling.md` | `assets/asyncapi.yaml`  |
| gRPC                                    | `references/protocols/grpc.md`      | `references/contracts/protobuf.md`                                            | `assets/service.proto`  |
| GraphQL                                 | `references/protocols/graphql.md`   | `references/contracts/graphql-sdl.md`                                         | `assets/schema.graphql` |

**Table B — signal → concern** (in `references/concerns/`)

| Signal                                                                                                                                                                                      | Read                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Every contract                                                                                                                                                                              | `errors.md`, `payload-conventions.md`      |
| List, search, filtering, sorting, cursor, or bulk selection                                                                                                                                 | `collections.md`                           |
| Mutation with side effects, retries, duplicate delivery, or concurrent writers                                                                                                              | `idempotency-retries-concurrency.md`       |
| Authenticated users, tenants, roles, scopes, or service identities                                                                                                                          | `authentication-authorization.md`          |
| Public, partner, or cross-boundary exposure; browser clients; untrusted input, sensitive data, uploads, or third-party dependencies                                                         | `api-security.md`                          |
| Public, partner, or multi-tenant consumption; quotas or abuse controls                                                                                                                      | `rate-limiting-quotas.md`                  |
| HTTP requests/responses support multiple representations or media types; `Accept`/`Content-Type` negotiation; localization; compression; range requests; upload, download, or file transfer | `content-negotiation-and-file-transfer.md` |
| Cacheable reads, conditional requests, validators, or lost-update prevention                                                                                                                | `caching-and-conditional-requests.md`      |
| Latency, payload size, deadlines, reliability, or service objectives                                                                                                                        | `performance-and-reliability.md`           |
| Tracing, correlation, audit events, or telemetry requirements                                                                                                                               | `observability.md`                         |
| Provider-initiated HTTP callback                                                                                                                                                            | `webhooks.md`                              |
| Contract changed, deprecated, versioned, or retired                                                                                                                                         | `versioning-compatibility.md`              |
| Long-running work, batch processing, import/export, or asynchronous job resources                                                                                                           | `long-running-bulk-operations.md`          |

## Workflow

1. **Intake**
   - Read the requirement or review objective and discover the smallest relevant set of existing contracts, conventions, ADRs, compatibility rules, and toolchain versions.
   - Classify as Create, Update, or Review. Extract actors, consumer capabilities, interaction direction, trust boundaries, data classification, expected volume, latency, and failure conditions.
   - Resolve unknowns from project evidence where possible; ask only for decision-changing unknowns.
2. **Select protocol per interaction**
   - Apply explicit project architecture and consumer constraints first.
   - If the protocol choice is open or questionable, read `references/protocols/protocol-selection.md`; select the simplest protocol that satisfies the requirements and explain material trade-offs in the hand-off or an ADR when the decision is durable.
   - One project may use several protocols; decide each interaction separately.
3. **Model the surface**
   - Identify resources, operations, RPCs, events, channels, messages, streams, subscriptions, callbacks, ownership, lifecycle, and state transitions.
   - Define names and identifiers consistently. State invariants, side effects, pagination, concurrency, ordering, and error conditions.
   - Distinguish command, query, event, notification, and reply; do not model an event as a command or a transport acknowledgement as business completion.
4. **Apply relevant concerns**
   - Read the protocol/contract references in Table A and only the concern files signaled by Table B.
   - Express each applicable concern at the narrowest level supported by the format: API, server, operation, channel, message, type, field, parameter, or response. Prefer structured contract elements over prose wherever supported.
   - For consumer-visible rules the format cannot encode, use a precise description at the most relevant level or link to maintained, consumer-accessible supplementary documentation. Keep internal rationale, threat models, and implementation policy in ADRs or internal design documents, not in the consumer contract.
   - Where a concern is inapplicable, do not add irrelevant fields or boilerplate; record a reason in the hand-off only when a reviewer could reasonably expect the control.
5. **Author, update, or review the contract**
   - Follow the selected format's authoring rules and the project's established file organization. Do not impose file splitting or flatten a modular project without a reason.
   - Define shared schemas/components once and reference them; avoid duplicate or contradictory representations.
   - Include representative valid request/message and success/error examples for each operation or message type where supported. Ensure examples match the schema and documented semantics.
   - In Update mode, preserve unrelated content, minimize unrelated formatting churn, diff old and new contracts, and classify all consumer-visible changes.
   - In Review mode, prioritize correctness and consumer-impacting issues; report each finding with severity, location/evidence, impact, and a concrete recommendation. Do not make speculative findings or edit unrelated content.
   - Obtain approval before applying a known breaking change; otherwise provide a compatible alternative or leave it as a proposal.
6. **Validate**
   - Run the validators and linters the project already uses for each format.
   - Without project validators, walk the verification checklist in the relevant contract and protocol references.
   - Fix and re-run until no errors remain; report warnings and unverified areas in the hand-off.
7. **Hand off**
   - Summarize artifacts, paths, protocol decisions, format versions/fallbacks and reasons, notable consumer-visible rules, compatibility classifications, review findings, validation commands/results, unresolved assumptions, and approvals still required.

## Common Rationalizations to Reject

| Rationalization                                     | Reality                                                                                              |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| "Implementation will define the contract."          | Consumer-visible behavior must be agreed in the contract first.                                      |
| "Consumers can ignore a new required field."        | A new required request field can break existing callers.                                             |
| "A separate schema file is always cleaner."         | File topology is a project choice; logical definitions must remain unique and references resolvable. |
| "One file is always easier."                        | A monolith may be unsuitable for a project with established modular contracts; preserve its layout.  |
| "Pagination can come later."                        | Unbounded collections create load risks and make later limits potentially breaking.                  |
| "Internal APIs do not need security."               | Internal callers and networks are not inherently trusted.                                            |
| "A draft is basically final."                       | Drafts can change or expire; label and verify the revision before adopting it.                       |
| "Exactly-once delivery means exactly-once effects." | Delivery guarantees do not by themselves make downstream business effects atomic or duplicate-free.  |
| "One protocol should serve every interaction."      | Different interaction shapes may justify different protocols.                                        |

## Verification

Before hand-off, verify each applicable item:

- [ ] Every interaction has a documented protocol decision grounded in project and consumer constraints.
- [ ] The contract format and version match the project or the verified baseline/fallback; no silent upgrade occurred.
- [ ] File organization follows the project; logical schemas and behavior are defined once and all references resolve.
- [ ] Effective authentication and authorization are clear for every operation/channel; intentionally public surfaces are explicit.
- [ ] Inputs, outputs, collections, payloads, concurrency, timeouts, and retries are bounded where applicable.
- [ ] Method safety, side effects, idempotency, ordering, delivery, retry, cancellation, and completion semantics are correct for the protocol.
- [ ] Errors use the protocol's error model and expose stable machine-readable information without internals.
- [ ] Request/message and success/error examples are syntactically valid and match their schemas.
- [ ] Requiredness, nullability/presence, formats, units, enums, unknown-field behavior, and numeric bounds are deliberate.
- [ ] Media types, negotiation behavior, transfer semantics, cache behavior, rate limits, observability, and long-running-operation rules are included when triggered.
- [ ] Drafts, profiles, bindings, and conventions are labeled accurately wherever they affect consumer interoperability; no draft is presented as a finalized RFC.
- [ ] Update mode: every consumer-visible change is classified; breaking changes are approved or left as proposals with a migration path.
- [ ] Review mode: findings are evidence-based, impact is stated, and recommendations do not exceed what the contract and requirements support.
- [ ] Validation reports exactly which tools ran, what passed, and what could not be verified.
- [ ] No real secrets, production credentials, internal hostnames, or personal data appear in examples or consumer-facing descriptions.
