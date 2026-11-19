---
name: test-strategy-design
description: Design or revise a risk-based test strategy for a product, service, library, or feature. Use when deciding what to verify, which test levels and tools to use, where and when checks should run, or what evidence is required before an implementation or release decision.
metadata:
  author: phatnguyen975
  version: "1.0"
---

# Test Strategy Design

## Purpose and Scope

Turn requirements, quality risks, and owned interfaces into an actionable verification strategy for a new or existing system. For systems with multiple units, produce one strategy across the owned units and their integration boundaries. Leave test implementation, harness setup, and CI wiring to the implementation handoff.

## Inputs

- In-scope behavior, acceptance or quality requirements, and known risks.
- Owned units, public interfaces, dependencies, and supported targets.
- Selected stack or existing test tooling, operational constraints, and any required verification or delivery gates.

Read only the relevant requirements, architecture, contracts, and existing checks. Ask about missing decisions that materially change coverage, tooling, or a required gate. Record a bounded assumption when it is sufficient to proceed.

## Principles

- Start with the failure and its consequence. Use the smallest observable boundary that can expose it. Add a broader check when the risk depends on integration, deployment, or a complete user journey.
- Record what each check can prove. A schema check establishes conformance of the inspected artifact. Runtime conformance and real dependency behavior require exercising those boundaries.
- Separate the reason to run a check from the environment that can run it and the decision that needs its result. Surface a blocker when required evidence cannot be collected by the decision point.
- Reuse existing coverage and compatible tools. Add a suite or target when it covers a distinct risk or satisfies a requirement.
- Derive pass criteria from the approved behavior. Flag unknown interface details, test controls, or external access as prerequisites when a check depends on them.

## Workflow

### 1. Identify Verification Priorities

Identify failures that would matter to users or consumers. Include critical journeys, cross-unit boundaries, compatibility, and measurable quality requirements where applicable. Tie each material risk to a requirement, contract, or concrete failure mode. Inspect existing coverage before adding a suite.

### 2. Select Checks and Run Conditions

Select the checks below that match the risks. For an interface check, identify the exercised boundary so that its result is interpreted at the correct level.

| Check                    | Use When                                                                                                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Unit or component        | A focused rule, calculation, state transition, or interaction can be exercised in isolation. Check observable outcomes at the unit's public boundary.                                                                                            |
| Integration              | Correctness depends on interaction between units or on a real dependency such as a datastore, queue, or service. Control the data and isolate the dependency when its behavior matters.                                                          |
| API or contract          | Consumers depend on an interface. Select schema/example validation, compatibility checks, or runtime conformance as needed. Identify the actual boundary exercised, such as an in-process handler, deployed endpoint, or message exchange.       |
| End-to-end or acceptance | A critical outcome depends on the complete in-scope path. Use the real entry point, such as a browser, API, message, command, or public library interface. For multi-unit products, cover the handoffs that make the outcome possible.           |
| Specialized or manual    | Add performance, accessibility, visual, resilience, or human checks for specific risks. For performance, define the workload, environment, metrics, and pass thresholds. For a human check, record the procedure, expected result, and verifier. |

Set **Run When** for each check. Specify the triggering change or event, when the result is needed, and which decision depends on it. Run fast feedback checks during development and at applicable automated gates. Schedule wider or expensive suites where the required environment is available and results can still inform the decision. Use local, review, post-merge, scheduled, or release execution as appropriate.

### 3. Choose Tooling, Targets, and Test Data

- Prefer tools already compatible with the selected stack and execution environment. Add a tool for a coverage or evidence need the current stack cannot meet. Record its role, the relevant version or compatibility constraint, and the intended test location. Mark unverified choices as pending.
- Select the targets that matter to each check, such as runtime, browser, platform, or dependency version. Use representative targets where they provide sufficient evidence and justify broader coverage when a requirement or risk calls for it.
- Specify required services, fixtures, setup/teardown behavior, and isolation. Identify which dependencies are real, substituted, or exercised in an approved sandbox. Limit claims to the boundary actually exercised. Treat prototype replay as evidence about design behavior and verify production behavior at its real boundary.

### 4. Specify Evidence and Handoff

Define a pass criterion and evidence for every required check. For observed results, identify the checked revision or artifact, target, and result. For a new or changed automated harness, specify how to prove discovery, an intentional assertion failure, and a passing result after restoration. Treat missing discovery, harness errors, and unavailable dependencies as distinct from a failed behavior assertion.

## Output

Read the [Test Strategy Template](assets/test-strategy-template.md) when drafting or revising the strategy. Keep the applicable sections and matrix columns in template order unless the caller supplies another format. Write to the requested or established location when available. Otherwise provide the strategy in the response.

## Verification Checklist

- Every material risk has a check at an appropriate boundary or an explicit gap with a next action. Cross-unit risks are covered at the relevant handoffs.
- Each required check has a trigger, execution point, feasible environment and target, and an observable pass criterion with evidence to capture.
- Tooling, test data, and real or substituted dependencies match the intended coverage. Manual checks identify the procedure, expected result, and verifier.
- The handoff identifies outstanding setup and how to prove harness readiness. Results already observed identify what was checked. Unrun checks are marked as planned.
