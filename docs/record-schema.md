# Agenix — Configuration and Record Schema

This maintainer specification defines the data that workflow templates, parsers and validators must agree on.

## Serialization and Value Types

Read Git-owned `*.agenix.json` files as strict UTF-8 JSON. Reject duplicate keys at every depth, malformed JSON, non-finite numbers, unresolved conflict markers, undeclared fields and unsupported versions. Key order and whitespace do not affect field equality. Preserve meaningful array order, such as command arguments. Use empty arrays for known empty collections. Omit inapplicable and later-stage fields. A missing required field is an error.

Type notation uses JSON primitives, `T[]` for arrays and `?` for optional object keys. Strings are nonempty unless the value is an argument that intentionally contains an empty string.

| Type                      | Meaning                                                                                                                                                                                                                                                                       |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ProjectPath`             | Repository-relative `string` using forward slashes. Allow `.` for a working or release-unit root. Reject absolute paths, parent traversal and paths that resolve outside the project.                                                                                         |
| `Target`                  | `ProjectPath` with optional anchor, or an absolute HTTPS URL. Relative paths resolve from the project root in every tracker mode.                                                                                                                                             |
| `ArtifactRef`             | `{target: Target, revision?: string}`. Where pinning is required, use the full Git commit or an immutable external revision.                                                                                                                                                  |
| `EvidenceRef`             | `{target: Target, revision?: GitOID, checkpoint-id?: string}`. Require a commit for snapshot-specific Git evidence. Use `checkpoint-id` to select a checkpoint inside a JSON record. For a native check, PR or tracker message, verify its durable URL against the candidate. |
| `GitOID`                  | Full hexadecimal `string` in the repository's object format. Verify the expected object type.                                                                                                                                                                                 |
| `UtcTime`                 | RFC 3339 `string` ending in `Z`.                                                                                                                                                                                                                                              |
| `CheckID`, `AcceptanceID` | Stable `string` identifiers. Resolve checks in the approved environment and acceptance IDs in their owning requirements or task record.                                                                                                                                       |

### Managed Locations

Each Git-owned file contains one top-level JSON object with `schema-version: 1` (`integer`) and the expected `kind` (`string`). Use the declared paths and reject duplicate item or checkpoint IDs within their owning file or record set.

| Location                                                     | Kind or Format                                                          |
| ------------------------------------------------------------ | ----------------------------------------------------------------------- |
| `config.agenix.json`                                         | `config`, written by setup.                                             |
| `environment.agenix.json`                                    | `environment`, written at final scaffold.                               |
| `docs/features/catalog.agenix.json`                          | `catalog`, the index of feature records in every tracker mode.          |
| `docs/features/<feature-id>/feature.agenix.json`             | `feature`, in every tracker mode.                                       |
| `docs/features/<feature-id>/tickets/<ticket-id>.agenix.json` | `ticket`, with embedded tasks in its `tasks` array. Local tracker only. |
| GitHub issue body or comment                                 | Markdown sections for definitions and checkpoints.                      |
| Jira description or comment                                  | Equivalent ADF paragraphs, lists and links.                             |

Root `AGENTS.md` links to the two root JSON files as they become available. Store Git-owned checkpoints in the owning feature, ticket or task's `checkpoints` array. Use `checkpoint-id` to identify a checkpoint within the file. Retain private drafts until the intended writes are reconciled.

### Schema Versioning

Keep `schema-version` when updating data under the same contract, including status changes, new tasks or checkpoints, and a new `plugin.revision` pin.

Increment `schema-version` when a format or semantic change makes existing helpers unable to read records correctly. Examples include renaming a field, changing its type, adding a required field or changing a status's meaning. With strict unknown-field rejection, a new optional field also requires a version bump once writers emit it.

For each version bump, document which versions the new helpers can read and whether existing records need migration. Update the templates, parser and validators together. Report unsupported versions without rewriting their records.

### Feature Catalog

The catalog has `features: {id: string, path: ProjectPath}[]`. Require unique feature IDs and paths. Each path must resolve to `docs/features/<feature-id>/feature.agenix.json`, and the ID must match the record. Publish catalog entries with their feature records. Read requirements, journeys, priority, dependencies and lifecycle state from the feature records when checking coverage or readiness.

## Project Configuration and Environment

Setup manages non-secret `config.agenix.json`. All fields are required unless marked conditional.

| Field            | Type                                                                   | Meaning                                                                                                                                                                                                                          |
| ---------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plugin`         | `{repository: string, revision: GitOID}`                               | HTTPS source repository and immutable commit used to resolve the compatible Agenix plugin and provision its helpers in CI.                                                                                                       |
| `github-repo`    | `string`                                                               | GitHub `owner/repository` of the project using Agenix. Branches, PRs and repository checks belong here.                                                                                                                          |
| `default-branch` | `string`                                                               | The project's Git default branch. Verify the configured `origin` against `github-repo`.                                                                                                                                          |
| `tracker`        | `local`, `github`, `jira`                                              | Store for ticket and task records.                                                                                                                                                                                               |
| `docs-language`  | `string`                                                               | Approved language. Setup defaults to `English`.                                                                                                                                                                                  |
| `project-scope`  | `frontend`, `backend`, `fullstack`, `library`, `cli`, `infrastructure` | Approved project scope.                                                                                                                                                                                                          |
| `targets`        | `string[]`                                                             | Nonempty, distinct platform or runtime IDs.                                                                                                                                                                                      |
| `exposure`       | `Exposure[]`                                                           | Conditional. Each entry has `action` (`release`, `deploy`, `apply`, or `enable`), `operation-id: string`, `target: string` and `input` (`merged-revision` or `verified-artifact`). Resolve it to an approved command before use. |
| `jira`           | `object`                                                               | Jira mode only. See the mapping below.                                                                                                                                                                                           |

