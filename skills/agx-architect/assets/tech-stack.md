# Technology Stack

<!--
Replace placeholders with approved project choices and remove authoring comments.
Use project release-unit names and link to the PRD, approved design and relevant
ADRs. Include only applicable components and environments.
-->

## Design Basis

<!--
Link the approved domain and system design where applicable.
List the drivers and constraints that materially affect technology choices.
Record relevant team, maintenance or budget constraints.
-->

## Client Design

<!--
For frontend-only projects, confirm this design before choosing dependent tools.
For other scopes, include this section only where applicable and link existing
system decisions. Describe runtime and rendering, routing, state ownership,
client storage, security boundaries and external integrations. Name the client
targets and clarify which decisions and data belong to external providers.
Omit this section when there is no owned client.
-->

## Release Units and Shared Technologies

<!--
List each release unit with its role, target and release boundary. Repeat the
technology table per unit. Include separate roles inside a joint release where
selections differ, and link shared entries instead of duplicating them.
Cover applicable languages, runtimes, frameworks, build and package tooling,
persistence, messaging, caching and operational tooling. Include testing tools
only when already mandated or approved. Record compatibility constraints that
will inform the test strategy. Record approved exact versions or supported
ranges and the intended pin.
-->

### <Release Unit or Shared Scope>

| Component and Responsibility | Selected Technology | Version and Pin                     | Driver, Rationale or ADR        |
| ---------------------------- | ------------------- | ----------------------------------- | ------------------------------- |
| <Component and role>         | <Technology>        | <Version or range and pin location> | <Driver and reason or ADR link> |

## Service Placement

<!--
For each applicable environment, identify the implementation and where it runs.
Distinguish a self-hosted process or container from a managed provider product.
Identify an image by repository and approved tag or digest. For managed services
record engine compatibility, provider version policy and relevant plan or region.
Name the party responsible for operation, upgrades and recovery. Describe
environment differences that affect behavior or verification. Keep secrets out.
-->

| Component   | Environment   | Hosting and Provider or Image                     | Version or Compatibility     | Operating Owner and Constraints |
| ----------- | ------------- | ------------------------------------------------- | ---------------------------- | ------------------------------- |
| <Component> | <Environment> | <Deployment model and product or image reference> | <Version or provider policy> | <Owner and material limits>     |

## Compatibility and Verification

<!--
Record cross-unit compatibility, required extensions and version constraints.
List checks and evidence needed to enforce decisions. Link existing verified
evidence where available. Leave executable setup commands to scaffold.
-->

## Decisions and Revisit Conditions

<!--
Link significant ADRs from the matching choices above. Record remaining risks
accepted by the human, conditions for revisiting a choice, and deferred optional
decisions with their trigger. Keep unapproved material choices out of the baseline.
-->
