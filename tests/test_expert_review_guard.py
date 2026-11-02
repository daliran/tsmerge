"""Tests for the expert-review guard hook (.claude/hooks/expert_review_guard.py).

The hook is run as a subprocess, exactly as Claude Code runs it: hook input as JSON on
stdin, exit code 2 to block, 0 to allow.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
GUARD = REPO / ".claude" / "hooks" / "expert_review_guard.py"
REVIEWER = "expert-reviewer"


LOG = Path(tempfile.gettempdir()) / "expert-review-guard-test.log"


def run_guard(event: dict | str) -> int:
    payload = event if isinstance(event, str) else json.dumps(event)
    result = subprocess.run(
        [sys.executable, str(GUARD)],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
        env={
            "CLAUDE_PROJECT_DIR": str(REPO),
            "PATH": "",
            "EXPERT_REVIEW_GUARD_LOG": str(LOG),
        },
    )
    return result.returncode


def bash(command: str, agent: str | None = REVIEWER) -> dict:
    event = {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(REPO)}
    if agent:
        event["agent_type"] = agent
    return event


def write(path: str, agent: str | None = REVIEWER) -> dict:
    event = {"tool_name": "Write", "tool_input": {"file_path": path}, "cwd": str(REPO)}
    if agent:
        event["agent_type"] = agent
    return event


@pytest.mark.parametrize(
    "command",
    [
        "ssh ailb squeue",
        "rsync -az a/ ailb:b/",
        "scp ailb:x .",
        "squeue -u me",
        "sbatch job.sbatch",
        "scripts/cluster/submit.sh hello python x.py",
        "cd scripts && cluster/submit.sh hello x",
        "bash scripts/cluster/pull.sh hello",
        "./scripts/start-session.sh",
        "FOO=1 scripts/cluster/status.sh",
        "echo ok; ssh ailb hostname",
        "echo $(ssh ailb hostname)",
        "timeout 10 ssh ailb true",
    ],
)
def test_blocks_cluster_commands_for_reviewers(command):
    assert run_guard(bash(command)) == 2


@pytest.mark.parametrize(
    "command",
    [
        "grep -c ssh docs/project/cluster.md",
        "cat scripts/cluster/submit.sh",
        "shellcheck -x scripts/cluster/submit.sh scripts/cluster/pull.sh",
        "bash -n scripts/cluster/job.sbatch",
        "scripts/check.sh",
        "uv run --frozen ruff check .",
        "git log --oneline -5 -- scripts/cluster/",
    ],
)
def test_allows_reading_and_checking(command):
    assert run_guard(bash(command)) == 0


def test_ignores_other_agents():
    assert run_guard(bash("ssh ailb hostname", agent=None)) == 0
    assert run_guard(bash("ssh ailb hostname", agent="general-purpose")) == 0


def test_aggregator_is_guarded_too():
    assert run_guard(bash("ssh ailb hostname", agent="expert-review-aggregator")) == 2


def test_writes_only_under_the_review_folder():
    assert run_guard(write(str(REPO / "artifacts/expert-reviews/x/roles/a.md"))) == 0
    assert run_guard(write(str(REPO / "scripts/check.sh"))) == 2
    assert run_guard(write("/tmp/elsewhere.md")) == 2


def test_fails_closed_on_unreadable_input():
    assert run_guard("not json") == 2


def test_logs_every_checked_call():
    LOG.unlink(missing_ok=True)
    run_guard(bash("grep -c ssh docs/project/cluster.md"))
    run_guard(bash("ssh ailb hostname"))
    run_guard(bash("ssh ailb hostname", agent=None))  # not a review agent: not logged
    lines = LOG.read_text().splitlines()
    assert len(lines) == 2
    assert "\tallowed\t" in lines[0] and "\tblocked\t" in lines[1]
