<!--
Place this managed region in AGENTS.md at an approved module or release-unit root.
Preserve team-owned sections and keep the accompanying CLAUDE.md as a thin adapter. Use
the project's approved documentation language. Remove authoring comments, placeholders
and inapplicable sections.
-->
<!-- agenix:begin -->

## Scope and Ownership

<!--
State the repository-relative root, owning unit or module, responsibility and public
boundaries. Link the nearest ancestor instructions. Describe relevant boundaries for
edits and cross-scope dependencies.
-->

- **Scope:** `<repository-relative path>`
- **Ownership:** <responsibility and public boundaries>
- **Parent instructions:** [AGENTS.md](relative-path-to-parent-AGENTS.md)

## Designs and Contracts

<!--
Link only the approved design, contracts, conventions and feature guidance applicable to
this subtree. Include a short local explanation when needed to apply the reference. Use
relative links from this file.
-->

- <What the artifact governs> — [<artifact or section>](relative-path-and-anchor)

## Verified Operations

<!--
List the approved command or check IDs for this scope with their working directory,
target and mode when relevant. Link to the verified environment using a path relative to
this file. Include only verified operations.
-->

- `<command or check ID>` — <working directory, target and mode>
- [Verified Environment](relative-path-to-environment.agenix.json)

## Scope Guardrails

<!--
List only rules specific to this scope, including allowed access, approval requirements
and disallowed actions where applicable. Apply root rules and workflow authority
throughout.
-->

- <Scope-specific restriction and the context where it applies>

## Child Scopes

<!--
List actual child instruction entries with a one-line responsibility. Omit the section
if there are none.
-->

- <Child scope and responsibility> — [Scope Instructions](relative-path-to-child-AGENTS.md)

<!-- agenix:end -->
