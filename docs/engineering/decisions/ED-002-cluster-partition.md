# ED-002 — Cluster partitions: `all_usr_prod` for GPU work, `all_serial` for light work, never `boost_usr_prod`

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author

## Context

The Unimore AImageLab-HPC Slurm cluster has three GPU partitions ([documentation](https://ailb-web.ing.unimore.it/coldfront/documentation/UKN8n)). GPU counts are from `sinfo` on 2026-11-01:

| Partition | Nodes | GPUs | Max time | Cost |
|---|---|---|---|---|
| `all_serial` (the default) | the 2 login nodes | 24: 16 K80, 8 P100 | 4 h | free |
| `all_usr_prod` | every GPU node | 87, from GTX 1080 to RTX PRO 6000 | 24 h | billed |
| `boost_usr_prod` | the high-end nodes only | 54: 4 A40, 36 L40S, 14 RTX PRO 6000 | 24 h | billed |

- The documentation's own advice is: "When in doubt, use `all_usr_prod`".
- In the author's understanding of the cluster's internal rules, `boost_usr_prod` is meant for projects that really need high-memory GPUs, so that those GPUs stay available to the people who need them. This rule is not stated on the documentation site; it was later confirmed by the cluster itself (see Consequences).
- This project's models don't need high GPU memory.
- Some work needs no GPU, or very little: data preparation, result aggregation, quick checks.
- The login nodes are shared by every user.

## Options

### A — `all_usr_prod` for everything

- 87 GPUs, 24 h per job.
- Billed even for work that needs no GPU.

### B — `boost_usr_prod` for GPU work

- 54 high-end GPUs (45–96 GB), faster, with a higher scheduling priority.
- Takes high-memory GPUs this project doesn't need.

### C — `all_usr_prod` for GPU work, `all_serial` for CPU-only or light GPU work

- GPU training gets the 87 GPUs of `all_usr_prod`.
- Light work runs free of charge on `all_serial`, through Slurm, with 4 h per job.
- On `all_serial`, only the 8 P100 GPUs can run this project's PyTorch: the 16 K80 GPUs are too old for CUDA 12 ([ED-001](ED-001-python-and-pytorch.md)).

## Decision

Option C.

- **GPU training and evaluation:** `all_usr_prod`.
- **CPU-only or very light GPU work:** `all_serial`, always through `sbatch` or `srun`.
- **Never `boost_usr_prod`.**
- **Every job states its partition explicitly**, so a job never lands on `all_serial` by accident.
- **Never run long or blocking processes directly on a login node**, Python included: the login nodes are shared. Anything that takes more than a few minutes goes through `srun` or `sbatch`, even when it needs no GPU.

## Consequences

- **`all_usr_prod` also contains the high-end nodes**, so jobs can still land on them unless the GPU constraint excludes them:
  - Blackwell is always excluded ([ED-001](ED-001-python-and-pytorch.md));
  - L40S and A40 stay allowed, as part of a mixed list ([ED-027](ED-027-gpu-pool.md)).
- **The memory rule is real** (found 2026-11-02, not on the documentation site): on `all_usr_prod`, a job whose GPU list asks for more than 24 GB of GPU memory is refused and sent to `boost_usr_prod`. This confirms the author's understanding of the internal rules behind this decision.
- **Light GPU work on `all_serial` must request the P100** (`--constraint=gpu_P100_16G`). The P100 node's driver is not verified yet ([EQ-013](../questions/EQ-013-p100-driver.md)).
- **Personal values are not part of this decision.** The Slurm account and personal paths stay out of committed files.

## Revisit if

- the cluster's rules for `boost_usr_prod` change, or a model needs more GPU memory than `all_usr_prod`'s older GPUs offer;
- the `all_serial` GPUs become unusable for light work, or light work needs a GPU too often.
