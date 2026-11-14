# Crosscutting Concepts

Use for **recurring, system-level architectural policies** that several elements must implement consistently. A concept may span modules within one application; it does not require multiple services or containers. Detail belongs in the relevant lower-level design, not here.

## Select Only What Matters

Include a concept when it:

- Resolves a significant driver or mandatory constraint across boundaries;
- Establishes a rule multiple elements need to observe to avoid inconsistency;
- Implements a significant architectural decision that must be understood in more than one view.

Do not fill a generic checklist merely for completeness. Mention an ADR by ID instead of copying its reasoning. Distinguish a concept (system rule) from an ADR (why chosen) and a fitness function (how guarded).

## Candidate Concept Areas

| Area                  | Examples of Architecture-Level Policy                                 |
| --------------------- | --------------------------------------------------------------------- |
| Security              | Identity boundaries, authorization ownership, secrets and audit rules |
| Integration           | Sync/async contracts, error semantics, retries, idempotency           |
| Data                  | Ownership, consistency, retention, replication, migration rules       |
| Reliability           | Failure isolation, timeout budgets, graceful degradation, recovery    |
| Observability         | Correlation IDs, telemetry responsibility, SLI boundaries             |
| Delivery              | Compatibility windows, release units, rollback guarantees             |
| Shared Domain Meaning | Cross-context translations and published terminology                  |

Policies like UI colors, detailed logging formats, object mapping implementations and coding style are **out of scope** unless they constitute a demonstrable architectural constraint. A security policy must still cover relevant trust boundaries even if only one application exists.

## Describe a Concept

In System Design §8, for each selected concept record:

- **Purpose and applicability:** driver/constraint IDs and exactly which modules/containers and boundaries follow the policy.
- **Rule and mechanism:** testable obligations, allowed exceptions, assumptions and the direction of dependencies or information flow.
- **Failure or change behavior:** what happens during a violation, outage, version mismatch or migration when relevant.
- **Ownership and evidence:** source ADR, verification `FF` IDs/status where applicable, and owner role when provided.

**Example — Cross-Boundary Request Correlation:**

- Applies to `Web App`, `Order API`, and `Fulfillment Worker`; supports `QUA-04` (diagnosis time).
- The entry point assigns or validates a correlation identifier and passes it along approved sync/async boundaries. No sensitive personal data is placed in that identifier.
- If context propagation is missing, record the boundary and a diagnostic fallback; do not silently claim end-to-end trace continuity.
- Verify with a representative request traversing all three elements. The `FF` is `planned` until an actual check exists.

## Additional Example — Authorization Ownership

- **Purpose:** enforce the authorized actions of a customer across the public API and asynchronous worker; trace the applicable security drivers.
- **Scope:** entry-point authentication, resource-level authorization in the owning business boundary, and identity/authorization context passed to deferred work.
- **Rule:** a validated session at the edge does not replace authorization at the action owner. A background consumer verifies the authority attached to the command or uses explicitly delegated service privileges; retries must not expand privileges.
- **Verification:** specify representative allowed/denied flows and a failure case exercise. If recorded as an FF, keep its execution status `planned` until evidence shows the check operates; otherwise describe the validation plan without assigning an FF state. Do not assume an identity provider or authorization protocol without a project decision.

This is an architecture policy, not an instruction to configure a particular identity product. Document implementation-specific roles and policy expressions elsewhere.

## Consistency Rules

- Use the same element names and semantics as the Container View and ADRs.
- Link concepts to affected elements without restating the same mechanism in every building-block description.
- Resolve contradictory crosscutting policies and ADRs as a defect in the design, not as two valid alternatives.
- Record "Not applicable" with rationale when a required arc42 section has no applicable shared policies; do not fabricate concepts.
