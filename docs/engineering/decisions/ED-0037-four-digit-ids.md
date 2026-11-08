# ED-0037 — Ids have 4 digits: decisions, questions and experiments

- **Status:** accepted
- **Date:** 2026-11-09
- **Decided by:** the author

## Problem

- Decision, question and experiment ids had 3 digits (`ED-034`, `EQ-012`, `e001`): at most 999 per prefix.
- The project had used 36 engineering decisions in its first days; research decisions, research questions and experiments were about to start.
- Changing the width later would touch more files and references than now (83 files, about 330 references at the time).

## Options

- **A. Keep 3 digits:** nothing to change; a later switch, if ever needed, costs more.
- **B. Switch to 4 digits now, for every kind of id:** one rewrite now, then room for 9,999 per prefix; a second exception to "ids never change" ([ED-0035](ED-0035-engineering-folder.md) was the first).

## Decision

Option B:

- `ED-`, `EQ-`, `RD-`, `RQ-` ids have 4 digits (`ED-0037`); experiments are `e<NNNN>-<slug>` (`e0001-joint-vs-merge`, [ED-0032](ED-0032-experiment-ids.md));
- every file name and every reference in the repository was rewritten at once, keeping each number;
- the hygiene check accepts only the 4-digit form, so a stray 3-digit id is reported as unknown.

## Consequences

- Commit messages before 2026-11-09 use 3 digits: read `ED-034` as `ED-0034`, `EQ-012` as `EQ-0012`; older ones use `PD-`/`PQ-` ([ED-0035](ED-0035-engineering-folder.md)).
- Decision texts written before the switch keep their own wording where it describes what happened then (ED-0035).
- Documented in the [decisions](README.md) and [questions](../questions/README.md) READMEs and the [docs README](../../README.md).

## Revisit if

- Never expected: 9,999 per prefix is far beyond a thesis.
