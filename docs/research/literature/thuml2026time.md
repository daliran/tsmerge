# thuml2026time — Time-Series-Library (TSLib)

- **Status:** reference: a checklist, not a verified note
- **Reference:** THUML, *Time-Series-Library*, public code, MIT license, pinned at commit `4e938a17` (2026-04-18) ([references.bib](references.bib))
- **Code:** <https://github.com/thuml/Time-Series-Library>
- **Paper:** [wang2026deep](wang2026deep.md) presents the library and its benchmark.

## What it is

The benchmark code behind the time-series survey [wang2026deep](wang2026deep.md): many deep time-series models and datasets behind one interface, covering forecasting, imputation, classification and anomaly detection. Benchmark numbers in the papers we read often come from it, so its defaults are the de-facto protocol.

## Why this file is a checklist

Our notes found protocol details the papers don't state. The code is where they're settled, but reading all of it now would be work without a use. So this file lists what to check, each with where the question came from; an item is checked when an experiment needs the answer.

- **Pinned:** every answer refers to the commit above, with `file:line`. If we move to a newer commit, the checked items are checked again.
- **Read-only:** a local clone, if needed, lives outside the repository or in a git-ignored folder; nothing from the library is copied in. Copying code would be a separate decision, and its MIT license would then require keeping its copyright notice.

## Things to check

| # | Question | Raised in | Status |
|---|---|---|---|
| 1 | Train/validation/test split ratios, per dataset | [wang2026deep](wang2026deep.md) (no split ratios in the paper) | to check |
| 2 | Window stride for training and evaluation | [wang2026deep](wang2026deep.md) | to check |
| 3 | Which normalization the benchmark runs apply, and with which statistics | [wang2026deep](wang2026deep.md) | to check |
| 4 | The denormalization formula: the paper's printed version isn't the inverse of its normalization | [wang2026deep](wang2026deep.md) | to check |
| 5 | Anomaly detection: window length, how reconstruction error becomes a label (the threshold rule) | [wang2026deep](wang2026deep.md), [wu2023timesnet](wu2023timesnet.md) | to check |
| 6 | Anomaly detection: whether point adjustment is applied | [wang2026deep](wang2026deep.md), [wu2023timesnet](wu2023timesnet.md) | to check |
| 7 | Anomaly detection: how window scores are mapped back to time steps | [wu2023timesnet](wu2023timesnet.md) | to check |

When an item is checked, its status becomes `checked (YYYY-MM-DD): <answer>, <file:line>`.
