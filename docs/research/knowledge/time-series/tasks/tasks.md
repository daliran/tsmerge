# Tasks

**In one sentence:** the same time series can be asked four different questions (what comes next, what's missing, what's abnormal, what kind is it), and each question is a different task with its own purpose, inputs, outputs and way of being judged.

- **Builds on:** [Time series](../time-series.md), [Patterns](../structure/patterns.md).
- **Used by:** [Forecasting](forecasting.md), [Imputation](imputation.md), [Anomaly detection](anomaly-detection.md), [Classification](classification.md).

## The four tasks at a glance

The time-series survey we read groups the main tasks into four ([wang2026deep](../../../literature/wang2026deep.md), p. 3):

| Task | The question | Given | Produce |
|---|---|---|---|
| **Forecasting** | what comes next? | the past | the future values |
| **Imputation** | what's missing? | a series with gaps | the missing values |
| **Anomaly detection** | is something abnormal? | a series | which steps (or stretches) are abnormal |
| **Classification** | what kind of series is this? | a whole series | one label |

![The four tasks: forecast the future, fill the gaps, flag the abnormal value, label the whole series](assets/tasks.png)

This project works on two of them, **[forecasting](forecasting.md)** and **[anomaly detection](anomaly-detection.md)**. The other two, [imputation](imputation.md) and [classification](classification.md), are described for completeness: they share the same ideas, and they explain why many methods treat all four as one family.

## One family

The four tasks look different, but they rest on the same skill: **understanding how the series normally behaves**.

- **Forecasting** uses it to continue the series.
- **Imputation** uses it to fill the series in.
- **Anomaly detection** uses it to measure how far the data are from normal.
- **Classification** uses it to tell kinds of behavior apart.

That's why the survey and benchmark we read evaluates its models across all four tasks ([wang2026deep](../../../literature/wang2026deep.md)), and why [windows](../data-preparation/windows.md) can describe one common way of preparing the data, with small differences per task.

## Key points

- **Forecasting:** past → future values. **Imputation:** a series with gaps → the missing values.
- **Anomaly detection:** series → normal or abnormal, step by step. **Classification:** whole series → one label.
- All four rest on modeling **normal behavior**; this project works on forecasting and anomaly detection.

## Sources

- [wang2026deep](../../../literature/wang2026deep.md): the four tasks, and the benchmark across them.
