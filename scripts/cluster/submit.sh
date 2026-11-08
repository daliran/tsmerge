#!/usr/bin/env bash
# Submit one run to the cluster: freeze the code in a new run folder, then sbatch it.
# usage: scripts/cluster/submit.sh <experiment> <command> [args...]
#   e.g. scripts/cluster/submit.sh hello python -m tsmerge.hello
# Optional, for one submission:
#   SWEEP=<id>             group this run with others of the same sweep (recorded in run.json)
#   INPUTS="<exp>/<run id> ..."  the earlier runs whose outputs this run reads (recorded in
#                          run.json; the job finds them under RUNS_ROOT)
#   CLUSTER_PROFILE=cpu    a CPU-only job, on all_serial by default (ED-0022)
#   CLUSTER_TIME=04:00:00  override a default from defaults.sh
#   SBATCH_OPTS="--mem=32G" add any other sbatch option
# Don't edit files while a submission runs (a few seconds): the run records the working
# tree as it was when the submission started.
# shellcheck source=common.sh
source "$(dirname "$0")/common.sh"

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

# Extra sbatch options are split into words here, on your machine, and each is passed
# quoted, so the cluster's shell never interprets characters like `$` or `;` in them.
read -r -a extra_opts <<<"${SBATCH_OPTS:-}"
extra_quoted=""
if [[ ${#extra_opts[@]} -gt 0 ]]; then
  extra_quoted=$(q "${extra_opts[@]}")
fi

load_env
require_connection

# GPU jobs get a GPU, the allowed GPU models, and a GPU check in the job; CPU-only jobs
# get none of these, and their own partition (defaults.sh).
case $CLUSTER_PROFILE in
  gpu)
    check_gpu_features
    partition=$CLUSTER_PARTITION
    gpus=$CLUSTER_GPUS
    constraint=$(gpu_constraint)
    gpu_quoted=$(q --constraint="$constraint" --gres="gpu:$gpus")
    ;;
  cpu)
    partition=$CLUSTER_CPU_PARTITION
    gpus=0
    constraint=""
    gpu_quoted=""
    ;;
  *) die "CLUSTER_PROFILE: 'gpu' or 'cpu', got '$CLUSTER_PROFILE'" ;;
esac
cd "$REPO_ROOT" || exit

commit=$(git rev-parse HEAD 2>/dev/null) || die "the repository has no commit yet"
run_id="$(date +%Y%m%d-%H%M%S)-$(od -An -N2 -tx1 /dev/urandom | tr -d ' \n')"
run_dir="$CLUSTER_WORK_DIR/runs/$experiment/$run_id"

# --- If the submission fails --------------------------------------------------------------
# Once the run folder exists on the cluster, a later failure (sbatch rejects the job, the
# budget is spent, the connection drops) would leave a folder marked "submitted" with no
# job. So until the job is accepted, a failure deletes the run folder (only if its path is
# inside the runs area) and says which step failed.
step="preparing"
folder_created=false
patch_file=$(mktemp)
status_file=$(mktemp)
on_exit() {
  local code=$?
  rm -f "$patch_file" "$status_file"
  if [[ $code -ne 0 && $folder_created == true ]]; then
    echo "error: submission failed while $step; removing the run folder $run_dir" >&2
    if [[ $run_dir == "$CLUSTER_WORK_DIR/runs/$experiment/$run_id" && -n $run_id ]]; then
      remote "rm -rf $(q "$run_dir")" || echo "error: could not remove $run_dir" >&2
    fi
  fi
}
trap on_exit EXIT

# --- What the run is made of, captured first ----------------------------------------------
# The uncommitted changes are captured before anything is sent, so the dirty flag and the
# patch describe the same moment.
step="recording uncommitted changes"
git status --porcelain >"$status_file"
working_tree_patch >"$patch_file"
dirty=false
[[ ! -s $status_file ]] || dirty=true

echo "run $run_id ($experiment), commit ${commit:0:7}"
# A commit that was never pushed can disappear (amended, rebased): then run.json would
# point to nothing. Checked against the remote-tracking branches, without contacting GitHub.
if git remote get-url origin >/dev/null 2>&1 && [[ -z $(git branch -r --contains "$commit" 2>/dev/null) ]]; then
  echo "warning: commit ${commit:0:7} isn't pushed yet: push it, so this run's commit can't" \
    "disappear (ED-0025)." >&2
fi
if [[ $dirty == true ]]; then
  echo "warning: uncommitted changes: this run can be rebuilt only from commit ${commit:0:7}" \
    "plus provenance/patch.diff. Commit first for a run that is exactly a commit." >&2
fi

