# ED-0013 — Default job resources, all set in one committed file

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author

## Problem

- Every cluster job needs Slurm options (partition, GPUs, time limit, …). Hardcoded in the job script and scattered across scripts, they are hard to find, review and change.
- Without a requested CPU count, programs can't read it from `SLURM_CPUS_PER_TASK` (e.g. for data-loader workers): first expert review, item L19.

## Options

- **A. Every option the scripts set, in one committed file,** each overridable for one submission by an environment variable.
- **B. Options in the job script** (`#SBATCH` lines): conventional, but scattered and harder to override.

## Decision

Option A: [scripts/cluster/defaults.sh](../../../scripts/cluster/defaults.sh) holds every option the scripts set; `job.sbatch` hardcodes none.

| Option | Default | Why |
|---|---|---|
| partition | `all_usr_prod` | [ED-0002](ED-0002-cluster-partition.md) |
| GPU models | the allow-list | [ED-0004](ED-0004-gpu-allow-list.md) |
| nodes, tasks | 1, 1 | one run per job ([ED-0003](ED-0003-runs-and-jobs.md)) |
| GPUs | 1 | the models fit one GPU |
| CPUs per task | 6 | what each GPU reserves anyway, so no extra cost; programs can read it |
| time limit | 1 hour | short jobs queue faster; billing counts only the time used |
| warning signal | 2 minutes before the limit | [ED-0006](ED-0006-run-endings.md) |
| memory | not set: the cluster's default (3 GB per CPU, 18 GB) | fits the models |

- Override for one submission: `CLUSTER_TIME=04:00:00 scripts/cluster/submit.sh …`; any other option: `SBATCH_OPTS="--mem=32G"`.
- `run.json` records the options each job actually got ([ED-0009](ED-0009-run-records.md)).

## Consequences

- Real training runs will usually need a longer `CLUSTER_TIME` than the 1-hour default.
- A variable of the same name in `.env` would also override a default, silently: `.env` holds personal values only ([ED-0014](ED-0014-personal-values.md)).

## Revisit if

- a default is overridden for most runs: change the default;
- a model needs more memory or GPUs than the defaults.
