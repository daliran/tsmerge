#!/usr/bin/env bash
# Submit one run to the cluster: freeze the code in a new run folder, then sbatch it.
# usage: scripts/cluster/submit.sh <experiment> <command> [args...]
#   e.g. scripts/cluster/submit.sh hello python scripts/cluster/hello.py
# Extra sbatch options: SBATCH_OPTS="--time=04:00:00" scripts/cluster/submit.sh ...
# shellcheck source=common.sh
source "$(dirname "$0")/common.sh"

[[ $# -ge 2 ]] || die "usage: $0 <experiment> <command> [args...]"
experiment=$1
shift
[[ $experiment =~ ^[a-z0-9][a-z0-9_-]*$ ]] \
  || die "experiment name: lowercase letters, digits, '-' and '_' only"

load_env
require_connection
check_gpu_features
cd "$REPO_ROOT" || exit

commit=$(git rev-parse HEAD 2>/dev/null) || die "the repository has no commit yet"
dirty=false
[[ -z $(git status --porcelain) ]] || dirty=true
run_id="$(date +%Y%m%d-%H%M%S)-$(od -An -N2 -tx1 /dev/urandom | tr -d ' \n')"
run_dir="$CLUSTER_WORK_DIR/runs/$experiment/$run_id"

note=""
[[ $dirty == false ]] || note=", with uncommitted changes"
echo "run $run_id ($experiment), commit ${commit:0:7}$note"

# 1. Freeze the code this run uses, with the uncommitted changes recorded.
remote "mkdir -p $(q "$run_dir/code")"
send_code "$run_dir/code"
git diff HEAD | remote "cat > $(q "$run_dir/code/patch.diff")"
git status --porcelain | remote "cat > $(q "$run_dir/code/git-status.txt")"

# 2. Keep the mirror equal to the latest submitted code, for remote debugging.
remote "mkdir -p $(q "$CLUSTER_HOME_DIR/code") && rsync -a --delete $(q "$run_dir/code/" "$CLUSTER_HOME_DIR/code/")"

# 3. What is known at submit time; the job adds the rest (scripts/cluster/run_info.py).
RUN_ID=$run_id EXPERIMENT=$experiment COMMIT=$commit DIRTY=$dirty \
  LOCK_HASH=$(sha256sum uv.lock | cut -d' ' -f1) \
  python3 - "$@" <<'PY' | remote "cat > $(q "$run_dir/run.json")"
import datetime, json, os, sys

print(json.dumps({
    "run_id": os.environ["RUN_ID"],
    "experiment": os.environ["EXPERIMENT"],
    "command": sys.argv[1:],
    "git_commit": os.environ["COMMIT"],
    "git_dirty": os.environ["DIRTY"] == "true",
    "uv_lock_sha256": os.environ["LOCK_HASH"],
    "submitted_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "status": "submitted",
}, indent=2))
PY

# 4. Submit, with every Slurm option from defaults.sh and .env.
# Values reach the job as arguments: an explicit --export gets jobs cancelled.
# SBATCH_OPTS is left unquoted on purpose, so it splits into separate options.
job_id=$(remote "cd $(q "$run_dir") && sbatch --parsable \
  $(q --job-name="$experiment" --account="$CLUSTER_ACCOUNT" --partition="$CLUSTER_PARTITION" \
      --constraint="$(gpu_constraint)" --nodes="$CLUSTER_NODES" --ntasks="$CLUSTER_NTASKS" \
      --gres="gpu:$CLUSTER_GPUS" --time="$CLUSTER_TIME" --output="$run_dir/slurm.out") \
  ${SBATCH_OPTS:-} \
  $(q "$run_dir/code/scripts/cluster/job.sbatch" "$run_dir" "$CLUSTER_HOME_DIR/venv" "$CLUSTER_WORK_DIR/tmp" "$@")")

mkdir -p outputs
printf '%s\t%s\t%s\t%s\t%s\n' "$job_id" "$run_id" "$experiment" "$(date -Is)" "$*" >> outputs/jobs.log
echo "submitted job $job_id -> $run_dir"
