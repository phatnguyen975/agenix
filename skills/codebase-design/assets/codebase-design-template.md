<!--
OUTPUT TEMPLATE — Codebase Design

How to use:
1. For a full design, keep the ten numbered top-level sections and the listed subsections.
2. Replace every `{{placeholder}}` with a verified project-specific value.
3. Delete all instructional HTML comments and illustrative rows before delivering.
4. Use "Not applicable — <specific reason>" for a truly inapplicable subsection;
   do not leave an empty table, heading, code fence, or bare "TBD".
5. For full/material structural design with discretionary choices, present a
   preliminary structure and obtain human decision approval before adopting it.
   If all decisions were already approved or mandated, cite that authority.
   Otherwise label the proposal Pending Approval and any material unknowns.
6. Repeat rows, ownership groups, trees, check entries, migration steps,
   and optional convention subsections only where useful.
7. Use the project's real paths, names, ownership, and framework conventions.
8. Rule IDs DR-xx / CV-xx / EN-xx are unique within each prefix and stable;
   G-xx identifies observed gaps. Example IDs are illustrative: renumber to match
   the adopted document and keep references synchronized.
9. Sections 5 and 9 define constraint/check mappings; module-specific allowed edges
   appear in section 4 (or one referenced canonical dependency group).
10. A tree shows meaningful boundaries/entry points, not an exhaustive file listing.
    Add an annotation for each shown entry explaining its structural role.
11. No patterns, contracts, shared packages, test types, or checks are mandatory
    merely because this template contains a place for them.
12. A focused review or partial update can operate on relevant sections only;
    it is not required to instantiate this entire template.
13. Every DR-xx and CV-xx rule must link to an EN-xx entry (active check,
    specific human review, or explicit enforcement gap), including rules in
    sections 6 and 7. Do not state a planned check is active.
14. For material decisions, capture an alternative or constraint considered,
    the resulting trade-off, approval status, and a revisit trigger if provisional.
    Approval of a document design does not authorize changing production code.
15. Use tables only for concise, comparable facts (at most four columns here).
    Keep cell text short; put long paths, explanations, exceptions, and evidence
    in adjacent bullets or annotated trees. If populated cells would force
    horizontal scrolling on GitHub, replace that table with keyed lists.
16. `{{...}}` markers are plain-text placeholders, not a templating-language
    requirement. Keep them visible in GitHub previews; replace all before use.
-->

# Codebase Design: {{project_name}}

## 1. Scope and Forces

<!-- Describe in 2–4 sentences what code organization this document governs,
including repository scope, scope exclusions, and authoritative project constraints.
Keep the approval fields below concise. "Approved" requires an explicit recorded
user/project decision; a fully specified mandated structure can cite that authority.
A draft may be Pending Approval but must not be presented as adopted. -->

{{scope_status_evidence_constraints}}

- **Structural Decision Status:** {{proposed_pending_approval_or_approved}}.
- **Decision Authority / Evidence:** {{approval_reference_or_pending_owner}}.

### 1.1 Release Units

<!-- One concise row per independently distributed/published/deployed unit.
`Purpose` names the key responsibility and consumer class, not a full
specification; `Ships` identifies the artifact and whether its release
cadence is independent. Put long target or artifact paths in a bullet
below the table, keyed by unit. Build-only internal targets belong to the
owning release unit. Single-unit repositories have one row. Unknown ownership
is unresolved in proposals, never asserted as adopted. -->

| Unit     | Purpose     | Ships     | Owner     |
| -------- | ----------- | --------- | --------- |
| {{unit}} | {{purpose}} | {{ships}} | {{owner}} |

### 1.2 Forces

<!-- Bullet only decision-relevant conditions: change locality, integration
volatility, ownership, published consumers, framework/build constraints, security
separation, testability, and existing structural issues. Cite a source path or
requirement where important. "Low complexity" without evidence is insufficient.
For a material choice, keep a short decision note with the selected option,
strongest alternative, cost, and approval status; avoid duplicating detail from
sections 2–5. Delete the example decision note if choices are already mandated. -->

- {{force_and_evidence}}

**Material Decision Notes:**

- **{{decision_name}}:** {{selected_option_and_decisive_force}}; **Alternative / Cost:** {{credible_alternative_and_tradeoff}}; **Status:** {{decision_approval_status}}.

## 2. Repository Layout

### 2.1 Repository Strategy

<!-- State monorepo, polyrepo, or hybrid, with each relevant repository and the
reason for its grouping. Distinguish repository from release boundaries. For a
single existing repository, say it is retained and why. -->

{{repo_strategy_and_tradeoff}}

### 2.2 Root Layout

<!-- Repeat one annotated tree per repository. Use real folder names and role
annotations. Show the root of a single-unit repo even when the unit is at root.
If repositories are inaccessible, label the tree a "proposed layout". -->

```text
{{repo_root}}/
├── {{release_unit_dir}}/      # {{owned_unit_role}}
├── {{optional_shared_pkg}}/     # {{shared_purpose_owner}}
└── {{docs_dir}}/     # {{design_doc_location}}
```

## 3. Code Organization Strategy

