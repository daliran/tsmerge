# ED-0014 — Personal values in a git-ignored `.env`, project settings committed

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author

## Problem

- The scripts need personal values: SSH key names, the cluster account, home and work paths. Committed files must never contain them (the privacy rule in [CLAUDE.md](../../../CLAUDE.md)).
- Project settings (partition, allowed GPUs, job defaults) are decisions: they must be visible in git and the same on every machine.

## Options

### A — one root `.env` (git-ignored) plus a committed `.env.example`

- One place for every personal value, now and later (e.g. a data path); a common convention that tools understand.
- It mixes unrelated settings, so it needs clear sections.

### B — `scripts/cluster/cluster.env`

- Scoped to the cluster scripts, but each future kind of personal value would need another file.

## Decision

Option A:

- **`.env`** (git-ignored): personal values only: `SSH_KEYS`, `CLUSTER_HOST`, `CLUSTER_ACCOUNT`, `CLUSTER_HOME_DIR`, `CLUSTER_WORK_DIR`, and optionally `DATA_DIR` ([ED-0020](ED-0020-dataset-location.md));
- **[.env.example](../../../.env.example)** (committed): the same keys with placeholders, as the template;
- **project settings are never in `.env`:** they live in committed files, e.g. [defaults.sh](../../../scripts/cluster/defaults.sh) ([ED-0013](ED-0013-default-job-resources.md)).

## Consequences

- A new clone copies `.env.example` to `.env` and fills it in ([setup.md](../setup.md#7-the-cluster-once-per-account)).
- `.gitignore` excludes `.env` and keeps `.env.example` (`!.env.example`).

## Revisit if

- personal values need to differ per tool or per machine in ways one file can't express.