For example, `plugin.repository` can be `https://github.com/example/agenix` while `github-repo` is `example/<project-name>`.

The Jira object holds `site-url` (HTTPS), `cloud-id`, and `project-key` as strings. Final setup requires:

- `issue-types: {ticket: string, task: string}`
- `dependency-link: {type-id: string, direction: "inward" or "outward"}`, measured from the dependent issue
- `status-targets`, an object keyed by `ticket` and `task`. Each maps `todo`, `in-progress`, `done` and `cancelled` to native status ID strings.
- Optional `field-defaults`, an object keyed by item type and native field ID. Each value must match its discovered native field type.

During configuration, omit undiscovered Jira mappings and report them as pending. Keep credentials in the private Jira credential file.

### Verified Environment

Scaffold writes `environment.agenix.json` with verified commands and controls. Keep shared settings in `config.agenix.json`.

| Field               | Type            | Meaning                                                                                             |
| ------------------- | --------------- | --------------------------------------------------------------------------------------------------- |
| `instruction-entry` | `"AGENTS.md"`   | Root instructions.                                                                                  |
| `units`             | `Unit[]`        | Nonempty list of release units.                                                                     |
| `commands`          | `Command[]`     | One approved command per operation, unit, target and mode.                                          |
| `services`          | `Service[]`     | Isolated services, possibly empty.                                                                  |
| `permissions`       | `Permission[]`  | Allowed, approval-required and prohibited operations by environment.                                |
| `evidence`          | `EvidenceRef[]` | Tool versions, harness and clean-checkout results, failure and restoration runs, and applicable CI. |

- `Unit` has `{id: string, root: ProjectPath, role: string, public-boundary: string, owned-modules: ProjectPath[], targets: string[]}`. Targets are nonempty.
- `Command` has `{id: string, operation: string, unit-id: string, argv: string[], cwd: ProjectPath, target: string, mode: string, check-level?: string, service-ids?: string[], permission-ids?: string[]}`. Require a nonempty argument vector and a level for check entries. Use the approved test strategy's levels, targets and modes.
- `Service` has `{id: string, identity: string, isolation: string, operations: object, fixtures?: ArtifactRef[]}`. The operations object maps applicable `start`, `readiness`, `seed`, `reset`, `cleanup` and `migration` keys to command IDs.
- `Permission` has `{id: string, environment: string, operation-ids: string[], boundary: object, disposition: string, enforcement: string, evidence-ref?: EvidenceRef}`. The boundary holds applicable `roots: ProjectPath[]`, `networks: string[]`, `services: string[]` and `resources: string[]`. Disposition is `allowed`, `approval-required` or `prohibited`. Enforcement is `verified` or `instruction-only`. Require evidence for verified enforcement.

