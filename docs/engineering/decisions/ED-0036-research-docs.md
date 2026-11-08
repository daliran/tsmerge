# ED-0036 — The research docs: literature, knowledge (generic above, time-series below), method; ids `RD-`/`RQ-`

- **Status:** accepted
- **Date:** 2026-11-08
- **Decided by:** the author

## Problem

- The research documentation lived in `docs/domain/`: the bibliography, the paper notes, and a five-chapter guide to the basic concepts (signals, time series, patterns, tasks, windows).
- Much more is coming: theory on drift, evaluation, models, continual learning and model merging; a file per dataset; and everything specific to this work (research questions and decisions, the protocol, experiments, findings).
- Five long chapters don't scale to that: a concept explained inside a chapter can't be linked, reused or reviewed on its own, and general theory would mix with what this thesis decides.
- "Domain" didn't say what the folder holds; the technical area had just become "engineering" ([ED-0035](ED-0035-engineering-folder.md)).

## Options

- **A. Keep `domain/` and grow the guide chapter by chapter:** no move; chapters get long, concepts can't be linked one by one, and general theory mixes with work-specific choices.
- **B. Split by kind of content:** `research/` with `literature/` (what others published), `knowledge/` (general theory, one concept per doc) and `method/` (everything specific to this work).
- **C. Split by topic only** (time series, drift, merging…), each folder mixing papers, theory and our choices: hard to tell what's general from what we decided.

## Decision

Option B:

- **`docs/domain/` is now `docs/research/`,** and `references.bib` moves into `literature/`, beside the notes it indexes.
- **`literature/`:** one verified note per paper, the bibliography, and code references (a pinned `@software` entry with a checklist note, e.g. the Time-Series-Library).
- **`knowledge/`:** general theory, **one concept per doc**, each with *Builds on* and *Used by* links. **Generic concepts sit at the top** (`evaluation/`, `change-over-time/`, `models/`, `learning/`); **the same topics specific to time series sit under `time-series/`** (`structure/`, `tasks/`, `data-preparation/`, `evaluation/`, `change-over-time/`, `models/`, `datasets/`). Signals have their own folder. Continual learning is under `learning/`, and model merging, with everything it relies on, under `learning/continual-learning/`.
- **`method/`:** everything specific to this work: research questions `RQ-NNNN`, research decisions `RD-NNNN`, the protocol, experiment docs ([ED-0032](ED-0032-experiment-ids.md)), findings; each part created when first needed.
- **The five guide chapters were split** into one-concept docs, keeping their text and sources; the rest of the planned docs exist as **placeholders** (what each will cover, its links, the sources to use), written and reviewed one at a time.
- **Figures:** one `assets/` folder per knowledge folder with pictures, each with its own drawing script ([ED-0028](ED-0028-diagrams.md)).

## Consequences

- Every concept has one place and one link; a new doc goes where its generality puts it, and the knowledge README's map lists it.
- Placeholders make the plan visible without writing everything at once; their status says what's still to write.
- The hygiene check knows the new ids (`RD-`, `RQ-`) and the new bibliographic path.
- Documented in [docs/research/README.md](../../research/README.md), [knowledge/README.md](../../research/knowledge/README.md) and [method/README.md](../../research/method/README.md).

## Revisit if

- A folder grows too large to scan, or a concept keeps not fitting the generic/time-series split.