# 1. Create the run folder. `mkdir` without -p for the run itself: it fails if the folder
# already exists, so a run can never silently reuse another run's folder.
step="creating the run folder"
remote "mkdir -p $(q "$CLUSTER_WORK_DIR/runs/$experiment") && mkdir $(q "$run_dir") \
  && mkdir $(q "$run_dir/code" "$run_dir/provenance")"
folder_created=true

# 2. Freeze the code this run uses, and record every difference from the commit, new files
# included, in provenance/: outside code/, so pull.sh brings it back (ED-0007).
step="copying the code"
send_code "$run_dir/code"
remote "cat > $(q "$run_dir/provenance/patch.diff")" <"$patch_file"
remote "cat > $(q "$run_dir/provenance/git-status.txt")" <"$status_file"

# 3. Keep the mirror equal to the latest submitted code, for remote debugging.
step="updating the code mirror"
remote "mkdir -p $(q "$CLUSTER_HOME_DIR/code") && rsync -a --delete $(q "$run_dir/code/" "$CLUSTER_HOME_DIR/code/")"

# 4. What is known at submit time; the job adds the rest (scripts/cluster/run_info.py).
# "slurm" records the options this job actually gets, overrides included: sacct's records
# expire, and the time limit explains why a run stopped.
step="writing run.json"
RUN_ID=$run_id EXPERIMENT=$experiment SWEEP_ID=$sweep INPUT_RUNS=${INPUTS:-} COMMIT=$commit DIRTY=$dirty \
  LOCK_HASH=$(sha256sum uv.lock | cut -d' ' -f1) UV_VERSION=$(uv --version | cut -d' ' -f2) \
  S_PROFILE=$CLUSTER_PROFILE S_ACCOUNT=$CLUSTER_ACCOUNT S_PARTITION=$partition S_CONSTRAINT=$constraint \
  S_NODES=$CLUSTER_NODES S_NTASKS=$CLUSTER_NTASKS S_GPUS=$gpus S_CPUS=$CLUSTER_CPUS S_TIME=$CLUSTER_TIME \
  S_SIGNAL=$CLUSTER_SIGNAL S_REQUEUE=$CLUSTER_REQUEUE S_EXTRA=${SBATCH_OPTS:-} \
  uv run --no-project python - "$@" <<'PY' | remote "cat > $(q "$run_dir/run.json")"
import datetime, json, os, sys

env = os.environ
print(json.dumps({
    "run_id": env["RUN_ID"],
    "experiment": env["EXPERIMENT"],
    "launcher": "cluster",
    "sweep": env["SWEEP_ID"] or None,
    "inputs": env["INPUT_RUNS"].split(),
    "command": sys.argv[1:],
    "git_commit": env["COMMIT"],
    "git_dirty": env["DIRTY"] == "true",
    "uv_lock_sha256": env["LOCK_HASH"],
    "uv_version": env["UV_VERSION"],
    "slurm": {
        "profile": env["S_PROFILE"],
        "account": env["S_ACCOUNT"],
        "partition": env["S_PARTITION"],
        "constraint": env["S_CONSTRAINT"] or None,
        "nodes": env["S_NODES"],
        "ntasks": env["S_NTASKS"],
        "gpus": env["S_GPUS"],
        "cpus_per_task": env["S_CPUS"],
        "time": env["S_TIME"],
        "signal": env["S_SIGNAL"],
        "requeue": env["S_REQUEUE"] == "true",
        "extra_options": env["S_EXTRA"] or None,
    },
    "submitted_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "status": "submitted",
}, indent=2))
PY

# 5. Submit, with every Slurm option from defaults.sh and .env.
# Values reach the job as arguments: an explicit --export gets jobs canceled.
step="submitting the job (sbatch)"
job_id=$(remote "cd $(q "$run_dir") && sbatch --parsable \
  $(q --job-name="$experiment" --account="$CLUSTER_ACCOUNT" --partition="$partition" \
      --nodes="$CLUSTER_NODES" --ntasks="$CLUSTER_NTASKS" --cpus-per-task="$CLUSTER_CPUS" \
      --time="$CLUSTER_TIME" --signal="$CLUSTER_SIGNAL" --output="$run_dir/output.log") \
  $([[ $CLUSTER_REQUEUE == true ]] && echo --requeue || echo --no-requeue) \
  $gpu_quoted \
  $extra_quoted \
  $(q "$run_dir/code/scripts/cluster/job.sbatch" "$run_dir" "$CLUSTER_HOME_DIR/venv" "$CLUSTER_WORK_DIR" \
      "$CLUSTER_PROFILE" "$@")")
folder_created=false # the job exists now: the folder belongs to it

mkdir -p outputs
printf '%s\t%s\t%s\t%s\t%s\n' "$job_id" "$run_id" "$experiment" "$(date -Is)" "$*" >>outputs/jobs.log
echo "submitted job $job_id -> $run_dir"