Require unique IDs within each list and resolve their references. Task checks use the approved command's unit, target and mode. README commands use its exact arguments and working directory.

## Work-Item Fields

### Shared Fields

| Field                            | Type                                                                | When Required                                                                                                                                                                                                                                  |
| -------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`, `title`, `outcome`         | `string` each                                                       | Initial planning. IDs follow `FEAT-NNN`, `FEAT-NNN-TNN` and `FEAT-NNN-TNN.N`. Allocate positive numbers above existing assignments in the same scope, including cancelled work. Use at least three feature digits and two ticket digits.       |
| `depends-on`                     | `string[]`                                                          | Initial planning, possibly empty. Feature dependencies target features. Ticket dependencies stay within the feature, and task dependencies within the ticket. Reject duplicates, missing targets, self-dependencies and cycles.                |
| `status`                         | `READY`, `BLOCKED`, `IN-PROGRESS`, `IN-REVIEW`, `DONE`, `CANCELLED` | First publication uses `READY` or `BLOCKED` according to readiness. Store feature and local status in Git. Derive remote status from native state and label.                                                                                   |
| `approval-ref`                   | `EvidenceRef`                                                       | Git only. Use when the approval is stored separately and cannot be resolved from the owning checkpoint and commit. Always resolve the approved definition before relying on a published record. Remote definitions resolve it via checkpoints. |
| `checkpoints`, `checkpoint-refs` | `Checkpoint[]`, `EvidenceRef[]`                                     | Store or reference evidence as produced. Remote items use comments or the linked PR. Preserve historical evidence.                                                                                                                             |
| `origin-ref`                     | `ArtifactRef` or `EvidenceRef`                                      | For applicable additive work, link the source finding, amendment or preceding item. Provenance does not create a dependency.                                                                                                                   |

### Feature

| Field                      | Type                                                       | When Required                                                                                                                   |
| -------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `priority`                 | `string`                                                   | Initial planning.                                                                                                               |
| `requirements`, `journeys` | `ArtifactRef[]` each                                       | Initial planning. Pin both sets of references. Require at least one requirement. Journeys may be empty when inapplicable.       |
| `quality-allocations`      | `{requirement-ref: ArtifactRef, responsibility: string}[]` | If a quality requirement is provisionally assigned in the catalog. Pin the reference.                                           |
| `references`               | `ArtifactRef[]`                                            | As specification outputs are approved. Pin the spec and applicable API, data impact and UI artifacts to the approved revisions. |
| `delivery-strategy`        | `DeliveryStrategy`                                         | Strategy approval.                                                                                                              |
| `tickets`                  | `TicketMapping[]`                                          | Delivery-plan publication. Require a nonempty set of mapped tickets.                                                            |

Record feature acceptance and finalization in checkpoints. When the finalization PR exists, record its reference in `publication.pr`.

`DeliveryStrategy` has `approach` and `summary: string` for ownership, delivery slices and independent checks. Use `single-scope` for work within one owned scope, `vertical-slices` for independently verifiable outcomes across layers, or `contract-first` for separate delivery tracks that use an approved shared contract. Add `integration-coverage: ArtifactRef[]` with pinned acceptance references when real-boundary checks apply. Add `exposure-boundary: string` when an exposure constraint applies. Reuse the shared contract pin in `references`. Record actual check IDs and results in delivery evidence.

### Ticket

| Field                                | Type                                                             | When Required                                                                                                                                                                        |
| ------------------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `feature-id`, `feature-ref`          | `string`, `ArtifactRef`                                          | Ticket planning. Pin the parent reference.                                                                                                                                           |
| `type`, `scope`, `priority`, `owner` | `string` each                                                    | Ticket planning. Store scope and priority in lowercase for label matching.                                                                                                           |
| `references`                         | `ArtifactRef[]` with applicable `acceptance-ids: AcceptanceID[]` | Ticket planning. Pin the relevant feature sections in a single list and select at least one feature acceptance ID. Use IDs that are unique within the referenced feature's criteria. |

Resolve the approved task set before build. Local tickets use `tasks: Task[]` once the task plan is approved. Each entry uses the task fields below, including its own status and checkpoints. The containing ticket supplies parent identity and the top-level file supplies the schema version. Remote mode uses the approved parent-ticket checkpoint and native child mappings. Record the implementation PR in `publication.pr` when created. Add review and closure evidence at their owning steps.

### Task

| Field          | Type                                                              | When Required                                                                                                                                                        |
| -------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ticket-id`    | `string`                                                          | Remote task planning. Derive it from the containing ticket in local mode.                                                                                            |
| `acceptance`   | `{id: AcceptanceID, criterion: string, covers: AcceptanceID[]}[]` | Task planning. Require at least one observable criterion and a distinct ID per criterion. Each `covers` list is nonempty and uses IDs selected by the parent ticket. |
| `verification` | `TaskVerification`                                                | Task planning.                                                                                                                                                       |
| `references`   | `ArtifactRef[]`                                                   | If the task needs a more precise reference than the ticket provides. Pin those targets.                                                                              |

