# Decomposition

**In one sentence:** decomposition takes a series apart into its trend-cycle, its seasonality and what's left, either by adding the parts or by multiplying them.

- **Builds on:** [Patterns](patterns.md).
- **Used by:** [Stationarity](stationarity.md).

## Taking a series apart

Splitting a series into its parts is called **decomposition**. There are two common ways to put the parts back together ([FPP3, 3.2][fpp-components]), with $y_t$ the series, $T_t$ the trend-cycle, $S_t$ the seasonality and $R_t$ the remainder:

| | Additive | Multiplicative |
|---|---|---|
| **Formula** | $y_t = S_t + T_t + R_t$ | $y_t = S_t \times T_t \times R_t$ |
| **Use it when** | the seasonal swings, and the variation around the trend-cycle, keep the same size whatever the level of the series | the seasonal swings, and the variation around the trend-cycle, grow in proportion to the level |

In the textbook's words ([FPP3, 3.2][fpp-components]):

- additive fits when "the magnitude of the seasonal fluctuations, or the variation around the trend-cycle, does not vary with the level of the time series";
- multiplicative fits when "the variation in the seasonal pattern, or the variation around the trend-cycle, appears to be proportional to the level of the time series";
- multiplicative decompositions "are common with economic time series".

Taking the logarithm turns a multiplicative series into an additive one, since $\log y_t = \log S_t + \log T_t + \log R_t$ ([FPP3, 3.2][fpp-components]).

![Additive: the seasonal swings keep the same size as the series rises. Multiplicative: they grow with it](assets/additive-multiplicative.png)

Decomposition is useful in itself, to see what drives a series.

It can also help the [tasks](../tasks/tasks.md), with a caveat on unusual values:

- a **robust** method such as STL can be set so that "occasional unusual observations will not affect the estimates of the trend-cycle and seasonal components. They will, however, affect the remainder component" ([FPP3, 3.6][fpp-stl]): unusual values tend to show up in the remainder;
- the simpler classical decomposition "is not robust to these kinds of unusual values" ([FPP3, 3.4][fpp-classical]): they can leak into the trend-cycle and seasonal estimates.

## Key points

- **Decomposition** takes a series apart: **additive** when swings stay the same size, **multiplicative** when they grow with the level.
- With a robust decomposition, unusual values tend to show up in the remainder; classical decomposition isn't robust to them.

## Sources

- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 3.2, Time series components][fpp-components]: decomposition, additive and multiplicative, trend-cycle, remainder, the log transform. Read on 2026-11-09.
- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 3.4, Classical decomposition][fpp-classical]: not robust to unusual values. Read on 2026-11-09.
- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 3.6, STL decomposition][fpp-stl]: robust decomposition, unusual values in the remainder. Read on 2026-11-09.

[fpp-components]: https://otexts.com/fpp3/decomposition.html#sec-components
[fpp-classical]: https://otexts.com/fpp3/decomposition.html#sec-classical-decomposition
[fpp-stl]: https://otexts.com/fpp3/decomposition.html#sec-stl
