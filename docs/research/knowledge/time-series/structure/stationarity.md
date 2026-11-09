# Stationarity

**In one sentence:** a stationary series has statistical properties that don't depend on when it's observed; trends and seasonality break this.

- **Builds on:** [Patterns](patterns.md), [Decomposition](decomposition.md).
- **Used by:**
  - [Distribution shift](../../drift/distribution-shift.md)
  - [Autocorrelation](autocorrelation.md)
  - [Forecasting](../tasks/forecasting.md)
  - [Normalization](../data-preparation/normalization.md)
  - [Drift in time series](../drift/drift-in-time-series.md)

## What stationarity is

"A stationary time series is one whose statistical properties do not depend on the time at which the series is observed" ([FPP3, 9.1][fpp-stationarity]).

In plain words: any stretch of the series looks statistically like any other stretch. Shift the series in time, and its average, its spread and the way its values relate to each other stay the same.

Formally, for a **strictly stationary** process, "the joint probability distribution of the process remains the same when shifted in time" ([Stationary process][wiki]). In practice a weaker version is used, **weak** (or wide-sense) **stationarity**, which only requires that the "1st moment (i.e. the mean) and autocovariance do not vary with respect to time and that the 2nd moment is finite for all times" ([Stationary process][wiki]).

## Stationary vs non-stationary

| Property | Stationary | Non-stationary |
|---|---|---|
| **Average level** | the same everywhere | changes: drifts, rises or falls |
| **Spread** (variance) | the same everywhere | changes: e.g. swings grow with the level |
| **Relation between values** (autocorrelation) | depends only on the distance between them, not on when | depends on when |
| **Time plot** | roughly horizontal (some cyclic movement is possible), with constant variance ([FPP3, 9.1][fpp-stationarity]) | trending, seasonal, or wandering |

