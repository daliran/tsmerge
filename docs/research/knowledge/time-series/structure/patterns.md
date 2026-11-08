# Patterns

**In one sentence:** most time series are a mix of a few simple patterns (a long-term direction, regular repetitions, slower irregular waves, and noise), and recognizing them is the first step to understanding, predicting or checking a series.

- **Builds on:** [Time series](../time-series.md).
- **Used by:** [Decomposition](decomposition.md), [Stationarity](stationarity.md), [Autocorrelation](autocorrelation.md), [Windows](../data-preparation/windows.md).

## The building blocks

Look at almost any real series (electricity use, temperature, sales) and you'll see the same few ingredients. The reference textbook on forecasting defines three patterns ([FPP3, 2.3][fpp-patterns]):

| Pattern | Definition | Example |
|---|---|---|
| **Trend** | "a long-term increase or decrease in the data" | a city's electricity use growing year after year |
| **Seasonality** | a pattern caused by "seasonal factors", "always of a fixed and known period" | higher electricity use every evening; lower every weekend |
| **Cycle** | "rises and falls that are not of a fixed frequency" | economic booms and recessions |

What's left after these is the **remainder** (also called noise or residual): "anything else in the time series" ([FPP3, 3.2][fpp-components]).

![A series built from a rising trend, a 24-step seasonal pattern and random noise, shown together and separately](assets/decomposition.png)

The top panel is what you'd actually record. The three panels below are the pieces it's made of.

## Seasonality

Seasonality means **repetition at a fixed, known period**. The word comes from the seasons of the year, but the period can be anything tied to a calendar or a clock:

- **daily:** busier during the day, quiet at night;
- **weekly:** different on weekends than on weekdays;
- **yearly:** heating in winter, cooling in summer.

The **period** is the number of steps before the pattern repeats: in an hourly series, a daily cycle has a period of 24 and a weekly one 168.

**A series can have more than one seasonality** at once: "one series can have more than one seasonal pattern" ([FPP3, 2.3][fpp-patterns]).

![An hourly series with a daily cycle and lower values every weekend](assets/multiple-seasonality.png)

**Why it matters:** seasonality is the most predictable part of many series.

It also sets a minimum for how much history a model must see: to recognize a weekly pattern, it needs to look at least a week back (see [windows](../data-preparation/windows.md)).

## Seasonality vs cycles

The two are easy to confuse, because both go up and down. The difference is **regularity**:

- "if the frequency is unchanging and associated with some aspect of the calendar, then the pattern is seasonal";
- "if the fluctuations are not of a fixed frequency then they are cyclic" ([FPP3, 2.3][fpp-patterns]).

![A seasonal wave repeating every 50 steps, and a cyclic one whose ups and downs last 70, 110, 60, 95 steps](assets/seasonal-cyclic.png)

Cycles are usually slower: in economic data their duration "is usually at least 2 years", and "the average length of cycles is longer than the length of a seasonal pattern" ([FPP3, 2.3][fpp-patterns]).

Because their length varies, cycles are much harder to predict than seasonality. That's why the trend and the cycle are often merged into one **trend-cycle** component ([FPP3, 3.2][fpp-components]).

## Key points

- Most series combine a **trend**, one or more **seasonalities**, **cycles** and a **remainder** (noise).
- **Seasonality** repeats at a fixed, known period; **cycles** rise and fall irregularly and are usually slower.
- A window must be at least as long as the slowest seasonality a model should learn.

## Sources

- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 2.3, Time series patterns][fpp-patterns]: trend, seasonality, cycles. Read on 2026-11-08.
- Hyndman, R. J., & Athanasopoulos, G., *Forecasting: Principles and Practice*, 3rd edition, OTexts, [Section 3.2, Time series components][fpp-components]: the remainder, the trend-cycle. Read on 2026-11-08.

[fpp-patterns]: https://otexts.com/fpp3/tspatterns.html
[fpp-components]: https://otexts.com/fpp3/components.html
