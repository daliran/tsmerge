# Contributing

How a change gets into this repository: decisions, git, checks and commit messages.

## Decisions and questions come first

- A structural or technical choice gets a decision record: [docs/project/decisions/](docs/project/decisions/README.md).
- Something not known or not decided yet gets a question: [docs/project/questions/](docs/project/questions/README.md).
- When a decision changes something, every document it affects is updated in the same change.

## Git

- People run every git command that changes the repository (`add`, `commit`, `push`, branches). AI agents only read (`git status`, `git diff`, `git log`) and propose commits with the [commit-plan](.claude/skills/commit-plan/SKILL.md) skill: the messages and the exact commands to run.
- The default branch is `main`.
- Small steps: each commit has one clear purpose.
- Never commit `outputs/` (local runs and job records), `.env` (personal values), checkpoints (`*.pt`, `*.pth`, `*.ckpt`) or files over ~5 MB.
- No personal data in committed files: personal names, dates or local paths stay in the git-ignored `CLAUDE.local.md`.

## Checks before committing

One script runs every check; all must pass:

```bash
scripts/check.sh
```

It runs:

- `uv lock --check`: `uv.lock` matches `pyproject.toml` (after changing dependencies, run `uv lock` and commit both files together);
- `uv run --locked ruff check .`: Python lint;
- `uv run --locked ruff format --check .`: Python formatting (fix with `uv run ruff format .`);
- `shellcheck`: the shell scripts and git hooks (settings in `.shellcheckrc`);
- `scripts/render_diagrams.sh --check`: every diagram's PNG matches its current source ([diagrams](docs/project/diagrams/README.md); no Docker needed);
- `uv run --locked pytest`: the tests ("no tests found" passes while there are none).

`--locked` makes every step fail instead of silently rewriting `uv.lock` when it doesn't match `pyproject.toml`.

The ruff rules are explicit in `pyproject.toml` (`E, W, F, I, UP, B, SIM, RUF`, line length 88), so a ruff upgrade can't change what is checked ([PD-012](docs/project/decisions/PD-012-code-checks.md)). `ruff` and `pytest` come with the project's environment (`uv sync`); `shellcheck` is a system package ([setup.md](docs/project/setup.md#1-base-tools)).

### Git hooks: the checks run by themselves

Two versioned hooks in [.githooks/](.githooks/README.md) run on every `git commit`:

- **pre-commit:** runs `scripts/check.sh`; a failure stops the commit.
- **commit-msg:** rejects a subject that isn't a Conventional Commit (below) or is over 72 characters.

They need one command per clone (see [setup.md](docs/project/setup.md#6-the-repository)):

```bash
git config core.hooksPath .githooks
```

- The hooks check the working tree, not only the staged files: an unstaged change can affect the result.
- To skip them once, only when really needed: `git commit --no-verify`.

## Commit messages

Commits follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>
```

- **Types:** `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `style`, `chore`, `revert`.
- **Subject:** imperative, lowercase, no trailing period, at most 72 characters.
- Mention the ids a change adds or answers when they fit, e.g. `docs(decisions): add cluster partition decision (PD-002)`.

The full rules and examples are in the [commit-plan](.claude/skills/commit-plan/SKILL.md) skill.

## In-depth reviews

For a review from several expert viewpoints (Python, ML engineering, HPC/Slurm, reproducibility, research), run `/expert-review` in Claude Code. It writes a verified report to `artifacts/expert-reviews/` (git-ignored) and never touches the cluster. See [.claude/README.md](.claude/README.md).
