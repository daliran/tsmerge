# Knowledge

General theory for people, one concept per doc: what a signal and a time series are, how data drift over time, how results are judged, the models, and how models learn and are combined.

**Nothing here is specific to this work.** A knowledge doc explains a concept for any reader: no statements about this project, its data, its choices or its results. What this work uses, chooses or finds belongs in [method/](../method/README.md) or in a [research decision](../decisions/README.md).

Unsure what a term means? The [glossary](glossary.md) gives each one in a line, with a link to its doc.

## How it's organized

- **Generic at the top, specific below:** a concept that applies to any data sits in a top-level folder (`evaluation/`, `anomaly-detection/`, `drift/`, `models/`, `learning/`); the same topic specific to time series sits under `time-series/`.
- **One concept per doc,** each starting with the idea in one sentence, then its **Builds on** and **Used by** links, so you can walk the concepts in either direction.
- **Placeholders** (`Status: placeholder`) mark docs to write: each says what it will cover and which sources to use. They're written and reviewed one at a time.

## Reading order

Read top-down the first time; the numbers are a suggested path, not a requirement. The two large areas, time series and learning, have their own README with the detailed reading order.

| # | Area | What it covers | Status |
|---|---|---|---|
| 1 | [signals/](signals/) | [signals](signals/signals.md), [sampling](signals/sampling.md), [Fourier transform](signals/fourier-transform.md) | 3 written |
| 2 | [time-series/](time-series/README.md) | what a series is, its structure, the tasks, data preparation; the time-series side of evaluation, drift and models; datasets | 12 written, 8 placeholders |
| 3 | [evaluation/](evaluation/) | [regression errors](evaluation/regression-errors.md), [precision, recall and F1](evaluation/precision-recall-f1.md); [AUROC (area under the receiver operating characteristic curve)](evaluation/auroc.md), [AUPRC (area under the precision-recall curve)](evaluation/auprc.md), [comparing results](evaluation/comparing-results.md) | 2 written, 3 placeholders |
| 4 | [anomaly-detection/](anomaly-detection/) | [anomaly detection](anomaly-detection/anomaly-detection.md), [kinds of anomalies](anomaly-detection/kinds-of-anomalies.md), [methods](anomaly-detection/methods.md) | 3 written |
| 5 | [drift/](drift/) | [distribution shift](drift/distribution-shift.md), [kinds of drift](drift/kinds-of-drift.md), [drift detection](drift/drift-detection.md), [responding to drift](drift/responding-to-drift.md) | 4 placeholders |
| 6 | [models/](models/) | [transformers](models/transformers.md), [masked autoencoder](models/masked-autoencoder.md) | 2 placeholders |
| 7 | [learning/](learning/README.md) | pretraining and fine-tuning, joint training, foundation models, continual learning, model merging | 25 placeholders |

The generic areas (3 to 6) come before the time-series docs that build on them; the [time-series README](time-series/README.md) says where.

## How the docs are written

- **Simple first:** each idea in plain words before any formula; formulas only where they save words.
- **Every fact has a source:** general concepts come from reference pages and textbooks, listed at the end of each doc with the date they were read; numbers from published papers come from the verified [literature notes](../literature/README.md).
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