The task's `verification` object is its approved plan. It uses the following fields.

| Field                                                         | Type                                 | When Required                                                                                                                                                |
| ------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `method`                                                      | `test-first`, `test-after`, `manual` | Every task.                                                                                                                                                  |
| `checks`                                                      | `CheckID[]`                          | Every task. Use distinct approved IDs. Require at least one for automated methods. Use an empty array for a manual task only when no automated checks apply. |
| `exception-reason`                                            | `string`                             | `test-after` or `manual`. Approve the reason during planning.                                                                                                |
| `manual-procedure`, `expected-result`, `responsible-verifier` | `string` each                        | `manual` only.                                                                                                                                               |

Read levels from the check definitions. Run applicable automated checks even for manual tasks. Store actual results, tested revisions and human confirmations in checkpoints.

### Mappings and Changes

| Type            | Shape                                                                                                                                                                                          |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TicketMapping` | Local uses `{id: string, path: ProjectPath}`. Remote uses `{id: string, native-ref: NativeRef}`.                                                                                               |
| `NativeRef`     | GitHub uses `{number: integer, url: string}`. Jira uses `{key: string, native-id: string, url: string}`. Use positive numbers and HTTPS URLs in the configured repository or site and project. |
| `PRRef`         | `{number: integer, url: string}` with a positive number and HTTPS URL in the configured repository.                                                                                            |

Use project-approved priority, work type and scope. Choose the Git component through project naming conventions. Freeze each definition when its owning step approves it, including the identity, title, outcome, parentage, scope, owner, dependencies, references, acceptance and verification. Track reassignments separately. Append later outputs and evidence. Compare definitions against their approved snapshot. Use amendments or additive work for material changes.

## Remote Projection and Recovery

| Data                    | GitHub                                                                                                                                                | Jira                                                                                    |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Native title            | Issue title `<agenix-id>: <title>`.                                                                                                                   | Same format in the summary.                                                             |
| Definition              | Markdown issue body with fixed sections and readable text.                                                                                            | ADF description with matching section labels and supported paragraphs, lists and links. |
| Lifecycle               | One `status:<lowercase-status>` label. Verify open state for nonterminal items, completed closure for `DONE` and not-planned closure for `CANCELLED`. | Same label rule. Verify the configured status ID for the item type and lifecycle state. |
| Parent and dependencies | Native sub-issue parent for tasks. Verify mirrored dependencies where supported.                                                                      | Native sub-task parent and configured directed dependency link.                         |
| Checkpoints             | Readable comments on the owning issue or appropriate PR.                                                                                              | Readable comments on the owning item, with PR references where applicable.              |

### Body and Comment Structure

Use the native title for the item's ID and title. Both ticket and task bodies have these sections:

- `Outcome` contains the approved outcome in prose.
- `Details` contains labeled fields. A ticket records the feature ID and feature reference, type, scope, priority and owner. A task records the parent ticket ID. Check that fields mirrored by native labels or parentage agree with native metadata.
- `Dependencies` lists the authoritative Agenix IDs. Render a known empty list as `None`.
- `References` lists applicable pinned targets and their acceptance IDs where required. For tasks, omit this section when the parent supplies all relevant references.
- Task bodies also have `Acceptance` and `Verification` sections. Each criterion includes its ID and `covers` IDs. Render the approved verification plan with the fields required for its method.

For checkpoints, use a `Checkpoint` section with the checkpoint ID, step, time, outcome and applicable item. Use labeled sections for candidate, decision, verification, publication and disposition as applicable. For task-plan approval, include a `Task Plan` section that identifies each approved task and preserves its exact definition in the same readable structure. Post it before child creation. Record verified child mappings after read-back. Keep approval, PR mappings and execution evidence in checkpoints.

The templates define the fixed labels within these sections. Preserve their spelling and field meanings across tracker modes. Write narrative content in the approved documentation language. On Jira, render section labels as standalone ADF paragraphs and the body fields as paragraphs, lists or links. Normalize the defined labels and fields for deterministic comparison. Missing or ambiguous required data blocks dependent work.

Before retrying a write, reconcile exact IDs, repository or project, native parentage and the approved snapshot. A remote ticket must match the Git-owned feature plan. A remote task must match both its native parent and the approved task-plan snapshot. The workflow reads GitHub through `gh` and Jira through `jira.py`. `verify-status.py` remains the local tracker verifier.

## Checkpoints and Receipts

A `Checkpoint` has `checkpoint-id: string`, `phase: string`, `step: string`, `recorded-at: UtcTime`, `outcome: string` and `references: EvidenceRef[]`. Include `item-id: string` for item steps and `next-action: string` when work remains. Include the typed entries that apply.

- `candidate: object` uses `base-commit: GitOID` (the intended parent) and `tree: GitOID` for Git review. Add `target-base-commit: GitOID` when review depends on the target base. Remote definition publication requires `approved-definitions: object[]` (exact immutable definitions) and `baseline-commit: GitOID`. A mixed batch can use both forms.
- `decision: object` has `kind: string`, `result: string`, `actor: string`, `at: UtcTime` and `confirmation: string`. Kinds include `artifact`, `review`, `feature-acceptance`, `merge`, `exposure`, `manual-confirmation`, `cancellation` and `override`. Use `approved`, `changes-requested`, `passed` or `failed` as applicable. Use `human-in-session` or a verified native identity. Record approved writes as `authorized-actions: {action: string, target: string}[]`. Bind merge to `pr: PRRef` and `head-commit: GitOID`. Bind exposure to `operation-id: string`, `target: string` and either `revision: GitOID` or `artifact-ref: EvidenceRef`. For manual confirmation, record related `acceptance-ids: AcceptanceID[]` or `check-ids: CheckID[]`. Keep findings and accepted risks in the evidence.
- `verification: VerificationReceipt[]` stores check results. Each entry follows the receipt fields below.
- `publication: object` records `head-commit: GitOID` for Git publication, `pr: PRRef` where applicable and `native-mappings: {id: string, native-ref: NativeRef}[]` for remote writes. Use the owning checkpoint's `pr` as the PR mapping for the feature or ticket. Record `merge-commit: GitOID` only after confirming merge. Preserve both original and repair evidence for post-merge repairs.
- `disposition: object` records `item-id: string` and `reason: string` for cancellation or override. For cancellation, include `replacement-refs: ArtifactRef[]` where applicable. For override, record `action` (`allow-work` or `accept-incomplete`), `revision: GitOID`, `waived-conditions: string[]`, `permitted-work: string` and `consumer-scope: string`. Retain the actual human confirmation and check outcomes.

Bind approvals to the candidate and authorized actions. Check the resulting commit tree and parent after accounting for explicitly approved mechanical updates. Reuse results only for the same candidate and context. Revalidate after material drift, verify native PR/check facts at their source, and keep failed checks recorded as failed even when an override applies.

### Verification Receipt Fields

| Field                       | Type                                                    | When Required                                                                     |
| --------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `check-id`                  | `CheckID`                                               | Every receipt.                                                                    |
| `item-id`, `acceptance-ids` | `string`, `AcceptanceID[]`                              | Work-item checks. Resolve the acceptance IDs in that item.                        |
| `result`                    | `passed`, `failed`, `pending`, `skipped`, `unavailable` | Every receipt.                                                                    |
| `at`, `environment`         | `UtcTime`, `string`                                     | Every receipt.                                                                    |
| `revision` or `tree`        | `GitOID`                                                | Use the checked commit or, for an uncommitted candidate, its tree.                |
| `check-level`, `mode`       | `string` each                                           | When applicable to the check.                                                     |
| `evidence-ref`              | `EvidenceRef`                                           | Required for a completed check. Point to the actual evidence, such as the CI run. |
| `detail`                    | `string`                                                | Required for a pending, skipped or unavailable check.                             |

Read the verification method from the approved task definition.

## Template Bindings

| Template Output                       | Binding                                                                                                                                  |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Project configuration and environment | Use JSON templates for the two root records. Root instructions link to the files.                                                        |
| Feature catalog and feature           | Use JSON templates for the catalog and each feature record in every tracker mode.                                                        |
| Local ticket                          | Use a JSON template with the task structure in its `tasks` array.                                                                        |
| Remote ticket and task                | Use readable sections. Render Markdown on GitHub and corresponding ADF on Jira. The tracker supplies native title, hierarchy and status. |
| Checkpoint                            | Embed JSON in the owning Git record. Render remote and PR checkpoints as readable comments.                                              |

Keep JSON templates syntactically valid and use defaults or sample values of the declared types. Fill and validate only the fields applicable to the selected mode and stage. Keep field requirements in the schema and use them to check rendered records.

## Worked Example

The example covers one address-validation behavior. Assume referenced requirements, specs and checkpoints exist at the indicated revisions.

### Local Mode

The catalog indexes the feature by ID and path.

```json
{
  "schema-version": 1,
  "kind": "catalog",
  "features": [
    {
      "id": "FEAT-003",
      "path": "docs/features/FEAT-003/feature.agenix.json"
    }
  ]
}
```

The feature record contains the following object once its delivery plan is published.

```json
{
  "schema-version": 1,
  "kind": "feature",
  "id": "FEAT-003",
  "title": "Manage delivery addresses",
  "outcome": "Shoppers can manage their delivery address.",
  "priority": "high",
  "depends-on": [],
  "status": "IN-PROGRESS",
  "requirements": [
    {
      "target": "docs/PRD.md#req-014",
      "revision": "1111111111111111111111111111111111111111"
    }
  ],
  "journeys": [],
  "references": [
    {
      "target": "docs/features/FEAT-003/spec.md",
      "revision": "2222222222222222222222222222222222222222"
    }
  ],
  "delivery-strategy": {
    "approach": "single-scope",
    "summary": "Deliver one server-side behavior. The checkout team verifies it through the public API.",
    "integration-coverage": [
      {
        "target": "docs/features/FEAT-003/spec.md#ac-003",
        "revision": "2222222222222222222222222222222222222222"
      }
    ]
  },
  "tickets": [
    {
      "id": "FEAT-003-T01",
      "path": "docs/features/FEAT-003/tickets/FEAT-003-T01.agenix.json"
    }
  ]
}
```

The local ticket contains one task in its `tasks` array.

```json
{
  "schema-version": 1,
  "kind": "ticket",
  "id": "FEAT-003-T01",
  "title": "Validate a delivery address",
  "outcome": "Reject an address without a postal code.",
  "feature-id": "FEAT-003",
  "feature-ref": {
    "target": "docs/features/FEAT-003/feature.agenix.json",
    "revision": "2222222222222222222222222222222222222222"
  },
  "type": "feat",
  "scope": "backend",
  "priority": "high",
  "owner": "checkout",
  "depends-on": [],
  "references": [
    {
      "target": "docs/features/FEAT-003/spec.md#ac-003",
      "revision": "2222222222222222222222222222222222222222",
      "acceptance-ids": ["AC-003"]
    }
  ],
  "status": "READY",
  "tasks": [
    {
      "id": "FEAT-003-T01.1",
      "title": "Reject a missing postal code",
      "outcome": "Reject the request without persisting the address.",
      "depends-on": [],
      "acceptance": [
        {
          "id": "AC-1",
          "criterion": "A request that omits the postal code returns a validation error and saves no address.",
          "covers": ["AC-003"]
        }
      ],
      "verification": {
        "method": "test-first",
        "checks": ["checkout-address-integration"]
      },
      "status": "READY"
    }
  ]
}
```

This task uses `test-first`, so its verification plan contains only `method` and `checks`. The task inherits the ticket's scoped reference. The check definition supplies the test level. Implementation evidence and PR mapping are recorded later.

### Remote Mode

Keep the feature record in Git and replace a local ticket `path` with a `native-ref`. Use `{"number":42,"url":"https://github.com/example/shop/issues/42"}` for the example GitHub ticket, or `{"key":"SHOP-42","native-id":"10421","url":"https://example.atlassian.net/browse/SHOP-42"}` for Jira.

The native ticket title is `FEAT-003-T01: Validate a delivery address`. Its labels are `status:ready`, `scope:backend` and `priority:high`. A Markdown ticket body can read as follows.

```markdown
## Outcome

