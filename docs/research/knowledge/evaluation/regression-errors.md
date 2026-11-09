# Regression errors

**In one sentence:** when a model predicts numbers, its errors are summarized by their average size: the mean absolute error, the mean squared error and its square root.

- **Builds on:** nothing: a starting point.
- **Used by:**
  - [Forecasting](../time-series/tasks/forecasting.md)
  - [Imputation](../time-series/tasks/imputation.md)
  - [Comparing results](comparing-results.md)
  - [Forecast evaluation](../time-series/evaluation/forecast-evaluation.md)

## Errors and their averages

A **forecast error** is "the difference between an observed value and its forecast" ([FPP3, 5.8][fpp-accuracy]), written $e_t$. The same holds for any predicted number, e.g. an imputed value.

Accuracy "can only be determined by considering how well a model performs on new data" ([FPP3, 5.8][fpp-accuracy]).

The errors are summarized by:

| Measure | Formula | Note |
|---|---|---|
| **MAE** (mean absolute error) | average of $\lvert e_t \rvert$ | in the units of the data |
| **MSE** (mean squared error) | average of $e_t^2$ | in squared units; punishes large errors more than small ones |
| **RMSE** (root mean squared error) | $\sqrt{\text{MSE}}$ | back in the units of the data; still punishes large errors more |

FPP3 defines MAE and RMSE ([FPP3, 5.8][fpp-accuracy]); MSE is RMSE before the square root, and its units are the square of the data's ([Mean squared error][mse]).

## Scale dependence

All three are **scale-dependent**: they are computed from the errors alone, which are on the scale of the data.

FPP3 says this of measures based only on $e_t$, naming MAE and RMSE: they "cannot be used to make comparisons between series that involve different units" ([FPP3, 5.8][fpp-accuracy]).
The same holds for MSE, which is built from the same errors.

So errors are comparable across series only when they are on a common scale.
One way to get a common scale is to compute the errors on normalized data ([normalization](../time-series/data-preparation/normalization.md)).
The numbers then depend on the scaling used, and are comparable only with results that use the same one.

## Key points

- **MAE** averages $\lvert e_t \rvert$, in the units of the data; **MSE** averages $e_t^2$, in squared units, and punishes large errors more; **RMSE** is its square root, back in the data's units.
- All three are **scale-dependent**: compare only results in the same units and the same scaling.
- Measure them on data the model has never seen.

## Sources

- Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*, 3rd ed., [Section 5.8, Evaluating point forecast accuracy][fpp-accuracy]: forecast errors, MAE, RMSE, scale dependence. Read on 2026-11-09.
- [Mean squared error (Wikipedia)][mse]: the units of MSE and RMSE. Read on 2026-11-09.

[fpp-accuracy]: https://otexts.com/fpp3/toolbox.html#sec-accuracy
[mse]: https://en.wikipedia.org/wiki/Mean_squared_error
