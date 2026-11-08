# ED-0003 — Experiments, runs and jobs: one run per job, one folder per run

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author

## Problem

Runs happen locally and on the Unimore cluster ([running.md](../running.md)). Their outputs must be:

- easy to find and compare;
- traceable to the exact code, configuration and environment that produced them;
- safe from being overwritten;
- pulled back locally, because cluster storage is not backed up and is deleted when access ends.

Two known pitfalls to avoid:

- **Run ids taken from the Slurm job id** collide as soon as one job runs several runs, and results get silently overwritten.
- **Configuration encoded in folder names** (method, dataset, seed, …) makes analysis depend on parsing names.

## Options

### A — one run per job, run id generated locally

- Every run is independent: one failure never affects another run.
- The id is unique however runs are launched.
- Many small jobs for a sweep: some scheduling overhead, reducible later with Slurm job arrays.

### B — several runs per job

- Less scheduling overhead for many short runs.
- One failure or time-out can take several runs down; logs and outputs get mixed.

## Decision

Option A.

### Concepts

- **Experiment:** a named study (lowercase letters, digits, `-`, `_`). It groups runs. Experiment names and ids: [ED-0032](ED-0032-experiment-ids.md).
- **Run:** one execution of one configuration, one seed included.
- **Job:** one Slurm submission. One job runs exactly one run.
- **Sweep:** a set of runs, each still one job (or one task of a Slurm job array), grouped by a sweep id ([ED-0009](ED-0009-run-records.md)).

### Run id

`<YYYYMMDD-HHMMSS>-<4 hex>`, e.g. `20261102-141503-a3f9`.

- Generated on your machine when the run is launched, never from the Slurm job id.
- The same id names the run folder, the line in `outputs/jobs.log`, and the wandb run if wandb is added later.
- A run folder is never reused ([ED-0010](ED-0010-safe-submissions.md)).

### Run folder

The same locally and on the cluster:

```
<runs root>/<experiment>/<run id>/
├─ run.json      how the run was launched and how it went (ED-0009, ED-0006)
├─ config.json   what the run computed with (ED-0009)
├─ code/         frozen copy of the code the run executes (kept on the cluster, not pulled;
│                deleted at the end of local runs, ED-0029)
├─ provenance/   uncommitted changes: patch.diff, git-status.txt (ED-0007)
├─ output.log    everything the command printed
├─ results/      small result files (json, csv)
├─ checkpoints/  model weights (pulled only on request)
└─ wandb/        reserved for wandb's local files, if wandb is added
```

### Roots

| Where | Path |
|---|---|
| Local runs root | `outputs/runs/` (git-ignored) |
| Cluster runs root | `/work/<account>/<user>/tsmerge/runs/` |
| Cluster code mirror (latest submitted code, for remote debugging) | `/homes/<user>/tsmerge/code/` |
| Cluster environment | `/homes/<user>/tsmerge/venv/` |
| Cluster per-job temporary files | `/work/<account>/<user>/tsmerge/tmp/<job id>/`, deleted at job end |

- **Pull:** cluster runs are copied into `outputs/runs/` with the same paths, without `code/`; checkpoints only on request.
- **Code changes:** only locally, never on the cluster, wherever a run is executed or debugged.

## Consequences

- How runs end, what they record, how they keep their provenance and how submissions stay safe are separate decisions:
  - [ED-0006](ED-0006-run-endings.md)
  - [ED-0007](ED-0007-run-provenance.md)
  - [ED-0009](ED-0009-run-records.md)
  - [ED-0010](ED-0010-safe-submissions.md)
- wandb is not used for now; curves go in `results/history.jsonl` ([ED-0033](ED-0033-training-curves.md)). If it's added, it plugs in without changing the layout: project `tsmerge`, group = experiment, run id = our run id, files in `wandb/`.
- Personal values (account, user, paths) come from the local `.env` ([ED-0014](ED-0014-personal-values.md)).

## Revisit if

- one run per job proves too costly for short runs (see [ED-0023](ED-0023-durations-and-budget.md)): then allow several runs per job, each keeping its own folder;
- runs need to span several jobs (see [ED-0021](ED-0021-runs-and-their-inputs.md)).
