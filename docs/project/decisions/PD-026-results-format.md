# PD-026 — Every run writes its metrics to `results/metrics.json`, in one fixed format

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author
- **Answers:** question PQ-009 (opened 2026-11-01, raised by the first expert review, item L25)
- **History:**
  - 2026-11-02: values during training (curves) get their own file, `results/history.jsonl` ([PD-033](PD-033-training-curves.md)), as foreseen below; `metrics.json` keeps the final values, written with `run.write_metrics()`.

## Problem

- Every number in the thesis must come from recorded results, by a script.
- Runs write `results/`, but there was no agreed format and no way to collect runs into tables.
- Fixed before the first sweep, a format costs little; fixed afterwards, earlier runs need converting.

## Options

### A — one fixed metrics format for every run, and one aggregation script

- Any run, of any experiment, can be read the same way.

### B — each experiment defines its own outputs, with its own aggregation script

- More freedom, but every experiment needs its own reader, and comparing across experiments is harder.

## Decision

Option A:

- every run writes **`results/metrics.json`**: a list of records, one per metric value, in "long" form, so new metrics or phases never change the format:

  ```json
  [
    {"phase": "merged", "split": "test", "metric": "mse", "value": 0.412},
    {"phase": "finetune_0", "split": "val", "metric": "mse", "value": 0.388}
  ]
  ```

  - `phase`: which model the value belongs to, when a run produces several (e.g. a base model, fine-tuned models, a merged model); omitted when there is one;
  - `split`: `train`, `val` or `test`;
  - `metric`: the metric's name; `value`: a number;
- one aggregation script, written with the first experiment, joins each run's `run.json`, `config.json` and `metrics.json` into one table per sweep or experiment; thesis tables and figures are produced from those tables.

## Consequences

- The experiment code writes `metrics.json` in this format from its first version.
- Documented in [runs.md](../runs.md#resultsmetricsjson-what-the-run-measured).

## Revisit if

- a result doesn't fit one number per record (e.g. curves): then add a separate file for it, and keep `metrics.json` for scalar values.
