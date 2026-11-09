# Glossary

One line per term, grouped by the area it belongs to, with a link to the doc that explains it and gives its sources. Terms whose doc isn't written yet carry their own source.

## Signals

- **Aliasing:** a component faster than half the sampling rate shows up in the samples disguised as a slower one ([sampling](signals/sampling.md#sampling-too-slowly-aliasing)).
- **Causal model:** a model whose output at a moment depends only on present and past inputs, never future ones ([signals](signals/signals.md#time-based-vs-not-time-based)).
- **DFT (discrete Fourier transform):** the Fourier transform of a finite list of samples ([Fourier transform](signals/fourier-transform.md#for-sampled-data-the-discrete-fourier-transform)).
- **Digital signal:** a signal both sampled (discrete time) and quantized (discrete values) ([sampling](signals/sampling.md)).
- **Domain (of a signal):** the set of values its independent variable can take: time, space, frequency, position ([signals](signals/signals.md)).
- **FFT (fast Fourier transform):** an algorithm computing the DFT in $O(n \log n)$ instead of $O(n^2)$ ([Fourier transform](signals/fourier-transform.md#the-fast-fourier-transform)).
- **Fourier transform:** rewriting a signal as a sum of sine waves, with an amplitude and a phase per frequency ([Fourier transform](signals/fourier-transform.md)).
- **Nyquist frequency:** half the sampling rate, $f_s/2$: the fastest frequency the samples can show ([sampling](signals/sampling.md#sampling-fast-enough)).
- **Nyquist rate:** $2B$ for a signal with no frequency above $B$; sampling must be faster than it ([sampling](signals/sampling.md#rebuilding-the-signal-from-its-samples)).
- **Quantization:** rounding each value to one of a limited set of levels ([sampling](signals/sampling.md)).
- **Sampling:** measuring a continuous signal at regular intervals, making time discrete ([sampling](signals/sampling.md)).
- **Sampling rate:** samples taken per second, $f_s = 1/T$ ([sampling](signals/sampling.md)).
- **Signal:** a function that conveys information about a phenomenon: "where or when" → "how much" ([signals](signals/signals.md)).
- **Spectrum:** how strong each frequency in a signal is ([Fourier transform](signals/fourier-transform.md)).

## Time series and their structure

- **Autocorrelation:** how strongly a series is linearly related to its own past, at each lag ([autocorrelation](time-series/structure/autocorrelation.md)).
- **Channel:** one of the values recorded at each step of a multivariate series; also called variable, variate or feature ([time series](time-series/time-series.md#univariate-and-multivariate)).
- **Classical decomposition:** the 1920s decomposition method: trend-cycle by moving average, seasonality by averaging each season; no longer recommended ([decomposition](time-series/structure/decomposition.md#classical-decomposition)).
- **Cycle:** rises and falls of no fixed length, unlike seasonality ([patterns](time-series/structure/patterns.md#seasonality-vs-cycles)).
- **Decomposition:** taking a series apart into trend-cycle, seasonality and remainder, additively or multiplicatively ([decomposition](time-series/structure/decomposition.md)).
- **Differencing:** looking at the changes between consecutive values instead of the values ([stationarity](time-series/structure/stationarity.md)).
- **Drift:** an unexpected change in a series' statistical properties over time ([stationarity](time-series/structure/stationarity.md)).
- **Feature:** in machine learning, an individual measurable property of the data; for a multivariate series, a channel ([time series](time-series/time-series.md#univariate-and-multivariate)).
- **Moving average (m-MA):** each value replaced by the average of itself and its $k$ neighbors on each side, $m = 2k + 1$ ([decomposition](time-series/structure/decomposition.md#moving-averages)).
- **Multivariate series:** a series with several channels sharing the same clock ([time series](time-series/time-series.md#univariate-and-multivariate)).
- **One-hot encoding:** turning symbols into numbers with one channel per symbol, set to 1 for the symbol present ([time series](time-series/time-series.md)).
- **Period:** the number of steps before a seasonal pattern repeats ([patterns](time-series/structure/patterns.md#seasonality)).
- **Random walk:** a series where each value is the previous one plus a random step, wandering with no fixed level ([stationarity](time-series/structure/stationarity.md)).
- **Remainder:** what is left of a series after removing trend-cycle and seasonality: noise and anything unusual ([patterns](time-series/structure/patterns.md)).
- **Seasonality:** repetition at a fixed, known period, tied to a calendar or a clock ([patterns](time-series/structure/patterns.md#seasonality)).
- **STL:** "Seasonal and Trend decomposition using Loess", a widely used method to decompose a series into trend-cycle, seasonal parts and remainder ([decomposition](time-series/structure/decomposition.md#stl-in-brief)).
- **Stationary series:** a series whose statistical properties don't depend on when it is observed ([stationarity](time-series/structure/stationarity.md)).
- **Time series:** a list of values in time order, usually equally spaced: a sampled, time-based signal ([time series](time-series/time-series.md)).
- **Trend:** "a long-term increase or decrease in the data" ([patterns](time-series/structure/patterns.md)).
- **Trend-cycle:** the trend and the cycle merged into one component, as decompositions usually do ([patterns](time-series/structure/patterns.md#how-they-fit-together)).
- **Univariate series:** a series with one value per step ([time series](time-series/time-series.md#univariate-and-multivariate)).
- **White noise:** a series with no autocorrelation: every autocorrelation close to zero ([autocorrelation](time-series/structure/autocorrelation.md)).

## Time-series tasks

- **Classification:** giving a whole series one label out of a fixed set ([classification](time-series/tasks/classification.md)).
- **Forecasting:** predicting the next values of a series from its past ([forecasting](time-series/tasks/forecasting.md)).
- **Imputation:** filling the gaps of a series with estimates of the missing values ([imputation](time-series/tasks/imputation.md)).

## Preparing the data

- **Context (look-back):** the part of a forecasting window the model is given, of length $L$ ([windows](time-series/data-preparation/windows.md)).
- **Horizon:** the part of a forecasting window the model must predict, of length $H$ ([windows](time-series/data-preparation/windows.md)).
- **Leakage:** information from the test period reaching training, silently making results look better ([splitting](time-series/data-preparation/splitting.md)).
- **Stride:** how many steps a window moves forward each time ([windows](time-series/data-preparation/windows.md)).
- **Window:** a short, fixed-length piece of a series, cut by sliding along it ([windows](time-series/data-preparation/windows.md)).

## Evaluation

- **Accuracy:** the share of all calls, positive and negative, that were right: $(tp+tn)/(tp+tn+fp+fn)$ ([precision, recall and F1](evaluation/precision-recall-f1.md#accuracy)).
- **F1:** the harmonic mean of precision and recall ([precision, recall and F1](evaluation/precision-recall-f1.md)).
- **Forecast error:** the difference between an observed value and its forecast ([regression errors](evaluation/regression-errors.md)).
- **MAE (mean absolute error):** the average absolute forecast error, in the units of the data ([regression errors](evaluation/regression-errors.md)).
- **MSE (mean squared error):** the average squared error, in squared units; it punishes large errors more ([regression errors](evaluation/regression-errors.md)).
- **Precision:** of the items called positive, the share that really are: $tp/(tp+fp)$ ([precision, recall and F1](evaluation/precision-recall-f1.md)).
- **Recall:** of the real positives, the share that were found: $tp/(tp+fn)$ ([precision, recall and F1](evaluation/precision-recall-f1.md)).
- **RMSE (root mean squared error):** the square root of MSE, back in the units of the data ([regression errors](evaluation/regression-errors.md)).
- **Threshold:** the value that turns a score into a yes-or-no call ([precision, recall and F1](evaluation/precision-recall-f1.md#the-threshold)).

## Anomaly detection

- **Anomaly detection:** finding the data that deviate from the majority; also called outlier or novelty detection ([anomaly detection](anomaly-detection/anomaly-detection.md)).
- **Anomaly score:** a number per item, higher for more anomalous items; a threshold turns it into a decision ([anomaly detection](anomaly-detection/anomaly-detection.md#how-it-works-in-general)).
- **Collective anomaly:** a group of items abnormal as a whole, though each looks normal alone ([kinds of anomalies](anomaly-detection/kinds-of-anomalies.md)).
- **Contextual anomaly:** an item normal in general, but not in its context, such as the time or the place ([kinds of anomalies](anomaly-detection/kinds-of-anomalies.md)).
- **Point anomaly:** a single item far from all the others ([kinds of anomalies](anomaly-detection/kinds-of-anomalies.md)).

## Learning

- **Foundation model:** a model "trained on vast datasets so that it can be applied across a wide range of use cases" ([Foundation model][foundation]; doc: [foundation models](learning/foundation-models.md)).
- **Joint training:** training one model on all the data at once; the reference that strategies learning in steps are compared with (e.g. joint multi-task training in [ilharco2023editing](../literature/ilharco2023editing.md), p. 25; doc: [joint training](learning/joint-training.md)).

## Continual learning and model merging

- **Backward transfer (BWT):** the average change in performance on earlier tasks after learning later ones; negative values mean forgetting ([lin2026unlocking](../literature/lin2026unlocking.md), p. 3; doc: [forward and backward transfer](learning/continual-learning/forward-and-backward-transfer.md)).
- **Catastrophic forgetting:** "the tendency of an artificial neural network to abruptly and drastically forget previously learned information upon learning new information" ([Catastrophic interference][forgetting]; doc: [forgetting](learning/continual-learning/forgetting.md)).
- **Task arithmetic:** editing a model by adding, negating or combining task vectors ([ilharco2023editing](../literature/ilharco2023editing.md), p. 2; doc: [task arithmetic](learning/continual-learning/model-merging/task-arithmetic.md)).
- **Task vector:** the difference between a model's weights after fine-tuning on a task and its pre-trained weights ([ilharco2023editing](../literature/ilharco2023editing.md), p. 2; doc: [task arithmetic](learning/continual-learning/model-merging/task-arithmetic.md)).

[forgetting]: https://en.wikipedia.org/wiki/Catastrophic_interference
[foundation]: https://en.wikipedia.org/wiki/Foundation_model
