# ED-0035 — The technical docs are "engineering": `docs/engineering/`, with ids `ED-`/`EQ-`

- **Status:** accepted
- **Date:** 2026-11-08
- **Decided by:** the author
- **History:**
  - 2026-11-09: ids became 4 digits ([ED-0037](ED-0037-four-digit-ids.md)); the text below keeps the 3-digit form it was written with, except the reading guide under Consequences.

## Problem

- The technical documentation (setup, environment, cluster, running and recording runs, checks, tooling) lived in `docs/project/`, with decisions `PD-NNN` and questions `PQ-NNN`.
- "Project" was ambiguous: the thesis is a project too, and the research documentation sits beside this folder. The folder covers all the technical work around the research, not only the repository.
- The research side is being reorganized at the same time (literature, knowledge, method), so the two areas need names that say what each one is.

## Options

- **A. Keep `project/` and `PD-`/`PQ-`:** no change; the ambiguity stays.
- **B. Rename the folder only:** `engineering/` with `PD-`/`PQ-` ids; the ids no longer match their folder.
- **C. Rename the folder and the ids:** `engineering/` with `ED-`/`EQ-`, same numbers; one exception to the rule that ids never change.

## Decision

Option C:

- `docs/project/` is now `docs/engineering/`;
- every `PD-NNN` is now `ED-NNN`, and every `PQ-NNN` is now `EQ-NNN`, keeping its number, in file names and in every reference in the repository;
- the rule that ids never change keeps this single, recorded exception ([decisions README](README.md)).

## Consequences

- Commit messages before 2026-11-08 still use `PD-`/`PQ-`: read `PD-NNN` as `ED-NNNN` and `PQ-NNN` as `EQ-NNNN` (4 digits since [ED-0037](ED-0037-four-digit-ids.md)).
- The research area's prefixes are `RD-`/`RQ-` ([ED-0036](ED-0036-research-docs.md)).
- The hygiene check of the expert review now looks for `ED-`/`EQ-` ids in `docs/engineering/`.

## Revisit if

- the split between engineering and research docs stops matching how the documentation is used.
