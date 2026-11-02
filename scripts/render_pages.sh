#!/usr/bin/env bash
# Render a paper's pages to PNG images, so its distillation note can be written and
# verified from the pages themselves, equations and tables included (PD-034).
# usage: scripts/render_pages.sh [--scale S] <bibkey> [output folder]
#   reads papers/<bibkey>.pdf; writes p01.png, p02.png, … (default: outputs/pages/<bibkey>/)
#   --scale: resolution factor (default 2.2: subscripts and small table cells stay legible;
#   raise it, e.g. 3, for pages that are still hard to read)
# The renderer runs in a temporary uv environment: nothing is added to the project.
set -euo pipefail
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"

scale=2.2
if [[ ${1:-} == --scale ]]; then
  scale=$2
  shift 2
fi
[[ $scale =~ ^[0-9]+([.][0-9]+)?$ ]] || { echo "error: --scale takes a number" >&2; exit 1; }
[[ $# -ge 1 ]] || { echo "usage: $0 [--scale S] <bibkey> [output folder]" >&2; exit 1; }
key=$1
pdf="papers/$key.pdf"
out=${2:-outputs/pages/$key}
[[ -f $pdf ]] || { echo "error: $pdf not found (papers/ holds the PDFs, PD-034)" >&2; exit 1; }
mkdir -p "$out"

uv run --quiet --no-project --with pypdfium2 --with pillow python - "$pdf" "$out" "$scale" <<'PY'
import sys

import pypdfium2 as pdfium

pdf = pdfium.PdfDocument(sys.argv[1])
for i in range(len(pdf)):
    pdf[i].render(scale=float(sys.argv[3])).to_pil().save(f"{sys.argv[2]}/p{i + 1:02d}.png")
print(f"{len(pdf)} pages -> {sys.argv[2]}")
PY
