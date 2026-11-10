# Assets of the data-preparation docs

The figures shown in the data-preparation docs of this folder, all drawn by [make_figures.py](make_figures.py) (how to run it: [the knowledge README](../../../README.md#figures)). They are synthetic and illustrative.

| Figure | What it shows | Shown in |
|---|---|---|
| sliding-windows.png | A series cut into windows, with window size and stride | [windows.md](../windows.md) |
| stride-overlap.png | One window size, three strides, three amounts of overlap | [windows.md](../windows.md) |
| window-count.png | Number of windows as a function of the stride | [windows.md](../windows.md) |
| forecast-window.png | A forecasting window: context and horizon | [windows.md](../windows.md) |
| split-leakage.png | Windows across the train/test boundary vs windows cut after splitting | [splitting.md](../splitting.md) |
| per-channel-scaling.png | Four channels of a small plant (temperature, power load, a valve, a constant setpoint), raw and scaled per channel | [normalization.md](../normalization.md) |
| constant-channel.png | A channel constant in training that rises slightly at test time, raw and after two kinds of scaling | [normalization.md](../normalization.md) |
| global-vs-window.png | A level shift and a spike next to a normal window: raw, scaled once with training statistics, and scaled per window | [normalization.md](../normalization.md) |
| eval-one-split.png | One split: train on the past, test once on what follows | [splitting.md](../splitting.md) |
| eval-rolling-origin.png | Rolling origin: five splits moving forward, scored by the average test error | [splitting.md](../splitting.md) |
| eval-prequential.png | Prequential evaluation: each piece first predicted, then learned from | [splitting.md](../splitting.md) |
| eval-every-period.png | Testing on every period after each training step: remembered, latest learned, not seen yet | [splitting.md](../splitting.md) |
| eval-permutation.png | Controlled permutation: the real order and two reorderings that swap only neighbors | [splitting.md](../splitting.md) |
| eval-question.png | The same model asked two questions: predict what comes next, or still work on every period learned | [splitting.md](../splitting.md) |
