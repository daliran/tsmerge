# ED-0007 — Runs carry their own provenance: commit plus a complete patch

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author

## Problem

Raised by the first expert review (2026-11-01, items H3, M1, L22):

- A run submitted with uncommitted changes recorded them in `patch.diff`, but inside `code/`, which `pull.sh` skips: back on your machine, only `"git_dirty": true` remained. Once the cluster copy is gone (it isn't backed up, and is deleted when access ends), such a run couldn't be rebuilt.
- The patch covered only tracked files: new files were in neither the commit nor the patch. The first `hello` run was an example.
- The dirty flag, the frozen code and the patch were captured at slightly different moments.

## Options

### A — refuse submissions with uncommitted changes

- Every run is exactly a commit: the simplest provenance.
- Every cluster run, debug runs included, needs a commit first.

### B — record the changes completely, and bring them back

- Any run can be rebuilt as commit + patch.
- About 10 lines; a large uncommitted file makes a large patch.

### C — pull the whole frozen code

- Simple, but a few hundred files per run, mostly copies of what git already has.

## Decision

Option B, with a warning:

- `submit.sh` captures, **before sending anything**, the status and a binary-safe patch of every difference from the commit, **new files included** (git's diff against a temporary copy of the index; your staging area is never touched);
- both go to `<run>/provenance/` (`patch.diff`, `git-status.txt`), outside `code/`, so `pull.sh` brings them back;
- a dirty submission prints a warning, but isn't blocked;
- rebuilding a run's code: [running.md](../running.md#rebuilding-a-runs-code).

**Verified:** locally, the commit plus the patch rebuilt every one of 24 changed or new files identically; on the cluster, the patch came back with the pull (2026-11-01).

## Consequences

- Runs you'll report are best submitted from a clean tree: they are then exactly their commit.
- Don't edit files during the few seconds a submission takes.
- The commit itself must still exist: an unpushed, later rebased commit disappears; `submit.sh` warns about unpushed commits ([ED-0025](ED-0025-run-safety.md)).

## Revisit if

- patches grow large in practice (then: consider option A for reported runs);
- runs are found that can't be rebuilt from commit + patch.
