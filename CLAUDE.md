# CLAUDE.md

tsmerge is a master's thesis repo (AI Engineering, Unimore) on joint training vs. task arithmetic (model merging) and other continual strategies for time-series anomaly detection and forecasting.

## Read first

- [README.md](README.md), then the `README.md` of every folder you work in: they describe what the folder holds and how it is used.
- `CLAUDE.local.md` (git-ignored, if present): personal and machine-specific context.

## Rules

- **Nothing is assumed; the user validates every decision.** Present each proposal with the context needed to understand it fully: what it changes, the options, their consequences and trade-offs. Give a recommendation, then wait for the user's decision. When something is ambiguous, ask instead of guessing.
- **Plan before acting.** Analyze first, present a plan, and act only once the user approves it. Only minor changes skip this: typos, formatting, or an edit the user has just described exactly.
- **Small steps, clean commits.** One concept per change; every commit has one clear purpose. No new dependencies and no cross-module refactors unasked.
- **Humans own git.** Only read-only git (`status`, `diff`, `log`, `show`). Propose commits with the [commit-plan](.claude/skills/commit-plan/SKILL.md) skill, only when asked; the user runs them.
- **No personal data in committed files:** no personal names, graduation date, links to other repositories, or paths outside the repo. Those live in `CLAUDE.local.md`.
- **This repo is the source of truth.** Committed files never refer to earlier or external implementations it takes inspiration from; any context on them lives in `CLAUDE.local.md`.
- **Sources are read-only:** never edit papers or external repositories used as reference.
- **US English** in everything written to the repository. Give bash commands, never PowerShell.
- **Folder `CLAUDE.md` files:** none yet. When a folder first needs rules that only agents need, propose adding one there (starting with `@README.md`).
- **Knowledge is written down.** When the user asks you to remember a rule, write it here or in the README it belongs to (personal or machine-specific context: `CLAUDE.local.md`), never only in session memory, so fresh sessions follow it too.
