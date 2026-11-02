"""PreToolUse hook for the expert-review subagents: a guardrail, not a security
boundary.

Registered in .claude/settings.json for every tool call, it acts only when the caller is
an expert-review subagent (the `agent_type` field of the hook input); for anyone else it
allows everything. For those subagents it blocks:
- shell commands that run a cluster or network program (ssh, rsync, Slurm, ...) or a
  cluster script (scripts/cluster/*.sh, scripts/start-session.sh, job.sbatch), or a
  script that writes outside the review folder (scripts/run_local.sh,
  scripts/render_diagrams.sh), under any path or through an interpreter;
- Write/Edit tool calls outside outputs/expert-reviews/.

Reading or checking those scripts (grep, cat, shellcheck, bash -n) stays allowed: only
what a command *runs* is checked, not every word in it. Shell redirections (`> file`)
are not inspected. Exit code 2 blocks the call and shows the message to the agent; if
the input can't be parsed, the hook blocks (it fails closed).

Every call it checks for those subagents is logged, allowed or blocked, one line each,
in
outputs/expert-reviews/guard.log: an audit trail, and proof that the hook runs.
"""

import json
import os
import re
import shlex
import sys
from datetime import UTC, datetime
from pathlib import Path

GUARDED_AGENTS = {"expert-reviewer", "expert-review-aggregator"}
ALLOWED_WRITE_ROOT = "outputs/expert-reviews/"
# One line per checked call (git-ignored): EXPERT_REVIEW_GUARD_LOG overrides it, for
# tests.
GUARD_LOG = "outputs/expert-reviews/guard.log"

NETWORK = {"ssh", "scp", "sftp", "rsync"}
SLURM = {
    "sbatch",
    "srun",
    "salloc",
    "squeue",
    "sacct",
    "scancel",
    "sinfo",
    "scontrol",
    "sprio",
    "sstat",
    "sshare",
    "sattach",
    "sbcast",
    "sreport",
    "squota",
    "susage",
    "sexpiration",
}
CLUSTER_SCRIPTS = {
    "submit.sh",
    "setup_remote.sh",
    "pull.sh",
    "status.sh",
    "logs.sh",
    "common.sh",
    "job.sbatch",
    "start-session.sh",
    # Not cluster scripts, but they write outside the review folder (run folders,
    # rendered images) or start Docker: just as off-limits for a read-only review.
    "run_local.sh",
    "render_diagrams.sh",
}
# Programs that run another program given as an argument.
LAUNCHERS = {
    "bash",
    "sh",
    "zsh",
    "source",
    ".",
    "env",
    "exec",
    "command",
    "uv",
    "python",
    "python3",
    "timeout",
    "nohup",
    "nice",
    "time",
    "xargs",
}
SEPARATORS = re.compile(r"\|\||&&|;|\||&|\n|\$\(|`|\(|\)")
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def block(reason: str) -> None:
    print(f"expert-review guard: {reason}", file=sys.stderr)
    sys.exit(2)


def blocked_program(command: str) -> str | None:
    """The first cluster or network program the command would run, if any."""
    for segment in SEPARATORS.split(command):
        try:
            words = shlex.split(segment)
        except ValueError:
            words = segment.split()
        words = [w for w in words if not ASSIGNMENT.match(w)]
        if not words:
            continue
        program = os.path.basename(words[0])
        if program in NETWORK | SLURM | CLUSTER_SCRIPTS:
            return program
        if program in {"bash", "sh", "zsh"} and "-n" in words[1:]:
            continue  # syntax check only: nothing runs
        if program in LAUNCHERS:
            for word in words[1:]:
                name = os.path.basename(word)
                if name in NETWORK | SLURM | CLUSTER_SCRIPTS:
                    return name
    return None


def log(project: Path, event: dict, decision: str, detail: str) -> None:
    """Append one line per checked call to the review log: an audit trail of what the
    review agents did, and proof that the guard runs. Never blocks on its own
    failure."""
    path = Path(os.environ.get("EXPERT_REVIEW_GUARD_LOG") or project / GUARD_LOG)
    line = "\t".join(
        [
            datetime.now(UTC).isoformat(timespec="seconds"),
            event.get("agent_type", "?"),
            event.get("tool_name", "?"),
            decision,
            " ".join(detail.split())[:200],
        ]
    )
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        block("could not read the hook input; blocking to be safe")
    if event.get("agent_type") not in GUARDED_AGENTS:
        sys.exit(0)

    project = Path(
        os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd", ".")
    ).resolve()
    tool = event.get("tool_name", "")
    tool_input = event.get("tool_input") or {}
    detail = tool_input.get("command") or tool_input.get("file_path") or ""

    if tool == "Bash":
        program = blocked_program(tool_input.get("command", ""))
        if program:
            log(project, event, "blocked", detail)
            block(
                f"reviewers never run '{program}': no cluster, network or "
                "cluster-script commands. Write the check under 'Proposed checks' "
                "instead."
            )

    if tool in {"Write", "Edit", "MultiEdit", "NotebookEdit"}:
        path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        target = Path(path).resolve()
        try:
            relative = target.relative_to(project).as_posix()
        except ValueError:
            relative = str(target)
        if not relative.startswith(ALLOWED_WRITE_ROOT):
            log(project, event, "blocked", detail)
            block(f"reviewers write only under {ALLOWED_WRITE_ROOT}, not {relative}")

    log(project, event, "allowed", detail)
    sys.exit(0)


if __name__ == "__main__":
    main()
