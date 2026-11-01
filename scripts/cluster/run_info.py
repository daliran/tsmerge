"""Add a run's runtime facts to its run.json. Called by job.sbatch at start and end.

usage: python run_info.py start <run.json>
       python run_info.py end <run.json> <exit code>
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
    }


def end_facts(exit_code: int) -> dict:
    return {
        "status": "completed" if exit_code == 0 else "failed",
        "exit_code": exit_code,
        "ended_at": now(),
    }


def main() -> None:
    phase, path = sys.argv[1], Path(sys.argv[2])
    info = json.loads(path.read_text())
    info |= start_facts() if phase == "start" else end_facts(int(sys.argv[3]))
    path.write_text(json.dumps(info, indent=2) + "\n")


if __name__ == "__main__":
    main()
