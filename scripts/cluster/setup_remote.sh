#!/usr/bin/env bash
# Prepare the cluster: create the folders and build the Python environment from uv.lock.
# Run once, and again whenever uv.lock or your uv version changes.
# usage: scripts/cluster/setup_remote.sh
# shellcheck source=common.sh
source "$(dirname "$0")/common.sh"
load_env
require_connection

code="$CLUSTER_HOME_DIR/code"
venv="$CLUSTER_HOME_DIR/venv"

echo "creating folders"
remote "mkdir -p $(q "$code" "$CLUSTER_WORK_DIR/runs" "$CLUSTER_WORK_DIR/tmp" "$CLUSTER_WORK_DIR/data")"

remote 'test -x ~/.local/bin/uv' \
  || die "uv is not installed on the cluster: ssh $CLUSTER_HOST 'curl -LsSf https://astral.sh/uv/install.sh | sh'"

# Same uv version as this machine, so both read uv.lock the same way.
uv_version=$(uv --version | cut -d' ' -f2)
echo "setting the cluster's uv to $uv_version"
remote "\$HOME/.local/bin/uv self update $(q "$uv_version")"

echo "copying the code to $code"
send_code "$code"

# uv's cache holds every package unpacked, as thousands of small files. Here it exists only
# during the build, in a temporary folder on the login node's local disk, deleted at the end:
# nothing is left in /homes, which limits the number of files, or on /work (ED-005).
# --locked refuses a uv.lock that doesn't match pyproject.toml, instead of installing it.
# The hash file lets each job check that it runs against the environment of its own uv.lock.
# It is deleted before the build and written only after it succeeds: during a rebuild, or
# after a failed one, no hash matches, so every job refuses instead of running on a
# half-updated environment.
# The build takes a few minutes, too long to run directly on a shared login node, so it
# runs as a Slurm step on all_serial: still the login nodes, with their local /tmp, but
# scheduled, and free of charge (ED-008). Variables inside build_cmd are expanded on the
# node, not here.
build_cmd="rm -f $(q "$venv/.uv-lock.sha256") \
  && cache=\$(mktemp -d /tmp/tsmerge-uv-cache.XXXXXX) && trap 'rm -rf \"\$cache\"' EXIT \
  && cd $(q "$code") \
  && UV_CACHE_DIR=\"\$cache\" UV_PROJECT_ENVIRONMENT=$(q "$venv") \$HOME/.local/bin/uv sync --locked \
  && sha256sum uv.lock | cut -d' ' -f1 > $(q "$venv/.uv-lock.sha256")"

echo "building the environment in $venv, as a Slurm step on all_serial" \
  "(downloads about 2.5 GB when packages change)"
remote "srun --partition=all_serial --account=$(q "$CLUSTER_ACCOUNT") --job-name=tsmerge-setup \
  --cpus-per-task=4 --time=00:30:00 bash -c $(q "$build_cmd")"

echo "done: environment built from uv.lock $(sha256sum "$REPO_ROOT/uv.lock" | cut -c1-12)"
