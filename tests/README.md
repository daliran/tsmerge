# Tests

The tests run with `scripts/check.sh` (and so on every commit), or alone with `uv run --locked pytest`.

- **Scripts are tested as they run for real:** as subprocesses, with temporary folders; nothing touches the cluster or your `outputs/`.
- **The experiment code** is imported as `tsmerge`, from the repository root (`pythonpath` in `pyproject.toml`, [ED-0030](../docs/engineering/decisions/ED-0030-experiment-code.md)).

| File | What it protects |
|---|---|
| [test_run_helper.py](test_run_helper.py) | `tsmerge/run.py`: the formats of `config.json`, `metrics.json` and `history.jsonl`; outputs going to `outputs/scratch/` outside a recorded run |
| [test_run_local.py](test_run_local.py) | `scripts/run_local.sh`: completed and failed runs are recorded, the command runs from the frozen code, the copy is removed, bad names create nothing |
| [test_check_gpu.py](test_check_gpu.py) | `scripts/cluster/check_gpu.py`: which of the cluster's GPUs the PyTorch build supports (Pascal to Ada yes, Kepler and Blackwell no) |
| [test_expert_review_guard.py](test_expert_review_guard.py) | the expert-review guard: what it blocks (cluster commands, scripts that write files) and allows (reading, checks) |
| [test_inventory.py](test_inventory.py) | every file the repository tracks is listed in the inventory of [overview.md](../docs/engineering/overview.md#every-file-in-the-repository) |

Not tested automatically, because they need the cluster: `submit.sh`, `job.sbatch`, `setup_remote.sh`, `pull.sh`, `status.sh`, `logs.sh`.

They were verified by hand on the cluster (2026-11-01 and 2026-11-02), as recorded in their decisions:

- [ED-0006](../docs/engineering/decisions/ED-0006-run-endings.md)
- [ED-0007](../docs/engineering/decisions/ED-0007-run-provenance.md)
- [ED-0008](../docs/engineering/decisions/ED-0008-environment-integrity.md)
- [ED-0010](../docs/engineering/decisions/ED-0010-safe-submissions.md)
- [ED-0029](../docs/engineering/decisions/ED-0029-local-runs.md)
