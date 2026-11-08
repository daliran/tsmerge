# ED-021 — Runs don't resume; a run names the earlier runs it reads

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author
- **Answers:** question EQ-005 (opened 2026-11-01, raised by the first expert review, items M12 and M13)

## Problem

Two related gaps:

- **Resume after a timeout.** A job lasts at most 24 hours. A run that times out could only restart from scratch, losing its GPU hours.
- **Runs that use other runs' outputs.** Task arithmetic needs a base model and several fine-tuned checkpoints produced by earlier runs. Nothing defined how a run names its input runs, how a job finds them, or how they are recorded; a merged model couldn't be traced to the exact checkpoints it was built from.

## Options

**Resume:**

- **A. A run can span several jobs:** `submit.sh --resume` into the same folder, with the program saving `checkpoints/last.pt` regularly and on the 2-minute warning.
- **B. No resume:** each run fits in one job; a run that times out is resubmitted from scratch.

**Inputs:**

- **C. An `inputs` list in `run.json`**, plus a `RUNS_ROOT` variable so a job can find those runs.
- **D. Input paths only inside `config.json`:** less structure, harder to trace automatically.

## Decision

- **B, no resume:** this project's runs are short (minutes to a few hours), so starting fresh costs little and keeps every run a single, simple job. A run that times out gets a larger `CLUSTER_TIME` and is resubmitted.
- **C, inputs:**
  - `INPUTS="<experiment>/<run id> …" scripts/cluster/submit.sh …` records the input runs in `run.json`'s `inputs` list (each entry checked for the right form);
  - every job receives `RUNS_ROOT`, the root of all runs, so the program reads `$RUNS_ROOT/<experiment>/<run id>/checkpoints/…`;
  - a merged model is then traceable to the exact runs, and through them to their commits and configurations.

## Consequences

- Runs must fit in one job (at most 24 hours on `all_usr_prod`).
- The experiment code reads its inputs' paths from the `inputs` it was given, not from hardcoded paths.
- Input runs must still exist on the cluster (`/work` isn't backed up, and is deleted when the project expires).
- Documented in [runs.md](../runs.md).

## Revisit if

- some runs need more than 24 hours, or timeouts become frequent (then: resume, option A);
- a run needs inputs that aren't runs (e.g. an external pretrained model): then record those in `config.json`'s `data`.
