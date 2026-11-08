#!/usr/bin/env bash
# Render the Mermaid diagrams of every assets/ folder (docs/**/assets/, .claude/assets/)
# to PNG, with Docker (ED-028).
# usage: scripts/render_diagrams.sh           render every diagram whose source changed
#        scripts/render_diagrams.sh --all     render every diagram
#        scripts/render_diagrams.sh --check   only check that every PNG is up to date
#                                             (no Docker needed; run by scripts/check.sh)
# Each assets/ folder keeps a rendered.sha256 with the hash of each of its sources at
# their last render, so the check knows whether a PNG matches its current source
# without rendering anything.
set -euo pipefail
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"

# The renderer, pinned by version and digest: the same input always gives the same image.
image="minlag/mermaid-cli:12.0.0@sha256:fa995339034aae7e5cd4f61482248b7f5c51be355b1a6f6eda11a2bbf8401f5f"

mode=${1:-changed}
# Every assets/ folder that holds at least one Mermaid source.
mapfile -t dirs < <(find docs .claude -type f -path '*/assets/*.mmd' -printf '%h\n' | sort -u)

current() { sha256sum "$1" | cut -d' ' -f1; }
# The source's hash as recorded at its last render; empty if never rendered.
recorded() {
  local manifest
  manifest="$(dirname "$1")/rendered.sha256"
  if [[ -f $manifest ]]; then awk -v f="$(basename "$1")" '$2 == f { print $1 }' "$manifest"; fi
}
up_to_date() { [[ -f ${1%.mmd}.png && $(recorded "$1") == "$(current "$1")" ]]; }

if [[ $mode == --check ]]; then
  stale=()
  for dir in "${dirs[@]}"; do
    for src in "$dir"/*.mmd; do
      up_to_date "$src" || stale+=("$src")
    done
  done
  if [[ ${#stale[@]} -gt 0 ]]; then
    echo "diagrams not rendered since their last change: ${stale[*]}" >&2
    echo "render them with scripts/render_diagrams.sh, and commit each .mmd with its .png" >&2
    exit 1
  fi
  exit 0
fi

if ! docker info >/dev/null 2>&1; then
  echo "error: Docker isn't available: see docs/engineering/setup.md#8-diagrams-optional" >&2
  exit 1
fi

for dir in "${dirs[@]}"; do
  for src in "$dir"/*.mmd; do
    [[ $mode == --all ]] || ! up_to_date "$src" || continue
    name=$(basename "$src" .mmd)
    echo "rendering $dir/$name"
    # Your user id, so the PNG belongs to you; white background and double scale, so it
    # reads well in light and dark viewers and on high-resolution screens.
    docker run --rm -u "$(id -u):$(id -g)" -v "$PWD/$dir:/data" "$image" \
      -i "$name.mmd" -o "$name.png" -b white -s 2 >/dev/null
  done
  # Rewrite the folder's record from the sources whose PNG exists, in a stable order.
  for src in "$dir"/*.mmd; do
    if [[ -f ${src%.mmd}.png ]]; then echo "$(current "$src")  $(basename "$src")"; fi
  done | sort -k2 >"$dir/rendered.sha256"
done
echo "diagrams up to date"
