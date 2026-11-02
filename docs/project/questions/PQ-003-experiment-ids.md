# PQ-003 — How are experiments identified, and linked to the research questions they answer?

- **Status:** open
- **Opened:** 2026-11-01

## Why it matters

- Every run belongs to an experiment, but today an experiment is only a free name (`hello`, `timeout-test`).
- The thesis needs to trace every result back to the question it answers. Without an id or a link, that relation lives only in someone's memory.
- Raised by the first expert review (2026-11-01).

## Options

- **A. Names start with their id**, e.g. `e-001-joint-vs-merge`.
  - Grep-able; runs group by id automatically in `outputs/runs/`.
  - The id format is fixed early, before the experiments' structure exists.
- **B. A separate `experiment_id` field** in `config.json`, with free names.
  - Names stay short and readable.
  - The link exists only inside files, not in folder names.
- **C. Decide with the experiments' structure:** where experiment code lives, and how experiments link to questions and claims (the domain docs).
  - Fits the id format to how experiments are actually organized.

## Hypotheses

Not established yet:

- Experiments will need a stable id, like decisions and questions, and each will answer one or more research questions.

## Evidence so far

- [PD-003](../decisions/PD-003-runs-and-jobs.md): runs, experiments and sweeps as implemented.

## Next action

Decide together with the experiments' structure and the domain docs (option C, chosen for now on 2026-11-01).
