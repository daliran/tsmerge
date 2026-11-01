# Running: locally and on the cluster

How to run things day to day: on your machine, and on the Unimore cluster.

- One-time preparation (your machine, your cluster account): [setup.md](setup.md).
- Facts and rules of the cluster itself: [cluster.md](cluster.md).
- Every option and file of the cluster scripts: [scripts/cluster/README.md](../../scripts/cluster/README.md).

## The model: local first

**Your machine is the source of truth; the cluster only computes.**

- You edit, commit and keep results locally.
- **Code changes only locally**, never on the cluster, even while debugging there.
- Each cluster run gets a **frozen copy** of the code it was submitted with, so you can keep editing, or submit other versions, while it waits in the queue.
- Results come back to your machine with `pull.sh`. Cluster storage is not backed up, and is deleted when access ends ([cluster.md](cluster.md#storage)).

```
your machine                                  cluster
────────────                                  ───────
working tree ──── submit.sh ────────────────▶ /work/…/runs/<experiment>/<run id>/code/  (frozen copy)
                                              /homes/…/tsmerge/code/   (mirror of the latest submit)
                                              /homes/…/tsmerge/venv/   (environment, from uv.lock)
outputs/runs/<experiment>/<run id>/ ◀── pull.sh ── /work/…/runs/<experiment>/<run id>/
outputs/jobs.log   one line per submitted job: job id, run id, experiment, date, command
```

The run folder layout and the reasons behind it: [PD-003](decisions/PD-003-runs-and-jobs.md).

## Start each session

After WSL or the machine restarts, and every 8 hours for the cluster connection:

```bash
scripts/start-session.sh
```

- It asks for your SSH key passphrases and the cluster password, once, and every terminal and script reuses them.
- Without it, git pushes and the cluster scripts fail with `Permission denied`.
- What it does and why: [scripts/README.md](../../scripts/README.md#start-sessionsh). Setting it up: [setup.md](setup.md#unlock-everything-once-per-session).

## Running locally

Run Python through uv, so it uses the project's environment:

```bash
uv run python scripts/cluster/hello.py
```

- Experiments use the local GPU when PyTorch sees one (`--device auto` once experiments exist), the CPU otherwise.
- **WSL2:** the GPU's memory is shared with Windows apps; check `nvidia-smi` before a long local run ([setup.md](setup.md#5-gpu-and-cuda-optional)).
- There is no local equivalent of `submit.sh` yet (run folder, `run.json`): it will come with the first real experiment.

## Running on the cluster

### Where jobs run

| Work | Partition | Why |
|---|---|---|
| GPU training and evaluation | `all_usr_prod` | [PD-002](decisions/PD-002-cluster-partition.md) |
| CPU-only or very light GPU work (data preparation, aggregating results) | `all_serial`, free, through `srun` or `sbatch` | [PD-002](decisions/PD-002-cluster-partition.md) |
| Never | `boost_usr_prod` | reserved for projects that need high-memory GPUs ([PD-002](decisions/PD-002-cluster-partition.md)) |

- **GPU models:** jobs run only on the models allowed in `scripts/cluster/defaults.sh`; Blackwell is always excluded, because this PyTorch build can't run on it ([PD-004](decisions/PD-004-gpu-allow-list.md)). Whether to also exclude L40S and A40 is open ([PQ-002](questions/PQ-002-exclude-high-end-gpus.md)).
- **Every Slurm option** (account, partition, GPUs, time limit, …) is preset: you pass only the experiment name and the command. Defaults and how to override them: [scripts/cluster/README.md](../../scripts/cluster/README.md#commands).

### The cycle

```bash
scripts/cluster/submit.sh hello python scripts/cluster/hello.py
#   run 20261102-141503-a3f9 (hello), commit a1b2c3d
#   submitted job 123456 -> /work/…/runs/hello/20261102-141503-a3f9

scripts/cluster/status.sh            # your queue
scripts/cluster/status.sh 123456     # one job: state, exit code, elapsed time, node

scripts/cluster/pull.sh hello        # bring the experiment's runs back into outputs/runs/
```

- `submit.sh` returns at once: the job runs on its own, even if you close your machine.
- Before submitting, it checks the GPU lists against the cluster, and warns if a GPU model appeared or disappeared ([PD-004](decisions/PD-004-gpu-allow-list.md)).
- Each run's `run.json` records what ran, where and how it ended; `slurm.out` holds the job's output.
- After a change to `uv.lock` or to your uv version, rerun `scripts/cluster/setup_remote.sh` first: jobs refuse to run against an outdated environment.

## Interactive work and debugging on the cluster

Most debugging happens locally. When it must happen on the cluster:

- **An interactive shell through Slurm**, never directly on a login node:

  ```bash
  # a GPU, on the debug QOS (high priority, at most 1 h)
  srun --partition=all_usr_prod --qos=all_qos_dbg --account=<project account> \
       --constraint="<allowed GPU models>" --gres=gpu:1 --time=00:30:00 --pty bash

  # CPU-only or light work, free of charge
  srun --partition=all_serial --account=<project account> --time=01:00:00 --pty bash
  ```

  Then activate the environment: `source /homes/<user>/tsmerge/venv/bin/activate`.
- **VS Code:** connect with *Remote-SSH* to a login node, open the code mirror (`/homes/<user>/tsmerge/code/`), and run the debugger inside an `srun` session ([cluster documentation](https://ailb-web.ing.unimore.it/coldfront/documentation/Zf44P)).
- **Fix the code locally**, then resubmit: the mirror is overwritten at every submit.

## Safety net

- **Pull regularly:** at least at the end of each working day, `scripts/cluster/pull.sh`. Checkpoints only when needed: `pull.sh --checkpoints <experiment>`.
- **Mind the account's expiry:** check with `sexpiration` on the cluster; when it ends, the work folder is deleted at once ([cluster.md](cluster.md#storage)).
