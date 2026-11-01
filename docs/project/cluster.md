# The Unimore cluster

Reference facts about the **AImageLab-HPC Slurm cluster of the University of Modena and Reggio Emilia (Unimore)**: access, partitions, GPUs, accounts, storage and rules. They hold whatever scripts or workflow we use.

- How this project runs things on it: [running.md](running.md).
- Preparing your machine and your cluster account: [setup.md](setup.md).

**Official documentation:** <https://ailb-web.ing.unimore.it/coldfront/documentation/jG2I5>

- This summary was taken from it on 2026-11-01; the GPU counts come from `sinfo` on the same day.
- When they disagree, the official documentation wins.

## Access

- **Login nodes:**
  - `ailb-login-02.ing.unimore.it`
  - `ailb-login-03.ing.unimore.it`

  Both share the same home and work folders.
- **Data-transfer node:** `ailb-data.ing.unimore.it`, for large transfers. It accepts only `scp`, `sftp` and `rsync`.
- **Authentication:**
  - From outside the Unimore network, an SSH key is required, and the password is still asked after the key.
  - Password-only login works only from a Unimore network or VPN.
  - Scripts can't type the password: see [running.md](running.md#start-each-session).
- **Login nodes are shared by every user, so they are for light work only:** editing files, submitting and monitoring jobs, commands that end within a few minutes.
  - **Never run long or blocking processes directly on a login node**, Python scripts included, even when they need no GPU. Run them through Slurm instead: `srun` (interactive) or `sbatch` (batch).
  - Long or heavy processes started directly are killed without warning.
  - Using the login nodes' GPUs outside Slurm is forbidden.
- **Usernames expire:**
  - check the date with `sexpiration`;
  - renew in ColdFront ("Renew Account").

## Connecting manually

For checking something by hand: the queue, a log, a folder, your quota. The scripts don't need this.

