# ED-019 — In-depth reviews by a panel of independent expert agents

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author
- **History:**
  - 2026-11-02: reports moved from `artifacts/expert-reviews/` to `outputs/expert-reviews/`: in an ML project "artifacts" suggests model files, and `outputs/` already holds everything generated locally.

## Problem

- A setup like this one (scripts, cluster rules, reproducibility, docs) has failure paths that a single reading misses.
- A review by one AI agent anchors on its own first reading; several agents that see each other's work converge on the same opinions.
- AI reviewers can be confidently wrong: findings must be checked against the files, not trusted.
- Agreement between AI reviewers is not evidence: they make correlated errors (research on multi-judge panels shows several AI judges are worth far fewer independent votes than their number).

## Options

### A — a panel of independent expert roles, then mechanical checks, then one verifying aggregator

- Find (independently, in parallel) → check (scripts) → verify (one aggregator) → report.

### B — a single reviewing agent

- Cheaper, but one viewpoint, and nothing checks its claims.

### C — the built-in `/code-review`

- Reviews a diff for correctness bugs; not role-based, not aware of the project's rules, no saved report. Complementary, not a replacement.

## Decision

Option A, as the `/expert-review` skill ([.claude/README.md](../../../.claude/README.md)):

- **roles are technical experts**, not stakeholders: `python-expert`, `ml-engineer`, `hpc-engineer`, `reproducibility`, `researcher`; later `methodology`, `timeseries`, `merging`, when their material exists;
- each reviewer works independently and must cite `path:line` with a quoted line;
- scripts check every citation and the repository's hygiene (personal data, secrets, links, ids, US English);
- one aggregator verifies every finding against the files, merges duplicates, and ranks by verified impact, never by how many roles raised a point;
- the report goes to `outputs/expert-reviews/` (git-ignored);
- **launched manually only** (`/expert-review`): it starts about 6 agents;
- **read-only, never the cluster:** checks that need the cluster are listed as proposed checks, for the user to approve ([ED-011](ED-011-expert-review-guard.md));
- after a review, its open points become questions and its solved points become decisions or docs ([ED-016](ED-016-engineering-docs.md)).

## Consequences

- The first review (2026-11-01) produced 51 verified items; their solutions are ED-006 to ED-013, ED-020 and ED-021, and the rest became open questions.
- A review costs several agents' worth of tokens: worth it before relying on a setup, after many changes, or for a new area.

## Revisit if

- reviews keep producing mostly dropped or low-value findings (then: fewer roles, or narrower scopes);
- the experiment code exists (then: activate the later roles).
