# System Data Model Document Synchronization

Apply this procedure in Phase 4 only to DMCs the user explicitly confirmed at Gate 1. At Phase 8, the same approval rule applies to any new or materially changed DMC. This procedure edits documentation only; it does not execute schema changes or migrations.

## Before editing

1. Read the whole relevant System Data Model Document set, including indexes, diagrams, references, summaries, and linked model files. Follow its established structure, formatting, terminology, and conventions.
2. Locate each target entity/field/key/relationship/index/constraint and its references. If the model is split across files, map which files own each definition.
3. For each confirmed DMC, check whether an equivalent change is already present. Compare semantics — not only names — and ensure type, optionality, constraints, ordering, and relationship behavior match.
4. If the document conflicts with data-access code or a separate schema source, stop and report the conflict rather than silently choosing the newer-looking artifact.

## Apply only confirmed changes

1. Change only what the confirmed DMCs require. Leave unrelated sections untouched.
2. Update every affected representation: entity/field definitions, keys, relationships, index and constraint lists, schema diagrams, tables of contents, navigation links, and summary tables.
3. For renames/removals, search and update references to the old name. Do not erase history or references without checking if the document intentionally tracks historical changes.
4. Preserve the project's naming, type, description, key, validation, and diagram conventions. If no suitable convention exists, ask before adding a new documentation structure that materially changes organization.
5. Use dependency order from the approved DMCs. Do not apply a rejected DMC or use it as an excuse to make a related unapproved change.
6. Make the edit idempotent: rerunning the sync procedure must not duplicate fields, indexes, relationships, or summary entries.

## Read-back verification

After writing:

1. Re-read every edited file from disk, not just the text held in memory.
2. Verify that every approved DMC is represented exactly once at the proper definition locations and that dependent diagrams/summaries/links are consistent.
3. Verify no rejected or unconfirmed DMC was applied.
4. Verify that names, types, defaults, nullability, keys, relationships, index ordering/options, constraint scope, and lifecycle values agree with the approved definitions.
5. Record the exact file and section/entity location for each applied DMC in the report.

If the change cannot be represented safely, a necessary consumer reference is ambiguous, or editing would require unrelated restructuring, stop and ask. Do not claim the Effective Data Model is established until read-back succeeds.

## Reversal and post-approval changes

Never remove an already synchronized structure only because a later response rejects it. First search the current model and available code/docs for consumers, check whether other features or deployed versions may have adopted it, and determine whether removing it would break data or compatibility. If reversal is not demonstrably safe, ask for an approved deprecation/expand-migrate-contract plan; keep the structure until a safe plan is agreed.

## Report

For each applied DMC, report the DMC ID, the exact file and model location changed, and whether the post-write read-back passed. Do not say a DMC was applied if its representation is only partially updated or the write-back could not be verified.
