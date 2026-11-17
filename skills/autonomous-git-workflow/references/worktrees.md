# Worktrees

A linked worktree provides another working directory and index in the same repository. Use it for parallel work, isolated reviews, bisect or an experiment that must not touch an existing checkout. A dirty tree alone does not require creating one if the task can safely proceed in its explicitly handed-over scope.

## Ownership and Shared State

Coordinate one active writer for overlapping files/index operations. Git normally prevents the same branch being checked out in two worktrees; do not force around that safeguard. Worktrees share objects, ordinary branch/tag refs, remotes, repository config and stashes; they do not isolate operations on those shared resources. Each has its own HEAD/index and working files, including untracked/ignored local data. Respect any worktree-specific configuration; Git's [worktree details](https://git-scm.com/docs/git-worktree#_details) explain shared versus per-worktree state.

An existing worktree can be handed over by the human with a defined task and write scope. Record its identity, branch and existing changes. Read-only review can inspect an available checkout without taking write ownership. Editing permission does not imply removal, abandoning its branch or changing unrelated content.

## Create or Resume

1. Inspect `git worktree list --porcelain`, ownership and the intended base. Resume the matching authorized checkout if one exists; avoid duplicate branches/worktrees.
2. If isolation is necessary and authorized, use a known empty/nonexistent target outside the main tree or a project-designated ignored directory (e.g., `../<project>-<branch-slug>`). For a new branch, `git worktree add --no-track -b <name> "<path>" origin/<trunk>`. Verify the branch name with `git check-ref-format --branch` first. For an existing branch, inspect it before `git worktree add "<path>" <branch>`.
3. Verify list output and `git -C "<path>" branch --show-current`, then prepare only the required environment under existing permissions. Local environment files do not transfer automatically; never copy another worker's secrets or install tools merely because a worktree was created.
4. Run the selected workflow using that checkout's explicit path and index. Optional `git worktree lock --reason "<reason>" "<path>"` protects metadata from removal/pruning, not a distributed editing lock; use only when within maintenance authority.

## Cleanup

Follow branch lifecycle deletion checks. Inspect `git -C "<path>" status --short --ignored`, preserve valuable local data and confirm that no active task still uses the checkout. Normal `git worktree remove "<path>"` can remove ignored contents; do not treat a lack of tracked changes as sufficient evidence. Forced removal requires the exact R9 authorization and preview.

Do not remove an existing human/other-worker worktree merely because it was handed over. Obtain explicit removal authority for its exact path. Repository-wide `git worktree prune -n -v` previews stale metadata, not a selected worktree's contents; mutating prune is R10 and must account for every affected entry. Preserve unknown entries. Never substitute filesystem deletion for a failed Git ownership/removal prerequisite.
