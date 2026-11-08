"""Draw the figures of the time-series doc, in the folder above, into this folder.

usage (from the repository root; matplotlib runs in a temporary uv environment, so it
is not a project dependency):
    uv run --no-project --with matplotlib==3.10.7 --with numpy python \
        docs/research/knowledge/time-series/assets/make_figures.py

Every figure is synthetic and illustrative: made from simple formulas, with a fixed
random seed, so the same command always draws the same picture. The PNGs are committed
next to this file; rerun it after changing a figure, and commit both.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(7)
BLUE, ORANGE, GREEN, RED, GRAY = "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#7f7f7f"

plt.rcParams.update(
    {
        "figure.dpi": 110,
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titleweight": "bold",
    }
)


def save(fig, name: str) -> None:
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {name}.png")


def daily_cycle(n_days: int, phase: float = 0.0, noise: float = 0.15) -> np.ndarray:
    h = np.arange(24 * n_days)
    return np.sin(2 * np.pi * (h / 24) + phase) + noise * RNG.standard_normal(h.size)


def univariate_multivariate() -> None:
    """One channel vs several channels sharing the same time axis."""
    hours = np.arange(24 * 5)
    temp = 15 + 6 * daily_cycle(5, -np.pi / 2)
    load = 50 + 15 * daily_cycle(5, -np.pi / 3) + 0.1 * hours
    humidity = 60 - 12 * daily_cycle(5, -np.pi / 2)

    fig = plt.figure(figsize=(11, 5))
    grid = fig.add_gridspec(3, 2, width_ratios=[1, 1.15])
    ax = fig.add_subplot(grid[:, 0])
    ax.plot(hours, temp, color=BLUE)
    ax.set(
        title="Univariate: one value per time step",
        xlabel="time (hours)",
        ylabel="temperature (°C)",
    )

    series = [
        (temp, "temperature (°C)", BLUE),
        (humidity, "humidity (%)", GREEN),
        (load, "power load (kW)", ORANGE),
    ]
    for i, (y, label, color) in enumerate(series):
        a = fig.add_subplot(grid[i, 1])
        a.plot(hours, y, color=color)
        a.set_ylabel(label, fontsize=8)
        if i == 0:
            a.set_title("Multivariate: several values per time step (channels)")
        if i < 2:
            a.set_xticklabels([])
        else:
            a.set_xlabel("time (hours)")
    save(fig, "univariate-multivariate")


def as_time_series() -> None:
    """Audio and DNA read as series: the index is time for audio, position for DNA."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.6))

    fs = 8000
    n = np.arange(0, 80)
    audio = np.sin(2 * np.pi * 440 * n / fs) + 0.05 * RNG.standard_normal(n.size)
    axes[0].stem(n, audio, linefmt=BLUE, markerfmt=".", basefmt=" ")
    axes[0].set(
        title="Audio: 8,000 samples per second, one channel",
        xlabel="sample index n (1 step = 1/8000 s)",
        ylabel="amplitude",
    )

    seq = "ACGTTGACCTGAGTCAGG"
    letters = "ACGT"
    onehot = np.array([[1 if s == b else 0 for s in seq] for b in letters])
    axes[1].imshow(onehot, cmap="Blues", aspect="auto", vmin=0, vmax=1.3)
    axes[1].set_yticks(range(4), [f"channel {b}" for b in letters])
    axes[1].set_xticks(range(len(seq)), list(seq), family="monospace")
    axes[1].set(
        title="DNA: one-hot encoded, 4 channels",
        xlabel="position along the sequence (the index)",
    )
    save(fig, "as-time-series")


if __name__ == "__main__":
    univariate_multivariate()
    as_time_series()
