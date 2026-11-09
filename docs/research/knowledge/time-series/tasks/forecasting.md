# Forecasting

**In one sentence:** forecasting predicts the next values of a series from its past.

- **Builds on:** [Stationarity](../structure/stationarity.md), [Tasks](tasks.md), [Regression errors](../../evaluation/regression-errors.md).
- **Used by:**
  - [Windows](../data-preparation/windows.md)
  - [Splitting](../data-preparation/splitting.md)
  - [Forecast evaluation](../evaluation/forecast-evaluation.md)
  - [Drift in time series](../change-over-time/drift-in-time-series.md)
  - [Forecasting models](../models/forecasting-models.md)

## The task

**Purpose:** forecasting "aims to predict future values or trends of the input series", by learning how the past relates to the future ([wang2026deep](../../../literature/wang2026deep.md), pp. 2–3).

**Examples:** weather forecasting; planning energy production or traffic ([wang2026deep](../../../literature/wang2026deep.md)); ordering stock for next week's sales.

**Input and output:**

- **given:** the last $L$ steps (the **context** or look-back);
- **produce:** the next $H$ steps (the **horizon**).

**Short and long term:** forecasts are commonly split into short-term and long-term, a separation that "depends on the forecasting horizon" ([wang2026deep](../../../literature/wang2026deep.md), p. 11).

The further ahead, the harder: "The further ahead we forecast, the more uncertainty is associated with the forecast", so prediction intervals usually widen as the horizon grows ([FPP3, 5.5][fpp-intervals]).

**How it's judged:** by the **forecast error**, "the difference between an observed value and its forecast" ([FPP3, 5.8][fpp-accuracy]):

- measured on data the model has never seen
- and summarized by measures such as MAE and MSE ([regression errors](../../evaluation/regression-errors.md)).

In the TSLib benchmark ([wang2026deep](../../../literature/wang2026deep.md)):

- long-term forecasting is judged by MSE and MAE (p. 11);
- short-term forecasting by SMAPE and MASE (p. 11), and its results figure reports the average OWA (Figure 9, p. 12).

**What makes it hard:** the future may not behave like the past.
When the series' behavior changes over time (drift), patterns learned from the past can stop holding ([stationarity](../structure/stationarity.md)).

## Key points

- **Given** the last $L$ steps (the context), **produce** the next $H$ (the horizon).
- Judged by forecast errors on data the model has never seen; the measures depend on the setting (in the TSLib benchmark, MSE and MAE for long-term, SMAPE and MASE for short-term).
- Hard because the future may not behave like the past: when the series' behavior changes, patterns learned from the past can stop holding.

## Sources

- [wang2026deep](../../../literature/wang2026deep.md): definition, examples, short and long term, benchmark metrics.
- Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*, 3rd ed.:
  - [Section 5.5, Distributional forecasts and prediction intervals][fpp-intervals]: uncertainty grows with the horizon. Read on 2026-11-09.
  - [Section 5.8, Evaluating point forecast accuracy][fpp-accuracy]: the forecast error. Read on 2026-11-09.

[fpp-intervals]: https://otexts.com/fpp3/toolbox.html#sec-prediction-intervals
[fpp-accuracy]: https://otexts.com/fpp3/toolbox.html#sec-accuracy
