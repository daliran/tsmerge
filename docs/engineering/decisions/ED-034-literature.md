# ED-034 — Papers: bibkeys, PDFs kept local, verified distillation notes as the source of truth

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author

## Problem

- The research builds on 24 papers, about 96 MB of PDFs, downloaded under inconsistent names: arXiv ids (`2212.04089v3.pdf`), submission numbers with truncated titles (`11979_Merging_on_the_Fly_Witho.pdf`), and hand-numbered titles whose numbers collide across two folders.
- The repository is public: most papers can't be redistributed, especially submissions still under review, and several PDFs exceed the 5 MB limit for committed files.
- What a paper says must be available to anyone working on the repository, and checkable, without the PDF.
- Citing a paper means naming its authors, which the no-names rule ([ED-018](ED-018-self-contained-repository.md)) forbade everywhere.

## Options

### Names

- **A. Keep the download names:** nothing to do; unreadable and inconsistent; journal papers have no arXiv id.
- **B. Hand-numbered titles:** readable, but the numbers mean nothing, collide, and don't link a file to its citation.
- **C. Bibkeys** (`ilharco2023editing`): one id for the PDF, the note and the bibliography entry; matches how papers are cited.

### Where the papers live

- **A. Committed PDFs:** self-contained, but redistributes copyrighted work in a public repository, and breaks the file-size rule.
- **B. PDFs local and git-ignored; committed bibliography and notes:** legal and light; the notes must then be complete and trustworthy.

## Decision

- **Names: C.** First author's surname + year + first meaningful title word, lowercase ASCII; anonymous submissions get `anon<year><word>` until their authors are known.
- **Location: B.**
  - PDFs in `papers/<bibkey>.pdf`, git-ignored.
  - `docs/domain/references.bib` holds one entry per paper: identifiers, URL, the version read, the original file name.
  - `docs/domain/literature/<bibkey>.md` holds one note per paper.
- **The notes are the source of truth for what a paper says:** equations in LaTeX, setups and the numbers we may compare against, every item with its page; our own comments marked as such.
- **Verified before done:** an independent agent compares each note with its paper; unsupported or misstated claims are fixed before the note is marked `verified`.
- **Author names are allowed in bibliographic content:** `docs/domain/references.bib`, `docs/domain/literature/`, and the thesis text (a `thesis/` folder, created when the writing starts). The no-names rule holds everywhere else, and the hygiene check skips only these paths, and only for names.
- **Earlier notes are not imported:** the knowledge base is rebuilt from the sources, never copied from earlier notes, and committed files don't refer to them.
- **Order:** the 8 model-merging and continual-learning papers first (a pilot note reviewed before the others), then the 6 background papers; the 10 other time-series papers only if found relevant.

## Consequences

- Each machine needs its own copy of the PDFs; `references.bib` says where to get each one.
- A note costs more than a summary (page references, transcribed equations, a verification pass), but it replaces the PDF for this project.
- Documented in [docs/domain/README.md](../../domain/README.md) and [docs/domain/literature/README.md](../../domain/literature/README.md).

## Revisit if

- a paper's license allows redistribution and keeping its PDF matters (still subject to the size limit);
- verification by an agent proves unreliable (then: verification by hand, or a second agent);
- the number of papers grows enough that the index needs grouping by topic.
