"""Summarize the runs in outputs/runs/ (local and pulled): status, duration, share of
the time limit, estimated cost.

usage: uv run --locked python scripts/runs_summary.py [<experiment>]

Reads every outputs/runs/<experiment>/<run id>/run.json. Mainly useful for choosing time
limits (how close runs come to theirs) and, secondarily, for the budget (ED-0023).

The cost estimates the cluster's billing (docs/engineering/cluster.md): standard hours =
max(CPUs x 0.39, memory GB x 0.06, GPUs x 6.0) x elapsed hours. Memory defaults to
3 GB per CPU, so CPUs or GPUs decide. `all_serial` and local runs are free.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

RUNS = Path(__file__).resolve().parents[1] / "outputs" / "runs"


def hours(text: str | None) -> float | None:
    """Slurm time limit "[D-]HH:MM:SS" or "MM:SS" as hours."""
    if not text:
        return None
    days, _, rest = text.rpartition("-")
    parts = [int(p) for p in rest.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts
    return (int(days or 0) * 24) + h + m / 60 + s / 3600


def elapsed_hours(run: dict) -> float | None:
    if not run.get("started_at") or not run.get("ended_at"):
        return None
    start = datetime.fromisoformat(run["started_at"])
    end = datetime.fromisoformat(run["ended_at"])
    return (end - start).total_seconds() / 3600


def standard_hours(run: dict, elapsed: float) -> float:
    slurm = run.get("slurm") or {}
    if run.get("launcher") == "local" or slurm.get("partition") == "all_serial":
        return 0.0
    cpus = int(slurm.get("cpus_per_task") or 0)
    # Runs recorded before the "slurm" section existed: count the GPUs the run saw.
    gpus = int(slurm.get("gpus") or len(run.get("gpus") or []))
    return max(cpus * 0.39, cpus * 3 * 0.06, gpus * 6.0) * elapsed


def main() -> None:
    experiment = sys.argv[1] if len(sys.argv) > 1 else "*"
    files = sorted(RUNS.glob(f"{experiment}/*/run.json"))
    if not files:
        sys.exit(f"no runs under {RUNS}/{experiment}: pull them first (pull.sh)")
    header = (
        f"{'run':<44} {'status':<10} {'gpu':<26} "
        f"{'time':>8} {'limit':>8} {'used':>5} {'stdh':>6}"
    )
    print(header)
    print("-" * len(header))
    total = 0.0
    for path in files:
        run = json.loads(path.read_text())
        elapsed = elapsed_hours(run)
        limit = hours((run.get("slurm") or {}).get("time"))
        gpus = run.get("gpus") or []
        gpu = gpus[0].removeprefix("NVIDIA ").removeprefix("GeForce ") if gpus else "-"
        cost = standard_hours(run, elapsed) if elapsed is not None else 0.0
        total += cost
        used = f"{elapsed / limit:.0%}" if elapsed is not None and limit else "-"
        print(
            f"{run.get('experiment', '?') + '/' + run.get('run_id', '?'):<44} "
            f"{run.get('status', '?'):<10} {gpu:<26} "
            f"{(f'{elapsed * 60:.1f}m' if elapsed is not None else '-'):>8} "
            f"{(f'{limit * 60:.0f}m' if limit else '-'):>8} {used:>5} {cost:>6.2f}"
        )
    print(f"\n{len(files)} runs, about {total:.2f} standard hours in total")


if __name__ == "__main__":
    main()