**Prerequisites** ([setup.md](setup.md#3-ssh-github-and-the-cluster)): your key is registered on the cluster, and the alias `ailb` is in your `~/.ssh/config`.

**Log in:**

```bash
ssh ailb                      # with the session open (scripts/start-session.sh): no password asked
```

Without the alias, or to reach the other login node:

```bash
ssh <username>@ailb-login-02.ing.unimore.it
ssh <username>@ailb-login-03.ing.unimore.it
```

**Run one command without opening a shell:**

```bash
ssh ailb squeue -u '$USER'    # quoted, so $USER is expanded on the cluster
ssh ailb squota
```

**The shared connection** (what `start-session.sh` opens):

```bash
ssh -O check ailb             # "Master running": open
ssh -fN ailb                  # open it (asks the password once)
ssh -O exit ailb              # close it
```

**Copy files by hand:**

```bash
scp ailb:/work/<project account>/<username>/tsmerge/runs/<experiment>/<run id>/run.json .
rsync -az <local folder>/ ailb:/work/<project account>/<username>/<folder>/
```

For large transfers, use the data-transfer node instead: `<username>@ailb-data.ing.unimore.it`.

**Once logged in:** the [common commands](#common-commands). Keep to light, short commands; anything long goes through `srun` or `sbatch` ([Access](#access)). **Never edit the project's code there**: change it locally and resubmit. Leave with `exit`.

## Partitions and GPUs

The GPU partitions:

| Partition | Nodes | GPUs | Max time per job | Cost |
|---|---|---|---|---|
| `all_serial` (the default) | the 2 login nodes, through Slurm | 24: 16 K80, 8 P100 | 4 h | free |
| `all_usr_prod` | every GPU node, older hardware included | 87 (table below) | 24 h | billed |
| `boost_usr_prod` | high-end only | 54: 4 A40, 36 L40S, 14 RTX PRO 6000 | 24 h | billed |

- Student and thesis accounts get their QOS automatically, so no `--qos` is needed. It allows at most 4 GPUs per user.
- The debug QOS `all_qos_dbg` suits quick tests: 1 GPU, 1 h, high priority.

The GPUs in `all_usr_prod` (87 in total, counted on 2026-11-01 with `sinfo`):

| Model | Feature (for `--constraint`) | Architecture | Memory | GPUs | Share |
|---|---|---|---|---|---|
| GTX 1080 | `gpu_1080_8G` | Pascal | 8 GB | 2 | 2% |
| RTX 2080 | `gpu_2080_11G` | Turing | 11 GB | 5 | 6% |
| RTX 2080 Ti | `gpu_2080Ti_11G` | Turing | 11 GB | 6 | 7% |
| Quadro RTX 5000 | `gpu_RTX5000_16G` | Turing | 16 GB | 10 | 11% |
| Quadro RTX 6000 | `gpu_RTX6000_24G` | Turing | 24 GB | 4 | 5% |
| RTX A5000 | `gpu_RTX_A5000_24G` | Ampere | 24 GB | 5 | 6% |
| A40 | `gpu_A40_45G` | Ampere | 45 GB | 4 | 5% |
| L40S | `gpu_L40S_45G` | Ada | 45 GB | 36 | 41% |
| RTX PRO 6000 | `gpu_RTXPro6000B_96G` | Blackwell | 96 GB | 14 | 16% |
| (untagged, node `vegeta`) | none | unknown | unknown | 1 | 1% |

The A40, L40S and RTX PRO 6000 nodes are also in `boost_usr_prod`. The login nodes have `gpu_K80_12G` and `gpu_P100_16G`, in `all_serial` only.

**Choosing GPU models:**

- GPU models are chosen with `--constraint`, joining features with `|`.
- Slurm can't exclude a feature, so a job lists the features it allows.

## Accounts and budget

- **Every job on a GPU partition needs `--account=<project account>`.** List your accounts with `susage`.
- **Billing** is in standard hours:
  - billed hours = max(CPUs × 0.39, memory GB × 0.06, GPUs × 6.0) × elapsed hours;
  - so one GPU-hour costs at least 6.
- **The yearly budget is a hard limit:**
  - submissions are rejected once it's spent;
  - it resets on January 1;
  - check it with `susage`.
- **Default reservation:** each GPU reserves 6 CPU cores and 18 GB of RAM, unless `--cpus-per-task` or `--mem` is set.

## Storage

| Path | Use | Quota | On expiry |
|---|---|---|---|
| `/homes/<username>` | code, configs, Python environments | 100 GB | archived for 6 months, then deleted |
| `/work/<project account>` | datasets, checkpoints, job outputs | per project | **deleted immediately** |
| node-local `/tmp` | per-job scratch | varies | cleared at job end |

- Members of a project use `/work/<project account>/<username>`.
- There are no `$HOME` or `$WORK` variables for these: use absolute paths.
- Check quotas with `squota`. Don't run `du` on `/work`.
- Prefer a few large files (tar, HDF5, …), and at most about 10,000 files per folder.
- **Nothing is backed up.**

## Common commands

Run them on a login node (`ssh ailb`, or one at a time: `ssh ailb <command>`). All are light.

### Your account, budget and storage

These are the cluster's own commands, not standard Slurm.

| Command | Shows |
|---|---|
| `susage` | your Slurm accounts and their budget: total, used, used this year |
| `squota` | your storage use and quotas: `/homes` and each `/work` project (refreshed periodically, not live) |
| `sexpiration` | when your username expires, and the days left |

### Your jobs

| Command | Shows or does |
|---|---|
| `squeue -u $USER` (or `squeue --me`) | your queued and running jobs |
| `squeue --start -u $USER` | estimated start times of your pending jobs |
| `sprio -u $USER` | the priority of your pending jobs, and what it's made of |
| `scontrol show job <jobid>` | everything about one job: resources, node, times, reason it's pending |
| `sacct -j <jobid> -X --format=JobID,JobName%30,State,ExitCode,Elapsed,NodeList` | a job's outcome, also after it ended |
| `scancel <jobid>` | cancels one job |
| `scancel -u $USER -t PD` | cancels all your pending jobs |

### Submitting and interactive sessions

| Command | Does |
|---|---|
| `sbatch <script>` | queues a batch job and returns at once (this project: through `scripts/cluster/submit.sh`) |
| `srun … --pty bash` | an interactive shell on a compute node; ends when you exit |
| `salloc …`, then `srun --pty bash` | reserves resources first, then opens shells in them; better when you run several commands |

Every job needs at least `--account=<project account>` and `--partition=…`; see [running.md](running.md#interactive-work-and-debugging-on-the-cluster) for complete examples.

### The cluster's state

| Command | Shows |
|---|---|
| `sinfo` | partitions and node states |
| `sinfo -p all_usr_prod` | the nodes of one partition |
| `sinfo -p all_usr_prod -N -o "%N %G %f"` | per node: its GPUs and their feature (for `--constraint`) |

**Help:**

- HPC Helpdesk: `aimagelab-srv-support@unimore.it`
- Service desk: <https://ailb-web.ing.unimore.it/tickets/>
- Web portal for projects and accounts (ColdFront): <https://ailb-web.ing.unimore.it/coldfront/>

## Observed behavior

Seen on this cluster in practice, but not in its documentation:

- `--exclude` is rejected: use `--constraint`.
- An explicit `sbatch --export=VAR=value` gets the job cancelled within seconds, with no log. Pass variables as an environment prefix instead: `VAR=value sbatch …`.
- Node-local `/tmp` can fill up: point `TMPDIR` to a per-job folder under `/work`.
- The folder of a job's log file must exist before submitting.
- **`/homes` seems to limit the number of files, not only their size.** With about 186,000 files in a home using 25 of 100 GB, creating more files failed with `Disk quota exceeded` (2026-11-01). `squota` shows a "chunks" count with no limit, and the documentation states none: the limit and its value are unconfirmed. Keep the home lean:
  - no caches there: uv's (see [PD-005](decisions/PD-005-uv-cache-on-the-cluster.md)), pip's (`pip cache purge`), Hugging Face's (set `HF_HOME` to a `/work` folder);
  - `uv cache prune` removes uv cache entries nothing uses anymore;
  - VS Code's *Remote-SSH* server (`~/.vscode-server`) keeps a copy per VS Code version, tens of thousands of files: old versions can be removed while VS Code isn't connected;
  - count files with `find ~ | wc -l`, or per folder with `find <folder> | wc -l`.
- **The login node's `/tmp` is a local disk** (71 GB free on 2026-11-01), not visible from compute nodes: fine for temporary files of commands run on the login node, never for files a job must read.
