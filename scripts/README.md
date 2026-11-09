# Scripts

Operational scripts, run from the repository root on your machine (a WSL shell on Windows).

| Script | What it does |
|---|---|
| [start-session.sh](start-session.sh) | Unlocks everything a working session needs, asking each password once |
| [run_local.sh](run_local.sh) | Runs a command as a recorded local run: run folder, `run.json`, provenance and `output.log` in `outputs/runs/` ([running.md](../docs/engineering/running.md#running-locally)) |
| [render_pages.sh](render_pages.sh) | Renders a paper's pages to PNG images (`outputs/pages/<bibkey>/`), for writing and verifying its note ([literature README](../docs/research/literature/README.md)) |
| [check.sh](check.sh) | Runs every check a commit must pass (also run by the pre-commit hook) |
| [runs_summary.py](runs_summary.py) | Lists the runs in `outputs/runs/`, local and pulled: status, duration, share of the time limit, estimated cost (`uv run --locked python scripts/runs_summary.py`) |
| [render_diagrams.sh](render_diagrams.sh) | Renders every Mermaid diagram in the docs' `assets/` folders to PNG with Docker; `--check` only checks they are up to date ([diagrams README](../docs/engineering/assets/README.md)) |
| [cluster/](cluster/README.md) | Runs experiments on the Unimore AImageLab-HPC cluster |

Personal values (SSH keys, cluster account, paths) come from the git-ignored `.env` at the repository root. Its template is `.env.example`.

## start-session.sh

**Why:** SSH keys with a passphrase, and a cluster that asks for a password after the key, would otherwise mean typing passwords all the time. Scripts can't type them at all, so without an unlocked session they fail with `Permission denied`.

**What it does:**

1. Loads the keys listed in `SSH_KEYS` (`.env`) into the SSH agent, asking only for keys not loaded yet.
2. Opens the shared connection to the cluster (`ssh -fN ailb`), asking for the password only if no connection is open.
3. Checks GitHub and the cluster, and prints what is unlocked.

**When:** after every restart of WSL or the machine, and when the cluster connection has closed (8 hours without use, or a network drop). It is safe to rerun.

Setting it up (the `~/.bashrc` line, `.env`) is described in [setup.md](../docs/engineering/setup.md#unlock-everything-once-per-session).

## run_local.sh

**Why:** a run on your machine should leave the same record as a cluster run, so results can be compared and traced back to the exact code that produced them.

**What it does:**

1. Copies the code as it is now (committed files and uncommitted changes, without git-ignored files) to a frozen folder in the run, so you can keep editing while the run goes on; the copy is deleted when the run ends.
2. Runs your command from that copy, in a new run folder under `outputs/runs/<experiment>/`.
3. Writes `run.json`, the provenance (commit, patch of uncommitted changes) and `output.log`.
4. Records how the run ended: `completed`, `failed`, or `canceled` (Ctrl-C).

**When:** for any local run you want to keep. A quick try or a debug session doesn't need it: those write to `outputs/scratch/`.

```bash
scripts/run_local.sh hello python -m tsmerge.hello
```

Optional, for one run: `SWEEP=<id>`, and `INPUTS="<exp>/<run id> ..."` for runs it reads from. Details: [running.md](../docs/engineering/running.md#running-locally), [runs.md](../docs/engineering/runs.md).

## render_pages.sh

**Why:** a paper note is written and verified from the pages themselves, because text extracted from a PDF garbles equations, tables and subscripts.

**What it does:** renders every page of `docs/research/literature/papers/<bibkey>.pdf` to a PNG image, `p01.png`, `p02.png`, …, in `outputs/pages/<bibkey>/` (or the folder you give). The renderer runs in a temporary uv environment, so nothing is added to the project.

**When:** before writing or checking a paper's note.

```bash
scripts/render_pages.sh lu2018learning
scripts/render_pages.sh --scale 3 lu2018learning outputs/pages/lu2018learning-zoom
```

The default scale, 2.2, keeps subscripts and small table cells legible; `--scale 3` is for pages still hard to read. Details: [literature README](../docs/research/literature/README.md).

## check.sh

**Why:** one place for the checks every commit must pass, so the list never exists in two copies.

**What it does:** checks `uv.lock`, runs ruff (lint and format), shellcheck and pytest, checks the diagrams are rendered, reports each, and fails if any fails.

The pre-commit hook in `.githooks/` runs it on every commit. Details: [CONTRIBUTING.md](../CONTRIBUTING.md#checks-before-committing).

## runs_summary.py

**Why:** to choose time limits, you need to see how close past runs came to theirs; secondarily, to keep an eye on the cluster budget.

**What it does:** reads the `run.json` of every run in `outputs/runs/`, local and pulled from the cluster, and lists for each:

- its status and duration;
- the share of its time limit it used;
- its estimated cost in the cluster's standard hours ([cluster.md](../docs/engineering/cluster.md)).

**When:** after pulling runs, and before setting the time limit of a new kind of job.

```bash
uv run --locked python scripts/runs_summary.py            # every experiment
uv run --locked python scripts/runs_summary.py hello      # one experiment
```

## render_diagrams.sh

**Why:** diagrams are kept as Mermaid text, which is easy to edit and review, but shown as PNG images; the images must always match their sources.

**What it does:**

- renders to PNG every `.mmd` source in an `assets/` folder (under `docs/` and `.claude/`) whose source changed since its last render, with a pinned Docker image, so the same source always gives the same image;
- records each source's hash in the folder's `rendered.sha256`;
- with `--all`, renders every diagram; with `--check`, only checks that every PNG is up to date, without Docker (`check.sh` runs this).

**When:** after changing a `.mmd` file; commit the source and its PNG together.

```bash
scripts/render_diagrams.sh
```

Details: [diagrams README](../docs/engineering/assets/README.md).
