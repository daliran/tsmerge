# Domain

What the research is about: the papers it builds on, the research questions, and (later) the experiments and the claims they support. How the repository's machinery works is in [project/](../engineering/README.md).

The area is built step by step, and every part is verified against its sources before it's marked done.

## Contents

| Path | What it holds | Status |
|---|---|---|
| [references.bib](references.bib) | The bibliography: one entry per paper, keyed by its bibkey | 24 papers |
| [literature/](literature/README.md) | One distillation note per paper: the source of truth for what a paper says | 14 notes verified: the 8 model-merging and continual-learning papers, and the 6 background papers |

Planned, created when first needed: research questions (`DQ-NNN`), domain decisions (`DD-NNN`), experiment docs (`e<NNN>-<slug>`, [ED-032](../engineering/decisions/ED-032-experiment-ids.md)), claims.

## Ids

| Type | Id | Example |
|---|---|---|
| Paper | bibkey: first author's surname + year + first meaningful title word, lowercase ASCII | `ilharco2023editing` |
| Research question | `DQ-NNN` | — |
| Domain decision | `DD-NNN` | — |
| Experiment | `e<NNN>-<slug>` | `e001-joint-vs-merge` |

- **Anonymous submissions** get `anon<year><word>` (e.g. `anon2026quasi`), renamed once their authors are known; the old key is then recorded in the entry's `note`.
- A bibkey never changes otherwise, and is never reused.

## Rules

- **Papers are sources, read-only.** Their PDFs stay on your machine, in the git-ignored `papers/` folder, named `<bibkey>.pdf`; they're never committed (size, and most can't be redistributed). Each entry in `references.bib` says where to get the paper.
- **Author names are allowed here,** in bibliographic content only (`references.bib`, `literature/`): citing a paper means naming its authors. Everywhere else, the repository's no-names rule applies ([ED-034](../engineering/decisions/ED-034-literature.md)).
- **No earlier notes are copied in:** knowledge enters this area only through notes written from, and checked against, the sources.

Why it works this way: [ED-034](../engineering/decisions/ED-034-literature.md).
