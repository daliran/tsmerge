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

# Every difference between the working tree and HEAD, as one binary-safe patch: edits,
# deletions and new (untracked, not ignored) files. It uses a temporary copy of the index,
# so the real staging area is never touched.
working_tree_patch() {
  local index status=0
  index=$(mktemp)
  cp "$(git -C "$REPO_ROOT" rev-parse --git-path index)" "$index" 2>/dev/null || true
  GIT_INDEX_FILE=$index git -C "$REPO_ROOT" add -A || status=$?
  [[ $status -ne 0 ]] || GIT_INDEX_FILE=$index git -C "$REPO_ROOT" diff --cached --binary HEAD || status=$?
  rm -f "$index"
  return "$status"
}

# The GPU features for --constraint: the allowed list, or the subset of it given in
# CLUSTER_GPU_SUBSET for one submission (e.g. one GPU family for a comparable sweep, ED-027).
gpu_constraint() {
  local features=("${CLUSTER_GPU_FEATURES[@]}") feature
  if [[ -n ${CLUSTER_GPU_SUBSET:-} ]]; then
    read -r -a features <<<"$CLUSTER_GPU_SUBSET"
    for feature in "${features[@]}"; do
      [[ " ${CLUSTER_GPU_FEATURES[*]} " == *" $feature "* ]] \
        || die "CLUSTER_GPU_SUBSET: $feature is not an allowed GPU model (defaults.sh)"
    done
  fi
  local IFS='|'
  echo "${features[*]}"
}

# Compare the two lists in defaults.sh with the partition's actual GPU models.
# An allowed model that is gone is an error. A model in neither list is new: it is
# reported, so the lists (and ED-001, ED-027) get reviewed.
check_gpu_features() {
  local available feature missing=() new=()
  local known=" ${CLUSTER_GPU_FEATURES[*]} ${CLUSTER_GPU_EXCLUDED[*]} "
  local listing
  listing=$(remote "sinfo -p $(q "$CLUSTER_PARTITION") -h -o %f") \
    || die "could not read the GPU models of $CLUSTER_PARTITION from the cluster (sinfo failed)"
  available=$(tr ',' '\n' <<<"$listing" | grep '^gpu_' | sort -u || true)
  [[ -n $available ]] \
    || die "no GPU models found in partition $CLUSTER_PARTITION: check its name in defaults.sh"
  for feature in "${CLUSTER_GPU_FEATURES[@]}"; do
    grep -qx "$feature" <<<"$available" || missing+=("$feature")
  done
  while read -r feature; do
    [[ $known == *" $feature "* ]] || new+=("$feature")
  done <<<"$available"
  if [[ ${#new[@]} -gt 0 ]]; then
    echo "warning: new GPU models in $CLUSTER_PARTITION, neither allowed nor excluded: ${new[*]}" >&2
    echo "         not used until added to scripts/cluster/defaults.sh (review ED-001 and ED-027)" >&2
  fi
  [[ ${#missing[@]} -eq 0 ]] \
    || die "allowed GPU models no longer in $CLUSTER_PARTITION: ${missing[*]}: update scripts/cluster/defaults.sh"
}
