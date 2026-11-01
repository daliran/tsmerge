# PQ-002 — On `all_usr_prod`, exclude the L40S and A40 nodes too?

- **Status:** open
- **Opened:** 2026-11-01

## Why it matters

- On the Unimore cluster, [PD-002](../decisions/PD-002-cluster-partition.md) keeps the project off `boost_usr_prod`, so that high-memory GPUs stay available to projects that need them.
- But `all_usr_prod` contains the same high-end nodes, so jobs can still land on them.
- The GPU constraint decides which nodes are allowed. Blackwell is excluded in any case ([PD-001](../decisions/PD-001-python-and-pytorch.md)).
- The choice sets how many GPUs the project can use (queue times), how much memory each job can count on, and what the hardware can do (speed, number formats).

## The GPUs in `all_usr_prod`

87 GPUs in total, counted on 2026-11-01. Per model, see [cluster.md](../cluster.md#partitions-and-gpus).

## Options

| | A — older GPUs only | B — all except Blackwell | C — Turing and Ampere only |
|---|---|---|---|
| Models | 1080, 2080, 2080 Ti, RTX 5000, RTX 6000, A5000 | A + A40, L40S | A without the GTX 1080 |
| GPUs available | 32 of 87 (37%) | 72 of 87 (83%) | 30 of 87 (34%) |
| GPU memory per job | 8–24 GB | 8–45 GB | 11–24 GB |
| Total GPU memory | 513 GB | 2,313 GB | 497 GB |
| Uses high-memory GPUs | no | yes (40 GPUs, 45 GB each) | no |
| Tensor cores (fast fp16) | all but the 1080 | all but the 1080 | all |
| bf16 and TF32 | only the A5000 (5 GPUs) | A5000, A40, L40S (45 GPUs) | only the A5000 (5 GPUs) |

Always excluded, in every option:

- the 14 RTX PRO 6000 Blackwell GPUs (16%): PyTorch 2.5.1 has no kernels for them;
- 1 GPU on node `vegeta` (1%): it has no feature tag, so no constraint can select it.

### A — older GPUs only

- **Gains:** follows the spirit of PD-002; the high-memory GPUs stay free for others.
- **Costs:**
  - only 37% of the partition, so queues can be longer;
  - a job must fit in 8 GB (the GTX 1080);
  - the GTX 1080 (Pascal) has no tensor cores, so mixed precision doesn't speed it up.

### B — all except Blackwell

- **Gains:**
  - 83% of the partition: the most nodes, so the shortest queues;
  - the 40 A40 and L40S GPUs are several times faster than the older ones, with 45 GB each and bf16/TF32 support.
- **Costs:** it uses high-memory GPUs this project doesn't need, which is what PD-002 tries to avoid.

### C — Turing and Ampere only

- **Gains:**
  - every GPU has tensor cores and at least 11 GB;
  - the hardware is close to the local GPU (Turing), so local and cluster runs behave alike.
- **Costs:** the fewest GPUs (34%) and no high-end speed.

## Hypotheses

Not established yet:

- The project's models fit in 8 GB of GPU memory (needed for A) or in 11 GB (needed for C).
- Queue times on the older GPUs are acceptable for the planned workload.

## Evidence so far

- GPU counts per node: `sinfo -p all_usr_prod -N -o "%N|%G|%f"` (2026-11-01).
- [Cluster documentation on node features](https://ailb-web.ing.unimore.it/coldfront/documentation/flOS4).

## Current default

Until this is answered, the scripts use option B: the allowed list in `scripts/cluster/defaults.sh` ([PD-004](../decisions/PD-004-gpu-allow-list.md)).

## Next action

The author chooses. The choice is recorded as a decision when the job script is written.

## Resolution

—
