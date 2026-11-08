# ED-0011 — Expert reviews: a guard keeps the review agents off the cluster

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author
- **History:**
  - 2026-11-02: the guard missed `logs.sh` (it connects to the cluster); it now blocks it, and the new `run_local.sh` and `render_diagrams.sh`, which write files.
  - 2026-11-02: the review folder, where the guard allows writes and keeps its log, moved to `outputs/expert-reviews/` (see ED-0019).

## Problem

The `/expert-review` skill ([.claude/README.md](../../../.claude/README.md)) runs several AI reviewer agents. They must only read and check the repository: never contact the cluster, never change files outside their review folder. In the first review (2026-11-01):

- the guard hook, declared inside the review agents' own definitions, **never ran**: commands it should have blocked went through (only the agents' instructions kept them off the cluster);
- its matching was too strict (it blocked `grep ssh …`) and too loose (it missed `cd scripts && cluster/submit.sh`), and it failed open on unreadable input;
- the harness refuses report files written by subagents, so the aggregator couldn't save its report.

## Options

### A — a project hook, filtered by agent

- Registered in `.claude/settings.json`, where hooks reliably run; acts only when the caller is a review agent.
- The hook runs on every tool call of every session, so it must be fast and silent for everyone else.

### B — keep the hook in the agents' definitions

- No effect on other sessions, but it silently didn't run, with no way to confirm it's active.

### C — no hook

- Only the agents' instructions protect the cluster: no safety net.

## Decision

Option A ([expert_review_guard.py](../../../.claude/hooks/expert_review_guard.py)):

- registered in `.claude/settings.json`, run with the project environment's Python (uv's 3.12.16, the fastest launcher); for any caller other than `expert-reviewer` and `expert-review-aggregator`, it allows everything;
- it checks **what each part of a command runs**, not every word: it blocks `ssh`, `rsync`, `scp`, Slurm commands, any cluster script, and the scripts that write outside the review folder (`run_local.sh`, `render_diagrams.sh`), under any path; it allows reading and checking them (`grep`, `cat`, `shellcheck`, `bash -n`);
- it blocks Write/Edit calls outside `outputs/expert-reviews/`;
- it fails closed: unreadable input is blocked;
- every call it checks is logged to `outputs/expert-reviews/guard.log` (git-ignored): an audit trail, and proof it runs;
- the aggregator returns the report as text; `save_report.py` writes it unchanged.

**Verified:** 25 tests at the time (`tests/test_expert_review_guard.py`, 28 since the 2026-11-02 additions); live, a review agent's call appeared in the log (2026-11-01).

## Consequences

- The guard needs the project environment (`uv sync`): without `.venv`, the hook can't start and doesn't block.
- It inspects command text: a guardrail, not a security boundary. The agents' instructions forbid the same things.

## Revisit if

- Claude Code gains a reliable per-agent permission system: replace the hook with it;
- the log shows blocked calls that were legitimate, or allowed calls that weren't.
