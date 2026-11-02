# Project decisions

Technical and organizational decisions: how the repository, the environment and the compute setup work.

Research decisions (methods, datasets, metrics) belong to the domain area. They get `DD-` ids, in their own folder, created with the first one.

**Decisions are history and rationale, not the documentation.** How things work is always described in the project docs ([setup](../setup.md), [cluster](../cluster.md), [running](../running.md), [runs](../runs.md), [CONTRIBUTING](../../../CONTRIBUTING.md), the folder READMEs), which link to the decisions for the *why*. A decision never holds the only copy of an operational fact.

**Why every relevant decision is written down:** without it, nobody can later reconstruct why something is the way it is, and nobody can tell whether a choice still holds. Each record states the problem it solves and when it should be reconsidered, so it can be checked, and if needed overturned, on its own reasons. Only truly minor choices (a wording, a variable name) go without a record.

## Rules

- **One file per decision:** `PD-NNN-short-slug.md`, e.g. `PD-001-python-and-pytorch.md`.
- **Stable ids:**
  - an id and its file name never change;
  - an id is never reused, not even for a rejected decision;
  - only a typo in a title may be fixed;
  - the next id is the highest existing one plus one.
- **Statuses:** `proposed` → `accepted` → `superseded by PD-NNN`, or `rejected`. Only the user accepts or rejects a decision.
- **Decisions are not frozen.** When new information emerges (a test result, a cluster rule, a consequence), update the decision in place, even after it is accepted and committed, and add a dated line to its **History** saying what changed and why.
- **When the choice itself is reversed,** write a new decision that supersedes it, and change the old one's status line to `superseded by PD-NNN`, so both the old reasons and the new ones stay readable.
- **A decision that no longer holds** is either kept, with its status (`superseded by PD-NNN` or `rejected`) and a line saying why, or deleted. Keep it when its reasons are still worth knowing (e.g. it's likely to be proposed again); delete it when nothing depends on it and the new decision already explains the change. Either way, its id is never reused.
- **Docs follow decisions.** When a decision is accepted, updated or superseded, in the same step:
  - update every Markdown file it affects, and every diagram ([diagrams](../diagrams/README.md));
  - close the [questions](../questions/README.md) it answers: their content moves into the decision, and the question files are deleted.
- **Short and readable:** about one screen, one idea per line, lists as bullets. Link to details instead of restating them.

## Template

```markdown
# PD-NNN — <the choice, stated as what we do>

- **Status:** proposed | accepted | superseded by PD-NNN | rejected
- **Date:** YYYY-MM-DD
- **Decided by:** the author
- **Answers:** question PQ-NNN (opened YYYY-MM-DD, …), if the decision closes one
- **History:** (once it changes) one dated line per update: what changed, and why

## Problem

What went wrong or was missing, why it mattered, the constraints; where it came from
(a review, a failed run, a question).

## Options

### A — …

- what it gives;
- what it costs.

### B — …

- what it gives;
- what it costs.

## Decision

What we chose, and why. How it was verified, if it was.

## Consequences

- what changes;
- what gets harder;
- related small fixes;
- follow-ups (PQ-NNN).

## Revisit if

- the conditions under which this decision should be reconsidered.
```

## Index

| Id | Decision | Status | Date |
|---|---|---|---|
| [PD-001](PD-001-python-and-pytorch.md) | Python 3.12.16 and PyTorch 2.14.1 with CUDA 12.6, managed by uv everywhere | accepted | 2026-11-01 |
| [PD-002](PD-002-cluster-partition.md) | Cluster partitions: `all_usr_prod` for GPU work, `all_serial` for light work, never `boost_usr_prod` | accepted | 2026-11-01 |
| [PD-003](PD-003-runs-and-jobs.md) | Experiments, runs and jobs: one run per job, one folder per run | proposed | 2026-11-01 |
| [PD-004](PD-004-gpu-allow-list.md) | GPU models: a committed allow-list, checked at submit time and in the job | accepted | 2026-11-01 |
| [PD-005](PD-005-uv-cache-on-the-cluster.md) | On the cluster, uv's cache is temporary, on the login node's local disk | accepted | 2026-11-01 |
| [PD-006](PD-006-run-endings.md) | Every run records how it ended | accepted | 2026-11-01 |
| [PD-007](PD-007-run-provenance.md) | Runs carry their own provenance: commit plus a complete patch | accepted | 2026-11-01 |
| [PD-008](PD-008-environment-integrity.md) | Runs can't use a mismatched environment | accepted | 2026-11-02 |
| [PD-009](PD-009-run-records.md) | What every run records: `run.json` and `config.json` | accepted | 2026-11-01 |
| [PD-010](PD-010-safe-submissions.md) | Submissions fail cleanly and never overwrite a run | accepted | 2026-11-02 |
| [PD-011](PD-011-expert-review-guard.md) | Expert reviews: a guard keeps the review agents off the cluster | accepted | 2026-11-01 |
| [PD-012](PD-012-code-checks.md) | Code checks: one script, explicit rules, run on every commit | accepted | 2026-11-02 |
| [PD-013](PD-013-default-job-resources.md) | Default job resources, all set in one committed file | accepted | 2026-11-02 |
| [PD-014](PD-014-personal-values.md) | Personal values in a git-ignored `.env`, project settings committed | accepted | 2026-11-01 |
| [PD-015](PD-015-session-unlock.md) | One session step unlocks SSH keys and the cluster | accepted | 2026-11-01 |
| [PD-016](PD-016-project-docs.md) | Project docs split by concern; questions end as decisions or docs | accepted | 2026-11-02 |
| [PD-017](PD-017-git-by-people.md) | People run git; AI agents propose commits | accepted | 2026-11-01 |
| [PD-018](PD-018-self-contained-repository.md) | A self-contained repository: no personal data, no references to earlier implementations | accepted | 2026-11-01 |
| [PD-019](PD-019-expert-reviews.md) | In-depth reviews by a panel of independent expert agents | accepted | 2026-11-01 |
| [PD-020](PD-020-dataset-location.md) | Datasets live in a data folder outside the code: `data/` locally, the work area on the cluster | accepted | 2026-11-02 |
| [PD-021](PD-021-runs-and-their-inputs.md) | Runs don't resume; a run names the earlier runs it reads | accepted | 2026-11-02 |
| [PD-022](PD-022-cpu-jobs.md) | CPU-only jobs go through `submit.sh` too, on `all_serial` by default | accepted | 2026-11-02 |
| [PD-023](PD-023-durations-and-budget.md) | Watch run durations and estimated cost from the run records | accepted | 2026-11-02 |
| [PD-024](PD-024-large-transfers.md) | Large transfers go through the login node, as resumable copies | accepted | 2026-11-02 |
| [PD-025](PD-025-run-safety.md) | Runs keep their provenance and results safe: pushed commits, no requeue, local backup | accepted | 2026-11-02 |
| [PD-026](PD-026-results-format.md) | Every run writes its metrics to `results/metrics.json`, in one fixed format | accepted | 2026-11-02 |
| [PD-027](PD-027-gpu-pool.md) | Runs may use every allowed GPU; numerics are made explicit, not left to the hardware | accepted | 2026-11-02 |
| [PD-028](PD-028-diagrams.md) | Diagrams: Mermaid sources, committed PNG images, rendered with Docker | accepted | 2026-11-02 |
