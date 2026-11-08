# ED-0005 — On the cluster, uv's cache is temporary, on the login node's local disk

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author

## Context

**The problem.** The first build of the environment on the Unimore cluster (`setup_remote.sh`) failed twice with `Disk quota exceeded` in the home folder, while uv was unpacking PyTorch.

- **Space was not the cause:** about 25 of 100 GB were used.
- **The number of files is the likely cause:** the home held about 186,000 files when the build failed, and the failure always came while *creating* files. `squota` reports usage in "chunks" but shows no limit for them, and the documentation states no file limit. A limit on the number of files is therefore a **hypothesis**, consistent with every observation but not confirmed.

**Why uv creates so many files there.** uv keeps every downloaded package **unpacked** in its cache (17,165 small files for this project's environment). On the cluster's home file system uv **copies** files from the cache into the environment instead of linking them, so every installed file existed twice: once in the cache, once in the environment.

**When the cache is used.** Only while installing packages: `uv sync` in `setup_remote.sh`, on the login node, once per change of `uv.lock` or of uv. Jobs never use it: they run the environment's Python directly.

**Immediate fix:** `uv cache prune` removed 50,170 unused files (11 GB); the build then succeeded.

## Options

### A — the cache in `/work`

- Fast rebuilds; nothing in the home.
- About 17,000 small files on `/work` (BeeGFS), which the cluster documentation asks to avoid, counting against the project's quota.

### B — a temporary cache on the login node's local disk

- `setup_remote.sh` creates a temporary folder in the login node's `/tmp` (a local disk, 71 GB free), uses it as uv's cache for the build, and deletes it at the end.
- **No files left** on any shared storage.
- Each rebuild downloads the packages again (about 2.5 GB); rebuilds are rare.

### C — the cache in the home (uv's default)

- Fast rebuilds.
- Thousands more files in the home with every package: what caused the failure.

## Decision

Option B.

## Consequences

- The home holds only the environment itself (about 17,600 files now), not a second copy of it.
- A rebuild takes a few minutes longer for the downloads.
- The file-count limit of `/homes` stays a hypothesis until the HPC helpdesk confirms it ([EQ-0012](../questions/EQ-0012-home-file-limit.md)); [cluster.md](../cluster.md#observed-behavior) records the observation.
- Other things in the cluster home add to the file count and are not managed by this repository (VS Code's server, other projects, other caches): see [cluster.md](../cluster.md#observed-behavior).

## Revisit if

- the HPC helpdesk confirms or rules out the file-count limit on `/homes`;
- rebuilds become frequent enough that downloading 2.5 GB each time hurts.
