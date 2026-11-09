# Splitting

**In one sentence:** a series is split by time into a training part and later evaluation parts, and nothing from the later parts may reach training: not a window, not a statistic.

- **Builds on:**
  - [Time series in time series](../time-series.md)
  - [Forecasting](../tasks/forecasting.md)
  - [Anomaly detection in time series](../tasks/anomaly-detection.md)
  - [Windows](windows.md)
- **Used by:** [Normalization](normalization.md).

## The rule not to break

A model is trained on one part of the data and evaluated on another it has never seen. With time series, the evaluation part must come **after** the training part, and the training windows must respect that boundary.

![Wrong: windows that cross the train/test boundary, mixing training and test steps. Right: split by time first, then cut windows inside each part](assets/split-leakage.png)

- **No training window may contain test-period steps.** A window that crosses the boundary contains test data; if it's used for training, the model has seen part of the test.
  - The simplest way to guarantee it: split by time first, then cut windows inside each part, as in the figure.
  - The rule binds training only. A test window may reach back into earlier steps as context, since past values are available when the model is used.
- **Never split windows at random.** With overlapping windows, almost every test window would have a near-identical twin in training: the model would look excellent and be useless on new data.
- **Compute anything learned from the data on the training part only,** e.g. the mean and spread used to scale the values ([normalization](normalization.md)). Using the whole series leaks information about the test period.

These mistakes, called **leakage**, raise no warning and don't crash anything. They silently make results look better than they are, which is why they're worth knowing before any experiment.

## Key points

- **No training window may contain test-period steps:** split by time first, then cut windows; test windows may still use earlier steps as context.
- **Never split windows at random:** overlapping windows would put near-copies of test windows in training.
- **Learn scaling statistics on the training part only.**
- These mistakes (**leakage**) raise no warning or crash; they silently inflate results.

## Sources

- The splitting rules are general practice; the figure illustrates them on synthetic data.
