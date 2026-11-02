"""Add a run's runtime facts to its run.json. Called by job.sbatch at start and end.

usage: python run_info.py start <run.json>
       python run_info.py end <run.json> <exit code> [timeout|canceled|stopped]
"""

import datetime
import json
import os
import platform
import socket
import subprocess
import sys
from pathlib import Path


def now() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")


def driver_version() -> str | None:
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    lines = out.split()
    return lines[0] if lines else None


def start_facts() -> dict:
    import torch

    return {
        "status": "running",
        "started_at": now(),
        "host": socket.gethostname(),
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "gpus": [
            torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())
        ],
        "driver": driver_version(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "cudnn": torch.backends.cudnn.version(),
        "gpu_capability": [
            ".".join(map(str, torch.cuda.get_device_capability(i)))
            for i in range(torch.cuda.device_count())
        ],
    }


def end_facts(exit_code: int, stop_reason: str | None) -> dict:
    """The end record. stop_reason ("timeout", "canceled", "stopped") comes from
    job.sbatch's signal handler; without it, the exit code decides."""
    status = stop_reason or ("completed" if exit_code == 0 else "failed")
    return {"status": status, "exit_code": exit_code, "ended_at": now()}


def main() -> None:
    phase, path = sys.argv[1], Path(sys.argv[2])
    if phase not in {"start", "end"}:
        sys.exit(f"run_info: unknown phase {phase!r}: use start or end")
    info = json.loads(path.read_text())
    if phase == "start":
        info |= start_facts()
    else:
        stop_reason = sys.argv[4] if len(sys.argv) > 4 else None
        info |= end_facts(int(sys.argv[3]), stop_reason)
    # Write a temporary file, then rename it over run.json: a rename is atomic, so a job
    # stopped mid-write leaves the old or the new record, never a half-written one.
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(info, indent=2) + "\n")
    os.replace(tmp, path)


if __name__ == "__main__":
    main()
