"""Mechanical repository checks for the expert review: things with right or wrong
answers.

usage: python3 check_hygiene.py <run dir>

Checks every file git would commit (tracked, plus untracked files not ignored) for:
- personal data: the patterns in PRIVATE_PATTERNS (from the git-ignored .env), and
  absolute paths of a personal machine;
- likely secrets;
- Markdown links whose file or heading doesn't exist;
- decision and question ids (PD-, PQ-, DD-, DQ-) with no matching file, and files
  missing from their folder's index;
- common UK spellings, in Markdown files.
Writes <run dir>/checks/hygiene.md.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]

# Personal machine and account paths; the documented placeholder forms (`<user>`,
# `<you>`,
# `<project account>`, ...) pass.
LOCAL_PATHS = re.compile(
    r"/home/(?!<)[a-z_][\w.-]*/"  # Linux home
    r"|/mnt/[a-z]/(?!<)(?!Users/<)"  # a Windows drive seen from WSL
    r"|\b[A-Za-z]:[\\/](?!<)(?!Users[\\/]<)"  # a Windows drive path
    r"|(?<![\w/])/Users/(?!<)"  # macOS home
    r"|/(?:homes|work)/(?!<)[a-z_][\w.-]*/"  # cluster home and work folders
)
SECRETS = re.compile(
    r"(?i)(api[_-]?key|token|password|secret)\s*[=:]\s*['\"]?[A-Za-z0-9/+_-]{12,}"
    # A key file's first line, not a mention of it in prose.
    r"|^-----BEGIN [A-Z ]*PRIVATE KEY-----"
)
LINK = re.compile(r"\]\(([^)#\s]*)(#[^)\s]+)?\)")
ID = re.compile(r"\b((?:PD|PQ|DD|DQ)-\d{3})\b")
# UK spellings, anchored to their British endings so US words (optimistic, organism,
# cancellation, analyses) don't match.
UK = re.compile(
    r"(?i)\b\w*(?:behaviour|colour|favour|honour|licence|centre|catalogue|artefact"
    r"|whilst|amongst"
    r"|(?:organ|recogn|optim|initial|normal|summar|priorit|real|util)is(?:e|ed|es|ing|ation)"
    r"|analys(?:e|ed|ing)"
    r"|(?:travel|model|cancel|label)l(?:ed|ing)"
    r")\b"
)
ID_FOLDERS = {
    "PD": "docs/project/decisions",
    "PQ": "docs/project/questions",
    "DD": "docs/domain/decisions",
    "DQ": "docs/domain/questions",
}


def committable() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return [REPO / p for p in out.splitlines() if (REPO / p).is_file()]


def private_patterns() -> re.Pattern | None:
    env = REPO / ".env"
    if not env.is_file():
        return None
    for line in env.read_text().splitlines():
        if line.startswith("PRIVATE_PATTERNS="):
            value = line.split("=", 1)[1].strip().strip("'\"")
            # The template's placeholder value counts as "not set".
            return (
                re.compile(value, re.IGNORECASE) if value and "<" not in value else None
            )
    return None


def highest_question_ids() -> dict[str, int]:
    """The "highest id used" recorded in each questions index, e.g. {"PQ": 10}."""
    found = {}
    for prefix in ("PQ", "DQ"):
        index = REPO / ID_FOLDERS[prefix] / "README.md"
        if index.is_file():
            m = re.search(
                rf"\*\*Highest id used:\*\* {prefix}-(\d{{3}})", index.read_text()
            )
            if m:
                found[prefix] = int(m.group(1))
    return found


HIGHEST_QUESTIONS = highest_question_ids()


def is_closed_question(question_id: str) -> bool:
    """Closed questions are deleted (PD-016), but their ids, up to the highest id used,
    remain valid in history (e.g. a decision's "Answers:" line)."""
    prefix, number = question_id[:2], int(question_id[3:])
    return prefix in HIGHEST_QUESTIONS and number <= HIGHEST_QUESTIONS[prefix]


def anchors(md: Path) -> set[str]:
    found = set()
    in_code = False
    for line in md.read_text(errors="replace").splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and line.startswith("#"):
            title = re.sub(r"[^\w\s-]", "", line.lstrip("#").strip().lower())
            found.add(title.replace(" ", "-"))
    return found


def strip_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def main() -> None:
    run_dir = Path(sys.argv[1])
    files = committable()
    private = private_patterns()
    issues: dict[str, list[str]] = {
        "Personal data": [],
        "Secrets": [],
        "Links": [],
        "Ids": [],
        "US English": [],
    }

    for file in files:
        rel = file.relative_to(REPO).as_posix()
        try:
            text = file.read_text()
        except UnicodeDecodeError:
            continue
        own_source = file.resolve() == Path(__file__).resolve()
        for n, line in enumerate(text.splitlines(), 1):
            if private and private.search(line):
                issues["Personal data"].append(f"`{rel}:{n}`: matches PRIVATE_PATTERNS")
            if LOCAL_PATHS.search(line) and not own_source:
                issues["Personal data"].append(f"`{rel}:{n}`: absolute personal path")
            if SECRETS.search(line):
                issues["Secrets"].append(f"`{rel}:{n}`: looks like a secret")
        if not rel.endswith(".md"):
            continue
        prose = strip_code_blocks(text)
        for m in LINK.finditer(prose):
            target, anchor = m.group(1), m.group(2)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            dest = (file.parent / target).resolve() if target else file
            if not dest.exists():
                issues["Links"].append(f"`{rel}`: link to missing `{target}`")
            elif anchor and dest.suffix == ".md" and anchor[1:] not in anchors(dest):
                issues["Links"].append(f"`{rel}`: missing heading `{target}{anchor}`")
        for m in ID.finditer(prose):
            folder = REPO / ID_FOLDERS[m.group(1)[:2]]
            if is_closed_question(m.group(1)):
                continue  # answered and deleted: its id stays valid history
            if not list(folder.glob(f"{m.group(1)}-*.md")):
                issues["Ids"].append(
                    f"`{rel}`: `{m.group(1)}` has no file in "
                    f"`{folder.relative_to(REPO)}`"
                )
        for m in UK.finditer(prose):
            issues["US English"].append(f'`{rel}`: "{m.group(0)}"')

    for prefix, folder in ID_FOLDERS.items():
        index = REPO / folder / "README.md"
        if not index.is_file():
            continue
        listed = index.read_text()
        for f in sorted((REPO / folder).glob(f"{prefix}-*.md")):
            if f.name not in listed:
                issues["Ids"].append(
                    f"`{folder}/README.md`: `{f.name}` missing from the index"
                )

    lines = ["# Hygiene check", "", f"{len(files)} files checked.", ""]
    for section, found in issues.items():
        lines += [f"## {section}", ""]
        lines += [f"- {item}" for item in sorted(set(found))] or ["none"]
        lines.append("")
    if private is None:
        lines.insert(
            3,
            "Note: PRIVATE_PATTERNS is not set in `.env`: "
            "personal names were not checked.\n",
        )
    out = run_dir / "checks" / "hygiene.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    total = sum(len(set(v)) for v in issues.values())
    print(f"hygiene: {total} issue(s) -> {out}")


if __name__ == "__main__":
    main()
