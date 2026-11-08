# ED-0031 — Shared VS Code tasks, debug configurations, extensions and settings

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author

## Problem

- Running, submitting, pulling and debugging meant remembering scripts and their arguments.
- `.vscode/` was git-ignored, so nothing editor-related was shared, and the debugger had no configuration that imports `tsmerge` correctly ([ED-0030](ED-0030-experiment-code.md)).

## Options

- **A. Commit the shared files:** `tasks.json`, `launch.json`, `extensions.json` and a few workspace settings; the rest of `.vscode/` stays ignored.
- **B. Keep `.vscode/` personal,** and only document the commands.

## Decision

Option A ([.vscode/](../../../.vscode/)):

- **tasks:** run locally, submit (GPU or CPU), status, logs, pull, set up the cluster environment, start the session, checks, render diagrams, runs summary; each runs the repository script with the same arguments as on the command line;
- **debug configurations:** *Debug a module* and *Debug current file*, from the working tree, with the repository root on the import path; their outputs go to `outputs/scratch/`;
- **extensions:** Python, debugger, Ruff, ShellCheck, Mermaid preview, WSL, Remote-SSH;
- **settings:** the project's `.venv`, pytest, LF line endings, and **Ruff exactly as the checks run it:**
  - the Ruff executable in `.venv` (`ruff.importStrategy: fromEnvironment`), the version `uv.lock` pins, not the extension's bundled copy;
  - the rules in `pyproject.toml` win over personal editor settings (`ruff.configurationPreference: filesystemFirst`);
  - format on save, and sort imports on save (the lint rule `I`); other lint fixes are left to you;
  - Black is marked as unwanted, since a second formatter would disagree with the checks;
  - ShellCheck: the system binary the checks use (`/usr/bin/shellcheck`), not the extension's bundled one; options for both from `.shellcheckrc`.
- Personal preferences stay in user settings.

## Consequences

- The files hold no personal values: those stay in `.env` ([ED-0014](ED-0014-personal-values.md)).
- Tasks and scripts must stay in step: a script's arguments change → its task changes in the same commit.
- Documented in [setup.md](../setup.md#9-vs-code) (installing and checking) and [running.md](../running.md#from-vs-code) (daily use).

## Revisit if

- another editor is used regularly (then: document its equivalents);
- the settings start to hold personal preferences.
