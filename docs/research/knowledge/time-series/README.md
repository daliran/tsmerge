# Time series

Everything specific to time series: what a series is, its structure, the tasks, how data are prepared, and the time-series side of evaluation, drift and models.

The generic concepts these build on are one level up, in [knowledge/](../README.md): [signals](../signals/), [data preparation](../data-preparation/), [evaluation](../evaluation/), [anomaly detection](../anomaly-detection/), [drift](../drift/), [models](../models/).

## Reading order

Read top-down the first time; the numbers are a suggested path, not a requirement.

| # | Folder | Docs | Status |
|---|---|---|---|
| 1 | this folder | [time series](time-series.md) | written |
| 2 | [structure/](structure/) | [patterns](structure/patterns.md), [decomposition](structure/decomposition.md), [stationarity](structure/stationarity.md), [autocorrelation](structure/autocorrelation.md) | written |
| 3 | [tasks/](tasks/) | [tasks](tasks/tasks.md), [forecasting](tasks/forecasting.md), [imputation](tasks/imputation.md), [anomaly detection](tasks/anomaly-detection.md), [classification](tasks/classification.md) | written |
| 4 | [data-preparation/](data-preparation/) | [windows](data-preparation/windows.md), [splitting](data-preparation/splitting.md); [normalization](data-preparation/normalization.md) | written |
| 5 | [evaluation/](evaluation/) | [forecast evaluation](evaluation/forecast-evaluation.md), [point adjustment](evaluation/point-adjustment.md), [VUS (volume under the surface)](evaluation/vus.md) | placeholders |
| 6 | [drift/](drift/) | [drift in time series](drift/drift-in-time-series.md) | placeholder |
| 7 | [models/](models/) | [tokens and patching](models/tokens-and-patching.md), [forecasting models](models/forecasting-models.md) | placeholders |
| — | [datasets/](datasets/README.md) | one file per dataset, added when datasets are chosen | placeholder |

- **Before the anomaly-detection task in 3:** read the generic [anomaly detection](../anomaly-detection/) docs (what it is, kinds of anomalies, methods).
- **Before normalization in 4:** read the generic [normalization](../data-preparation/normalization.md) doc (standard, min-max and robust scaling).
- **Before 5:** read the generic [evaluation](../evaluation/) docs (errors, precision and recall, AUROC (area under the receiver operating characteristic curve), AUPRC (area under the precision-recall curve)).
- **Before 6:** read the generic [drift](../drift/) docs (distribution shift, kinds of drift).
- **Before 7:** read the generic [models](../models/) docs (transformers, masked autoencoder).

Each folder with figures keeps them, and the script that draws them, in its `assets/` folder ([figures](../README.md#figures)).
