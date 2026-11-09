# Research

What the research is about and how it's done. How the repository's machinery works (setup, the cluster, runs, checks) is in [engineering/](../engineering/README.md).

The area is built step by step, and every part is checked against its sources before it's marked done.

## Contents

| Folder | What it holds | Status |
|---|---|---|
| [literature/](literature/README.md) | What others published: one note per paper, the bibliography ([references.bib](literature/references.bib)), and code references | 17 papers verified, 1 code reference |
| [knowledge/](knowledge/README.md) | General theory, one concept per doc, independent of this thesis: signals, time series, change over time, evaluation, models, learning | 20 docs written, 41 placeholders |
| [method/](method/README.md) | Everything specific to this work: the protocol, experiments, findings | planned |
| [decisions/](decisions/README.md) | Research decisions (`RD-`): why the research and its docs work the way they do | 2 accepted |
| [questions/](questions/README.md) | Open research questions (`RQ-`) | none yet |

Each area answers a different question:

- **literature:** what does a source say? (one note per source, traceable to its pages)
- **knowledge:** what does a concept mean? (built from the literature notes and reference pages)
- **method:** what do *we* do, and what did we find? (links to knowledge for the concepts it uses)

## Ids

| Type | Id | Example |
|---|---|---|
| Paper or code reference | bibkey: first author's surname (or the organization) + year + first meaningful title word, lowercase ASCII | `ilharco2023editing` |
| Research question | `RQ-NNNN` | — |
| Research decision | `RD-NNNN` | — |
| Experiment | `e<NNNN>-<slug>` ([ED-0032](../engineering/decisions/ED-0032-experiment-ids.md)) | `e0001-joint-vs-merge` |

- **Anonymous submissions** get `anon<year><word>` (e.g. `anon2026quasi`), renamed once their authors are known.
- A bibkey never changes otherwise, and is never reused.
- Research decisions and questions live in [decisions/](decisions/README.md) and [questions/](questions/README.md), with the same rules as the engineering ones.

## Rules

- **Papers are sources, read-only.**
  - Their PDFs stay on your machine, in the git-ignored `literature/papers/` folder, named `<bibkey>.pdf`; they're never committed (size, and most can't be redistributed).
  - Each entry in `references.bib` says where to get the paper.
- **No earlier notes are copied in:** knowledge enters this area only through notes written from, and checked against, the sources.
- **Public sources can be cited and linked** (papers, books, reference pages, public code); every choice is still justified on its own merits ([ED-0018](../engineering/decisions/ED-0018-self-contained-repository.md)).
