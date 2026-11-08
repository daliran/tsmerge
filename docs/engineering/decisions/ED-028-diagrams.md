# ED-028 — Diagrams: Mermaid sources, committed PNG images, rendered with Docker

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author
- **History:**
  - 2026-11-08: pictures moved beside the docs that show them: each doc folder has an `assets/` folder (`docs/assets/`, `docs/engineering/assets/`, `.claude/assets/`, and one beside each knowledge folder with figures under `docs/research/knowledge/`), with one `rendered.sha256` per folder; `scripts/render_diagrams.sh` finds them all. Was: one central `docs/engineering/diagrams/` folder.

## Problem

The docs explain the structure and the flows (machines, storage, a run's life, decisions) only in text. Diagrams make them faster to understand, but they need:

- a source that can be reviewed in a diff and read by AI agents;
- an image that shows in every viewer: GitHub, VS Code, Obsidian, a future PDF;
- a way to keep the image from drifting away from its source.

## Options

### Format

| | 1 — Mermaid inline in Markdown | 2 — Mermaid source + PNG | 3 — Mermaid source + SVG |
|---|---|---|---|
| Shows in | GitHub, Obsidian; VS Code with an extension | every viewer | every viewer, text may render slightly differently |
| Render step | none | yes | yes |
| Repository cost | none | about 50–150 KB of binary per diagram | smaller, text |
| Can drift from source | no | yes, unless checked | yes, unless checked |

### Renderer (for 2 and 3)

- **Node.js + `@mermaid-js/mermaid-cli`:** needs Node 22.13 or newer (Ubuntu 24.04's apt has 18.19), a Chrome download of about 280 MB, and system libraries that differ between machines.
- **Docker image `minlag/mermaid-cli`:** about 1 GB, bundles Node, Chromium and fonts; needs Docker (Engine on Linux, Desktop on Windows).
- **An online renderer:** sends the diagrams to an external service.

## Decision

- **Format 2:** each diagram is a `.mmd` source with its rendered `.png`, both committed, in the `assets/` folder beside the docs that show them ([docs/README.md](../../README.md#assets)); the docs embed the PNG and link the source.
- **Renderer: Docker,** with the image pinned by version and digest (`minlag/mermaid-cli:12.0.0`) in `scripts/render_diagrams.sh`: the same image on every machine, with nothing else to install.
- **Drift check without Docker:** rendering records each source's SHA-256 in `rendered.sha256`; `scripts/check.sh` fails when a source changed since its last render. So committing other changes never needs Docker.

## Consequences

- Changing a diagram needs Docker ([setup.md](../setup.md#8-diagrams-optional)); reading the docs doesn't.
- The image's Chromium runs without its sandbox (`--no-sandbox`, set inside the image): acceptable, because it renders only our own diagram sources.
- PNGs are binary: review a diagram change through its `.mmd` diff.

## Revisit if

- Docker becomes unavailable where diagrams are edited (then: Node, option above);
- the PNGs grow large or numerous enough to weigh on the repository (then: SVG);
- GitHub, VS Code and the PDF toolchain all render Mermaid natively (then: format 1).
