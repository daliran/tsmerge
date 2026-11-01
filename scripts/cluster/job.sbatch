#!/bin/bash
# Generic job: runs one command for one run, from the run's frozen code.
# Submitted by submit.sh, which passes every Slurm option (from defaults.sh and .env):
# nothing is hardcoded here.
# args: <run dir> <venv> <temp root> <command> [args...]
set -euo pipefail

run_dir=$1
venv=$2
tmp_root=$3
shift 3

# Node-local /tmp is shared and can fill up: use a per-job folder on /work instead.
export TMPDIR="$tmp_root/$SLURM_JOB_ID"
mkdir -p "$TMPDIR"
trap 'rm -rf "$TMPDIR"' EXIT

# Refuse to run against an environment built from a different uv.lock.
expected=$(sha256sum "$run_dir/code/uv.lock" | cut -d' ' -f1)
actual=$(cat "$venv/.uv-lock.sha256" 2>/dev/null || echo none)
if [[ $expected != "$actual" ]]; then
  echo "error: the cluster environment was built from a different uv.lock: run scripts/cluster/setup_remote.sh" >&2
  exit 1
fi

export VIRTUAL_ENV="$venv"
export PATH="$venv/bin:$PATH"
export RUN_DIR="$run_dir"
cd "$run_dir/code"

python scripts/cluster/run_info.py start "$run_dir/run.json"

# Stop at once on a GPU this PyTorch build can't run.
if ! python scripts/cluster/check_gpu.py; then
  python scripts/cluster/run_info.py end "$run_dir/run.json" 3
  exit 3
fi

set +e
"$@"
status=$?
set -e
python scripts/cluster/run_info.py end "$run_dir/run.json" "$status"
exit "$status"
