# PD-001 — Python 3.12 and PyTorch 2.5.1 with CUDA 12.1, managed by uv everywhere

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author

## Context

The same environment must run in two places:

- the local workstation, with an NVIDIA Turing GPU;
- the GPU nodes of the Unimore AImageLab-HPC Slurm cluster ([cluster.md](../cluster.md)).

PyTorch wheels ship their own CUDA runtime. So on each machine only two things matter:

- **the GPU architecture:** the wheel must contain kernels for it;
- **the driver:** it must support the wheel's CUDA version.

The cluster's `all_usr_prod` partition has 87 GPUs, from Pascal (GTX 1080) to Blackwell (RTX PRO 6000); see the [GPU inventory](../cluster.md#partitions-and-gpus).

The cluster also offers its own Python and PyTorch as modules (Python 3.9–3.11; PyTorch 2.7 and 2.8 with CUDA 12.6).

## Options: PyTorch build

GPU coverage is counted on the 87 GPUs of `all_usr_prod`.

### A — torch 2.5.1 + CUDA 12.1

- Kernels for `sm_50`, `sm_60`, `sm_70`, `sm_75`, `sm_80`, `sm_86`, `sm_90`: Pascal to Ada.
- **Cluster coverage: 72 of 87 GPUs (83%).** Not usable: the 14 Blackwell GPUs (16%) and 1 untagged GPU (1%).
- Runs on the local GPU (verified).
- Needs a driver ≥ 525.
- Mature, but no longer updated.

### B — torch 2.14.1 + CUDA 12.6

- The newest release with a CUDA 12.6 build, the CUDA version the cluster itself supports.
- **Cluster coverage: not verified.** At most 72 of 87 GPUs (83%), as A. Newer PyTorch releases have been dropping kernels for the oldest architectures, so the 2 GTX 1080 (Pascal) may not be covered: then 70 of 87 (80%).
- Runs on the local GPU (expected; not verified).
- Needs a driver ≥ 560.
- A much newer PyTorch, with behavior changes accumulated over nine releases (e.g. `torch.load` defaults to `weights_only=True` since 2.6).

### C — torch 2.15 + CUDA 13.x

- Turing to Blackwell; drops Pascal.
- **Cluster coverage: 84 of 87 GPUs (97%)**, adding the 14 Blackwell GPUs but losing the 2 GTX 1080 (2%).
- Needs a driver ≥ 580: verified locally, **not verified** on the cluster's compute nodes.

## Options: environment manager

### uv everywhere

- The same `uv.lock` gives the same Python, PyTorch and libraries on every machine, so every result is reproducible.
- Independent of which modules the cluster offers, and of the cluster itself if access ends.
- Costs a few GB of PyTorch and CUDA libraries in the cluster home folder (quota: 100 GB).

### uv locally, the cluster's modules on the cluster

- A PyTorch build the cluster's team tested; less storage.
- Local and cluster environments differ (Python 3.12 vs 3.11; PyTorch 2.5.1 vs 2.8), so the lockfile wouldn't describe where most results come from.
- Changes whenever the cluster's modules change.

### Python

3.12 works with all three PyTorch options and with the libraries we need.

## Decision

- **PyTorch:** option A, torch 2.5.1 with CUDA 12.1.
  - It is verified on the local GPU and covers 83% of the cluster's GPUs.
  - The upgrade to B is deferred until the environment and the cluster workflow are complete: see [PQ-001](../questions/PQ-001-upgrade-pytorch-cuda-12-6.md).
- **Environment manager:** uv everywhere, for reproducibility. The cluster's Python and PyTorch modules are not used.
- **Python:** 3.12, managed by uv only (`python-preference = "only-managed"`), so every machine runs the same Python build, never the system one.

## Consequences

- **Cluster jobs must never land on Blackwell nodes.** Slurm constraints can't exclude a feature, so every GPU job lists the allowed GPU features with `--constraint`. How the list is kept and checked: [PD-004](PD-004-gpu-allow-list.md).
- **The environment is built on the cluster with uv** from the same `uv.lock`, in the home folder.
- **Verified on the cluster** on 2026-11-01: node `germano`, RTX 2080 Ti, driver 535.247.01 (run `hello/20261101-222747-f38a`).
