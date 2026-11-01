#!/usr/bin/env bash
# Prepare the cluster: create the folders and build the Python environment from uv.lock.
# Run once, and again whenever uv.lock changes.
# usage: scripts/cluster/setup_remote.sh
# shellcheck source=common.sh
source "$(dirname "$0")/common.sh"
load_env
require_connection

code="$CLUSTER_HOME_DIR/code"
venv="$CLUSTER_HOME_DIR/venv"

echo "creating folders"
remote "mkdir -p $(q "$code" "$CLUSTER_WORK_DIR/runs" "$CLUSTER_WORK_DIR/tmp")"

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
# nothing is left in /homes, which limits the number of files, or on /work (PD-005).
# The hash file lets each job check that it runs against the environment of its own uv.lock.
echo "building the environment in $venv (downloads about 2.5 GB when packages change)"
remote "cache=\$(mktemp -d /tmp/tsmerge-uv-cache.XXXXXX) && trap 'rm -rf \"\$cache\"' EXIT \
  && cd $(q "$code") \
  && UV_CACHE_DIR=\"\$cache\" UV_PROJECT_ENVIRONMENT=$(q "$venv") \$HOME/.local/bin/uv sync --frozen \
  && sha256sum uv.lock | cut -d' ' -f1 > $(q "$venv/.uv-lock.sha256")"

echo "done: environment built from uv.lock $(sha256sum "$REPO_ROOT/uv.lock" | cut -c1-12)"
