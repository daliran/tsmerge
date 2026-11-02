"""What every experiment needs from its run: folders, seeds, numerics and the records.

The same code works in a recorded run (local with scripts/run_local.sh, or on the
cluster), where the runner sets RUN_DIR, and in a plain or debugger start, where it
doesn't: then outputs go to outputs/scratch/, overwritten each time (PD-030).
Records: config.json, results/metrics.json (final values), results/history.jsonl
(curves); their formats are in docs/project/runs.md.
"""

import json
import os
import random
from pathlib import Path

import numpy as np
import torch

REPO = Path(__file__).resolve().parents[1]
SPLITS = {"train", "val", "test"}


def run_dir() -> Path:
    """This run's folder (RUN_DIR), or outputs/scratch/ outside a recorded run."""
    path = Path(os.environ.get("RUN_DIR") or REPO / "outputs" / "scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def data_dir() -> Path:
    """The datasets folder (PD-020): DATA_DIR, or data/ in the repository."""
    return Path(os.environ.get("DATA_DIR") or REPO / "data")


def runs_root() -> Path:
    """The root of all runs, to read the runs listed in run.json's inputs (PD-021)."""
    return Path(os.environ.get("RUNS_ROOT") or REPO / "outputs" / "runs")


def device(choice: str = "auto") -> torch.device:
    """`auto`: the GPU when PyTorch sees one, the CPU otherwise."""
    if choice == "auto":
        choice = "cuda" if torch.cuda.is_available() else "cpu"
    return torch.device(choice)


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)  # also seeds every GPU


def set_numerics(deterministic: bool = False, tf32: bool = False) -> dict:
    """Set the numeric behavior explicitly, so it doesn't depend on the GPU (PD-027).

    TF32 is off by default: Ampere and newer GPUs would otherwise use it for
    convolutions, older ones can't, and results would differ by node.
    Returns the settings, for config.json.
    """
    torch.backends.cudnn.deterministic = deterministic
    torch.backends.cudnn.benchmark = not deterministic
    torch.backends.cuda.matmul.allow_tf32 = tf32
    torch.backends.cudnn.allow_tf32 = tf32
    torch.use_deterministic_algorithms(deterministic, warn_only=True)
    return {
        "cudnn_deterministic": deterministic,
        "cudnn_benchmark": not deterministic,
        "allow_tf32_matmul": tf32,
        "allow_tf32_cudnn": tf32,
        "use_deterministic_algorithms": deterministic,
    }


def write_config(config: dict, seeds: dict, data: list, determinism: dict) -> Path:
    """Write config.json before any computation (PD-009): every setting with its
    final value, the seeds, the datasets used, and the numeric settings.
    It marks the start of a run: a curve left in outputs/scratch/ by an earlier quick
    try is removed, so log_history() starts a new one."""
    (run_dir() / "results" / "history.jsonl").unlink(missing_ok=True)
    path = run_dir() / "config.json"
    record = {
        "config": config,
        "seeds": seeds,
        "data": data,
        "determinism": determinism,
    }
    path.write_text(json.dumps(record, indent=2) + "\n")
    return path


def log_history(step: int, split: str, metric: str, value: float, **extra) -> None:
    """Append one point of a curve to results/history.jsonl (PD-033): one JSON line
    per value, written at once, so a stopped run keeps every point logged so far.
    `extra` may hold `phase` and `epoch`."""
    if split not in SPLITS:
        raise ValueError(f"split must be one of {sorted(SPLITS)}, got {split!r}")
    if unknown := extra.keys() - {"phase", "epoch"}:
        raise ValueError(f"unknown fields {sorted(unknown)}")
    record = {"step": step, **extra, "split": split, "metric": metric}
    record["value"] = float(value)
    path = run_dir() / "results" / "history.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as file:
        file.write(json.dumps(record) + "\n")


def write_metrics(records: list[dict]) -> Path:
    """Write results/metrics.json (PD-026): one record per value, with `split`,
    `metric`, `value` and, when a run has several models, `phase`."""
    for record in records:
        missing = {"split", "metric", "value"} - record.keys()
        if missing:
            raise ValueError(f"metric record {record} lacks {sorted(missing)}")
        if record["split"] not in SPLITS:
            raise ValueError(f"split must be one of {sorted(SPLITS)}: {record}")
        if extra := record.keys() - {"phase", "split", "metric", "value"}:
            raise ValueError(f"unknown fields {sorted(extra)} in {record}")
        record["value"] = float(record["value"])
    path = run_dir() / "results" / "metrics.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, indent=2) + "\n")
    return path
