# ED-001 — Python 3.12.16 and PyTorch 2.14.1 with CUDA 12.6, managed by uv everywhere

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author
- **Answers:** question EQ-001 (opened 2026-11-01: upgrade from torch 2.5.1 + CUDA 12.1?)
- **History:**
  - 2026-11-01: torch 2.5.1 + CUDA 12.1 chosen; the upgrade deferred to a question.
  - 2026-11-02: upgraded to 2.14.1 + CUDA 12.6, after testing it locally and on the cluster; exact Python pin and tooling Python added after the first expert review.

## Problem

The same environment must run in two places:

- the local workstation, with an NVIDIA Turing GPU;
- the GPU nodes of the Unimore AImageLab-HPC Slurm cluster ([cluster.md](../cluster.md)).

PyTorch wheels ship their own CUDA runtime. So on each machine only two things matter:

- **the GPU architecture:** the wheel must contain kernels for it;
- **the driver:** it must support the wheel's CUDA version, natively or through CUDA's compatibility within a major version.

The cluster's `all_usr_prod` partition has 87 GPUs, from Pascal (GTX 1080) to Blackwell (RTX PRO 6000) ([GPU inventory](../cluster.md#partitions-and-gpus)); the drivers seen on its nodes are 535 (CUDA ≤ 12.2 natively). The local driver supports CUDA up to 13.4.

The cluster also offers its own Python and PyTorch as modules (Python 3.9–3.11; PyTorch 2.7 and 2.8 with CUDA 12.6).

## Options: PyTorch build

GPU coverage is counted on the 87 GPUs of `all_usr_prod`.

### A — torch 2.5.1 + CUDA 12.1

- Kernels for `sm_50` to `sm_90`: Pascal to Ada. **Coverage: 72 of 87 GPUs (83%)**; not usable: the 14 Blackwell GPUs and 1 untagged GPU.
- Mature, but no longer updated (November 2024).

### B — torch 2.14.1 + CUDA 12.6

- The newest release with a CUDA 12.6 build, the CUDA version the cluster itself supports.
- **The same kernels as A** (`sm_50` to `sm_90`, Pascal included): **coverage 72 of 87 GPUs (83%)**.
- A much newer PyTorch, with behavior changes accumulated over nine releases (e.g. `torch.load` defaults to `weights_only=True` since 2.6).

### C — torch 2.15 + CUDA 13.x

- Turing to Blackwell, dropping Pascal: **84 of 87 GPUs (97%)**.
- Needs a driver ≥ 580; the cluster's nodes have 535.

## Options: environment manager

### uv everywhere

- The same `uv.lock` gives the same Python, PyTorch and libraries on every machine, so every result is reproducible.
- Independent of which modules the cluster offers, and of the cluster itself if access ends.
- Costs a few GB of PyTorch and CUDA libraries in the cluster home folder (quota: 100 GB).

### uv locally, the cluster's modules on the cluster

- A PyTorch build the cluster's team tested; less storage.
- Local and cluster environments differ (Python, PyTorch version), so the lockfile wouldn't describe where most results come from.
- Changes whenever the cluster's modules change.

## Decision

- **PyTorch: option B, torch 2.14.1 with CUDA 12.6.** Same GPU coverage as A, a maintained version, and adopted before any experiment code exists, so no results are split across versions. Option C needs newer drivers than the cluster's.
- **Environment manager:** uv everywhere, for reproducibility. The cluster's Python and PyTorch modules are not used.
- **Python:** exactly **3.12.16** (`.python-version`), managed by uv only (`python-preference = "only-managed"`), so every machine runs the same Python build, never the system one. Pinning only `3.12` would let another machine pick a newer 3.12.x (first expert review, item L21).
- **The repository's own tooling uses the same Python:** scripts run with `uv run`; the guard hook, which runs on every tool call, uses the project environment's Python directly (`.venv/bin/python`), the fastest way to start it (first expert review, item L4).

**Verified** (2026-11-02):

- locally, on the RTX 2070 SUPER (driver supporting CUDA 13.4): matrix multiply, a cuDNN convolution and a backward pass;
- on the cluster, with driver 535.247.01: the same operations on an RTX 2080-class node (`germano`) and an RTX A5000 node (`huber`), through CUDA's compatibility within 12.x; then the project environment, rebuilt with 2.14.1, ran the `hello` job.
- Not tested directly: RTX 2080 Ti nodes (out of service at the time; same architecture as `germano`) and L40S (refused alone on `all_usr_prod` by the 24 GB rule, [ED-027](ED-027-gpu-pool.md)).

## Consequences

- **Cluster jobs must never land on Blackwell nodes.** Slurm constraints can't exclude a feature, so every GPU job lists the allowed GPU features with `--constraint`: [ED-004](ED-004-gpu-allow-list.md).
- **The environment is built on the cluster with uv** from the same `uv.lock`, in the home folder ([ED-008](ED-008-environment-integrity.md)).
- **Installing from the CUDA 12.6 index only:** `pyproject.toml` points torch at it. With PyPI as an extra index, uv would pick PyPI's default `+cu130` build, which needs a driver ≥ 580.

## Revisit if

- a library the experiments need drops Python 3.12 or torch 2.14;
- the cluster's drivers reach CUDA 13 (then option C would add the Blackwell GPUs);
- the cluster's GPUs change so that this build covers too few of them ([ED-004](ED-004-gpu-allow-list.md) reports new models at every submission).
