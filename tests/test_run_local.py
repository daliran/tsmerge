"""Tests for scripts/run_local.sh: recorded local runs, as subprocesses (ED-0029)."""

import json
import os
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "run_local.sh"


def run_local(tmp_path: Path, *command: str) -> tuple[int, dict, Path]:
    env = {**os.environ, "RUNS_ROOT": str(tmp_path)}
    result = subprocess.run(
        [str(SCRIPT), "test", *command],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    (run_dir,) = (tmp_path / "test").iterdir()
    return result.returncode, json.loads((run_dir / "run.json").read_text()), run_dir


def test_completed_run_is_recorded(tmp_path):
    code, record, run_dir = run_local(
        tmp_path, "python", "-c", "import os; print(os.environ['RUN_DIR'])"
    )
    assert code == 0
    assert record["status"] == "completed"
    assert record["exit_code"] == 0
    assert record["launcher"] == "local"
    assert record["command"] == [
        "python",
        "-c",
        "import os; print(os.environ['RUN_DIR'])",
    ]
    assert (run_dir / "output.log").read_text().strip() == str(run_dir)
    assert (run_dir / "provenance" / "patch.diff").exists()
    assert not (run_dir / "code").exists(), "the frozen code is removed at the end"


def test_failed_run_keeps_the_exit_code(tmp_path):
    code, record, _ = run_local(tmp_path, "python", "-c", "raise SystemExit(3)")
    assert code == 3
    assert record["status"] == "failed"
    assert record["exit_code"] == 3


def test_command_runs_from_the_frozen_code(tmp_path):
    code, _, run_dir = run_local(
        tmp_path,
        "python",
        "-c",
        "import os, tsmerge; print(os.getcwd(), tsmerge.__file__)",
    )
    assert code == 0
    cwd, package = (run_dir / "output.log").read_text().split()
    assert cwd == str(run_dir / "code")
    assert package.startswith(str(run_dir / "code"))


def test_bad_experiment_name_creates_nothing(tmp_path):
    env = {**os.environ, "RUNS_ROOT": str(tmp_path)}
    result = subprocess.run(
        [str(SCRIPT), "Bad Name", "true"], capture_output=True, env=env, check=False
    )
    assert result.returncode != 0
    assert not any(tmp_path.iterdir())
