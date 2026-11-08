# Assets of the engineering docs, and how diagrams work

This folder holds the pictures shown in the engineering docs. It's also the reference for **how diagrams work anywhere in the repository**: every `assets/` folder that holds diagrams follows the rules below. The convention itself (one `assets/` folder beside the docs it serves) is in [docs/README.md](../../README.md#assets).

Why this format and renderer: [ED-028](../decisions/ED-028-diagrams.md).

## The diagrams in this folder

| Diagram | What it shows | Shown in |
|---|---|---|
| [machines-and-storage](machines-and-storage.mmd) | Your machine and the cluster: partitions, storage areas, and which script moves what where | [running.md](../running.md#the-model-local-first), [overview.md](../overview.md) |
| [local-run](local-run.mmd) | A recorded local run with `run_local.sh`, and how a quick try or a debug session differs | [running.md](../running.md#running-locally), [overview.md](../overview.md) |
| [cluster-run](cluster-run.mmd) | One cluster run, from `submit.sh` to the pulled results, with how its end is recorded | [running.md](../running.md#the-cycle), [overview.md](../overview.md) |
| [environment-build](environment-build.mmd) | How `setup_remote.sh` builds the cluster environment, and how every job checks it | [running.md](../running.md#the-cluster-environment) |
| [run-statuses](run-statuses.mmd) | The statuses in `run.json`, and what moves a run from one to the next | [runs.md](../runs.md#how-a-run-ended-status), [overview.md](../overview.md) |
| [questions-and-decisions](questions-and-decisions.mmd) | How a question becomes a decision, and how a decision changes over time | [decisions/README.md](../decisions/README.md#rules), [overview.md](../overview.md) |

Diagrams elsewhere: [repository-map](../../assets/repository-map.mmd) in `docs/assets/` (shown in [docs/README.md](../../README.md#contents) and [overview.md](../overview.md)); [expert-review](../../../.claude/assets/expert-review.mmd) in `.claude/assets/` (shown in [.claude/README.md](../../../.claude/README.md#the-expert-review-in-short)).

## How a diagram is stored

- **Source:** a Mermaid file, `<name>.mmd`: plain text, easy to review in a diff, and readable by AI agents.
- **Image:** `<name>.png`, rendered from the source; the docs embed it, so it shows in every viewer.
- **Record:** each `assets/` folder with diagrams has a `rendered.sha256` holding the hash of each source at its last render, so `scripts/check.sh` can tell when a PNG is out of date without rendering anything.

## Keeping them accurate

A diagram that no longer matches the docs misleads more than no diagram. So every time the docs change, check the diagrams that show the same thing (each folder's table says where each is shown): if one is out of date, update its `.mmd` and re-render it in the same change.

`scripts/check.sh` only catches an image that is out of date with its own source; whether the source still matches the docs is up to whoever changes the docs.

## Changing or adding a diagram

1. Edit or create `<name>.mmd` in the `assets/` folder beside the doc that shows it (several docs: their nearest common folder). Start it with a `%%` comment saying what it shows and where it is shown.
2. Render: `scripts/render_diagrams.sh`. It finds the `.mmd` files in every `assets/` folder, needs Docker ([setup.md](../setup.md#8-diagrams-optional)), and renders only the diagrams whose source changed (`--all` renders every one).
3. Embed the image where it belongs, with a link to its source:

   ```markdown
   ![What it shows](assets/<name>.png)

   *Source: [assets/<name>.mmd](assets/<name>.mmd)*
   ```

4. Add it to the table of its folder's README.
5. Commit the `.mmd`, the `.png` and that folder's `rendered.sha256` together.

Without Docker, you can still edit the docs and commit, as long as no `.mmd` changed: the check fails only when a source changed without being rendered.

## Writing Mermaid

- In sequence diagrams, write `<` and `>` as `#lt;` and `#gt;`; in flowchart labels, as `&lt;` and `&gt;`. Otherwise they are read as HTML and disappear.
- **Avoid arrows into groups nested inside other groups:** the default layout then routes them around the whole picture. Keep groups one level deep and let the flow go one way (e.g. left to right). The ELK layout engine, which handles nesting better, isn't included in the pinned renderer image (`layout: elk` is silently ignored).
- Preview while editing: GitHub and Obsidian show Mermaid natively; VS Code needs a Mermaid preview extension. The committed PNG is what readers see.
