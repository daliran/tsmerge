"""Draw the figures of the task docs, in the folder above, into this folder.

usage (from the repository root; matplotlib runs in a temporary uv environment, so it
is not a project dependency):
    uv run --no-project --with matplotlib==3.10.7 --with numpy python \
        docs/research/knowledge/time-series/tasks/assets/make_figures.py

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


def tasks() -> None:
    """The four tasks: what goes in, what comes out."""
    t = np.arange(150)
    x = np.sin(2 * np.pi * t / 30) + 0.15 * RNG.standard_normal(t.size)
    fig, axes = plt.subplots(2, 2, figsize=(12, 6.5))

    ax = axes[0, 0]
    cut = 110
    ax.plot(t[:cut], x[:cut], color=BLUE, label="known past")
    ax.plot(t[cut:], x[cut:], color=GRAY, ls=":", label="true future (unknown)")
    ax.plot(t[cut:], np.sin(2 * np.pi * t[cut:] / 30), color=ORANGE, label="forecast")
    ax.axvline(cut, color="black", lw=1)
    ax.set_title("Forecasting: predict what comes next", loc="left", fontsize=10)
    ax.legend(fontsize=8, loc="lower left")

    ax = axes[0, 1]
    gaps = (t > 40) & (t < 60) | (t > 95) & (t < 105)
    ax.plot(t, np.where(gaps, np.nan, x), color=BLUE, label="observed")
    ax.plot(
        t[gaps],
        np.sin(2 * np.pi * t[gaps] / 30),
        "o",
        ms=3,
        color=ORANGE,
        label="filled in",
    )
    ax.set_title("Imputation: fill in the missing values", loc="left", fontsize=10)
    ax.legend(fontsize=8, loc="lower left")

    ax = axes[1, 0]
    y = x.copy()
    y[70] += 3
    ax.plot(t, y, color=BLUE)
    ax.plot(70, y[70], "o", color=RED, ms=9, mfc="none", mew=2)
    ax.set_title("Anomaly detection: flag what isn't normal", loc="left", fontsize=10)

    ax = axes[1, 1]
    for i, (period, label) in enumerate(((30, "class A"), (12, "class B"))):
        z = np.sin(2 * np.pi * t / period) + 0.15 * RNG.standard_normal(t.size)
        ax.plot(t, z + 3 * i, color=(BLUE, GREEN)[i])
        ax.text(155, 3 * i, f"→ {label}", va="center", fontsize=10)
    ax.set_xlim(0, 185)
    ax.set_title(
        "Classification: give the whole series one label", loc="left", fontsize=10
    )

    for ax in axes.flat:
        ax.set_yticks([])
    for ax in axes[1]:
        ax.set_xlabel("time step")
    save(fig, "tasks")


def anomaly_types() -> None:
    """Point, contextual and collective anomalies."""
    t = np.arange(240)
    base = np.sin(2 * np.pi * t / 48) + 0.1 * RNG.standard_normal(t.size)
    point, contextual, collective = base.copy(), base.copy(), base.copy()
    point[100] += 2.5
    contextual[80:89] = 0.95  # a peak-like value where a trough is due (steps 80-88)
    collective[130:160] = 0.05 * RNG.standard_normal(30)  # the rhythm stops
    cases = [
        (point, "Point: one value far from all the others", (100, 101)),
        (contextual, "Contextual: a normal value, at the wrong moment", (80, 89)),
        (
            collective,
            "Collective: each value looks fine, together they don't",
            (130, 160),
        ),
    ]
    fig, axes = plt.subplots(3, 1, figsize=(10, 6.2), sharex=True)
    for ax, (y, label, (a, b)) in zip(axes, cases, strict=True):
        ax.plot(t, y, color=BLUE, lw=1)
        ax.axvspan(a - 1, b, color=RED, alpha=0.2)
        ax.set_title(label, loc="left", fontsize=10)
        ax.set_yticks([])
    axes[-1].set_xlabel("time step")
    save(fig, "anomaly-types")


if __name__ == "__main__":
    tasks()
    anomaly_types()
