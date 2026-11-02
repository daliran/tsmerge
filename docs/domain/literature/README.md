# Literature

One distillation note per paper. **The notes are the source of truth for what a paper says:** the PDFs stay local and uncommitted, so a note must hold everything this project needs from its paper, checked against it ([PD-034](../../project/decisions/PD-034-literature.md)).

## Rules

- **One file per paper:** `<bibkey>.md`, with the paper's entry in [references.bib](../references.bib) and its PDF in `papers/<bibkey>.pdf`.
- **Everything is traceable:** every equation, number and claim carries the page it comes from (`p. 4`, `Table 2, p. 7`). What isn't in the paper isn't in the note; our own comments are marked as such (**Our reading:**).
- **Pages are the PDF's own pages,** counted from 1 (the `pNN.png` of `render_pages.sh`), which may differ from the number printed on the page.
- **Equations in LaTeX, numbers exactly as printed:** results we may compare against are copied as tables, with their units and settings.
- **Read from the page images,** not from extracted text, so equations and tables come through correctly: `scripts/render_pages.sh <bibkey>` writes one PNG per page to `outputs/pages/<bibkey>/`. The default resolution (scale 2.2) keeps subscripts and small table cells legible; for a page that is still hard to read, render again with `--scale 3` into another folder. (The first notes were read at scale 1.6, which proved too small for some cells: their writers rendered zoomed copies.)
- **Verified before done:** after the note is written, an independent agent reads the paper and the note and lists every claim it can't find in the paper, or finds stated differently. The note is fixed, and only then marked `verified`, with the date.
- **A paper's own code link** (from the paper itself) belongs in its note's header: it's part of the bibliographic record, not a link to another project of ours.
- **Statuses:** `draft` → `verified`. A note is updated when we read further (e.g. an appendix), and checked again.
- **A newer version of a paper** (e.g. arXiv v3 after we read v2) is noted in its entry; the note says which version it describes.

## Template

```markdown
# <bibkey> — <title>

- **Status:** draft | verified (YYYY-MM-DD)
- **Reference:** authors, venue, year; arXiv id or DOI ([references.bib](../references.bib))
- **Version read:** e.g. arXiv v3 (31 pages: main text pp. 1–10, appendix pp. 11–31)
- **Read:** which parts (e.g. main text and appendices A–C)

## In one paragraph

What the paper does, why, and what it finds.

## Problem

The question it addresses, and the setting.

## Method

Definitions and equations (LaTeX), with pages. Enough to reimplement what we need.

## Experimental setup

Models, datasets, training and evaluation details, hyperparameters.

## Results

The numbers that matter for this project, as tables, with pages.

## Assumptions and limitations

What the paper assumes, what it doesn't show, and what it says itself about its limits.

## Relevance to this thesis

**Our reading:** what we reuse, what we test, which open questions it informs.

## Quotes worth keeping

> Exact quotes, each with its page.
```

## Index

| Paper | Topic | Status |
|---|---|---|
| [ilharco2023editing](ilharco2023editing.md) | model merging: task arithmetic, the founding paper | verified |
| [ortizjimenez2023task](ortizjimenez2023task.md) | model merging: weight disentanglement, fine-tuning in the tangent space | verified |
| [porrello2026dataless](porrello2026dataless.md) | model merging: curvature (KFAC) regularization against interference, without other tasks' data | verified |
| [tang2025merging](tang2025merging.md) | continual model merging: orthogonal projection (OPCM) | verified |
| [lin2026unlocking](lin2026unlocking.md) | continual model merging: an ODE view (ODE-M) | verified |
| [wang2026revitalizing](wang2026revitalizing.md) | continual model merging without storing past models (TRM) | verified |
| [anon2026quasi](anon2026quasi.md) | continual model merging: quasi-orthogonal projection (QOMM); under review | verified |
| [li2025became](li2025became.md) | continual learning: Bayesian adaptive model merging (BECAME) | verified |
| [pang2021deep](pang2021deep.md) | anomaly detection: survey of deep methods (taxonomy, challenges, datasets) | verified |
| [he2022masked](he2022masked.md) | self-supervised pre-training: masked autoencoders | verified |
| [wang2026deep](wang2026deep.md) | time series: survey of deep models, and the TSLib benchmark | verified |
| [wu2023timesnet](wu2023timesnet.md) | time series: TimesNet, one backbone for five tasks including anomaly detection | verified |
| [cao2023anomaly](cao2023anomaly.md) | anomaly detection under distribution shift | verified |
| [mathur2016swat](mathur2016swat.md) | dataset: the SWaT testbed (no released-dataset details) | verified |

Planned, in this order (see [references.bib](../references.bib) for the full list):

1. ~~Model merging and continual learning~~: done (8 notes above).
2. ~~Time series, anomaly detection, background~~: done (6 notes above).
3. **Other time-series papers,** only if found relevant: the remaining 10 entries of `references.bib`.
