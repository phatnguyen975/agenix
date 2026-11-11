# Repository Layout

## Purpose

Choose version-control grouping and locate release units, local libraries, build tooling, tests, and documentation. **Repository**, **build target/package**, **release unit**, and **module** are different boundaries. A build target can be compiled/tested without an independent release, while a release unit can comprise several targets. A monorepo can contain separately released products; a polyrepo can contain several packages per repository. This file does not select deployment topology.

## Decision Inputs

Collect, for the affected units: existing repositories; team ownership; access and compliance separation; shared dependencies; frequency of cross-unit change; ability to coordinate changes; version/release process; build graph/test selection; CI capacity; and current tooling constraints. A single owner or uniform stack does not, by itself, decide the topology.

## Repository Strategy

| Consideration       | One Shared Repository Favors                                              | Separate Repositories Favor                                                            |
| ------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Cross-unit changes  | Coordinated, atomic edits across tightly related units                    | Rare changes; compatibility can be managed through published interfaces                |
| Build and test      | Reliable dependency graph, caching, and affected-target testing available | Tooling cannot scale a combined graph or security isolation demands separate pipelines |
| Access control      | Common read access is acceptable                                          | Different confidentiality, regulatory, or trust requirements                           |
| Developer workflows | Contributors frequently navigate and update several units                 | Teams need independently governed history or contribution workflows                    |
| Dependency upgrades | Shared revisions and one reviewed change are valuable                     | Dependencies are intentionally versioned and updated independently                     |
| Release cadence     | Either: independent releases **are possible** in a monorepo               | Either: releases may still be coordinated across repositories                          |

Decision rules:

1. Select the repository grouping from the strongest constraints; include **hybrid grouping** if warranted (e.g., app and its packages together, regulated subsystem separately).
2. **Do not equate monorepo with lockstep releases** or polyrepo with autonomous deployments. Record build/release independence separately for each release unit.
3. Explicitly state the source of truth for published interfaces, versioning, and multi-repository coordination when units span repositories.
4. For an existing repository, retain the arrangement unless demonstrable coordination, access, or tooling costs justify a move. Repository migration has separate operational risk.

**Example:** A web client, API server, and published UI library may share one repository while releasing independently; an internal UI build target consumed only by the client need not be a separate release unit. A separate restricted-data service may require a second repository because access control differs. This choice does _not_ prescribe how either runtime communicates.

## Release Unit Placement

- A release unit has a discernible **distribution, publication, or deployment boundary**, not merely a buildable directory. A separately buildable internal package may remain part of a parent release unit.
- Put each release unit at an unambiguous path. Within a single-unit repository, the repository root may be its root.
- Shared **in-repository packages** have explicit consumers, an owner, and a declared build/import boundary; when independently published, catalog them as release units, not anonymous shared directories.
- Build metadata lives where the selected build system expects it; generated output and caches are not hand-maintained source modules.
- Keep generated files separate or explicitly marked, and record whether they are committed only if it affects ownership or dependency boundaries.
- For multi-language repositories, organize by independently owned units rather than adding language directories automatically; language grouping is justified when tooling or ownership requires it.

## Directory Roles

Use only roles actually present:

| Role                     | Content And Constraint                                                               |
| ------------------------ | ------------------------------------------------------------------------------------ |
| Release-unit root        | Entry points and module directories owned by one release unit                        |
| Internal package/library | Reusable code within the repository with declared public access and dependency rules |
| Published library        | Independently versioned release unit when that lifecycle exists                      |
| Build tooling            | Repository-wide scripts, generators, and build metadata; does not own product logic  |
| Integration/system tests | Tests that span multiple units and are owned at that scope                           |
| Documentation            | Project-facing design and contributor documentation                                  |
| Configuration            | Repository-wide control files or settings, not secrets                               |

Do not reject established names such as `src`, `packages`, or framework-required directories solely because they are technical. Avoid an unowned `misc`/`common` directory whose permitted contents cannot be stated.

## Ownership and Access

- Name an accountable owner (person, role, or team) for each release unit and separately governed shared package. An individual-maintained project can use `Project maintainer`.
- Document review responsibility and enforcement **separately**: ownership metadata routes reviewers; it does not restrict imports or automatically require approval.
- When platform support exists, map ownership to paths; require owner approval only if repository protection/rules explicitly enable it.
- If confidentiality differs, do not assume a directory inside a shared repository provides the same read-access barrier as a separate repository.
- When a unit spans repositories or packages, make the contract's owner and compatibility policy explicit (`dependency-rules.md`).

## Layout Hierarchy

Use the minimum tree depth needed to explain the decision:

1. **Root Layout:** one tree per repository; significant roots and build/release boundaries.
2. **Unit Layout:** one per release unit; entry points and module boundaries (including actual public-export locations where relevant).
3. **Pattern Layout:** module internals _only_ when a meaningful pattern is selected. If two modules use different variants, show variant-specific layouts rather than an inaccurate universal tree.

Annotate significant entries with responsibility, ownership, or public/internal status. Ignore boilerplate files that do not help interpret the structure. Split large trees into focused subtrees.

**Illustrative, not a mandatory naming convention:**

```text
workspace/
├── client/              # distributable client release unit
│   └── orders/          # order-facing feature module
├── server/              # independently deployable server release unit
│   └── orders/          # server-owned order module; not the same module as client/orders
├── contracts/           # published API definitions, if cross-unit sharing is required
├── tooling/             # repository-wide development/build support
└── docs/                # design documentation
```

Do not infer that `client/orders` may directly import `server/orders`: runtime communication and static imports are different relations. A `contracts` directory is optional; provider-owned contracts or package exports may be more appropriate.

## Failure Modes

- Treating repository layout as proof of module boundaries without build/import rules.
- Selecting polyrepo solely because units deploy independently.
- Selecting monorepo without accounting for access restrictions or scalable builds.
- Moving existing repositories merely to match a reference tree.
- Duplicating global configuration into every release unit without a build requirement.
- Exposing private code just because a sibling release unit shares the same checkout.
