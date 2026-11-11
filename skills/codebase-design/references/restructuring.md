# Current-State Review and Restructuring

## Purpose

Inspect an existing codebase, distinguish observed structural defects from preferences, and plan **incremental, recoverable** movement toward a justified target. The goal is safer maintenance, not a full rewrite or forced conformity to a fashionable tree. Review-only requests stop after findings unless the user asks for a migration plan or changes.

## Evidence-Based Scan

Inspect only the relevant scope first; expand when a dependency crosses it:

1. **Build and release inventory:** repository paths, manifests, package boundaries, independently published artifacts, entry points, and generated code.
2. **Module inventory:** responsibilities, ownership, public exports, internal folders, conventions, test locations, and their confidence level.
3. **Static dependency graph:** actual imports, build references, exports, and graph edges. Map files/packages to architectural modules; differentiate production, tests, generated sources, and third-party dependencies.
4. **Runtime boundary evidence:** when a finding concerns cross-unit coupling, identify whether it is a static import, a contract, or runtime communication. Do not infer static dependencies from service names.
5. **Violation evidence:** path/edge, affected owners/consumers, applicable `DR-xx` or `CV-xx`, impact, and available proof.
6. **Unknowns:** graph blind spots, undocumented consumers, dynamic imports, code generation, third-party constraints. Ask for material unknown facts before disruptive work; mark others unverified.

For large projects sample by release unit or dependency-connected change region, then expand the scan around observed cross-boundary edges. Sampling is not proof that the entire repository is compliant.

## Findings and Severity

Each review finding records:

| Field             | Required Content                                                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Evidence          | File path/import or manifest/reference proving the behavior                                                                                 |
| Expected Boundary | Existing or proposed rule and source of authority                                                                                           |
| Impact            | Change coupling, visibility leak, risky shared state, build/test friction, or another specific consequence                                  |
| Severity          | Critical / High / Medium / Low based on demonstrated consumer impact, security exposure, or change risk; do not inflate a naming preference |
| Confidence        | Verified / Likely / Unverified (do not label inferred edges as verified)                                                                    |
| Recommendation    | Smallest useful structural change, with alternatives where material                                                                         |
| Migration Risk    | Public consumer impact, versioning, compatibility, data or environment preconditions                                                        |

Prioritize by actual risk: cross-module hidden writes and release-breaking imports usually outweigh a merely unfamiliar directory name. A pattern preference is not a violation without a project requirement, demonstrable coupling, or maintainability impact.

## Target State and Delta

1. Describe the minimal target boundaries and dependency graph; retain unaffected code and existing public paths.
2. Identify exactly which changes are **internal** versus **consumer-visible**. An internal move can still break imports if consumers illegally rely on internals.
3. Identify unchanged contracts that should survive the migration and any planned compatible replacements.
4. Link each gap to a target rule; if the rule is new, justify it rather than retroactively declaring all existing code defective.
5. Record unresolved dependencies or external owners before locking in a breaking change.

**Example:**

```text
Observed: Checkout imports Orders/internal/db (verified static edge).
Target:   Checkout → Orders/public; Orders/internal/db remains private.
Gap:      G-01 violates DR-01 (public-entry boundary).
Change:   Add needed order operation to Orders/public, migrate Checkout,
          ban the internal import, then remove the exception.
```

This describes a structural change without fabricating business method signatures.

## Migration Techniques

| Technique                                 | Appropriate Situation                                           | Main Precaution                                                                                              |
| ----------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Move/Rename/Extract (refactoring)         | Local responsibility or import-path cleanup                     | Preserve externally observed behavior; update references and tests                                           |
| Parallel Change (Expand–Migrate–Contract) | Public API/contract cannot change atomically                    | Keep old and new forms compatible during migration; remove old only after consumers move                     |
| Branch By Abstraction                     | Widely used dependency/implementation needs gradual replacement | Introduce one stable seam, migrate clients gradually, then remove temporary abstraction if unnecessary       |
| Incremental Module Extraction             | Code from one boundary is moved behind a new module interface   | Extract ownership and tests first; avoid simultaneous behavior redesign                                      |
| Cycle Breaking                            | Strongly connected **static** module graph                      | Change ownership, extract legitimate shared abstraction, invert one edge, or merge truly inseparable modules |
| Strangler Fig                             | Gradual replacement of a legacy application or large subsystem  | Applies to system/subsystem modernization, not a synonym for renaming a folder                               |

