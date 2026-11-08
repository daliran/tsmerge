# ED-0016 — Engineering docs split by concern; questions end as decisions or docs

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author

## Problem

- The first engineering docs (then called project docs) mixed reference facts, one-time setup, daily how-to and contribution rules: hard to find things, and the same fact ended up in several places.
- Open points and resolved ones were tracked in different ways (a review record, questions, decisions), duplicating information.
- Decisions taken in conversation were lost unless written down.

## Options

- **A. One file per concern, plus decisions and questions with a clear lifecycle.**
- **B. Fewer, larger files** (e.g. one "compute" doc): fewer files, but mixed concerns.

## Decision

Option A:

| File | Concern |
|---|---|
| [setup.md](../setup.md) | one-time setup: your machine and your cluster account |
| [cluster.md](../cluster.md) | reference facts about the Unimore cluster, independent of our scripts |
| [running.md](../running.md) | daily operation: locally and on the cluster |
| [runs.md](../runs.md) | what a run is and what it records |
| [CONTRIBUTING.md](../../../CONTRIBUTING.md) (root, where GitHub finds it) | how a change gets in: decisions first, git, checks, commit messages |
| [decisions/](README.md) | every relevant decision: problem, options, decision, consequences, when to revisit |
| [questions/](../questions/README.md) | what is still undecided |

- **The goal is zero open questions:** an answered question becomes a decision or part of a doc, and its file is deleted. Ids are never reused.
- **No separate review records:** a review's open points become questions; its solved points become decisions or docs.
- **The root README stays minimal:** it links to these files.
- **Docs are the reference, decisions the rationale:** every operational fact lives in a doc; decisions explain why, and docs link to them.

## Consequences

- Each fact has one home; other files link to it.
- Decisions describe the present: they're updated in place when new information emerges or the choice changes, and deleted when they no longer hold ([decisions README](README.md)).

## Revisit if

- a file grows past what fits its concern, or two files keep needing the same edits.
