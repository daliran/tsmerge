# Stationarity

**In one sentence:** a stationary series has statistical properties that don't depend on when it's observed; trends and seasonality break this.

- **Builds on:** [Patterns](patterns.md), [Decomposition](decomposition.md).
- **Used by:**
  - [Distribution shift](../../drift/distribution-shift.md)
  - [Autocorrelation](autocorrelation.md)
  - [Forecasting](../tasks/forecasting.md)
  - [Normalization](../data-preparation/normalization.md)
  - [Drift in time series](../drift/drift-in-time-series.md)

## Does the series keep its character?

"A stationary time series is one whose statistical properties do not depend on the time at which the series is observed" ([FPP3, 9.1][fpp-stationarity]).

In plain words: any stretch of the series looks statistically like any other stretch, with the same average level and the same amount of variation.

- **Not stationary:** "time series with trends, or with seasonality, are not stationary" ([FPP3, 9.1][fpp-stationarity]): the trend moves the average, and the seasonality makes the expected value depend on the hour or the day.
- **Stationary:** "a white noise series is stationary" ([FPP3, 9.1][fpp-stationarity]).
- **Perhaps surprisingly,** a series with cycles but no trend or seasonality is stationary ([FPP3, 9.1][fpp-stationarity]). This is "because the cycles are not of a fixed length, so before we observe the series we cannot be sure where the peaks and troughs of the cycles will be" ([FPP3, 9.1][fpp-stationarity]).

![White noise has the same mean and spread everywhere; a trended series and a random walk don't](assets/stationarity.png)

The random walk in the figure is built by adding a random step to the previous value: $y_t = y_{t-1} + \varepsilon_t$, with $\varepsilon_t$ white noise ([FPP3, 9.1][fpp-stationarity]).
It wanders with no fixed level, so it isn't stationary; its differences $y_t - y_{t-1}$ are the white-noise steps, which are.

**Stationary is not the same as predictable:**

- "In general, a stationary time series will have no predictable patterns in the long-term" ([FPP3, 9.1][fpp-stationarity]); white noise is stationary and can't be predicted at all.
- A seasonal series is not stationary, yet its seasonality repeats at a fixed, known period, which makes it easy to predict ([patterns](patterns.md)).

**Why it matters:** a model learns from the past and is used on the future.

- Models that assume the statistical properties stay the same rely on what they learned staying valid.
- When those properties change, what was learned may stop being valid.

An unexpected change in the statistical properties over time is called **drift** ([drift in time series](../drift/drift-in-time-series.md), [distribution shift](../../drift/distribution-shift.md)).
Drift is narrower than non-stationarity: a known trend or seasonality makes a series non-stationary, but it's a regular pattern, not drift.

A common way to make a series more stationary is **differencing**: instead of the values, look at the changes between consecutive values. This can help stabilize the mean of a series by removing changes in its level ([FPP3, 9.1][fpp-stationarity]).
The random walk is the simplest case: one round of differencing turns it into white noise.

## Key points

- A **stationary** series has statistical properties that don't depend on time; trends and seasonality break this.
- Stationary doesn't mean predictable: white noise is stationary and unpredictable, while seasonality is non-stationary but regular.
- **Drift** is an unexpected change in the statistical properties over time, which can make what a model learned stop being valid; a known trend or seasonality is not drift.
- **Differencing** (looking at changes between consecutive values) can make a series more stationary: a random walk becomes white noise.

## Sources

- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 9.1, Stationarity and differencing][fpp-stationarity]: stationarity, differencing, the random walk. Read on 2026-11-09.

[fpp-stationarity]: https://otexts.com/fpp3/arima.html#sec-stationarity
