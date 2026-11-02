"""Save the aggregator's report, returned as text, to <run dir>/report.md, unchanged.

usage: python3 save_report.py <run dir> <aggregator output file>

The harness doesn't let subagents write report files, so the aggregator returns the
report as text. Its output file (the path the Agent tool gives when the aggregator is
launched) is a JSONL transcript. This script takes the last assistant text (or tool-call
input, such as the hand-back message) containing the report's title, and writes it from
the title onward, without passing it through the orchestrator's context.
"""

import json
import sys
from pathlib import Path

TITLE = "# Expert review"


def assistant_texts(transcript: Path) -> list[str]:
    texts = []
    for line in transcript.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = event.get("message") or {}
        content = message.get("content")
        if message.get("role") != "assistant" or not isinstance(content, list):
            continue
        for part in content:
            if part.get("type") == "text":
                texts.append(part["text"])
            # The report usually arrives inside a tool call: the subagent's hand-back.
            elif part.get("type") == "tool_use":
                texts += [
                    v for v in (part.get("input") or {}).values() if isinstance(v, str)
                ]
    return texts


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    run_dir, transcript = Path(sys.argv[1]), Path(sys.argv[2])
    reports = [t for t in assistant_texts(transcript) if TITLE in t]
    if not reports:
        sys.exit(f"no text containing '{TITLE}' in {transcript}")
    report = reports[-1]
    report = report[report.index(TITLE) :].rstrip() + "\n"
    out = run_dir / "report.md"
    out.write_text(report, encoding="utf-8")
    print(f"report: {len(report.splitlines())} lines -> {out}")


if __name__ == "__main__":
    main()
