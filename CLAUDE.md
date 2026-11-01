# CLAUDE.md

tsmerge is a master's thesis repo (AI Engineering, Unimore) on joint training vs. task arithmetic (model merging) and other continual strategies for time-series anomaly detection and forecasting.

## Read first

- [README.md](README.md), then the `README.md` of every folder you work in: they describe what the folder holds and how it is used.
- `CLAUDE.local.md` (git-ignored, if present): personal and machine-specific context.

## Rules

- **Approval first.** Write or change code, config or scripts only when the user asked for that change. When a task needs more, propose it and wait.
- **Humans own git.** Only read-only git (`status`, `diff`, `log`, `show`). Propose commits with the [commit-plan](.claude/skills/commit-plan/SKILL.md) skill, only when asked; the user runs them.
- **No personal data in committed files:** no personal names, graduation date, links to the legacy repo, or paths outside the repo. Those live in `CLAUDE.local.md`.
- **Never guess.** When something is ambiguous, ask.
- **Small steps.** One concept per change. No new dependencies and no cross-module refactors unasked.
- **Sources are read-only:** never edit papers or the legacy repo.
- **Write in English**, and give bash commands (never PowerShell).
- When the user asks you to remember a rule, write it here or in the README it belongs to.
