# PD-003 — Experiments, runs and jobs: one run per job, one folder per run

- **Status:** proposed
- **Date:** 2026-11-01
- **Decided by:** the author (to be reviewed together with the cluster scripts)

## Context

Runs happen locally and on the Unimore cluster ([running.md](../running.md)). Their outputs must be:

- easy to find and compare;
- traceable to the exact code, configuration and environment that produced them;
- safe from being overwritten;
- pulled back locally, because cluster storage is not backed up and is deleted when access ends.

Two known pitfalls to avoid:

- **Run ids taken from the Slurm job id** collide as soon as one job runs several runs, and results get silently overwritten.
- **Configuration encoded in folder names** (method, dataset, seed, …) makes analysis depend on parsing names.

## Options

### A — one run per job, run id generated locally (recommended)

- Every run is independent: one failure never affects another run.
- The id is unique however runs are launched.
- Many small jobs for a sweep: some scheduling overhead, reducible later with Slurm job arrays.

### B — several runs per job

- Less scheduling overhead for many short runs.
- One failure or time-out can take several runs down; logs and outputs get mixed.

## Decision

Option A.

**Concepts:**

- **Experiment:** a named study (lowercase letters, digits, `-`, `_`). It groups runs.
- **Run:** one execution of one configuration, one seed included.
- **Job:** one Slurm submission. One job runs exactly one run.
- **Sweep:** a set of runs, each still one job (or one task of a Slurm job array). Its id is recorded in each run's `run.json`.

**Run id:** `<YYYYMMDD-HHMMSS>-<4 hex>`, e.g. `20261102-141503-a3f9`.

- Generated locally at submit time, never from the Slurm job id.
- The same id names the run folder, the line in `outputs/jobs.log`, and the wandb run if wandb is added later.
- Configuration lives in files, never in folder names.

**Run folder**, the same locally and on the cluster:

```
<runs root>/<experiment>/<run id>/
├─ run.json      what, where, when: run id, experiment, command, git commit, uncommitted
│                changes (yes/no), uv.lock hash, host, GPU, driver, Python and PyTorch
│                versions, Slurm job id, start and end, status, exit code
├─ code/         frozen copy of the code this run used, with patch.diff (cluster runs only)
├─ slurm.out     the job's log (cluster runs only)
├─ results/      small result files (json, csv)
├─ checkpoints/  model weights
└─ wandb/        reserved for wandb's local files, if wandb is added
```

**Roots:**

| Where | Path |
|---|---|
| Local runs root | `outputs/runs/` (git-ignored) |
| Cluster runs root | `/work/<account>/<user>/tsmerge/runs/` |
| Cluster code mirror (latest submitted code, for remote debugging) | `/homes/<user>/tsmerge/code/` |
| Cluster environment | `/homes/<user>/tsmerge/venv/` |
| Cluster per-job temporary files | `/work/<account>/<user>/tsmerge/tmp/<job id>/`, deleted at job end |

**Pull:** cluster runs are copied into `outputs/runs/` with the same paths, without `code/`. Checkpoints only on request.

**Environment check:** a job refuses to start if the cluster environment was built from a different `uv.lock` than the run's frozen code.

**Code changes:** only locally, never on the cluster, wherever a run is executed or debugged.

## Consequences

- Sweeps are many runs. A `sweep` id in `run.json` groups them; job arrays come later if the overhead matters.
- wandb is not used for now. If it's added, it plugs in without changing the layout: project `tsmerge`, group = experiment, run id = our run id, files in `wandb/`.
- Personal values (account, user, paths) come from the local `.env`, never from committed files.
