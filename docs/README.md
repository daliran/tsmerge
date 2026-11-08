# Docs

Everything we write lives here. External sources (papers) are kept apart and never edited.

## Knowledge first

Every experiment answers a question, every result supports or refutes a claim, and every structural change has a decision. Each has a stable, grep-able id: never changed, never reused.

| Type | Id |
|---|---|
| Question | `EQ-NNN` (engineering), `DQ-NNN` (domain) |
| Decision | `ED-NNN` (engineering), `DD-NNN` (domain) |
| Experiment | `eNNN-<slug>`, e.g. `e001-joint-vs-merge` ([ED-032](engineering/decisions/ED-032-experiment-ids.md)) |
| Claim | to be defined, with the domain docs |
| Paper | bibkey |

Knowledge flows one way: sources → literature notes → concepts → questions → experiments → results → claims → thesis. Later layers link to earlier ones and never restate them.

## Contents

![The repository's folders, what each holds, and where to start reading](assets/repository-map.png)

*Source: [assets/repository-map.mmd](assets/repository-map.mmd)*

- [engineering/](engineering/README.md): all the technical work around the research: setup, the environment, the Unimore cluster, running and recording runs, checks and tooling, with its decisions (`ED-`) and open questions (`EQ-`).
- [domain/](domain/README.md): what the research is about: the papers and their distillation notes, and later the research questions, experiments and claims.

## Assets

Pictures live **beside the docs that show them**, never in one central folder:

- each doc folder with pictures has an **`assets/`** subfolder, e.g. `docs/engineering/assets/`, `docs/domain/background/assets/`;
- a picture shown by docs in several folders goes in the `assets/` of their nearest common folder (e.g. `docs/assets/` for one shown in `docs/README.md` and `docs/engineering/overview.md`);
- an `assets/` folder holds the pictures **and what generates them** (a Mermaid `.mmd` source, a drawing script), and a short README listing each file, what it shows and where it's shown.

How diagrams are made and checked: [engineering/assets/README.md](engineering/assets/README.md).
