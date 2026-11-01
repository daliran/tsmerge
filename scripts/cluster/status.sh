#!/usr/bin/env bash
# Show your queued jobs, or the state of one job.
# usage: scripts/cluster/status.sh [<job id>]
# shellcheck source=common.sh
source "$(dirname "$0")/common.sh"
load_env
require_connection

if [[ $# -eq 0 ]]; then
  # $USER is expanded on the cluster, not here.
  # shellcheck disable=SC2016
  remote 'squeue -u $USER'
else
  remote "sacct -j $(q "$1") -X --format=JobID,JobName%30,State,ExitCode,Elapsed,NodeList"
fi
