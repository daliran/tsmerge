# ED-0024 — Large transfers go through the login node, as resumable copies

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author
- **Answers:** question EQ-0010 (opened 2026-11-01, raised by the first expert review, item M20)

## Problem

- Pulling checkpoints and uploading datasets copies large files through the login node. The cluster's documentation names a data-transfer node, `ailb-data.ing.unimore.it`, for large transfers ([cluster.md](../cluster.md#access)).
- An interrupted copy restarted large files from scratch.

## Options

### A — the data-transfer node for large copies

- What the cluster's documentation intends for large transfers.

### B — keep the login node, with resumable copies

- Works from anywhere the login node does.

## Decision

Option B, decided by testing option A (2026-11-02):

- from outside the Unimore network, the data-transfer node's SSH port doesn't answer (the connection times out);
- reaching it through the login node as a jump host is refused: the login node doesn't forward connections;
- so large copies use the login node, and every copy is resumable: `pull.sh` uses `rsync --partial`, and the documented upload command too.

## Consequences

- Large copies take a long session on the login node: `rsync` is light on the node, but run big transfers sparingly.
- Recorded in [cluster.md](../cluster.md#observed-behavior); documented in [running.md](../running.md#datasets).

## Revisit if

- you work from inside the Unimore network or VPN (then the data-transfer node may be reachable: test again);
- the HPC team asks for large transfers to go through the data-transfer node.
