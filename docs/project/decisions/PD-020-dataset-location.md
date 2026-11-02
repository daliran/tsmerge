# PD-020 — Datasets live in a data folder outside the code: `data/` locally, the work area on the cluster

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author
- **Answers:** question PQ-004 (opened 2026-11-01, raised by the first expert review, item M10)

## Problem

- Nothing said where datasets go.
- The natural first move, downloading a benchmark into the repository, would have been harmful: `submit.sh` copies every non-ignored file into each run's frozen code and into the cluster's code mirror; the cluster home limits the number of files ([PD-005](PD-005-uv-cache-on-the-cluster.md)), and the work area asks for few large files ([cluster.md](../cluster.md#storage)).
- `config.json` must record each dataset's identity and checksum ([PD-009](PD-009-run-records.md)), so data needs a known, stable location.

## Options

### A — a data folder given by a variable, outside the code that is copied

- Locally and on the cluster, programs read `DATA_DIR`; data never travels with the code.

### B — a `data/` folder inside the repository, used on the cluster too

- Simple locally, but on the cluster it would be inside the code mirror, against the storage rules; a second location would be needed anyway.

## Decision

Option A:

- **locally:** `data/` in the repository, git-ignored; another folder can be set with `DATA_DIR` in `.env`;
- **on the cluster:** `/work/<project account>/<username>/tsmerge/data/`, created by `setup_remote.sh`; every job receives it as `DATA_DIR`;
- datasets are uploaded once, preferably as few large files (archives, HDF5, Parquet);
- `.gitignore` excludes `data/` and common data formats (`*.parquet`, `*.npz`, `*.h5`, `*.hdf5`, `*.safetensors`) anywhere, so data can't be committed or sent with the code by accident.

## Consequences

- Programs read datasets from `DATA_DIR`, never from a path inside the code.
- Large uploads go through the login node, as resumable copies ([PD-024](PD-024-large-transfers.md)).
- Documented in [runs.md](../runs.md#what-a-run-provides) and [running.md](../running.md#datasets).

## Revisit if

- datasets become too large for the 100 GB work quota, or for one upload;
- datasets need versioning beyond a checksum (e.g. several prepared variants).
