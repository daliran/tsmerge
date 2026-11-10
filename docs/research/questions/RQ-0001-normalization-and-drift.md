# RQ-0001 — Should the experiments normalize once, per window, or both?

- **Status:** open
- **Opened:** 2026-11-10

## Why it matters

- Per-window normalization removes shifts in level and spread from every input window ([normalization in time series](../knowledge/time-series/data-preparation/normalization.md#normalization-or-the-learning-method)).
- Part of the drift between periods then disappears before training: the periods look more alike, and the continual strategies (joint training, fine-tuning, task arithmetic) have less drift to handle.
- A comparison of the strategies would then measure only the drift that normalization leaves behind.
- In anomaly detection, per-window normalization also hides anomalies that change a whole window's level or spread, and can turn a reconstruction score into roughly the window variance ([anon2026when](../literature/anon2026when.md), p. 6).

## Options

- **A. Normalize once,** with statistics from the first training period: the strategies meet the full drift; drift may also raise false alarms and push values outside the training range.
- **B. Normalize per window** (e.g. RevIN, reversible instance normalization), as many deep models and benchmarks do: matches common practice; hides part of the drift and some anomalies.
- **C. Run both:** shows how much of each strategy's result depends on the normalization; doubles the runs for the affected experiments.

## Hypotheses

Not established yet:

- The gap between joint training and the continual strategies is smaller with per-window normalization than with global normalization.

## Evidence so far

- Normalization as stationarization, and its link to distribution shift: [wang2026deep](../literature/wang2026deep.md), p. 3.
- The variance shortcut of per-window normalization in anomaly detection: [anon2026when](../literature/anon2026when.md), pp. 5–6.

## Next action

Check which normalization the chosen models and the Time-Series-Library apply by default, then decide for the first experiment.
