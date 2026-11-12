# Review and Restructuring

## Purpose and Boundaries

Assess **current source-code structure**, identify maintainability risks with evidence, and recommend improvements. When a structural change is selected for further design, define a **target structure and incremental migration** in the Design path. A review alone neither approves a target architecture nor authorizes code changes.

A read-only assessment may be focused, repository-wide, continuous (against new changes), or periodic. A recurring cadence is set by the user/project, not by this reference. Refactoring improves internal design while preserving externally observable behavior; contract or behavior changes are different work and require explicit compatibility planning.

## Evidence-Based Assessment

1. **Inventory the requested scope.** Identify repositories, release units, build packages, module owners, shared packages, and significant cross-unit contracts. For repository-wide review, account for every unit even when deeper inspection is sampled.
2. **Inspect actual boundaries.** Locate entry points, public exports, internal implementation, declared dependency groups, state ownership, structural conventions, tests, and current enforcement.
3. **Build the relevant graph.** Distinguish direct static source/type imports, declared build dependencies, runtime communication, and generated/dynamic links. Map source artifacts to architectural modules before checking cycles or policy violations.
4. **Compare with authority.** Prefer approved design rules, project instructions, and language/framework constraints. Where no rule exists, describe an evidenced risk or improvement opportunity; a different style is not automatically a violation.
5. **Record evidence and limits.** Cite path/edge, manifest, check output, or change history. Separate unexamined units, inaccessible consumers, inferred dependencies, and unrun checks from verified observations.

For large repositories, do an inventory-level pass across release units and shared boundaries, then inspect risk-heavy areas and dependency-connected neighborhoods. **Sampling limits coverage claims**; mark it as partial, even when no sampled issue is found.

## Findings and Prioritization

Classify each `G-xx` finding by **type**, **severity**, **confidence**, and **recommendation**; these are distinct fields:

| Field      | Meaning                                                                                                         |
| ---------- | --------------------------------------------------------------------------------------------------------------- |
| Type       | `Violation` of an established rule, evidenced `Risk`, or `Opportunity` for better structure                     |
| Severity   | `Critical`, `High`, `Medium`, `Low` — actual or credible harm/consumer impact                                   |
| Confidence | `Verified` from examined evidence, `Likely` with supporting but incomplete evidence, or `Unverified` hypothesis |
| Priority   | Action ordering from risk reduction, urgency, effort, ownership, and prerequisites; need not equal severity     |

**Severity guidance:** Critical requires strong evidence of an urgent, consequential structural failure (for example, known release-blocking contract break). High involves significant consumer coupling or change/release risk; Medium involves localized but material maintenance friction; Low is limited impact. Do not assign Critical solely for a pattern preference. A security issue outside structural scope should be handed to the appropriate review, not silently reclassified as a codebase-layout violation.

Each finding should include evidence (path/import/check), expected boundary and its source, affected consumers, impact, confidence explanation, smallest feasible remediation, and verification unknowns. **No finding** means none established **within the examined scope**, not proof of whole-repository health.

**Example:**

```text
G-01 — Type: Violation — Severity: High — Confidence: Verified
Evidence:  Checkout/application imports Orders/internal/storage.
Authority: Approved DR-01 allows Checkout → Orders/public only.
Impact:    Checkout changes when Orders storage representation changes.
Proposal:  Introduce/use an Orders-owned public operation; then remove the
           internal import and enforce DR-01.
```

A proposed new rule is not an approved violation criterion: document the risk first, then propose the rule through the Design path if it warrants a new architectural commitment.

## Recommendations and Periodic Comparison

- Prefer the smallest change that removes an evidenced risk, preserving effective existing boundaries. State a plausible alternative and trade-off for consequential recommendations.
- Rank recommendations as **Now / Next / Later** or the project's existing prioritization scheme. Record expected benefit, owner when known, prerequisites, consumer impact, and decision required. Do not equate high severity with permission to implement.
- For periodic reviews, compare against an accessible previous snapshot by actual issue identity (paths/rules/consumers), classifying **new, persisting, resolved, or unverified**. `G-xx` IDs are unique within each report; the same number in another report does not establish continuity.
- Report current check coverage, new or reduced violations, and remaining blind spots. Do not invent trends, test results, or previous review history.
- Keep the review improvement plan **high-level**. A detailed source migration plan belongs with a proposed or approved target design, not as an implicit part of a read-only review.