### 3.1 Primary Organization

<!-- One row per release unit. Use "package by feature/capability", "package by
component", "package by layer", "package by use case/operation", or a
framework-constrained hybrid. These may combine; identify the dominant grouping
and any meaningful secondary grouping. Operation folders are not automatically
modules or release units. Explain shared-invariant ownership and the decisive
forces/trade-off. The presence of layers does not imply a single module. -->

| Unit     | Strategy     | Trade-Off    |
| -------- | ------------ | ------------ |
| {{unit}} | {{strategy}} | {{tradeoff}} |

### 3.2 Module Structure

<!-- Repeat for substantive modules only. Internal patterns are optional and can
combine; possible values: simple, layered, ports and adapters, vertical slices,
pipes and filters, presentation-state separation. Record the forces, not arbitrary
complexity scores. An internal-only module is valid. -->

| Module     | Pattern(s)  | Rationale     |
| ---------- | ----------- | ------------- |
| {{module}} | {{pattern}} | {{rationale}} |

### 3.3 Unit Layout

<!-- Repeat one annotated tree per release unit. Show the package/module
boundaries, significant entrypoints, actual exported public surfaces if any,
and framework-required roots. Do not substitute an imagined file layout. -->

```text
{{release_unit_path}}/
├── {{module_a}}/                   # {{responsibility_and_boundary}}
└── {{module_b}}/                   # {{responsibility_and_visibility}}
```

### 3.4 Pattern Layout

<!-- Show one focused annotated tree for each materially different internal
pattern variant that needs explaining. One universal pattern tree is NOT required
for modules with different idioms. If all modules are simple or patterns are
fully represented in Unit Layout, write "Not applicable — ..." instead. -->

```text
{{representative_module_path}}/
├── {{role_a}}/          # {{purpose_and_import_direction}}
└── {{role_b}}/          # {{purpose_and_visibility}}
```

## 4. Module Catalog

<!-- Group modules under their owning release unit or shared package; repeat
this subsection as 4.2, 4.3, etc. The group owner is the default module owner;
list module ownership exceptions after the public-surface details. `Direct Edges`
means PERMITTED DIRECT static source imports or build edges (state the edge kind
for this document), not observed edges or runtime calls. Use short module names,
"None", or a named dependency group defined in section 5. Put public surfaces
and long dependency details in bullets keyed by module. "Internal only" is valid. -->

### 4.1 {{unit_or_package}}

**Owner:** {{default_owner}}. **Dependency Edge:** {{source_import_or_build}}.

| Module     | Purpose     | Direct Edges |
| ---------- | ----------- | ------------ |
| {{module}} | {{purpose}} | {{allowed}}  |

**Public Surfaces:**

- **{{module}}:** {{surface}}.

<!-- Optional: list only module owners differing from the group owner. Delete
this block when ownership does not differ. -->

**Ownership Exceptions:**

- **{{module}}:** {{different_owner}}.

## 5. Dependency Rules

<!-- Record cross-cutting rules, not a duplicate of every module allowlist.
Do not mark a proposed DR rule adopted when the structural direction still
awaits approval. Existing imports forbidden by a new rule need a documented
migration gap/exception, not an assumption that they have already changed.
Each `Constraint` includes the affected nodes, static edge kind, and
allowed or forbidden direction. Define named dependency-group membership below
this table when used by section 4. Keep exceptions short in the table; put
scope, reason, owner, and review trigger in keyed bullets if they do not fit.
Each DR-xx links to a real EN-xx entry or an explicit enforcement gap. If only
per-module allowlists apply, describe their enforcement without inventing a
redundant DR-xx. -->

| Rule  | Constraint     | Exception  | Check |
| ----- | -------------- | ---------- | ----- |
| DR-01 | {{constraint}} | {{except}} | EN-01 |

## 6. Shared Code Policy

### 6.1 Shared Packages and Modules

<!-- Include code intentionally shared across module/release boundaries, not
private helpers. Put owner and public paths/contracts in the keyed bullets
immediately below so tables remain narrow. If none, write "Not applicable —
no cross-module shared packages are proposed" (remove the table and bullets). -->

| Shared Unit | Purpose     | Consumers     |
| ----------- | ----------- | ------------- |
| {{shared}}  | {{purpose}} | {{consumers}} |

**Ownership and Public Surfaces:**

- **{{shared}}:** **Owner:** {{owner}}; **Public Surface:** {{exports_or_contract_location}}.

### 6.2 Ownership, Change, and Contract Policy

<!-- Assign CV-xx IDs to substantive shared-code/contract governance policies;
put import restrictions in section 5 as DR-xx. Record approval, consumer
review/verification, and compatibility for published interfaces (do not impose
Semantic Versioning on private modules). Below the table, key each relevant
cross-unit contract's source path, consumers, compatibility policy, and
verification owner by its CV-xx ID; do not cram paths into cells. Delete
non-applicable example rows, or use "Not applicable — ..." for the subsection. -->

| Rule  | Policy     | Owner     | Check |
| ----- | ---------- | --------- | ----- |
| CV-01 | {{policy}} | {{owner}} | EN-02 |
| CV-02 | {{policy}} | {{owner}} | EN-03 |

