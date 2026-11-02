# PD-030 — Experiment code in a `tsmerge/` package, run as modules, not installed; a shared run helper

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author

## Problem

- The only script was a smoke test inside the cluster tooling (`scripts/cluster/hello.py`): there was no place for experiment code.
- Every recorded run must import exactly its own frozen code, on the cluster as locally ([PD-007](PD-007-run-provenance.md), [PD-029](PD-029-local-runs.md)).
- Every experiment must find its folders, set seeds and numerics, and write `config.json` and `metrics.json` in fixed formats ([PD-009](PD-009-run-records.md), [PD-026](PD-026-results-format.md), [PD-027](PD-027-gpu-pool.md)).

## Options

### Where the code lives, and how it's imported

- **A. A `tsmerge/` package at the repository root, run as `python -m tsmerge.<module>`, not installed.** Python finds the package in the folder the run starts from: the run's frozen `code/`. A script started by path fails at once with "No module named tsmerge".
- **B. An installed package (`src/` layout, editable install).** Importable from anywhere, but on the cluster the environment is built from the code mirror, which every submission overwrites: a script started by path would silently import the mirror's newer code instead of its frozen copy.

### A shared helper

- **A. A minimal helper now** (folders, device, seeds, numerics, the two records).
- **B. None until real experiments:** each script repeats the same code.

## Decision

- **Code: option A.** `pyproject.toml` keeps `package = false`; pytest gets the repository root on its import path (`pythonpath = ["."]`).
- **Helper: option A,** [tsmerge/run.py](../../../tsmerge/run.py):
  - `run_dir()`, `data_dir()`, `runs_root()`: the run's folders from `RUN_DIR`, `DATA_DIR`, `RUNS_ROOT`; outside a recorded run, `outputs/scratch/`, `data/` and `outputs/runs/`;
  - `device("auto")`, `seed_everything(seed)`;
  - `set_numerics()`: explicit cuDNN, determinism and TF32 settings, **TF32 off by default**, so results don't depend on which GPU a run lands on;
  - `write_config()` and `write_metrics()`: the two records in their fixed formats; metrics outside the format are refused.
- **The template and smoke test:** [tsmerge/hello.py](../../../tsmerge/hello.py) fits a linear model to synthetic data through every step a real experiment takes; it replaces `scripts/cluster/hello.py`.

**Verified** (2026-11-02): `python -m tsmerge.hello` as a recorded run locally (RTX 2070 SUPER) and on the cluster (job 178372, RTX 2080 Ti): both imported their frozen copy and wrote `config.json` and `metrics.json`; with the same seeds, both reached the same validation error (0.0096).

## Consequences

- Modules are always started as `python -m tsmerge.<module>` from the repository root (or a run's `code/`); the VS Code configurations do this ([PD-031](PD-031-vs-code.md)).
- TF32 off makes Ampere and newer GPUs slower on large matrix products; an experiment can turn it on explicitly, and `config.json` records it.

## Revisit if

- notebooks in a subfolder need to import `tsmerge` (then: an editable install locally only, never in the cluster environment);
- the helper grows beyond what every experiment needs (then: split it).
