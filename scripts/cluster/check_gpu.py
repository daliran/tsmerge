"""Fail fast if this node's GPU can't run the installed PyTorch build.

Called by job.sbatch before the run's command. Without this check, a job on an
unsupported GPU looks healthy until its first CUDA operation fails with "no kernel image
is available" (ED-004).
"""

import sys


def is_supported(capability: tuple[int, int], arch_list: list[str]) -> bool:
    """Whether a GPU of this compute capability can run a build with these kernels.

    A GPU runs kernels compiled for the same major architecture and an equal or lower
    minor one: sm_86 kernels run on an sm_89 GPU, but sm_90 kernels don't run on sm_120.
    Entries that aren't plain `sm_<digits>` (PTX `compute_*`, suffixed `sm_90a`) are
    ignored, which errs on the side of rejecting.
    """
    major, minor = capability
    for arch in arch_list:
        digits = arch.removeprefix("sm_")
        if not arch.startswith("sm_") or not digits.isdigit() or len(digits) < 2:
            continue
        if int(digits[:-1]) == major and int(digits[-1]) <= minor:
            return True
    return False


def main() -> int:
    import torch

    if not torch.cuda.is_available():
        print("check_gpu: no GPU visible to PyTorch", file=sys.stderr)
        return 1
    capability = torch.cuda.get_device_capability(0)
    name = torch.cuda.get_device_name(0)
    built = torch.cuda.get_arch_list()
    sm = f"sm_{capability[0]}{capability[1]}"
    if not is_supported(capability, built):
        print(
            f"check_gpu: {name} ({sm}) is not supported by torch {torch.__version__} "
            f"(built for {', '.join(built)}). "
            "Remove its feature from scripts/cluster/defaults.sh.",
            file=sys.stderr,
        )
        return 1
    print(f"check_gpu: {name} ({sm}) ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
