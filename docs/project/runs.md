# Runs

What a run is, where it lives and what it records. How to launch and follow runs is in [running.md](running.md). The reasons behind each choice are in the linked decisions.

## Concepts

- **Experiment:** a named study (lowercase letters, digits, `-`, `_`). It groups runs. How experiments get ids is still open ([PQ-003](questions/PQ-003-experiment-ids.md)).
- **Run:** one execution of one configuration, one seed included.
- **Job:** one Slurm submission. One job runs exactly one run.
- **Sweep:** a set of runs, each still one job, grouped by a sweep id given at submit time (`SWEEP=<id>`).

Why one run per job: [PD-003](decisions/PD-003-runs-and-jobs.md).

## Run id

`<YYYYMMDD-HHMMSS>-<4 hex>`, e.g. `20261102-141503-a3f9`.

- Generated on your machine at submit time, never from the Slurm job id.
- The same id names the run folder and its line in `outputs/jobs.log`.
- A run folder is never reused: a submission fails if the folder already exists ([PD-010](decisions/PD-010-safe-submissions.md)).

## Run folder

The same layout locally and on the cluster:

```
<runs root>/<experiment>/<run id>/
├─ run.json      how the run was launched and how it went
├─ config.json   what the run computed with
├─ code/         frozen copy of the code this run used (cluster runs only; not pulled)
├─ provenance/   uncommitted changes at submit time: patch.diff, git-status.txt (pulled)
├─ slurm.out     the job's output (cluster runs only)
├─ results/      small result files (json, csv)
├─ checkpoints/  model weights (pulled only on request)
└─ wandb/        reserved for wandb's local files, if wandb is added
```

| Where | Path |
|---|---|
| Local runs root | `outputs/runs/` (git-ignored) |
| Cluster runs root | `/work/<project account>/<username>/tsmerge/runs/` |
| Cluster code mirror (the latest submitted code, for remote debugging) | `/homes/<username>/tsmerge/code/` |
| Cluster environment | `/homes/<username>/tsmerge/venv/` |
| Cluster per-job temporary files | `/work/<project account>/<username>/tsmerge/tmp/<job id>/`, deleted at job end |

`pull.sh` copies cluster runs into `outputs/runs/` with the same paths, without `code/`, and without `checkpoints/` unless asked.

## What a job provides

Every cluster job gets these environment variables. Locally, programs use the same names, with the defaults shown.

| Variable | What it is | On the cluster | Locally (default) |
|---|---|---|---|
| `RUN_DIR` | this run's folder: write `results/` and `checkpoints/` here | the run folder | — |
| `DATA_DIR` | the datasets folder ([PD-020](decisions/PD-020-dataset-location.md)) | `/work/<project account>/<username>/tsmerge/data/` | `data/` in the repository, or `DATA_DIR` in `.env` |
| `RUNS_ROOT` | the root of all runs, to read the outputs of the runs listed in `inputs` ([PD-021](decisions/PD-021-runs-and-their-inputs.md)) | `/work/<project account>/<username>/tsmerge/runs/` | `outputs/runs/` |
| `TMPDIR` | a temporary folder, deleted at the end of the job | `/work/…/tsmerge/tmp/<job id>/` | the system's |
| `SLURM_CPUS_PER_TASK` | the CPU cores the job has, e.g. for data-loader workers | 6 by default | — |

## `run.json`: how the run was launched and how it went

Written by `submit.sh`, completed by the job ([PD-009](decisions/PD-009-run-records.md)):

| Group | Fields |
|---|---|
| Identity | `run_id`, `experiment`, `sweep`, `inputs` (the earlier runs it reads), `command` |
| Code and environment | `git_commit`, `git_dirty`, `uv_lock_sha256`, `uv_version` |
| Slurm options actually used (`slurm`) | `profile` (`gpu` or `cpu`), `account`, `partition`, `constraint`, `nodes`, `ntasks`, `cpus_per_task`, `gpus`, `time`, `signal`, `requeue`, `extra_options` |
| Where it ran | `host`, `slurm_job_id`, `gpus`, `gpu_capability`, `driver`, `python`, `torch`, `torch_cuda`, `cudnn` |
| How it went | `submitted_at`, `started_at`, `ended_at`, `exit_code`, `status` |

### How a run ended: `status`

| Status | Meaning |
|---|---|
| `submitted` | queued, not started yet |
| `running` | started, still running (or the node died without warning) |
| `completed` | the command exited with 0 |
| `failed` | the command, or a check before it, exited with another code: see `slurm.out` |
| `timeout` | stopped at the time limit: rerun with a larger `CLUSTER_TIME` |
| `canceled` | stopped before its time limit (`scancel`, or a node problem) |
| `stopped` | stopped by Slurm, but the reason couldn't be determined |

- Slurm warns the job **2 minutes before** its time limit, so the job script can record the ending and stop the command cleanly. A run therefore gets its time limit **minus 2 minutes**.
- Slurm's own record (`sacct`, `status.sh <job id>`) shows such runs as `FAILED` with exit code 15, not `TIMEOUT`: trust `run.json`.
- The program needs nothing special for this.
- **Runs don't resume:** a run that times out is resubmitted from scratch, with a larger `CLUSTER_TIME` ([PD-021](decisions/PD-021-runs-and-their-inputs.md)).

Why it works this way: [PD-006](decisions/PD-006-run-endings.md).

## `config.json`: what the run computed with

Written by the experiment code when the run starts, before any computation, locally and on the cluster alike ([PD-009](decisions/PD-009-run-records.md)):

| Field | Contents |
|---|---|
| `config` | every setting with its final value, **defaults included**, not only what was typed |
| `seeds` | a training seed, and a separate evaluation seed (default: training seed + 1) |
| `data` | for each dataset: name, source or version, a checksum of the files used, the split definition |
| `determinism` | `torch.backends.cudnn.deterministic`, `cudnn.benchmark`, `allow_tf32` (matmul and cuDNN), `torch.use_deterministic_algorithms` |

Results are compared by reading these files, never by parsing commands or folder names. The code that writes `config.json` comes with the first experiment.

## `results/metrics.json`: what the run measured

Every run writes its metric values in one fixed format ([PD-026](decisions/PD-026-results-format.md)): a list of records, one per value.

```json
[
  {"phase": "merged", "split": "test", "metric": "mse", "value": 0.412},
  {"phase": "finetune_0", "split": "val", "metric": "mse", "value": 0.388}
]
```

| Field | Meaning |
|---|---|
| `phase` | which model the value belongs to, when a run produces several (base, fine-tuned, merged); omitted when there is one |
| `split` | `train`, `val` or `test` |
| `metric` | the metric's name |
| `value` | a number |

One aggregation script, written with the first experiment, joins `run.json`, `config.json` and `metrics.json` into one table per sweep or experiment; thesis tables and figures come from those tables.

## Provenance: the exact code of a run

- `git_commit` names the commit; `provenance/patch.diff` holds every uncommitted difference at submit time, **new files included**, binary-safe.
- A run submitted from a clean tree is exactly its commit; `submit.sh` warns when it isn't.
- To rebuild a run's code: [running.md](running.md#rebuilding-a-runs-code).

Why: [PD-007](decisions/PD-007-run-provenance.md).
