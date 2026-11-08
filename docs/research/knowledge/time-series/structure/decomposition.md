# Decomposition

**In one sentence:** decomposition takes a series apart into its trend-cycle, its seasonality and what's left, either by adding the parts or by multiplying them.

- **Builds on:** [Patterns](patterns.md).
- **Used by:** [Stationarity](stationarity.md).

## Taking a series apart

Splitting a series into its parts is called **decomposition**. There are two common ways to put the parts back together ([FPP3, 3.2][fpp-components]), with $y_t$ the series, $T_t$ the trend-cycle, $S_t$ the seasonality and $R_t$ the remainder:

| | Additive | Multiplicative |
|---|---|---|
| **Formula** | $y_t = S_t + T_t + R_t$ | $y_t = S_t \times T_t \times R_t$ |
| **Use it when** | the seasonal swings "do not vary with the level" of the series | the swings are "proportional to the level" |
| **Typical of** | physical quantities with a stable range | economic series: "multiplicative decompositions are common with economic time series" |

![Additive: the seasonal swings keep the same size as the series rises. Multiplicative: they grow with it](assets/additive-multiplicative.png)

Decomposition is useful in itself, to see what drives a series. It also helps the [tasks](../tasks/tasks.md): what remains after removing trend and seasonality is where unexpected behavior shows most clearly.

## Key points

- **Decomposition** takes a series apart: **additive** when swings stay the same size, **multiplicative** when they grow with the level.
- What remains after removing trend and seasonality is where unexpected behavior shows most clearly.

## Sources

- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 3.2, Time series components][fpp-components]: decomposition, additive and multiplicative, trend-cycle, remainder. Read on 2026-11-08.

[fpp-components]: https://otexts.com/fpp3/components.html
