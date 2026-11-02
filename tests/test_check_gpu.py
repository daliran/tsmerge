"""Tests for the GPU compatibility rule of scripts/cluster/check_gpu.py (PD-004)."""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "cluster" / "check_gpu.py"
_spec = importlib.util.spec_from_file_location("check_gpu", SCRIPT)
check_gpu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_gpu)

# The kernels of the project's PyTorch build (torch 2.14.1 + CUDA 12.6, PD-001).
BUILD = ["sm_50", "sm_60", "sm_70", "sm_75", "sm_80", "sm_86", "sm_90"]


@pytest.mark.parametrize(
    ("gpu", "capability", "supported"),
    [
        ("GTX 1080", (6, 1), True),
        ("P100", (6, 0), True),
        ("RTX 2070 SUPER / 2080 Ti", (7, 5), True),
        ("RTX A5000 / A40", (8, 6), True),
        ("L40S", (8, 9), True),
        ("K80", (3, 7), False),
        ("RTX PRO 6000 Blackwell", (12, 0), False),
    ],
)
def test_cluster_gpus_against_the_project_build(gpu, capability, supported):
    assert check_gpu.is_supported(capability, BUILD) is supported, gpu


def test_ignores_ptx_and_suffixed_entries():
    assert not check_gpu.is_supported((9, 0), ["compute_90", "sm_90a"])
    assert check_gpu.is_supported((10, 0), ["sm_100"])
