# CLAUDE.md

tsmerge is a master's thesis repo (AI Engineering, Unimore) on joint training vs. task arithmetic (model merging) and other continual strategies for time-series anomaly detection and forecasting.

## Read first

- [README.md](README.md), then the `README.md` of every folder you work in: they describe what the folder holds and how it is used.
- `CLAUDE.local.md` (git-ignored, if present): personal and machine-specific context.
- [docs/engineering/decisions/README.md](docs/engineering/decisions/README.md) and [docs/research/decisions/README.md](docs/research/decisions/README.md): why things are the way they are. Read the relevant decision before changing what it covers.

## Rules

- **Nothing is assumed; the user validates every decision.** Present each proposal with the context needed to understand it fully: what it changes, the options, their consequences and trade-offs. Give a recommendation, then wait for the user's decision. When something is ambiguous, ask instead of guessing.
- **Verify, don't trust memory.** Check facts about external systems (the cluster, libraries, tools) against their official documentation or the system itself, including the user's own statements, and say plainly when something can't be verified.
- **Plan before acting.** Analyze first, present a plan, and act only once the user approves it. Only minor changes skip this: typos, formatting, or an edit the user has just described exactly.
- **Small steps, clean commits.** One concept per change; every commit has one clear purpose. No new dependencies and no cross-module refactors unasked.
- **Humans own git.** Only read-only git (`status`, `diff`, `log`, `show`). Propose commits with the [commit-plan](.claude/skills/commit-plan/SKILL.md) skill, only when asked; the user runs them. Before proposing a commit, run `scripts/check.sh` ([CONTRIBUTING.md](CONTRIBUTING.md#checks-before-committing)).
- **Nothing machine-specific in committed files:** no paths outside the repo and no personal values (usernames, accounts, hosts): those live in `.env` and `CLAUDE.local.md`; docs use placeholders such as `<username>`.
- **This repo is the source of truth.** Committed files never refer to the private material used to build it: the author's own earlier work and repositories, local files, notes, drafts (the list is in `CLAUDE.local.md`). Public sources (papers, books, official documentation, public code) may be cited and linked; every choice is still justified on its own merits ([ED-0018](docs/engineering/decisions/ED-0018-self-contained-repository.md)).
- **Cluster login nodes are shared.** Run only short, light commands there. Anything long or blocking, Python included, goes through `srun` or `sbatch` ([cluster.md](docs/engineering/cluster.md), [running.md](docs/engineering/running.md)).
- **Code changes only locally**, never on the cluster, wherever the code runs or is debugged.
- **Sources are read-only:** never edit papers or external repositories used as reference.
- **US English** in everything written to the repository. Give bash commands, never PowerShell.
- **Readable Markdown, written for humans.** A blank line between blocks, short paragraphs, one idea per line, and bullet lists for anything that enumerates. Split long sections with headings. When presenting options, give numbers where they exist (counts, percentages, costs) and what each option gains and costs.
- **Folder `CLAUDE.md` files:** none yet. When a folder first needs rules that only agents need, propose adding one there (starting with `@README.md`).
- **Document what and why, as you go.** Every script, configuration file and folder says what it does and why it exists: in the folder's README, a decision, or a short comment. Write it together with the change, not afterwards; a new file also gets its line in the inventory of [docs/engineering/overview.md](docs/engineering/overview.md#every-file-in-the-repository) (a test checks it).
- **Record problems with their solutions.** When a problem is found (a review, a failed run, a bug), write down the problem, why it mattered and how it was solved, in a decision (its Problem section) or as the rule in the relevant doc, not as a dated incident note; what isn't solved yet becomes an open question. Never leave it only in the conversation.
- **Docs are the reference; decisions explain why.** Every operational fact lives in an engineering or research doc, or a folder README, which may link to the decision behind it. A decision is history and rationale, never the only place a fact is written.
- **Describe the present.** Committed files say how things are now: no old paths, names or ids, no "was", "moved from" or dated change logs; the past lives in git history and commit messages. A decision may note a change of its choice (what changed and why), never a move or a rename ([decisions README](docs/engineering/decisions/README.md#rules)). Deleted decisions and questions keep their ids reserved.
- **Docs follow decisions.** When a decision is made or changed, update every Markdown file it affects in the same step: committed files, untracked docs, and `CLAUDE.local.md`. Never leave a file stating something a decision has changed.
- **Diagrams follow the docs.** Every time you update the docs, check whether the pictures that illustrate them still match: each doc folder keeps its pictures, and what generates them, in an `assets/` folder beside it ([docs/README.md](docs/README.md#assets)). If not, update the `.mmd` sources or drawing scripts and regenerate the images (`scripts/render_diagrams.sh` for diagrams) in the same step.
- **Knowledge is written down.** When the user asks you to remember a rule, write it here or in the README it belongs to (personal or machine-specific context: `CLAUDE.local.md`), never only in session memory, so fresh sessions follow it too.
