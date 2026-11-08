#!/usr/bin/env bash
# Copy cluster runs into outputs/runs/, with the same paths. Skips each run's frozen code;
# checkpoints only with --checkpoints.
# usage: scripts/cluster/pull.sh [--checkpoints] [<experiment>[/<run id>]]
# shellcheck source=common.sh
source "$(dirname "$0")/common.sh"

with_checkpoints=false
if [[ ${1:-} == --checkpoints ]]; then
  with_checkpoints=true
  shift
fi
subpath=${1:-}

load_env
require_connection

src="$CLUSTER_WORK_DIR/runs/${subpath:+$subpath/}"
dest="$REPO_ROOT/outputs/runs/${subpath:+$subpath/}"
mkdir -p "$dest"

# Skip only the run folders' own code/ and checkpoints/, not any folder with those names
# deeper inside (e.g. results/code/). Run folders sit at <experiment>/<run id>/ below the
# runs root, so the anchor depends on how deep the requested subpath already is.
case "$subpath" in
  "") anchor="/*/*/" ;;
  */*) anchor="/" ;;
  *) anchor="/*/" ;;
esac
excludes=(--exclude="${anchor}code/")
$with_checkpoints || excludes+=(--exclude="${anchor}checkpoints/")

# --partial: an interrupted copy keeps what it transferred, and resumes from there (ED-0024).
rsync -az --partial "${excludes[@]}" "$CLUSTER_HOST:$src" "$dest"
echo "pulled into ${dest#"$REPO_ROOT"/}"
