# Project decisions

Technical and organizational decisions: how the repository, the environment and the compute setup work.

Research decisions (methods, datasets, metrics) belong to the domain area. They get `DD-` ids, in their own folder, created with the first one.

## Rules

- **One file per decision:** `PD-NNN-short-slug.md`, e.g. `PD-001-python-and-pytorch.md`.
- **Stable ids:**
  - an id and its file name never change;
  - an id is never reused, not even for a rejected decision;
  - only a typo in a title may be fixed;
  - the next id is the highest existing one plus one.
- **Statuses:** `proposed` → `accepted` → `superseded by PD-NNN`, or `rejected`. Only the user accepts or rejects a decision.
- **Accepted decisions are never edited.** To change one:
  1. write a new decision that supersedes it;
  2. change only the old one's status line to `superseded by PD-NNN`.
- **Docs follow decisions.** When a decision is accepted or superseded, in the same step:
  - update every Markdown file it affects;
  - close the [questions](../questions/README.md) it answers.
- **Short and readable:** about one screen, one idea per line, lists as bullets. Link to details instead of restating them.

## Template

```markdown
# PD-NNN — <the choice, stated as what we do>

- **Status:** proposed | accepted | superseded by PD-NNN | rejected
- **Date:** YYYY-MM-DD
- **Decided by:** the author

## Context

What forced the decision, the constraints, related questions (PQ-NNN).

## Options

### A — …

- what it gives;
- what it costs.

### B — …

- what it gives;
- what it costs.

## Decision

What we chose, and why.

## Consequences

- what changes;
- what gets harder;
- follow-ups (PQ-NNN).
```

## Index

| Id | Decision | Status | Date |
|---|---|---|---|
| [PD-001](PD-001-python-and-pytorch.md) | Python 3.12 and PyTorch 2.5.1 with CUDA 12.1, managed by uv everywhere | accepted | 2026-11-01 |
| [PD-002](PD-002-cluster-partition.md) | Cluster partitions: `all_usr_prod` for GPU work, `all_serial` for light work, never `boost_usr_prod` | accepted | 2026-11-01 |
| [PD-003](PD-003-runs-and-jobs.md) | Experiments, runs and jobs: one run per job, one folder per run | proposed | 2026-11-01 |
| [PD-004](PD-004-gpu-allow-list.md) | GPU models: a committed allow-list, checked at submit time and in the job | accepted | 2026-11-01 |
| [PD-005](PD-005-uv-cache-on-the-cluster.md) | On the cluster, uv's cache is temporary, on the login node's local disk | accepted | 2026-11-01 |
