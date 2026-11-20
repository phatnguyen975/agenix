# Design Shared Web UI Foundations

## Applicability and Inputs

Apply this step when the approved scope includes an owned web UI. If it does not, report the reason and leave the worktree unchanged.

Read project instructions and `config.agenix.json` for scope, targets and documentation language. Use the merged PRD, feature catalog and relevant feature records for users, journeys, accessibility, localization and product context. Read the approved domain model, applicable system design and tech stack for shared terminology, client responsibilities and supported browsers. If an approved database design exists, consult it only when data ownership, availability or lifecycle affects an interface decision. Use existing approved brand assets and UI foundations when available.

Verify upstream approval and revisions under the shared phase rules. Ask about material gaps in brand direction, target users, supported languages, styles, themes or accessibility targets. Reuse confirmed decisions and group independent questions. Check available evidence before requesting it again.

## Outputs

Create `docs/blueprint/ui-design/`:

```text
ui-design/
├── README.md
├── index.html
├── styles.css
├── app.js
├── assets/         # when visual assets are needed
└── data/           # when scenario fixtures are needed
```

Write the README using the [UI Design Template](../assets/ui-design-template.md). It owns shared visual and interaction rules. Use the approved demo revision as design-time evidence. The demonstration uses lightweight HTML, CSS and JavaScript. Additional files under the directory are allowed when they make the demo clearer.

The screens are representative illustrations of shared rules. Later feature designs apply these rules to their own scope and define their own requirements and acceptance. Preserve the historical demo after production work starts and exclude it from production packaging.

## Develop the Shared Direction

1. Frame a brief from the approved inputs: audience, primary activities, product context, constraints and required targets. Apply [Frontend Design](../../frontend-design/SKILL.md) to establish and critique a coherent visual direction, typography, layout and interaction character suited to that brief.
2. Use [UI/UX Pro Max](../../ui-ux-pro-max/SKILL.md) as design research. For a new global direction, run its `--design-system` search with non-sensitive product and style terms. Examine relevant style, palette, typography and UX suggestions. Validate applicability and accessibility against the brief. Use focused domain searches for specific gaps. Treat results as candidates, combine them with the visual direction above, and write decisions in the owning README. Do not persist a second generated design system.
3. Use [Canvas Design System](../../ui-styling/references/canvas-design-system.md) selectively for composition, visual hierarchy or spacing when it adds useful guidance. Keep framework-specific utility and component implementation rules in the applicable conventions.
4. Propose material alternatives where the brief leaves a consequential direction open. Present the rationale and trade-offs. Obtain human confirmation of the direction, supported themes and languages, and other material design decisions before building dependent work. Reuse existing approvals.

## Build and Verify the Demonstration

Select a small set of representative scenarios and states that exercises shared navigation, layout, components and feedback across the approved product scope. Choose examples for their coverage of shared rules, including applicable loading, empty, error and success states. Use synthetic data. Provide clear instructions to start, select, reset and replay each scenario deterministically, including theme and language switches when applicable. Do not invent production behavior or claim feature acceptance.

Implement one authoritative set of shared tokens and reference it from the README. Keep semantic names for colors, typography, spacing, motion and other applicable values. Record concrete component and interaction criteria, mobile-first layout and supported viewport/browser expectations, keyboard and focus behavior, accessibility targets, localization and theme behavior. Confirm logo or image rights and use approved assets or clearly identified representative assets.

Replay every selected scenario in a real browser before the design gate. Check layouts at the approved viewport matrix, responsive behavior, keyboard navigation, focus, interaction and visible states. Inspect screenshots where useful and correct discrepancies between the rendered demo and README. Use [Playwright CLI](../../playwright-cli/SKILL.md) when available and selected for replay. Use [Accessibility](../../accessibility/SKILL.md) for targeted accessibility checks, including automated and manual evidence where available. Use available browser tools when a particular tool is unavailable. Report exact results, coverage and blockers. Automated checks alone do not establish full accessibility conformance.

## Approve and Publish

Prepare the root documentation map update for the candidate using [Configure Instructions and Scope](../../../references/project-content.md#configure-instructions-and-scope). Include it in the same approval and publication.

Apply [Artifact Gates](../../../references/workflow-control.md#artifact-gates) to the README and demonstration together. Present the shared direction, representative scenarios, supported targets, browser evidence, outstanding limitations and intended publication. Obtain human review of the rendered UI and material design decisions. After approval, [publish the candidate](../../../references/git-publication.md#publish-the-approved-candidate) on the architecture branch and bind approval and verification evidence to the published revision in the phase PR or a durable checkpoint. Follow the shared phase and session rules.
