# EQ-0013 — Can the P100 GPUs on `all_serial` run this project's PyTorch?

- **Status:** open
- **Opened:** 2026-11-02

## Why it matters

- `all_serial` is free, and its 8 P100 GPUs are the only ones there this PyTorch build supports (the K80s are too old) ([ED-0002](../decisions/ED-0002-cluster-partition.md)).
- If they work, light GPU work (short checks, small evaluations) can run without spending the budget; if not, every GPU job is billed.
- PyTorch 2.14.1 with CUDA 12.6 has kernels for the P100 (`sm_60`, [ED-0001](../decisions/ED-0001-python-and-pytorch.md)); what isn't known is the node's driver: CUDA 12.x needs a driver of at least the 525 series.

## Options

- **A. Test it once:** a short CPU-profile job on `all_serial` that requests the P100 (`CLUSTER_PROFILE=cpu SBATCH_OPTS="--constraint=gpu_P100_16G --gres=gpu:1" scripts/cluster/submit.sh hello python -m tsmerge.hello`), then read the driver and the result in `run.json`. About a minute, free.
- **B. Never use GPUs on `all_serial`:** simpler; light GPU work goes to `all_usr_prod`, billed.

## Hypotheses

Not established yet:

- The login nodes have the same driver series (535) as the compute nodes seen so far, which would work.

## Evidence so far

- Drivers seen on `all_usr_prod` nodes: 535 ([ED-0001](../decisions/ED-0001-python-and-pytorch.md)).

## Next action

Run the test in option A, with the user's approval (it uses the cluster).
