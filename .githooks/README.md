# Git hooks

Versioned git hooks. Git runs them automatically once the clone points at this folder (one time per clone):

```bash
git config core.hooksPath .githooks
```

| Hook | Runs on | What it does | Why |
|---|---|---|---|
| `pre-commit` | `git commit`, before the message | Runs `scripts/check.sh` (ruff, shellcheck, pytest); a failure stops the commit | No commit can skip the checks in [CONTRIBUTING.md](../CONTRIBUTING.md#checks-before-committing) |
| `commit-msg` | `git commit`, after the message | Rejects a subject that isn't a Conventional Commit, or is over 72 characters | Keeps the history readable and consistent |

- They check the working tree, not only the staged files: an unstaged change can affect the result.
- To skip them once, only when really needed: `git commit --no-verify`.
