"""Every file the repository tracks is listed in docs/engineering/overview.md.

The overview ends with an inventory of every file that isn't documentation, so nobody
loses track of what a file is for. This test fails when a file is added without a line
there. Docs, decisions and questions are listed in their own indexes instead, and the
files of every assets/ folder (pictures and what draws them) in that folder's README.
"""

import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
OVERVIEW = REPO / "docs" / "engineering" / "overview.md"


def repository_files() -> list[str]:
    """Tracked files, plus new files git would commit (not ignored)."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("not a git repository")
    return [path for path in out.splitlines() if (REPO / path).exists()]


def needs_listing(path: str) -> bool:
    if path.endswith(".md"):
        return False  # docs: indexed by the folder READMEs
    # Pictures and what generates them: listed in their assets/ folder's README.
    return "assets" not in path.split("/")[:-1]


def test_every_file_is_in_the_overview():
    listed = OVERVIEW.read_text()
    missing = [p for p in repository_files() if needs_listing(p) and p not in listed]
    assert not missing, f"add these to the inventory in {OVERVIEW.name}: {missing}"
