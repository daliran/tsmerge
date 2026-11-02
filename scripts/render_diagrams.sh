#!/usr/bin/env bash
# Render the Mermaid diagrams of docs/project/diagrams/ to PNG, with Docker (PD-028).
# usage: scripts/render_diagrams.sh           render every diagram whose source changed
#        scripts/render_diagrams.sh --all     render every diagram
#        scripts/render_diagrams.sh --check   only check that every PNG is up to date
#                                             (no Docker needed; run by scripts/check.sh)
# Each source's SHA-256 is recorded in rendered.sha256 when its PNG is rendered, so the
# check knows whether a PNG matches its current source without rendering anything.
set -euo pipefail
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"

dir=docs/project/diagrams
manifest=$dir/rendered.sha256
# The renderer, pinned by version and digest: the same input always gives the same image.
image="minlag/mermaid-cli:12.0.0@sha256:fa995339034aae7e5cd4f61482248b7f5c51be355b1a6f6eda11a2bbf8401f5f"

mode=${1:-changed}
shopt -s nullglob
sources=("$dir"/*.mmd)

# The source's hash as recorded at its last render; empty if never rendered.
recorded() {
  if [[ -f $manifest ]]; then awk -v f="$1" '$2 == f { print $1 }' "$manifest"; fi
}
current() { sha256sum "$1" | cut -d' ' -f1; }
up_to_date() { [[ -f ${1%.mmd}.png && $(recorded "$(basename "$1")") == "$(current "$1")" ]]; }

if [[ $mode == --check ]]; then
  stale=()
  for src in "${sources[@]}"; do
    up_to_date "$src" || stale+=("$(basename "$src")")
  done
  if [[ ${#stale[@]} -gt 0 ]]; then
    echo "diagrams not rendered since their last change: ${stale[*]}" >&2
    echo "render them with scripts/render_diagrams.sh, and commit each .mmd with its .png" >&2
    exit 1
  fi
  exit 0
fi

if ! docker info >/dev/null 2>&1; then
  echo "error: Docker isn't available: see docs/project/setup.md#8-diagrams-optional" >&2
  exit 1
fi

for src in "${sources[@]}"; do
  [[ $mode == --all ]] || ! up_to_date "$src" || continue
  name=$(basename "$src" .mmd)
  echo "rendering $name"
  # Your user id, so the PNG belongs to you; white background and double scale, so it
  # reads well in light and dark viewers and on high-resolution screens.
  docker run --rm -u "$(id -u):$(id -g)" -v "$PWD/$dir:/data" "$image" \
    -i "$name.mmd" -o "$name.png" -b white -s 2 >/dev/null
done

# Rewrite the manifest from the sources whose PNG exists, in a stable order.
for src in "${sources[@]}"; do
  if [[ -f ${src%.mmd}.png ]]; then echo "$(current "$src")  $(basename "$src")"; fi
done | sort -k2 >"$manifest"
echo "diagrams up to date"
