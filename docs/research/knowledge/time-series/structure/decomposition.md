# Decomposition

**In one sentence:** decomposition takes a series apart into its trend-cycle, its seasonalities (one or more) and what's left, either by adding the parts or by multiplying them.

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

### Several seasonalities

The formulas above have one seasonal part, but many series have more ([patterns](patterns.md#seasonality)). "Higher frequency time series often exhibit more complicated seasonal patterns. For example, daily data may have a weekly pattern as well as an annual pattern. Hourly data usually has three types of seasonality: a daily pattern, a weekly pattern, and an annual pattern" ([FPP3, 12.1][fpp-complex]).

A decomposition then has **one seasonal part per period**. In the additive case, for an hourly series with daily and weekly seasonality:

$$y_t = S^{\text{day}}_t + S^{\text{week}}_t + T_t + R_t$$

STL handles this directly: it "is designed to deal with multiple seasonality. It will return multiple seasonal components, as well as a trend and remainder component" ([FPP3, 12.1][fpp-complex]).

Decomposition is useful in itself, to see what drives a series.

It can also help the [tasks](../tasks/tasks.md), with a caveat on unusual values:

- a **robust** method such as STL can be set so that "occasional unusual observations will not affect the estimates of the trend-cycle and seasonal components. They will, however, affect the remainder component" ([FPP3, 3.6][fpp-stl]): unusual values tend to show up in the remainder;
- the simpler classical decomposition "is not robust to these kinds of unusual values" ([FPP3, 3.4][fpp-classical]): they can leak into the trend-cycle and seasonal estimates.

## Trend or cycle? It depends on the smoothing

The trend-cycle isn't found by estimating a trend and a cycle separately and adding them. It is estimated directly, by **smoothing** the series, for example with a moving average:

- "The order of the moving average determines the smoothness of the trend-cycle estimate. In general, a larger order means a smoother curve" ([FPP3, 3.3][fpp-ma]).
- The result "captures the main movement of the time series without all of the minor fluctuations" ([FPP3, 3.3][fpp-ma]).

So the trend-cycle is **whatever slow movement survives the smoothing**, and the size of the smoothing window decides where the line falls:

- a **small window** lets the trend-cycle follow faster ups and downs, at the risk of also following noise;
- a **large window** keeps only the slowest movement; faster ups and downs are smoothed away.

STL, a common decomposition method, exposes this choice directly: its trend window controls "how rapidly the trend-cycle and seasonal components can change. Smaller values allow for more rapid changes" ([FPP3, 3.6][fpp-stl]).

![One series, its trend-cycle estimated with a small and a large moving average: the small window follows the cycle and leaves only noise in the remainder; the large window keeps only the trend and leaves the cycle in the remainder](assets/smoothing-window.png)

- **Small window** (a 2x24 moving average, which also cancels the daily seasonality): the estimated trend-cycle follows the true trend and cycle, and the remainder is only noise.
- **Large window** (2x168, one week): the trend-cycle keeps only the slow rise; the cycle is smoothed away and ends up in the **remainder**, with the noise.
- The large window's curve is shorter: a moving average can't be computed within half a window of either end of the series.

### A fast cycle ends up in the remainder

A cycle faster than the smoothing window isn't captured by the trend-cycle. It can't be seasonality either, because it has no fixed period. So it lands in the remainder.

Fast irregular swings are rarely called cycles anyway: "the average length of cycles is longer than the length of a seasonal pattern" ([FPP3, 2.3][fpp-patterns]).

### Trend or cycle also depends on how much you see

The same movement can look like a trend over a short stretch and like part of a cycle over a long one: "if we had a much longer series, we would see that this downward trend is actually part of a long cycle, but when viewed over only 100 days it appears to be a trend" ([FPP3, 2.3][fpp-patterns]).

### One cycle or several?

A series can have irregular ups and downs at several scales at once, for example a long cycle and shorter swings. A decomposition doesn't name them one by one: it has a single trend-cycle, and the smoothing window decides which of them it keeps and which go to the remainder.

## Key points

- **Decomposition** takes a series apart: **additive** when swings stay the same size, **multiplicative** when they grow with the level.
- A series with **several seasonalities** (e.g. daily and weekly) gets **one seasonal part per period**.
- With a robust decomposition, unusual values tend to show up in the remainder; classical decomposition isn't robust to them.
- The **trend-cycle** is estimated by **smoothing**: whatever slow movement survives it. A larger window keeps only slower movements; faster cycles end up in the remainder.

## Sources

- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 3.2, Time series components][fpp-components]: decomposition, additive and multiplicative, trend-cycle, remainder, the log transform. Read on 2026-11-09.
- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 3.4, Classical decomposition][fpp-classical]: not robust to unusual values. Read on 2026-11-09.
- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 3.6, STL decomposition][fpp-stl]: robust decomposition, unusual values in the remainder, the trend window. Read on 2026-11-09.
- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 3.3, Moving averages][fpp-ma]: estimating the trend-cycle by smoothing, window size and smoothness. Read on 2026-11-09.
- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 2.3, Time series patterns][fpp-patterns]: the length of cycles; trend or cycle depending on how much is seen. Read on 2026-11-09.
- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 12.1, Complex seasonality][fpp-complex]: several seasonal patterns, STL with several seasonal components. Read on 2026-11-09.

[fpp-components]: https://otexts.com/fpp3/decomposition.html#sec-components
[fpp-complex]: https://otexts.com/fpp3/advanced.html#sec-complexseasonality
[fpp-ma]: https://otexts.com/fpp3/decomposition.html#sec-moving-averages
[fpp-patterns]: https://otexts.com/fpp3/graphics.html#sec-tspatterns
[fpp-classical]: https://otexts.com/fpp3/decomposition.html#sec-classical-decomposition
[fpp-stl]: https://otexts.com/fpp3/decomposition.html#sec-stl
