# ED-0027 — Runs may use every allowed GPU; numerics are made explicit, not left to the hardware

- **Status:** accepted
- **Date:** 2026-11-02
- **Decided by:** the author
- **Answers:** question EQ-0002 (opened 2026-11-01)

## Problem

- [ED-0002](ED-0002-cluster-partition.md) keeps the project off `boost_usr_prod`, but `all_usr_prod` contains the same high-end nodes (L40S, A40). The GPU list decides which nodes a job may use.
- The choice sets:
  - how many GPUs are available (queue times),
  - how much memory a job can count on,
  - and how comparable runs are: Ampere and newer GPUs use TF32 for convolutions by default, older ones don't, so a difference between two runs could come from the node rather than the method (first expert review, item M4).
- **A cluster rule found on 2026-11-02:** on `all_usr_prod`, a job whose GPU list asks for more than 24 GB of GPU memory is refused ("Jobs requiring > 24G VRAM must be run on the 'boost_usr_prod' partition").
  - The cluster computes the minimum memory over the list: a mixed list (minimum 8 GB) is accepted; a list of only L40S or A40 is not.

## Options

| | A — older GPUs only | B — all except Blackwell | C — Turing and Ampere only |
|---|---|---|---|
| GPUs available | 32 of 87 (37%) | 72 of 87 (83%) | 30 of 87 (34%) |
| GPU memory per job | 8–24 GB | 8–45 GB | 11–24 GB |
| Uses high-memory GPUs | no | yes (40 GPUs) | no |
| bf16 and TF32 GPUs | 5 | 45 | 5 |

(Counts from `sinfo`, 2026-11-01.)

## Decision

- **Option B:** every GPU except Blackwell, for the most nodes and the shortest queues ([defaults.sh](../../../scripts/cluster/defaults.sh)).
- **Numerics are explicit:** the experiment code sets TF32 and the other determinism flags itself, and records them in `config.json` ([ED-0009](ED-0009-run-records.md)), so results don't depend on which GPU a job landed on.
- **For a sweep that needs strictly comparable hardware,** narrow the GPU list for that sweep to one family.
  - Because of the 24 GB rule, on `all_usr_prod` that means a family of at most 24 GB: Turing (2080, 2080 Ti, RTX 5000, RTX 6000) or the RTX A5000.

## Consequences

- `run.json` records each run's GPU and its compute capability, so the hardware behind every result stays visible.
- High-memory GPUs are used only as part of the mixed list, never requested alone.

## Revisit if

- results show differences that track the GPU type despite explicit numerics;
- queue times on the mixed list become a problem.
