# ED-0004 — GPU models: a committed allow-list, checked at submit time and in the job

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author

## Context

- On the Unimore cluster, `all_usr_prod` mixes GPUs from Pascal to Blackwell ([cluster.md](../cluster.md#partitions-and-gpus)).
- This project's PyTorch build can't run on Blackwell ([ED-0001](ED-0001-python-and-pytorch.md)). A job that lands there looks healthy for about 30 seconds, then fails at the first CUDA operation with "no kernel image is available".
- GPU models are chosen with `--constraint`. Slurm can't exclude a model, and the cluster rejects `--exclude`, so a job must list the models it allows.
- The cluster's hardware changes over time. A fixed list goes stale:
  - a **new** model is never used, silently;
  - a **removed** model makes the list wrong.
- The allowed models are a project decision, not a personal value: they must be visible in git and the same on every machine.

## Options

### Where the list lives

- **In `.env`:** easy to change locally, but invisible in git; it can differ between machines, and its changes leave no history.
- **In a committed file:** reviewed changes, with history, the same everywhere. A one-off override is still possible with `SBATCH_OPTS="--constraint=…"`.

### How it stays correct

- **A. Fixed allow-list only:** safe, but goes stale silently.
- **B. Build the list at submit time** from the partition's models minus a deny-list: adapts automatically, but admits unknown new models, which may crash.
- **C. Allow-list plus a drift check at submit time:** safe, and changes on the cluster are reported at the next submission.
- **D. Runtime check in the job:** the job verifies its GPU before running anything. Combinable with A, B or C.

## Decision

- **The list lives in a committed file:** `scripts/cluster/defaults.sh`, with the partition. `.env` keeps only personal values.
- **Two explicit lists** cover every GPU model in the partition:
  - **allowed** models (used for `--constraint`);
  - **excluded** models, each with its reason (now: Blackwell, ED-0001).
- **C + D:**
  - **Drift check, before every submission** (`submit.sh`): it compares the two lists with the partition's actual models (`sinfo`).
    - An allowed model that no longer exists → the submission stops with an error.
    - A model in neither list → a warning; it isn't used until someone adds it to one of the lists.
  - **Runtime check, in every job** (`job.sbatch` runs `check_gpu.py`): if the node's GPU architecture isn't supported by the installed PyTorch, the job stops at once with a clear message and is recorded as failed.

## Consequences

- No job can run on Blackwell by accident, and a hardware change on the cluster is noticed at the next submission instead of never.
- Changing the allowed GPUs is a commit to `defaults.sh`, together with the decision behind it (ED-0027, ED-0001).
- When PyTorch is upgraded ([ED-0001](ED-0001-python-and-pytorch.md)), the excluded list must be reviewed.

## Revisit if

- PyTorch is upgraded ([ED-0001](ED-0001-python-and-pytorch.md)): review the excluded list;
- the drift check reports new GPU models;
- the GPU pool is reconsidered ([ED-0027](ED-0027-gpu-pool.md)).
