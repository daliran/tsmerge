# ED-032 — Experiments are named `e<NNN>-<slug>`, and each has a short doc

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author
- **Answers:** question EQ-003 (opened 2026-11-01, raised by the first expert review)
- **History:**
  - 2026-11-08: the research area is `docs/research/`; experiment docs and research questions (`RQ-`) live in its `method/` folder ([ED-036](ED-036-research-docs.md)). Was: the domain area, with `DQ-` ids.

## Problem

- Every run belongs to an experiment, but an experiment was only a free name (`hello`, `timeout-test`), and that name is its folder in `outputs/runs/`.
- The thesis must trace every result back to the research question it answers; without an id, that link lived only in memory.

## Options

- **A. The id is part of the name,** e.g. `e001-joint-vs-merge`: grep-able in folders, `outputs/jobs.log` and `run.json`; runs sort by id. The id format is fixed now.
- **B. A separate `experiment_id` field** in `config.json`, with free names: shorter names, but the link exists only inside files.
- **C. Decide with the domain docs and the first real experiment:** fits a structure not known yet, but leaves the question open.

## Decision

Option A:

- **an experiment's name is `e<NNN>-<slug>`:** `NNN` is three digits, never changed and never reused, like decision ids; the slug says what it studies in a few words (`e001-joint-vs-merge`);
- **each experiment has a short doc,** written before its first run, in [docs/research/method/](../../research/method/README.md) (created with the first experiment): what it tests, which research questions it answers, which runs or sweeps belong to it;
- **names that aren't experiments stay allowed,** for setup and smoke tests (`hello`): the scripts accept any valid name; only experiment runs use the `e<NNN>-` form.

## Consequences

- Runs of an experiment are found by name everywhere: `outputs/runs/e001-…/`, `run.json`'s `experiment`, `outputs/jobs.log`.
- Research questions get `RQ-` ids in [docs/research/method/](../../research/method/README.md); each experiment doc links its questions.
- Documented in [runs.md](../runs.md#concepts).

## Revisit if

- experiments turn out to need a hierarchy (e.g. sub-studies) that one flat id can't express;
- more than 999 experiments (unlikely).
