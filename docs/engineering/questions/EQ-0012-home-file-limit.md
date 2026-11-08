# EQ-0012 — Does the cluster's `/homes` limit the number of files?

- **Status:** open
- **Opened:** 2026-11-02

## Why it matters

- The first environment build failed with `Disk quota exceeded` while creating files, with about 186,000 files in the home and far below its 100 GB ([ED-0005](../decisions/ED-0005-uv-cache-on-the-cluster.md)).
- If there is a file limit, every new dependency adds files toward it: the environment alone holds about 17,600; a large library could break the next rebuild.
- The answer decides how much room is left, and whether file counts need watching.

## Options

- **A. Ask the HPC helpdesk** for the limit, if any, and how to see current usage against it.
- **B. Measure it ourselves:** create files in a scratch folder until the error appears, then delete them. Gives a number, but loads the shared file system and risks breaking other work in the home meanwhile; not recommended.
- **C. Keep working with the hypothesis:** keep the home's file count low (about 128,000 after the 2026-11-01 cleanup, [cluster.md](../cluster.md#observed-behavior)) and treat a new `Disk quota exceeded` as the signal.

## Hypotheses

Not established yet:

- A limit on the number of files exists, somewhere around 160,000–190,000; `squota` shows usage in "chunks" with no limit, and the documentation states none.

## Evidence so far

- The failure, the cleanup that fixed it, and the current file count: [ED-0005](../decisions/ED-0005-uv-cache-on-the-cluster.md), [cluster.md](../cluster.md#observed-behavior).

## Next action

Write to the HPC helpdesk (option A), with the error and the file counts.
