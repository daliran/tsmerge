"""Fail fast if this node's GPU can't run the installed PyTorch build. Called by job.sbatch.

A GPU can run a build's kernels for the same major architecture and an equal or lower minor
one (e.g. sm_86 kernels run on sm_89). Without this check, a job on an unsupported GPU looks
healthy until the first CUDA operation fails with "no kernel image is available".
"""

import sys

import torch


def main() -> int:
    if not torch.cuda.is_available():
        print("check_gpu: no GPU visible to PyTorch", file=sys.stderr)
        return 1
    major, minor = torch.cuda.get_device_capability(0)
    name = torch.cuda.get_device_name(0)
    built = torch.cuda.get_arch_list()
    supported = any(
        arch.startswith("sm_") and int(arch[3:-1]) == major and int(arch[-1]) <= minor
        for arch in built
    )
    if not supported:
        print(
            f"check_gpu: {name} (sm_{major}{minor}) is not supported by "
            f"torch {torch.__version__} (built for {', '.join(built)}). "
            "Remove its feature from scripts/cluster/defaults.sh.",
            file=sys.stderr,
        )
        return 1
    print(f"check_gpu: {name} (sm_{major}{minor}) ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
