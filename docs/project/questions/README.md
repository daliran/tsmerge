# Project questions

Open technical and organizational questions: what we don't know or haven't decided yet about the repository, the environment and the compute setup.

Research questions belong to the domain area. They get `DQ-` ids, in their own folder, created with the first one.

## Rules

- **One file per question:** `PQ-NNN-short-slug.md`.
- **Stable ids:**
  - an id and its file name never change;
  - an id is never reused;
  - the next id is the highest existing one plus one.
- **Statuses:** `open` → `investigating` → `answered` or `dropped`.
- **A question closes only:**
  - through a decision (`PD-NNN`);
  - or as `dropped: <reason>`.

  Only the user closes a question.
- **Hypotheses are marked as hypotheses.** Evidence links to sources, results or decisions.
- **Docs follow decisions.** When a question closes, update the decision it points to and every Markdown file it affects.
- **Readable:** one idea per line, lists as bullets, options with numbers when they exist.

## Template

```markdown
# PQ-NNN — <the question?>

- **Status:** open | investigating | answered | dropped
- **Opened:** YYYY-MM-DD

## Why it matters

- what depends on the answer.

## Options

- the possible answers, with what each gives and costs (numbers where possible).

## Hypotheses

Not established yet:

- …

## Evidence so far

- links.

## Next action

The smallest step that moves it.

## Resolution

— (when closed: the answer and its decision, PD-NNN, or `dropped: <reason>`)
```

## Index

Open questions first, then by id.

| Id | Question | Status | Opened | Resolution |
|---|---|---|---|---|
| [PQ-001](PQ-001-upgrade-pytorch-cuda-12-6.md) | Upgrade PyTorch to 2.14.1 with CUDA 12.6? | open | 2026-11-01 | — |
| [PQ-002](PQ-002-exclude-high-end-gpus.md) | On `all_usr_prod`, exclude the L40S and A40 nodes too? | open | 2026-11-01 | — |