<!-- Required only for each recorded cross-unit contract; remove otherwise. -->

- **CV-02 Contract Details:** {{source_path}}; {{consumers}}; {{compatibility_policy}}; {{verification_owner}}.

## 7. Conventions

### 7.1 Naming and Public Surfaces

<!-- Name module/path/public-entry conventions and how consumers discover
module APIs; use project language/framework idioms and do not copy formatter
configuration. Assign each genuine CV-xx a unique ID and an EN-xx mapping. -->

| Rule  | Convention     | Owner     | Check |
| ----- | -------------- | --------- | ----- |
| CV-03 | {{convention}} | {{owner}} | EN-04 |

### 7.2 Error Boundaries

<!-- Describe failure categories and where module-specific or vendor errors
are translated for consumers. If no meaningful error boundary exists (for
example static assets), replace the table with "Not applicable — ...". -->

| Rule  | Convention     | Owner     | Check |
| ----- | -------------- | --------- | ----- |
| CV-04 | {{convention}} | {{owner}} | EN-05 |

### 7.3 Additional Structural Conventions

<!-- OPTIONAL: Rename this subsection to one topic (for example "Dependency
Composition", "Configuration Ownership", "Logging Boundaries", "State
Ownership", or "Generated Sources"). Repeat as 7.4, 7.5, ... only if relevant.
If none, replace the table with "Not applicable — no additional structural
conventions are required". -->

| Rule  | Convention     | Owner     | Check |
| ----- | -------------- | --------- | ----- |
| CV-05 | {{convention}} | {{owner}} | EN-06 |

## 8. Test Layout

### 8.1 Test Types and Placement

<!-- Include only applicable unit/module/integration/contract/E2E or equivalent
types. A library need not have E2E tests. State colocated, mirrored, or hybrid
placement and naming pattern; put long paths in bullets keyed by test type. -->

| Type     | Boundary  | Location | Stage     |
| -------- | --------- | -------- | --------- |
| {{type}} | {{scope}} | {{path}} | {{stage}} |

### 8.2 Module and Boundary Mapping

<!-- Map substantive modules to their primary tests or explain that their
behavior is verified through a larger test boundary. Add contract/provider or
cross-unit tests only when relevant and identify ownership. -->

| Module / Contract | Tests     | Owner     |
| ----------------- | --------- | --------- |
| {{boundary}}      | {{tests}} | {{owner}} |

### 8.3 Fixtures and Test Doubles

<!-- Define fixture owner, where shared test support lives, any legitimate test
visibility exception, and that production may not import test support. If no
fixtures/doubles are needed state "Not applicable — ...". -->

- {{fixtures_and_test_doubles_policy}}

## 9. Enforcement

<!-- Use one keyed list entry per unique EN-xx; an entry may cover many DR/CV
rules, and a rule may link to multiple checks. Repeat the example for each
populated rule in sections 5–7 and do not duplicate an EN ID. State the actual
check and what sources/edges it covers; "CI" alone is not a mechanism. Include
review trigger for human review, or explicitly mark a gap. The illustrative
CV-01–CV-05 rows refer to EN-02–EN-06: create those check entries if keeping
the rules, otherwise remove the rows and unused IDs. Do not mark planned
checks Active; evidence must come from an observed execution or review. -->

- **EN-01 — {{check_name}}**
  - **Rules:** DR-01.
  - **Mechanism / Scope:** {{mechanism_and_paths_or_gap}}.
  - **Stage:** {{local_ci_review_or_unscheduled}}.
  - **Owner:** {{owner}}.
  - **Status:** {{active_proposed_or_gap}}.
  - **Evidence / Limitations:** {{observed_evidence_or_not_run}}.

## 10. Restructuring Path

### 10.1 Current Gaps

<!-- Existing-codebase restructuring only; each gap must reference observed
paths or dependency edges, a rule, affected consumer, and a related step.
If not restructuring, state "Not applicable — new design" or
"Not applicable — no structural changes requested". Never infer violations
from stylistic preference alone. -->

| Gap  | Evidence / Impact | Rule        | Step     |
| ---- | ----------------- | ----------- | -------- |
| G-01 | {{evidence}}      | {{rule_id}} | {{step}} |

### 10.2 Migration Steps

<!-- Use an ordered list: steps carry too much distinct information for a
readable table. Repeat one item per small, dependency-ordered, reviewable change.
Link observed gap IDs, name owner, test/check evidence, and compatibility or
release recovery (source revert alone may not reverse published changes).
"Verified" requires executed checks and evidence, not merely a plan. For new
code or review-only tasks, use a specific Not applicable reason. -->

1. **{{step_title}}** — {{proposed_in_progress_blocked_or_verified}}
   - **Change / Prerequisites:** {{change_and_preconditions}}.
   - **Addresses:** G-01.
   - **Owner:** {{owner}}.
   - **Verification / Evidence:** {{executed_or_planned_checks}}.
   - **Compatibility / Recovery:** {{contract_compatibility_and_release_recovery}}.
