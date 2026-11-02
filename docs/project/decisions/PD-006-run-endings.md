# PD-006 — Every run records how it ended

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author

## Problem

Raised by the first expert review (2026-11-01, item H1):

- `run.json`'s end record was written by the job script's last line, after the command.
- When Slurm stops a job (time limit, `scancel`, out of memory), the script dies before that line, so the run stayed `"running"` forever, with no end time or exit code.
- With a 1-hour default time limit, timeouts would be routine: dead runs would be indistinguishable from live ones, and only `sacct`, whose records expire, would know the truth.
- Related (M11): Python buffers output written to a file, so a stopped job also lost its last log lines.

## Options

### A — record the end from handlers inside the job script

- An exit handler that always writes the end record, plus a signal handler for Slurm's warning before the time limit.
- Covers every ending the script can see; no extra cluster calls.

### B — reconcile afterwards with `sacct`

- `pull.sh` or `status.sh` fixes stale `run.json` files from Slurm's records.
- Robust even against a hard kill, but depends on `sacct` records that expire, and touches the cluster at every pull.

## Decision

Option A ([job.sbatch](../../../scripts/cluster/job.sbatch)):

- the command runs in the background while the script waits, so the script can react to signals at once;
- Slurm warns the script 2 minutes before the time limit (`--signal=B:TERM@120`, in [defaults.sh](../../../scripts/cluster/defaults.sh)); the same signal arrives on `scancel`;
- the signal handler asks Slurm for the time left: 3 minutes or less → `timeout`, more → `canceled`, no answer → `stopped`; it stops the command and exits;
- an exit handler writes the end record in every case: status, exit code, end time;
- statuses: `completed`, `failed`, `timeout`, `canceled`, `stopped` (meanings in [runs.md](../runs.md#how-a-run-ended-status));
- jobs run Python unbuffered (`PYTHONUNBUFFERED=1`), so `slurm.out` is complete.

**Verified:** locally, six endings simulated (success, failure, timeout, cancel, unknown, environment mismatch); on the cluster, a 4-minute job was stopped at 2 minutes and recorded `timeout` (2026-11-01).

## Consequences

- A run effectively gets its time limit **minus 2 minutes**: set `CLUSTER_TIME` with a margin.
- `sacct` shows runs stopped this way as `FAILED` (signal 15), not `TIMEOUT`: `run.json` is the reliable record.
- The experiment code needs nothing special. Runs don't resume after a timeout: they are resubmitted from scratch ([PD-021](PD-021-runs-and-their-inputs.md)).
- A node crash (no signal at all) still leaves `running`; option B could be added if that happens.

## Revisit if

- runs regularly need their last 2 minutes (then: let the command run until the hard kill, and record the timeout differently);
- runs are found stuck at `running` after node failures (then: add option B).
