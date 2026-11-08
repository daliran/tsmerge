# ED-022 — CPU-only jobs go through `submit.sh` too, on `all_serial` by default

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author
- **Answers:** question EQ-006 (opened 2026-11-01, raised by the first expert review, item M17)

## Problem

- [ED-002](ED-002-cluster-partition.md) sends CPU-only and light work (data preparation, aggregating results) to `all_serial`, but `submit.sh` only supported GPU jobs: it always requested a GPU and the GPU allow-list, and every job checked its GPU.
- So such work ran either by hand (no frozen code, no `run.json`) or as a billed GPU job.

## Options

### A — a CPU profile in `submit.sh`

- Same run folder, provenance and `run.json` as GPU runs; about 20 lines.

### B — keep `submit.sh` GPU-only

- No change, but CPU work stays untracked.

**Where CPU jobs run:**

| | `all_serial` | a regular node (`all_usr_prod`, CPU only) |
|---|---|---|
| Cost | free | billed by CPU and memory (about 2.3 standard hours per hour with 6 cores) |
| Where | the login nodes, but through Slurm (scheduled, allowed) | the GPU nodes, taking cores GPU jobs need |
| Time limit | 4 h | 24 h |
| Resources | modest, shared | larger |

## Decision

Option A, on `all_serial` by default:

- `CLUSTER_PROFILE=cpu scripts/cluster/submit.sh …`: no GPU request, no GPU list, no GPU check in the job;
- the partition is `CLUSTER_CPU_PARTITION` ([defaults.sh](../../../scripts/cluster/defaults.sh)), `all_serial` by default: free, and it leaves the GPU nodes' cores to GPU jobs;
- for heavy or long CPU work, override it for that submission: `CLUSTER_CPU_PARTITION=all_usr_prod` (billed, up to 24 h);
- `run.json` records the profile, with 0 GPUs and no constraint.

**Verified:** locally, a simulated CPU job skipped the GPU check and received `DATA_DIR` and `RUNS_ROOT` (2026-11-02).

## Consequences

- Documented in [running.md](../running.md#where-jobs-run).
- `all_serial` jobs stop after 4 hours, minus the 2-minute warning ([ED-006](ED-006-run-endings.md)).

## Revisit if

- CPU jobs often need more than 4 hours or more resources (then: change the default partition);
- `all_serial` slots become hard to get.
