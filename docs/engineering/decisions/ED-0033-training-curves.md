# ED-0033 — Training curves go in the run folder (`results/history.jsonl`); no wandb for now

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author
- **Answers:** question EQ-0011 (opened 2026-11-02: should runs also be tracked in wandb?)

## Problem

- Each run recorded its settings (`config.json`) and final values (`results/metrics.json`), but nothing recorded values during training (loss per step or epoch).
- Training experiments need curves, to see convergence and to compare runs.

## Options

- **A. wandb,** offline on the cluster and synced from your machine after pulling: live dashboards and a shared UI.
  - Costs:
    - a new dependency (several thousand files in the cluster environment, which already hit the home's file limit, [ED-0005](ED-0005-uv-cache-on-the-cluster.md)),
    - an API key
    - and a sync step.
  - Whether compute nodes reach the internet wasn't verified ([EQ-0014](../questions/EQ-0014-compute-node-internet.md)).
- **B. Curves in the run folder:** a file written by the run helper, pulled and backed up with the run; no setup, no dashboard.

## Decision

Option B:

- **`results/history.jsonl`:** one JSON line per value, `{"step", "epoch"?, "phase"?, "split", "metric", "value"}`, the same fields as `metrics.json` plus the step;
  - written by `run.log_history()` ([tsmerge/run.py](../../../tsmerge/run.py)), appended and flushed at once, so a stopped run keeps every point logged before it stopped;
- each run starts a new curve (`run.write_config()` clears a curve left in `outputs/scratch/` by an earlier quick try);
- **plots** come from a script reading these files, written with the first training experiment (it needs a plotting library, a dependency to approve then).

## Consequences

- No live dashboard: curves are seen after pulling, or with `logs.sh` while a run goes (the code also prints them).
- Run folders keep `wandb/` reserved; if wandb is added later, these files can be uploaded to it, so nothing is lost.
- Documented in [runs.md](../runs.md#resultshistoryjsonl-curves-during-the-run).

## Revisit if

- comparing many runs' curves by hand becomes slow (then: option A, or a local dashboard);
- the cluster's compute nodes turn out to reach the internet, making live tracking cheap.