## Target Design and Delta

When the user requests a structural redesign or migration, enter the **Design Path** in `SKILL.md`:

1. Describe the smallest target responsibility, module boundary, public surface, and permitted static graph that addresses the approved objective.
2. Compare observed and proposed paths/edges; distinguish internal-only changes from consumer-visible imports, contracts, build/release boundaries, and ownership changes.
3. Identify supported consumers, existing exceptions, and compatibility obligations. If external consumers cannot be inventoried fully, clarify the required support and compatibility policy with the human; do not assume unknown clients are safe to break.
4. Resolve any material target-design ambiguity with the human, then present concrete choices, consequences, and alternatives at the Human Gate before adoption; existing approvals need not be repeated.
5. Link relevant findings to target `DR`/`CV` rules and `EN` checks. A new constraint is not proof the current code violates an already-accepted rule.

```text
Current: Checkout → Orders/internal/storage  (observed static import)
Target:  Checkout → Orders/public            (proposed allowed import)
Delta:   introduce owned public operation; migrate Checkout; remove backdoor
Check:   inspect imports and validate the intended graph after each step
```

## Migration Techniques

| Technique               | Useful For                                         | Critical Condition                                                             |
| ----------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------ |
| Move / Extract / Rename | Local responsibility or path cleanup               | Preserve consumed behavior and update all relevant imports/build/tests         |
| Parallel Change         | Interface changes across non-atomic consumers      | Expand compatibility, migrate consumers, then contract only when safe          |
| Branch by Abstraction   | Gradual replacement of an implementation           | Introduce one useful seam and remove temporary indirection if no longer needed |
| Module Extraction       | Carving a responsibility from tightly coupled code | Define ownership/public surface and move clients incrementally                 |
| Cycle Breaking          | Static architectural dependency cycles             | Show the revised graph; events do not automatically remove static edges        |
| Strangler Fig           | Gradual large-subsystem/application replacement    | Use only when the problem genuinely involves subsystem modernization           |

Do not use migration patterns as mandatory recipes. Branch by Abstraction and Parallel Change can be combined. A code-only refactor may require no contract versioning; independently released consumers may require a compatible period even within one repository.

## Migration Planning and Acceptance

Plan small, dependency-ordered and recoverable steps; use the **Design Template**'s optional migration section for a full persistent plan. Each step records:

- **Preconditions:** affected consumers, known baseline, approvals, build/test ability, and required compatibility window.
- **Change:** exact ownership/public-surface or static-graph delta, plus generated artifacts and manifest updates where relevant.
- **Verification:** runnable scope, positive/negative boundary checks when applicable, consumer compatibility, and actual result or `Not Run`/`Blocked`.
- **Recovery:** source rollback _and_ separately the release/consumer recovery approach when already-published artifacts cannot simply be reverted.
- **Responsibility:** owner, related `G-xx` finding or target rule, and completion evidence.

**A possible order is:** capture baseline → guard against new violations → add compatible seam → migrate consumer groups → remove obsolete access → tighten checks. Reorder based on actual dependencies. Never remove an old interface while supported consumers still need it.

A passing local test cannot prove compatibility with unknown external consumers; a step is complete only against its declared, executed acceptance criteria. Keep intentional behavior changes separate from behavior-preserving structure changes when practical.

## Approval and Change Classification

- **Review** reports findings without a Human Gate. Approval of a _proposed structural direction_ is needed for material new Design choices, except already approved/mandated choices.
- **Documents versus code:** permission to write a design report is separate from accepting its architecture; accepting architecture is separate from permission to edit source. Check exact execution scope before destructive or consumer-impacting changes.
- **Administrative:** documentation clarification without consumer effects. **Additive:** change preserving established consumers. **Potentially Breaking:** any change to consumed paths, contract semantics, dependency permissions, ownership, or build/release boundaries; unknown consumer effect is not assumed additive.
- **Late discoveries:** return only materially changed decisions to the Human Gate. Preserve stable `DR`/`CV`/`EN` IDs in the living design; retire/supersede rather than repurpose.