Reject an address without a postal code.

## Details

- Feature: FEAT-003
- Feature Reference: `docs/features/FEAT-003/feature.agenix.json` at `2222222222222222222222222222222222222222`
- Type: feat
- Scope: backend
- Priority: high
- Owner: checkout

## Dependencies

None

## References

- `docs/features/FEAT-003/spec.md#ac-003` at `2222222222222222222222222222222222222222` (Acceptance: AC-003)
```

The native task title is `FEAT-003-T01.1: Reject a missing postal code`. Use `status:ready` and attach it to the native ticket. The parent checkpoint preserves the approved task definition in this readable form. The same definition then goes into the child body.

```markdown
## Outcome

Reject the request without persisting the address.

## Details

- Parent Ticket: FEAT-003-T01

## Dependencies

None

## Acceptance

- AC-1 (Covers: AC-003): A request that omits the postal code returns a validation error and saves no address.

## Verification

- Method: test-first
- Checks: checkout-address-integration
```

For Jira, render these sections using the equivalent ADF labels and lists. Both native items use the configured To Do status.

### Verification Receipt

In the local ticket JSON, this example is one entry at `tasks[0].checkpoints[0].verification[0]`. The task's separate `tasks[0].verification` field holds its approved plan. The receipt's `revision` is the checked commit and its evidence points to the CI run. For remote records, render the receipt in the checkpoint comment.

```json
{
  "check-id": "checkout-address-integration",
  "item-id": "FEAT-003-T01.1",
  "acceptance-ids": ["AC-1"],
  "result": "passed",
  "at": "2026-11-19T10:00:00Z",
  "revision": "3333333333333333333333333333333333333333",
  "environment": "ci",
  "check-level": "integration",
  "mode": "live",
  "evidence-ref": {
    "target": "https://github.com/example/shop/actions/runs/12345"
  }
}
```

For evidence stored in Git, `evidence-ref.revision` identifies the commit containing the evidence. It may differ from the checked revision.

### Rejection Examples

| Input                                                                                                                   | Expected Handling                                                                              |
| ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| A duplicate `depends-on` key, an unknown field or a malformed managed record                                            | Reject the record.                                                                             |
| The task ID names `FEAT-003-T01` but its native parent is a different ticket                                            | Reject the mapping and block dependent work.                                                   |
| A task has no acceptance criteria, or an approved `test-after` task has no exception reason                             | Reject the task plan.                                                                          |
| A task claims to cover a feature acceptance ID outside its ticket's scoped references                                   | Reject the task plan.                                                                          |
| A pinned acceptance anchor or required check ID cannot be resolved                                                      | Report the missing prerequisite and block the dependent action.                                |
| The ticket is labelled `status:done` while its native state is open                                                     | Report inconsistent tracker state and block on reconciliation.                                 |
| A local candidate declares `DONE` while required final-head CI is pending or a required result belongs to an older head | Report the declaration and pending or stale evidence separately. Withhold verified completion. |
| A Git record at initial planning has no PR, merge or execution evidence yet                                             | Accept the omission at that stage. Require the evidence when the relevant gate is evaluated.   |
