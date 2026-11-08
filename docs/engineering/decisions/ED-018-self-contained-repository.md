# ED-018 — A self-contained repository: no local paths or personal values, no references to the material used to build it

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author
- **History:**
  - 2026-11-02: authors' names are allowed in bibliographic content (the bibliography, the paper notes, the thesis text), since citing a paper names its authors; the hygiene check skips those paths for names only ([ED-034](ED-034-literature.md)).
  - 2026-11-08: narrowed to what it was meant for. Only the private material used to build the repository is excluded (the author's own earlier work and repositories, local files, notes, drafts); public sources (papers, books, official documentation, public code) may be cited and linked. Was: no links to other repositories and no references to any external implementation, which read literally forbade citing public code and reference pages.
  - 2026-11-08: personal names and the graduation date are no longer excluded, and the private-pattern check is removed: the goal was only to keep the repository independent of the private material used to build it and of this machine. Was: no personal names (except authors in bibliographic content) and no graduation date, checked against `PRIVATE_PATTERNS` in `.env`.

## Problem

- The repository may be shared, published, or reused as a template. Paths on a personal machine and personal values (usernames, accounts, hosts) make it work only on one machine, and are hard to remove from history once committed.
- The project takes inspiration from earlier work, but this repository is meant to be the source of truth: committed files that point to earlier implementations ("same as before", "parity with …") make its content depend on something outside it.
- Agents still need that personal and machine context to work well.

## Options

### A — keep committed files free of it, and the context in a git-ignored file

- The history stays clean; the context is still available to agents and to the author.

### B — allow it in committed files

- Simpler, but personal data spreads into the history, and the repository can't stand on its own.

## Decision

Option A ([CLAUDE.md](../../../CLAUDE.md)):

- committed files contain no paths outside the repository and no personal values (they go in `.env`, [ED-014](ED-014-personal-values.md)); people are "the user" (agent rules) or "the author" (records), a writing convention;
- committed files never refer to the private material used to build the repository: the author's own earlier work and repositories, local files, notes, drafts (listed in `CLAUDE.local.md`); public sources (papers, books, official documentation, public code) may be cited and linked, and every choice is still justified on its own merits;
- personal and machine-specific context lives in `CLAUDE.local.md` (git-ignored), which agents read automatically; personal values the scripts need live in `.env` ([ED-014](ED-014-personal-values.md));
- the expert review's hygiene check flags absolute paths of a personal machine ([ED-011](ED-011-expert-review-guard.md)); references to the private material are kept out by this rule and by review, since a check would have to name it.

## Consequences

- Documentation uses placeholders (`<username>`, `<project account>`) where a personal value would go.
- Comparisons with earlier work happen in conversation or in git-ignored files only.

## Revisit if

- the repository's visibility or purpose changes (e.g. it becomes a private archive only).
