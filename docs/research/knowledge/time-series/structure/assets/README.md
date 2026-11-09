# Assets of the structure docs

The figures shown in the structure docs of this folder, all drawn by [make_figures.py](make_figures.py) (how to run it: [the knowledge README](../../../README.md#figures)). They are synthetic and illustrative.

| Figure | What it shows | Shown in |
|---|---|---|
| decomposition.png | A series built by adding trend-cycle + seasonality + remainder; the trend-cycle panel shows the trend alone (dashed) and with the cycle | [patterns.md](../patterns.md) |
| multiple-seasonality.png | Daily seasonality and lower weekends in one series | [patterns.md](../patterns.md) |
| seasonal-cyclic.png | Fixed-period seasonality vs irregular cycles | [patterns.md](../patterns.md) |
| smoothing-window.png | One series, its trend-cycle estimated with a small (2x24) and a large (2x168) moving average, and the two remainders: the large window leaves the cycle in the remainder | [decomposition.md](../decomposition.md) |
| additive-multiplicative.png | Seasonal swings of constant size vs swings growing with the level | [decomposition.md](../decomposition.md) |
| to-stationary.png | Three non-stationary series and the same series after differencing, seasonal differencing, and a logarithm followed by seasonal differencing | [stationarity.md](../stationarity.md) |
| stationarity.png | White noise vs a trended series vs a random walk | [stationarity.md](../stationarity.md) |
| autocorrelation.png | Autocorrelation of a series with daily seasonality, peaking at lags 24, 48, 72 | [autocorrelation.md](../autocorrelation.md) |
