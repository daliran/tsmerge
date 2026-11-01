# Project docs

How this repository works: setting it up, running experiments, and making changes.

This folder is only about the machinery. What the research is about will live in the domain area (not written yet).

## Contents

| File | Concern | When you read it |
|---|---|---|
| [setup.md](setup.md) | One-time setup: your machine (Linux or WSL2: tools, git, SSH, Python with uv, GPU) and your cluster account | once per machine or account |
| [cluster.md](cluster.md) | Reference facts about the Unimore AImageLab-HPC cluster: access, partitions, GPUs, accounts, storage, rules | when you need a fact |
| [running.md](running.md) | Daily operation: running locally and on the cluster, debugging, getting results back | every working day |
| [decisions/](decisions/README.md) | Project decisions (`PD-NNN`): template, rules, index | before changing how things work |
| [questions/](questions/README.md) | Open project questions (`PQ-NNN`): template, rules, index | when something isn't decided yet |

How to change the repository (git, checks, commit messages) is in the root [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Planned

Written when first needed:

- **conventions.md:** code style, naming, config files, tests and their markers.
- **results-format.md:** what a run folder holds; what goes into `results/`.
- **learning-log.md:** one entry per implementation step: concept, code, gotchas.
