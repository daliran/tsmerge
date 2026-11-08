---
name: commit-plan
description: Check the uncommitted changes and propose a sequence of Conventional Commits with the exact git commands for the user to run. Use when the user asks to prepare, plan, split or write commits or commit messages. Never runs git commands that change the repository.
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git show:*), Bash(git ls-files:*), Bash(git branch:*), Bash(git check-ignore:*), Bash(find:*), Bash(du:*), Read, Grep, Glob
---

# Commit plan

The user owns git in this repository. Your job is to **check and propose** commits, never to make them. The plan is the checkpoint: the user reviews it, then runs the commands one commit at a time.

## Hard rules

- **Read-only git only:** `status`, `diff`, `log`, `show`, `ls-files`, `branch`, `check-ignore`.
  - Never run `add`, `commit`, `restore`, `reset`, `stash`, `checkout`, `switch`, `rm`, `push`, or anything else that changes the index, the working tree, branches or the remote.
- **Don't edit files** while preparing the plan, `.gitignore` included. Report problems in the plan instead of fixing them.
- **Describe only what the diff shows.**
- Only prepare a plan when the user asks for one.

## Steps

1. **Read the project's conventions** in `CLAUDE.md` and the READMEs: commit rules, checks to run, paths that must never be committed. Where they differ from this skill, the project's rules win.
2. **Collect the changes.**
   - `git status --porcelain=v1 -uall`, `git diff --stat`, `git diff`, `git diff --staged`. Read new files directly.
   - `git log --oneline -15` to match existing scopes. With no commits yet, say the first commit is the initial one.
   - Stop early when there is nothing to commit, or when a merge, rebase or cherry-pick is in progress (tell the user to finish or abort it first).
3. **Check** and report each item as clear / flagged / not run (why):
   - the checks the project defines (formatter, linter, fast tests), if any;
   - **private or machine-specific content:** paths outside the repo, personal values, references to the private material used to build the repo (see `CLAUDE.md`);
   - **secrets:** tokens, passwords, keys, `.env` files;
   - **large files:** anything over ~5 MB (`find . -size +5M -not -path './.git/*' -not -path './.venv/*'`);
   - leftover debug output, commented-out code, temporary `TODO`s.
4. **Propose `.gitignore` additions** for untracked files that shouldn't be committed (caches, editor state, local settings, generated output).
   - Check `.gitignore` and `git check-ignore -v <path>` first.
   - If such a file is already tracked, add `git rm --cached <path>`.
   - The user edits `.gitignore`; put a `chore: update gitignore` commit first.
5. **Group into commits.** One commit = one logical change that could be reverted alone. Group by intent, not by file.
   - Split: feature vs refactor vs fix; docs vs code; formatting-only (`style`) vs logic; dependency changes vs behavior changes.
   - Keep together: tests with the code they test; a lockfile with the dependency change that produced it; a source and what is generated from it.
   - Order so every commit leaves the repo consistent: tooling before what uses it, renames before edits.
   - If you can't describe a commit in one short sentence, split it. Don't over-split a handful of related doc edits.
   - For one file split across commits, give `git add -p <path>`; prefer whole files when the split would be fiddly.
6. **Write each message** (format below) and **output the plan** (format below).

## Message format (Conventional Commits 1.0)

```
<type>(<scope>): <subject>
```

- **type:** `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build` (dependencies, packaging), `ci`, `style`, `chore` (repo config, `.gitignore`, `.claude/`, tooling), `revert`. Breaking change: `!` after type/scope.
- **scope** (optional, lowercase): the area touched. Reuse scopes from `git log`.
- **subject:** imperative ("add", not "added"), lowercase start, no trailing period, aim for 50 characters, never more than 72 including the prefix.
- **Title only** by default. Add a short body only when the *why* isn't obvious from the title.
- No `Co-Authored-By` or other attribution lines unless the user asks for them.

| Good | Bad | Why bad |
|---|---|---|
| `feat(merging): add TIES merge` | `feat: added ties.py` | past tense, names the file |
| `test(data): cover window splits` | `Test: Add tests.` | capitalized, trailing period, vague |
| `fix(data): stop val windows overlapping test` | `fix: fix leakage, add model, update deps` | three changes in one |

## Output format

````
## Commit plan (N commits)

Branch: <branch>  ·  Already staged: <none | list>

| # | Message | Files |
|---|---------|-------|
| 1 | `<type>(<scope>): <subject>` | … |

### Checks
| Check | Result |
|---|---|

### 1. <type>(<scope>): <subject>
What changed: <one line>
Files:
- path/one

```bash
git add path/one
git commit -m "<type>(<scope>): <subject>"
```

### Left out on purpose   (omit if empty)
### Warnings              (omit if empty)
````

- Each commit gets **its own command block**, so the user can run and check one at a time. Bash syntax.
- Stage files by explicit path, never `git add .` or `git add -A`.
- After the last commit, a final block with `git status` and `git log --oneline -N`.
- On the default branch with a substantial change, mention that the user may want to branch first; don't add it to the commands.
- Never include `git push` unless asked.
- If the user adjusts the plan, show the **whole** revised plan again. If they have already run some commits, check `git status` and `git log`, then plan only what is left.
