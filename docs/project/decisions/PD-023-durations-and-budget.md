# PD-023 — Watch run durations and estimated cost from the run records

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author
- **Answers:** question PQ-007 (opened 2026-11-01, raised by the first expert review, items M19 and L26)

## Problem

- The cluster's yearly budget is a hard limit, and one run per GPU job ([PD-003](PD-003-runs-and-jobs.md)) bills at least 6 standard hours per GPU-hour, busy or not.
- More pressing in practice: choosing time limits. A run that hits its limit is lost and restarted from scratch ([PD-021](PD-021-runs-and-their-inputs.md)), and a run gets its limit minus 2 minutes ([PD-006](PD-006-run-endings.md)).
- The author's budget for this project is ample: cost is a secondary concern.

## Options

### A — look at durations and cost from the run records

- `run.json` already holds start, end, time limit, CPUs and GPUs: a small script turns them into a table.

### B — no tracking

- Nothing to build, but time limits are chosen blind, and spending is noticed only through `susage`.

## Decision

Option A, mainly for time limits:

- **[scripts/runs_summary.py](../../../scripts/runs_summary.py)** lists the pulled runs with status, GPU, duration, time limit, the share of the limit used, and an estimate of the standard hours billed;
- **choosing `CLUSTER_TIME`:** from the durations of similar runs, with a margin (and the 2 minutes);
- **cost:** checked with the same table, and with `susage` on the cluster; one run per job stays.

## Consequences

- Documented in [running.md](../running.md#durations-and-budget).
- The cost shown is an estimate of the cluster's billing formula, not the official figure (`susage` is).

## Revisit if

- the budget becomes tight (then: estimate every sweep before launching it, and consider several runs per job);
- the summary shows short runs wasting most of their billed time.
