# ED-017 — People run git; AI agents propose commits

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author

## Problem

- AI agents work in this repository. If they commit, push or rewrite history on their own, changes land without a human understanding or approving them, and the history stops reflecting deliberate steps.
- Commits must stay small, purposeful and readable, so the history explains itself.

## Options

### A — agents only read git, and propose commits for a person to run

- Every change into the history is a human action; the plan is a checkpoint.
- A few more steps for each commit.

### B — agents commit, people review afterwards

- Faster, but changes land before anyone has read them.

## Decision

Option A ([CONTRIBUTING.md](../../../CONTRIBUTING.md)):

- agents use only read-only git (`status`, `diff`, `log`, `show`);
- they propose commits with the [commit-plan](../../../.claude/skills/commit-plan/SKILL.md) skill, only when asked: which files go in each commit, the message and the exact commands;
- commit messages follow Conventional Commits, enforced by the `commit-msg` hook ([ED-012](ED-012-code-checks.md));
- each commit has one clear purpose; the default branch is `main`;
- agent-written commits carry no attribution lines.

## Consequences

- A commit plan is proposed only on request; the person decides when to commit.
- Work can stay uncommitted across several steps, until the person chooses to commit it.

## Revisit if

- the repository gets other contributors, or a CI that should commit (e.g. generated results).
