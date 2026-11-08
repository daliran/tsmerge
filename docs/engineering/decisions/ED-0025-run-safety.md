# ED-0025 — Runs keep their provenance and results safe: pushed commits, no requeue, local backup

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author
- **Answers:** question EQ-0008 (opened 2026-11-01, raised by the first expert review, items M5, M6 and M16)

## Problem

Three ways a run could lose its provenance or its results:

- **Unpushed commits:** `run.json` records the commit, but if it was never pushed and later amended or rebased, it disappears, and the run points to nothing.
- **Requeued jobs:** if Slurm reran a job (e.g. after a node failure), it would run again in the same run folder, mixing two executions in one record.
- **No backup of local results:** after the cluster copy is gone, every result and `run.json` lives only in the git-ignored `outputs/`, on one machine.

## Options

**Unpushed commits:**

- **A. Warn** in `submit.sh` when the commit isn't on the remote yet.
- **B. Refuse** to submit unpushed commits: strict, but blocks quick test runs.

**Requeue:** check the cluster's setting, then decide.

**Backup:**

- **A. A documented habit,** with one command copying `outputs/` elsewhere.
- **B. A separate git repository** for results.

## Decision

- **Unpushed commits, A:** `submit.sh` warns when no remote-tracking branch contains the commit (checked locally, without contacting GitHub).
- **Requeue:** the cluster doesn't requeue jobs (`JobRequeue = 0`, checked 2026-11-02); `submit.sh` still passes `--no-requeue` explicitly (`CLUSTER_REQUEUE` in [defaults.sh](../../../scripts/cluster/defaults.sh)), so it stays that way if the configuration changes. `run.json` records it.
- **Backup, A:** after pulling, copy `outputs/` to a second place (another drive, a cloud-synced folder), checkpoints only if needed: the command is in [running.md](../running.md#safety-net).

## Consequences

- Push before submitting runs you will report.
- The backup is a habit, not automated: easy to forget.

## Revisit if

- results get lost or a commit disappears despite this (then: refuse unpushed commits, automate the backup);
- the cluster starts requeueing jobs and resuming becomes useful.
