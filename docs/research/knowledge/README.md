# Knowledge

General theory for people, one concept per doc: what a signal and a time series are, how series change over time, how results are judged, the models, and how models learn and are combined.

Nothing here is specific to our experiments: it's the shared vocabulary they rely on ([method/](../method/README.md) holds what's specific).

## How it's organized

- **Generic at the top, specific below:** a concept that applies to any data sits in a top-level folder (`evaluation/`, `change-over-time/`, `models/`, `learning/`); the same topic specific to time series sits under `time-series/`.
- **One concept per doc,** each starting with the idea in one sentence, then its **Builds on** and **Used by** links, so you can walk the concepts in either direction.
- **Placeholders** (`Status: placeholder`) mark docs to write: each says what it will cover and which sources to use. They're written and reviewed one at a time.

## Reading order

Read top-down the first time; the numbers are a suggested path, not a requirement.

| # | Folder | Docs | Status |
|---|---|---|---|
| 1 | [signals/](signals/) | [signals](signals/signals.md), [sampling](signals/sampling.md) | written |
| 2 | [time-series/](time-series/) | [time series](time-series/time-series.md) | written |
| 3 | [time-series/structure/](time-series/structure/) | [patterns](time-series/structure/patterns.md), [decomposition](time-series/structure/decomposition.md), [stationarity](time-series/structure/stationarity.md), [autocorrelation](time-series/structure/autocorrelation.md) | written |
| 4 | [time-series/tasks/](time-series/tasks/) | [tasks](time-series/tasks/tasks.md), [forecasting](time-series/tasks/forecasting.md), [imputation](time-series/tasks/imputation.md), [anomaly detection](time-series/tasks/anomaly-detection.md), [classification](time-series/tasks/classification.md) | written |
| 5 | [time-series/data-preparation/](time-series/data-preparation/) | [windows](time-series/data-preparation/windows.md), [splitting](time-series/data-preparation/splitting.md); [normalization](time-series/data-preparation/normalization.md) | written; 1 placeholder |
| 6 | [evaluation/](evaluation/) | [regression errors](evaluation/regression-errors.md), [precision, recall and F1](evaluation/precision-recall-f1.md); [AUROC](evaluation/auroc.md), [AUPRC](evaluation/auprc.md), [comparing results](evaluation/comparing-results.md) | 2 written; 3 placeholders |
| 7 | [time-series/evaluation/](time-series/evaluation/) | [forecast evaluation](time-series/evaluation/forecast-evaluation.md), [point adjustment](time-series/evaluation/point-adjustment.md), [VUS](time-series/evaluation/vus.md) | placeholders |
| 8 | [change-over-time/](change-over-time/) | [distribution shift](change-over-time/distribution-shift.md), [kinds of drift](change-over-time/kinds-of-drift.md), [drift detection](change-over-time/drift-detection.md), [responding to drift](change-over-time/responding-to-drift.md) | placeholders |
| 9 | [time-series/change-over-time/](time-series/change-over-time/) | [drift in time series](time-series/change-over-time/drift-in-time-series.md) | placeholder |
| 10 | [models/](models/) | [transformers](models/transformers.md), [masked autoencoder](models/masked-autoencoder.md) | placeholders |
| 11 | [time-series/models/](time-series/models/) | [tokens and patching](time-series/models/tokens-and-patching.md), [forecasting models](time-series/models/forecasting-models.md) | placeholders |
| 12 | [learning/](learning/) | [self-supervised learning](learning/self-supervised-learning.md), [pretraining and fine-tuning](learning/pretraining-and-fine-tuning.md), [parameter-efficient fine-tuning](learning/parameter-efficient-fine-tuning.md), [joint training](learning/joint-training.md) | placeholders |
| 13 | [learning/continual-learning/](learning/continual-learning/) | [continual learning](learning/continual-learning/continual-learning.md), [forgetting and plasticity](learning/continual-learning/forgetting-and-plasticity.md), [co-observation](learning/continual-learning/co-observation.md), [sequential fine-tuning](learning/continual-learning/sequential-fine-tuning.md), [replay](learning/continual-learning/replay.md), [regularization](learning/continual-learning/regularization.md), [parameter isolation](learning/continual-learning/parameter-isolation.md) | placeholders |
| 14 | [learning/continual-learning/model-merging/](learning/continual-learning/model-merging/) | [weight-space geometry](learning/continual-learning/model-merging/weight-space-geometry.md), [loss landscape](learning/continual-learning/model-merging/loss-landscape.md), [task arithmetic](learning/continual-learning/model-merging/task-arithmetic.md), [model merging](learning/continual-learning/model-merging/model-merging.md), [interference reduction](learning/continual-learning/model-merging/interference-reduction.md), [continual merging](learning/continual-learning/model-merging/continual-merging.md), [Fisher information](learning/continual-learning/model-merging/fisher-information.md) | placeholders |
| — | [time-series/datasets/](time-series/datasets/README.md) | one file per dataset, added when datasets are chosen | placeholder |

## How the docs are written

- **Simple first:** each idea in plain words before any formula; formulas only where they save words.
- **Every fact has a source:** general concepts come from reference pages and textbooks, listed at the end of each doc with the date they were read; numbers from published papers come from our verified [literature notes](../literature/README.md).
- **Theory only:** no code, and models are described as ideas, not implementations.

## Figures

Each folder with pictures has an `assets/` folder beside its docs, holding the figures and the script that draws them.

Its README lists each figure and where it's shown. The figures are synthetic and illustrative, drawn from simple formulas with a fixed random seed.

To redraw one folder's figures, from the repository root (matplotlib runs in a temporary uv environment, so it isn't a project dependency):

```bash
uv run --no-project --with matplotlib==3.10.7 --with numpy python \
    docs/research/knowledge/<folder>/assets/make_figures.py
```

After changing a figure, rerun its script and commit the script and the PNGs together.
