#!/usr/bin/env bash
# Run every check a commit must pass. Run by hand, and by the pre-commit hook (.githooks/).
# usage: scripts/check.sh
set -uo pipefail
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)" || exit 1

failed=()

step() {
  local name=$1
  shift
  echo "== $name"
  "$@" || failed+=("$name")
}

# pytest exits with 5 when it finds no tests: not a failure while there are none.
pytest_or_none() {
  uv run pytest -q
  local status=$?
  [[ $status -eq 0 || $status -eq 5 ]]
}

step "ruff lint" uv run ruff check .
step "ruff format" uv run ruff format --check .
step "shellcheck" shellcheck -x scripts/*.sh scripts/cluster/*.sh scripts/cluster/job.sbatch .githooks/pre-commit .githooks/commit-msg
step "pytest" pytest_or_none

if [[ ${#failed[@]} -gt 0 ]]; then
  echo "FAILED: ${failed[*]}" >&2
  exit 1
fi
echo "all checks passed"
