# Project questions

Open technical and organizational questions: what we don't know or haven't decided yet about the repository, the environment and the compute setup.

**The goal is zero open questions.** A question exists only while something is undecided: once answered, its content moves into a decision or a doc, and the question file is deleted.

Research questions belong to the domain area. They get `DQ-` ids, in their own folder, created with the first one.

## Rules

- **One file per question:** `PQ-NNN-short-slug.md`.
- **Stable ids:**
  - an id and its file name never change while the question exists;
  - an id is never reused, even after the question is closed and deleted;
  - the next id is the **highest id used** (recorded below the index) plus one.
- **Statuses while open:** `open` → `investigating`.
- **Closing a question.** Only the user closes a question. Then, in the same step:
  1. the answer, its reasons and the options considered go into a decision (`PD-NNN`) or the doc they belong to; if the question is dropped, the reason goes where it will be found (a doc or decision);
  2. every link to the question is updated to point to that decision or doc;
  3. the question file and its index row are deleted.
- **Hypotheses are marked as hypotheses.** Evidence links to sources, results or decisions.
- **Readable:** one idea per line, lists as bullets, options with numbers when they exist.

## Template

```markdown
# PQ-NNN — <the question?>

- **Status:** open | investigating
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

```

## Index

By id.

| Id | Question | Status | Opened |
|---|---|---|---|
| [PQ-012](PQ-012-home-file-limit.md) | Does the cluster's `/homes` limit the number of files? | open | 2026-11-02 |
| [PQ-013](PQ-013-p100-driver.md) | Can the P100 GPUs on `all_serial` run this project's PyTorch? | open | 2026-11-02 |
| [PQ-014](PQ-014-compute-node-internet.md) | Can the cluster's compute nodes reach the internet? | open | 2026-11-02 |

**Highest id used:** PQ-014. The next question takes the number after it, even if earlier questions have been closed and deleted.
