# ED-035 — The technical docs are "engineering": `docs/engineering/`, with ids `ED-`/`EQ-`

- **Status:** accepted
- **Date:** 2026-11-08
- **Decided by:** the author

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

- Commit messages before 2026-11-08 still use `PD-`/`PQ-`: read `PD-NNN` as `ED-NNN` and `PQ-NNN` as `EQ-NNN`.
- The research area gets its own prefixes when it gets its first questions and decisions.
- The hygiene check of the expert review now looks for `ED-`/`EQ-` ids in `docs/engineering/`.

## Revisit if

- the split between engineering and research docs stops matching how the documentation is used.
