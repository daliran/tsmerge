# ED-012 — Code checks: one script, explicit rules, run on every commit

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author
- **History:**
  - 2026-11-02: `check.sh` also checks that the diagrams' images match their sources (ED-028); ShellCheck's options moved to `.shellcheckrc`, shared with the VS Code extension (ED-031).

## Problem

- Checks that depend on remembering to run them don't get run.
- The list of checks must live in one place, or the docs, the hook and the habits drift apart.
- Raised by the first expert review (2026-11-01):
  - **M7:** plain `uv run` silently rewrites `uv.lock` when it doesn't match `pyproject.toml`, so a commit could hold a mismatched pair;
  - **L10:** ruff used its default rules, which can change when ruff is upgraded;
  - **M21, L9:** no tests and no pytest configuration.

## Options

For running the checks:

- **A. A versioned git hook** that runs one checks script: it's in the repo and reviewed like any file; each clone enables it once.
- **B. The `pre-commit` framework:** checks only staged files and manages tool versions, but adds a dependency and its own configuration.
- **C. A hook in `.git/hooks/`:** not versioned, lost on a fresh clone.

## Decision

Option A:

- **[scripts/check.sh](../../../scripts/check.sh)** runs every check:
  - `uv lock --check`: the lockfile matches `pyproject.toml`;
  - ruff lint and format, with `uv run --locked`, which never rewrites the lockfile;
  - shellcheck on every shell script and hook (settings in `.shellcheckrc`);
  - pytest (`tests/`; "no tests found" passes);
  - the diagrams' images match their sources ([ED-028](ED-028-diagrams.md));
- **[.githooks/](../../../.githooks/README.md)**: `pre-commit` runs `check.sh`; `commit-msg` enforces Conventional Commits; enabled once per clone with `git config core.hooksPath .githooks`;
- **ruff rules are explicit** in `pyproject.toml`: `E, W, F, I, UP, B, SIM, RUF`, line length 88 (ruff's default);
- tests run scripts the way they really run (as subprocesses, or loaded from their file).

## Consequences

- The hooks check the working tree, not only the staged files.
- `git commit --no-verify` skips the hooks: only when really needed.
- After changing dependencies: `uv lock`, and commit both files together.

## Revisit if

- the checks become slow enough to discourage committing (then: run the slow part only in a later CI);
- staged-only checking matters (then: option B).
