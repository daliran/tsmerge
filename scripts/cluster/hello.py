"""Smoke test for the environment: prints what PyTorch sees and runs one CUDA operation.

In a cluster run (RUN_DIR set by job.sbatch) it also writes results/hello.json.
"""

import json
import os
import platform
from pathlib import Path

import torch


def main() -> None:
    info = {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "arch_list": torch.cuda.get_arch_list(),
        "cuda_available": torch.cuda.is_available(),
    }
    if info["cuda_available"]:
        info["gpu"] = torch.cuda.get_device_name(0)
        info["capability"] = ".".join(map(str, torch.cuda.get_device_capability(0)))
        x = torch.randn(1024, 1024, device="cuda")
        info["matmul_ok"] = bool(torch.isfinite(x @ x.T).all())

    for key, value in info.items():
        print(f"{key}: {value}")

    run_dir = os.environ.get("RUN_DIR")
    if run_dir:
        out = Path(run_dir) / "results" / "hello.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(info, indent=2) + "\n")
        print(f"written: {out}")


if __name__ == "__main__":
    main()
