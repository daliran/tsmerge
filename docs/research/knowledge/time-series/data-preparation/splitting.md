# Splitting

**In one sentence:** a series is split by time into a training part and later evaluation parts, and nothing from the later parts may reach training: not a window, not a statistic.

- **Builds on:** [Time series](../time-series.md), [Windows](windows.md).
- **Used by:** [Normalization](normalization.md), [Forecasting](../tasks/forecasting.md), [Anomaly detection](../tasks/anomaly-detection.md).

## The rule not to break

A model is trained on one part of the data and evaluated on another it has never seen. With time series, the evaluation part must come **after** the training part, and the windows must respect that boundary.

![Wrong: windows that cross the train/test boundary. Right: split by time first, then cut windows inside each part](assets/split-leakage.png)

- **Split by time first, then cut windows inside each part.** A window that crosses the boundary contains test data. If it's used for training, the model has seen part of the test.
- **Never split windows at random.** With overlapping windows, almost every test window would have a near-identical twin in training: the model would look excellent and be useless on new data.
- **Compute anything learned from the data on the training part only,** e.g. the mean and spread used to scale the values ([normalization](normalization.md)). Using the whole series leaks information about the test period.

These mistakes, called **leakage**, don't cause errors. They silently make results look better than they are, which is why they're worth knowing before any experiment.

## Key points

- **Split by time first, then cut windows** inside each part.
- **Never split windows at random:** overlapping windows would put near-copies of test windows in training.
- **Learn scaling statistics on the training part only.**
- These mistakes (**leakage**) cause no errors; they silently inflate results.

## Sources

- The splitting rules are general practice, explained here in our own words; the figure illustrates them on synthetic data.
