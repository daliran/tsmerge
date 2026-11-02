# Scripts

Operational scripts, run from the repository root on your machine (a WSL shell on Windows).

| Script | What it does |
|---|---|
| [start-session.sh](start-session.sh) | Unlocks everything a working session needs, asking each password once |
| [run_local.sh](run_local.sh) | Runs a command as a recorded local run: run folder, `run.json`, provenance and `output.log` in `outputs/runs/` ([running.md](../docs/project/running.md#running-locally)) |
| [render_pages.sh](render_pages.sh) | Renders a paper's pages to PNG images (`outputs/pages/<bibkey>/`), for writing and verifying its note ([literature README](../docs/domain/literature/README.md)) |
| [check.sh](check.sh) | Runs every check a commit must pass (also run by the pre-commit hook) |
| [runs_summary.py](runs_summary.py) | Lists the runs in `outputs/runs/`, local and pulled: status, duration, share of the time limit, estimated cost (`uv run --locked python scripts/runs_summary.py`) |
| [render_diagrams.sh](render_diagrams.sh) | Renders the Mermaid diagrams of `docs/project/diagrams/` to PNG with Docker; `--check` only checks they are up to date ([diagrams README](../docs/project/diagrams/README.md)) |
| [cluster/](cluster/README.md) | Runs experiments on the Unimore AImageLab-HPC cluster |

Personal values (SSH keys, cluster account, paths) come from the git-ignored `.env` at the repository root. Its template is `.env.example`.

## start-session.sh

**Why:** SSH keys with a passphrase, and a cluster that asks for a password after the key, would otherwise mean typing passwords all the time. Scripts can't type them at all, so without an unlocked session they fail with `Permission denied`.

**What it does:**

1. Loads the keys listed in `SSH_KEYS` (`.env`) into the SSH agent, asking only for keys not loaded yet.
2. Opens the shared connection to the cluster (`ssh -fN ailb`), asking for the password only if no connection is open.
3. Checks GitHub and the cluster, and prints what is unlocked.

**When:** after every restart of WSL or the machine, and when the cluster connection has closed (8 hours without use, or a network drop). It is safe to rerun.

Setting it up (the `~/.bashrc` line, `.env`) is described in [setup.md](../docs/project/setup.md#unlock-everything-once-per-session).

## check.sh

**Why:** one place for the checks every commit must pass, so the list never exists in two copies.

**What it does:** checks `uv.lock`, runs ruff (lint and format), shellcheck and pytest, checks the diagrams are rendered, reports each, and fails if any fails. The pre-commit hook in `.githooks/` runs it on every commit. Details: [CONTRIBUTING.md](../CONTRIBUTING.md#checks-before-committing).