**Do not confuse:** Branch By Abstraction (an intermediate code seam) and Parallel Change (an interface compatibility sequence) are complementary, not substitutes chosen solely by client count. Either can be used without introducing a network boundary.

## Safe Step Ordering

Order by prerequisites, not an inflexible universal sequence:

1. Establish a reliable test/build baseline and record unverified behavior. Add characterization tests when behavior preservation is otherwise not demonstrable.
2. Install checks or a narrow legacy violation baseline so new violations do not accumulate.
3. Introduce a public seam or compatible contract where consumers require it.
4. Redirect one consumer or one dependency cluster at a time; preserve old paths where external consumers cannot migrate in one change.
5. Move implementation ownership and remove back-edges; update test-support placement and dependency permissions.
6. Verify consumer compatibility and remove obsolete exports/adapters/exception entries only after the necessary migration window.
7. Tighten enforcement and verify target graph integrity.

Some steps require temporary dual implementations or compatibility adapters; these are valid if their removal criteria are explicit.

## Step Acceptance Criteria

Each migration step should specify **changed boundary, prerequisites, expected graph delta, tests/checks, rollback or release recovery, owner, and completion evidence**. In a full design document, present steps as an ordered list with these details under each step rather than a wide table.

- Keep changes reviewable and recoverable; do not promise every phase can preserve _all_ tests if a required test suite is broken initially—record and avoid regressions against an observed baseline.
- Separate behavior-preserving refactoring from intentional behavior changes in commits/reviews where feasible. When an interface must evolve, use explicit compatibility steps rather than pretending it is behavior-preserving.
- For a published contract, identify consumers and migration readiness before removing old exports or protocol forms.
- Account for generated code, build manifests, packaging, imports, and public paths; a source-only tree move may be incomplete.
- A step remains **proposed** or **in progress** until the declared checks have actually run and the completion evidence is recorded. A passing test suite does not prove compatibility with unobserved consumers.
- Distinguish source rollback (revert/refactor) from release recovery: published artifacts or independently deployed consumers may require a forward fix, compatibility adapter, or coordinated rollout rather than a simple repository revert.

## Approval and Delivery Boundaries

- **Proposed structural direction:** for a full or materially changed codebase design, present the candidate topology, modules, public surfaces, main dependency direction, forces, and alternatives at a human decision checkpoint **before** expanding into detailed rules and migration, unless those choices are already approved or mandated. Read-only findings do not require approval.
- **Document modification:** an explicit request to update a design file authorizes only the requested scope; clarify whether a previously accepted boundary would be replaced. Mark a proposal **Pending Approval** until approved.
- **Source restructuring:** approval of a design does not automatically authorize implementing it. Before destructive or consumer-impacting edits, identify affected paths/consumers, planned compatibility and recovery, and seek approval for that execution scope. Do not request approval twice for the _same_ precisely approved action.
- **Late discovery:** when a hidden consumer, changed ownership, or graph edge invalidates an approved decision, pause that portion, present the delta, and seek targeted re-approval. Continue unaffected review work only.

## Update Classification

- **Additive:** adds an internal module, rule, test-support location, or optional public capability without invalidating documented consumers.
- **Potentially Breaking:** moves/renames public paths, changes exports or error behavior, restricts currently used imports, changes contract compatibility, or reassigns ownership across independently evolving units.
- **Administrative:** documentation clarification or naming cleanup with no consumer effect.

Classify by **consumer impact**, not edit size. Preserve stable `DR/CV/EN` identifiers; retire or supersede an old rule instead of reassigning its ID to unrelated meaning. Request explicit confirmation before changing/removing consumer-visible contracts or performing destructive restructuring; a migration plan does not authorize executing it.
