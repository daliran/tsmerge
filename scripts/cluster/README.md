# Cluster scripts

Scripts that run experiments on the Unimore AImageLab-HPC Slurm cluster, from your machine. Local recorded runs use `scripts/run_local.sh` instead. The cluster's facts and rules are in [cluster.md](../../docs/engineering/cluster.md); how we work with it, in [running.md](../../docs/engineering/running.md). What a run is and records: [runs.md](../../docs/engineering/runs.md).

**Before using them:**

- `.env` is filled in (template: `.env.example`);
- the session is unlocked: `scripts/start-session.sh`.

## Commands

| Command | What it does |
|---|---|
| `setup_remote.sh` | Creates the cluster folders and builds the Python environment from `uv.lock`. Run once, and again whenever `uv.lock` or your uv version changes |
| `submit.sh <experiment> <command> [args…]` | Submits one run: freezes the code, records the run, submits the job |
| `status.sh [<job id>]` | Shows your queued jobs, or the state of one job |
| `pull.sh [--checkpoints] [<experiment>[/<run id>]]` | Copies runs back into `outputs/runs/` |
| `logs.sh <job id> [lines]` | Shows the end of a job's output, to follow it while it runs |

Example:

```bash
scripts/cluster/submit.sh hello python -m tsmerge.hello
scripts/cluster/status.sh <job id>
scripts/cluster/pull.sh hello
```

**Slurm options:** every option the scripts set comes from `defaults.sh` (project settings) or `.env` (your account). You pass only the experiment name and the command. For one submission:

- override a default with its variable, e.g. `CLUSTER_TIME=04:00:00 scripts/cluster/submit.sh …`;
- group runs into a sweep: `SWEEP=<id> scripts/cluster/submit.sh …` (recorded in `run.json`);
- run on one GPU family only (a subset of the allowed models): `CLUSTER_GPU_SUBSET="gpu_2080_11G gpu_2080Ti_11G" scripts/cluster/submit.sh …` (ED-0027);
- submit a CPU-only job, on `all_serial` by default: `CLUSTER_PROFILE=cpu scripts/cluster/submit.sh …` (ED-0022);
- name the earlier runs this run reads: `INPUTS="<experiment>/<run id> …" scripts/cluster/submit.sh …` (recorded in `run.json`);
- add any other option with `SBATCH_OPTS`, e.g. `SBATCH_OPTS="--mem=32G" scripts/cluster/submit.sh …`.

| Option | Default | Set in |
|---|---|---|
| `--account` | your project account | `.env` |
| `--partition` | `all_usr_prod` | `defaults.sh` |
| `--constraint` | the allowed GPU models | `defaults.sh` |
| `--nodes`, `--ntasks` | 1, 1 | `defaults.sh` |
| `--cpus-per-task` | 6 (what each GPU reserves anyway) | `defaults.sh` |
| `--gres=gpu:N` | 1 GPU | `defaults.sh` |
| `--time` | 1 hour | `defaults.sh` |
| `--signal` | warn the job script 2 minutes before the time limit | `defaults.sh` |
| memory | not set: the cluster's default (3 GB per CPU, 18 GB) | — |
| `--job-name` | the experiment name | `submit.sh` |
| `--output` | `<run folder>/output.log`, the same name as for local runs | `submit.sh` |

## Files, and why each exists

| File | What | Why |
|---|---|---|
| `defaults.sh` | Project-wide settings: every Slurm option the scripts set (partition, GPU models, nodes, GPUs, time limit) | They are decisions (ED-0002, ED-0004), so they are committed, unlike the personal values in `.env`; one place instead of options scattered across scripts |
| `common.sh` | Shared helpers: loads `.env` and `defaults.sh`, checks the connection, copies code, checks the GPU lists against the cluster | One place for what every script needs |
| `setup_remote.sh` | Folders, the cluster's uv version, the environment (built as a Slurm step on `all_serial`, with a temporary cache on the login node's local disk; the lock hash is removed during the build) | The cluster runs the same Python, PyTorch and uv as your machine (ED-0001); no cache files pile up in the home, which seems to limit the number of files (ED-0005) |
| `submit.sh` | Creates the run id and its folder (never reusing an existing one), freezes the code, records uncommitted changes in `provenance/` (warning when there are any), writes `run.json`, submits; on failure, removes the half-created folder | Every run is traceable to its exact code (ED-0007), and no run can overwrite another (ED-0010) |
| `job.sbatch` | The generic job: temporary folder, environment check, GPU check, runs the command, records the outcome | The same steps for every run; the experiment itself lives in the command |
| `run_info.py` | Adds host, GPU model and capability, driver, Python/PyTorch/CUDA/cuDNN versions, start, end, exit code and status to `run.json` | Every run records where and how it ran, and how it ended; local runs use it too (`scripts/run_local.sh`) |
| `check_gpu.py` | Stops the job if the node's GPU can't run the installed PyTorch | A clear failure in seconds instead of a cryptic CUDA error (ED-0004) |
| `pull.sh`, `status.sh`, `logs.sh` | Bring runs back (skipping each run's own `code/`, and `checkpoints/` unless asked); show jobs | Cluster storage is not backed up and is deleted when access ends |

## What each job does, in order

1. Points `TMPDIR` to a per-job folder under `/work`, deleted at the end. Node-local `/tmp` is shared and can fill up.
2. Sets up how the end gets recorded, whatever stops the job: an exit handler that always writes the end record, and a signal handler for Slurm's warning (time limit) or a cancel.
3. Checks that the cluster environment was built from the same `uv.lock` as the run's frozen code. If not, it stops and asks you to rerun `setup_remote.sh`.
4. Records the start in `run.json`.
5. Checks the GPU (`check_gpu.py`), for GPU jobs.
6. Runs the command from the run's frozen code, with `RUN_DIR`, `DATA_DIR` and `RUNS_ROOT` set ([runs.md](../../docs/engineering/runs.md#what-a-run-provides)) and Python's output unbuffered (so `output.log` is up to date), and waits for it.
7. On any ending, records the status (`completed`, `failed`, `timeout`, `canceled` or `stopped`), the exit code and the end time in `run.json`. The statuses are explained in [runs.md](../../docs/engineering/runs.md#how-a-run-ended-status).

## Rules

- **Code changes only locally**, never on the cluster, even while debugging there. Each submission overwrites the cluster's copy.
- **Nothing heavy on the login nodes:** these scripts run only light commands there (copying files, `sbatch`, `squeue`). The work happens in the jobs.
- Values reach a job as arguments, never with `sbatch --export`, which gets jobs canceled on this cluster.
