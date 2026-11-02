# PD-010 — Submissions fail cleanly and never overwrite a run

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author

## Problem

Raised by the first expert review (2026-11-01):

- **M18:** if `sbatch` rejected a job (bad option, budget spent), the run folder already existed on the cluster, marked "submitted" with no job: later pulls showed a run that never ran.
- **L23:** a second run with the same id (same second, same 4 random characters) would silently reuse the first's folder.
- **L14:** extra sbatch options (`SBATCH_OPTS`) reached the cluster's shell as raw text, where characters like `$` or `;` would be interpreted.
- **L2:** when the GPU-list check couldn't read the cluster's GPUs, the script stopped without a message.
- **L15:** `pull.sh` skipped any folder named `code/` or `checkpoints/` at any depth, e.g. `results/code/`.
- **L12:** `run.json` was rewritten in place, so a job stopped mid-write could leave it half-written.

## Options

For M18, the only real choice:

- **A. Delete the half-created folder** on failure: no trace of a run that never ran.
- **B. Keep it, marked `submit_failed`:** a trace of the attempt, but more clutter to filter.

The other items have one obvious fix each.

## Decision

Option A, and:

- until `sbatch` accepts the job, any failure deletes the run folder (only after checking its path is inside the runs area) and says which step failed;
- the run folder is created with a plain `mkdir`: an existing folder makes the submission fail, never reused;
- `SBATCH_OPTS` is split into options on your machine, and each is passed quoted;
- the GPU-list check says clearly when it can't read the cluster's GPUs, or finds none;
- `pull.sh` skips only each run folder's own `code/` and `checkpoints/`;
- `run.json` is written to a temporary file, then renamed (atomic).

**Verified:** on the cluster, a submission with an invalid option was rejected, the step was named, and the folder removed (2026-11-02); locally, the pull excludes, the option quoting and the atomic write.

## Consequences

- A failed submission leaves only an empty experiment folder, if it was the first run of that experiment.
- New tool to follow a job: `scripts/cluster/logs.sh <job id>` ([scripts/cluster/README.md](../../../scripts/cluster/README.md)).

## Revisit if

- failed submissions need investigating after the fact (then: option B).
