# PQ-001 — Upgrade PyTorch to 2.14.1 with CUDA 12.6?

- **Status:** open
- **Opened:** 2026-11-01

## Why it matters

- [PD-001](../decisions/PD-001-python-and-pytorch.md) uses torch 2.5.1 with CUDA 12.1, which no longer gets fixes.
- torch 2.14.1 is the newest release with a CUDA 12.6 build, the CUDA version the Unimore cluster supports on its compute nodes.
- An upgrade would supersede PD-001.

## Hypotheses

Not established yet:

- The compute nodes' drivers support CUDA 12.6, since the cluster loads and recommends its CUDA 12.6 module for them.
- 2.14.1 + CUDA 12.6 covers the same GPUs as 2.5.1 + CUDA 12.1: Pascal to Ada, not Blackwell. Pascal (GTX 1080) may have been dropped: check `torch.cuda.get_arch_list()` for `sm_60`.
- Numeric results change only at the level of floating-point noise.

## Evidence so far

- The PyTorch index lists `torch-2.14.1+cu126` for Python 3.12 on Linux (checked 2026-11-01).
- **Against the first hypothesis:** the first cluster job ran on node `germano` (RTX 2080 Ti) with driver **535.247.01**, which natively supports CUDA up to 12.2, not 12.6 (run `hello/20261101-222747-f38a`, 2026-11-01). A CUDA 12.6 build might still run there through CUDA's minor-version compatibility: to be tested, not assumed.

## Next action

Once the cluster workflow works:

1. Install it locally, on a branch, and check `torch.cuda.get_arch_list()`.
2. Run one short debug job on a cluster GPU node that prints the driver version and runs a CUDA operation.

## Resolution

—
