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

excludes=(--exclude='code/')
$with_checkpoints || excludes+=(--exclude='checkpoints/')

rsync -az "${excludes[@]}" "$CLUSTER_HOST:$src" "$dest"
echo "pulled into ${dest#"$REPO_ROOT"/}"
