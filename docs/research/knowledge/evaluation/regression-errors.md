# Regression errors

**In one sentence:** when a model predicts numbers, its errors are summarized by their average size: the mean absolute error, the mean squared error and its square root.

- **Builds on:** nothing: a starting point.
- **Used by:** [Forecasting](../time-series/tasks/forecasting.md), [Imputation](../time-series/tasks/imputation.md), [Forecast evaluation](../time-series/evaluation/forecast-evaluation.md).

## Errors and their averages

A **forecast error** is "the difference between an observed value and its forecast" ([FPP3, 5.8][fpp-accuracy]), written $e_t$. The same holds for any predicted number, e.g. an imputed value. Accuracy "can only be determined by considering how well a model performs on new data" ([FPP3, 5.8][fpp-accuracy]). The errors are summarized by:

| Measure | Formula | Note |
|---|---|---|
| **MAE** (mean absolute error) | average of $\lvert e_t \rvert$ | in the units of the data |
| **MSE** (mean squared error) / **RMSE** (its square root) | average of $e_t^2$ | punishes large errors more than small ones |

## Scale dependence

Both are **scale-dependent**: they "cannot be used to make comparisons between series that involve different units" ([FPP3, 5.8][fpp-accuracy]). This is one reason series are usually rescaled before modeling ([normalization](../time-series/data-preparation/normalization.md)).

## Key points

- **MAE** averages $\lvert e_t \rvert$, in the units of the data; **MSE** averages $e_t^2$ and punishes large errors more; **RMSE** is its square root.
- Both are **scale-dependent**: compare them only within one series and one scaling.
- Measure them on data the model has never seen.

## Sources

- Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*, 3rd ed., [Section 5.8, Evaluating point forecast accuracy][fpp-accuracy]: forecast errors, MAE, RMSE, scale dependence. Read on 2026-11-08.

[fpp-accuracy]: https://otexts.com/fpp3/accuracy.html
