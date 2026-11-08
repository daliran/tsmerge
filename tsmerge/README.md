# tsmerge

The experiment code.

Every module runs as `python -m tsmerge.<module>`, from the repository root, or from a run's frozen `code/` copy.

The package isn't installed, so each run imports exactly its own code ([ED-0030](../docs/engineering/decisions/ED-0030-experiment-code.md)).

| Module | What it is |
|---|---|
| [run.py](run.py) | What every experiment needs from its run: folders (`RUN_DIR`, `DATA_DIR`, `RUNS_ROOT`), device, seeds, numeric settings, and the records: `config.json`, `results/metrics.json`, `results/history.jsonl` |
| [hello.py](hello.py) | The smallest complete experiment: the template for new ones, and the smoke test for a new setup |

## Running a module

```bash
scripts/run_local.sh <experiment> python -m tsmerge.<module> [args…]          # recorded, locally
scripts/cluster/submit.sh <experiment> python -m tsmerge.<module> [args…]     # recorded, on the cluster
uv run python -m tsmerge.<module> [args…]                                     # quick try: outputs in outputs/scratch/
```

How runs work: [running.md](../docs/engineering/running.md); what they record: [runs.md](../docs/engineering/runs.md).

## A new experiment

Name it `e<NNNN>-<slug>` when you run it ([ED-0032](../docs/engineering/decisions/ED-0032-experiment-ids.md)). Start from a copy of `hello.py`, and keep its steps in order:

1. all settings in one dataclass, every one a command-line option;
2. seeds and numeric settings, then `run.write_config()`, before any computation;
3. the computation, logging curves with `run.log_history()`;
4. `run.write_metrics()` with every value the run measured; other outputs under `run.run_dir()`.