![White noise has the same mean and spread everywhere; a trended series and a random walk don't](assets/stationarity.png)

**Stationary:**

- **White noise:** "a white noise series is stationary" ([FPP3, 9.1][fpp-stationarity]).
- **Perhaps surprisingly, a series with cycles but no trend or seasonality.** This is "because the cycles are not of a fixed length, so before we observe the series we cannot be sure where the peaks and troughs of the cycles will be" ([FPP3, 9.1][fpp-stationarity]).

**Not stationary:**

- **Trend or seasonality:** "time series with trends, or with seasonality, are not stationary" ([FPP3, 9.1][fpp-stationarity]). The trend moves the average; the seasonality makes the expected value depend on the hour or the day.
- **Changing variance:** swings that grow or shrink over time.
- **A random walk:** each value is the previous one plus a random step, $y_t = y_{t-1} + \varepsilon_t$ with $\varepsilon_t$ white noise ([FPP3, 9.1][fpp-stationarity]). It wanders with no fixed level.

Most real series are not stationary: anything with a trend or a seasonality isn't.

## How to tell

- **Look at the time plot:** a stationary series stays roughly horizontal, with the same spread throughout.
- **Look at the autocorrelation:** "for a stationary time series, the ACF (autocorrelation function) will drop to zero relatively quickly, while the ACF of non-stationary data decreases slowly" ([FPP3, 9.1][fpp-stationarity]; [autocorrelation](autocorrelation.md)).
- **Use a test:** a unit root test decides "more objectively whether differencing is required" ([FPP3, 9.1][fpp-stationarity]). In the KPSS (Kwiatkowski–Phillips–Schmidt–Shin) test, for example, "the null hypothesis is that the data are stationary, and we look for evidence that the null hypothesis is false" ([FPP3, 9.1][fpp-stationarity]). Different tests rest on different assumptions "and may lead to conflicting answers" ([FPP3, 9.1][fpp-stationarity]).

## How to make a series stationary

Most non-stationary series can be made (close to) stationary by transforming them ([FPP3, 9.1][fpp-stationarity]):

- **Differencing:** look at the changes between consecutive values instead of the values. It can help stabilize the mean by removing changes in the level, and so eliminate or reduce trend and seasonality. A random walk becomes white noise after one round.
- **Seasonal differencing:** "the difference between an observation and the previous observation from the same season", for example this Monday minus last Monday. It removes the seasonality.
- **A logarithm:** it can help stabilize the variance, when swings grow with the level.
- **Second-order differencing:** occasionally the differenced series still isn't stationary, and it's differenced a second time.

![Three non-stationary series (a trend; a trend with daily seasonality; swings growing with the level) and the same series after differencing, seasonal differencing, and a logarithm followed by seasonal differencing: all three end up flat, with an even spread](assets/to-stationary.png)

- **A trend:** differencing removes the changing level; what's left moves around a constant mean.
- **A trend and a daily seasonality:** subtracting the value 24 steps earlier removes both the seasonality and the trend.
- **Swings growing with the level:** the logarithm makes the swings the same size; seasonal differencing then removes the rest.

The series are synthetic; the transformed ones are flat with an even spread, which is how a stationary series looks in a plot.

Decomposition gets close too: once the trend-cycle and the seasonality are removed, the remainder is much closer to stationary ([decomposition](decomposition.md)).

## Why do it

- **Many models need it.** ARIMA (autoregressive integrated moving average) models "aim to describe the autocorrelations in the data" ([FPP3, chapter 9][fpp-arima]). Those relations can only be learned if they stay the same over time, so the series is transformed first, modeled, and the forecasts transformed back.
- **The past becomes a reliable summary.** A mean, a spread or an autocorrelation estimated on past data describes the future only if it doesn't depend on time, which is what stationarity guarantees.
- **Deep models do the same with normalization.** In deep learning, data normalization "takes the role of stationarization", and "helps mitigate the distribution shift between the source and target domains" ([wang2026deep](../../../literature/wang2026deep.md), p. 3): each input is rescaled to a common mean and spread ([normalization](../data-preparation/normalization.md)).

## Stationary is not predictable

- "In general, a stationary time series will have no predictable patterns in the long-term" ([FPP3, 9.1][fpp-stationarity]); white noise is stationary and can't be predicted at all.
- A seasonal series is not stationary, yet its seasonality repeats at a fixed, known period, which makes it easy to predict ([patterns](patterns.md)).

So stationarity isn't the goal in itself: it's the form in which a series' regular structure can be estimated reliably.

## Stationarity and drift

When the statistical properties change in ways nobody anticipated, what a model learned may stop being valid.

An unexpected change in the statistical properties over time is called **drift** ([drift in time series](../drift/drift-in-time-series.md), [distribution shift](../../drift/distribution-shift.md)).
Drift is narrower than non-stationarity: a known trend or seasonality makes a series non-stationary, but it's a regular pattern, not drift.

## Key points

- A **stationary** series has statistical properties (average, spread, how values relate) that don't depend on when it's observed; in practice, **weak stationarity**: constant mean and autocovariance.
- **Not stationary:** trends, seasonality, changing variance, random walks; most real series.
- **How to tell:** a roughly horizontal time plot with constant spread, an autocorrelation that drops to zero quickly, or a unit root test such as KPSS.
- **How to make it stationary:** differencing and seasonal differencing remove trend and seasonality; a logarithm stabilizes the variance.
- **Why:** many models (e.g. ARIMA) need it, and it makes statistics from the past valid for the future; deep models do the same with normalization.
- Stationary doesn't mean predictable; **drift** is an unexpected change, narrower than non-stationarity.

## Sources

- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 9.1, Stationarity and differencing][fpp-stationarity]: definition, examples, time plots, the ACF of stationary series, unit root tests and KPSS, differencing, seasonal and second-order differencing, logarithms, the random walk. Read on 2026-11-09.
- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Chapter 9, ARIMA models][fpp-arima]: ARIMA models describe autocorrelations. Read on 2026-11-09.
- [Stationary process (Wikipedia)][wiki]: strict and weak stationarity. Read on 2026-11-09.
- [wang2026deep](../../../literature/wang2026deep.md): normalization as stationarization in deep models.

[fpp-stationarity]: https://otexts.com/fpp3/arima.html#sec-stationarity
[fpp-arima]: https://otexts.com/fpp3/arima.html#sec-arima
[wiki]: https://en.wikipedia.org/wiki/Stationary_process
