#!/usr/bin/env bash
# Unlock everything a working session needs, asking each password once:
# the SSH keys (passphrases) and the shared connection to the cluster (password).
# Safe to rerun: whatever is already unlocked is skipped.
# usage: source scripts/start-session.sh   (sourcing also points this shell at the agent)
#        scripts/start-session.sh          (other terminals find the agent through ~/.bashrc)

_session() {
  local root
  root=$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel) || return 1
  [[ -f "$root/.env" ]] || { echo "error: missing .env: copy .env.example to .env" >&2; return 1; }
  local SSH_KEYS CLUSTER_HOST
  # shellcheck source=/dev/null
  eval "$(grep -E '^(SSH_KEYS|CLUSTER_HOST)=' "$root/.env")"

  # 1. SSH keys: keychain asks only for keys the agent doesn't hold yet.
  # shellcheck disable=SC2086
  eval "$(keychain --eval --quiet ${SSH_KEYS:-})" || return 1

  # 2. Cluster: open the shared connection unless one is already open (asks the password).
  if [[ -n ${CLUSTER_HOST:-} ]]; then
    if ! ssh -O check "$CLUSTER_HOST" 2>/dev/null; then
      echo "opening the connection to $CLUSTER_HOST"
      ssh -fN "$CLUSTER_HOST" || return 1
    fi
  fi

  # 3. Summary.
  echo
  echo "keys loaded:"
  ssh-add -l | sed 's/^/  /'
  if ssh -o BatchMode=yes -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "github:  ok"
  else
    echo "github:  NOT reachable"
  fi
  if [[ -n ${CLUSTER_HOST:-} ]]; then
    if ssh -O check "$CLUSTER_HOST" 2>/dev/null; then
      echo "cluster: connected ($CLUSTER_HOST; it stays open until 8 h without use or a network drop, then rerun this script)"
    else
      echo "cluster: NOT connected"
    fi
  fi
}

_session
_session_status=$?
unset -f _session
# Only exit when run as a script; when sourced, return to the caller's shell.
(return 0 2>/dev/null) && return $_session_status || exit $_session_status
