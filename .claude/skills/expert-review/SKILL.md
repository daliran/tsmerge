---
name: expert-review
description: "In-depth review of the repository by a panel of independent expert reviewers (Python, ML engineering, HPC/Slurm, reproducibility, research), followed by one aggregator that verifies every finding against the files and writes a merged report by severity into outputs/expert-reviews/. Launched manually only, with /expert-review. Read-only on the repository; never touches the cluster."
argument-hint: "[project|all|<path>] [--roles role1,role2] [--max-findings N]"
disable-model-invocation: true
---

# Expert review

A panel of independent reviewers, each playing one expert role, reads the same scope and reports what that expert would find. Scripts check every citation and the repository's hygiene mechanically. A separate aggregator then verifies each finding against the files, merges duplicates, drops what doesn't hold, and writes one report by severity.

The pattern is **find** (independent, in parallel) → **check** (mechanical) → **verify** (one aggregator) → **report**. Reviewers never see each other's output. **Agreement between roles is not evidence:** AI reviewers make correlated errors, so the report ranks by verified impact, not by how many roles raised a point.

## Manual only

Only the user launches this skill, with `/expert-review`. When a change would benefit from it (a new area, a reworked workflow, many changes at once, before relying on a setup), suggest it in one line, with a scope, and let the user launch it.

## Cost

One subagent per role plus the aggregator: 6 with the default `project` set, each reading a large part of the repository. Say so in one line before starting, with the roles.

## Arguments

- **Scope** (first argument, default `project`):
  - `project`: `docs/`, `scripts/`, `tsmerge/`, `tests/`, `.githooks/`, `.claude/`, `.vscode/`, `pyproject.toml`, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`;
  - `all`: the whole repository;
  - a path: only that file or folder, read in the context of what it depends on.
- **`--roles`**: a comma-separated subset of the roles in [references/roles.md](references/roles.md). Without it, the default set for the scope listed there.
- **`--max-findings N`**: the cap per reviewer on Medium and Low findings (default 15). Critical and High are never capped.

## Hard rules

- **Read-only.** Nothing outside the run folder is created, changed or deleted. No git writes, no installs, no `uv sync`. Fixes happen afterwards, only when the user asks.
- **Never the cluster.** No agent, the orchestrator included, runs `ssh`, `scp`, `rsync`, Slurm commands, or anything in `scripts/cluster/` or `scripts/start-session.sh` during a review; nor `scripts/run_local.sh` or `scripts/render_diagrams.sh`, which write outside the run folder. Checks that need the cluster are listed in the report as **proposed checks**, for the user to approve and run.
  - A hook enforces this for the reviewer and aggregator subagents: `.claude/hooks/expert_review_guard.py`, registered in `.claude/settings.json`, acts only when the caller is one of them. It blocks commands that run a cluster or network program or a cluster script, and Write/Edit calls outside `outputs/expert-reviews/`; reading and checking those scripts stays allowed. It inspects command text, so it is a guardrail, not a security boundary: the rules above still apply.
- **Only local, read-only checks** on the repository: reading and searching files, `scripts/check.sh`, linters, short inspections with `python -c`, read-only git, official documentation on the web.
- **Independence.** Every reviewer gets the same scope and the same rules, and nothing else: no other role's output, no hint of expected findings, no conclusions of your own.
- **Evidence or nothing.** Every finding cites `path:line` and quotes one line from it. Unverifiable findings are marked as such, never presented as fact.
- **The project's rules win.** Reviewers judge against `CLAUDE.md`, `CONTRIBUTING.md`, the folder READMEs and the decisions. An accepted decision is not a finding without new evidence; an open question is not a new finding.
- **Keep your context small.** As orchestrator, don't read the role files or the full report: relay the aggregator's summary and the report's path.

## Steps

1. **Prepare the run folder:** `outputs/expert-reviews/<YYYY-MM-DD>-<scope>/` (a path scope uses its last component; add `-2`, `-3`… if it exists), with `roles/` and `checks/`. Write `run.md`: date, scope, roles, cap, and the commit (`git log -1 --oneline`, plus "uncommitted changes" if `git status --porcelain` isn't empty).
2. **Pick the roles:** `--roles`, or the default set for the scope in [references/roles.md](references/roles.md). Tell the user in one line which roles run and how many agents that is.
3. **Hygiene check:** `uv run --locked python .claude/skills/expert-review/scripts/check_hygiene.py <run dir>` writes `checks/hygiene.md`.
4. **Spawn the reviewers, all in one message**, so they run in parallel: one `Agent` call per role, `subagent_type: expert-reviewer`, with the prompt from [references/reviewer-prompt.md](references/reviewer-prompt.md). Fill in the role's brief and id prefix ([references/roles.md](references/roles.md), [references/finding-format.md](references/finding-format.md)), the scope, the cap and the output path `<run dir>/roles/<role>.md`.
5. **Wait** for every reviewer. Don't poll and don't predict results. If one fails, note it in `run.md` and continue with the others.
6. **Citation check:** `uv run --locked python .claude/skills/expert-review/scripts/check_citations.py <run dir>` writes `checks/citations.md`.
7. **Spawn the aggregator:** one `Agent` call, `subagent_type: expert-review-aggregator`, with the prompt from [references/aggregator-prompt.md](references/aggregator-prompt.md) and the run folder. Subagents can't write report files, so it **returns** the report as text, following [references/report-template.md](references/report-template.md), after a short summary: the counts, the five most important items and the number of proposed checks.
8. **Save the report** without reading it into your context: `uv run --locked python .claude/skills/expert-review/scripts/save_report.py <run dir> <aggregator output file>`, where the output file is the path the `Agent` tool gave when the aggregator was launched. It writes `report.md` unchanged.
9. **Check the guard's log:** `outputs/expert-reviews/guard.log` lists every call the review agents made, allowed or blocked. Note in `run.md` how many were blocked, if any, and mention them to the user.
10. **Report to the user:** relay the aggregator's summary, the report's path as a clickable link, the counts by severity, and the proposed checks that need their approval. Offer, in one line, to turn verified findings into fixes, questions (`EQ-NNN`) or decisions; do nothing until the user picks.

## When the Agent tool is unavailable

Run the roles one after another yourself, writing each role file before starting the next and never rereading an earlier one while reviewing; then run the citation check and do the aggregation as a separate pass. Say in `run.md` that the reviewers were not independent.
