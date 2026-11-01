# shellcheck shell=bash
# Shared helpers for the cluster scripts. Sourced, never run directly.
set -euo pipefail

REPO_ROOT=$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)

# Every ssh and rsync call fails instead of prompting: the shared connection
# must already be open (scripts/start-session.sh).
export RSYNC_RSH="ssh -o BatchMode=yes"

die() {
  echo "error: $*" >&2
  exit 1
}

# Load .env (personal values) and defaults.sh (project settings), and check .env is filled in.
load_env() {
  [[ -f "$REPO_ROOT/.env" ]] || die "missing .env: copy .env.example to .env and fill it in"
  set -a
  # shellcheck source=/dev/null
  source "$REPO_ROOT/.env"
  set +a
  # shellcheck source=defaults.sh
  source "$REPO_ROOT/scripts/cluster/defaults.sh"
  local name
  for name in CLUSTER_HOST CLUSTER_ACCOUNT CLUSTER_HOME_DIR CLUSTER_WORK_DIR; do
    [[ -n "${!name:-}" && "${!name}" != *"<"* ]] || die "$name is not set in .env"
  done
}

require_connection() {
  ssh -O check "$CLUSTER_HOST" 2>/dev/null \
    || die "no open connection to $CLUSTER_HOST: run scripts/start-session.sh first"
}

# Run a command on the cluster's login node. Only light commands belong there.
remote() {
  ssh -o BatchMode=yes "$CLUSTER_HOST" "$@"
}

# Quote arguments so the remote shell receives them unchanged.
q() {
  printf '%q ' "$@"
}

# Copy the working tree to a folder on the cluster: tracked and untracked files,
# without what .gitignore excludes (.env, outputs/, .venv/, ...).
send_code() {
  local dest=$1
  git -C "$REPO_ROOT" ls-files -z --cached --others --exclude-standard \
    | rsync -az --from0 --files-from=- --ignore-missing-args "$REPO_ROOT/" "$CLUSTER_HOST:$dest/"
}

# The allowed GPU features, joined for --constraint.
gpu_constraint() {
  local IFS='|'
  echo "${CLUSTER_GPU_FEATURES[*]}"
}

# Compare the two lists in defaults.sh with the partition's actual GPU models.
# An allowed model that is gone is an error. A model in neither list is new: it is
# reported, so the lists (and PD-001, PQ-002) get reviewed.
check_gpu_features() {
  local available feature missing=() new=()
  local known=" ${CLUSTER_GPU_FEATURES[*]} ${CLUSTER_GPU_EXCLUDED[*]} "
  available=$(remote "sinfo -p $(q "$CLUSTER_PARTITION") -h -o %f" | tr ',' '\n' | grep '^gpu_' | sort -u)
  for feature in "${CLUSTER_GPU_FEATURES[@]}"; do
    grep -qx "$feature" <<<"$available" || missing+=("$feature")
  done
  while read -r feature; do
    [[ $known == *" $feature "* ]] || new+=("$feature")
  done <<<"$available"
  if [[ ${#new[@]} -gt 0 ]]; then
    echo "warning: new GPU models in $CLUSTER_PARTITION, neither allowed nor excluded: ${new[*]}" >&2
    echo "         not used until added to scripts/cluster/defaults.sh (review PD-001 and PQ-002)" >&2
  fi
  [[ ${#missing[@]} -eq 0 ]] \
    || die "allowed GPU models no longer in $CLUSTER_PARTITION: ${missing[*]}: update scripts/cluster/defaults.sh"
}
