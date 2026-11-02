"""Check every reviewer finding's location and quoted evidence against the repository.

usage: python3 check_citations.py <run dir>

Reads <run dir>/roles/*.md, writes <run dir>/checks/citations.md. A finding is:
- verified: the file exists, the line exists, and the quote is within a few lines of it;
- moved: the quote exists in the file, but far from the cited line;
- unverified: the file, the line or the quote is missing.
"""

import itertools
import re
import sys
from pathlib import Path

FINDING = re.compile(r"^## ([A-Z]+-\d+) · (.+)$", re.MULTILINE)
LOCATION = re.compile(r"^- \*\*Location:\*\* (.+)$", re.MULTILINE)
EVIDENCE = re.compile(r'^- \*\*Evidence:\*\* "(.*)"\s*$', re.MULTILINE)
LOOSE_FINDING = re.compile(r"^##\s+([A-Z]+-\d+)\b", re.MULTILINE)
FIRST_PATH = re.compile(r"`([^`:]+)(?::(\d+))?`")
NEAR = 5


def normalize(text: str) -> str:
    return " ".join(text.split())


def check(repo: Path, location: str, quote: str) -> tuple[str, str]:
    match = FIRST_PATH.search(location)
    if not match:
        return "unverified", "no `path:line` in the location"
    path, line = match.group(1), match.group(2)
    file = repo / path
    if not file.is_file():
        return "unverified", f"file not found: {path}"
    lines = file.read_text(errors="replace").splitlines()
    if line and not 1 <= int(line) <= len(lines):
        return "unverified", f"line {line} beyond the file's {len(lines)} lines"
    needle = normalize(quote.strip("…").strip())
    if not needle:
        return "unverified", "empty evidence"
    hits = [i + 1 for i, text in enumerate(lines) if needle in normalize(text)]
    if not hits:
        return "unverified", "quote not found in the file"
    if line and all(abs(hit - int(line)) > NEAR for hit in hits):
        return "moved", f"quote found at line {hits[0]}, not near {line}"
    return "verified", ""


def main() -> None:
    run_dir = Path(sys.argv[1])
    repo = Path(__file__).resolve().parents[4]
    rows, counts = [], {"verified": 0, "moved": 0, "unverified": 0}
    for role_file in sorted((run_dir / "roles").glob("*.md")):
        text = role_file.read_text(encoding="utf-8")
        # A heading that names a finding id but doesn't match the format is reported,
        # not skipped.
        well_formed = {m.group(1) for m in FINDING.finditer(text)}
        for m in LOOSE_FINDING.finditer(text):
            if m.group(1) not in well_formed:
                counts["unverified"] += 1
                rows.append(
                    f"| {m.group(1)} | {role_file.stem} | unverified "
                    "| malformed heading |"
                )
        starts = [m.start() for m in FINDING.finditer(text)] + [len(text)]
        for start, end in itertools.pairwise(starts):
            block = text[start:end]
            finding_id = FINDING.search(block).group(1)
            location = LOCATION.search(block)
            evidence = EVIDENCE.search(block)
            if not location or not evidence:
                status, note = "unverified", "missing Location or Evidence line"
            else:
                status, note = check(repo, location.group(1), evidence.group(1))
            counts[status] += 1
            rows.append(f"| {finding_id} | {role_file.stem} | {status} | {note} |")

    out = run_dir / "checks" / "citations.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    summary = ", ".join(f"{n} {status}" for status, n in counts.items())
    out.write_text(
        "# Citation check\n\n"
        f"{summary}.\n\n"
        "| Finding | Role | Status | Note |\n|---|---|---|---|\n"
        + "\n".join(rows)
        + "\n"
    )
    print(f"citations: {summary} -> {out}")


if __name__ == "__main__":
    main()
