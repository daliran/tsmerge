#!/bin/bash
# shellcheck disable=SC2317  # finish and on_signal run from `trap`, which shellcheck can't follow
# Generic job: runs one command for one run, from the run's frozen code.
# Submitted by submit.sh, which passes every Slurm option (from defaults.sh and .env):
# nothing is hardcoded here.
# args: <run dir> <venv> <work dir> <profile: gpu|cpu> <command> [args...]
set -euo pipefail

run_dir=$1
venv=$2
work_dir=$3
profile=$4
shift 4
tmp_root="$work_dir/tmp"

# --- Recording how the run ends --------------------------------------------------------
# run.json must always end with a real status, whatever stops the job (PD-003):
#   completed   the command exited with 0
#   failed      the command, or a check before it, exited with another code
#   timeout     Slurm stopped the job at its time limit
#   canceled    the job was stopped before its time limit (scancel, or a node problem)
#   stopped     Slurm stopped the job, but the reason couldn't be determined
# Slurm doesn't let a killed script finish its last lines, so the end is recorded by:
#   - an exit handler (`trap finish EXIT`), which bash runs whenever this script ends;
#   - a signal handler (`trap … TERM`): Slurm sends TERM to this script 2 minutes before
#     the time limit (--signal=B:TERM@120 in defaults.sh), and on scancel. The handler
#     notes why, stops the command, and exits; the exit handler then writes the record.
# The command itself needs nothing special: it is stopped like any program. (To save a
# checkpoint first, it could catch SIGTERM itself; see docs/project/running.md.)

stop_reason=""  # set by the signal handler: "timeout" or "canceled"
child=""        # the command's process id, once it runs

finish() {
  local code=$?
  # run_info.py's end phase needs only the standard library, so it works even when the
  # environment check failed.
  "$venv/bin/python" "$run_dir/code/scripts/cluster/run_info.py" end \
    "$run_dir/run.json" "$code" ${stop_reason:+"$stop_reason"} || true
  rm -rf "$TMPDIR"
}

# Seconds left before the time limit, from Slurm's "[D-][H:]M:S" format; empty if unknown.
seconds_left() {
  local left d=0 h=0 m=0 s=0 a b c
  left=$(squeue -h -j "$SLURM_JOB_ID" -o %L 2>/dev/null) || return 0
  [[ $left =~ ^[0-9:-]+$ ]] || return 0
  if [[ $left == *-* ]]; then
    d=${left%%-*}
    left=${left#*-}
  fi
  IFS=: read -r a b c <<<"$left"
  if [[ -n $c ]]; then
    h=$a m=$b s=$c
  elif [[ -n $b ]]; then
    m=$a s=$b
  else
    s=$a
  fi
  echo $((10#$d * 86400 + 10#$h * 3600 + 10#$m * 60 + 10#$s))
}

on_signal() {
  # Within 3 minutes of the time limit, it's the timeout warning; earlier, a cancel.
  # If Slurm can't be asked, say so instead of guessing.
  local left
  left=$(seconds_left)
  if [[ -z $left ]]; then
    stop_reason=stopped
  elif ((left <= 180)); then
    stop_reason=timeout
  else
    stop_reason=canceled
  fi
  echo "job: stopping the command ($stop_reason)" >&2
  if [[ -n $child ]]; then
    kill -TERM "$child" 2>/dev/null || true
    wait "$child" 2>/dev/null || true
  fi
  exit 143  # the conventional exit code of a process stopped by TERM
}

# Node-local /tmp is shared and can fill up: use a per-job folder on /work instead.
export TMPDIR="$tmp_root/$SLURM_JOB_ID"
mkdir -p "$TMPDIR"
trap finish EXIT
trap on_signal TERM INT

# --- Checks before running --------------------------------------------------------------

# Refuse to run against an environment built from a different uv.lock.
expected=$(sha256sum "$run_dir/code/uv.lock" | cut -d' ' -f1)
actual=$(cat "$venv/.uv-lock.sha256" 2>/dev/null || echo none)
if [[ $expected != "$actual" ]]; then
  echo "error: the cluster environment was built from a different uv.lock," \
    "or is being rebuilt: run scripts/cluster/setup_remote.sh" >&2
  exit 1
fi

export VIRTUAL_ENV="$venv"
export PATH="$venv/bin:$PATH"
# What the command can rely on (docs/project/runs.md#what-a-run-provides):
#   RUN_DIR    this run's folder: write results/ and checkpoints/ here
#   DATA_DIR   the datasets folder (PD-020)
#   RUNS_ROOT  the root of all runs, to read other runs' outputs listed in "inputs" (PD-021)
export RUN_DIR="$run_dir"
export DATA_DIR="$work_dir/data"
export RUNS_ROOT="$work_dir/runs"
# Python buffers output written to a file: unbuffered, output.log shows progress as it
# happens, and the last lines aren't lost when the job is stopped.
export PYTHONUNBUFFERED=1
cd "$run_dir/code"

python scripts/cluster/run_info.py start "$run_dir/run.json"

# Stop at once on a GPU this PyTorch build can't run (GPU jobs only).
if [[ $profile == gpu ]]; then
  python scripts/cluster/check_gpu.py || exit 3
fi

# --- The run ----------------------------------------------------------------------------
# The command runs in the background while this script waits for it: a waiting script
# can react to Slurm's signal at once, which a script running a command directly can't.
"$@" &
child=$!
set +e
wait "$child"
code=$?
set -e
exit "$code"
