# PD-018 — A self-contained repository: no personal data, no references to earlier implementations

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author

## Problem

- The repository may be shared, published, or reused as a template. Personal names, dates tied to a person, links to other private repositories or paths on a personal machine must not end up in its history, where they are hard to remove.
- The project takes inspiration from earlier work, but this repository is meant to be the source of truth: committed files that point to earlier implementations ("same as before", "parity with …") make its content depend on something outside it.
- Agents still need that personal and machine context to work well.

## Options

### A — keep committed files free of it, and the context in a git-ignored file

- The history stays clean; the context is still available to agents and to the author.

### B — allow it in committed files

- Simpler, but personal data spreads into the history, and the repository can't stand on its own.

## Decision

Option A ([CLAUDE.md](../../../CLAUDE.md)):

- committed files contain no personal names, no graduation date, no links to other repositories, no paths outside the repository; people are "the user" (agent rules) or "the author" (records);
- committed files never refer to earlier or external implementations: every choice is justified on its own merits;
- personal and machine-specific context lives in `CLAUDE.local.md` (git-ignored), which agents read automatically; personal values the scripts need live in `.env` ([PD-014](PD-014-personal-values.md));
- the expert review's hygiene check scans for personal data ([PD-011](PD-011-expert-review-guard.md)); your names and identifiers go in `PRIVATE_PATTERNS` in `.env`.

## Consequences

- Documentation uses placeholders (`<username>`, `<project account>`) where a personal value would go.
- Comparisons with earlier work happen in conversation or in git-ignored files only.

## Revisit if

- the repository's visibility or purpose changes (e.g. it becomes a private archive only).
