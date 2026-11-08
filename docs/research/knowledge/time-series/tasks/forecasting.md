# Forecasting

**In one sentence:** forecasting predicts the next values of a series from its past.

- **Builds on:** [Tasks](tasks.md), [Stationarity](../structure/stationarity.md).
- **Used by:** [Windows](../data-preparation/windows.md), [Regression errors](../../evaluation/regression-errors.md), [Forecast evaluation](../evaluation/forecast-evaluation.md).

## The task

**Purpose:** forecasting "aims to predict future values or trends of the input series", by learning how the past relates to the future ([wang2026deep](../../../literature/wang2026deep.md), pp. 2–3).

**Examples:** weather forecasting; planning energy production or traffic ([wang2026deep](../../../literature/wang2026deep.md)); ordering stock for next week's sales.

**Input and output:**

- **given:** the last $L$ steps (the **context** or look-back);
- **produce:** the next $H$ steps (the **horizon**).

**Short and long term:** forecasts are commonly split into short-term and long-term, a separation that "depends on the forecasting horizon" ([wang2026deep](../../../literature/wang2026deep.md), p. 11). The further ahead, the harder: uncertainty accumulates with every step.

**How it's judged:** by the **forecast error**, the difference between an observed value and its forecast, measured on data the model has never seen and summarized by MAE and MSE ([regression errors](../../evaluation/regression-errors.md)). MSE and MAE are the standard measures for long-term forecasting benchmarks ([wang2026deep](../../../literature/wang2026deep.md), p. 11).

**What makes it hard:** the future may not behave like the past ([stationarity](../structure/stationarity.md): when the series isn't stationary, past patterns stop being a reliable guide).

## Key points

- **Given** the last $L$ steps (the context), **produce** the next $H$ (the horizon).
- Judged by errors such as MAE and MSE, on data the model has never seen.
- Hard when the series isn't stationary: past patterns stop being a reliable guide.

## Sources

- [wang2026deep](../../../literature/wang2026deep.md): definition, examples, short and long term, benchmark metrics.
