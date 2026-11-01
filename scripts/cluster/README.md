# Cluster scripts

Scripts that run experiments on the Unimore AImageLab-HPC Slurm cluster, from your machine. The cluster's facts and rules are in [cluster.md](../../docs/project/cluster.md); how we work with it, in [running.md](../../docs/project/running.md). The layout of runs is [PD-003](../../docs/project/decisions/PD-003-runs-and-jobs.md).

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

Example:

```bash
scripts/cluster/submit.sh hello python scripts/cluster/hello.py
scripts/cluster/status.sh <job id>
scripts/cluster/pull.sh hello
```

**Slurm options:** every option the scripts set comes from `defaults.sh` (project settings) or `.env` (your account). You pass only the experiment name and the command. For one submission:

- override a default with its variable, e.g. `CLUSTER_TIME=04:00:00 scripts/cluster/submit.sh …`;
- add any other option with `SBATCH_OPTS`, e.g. `SBATCH_OPTS="--mem=32G" scripts/cluster/submit.sh …`.

| Option | Default | Set in |
|---|---|---|
| `--account` | your project account | `.env` |
| `--partition` | `all_usr_prod` | `defaults.sh` |
| `--constraint` | the allowed GPU models | `defaults.sh` |
| `--nodes`, `--ntasks` | 1, 1 | `defaults.sh` |
| `--gres=gpu:N` | 1 GPU | `defaults.sh` |
| `--time` | 1 hour | `defaults.sh` |
| CPUs, memory | not set: the cluster's default per GPU (6 cores, 18 GB) | — |
| `--job-name` | the experiment name | `submit.sh` |
| `--output` | `<run folder>/slurm.out` | `submit.sh` |

## Files, and why each exists

| File | What | Why |
|---|---|---|
| `defaults.sh` | Project-wide settings: every Slurm option the scripts set (partition, GPU models, nodes, GPUs, time limit) | They are decisions (PD-002, PD-004), so they are committed, unlike the personal values in `.env`; one place instead of options scattered across scripts |
| `common.sh` | Shared helpers: loads `.env` and `defaults.sh`, checks the connection, copies code, checks the GPU lists against the cluster | One place for what every script needs |
| `setup_remote.sh` | Folders, the cluster's uv version, the environment (built with a temporary cache on the login node's local disk) | The cluster runs the same Python, PyTorch and uv as your machine (PD-001); no cache files pile up in the home, which seems to limit the number of files (PD-005) |
| `submit.sh` | Creates the run id, freezes the code into the run folder, writes `run.json`, submits | Every run is traceable to its exact code, and no run can overwrite another (PD-003) |
| `job.sbatch` | The generic job: temporary folder, environment check, GPU check, runs the command, records the outcome | The same steps for every run; the experiment itself lives in the command |
| `run_info.py` | Adds host, GPU, driver, versions, start, end and status to `run.json` | Every run records where and how it ran |
| `check_gpu.py` | Stops the job if the node's GPU can't run the installed PyTorch | A clear failure in seconds instead of a cryptic CUDA error (PD-004) |
| `hello.py` | Prints what PyTorch sees and runs one CUDA operation | The smoke test for a new setup |
| `pull.sh`, `status.sh` | Bring runs back; show jobs | Cluster storage is not backed up and is deleted when access ends |

## What each job does, in order

1. Points `TMPDIR` to a per-job folder under `/work`, deleted at the end. Node-local `/tmp` is shared and can fill up.
2. Checks that the cluster environment was built from the same `uv.lock` as the run's frozen code. If not, it stops and asks you to rerun `setup_remote.sh`.
3. Records the start in `run.json`.
4. Checks the GPU (`check_gpu.py`).
5. Runs the command from the run's frozen code, with `RUN_DIR` set to the run folder.
6. Records the end, status and exit code in `run.json`.

## Rules

- **Code changes only locally**, never on the cluster, even while debugging there. Each submission overwrites the cluster's copy.
- **Nothing heavy on the login nodes:** these scripts run only light commands there (copying files, `sbatch`, `squeue`). The work happens in the jobs.
- Values reach a job as arguments, never with `sbatch --export`, which gets jobs cancelled on this cluster.
