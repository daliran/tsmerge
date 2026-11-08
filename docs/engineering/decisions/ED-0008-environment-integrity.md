# ED-0008 — Runs can't use a mismatched environment

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author

## Problem

The cluster has one Python environment, built from `uv.lock` by `setup_remote.sh`. Raised by the first expert review (2026-11-01):

- **H2:** the lock hash that each job checks was rewritten only after a successful build, so during a rebuild, or after a failed one, the old hash stayed valid: a queued job could run on a half-updated environment.
- **M2:** rebuilding in place under running or queued jobs could give them a mix of old and new packages.
- **M7:** nothing checked that `uv.lock` matches `pyproject.toml`; plain `uv run` silently rewrites the lockfile when they differ, and the cluster installed whatever lockfile it got.
- **L3:** the build took several minutes directly on a shared login node, against the cluster's rules ([cluster.md](../cluster.md#access)).

## Options

### A — guard the single environment

- The hash is removed during a build; lockfile consistency is checked everywhere; no rebuilds while jobs run or wait.
- Small changes; one environment to keep within the home's file limit (ED-0005).

### B — one environment per lock hash

- Old jobs keep their environment while a new one is built.
- About 17,600 files per environment, in a home that already hit its file limit; needs cleanup rules.

## Decision

Option A:

- `setup_remote.sh` deletes the lock hash **before** building and writes it only after success: during a build or after a failure, every job refuses to start;
- the build uses `uv sync --locked`: a `uv.lock` that doesn't match `pyproject.toml` is refused, not installed; locally, `scripts/check.sh` runs `uv lock --check` and every step with `--locked` ([ED-0012](ED-0012-code-checks.md));
- the build runs as a Slurm step on `all_serial` (`srun`): still the login nodes and their local `/tmp` (as ED-0005 needs), but scheduled, and free;
- rule in [running.md](../running.md#the-cycle): don't rebuild while jobs run or wait.

**Verified** (2026-11-02): `setup_remote.sh` built the environment as an `srun` step on `all_serial`, including the rebuild for PyTorch 2.14.1; the jobs submitted afterwards passed the lock-hash check and completed.

## Consequences

- After changing dependencies, rerun `setup_remote.sh` before submitting; queued jobs with the old lockfile will refuse to start.
- The build waits for an `all_serial` slot, usually immediate.

## Revisit if

- you often need two environments at once (e.g. comparing PyTorch versions): then option B;
- `all_serial` slots become hard to get.
