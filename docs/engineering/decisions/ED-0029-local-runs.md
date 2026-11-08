# ED-0029 — Local runs are recorded like cluster runs, from a frozen copy of the code

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author

## Problem

- Cluster runs got a run folder, `run.json`, provenance and an end status; local runs got nothing (`uv run python …`).
- A local result therefore couldn't be traced or compared, and a script written for the cluster (which writes to `RUN_DIR`) didn't know where to write locally.
- During a long local run you keep editing: code the run imports later would pick up the edits, and the run would no longer match its recorded state.

## Options

### Recording

- **A. A local runner, `scripts/run_local.sh`,** that creates the same run folder and records as `submit.sh`, in `outputs/runs/`; plain `uv run` stays for quick tries.
- **B. No local records:** simpler, but local results leave no trace.

### Where a local run executes from (code size today: 90 files, 704 KB, copied in 0.05 s)

| | During the run | After the run |
|---|---|---|
| **1. The working tree** | edits during the run can leak into it | nothing to clean |
| **2. A frozen copy in `code/`, kept** | safe to keep editing | about 0.7 MB per run kept |
| **3. A frozen copy in `code/`, deleted at the end** | safe to keep editing | commit + `patch.diff` rebuild it, as for pulled cluster runs |

## Decision

- **Recording: A.** `run_local.sh <experiment> <command>` creates `outputs/runs/<experiment>/<run id>/` with:
  - `run.json` (`launcher: local`, no Slurm section),
  - provenance,
  - `output.log`,
  - and the same environment variables as a cluster job (`RUN_DIR`, `DATA_DIR`, `RUNS_ROOT`).

  It records `completed`, `failed`, or `canceled` (Ctrl-C).
- **Execution: option 3,** a frozen copy deleted at the end: local and pulled run folders look the same.
- **The environment is checked first** (`uv sync --locked`), as cluster jobs check theirs ([ED-0008](ED-0008-environment-integrity.md)).
- **A script started directly** (quick tries, the debugger) is not a recorded run: its outputs go to `outputs/scratch/`, overwritten each time ([ED-0030](ED-0030-experiment-code.md)).
- **The log has one name everywhere:** `output.log`, for local and cluster runs.

**Verified** (2026-11-02): a completed, a failed (exit code 3) and a Ctrl-C run recorded `completed`, `failed` and `canceled`, with the code copy removed; covered by `tests/test_run_local.py`.

The same day, a cluster run (job 178372) wrote `output.log` and `launcher: cluster`, so pulled and local runs have the same files.

## Consequences

- Breakpoints don't stop inside a recorded run (it runs from the copy): debug from the working tree instead ([ED-0031](ED-0031-vs-code.md)).
- `run_local.sh` reuses the cluster scripts' helpers (`common.sh`) and `run_info.py`, so both launchers record the same fields.
- Documented in [running.md](../running.md#running-locally) and [runs.md](../runs.md).

## Revisit if

- the code grows large enough that copying it per run takes noticeable time;
- breakpoints inside recorded runs become necessary (then: a debug mode attaching to the copy, with path mappings).
