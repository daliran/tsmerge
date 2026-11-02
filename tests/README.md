# Tests

The tests run with `scripts/check.sh` (and so on every commit), or alone with `uv run --locked pytest`.

- **Scripts are tested as they run for real:** as subprocesses, with temporary folders; nothing touches the cluster or your `outputs/`.
- **The experiment code** is imported as `tsmerge`, from the repository root (`pythonpath` in `pyproject.toml`, [PD-030](../docs/project/decisions/PD-030-experiment-code.md)).

| File | What it protects |
|---|---|
| [test_run_helper.py](test_run_helper.py) | `tsmerge/run.py`: the formats of `config.json`, `metrics.json` and `history.jsonl`; outputs going to `outputs/scratch/` outside a recorded run |
| [test_run_local.py](test_run_local.py) | `scripts/run_local.sh`: completed and failed runs are recorded, the command runs from the frozen code, the copy is removed, bad names create nothing |
| [test_check_gpu.py](test_check_gpu.py) | `scripts/cluster/check_gpu.py`: which of the cluster's GPUs the PyTorch build supports (Pascal to Ada yes, Kepler and Blackwell no) |
| [test_expert_review_guard.py](test_expert_review_guard.py) | the expert-review guard: what it blocks (cluster commands, scripts that write files) and allows (reading, checks) |
| [test_inventory.py](test_inventory.py) | every file the repository tracks is listed in the inventory of [overview.md](../docs/project/overview.md#every-file-in-the-repository) |

Not tested automatically, because they need the cluster: `submit.sh`, `job.sbatch`, `setup_remote.sh`, `pull.sh`, `status.sh`, `logs.sh`. They were verified by hand on the cluster (2026-11-01 and 2026-11-02), as recorded in their decisions ([PD-006](../docs/project/decisions/PD-006-run-endings.md), [PD-007](../docs/project/decisions/PD-007-run-provenance.md), [PD-008](../docs/project/decisions/PD-008-environment-integrity.md), [PD-010](../docs/project/decisions/PD-010-safe-submissions.md), [PD-029](../docs/project/decisions/PD-029-local-runs.md)).
