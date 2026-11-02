# PD-015 — One session step unlocks SSH keys and the cluster

- **Status:** accepted
- **Date:** 2026-11-01
- **Decided by:** the author

## Problem

- The SSH keys have passphrases, and the cluster asks for a password after the key ([cluster.md](../cluster.md#access)).
- Every new terminal asked for the passphrases again, after each WSL restart.
- Scripts run ssh non-interactively: they can't type a password, so without unlocked keys and an open connection they fail with `Permission denied`.

## Options

### A — terminals never ask; one explicit session step asks for everything once

- A predictable moment for passwords; every terminal and script reuses them.

### B — keep unlocking in every terminal (`keychain` in `~/.bashrc`)

- Automatic, but asks in whichever terminal opens first, and doesn't open the cluster connection.

### C — run the session step automatically when VS Code opens the repository

- Never forgotten, but it prompts even when you only want to read code.

## Decision

Option A:

- `~/.bashrc` uses `keychain --eval --quiet --noask`: terminals join the SSH agent but never prompt;
- **[scripts/start-session.sh](../../../scripts/start-session.sh)** loads the keys listed in `.env` (asking only for those not loaded yet), opens the shared cluster connection (`ssh -fN ailb`, asking the cluster password only if needed), and checks GitHub and the cluster;
- safe to rerun.

## Consequences

- Run it after every WSL or machine restart, and when the cluster connection has closed (8 hours without use, or a network drop).
- Setup: [setup.md](../setup.md#unlock-everything-once-per-session).

## Revisit if

- you keep forgetting it: then option C.
