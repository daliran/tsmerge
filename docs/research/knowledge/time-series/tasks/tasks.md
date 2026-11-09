# Tasks

**In one sentence:** the same time series can be asked four different questions (what comes next, what's missing, what's abnormal, what kind is it), and each question is a different task with its own purpose, inputs, outputs and way of being judged.

- **Builds on:** [Time series](../time-series.md), [Patterns](../structure/patterns.md).
- **Used by:**
  - [Forecasting](forecasting.md)
  - [Imputation](imputation.md)
  - [Anomaly detection in time series](anomaly-detection.md)
  - [Classification](classification.md)
  - [Windows](../data-preparation/windows.md)
  - [Datasets](../datasets/README.md)

## The four tasks at a glance

A survey of deep time-series models groups the main tasks into four ([wang2026deep](../../../literature/wang2026deep.md), p. 3):

| Task | The question | Given | Produce |
|---|---|---|---|
| **Forecasting** | what comes next? | the past | the future values |
| **Imputation** | what's missing? | a series with gaps | the missing values |
| **Anomaly detection** | is something abnormal? | a series | which steps (or stretches) are abnormal |
| **Classification** | what kind of series is this? | a whole series | one label |

![The four tasks: forecast the future, fill the gaps, flag the abnormal value, label the whole series](assets/tasks.png)

Each has its own doc: [forecasting](forecasting.md), [imputation](imputation.md), [anomaly detection](anomaly-detection.md) and [classification](classification.md).

## One family

One way to see the four tasks: they share one skill, **understanding how the series normally behaves**. Forecasting uses it to continue the series, imputation to fill it in, anomaly detection to spot what departs from it, and classification to tell kinds of behavior apart.

That's why one model can serve all four: the TSLib (Time-Series-Library) benchmark uses a shared backbone with a small task-specific part on top ([wang2026deep](../../../literature/wang2026deep.md), p. 11).

## Key points

- **Forecasting:** past → future values. **Imputation:** a series with gaps → the missing values.
- **Anomaly detection:** series → normal or abnormal, step by step. **Classification:** whole series → one label.
- All four draw on understanding **normal behavior**, so one model with a shared backbone can serve them all.

## Sources

- [wang2026deep](../../../literature/wang2026deep.md): the four tasks, and the benchmark's shared backbone with task-specific heads.
