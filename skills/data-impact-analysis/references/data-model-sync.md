# System Data Model Document Synchronization

Use in Phase 4 for DMCs explicitly approved at Gate 1. At Phase 8, the same approval rule applies to new or materially changed DMCs. This procedure edits documentation only; it does not execute schema changes or migrations.

## Before Editing

1. Read all relevant model files, indexes, diagrams, summaries, and references.
2. Locate each target and identify which files own its definition.
3. Check for an equivalent change by semantics, not name alone.
4. Stop if model documentation conflicts with schema or data-access evidence.

## Apply Approved Changes

1. Change only what approved DMCs require.
2. Update affected definitions, relationships, indexes, constraints, diagrams, summaries, and links.
3. For renames/removals, search old-name references; preserve intentional history.
4. Follow project naming, type, key, validation, and diagram conventions.
5. Apply dependencies in order. Never include rejected or unapproved changes.
6. Make the edit idempotent; reruns must not duplicate entries.

## Verify

1. Re-read every edited file from disk.
2. Confirm each approved DMC is represented correctly and consistently.
3. Confirm no rejected/unapproved change was applied.
4. Check names, types, defaults, nullability, keys, relationships, indexes, constraints, and lifecycle values.
5. Record each DMC's exact file and model location.

Stop if the change cannot be represented safely or requires unrelated restructuring. The Effective Data Model is established only after read-back succeeds.

## Reversal and Reporting

Never remove an applied structure solely because a later response rejects it. Check consumers and deployed versions first; obtain a safe deprecation/rollout plan when needed.

Report each DMC ID, changed location, and read-back result. Do not claim partial or unverified changes were applied.
