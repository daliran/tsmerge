#!/usr/bin/env bash
# shellcheck disable=SC2317  # finish runs from `trap`, which shellcheck can't follow
# Run one command as a recorded local run: the same run folder and records as a cluster
# run, in outputs/runs/ (ED-029).
# usage: scripts/run_local.sh <experiment> <command> [args...]
#   e.g. scripts/run_local.sh hello python -m tsmerge.hello
# Optional, for one run: SWEEP=<id>, INPUTS="<exp>/<run id> ..." (as for submit.sh).
# The command runs from a frozen copy of the code, so you can keep editing while it runs;
# the copy is deleted at the end (commit + provenance/patch.diff rebuild it).
# Ctrl-C stops the run and records it as canceled.
# shellcheck source=cluster/common.sh
source "$(dirname "$0")/cluster/common.sh"

[[ $# -ge 2 ]] || die "usage: $0 <experiment> <command> [args...]"
experiment=$1
shift
[[ $experiment =~ ^[a-z0-9][a-z0-9_-]*$ ]] \
  || die "experiment name: lowercase letters, digits, '-' and '_' only"
sweep=${SWEEP:-}
[[ -z $sweep || $sweep =~ ^[a-z0-9][a-z0-9_-]*$ ]] \
  || die "SWEEP: lowercase letters, digits, '-' and '_' only"
read -r -a inputs <<<"${INPUTS:-}"
for input in "${inputs[@]}"; do
  [[ $input =~ ^[a-z0-9][a-z0-9_-]*/[0-9]{8}-[0-9]{6}-[0-9a-f]{4}$ ]] \
    || die "INPUTS: each entry is <experiment>/<run id>, got '$input'"
done

cd "$REPO_ROOT" || exit
# DATA_DIR may be set in .env (ED-020); nothing else from it is needed here.
# Read in a separate shell, so nothing else from .env leaks into this script.
if [[ -f .env ]]; then
  # shellcheck disable=SC2016  # expanded by the inner shell, after sourcing .env
  data_dir=$(bash -c 'set -a && source .env && echo "${DATA_DIR:-}"')
fi
export DATA_DIR=${data_dir:-$REPO_ROOT/data}
export RUNS_ROOT=${RUNS_ROOT:-$REPO_ROOT/outputs/runs}

commit=$(git rev-parse HEAD 2>/dev/null) || die "the repository has no commit yet"
run_id="$(date +%Y%m%d-%H%M%S)-$(od -An -N2 -tx1 /dev/urandom | tr -d ' \n')"
run_dir="$RUNS_ROOT/$experiment/$run_id"

# The environment must match uv.lock: fail now rather than run on outdated packages.
uv sync --locked --quiet || die "the environment doesn't match uv.lock (see the error above)"
python="$REPO_ROOT/.venv/bin/python"

# 1. The run folder: `mkdir` without -p for the run itself, so a run never reuses a folder.
mkdir -p "$RUNS_ROOT/$experiment"
mkdir "$run_dir" || die "run folder $run_dir already exists"
mkdir "$run_dir/provenance"

# 2. Provenance first, then the frozen code, both from the same working tree (ED-007).
working_tree_patch >"$run_dir/provenance/patch.diff" || die "could not record uncommitted changes"
git status --porcelain=v1 -uall >"$run_dir/provenance/git-status.txt"
dirty=false
[[ -s $run_dir/provenance/git-status.txt ]] && dirty=true
git ls-files -z --cached --others --exclude-standard \
  | rsync -a --from0 --files-from=- --ignore-missing-args ./ "$run_dir/code/"

echo "run $run_id ($experiment), commit ${commit:0:7} -> ${run_dir#"$REPO_ROOT"/}"
if $dirty; then
  echo "note: uncommitted changes are recorded in provenance/patch.diff"
fi

# 3. run.json, with the same fields as a cluster run, minus Slurm's (runs.md).
RUN_ID=$run_id EXPERIMENT=$experiment SWEEP_ID=$sweep INPUT_RUNS=${INPUTS:-} COMMIT=$commit \
  DIRTY=$dirty LOCK_HASH=$(sha256sum uv.lock | cut -d' ' -f1) UV_VERSION=$(uv --version | cut -d' ' -f2) \
  "$python" - "$@" >"$run_dir/run.json" <<'PY'
import datetime, json, os, sys

env = os.environ
print(json.dumps({
    "run_id": env["RUN_ID"],
    "experiment": env["EXPERIMENT"],
    "launcher": "local",
    "sweep": env["SWEEP_ID"] or None,
    "inputs": env["INPUT_RUNS"].split(),
    "command": sys.argv[1:],
    "git_commit": env["COMMIT"],
    "git_dirty": env["DIRTY"] == "true",
    "uv_lock_sha256": env["LOCK_HASH"],
    "uv_version": env["UV_VERSION"],
    "slurm": None,
    "submitted_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "status": "submitted",
}, indent=2))
PY

# 4. Run, recording the end whatever happens. Ctrl-C reaches the command too (same
# terminal); the handler only notes it, and the run is recorded as canceled.
stop_reason=""
finish() {
  local code=$?
  "$python" "$REPO_ROOT/scripts/cluster/run_info.py" end "$run_dir/run.json" "$code" \
    ${stop_reason:+"$stop_reason"} || true
  rm -rf "$run_dir/code"
  echo "run $run_id: $(sed -n 's/.*"status": "\(.*\)".*/\1/p' "$run_dir/run.json" | tail -n 1)" \
    "(exit code $code)"
}
trap finish EXIT
trap 'stop_reason=canceled' INT TERM

export RUN_DIR=$run_dir
export PYTHONUNBUFFERED=1
export VIRTUAL_ENV="$REPO_ROOT/.venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"
"$python" scripts/cluster/run_info.py start "$run_dir/run.json"

cd "$run_dir/code"
set +e
"$@" 2>&1 | tee "$run_dir/output.log"
code=${PIPESTATUS[0]}
set -e
exit "$code"
