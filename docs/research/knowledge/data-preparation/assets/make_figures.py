"""Draw the figures of the data-preparation docs, in the folder above, into this folder.

usage (from the repository root; matplotlib runs in a temporary uv environment, so it
is not a project dependency):
    uv run --no-project --with matplotlib==3.10.7 --with numpy python \
        docs/research/knowledge/data-preparation/assets/make_figures.py

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


def scalers() -> None:
    """The values 1, 2, 3, 4 and an outlier 100: raw on top, on their own scale; then
    under standard, min-max and robust scaling, on one shared scale, where an outlier
    off the chart is marked by an arrow."""
    x = np.array([1, 2, 3, 4, 100.0])
    q1, q2, q3 = np.percentile(x, [25, 50, 75])
    rows = [
        (
            "standard scaling: (x - mean) / standard deviation",
            (x - x.mean()) / x.std(),
            ORANGE,
        ),
        (
            "min-max scaling: (x - min) / (max - min)",
            (x - x.min()) / (x.max() - x.min()),
            GREEN,
        ),
        ("robust scaling: (x - median) / (Q3 - Q1)", (x - q2) / (q3 - q1), RED),
    ]
    fig, axes = plt.subplots(len(rows) + 1, 1, figsize=(10, 5.8))
    raw = axes[0]
    raw.scatter(x[:4], np.zeros(4), color=BLUE, s=60, zorder=3)
    raw.scatter([x[4]], [0], color=BLUE, s=60, marker="X", zorder=3)
    raw.text(-3, 0.35, "1, 2, 3, 4 (bunched on the left)", fontsize=9, color=BLUE)
    raw.text(100, 0.35, "outlier 100", fontsize=9, color=BLUE, ha="right")
    raw.axhline(0, color=GRAY, lw=0.8)
    raw.set(yticks=[], xlim=(-5, 105), ylim=(-0.4, 0.7))
    raw.spines["left"].set_visible(False)
    raw.set_title("raw data (before scaling, its own scale)", loc="left", fontsize=10)
    for ax, (title, values, color) in zip(axes[1:], rows, strict=True):
        normal, outlier = values[:4], values[4]
        ax.scatter(normal, np.zeros(4), color=color, s=60, zorder=3)
        span = f"1, 2, 3, 4 become {normal.min():.2f} … {normal.max():.2f}"
        ax.text(-1.55, 0.35, span, fontsize=9, color=color)
        if outlier <= 1.55:
            ax.scatter([outlier], [0], color=color, s=60, marker="X", zorder=3)
            ax.annotate(
                f"outlier 100 → {outlier:.2f}",
                xy=(outlier, 0),
                xytext=(0.6, 0.35),
                fontsize=9,
                color=color,
                arrowprops={"arrowstyle": "->", "color": color},
            )
        else:
            ax.annotate(
                f"outlier 100 → {outlier:.2f} (off the chart)",
                xy=(1.6, 0),
                xytext=(0.6, 0.35),
                fontsize=9,
                color=color,
                arrowprops={"arrowstyle": "->", "color": color},
            )
        ax.axhline(0, color=GRAY, lw=0.8)
        ax.set(yticks=[], xlim=(-1.6, 1.6), ylim=(-0.4, 0.7))
        ax.spines["left"].set_visible(False)
        ax.set_title(title, loc="left", fontsize=10)
    axes[-1].set_xlabel("scaled value (one shared scale for the three methods)")
    save(fig, "scalers")


if __name__ == "__main__":
    scalers()
