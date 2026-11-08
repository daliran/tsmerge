"""Draw the figures of the signals docs, in the folder above, into this folder.

usage (from the repository root; matplotlib runs in a temporary uv environment, so it
is not a project dependency):
    uv run --no-project --with matplotlib==3.10.7 --with numpy python \
        docs/research/knowledge/signals/assets/make_figures.py

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


def signal_examples() -> None:
    """Four signals with different independent variables: time, space, frequency,
    position in a sequence."""
    fig, axes = plt.subplots(2, 2, figsize=(10, 6))

    t = np.linspace(0, 0.02, 2000)
    sound = np.sin(2 * np.pi * 440 * t) + 0.4 * np.sin(2 * np.pi * 880 * t)
    axes[0, 0].plot(t * 1000, sound, color=BLUE)
    axes[0, 0].set(
        title="Sound: pressure over time",
        xlabel="time (ms)",
        ylabel="air pressure (a.u.)",
    )

    x = np.linspace(0, 1, 64)
    image = np.outer(np.sin(3 * np.pi * x) ** 2, np.cos(2 * np.pi * x) ** 2)
    axes[0, 1].imshow(image, cmap="gray", extent=(0, 1, 0, 1))
    axes[0, 1].set(
        title="Image: brightness over space",
        xlabel="horizontal position",
        ylabel="vertical position",
    )

    f = np.linspace(0, 1500, 600)
    spectrum = np.exp(-((f - 440) ** 2) / 200) + 0.4 * np.exp(-((f - 880) ** 2) / 200)
    axes[1, 0].plot(f, spectrum, color=ORANGE)
    axes[1, 0].set(
        title="Spectrum: strength over frequency",
        xlabel="frequency (Hz)",
        ylabel="strength (a.u.)",
    )

    bases = "ACGTTGACCTGAGTCA"
    ax = axes[1, 1]
    for i, b in enumerate(bases):
        ax.text(i, 0, b, ha="center", va="center", fontsize=13, family="monospace")
    ax.set(
        xlim=(-1, len(bases)),
        ylim=(-1, 1),
        title="DNA: a letter at each position",
        xlabel="position along the molecule",
    )
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    save(fig, "signal-examples")


def analog_to_digital() -> None:
    """The same signal three ways: continuous, sampled (discrete time), sampled and
    quantized (digital)."""
    t = np.linspace(0, 1, 1000)
    x = np.sin(2 * np.pi * 2 * t) + 0.3 * np.sin(2 * np.pi * 5 * t)
    n = np.arange(0, 1, 1 / 25)
    xn = np.sin(2 * np.pi * 2 * n) + 0.3 * np.sin(2 * np.pi * 5 * n)
    levels = 0.25
    xq = np.round(xn / levels) * levels

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.3), sharey=True)
    axes[0].plot(t, x, color=BLUE)
    axes[0].set(title="1. Continuous (analog)", xlabel="time t (s)", ylabel="x(t)")

    axes[1].plot(t, x, color=GRAY, alpha=0.35)
    axes[1].stem(n, xn, linefmt=BLUE, markerfmt="o", basefmt=" ")
    axes[1].set(title="2. Sampled: discrete time", xlabel="sample n (every 0.04 s)")

    axes[2].plot(t, x, color=GRAY, alpha=0.35)
    for q in np.arange(-1.5, 1.51, levels):
        axes[2].axhline(q, color=GRAY, lw=0.4, alpha=0.5)
    axes[2].stem(n, xq, linefmt=ORANGE, markerfmt="o", basefmt=" ")
    axes[2].set(title="3. Sampled + quantized: digital", xlabel="sample n")
    save(fig, "analog-to-digital")


def aliasing() -> None:
    """A 9 Hz wave sampled at 10 Hz looks like a 1 Hz wave."""
    t = np.linspace(0, 1, 2000)
    fs = 10
    n = np.arange(0, 1.0001, 1 / fs)
    fig, ax = plt.subplots(figsize=(9, 3))
    ax.plot(
        t, np.sin(2 * np.pi * 9 * t), color=GRAY, alpha=0.6, label="true wave: 9 Hz"
    )
    ax.plot(
        t,
        -np.sin(2 * np.pi * 1 * t),
        color=RED,
        ls="--",
        label="what the samples suggest: 1 Hz",
    )
    ax.plot(
        n,
        np.sin(2 * np.pi * 9 * n),
        "o",
        color=BLUE,
        ms=7,
        label="samples, 10 per second",
    )
    ax.set(
        xlabel="time (s)",
        ylabel="value",
        title="Sampling too slowly: a fast wave looks like a slow one (aliasing)",
    )
    ax.legend(loc="upper right", fontsize=8, ncols=3)
    ax.set_ylim(-1.4, 1.6)
    save(fig, "aliasing")


if __name__ == "__main__":
    signal_examples()
    analog_to_digital()
    aliasing()
