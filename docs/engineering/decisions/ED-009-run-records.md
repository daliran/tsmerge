# ED-009 — What every run records: `run.json` and `config.json`

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author
- **History:**
  - 2026-11-02: `run.json` gains `launcher` (`cluster` or `local`) and is also written by `run_local.sh` ([ED-029](ED-029-local-runs.md)); `config.json` is written with the helper in `tsmerge/run.py` ([ED-030](ED-030-experiment-code.md)).

## Problem

A result is only useful if you can later say what produced it and compare it with others. Raised by the first expert review (2026-11-01):

- **M3:** runs recorded their command line, but no resolved configuration, seed, data version or determinism settings; analysis would have had to parse command lines.
- **M14:** [ED-003](ED-003-runs-and-jobs.md) promised a sweep id in `run.json`, but nothing set one.
- **M15:** the Slurm options a job actually got (time limit, GPUs, overrides) weren't recorded, and `sacct`'s records expire.

## Options

### A — two records per run, with fixed contents

- `run.json` (written by the scripts): how the run was launched and how it went.
- `config.json` (written by the experiment code): what it computed with.

### B — one record, filled by the scripts

- Simpler, but the scripts can't know the configuration the code actually applied (defaults, derived values).

## Decision

Option A.

**`run.json`**, written by `submit.sh` and completed by the job:

- identity: run id, experiment, **sweep id** (`SWEEP=<id> scripts/cluster/submit.sh …`), command;
- code and environment: commit, uncommitted changes (yes/no), `uv.lock` hash, uv version;
- **the Slurm options actually used:** account, partition, GPU constraint, nodes, tasks, CPUs, GPUs, time limit, warning signal, extra options;
- where it ran: host, job id, GPU model and compute capability, driver, Python, PyTorch, CUDA and cuDNN versions;
- how it ended ([ED-006](ED-006-run-endings.md)).

**`config.json`**, written by the experiment code when the run starts, locally and on the cluster:

- `config`: every setting with its final value, **defaults included**;
- `seeds`: a training seed and a separate evaluation seed (default: training + 1), so evaluation sampling doesn't depend on training;
- `data`: each dataset's name, source or version, files checksum and split definition;
- `determinism`: `cudnn.deterministic`, `cudnn.benchmark`, `allow_tf32` (matmul and cuDNN), `use_deterministic_algorithms`.

## Consequences

- Results are compared by reading files, never by parsing commands or folder names.
- `config.json` is written with `run.write_config()` ([tsmerge/run.py](../../../tsmerge/run.py)), as `tsmerge/hello.py` shows.
- Datasets come from `DATA_DIR` ([ED-020](ED-020-dataset-location.md)); `config.json` records which ones and their checksums.
- `run.json` also lists the earlier runs a run reads, in `inputs` ([ED-021](ED-021-runs-and-their-inputs.md)).

## Revisit if

- analysis needs a field neither record has: add it here first, then to the code.
