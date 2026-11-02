#!/usr/bin/env bash
# Show the end of a job's output (its run's output.log), to follow a job while it runs.
# usage: scripts/cluster/logs.sh <job id> [lines]   (default: the last 50 lines)
# The job is looked up in outputs/jobs.log, which submit.sh writes on this machine.
# shellcheck source=common.sh
source "$(dirname "$0")/common.sh"

[[ $# -ge 1 ]] || die "usage: $0 <job id> [lines]"
job_id=$1
lines=${2:-50}
[[ $lines =~ ^[0-9]+$ ]] || die "lines: a number"

load_env
require_connection

# jobs.log columns: job id, run id, experiment, date, command (tab-separated).
record=$(awk -F'\t' -v id="$job_id" '$1 == id { print $2 "\t" $3 }' "$REPO_ROOT/outputs/jobs.log" 2>/dev/null | tail -n 1)
[[ -n $record ]] || die "job $job_id is not in outputs/jobs.log: was it submitted from this machine?"
run_id=${record%%$'\t'*}
experiment=${record#*$'\t'}

log="$CLUSTER_WORK_DIR/runs/$experiment/$run_id/output.log"
echo "== $experiment/$run_id (job $job_id): last $lines lines of output.log"
remote "tail -n $(q "$lines") $(q "$log") 2>/dev/null" \
  || echo "(no output yet: the job may still be waiting in the queue; see scripts/cluster/status.sh $job_id)"
