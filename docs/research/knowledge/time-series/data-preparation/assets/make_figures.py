"""Draw the figures of the data-preparation docs, in the folder above, into this folder.

usage (from the repository root; matplotlib runs in a temporary uv environment, so it
is not a project dependency):
    uv run --no-project --with matplotlib==3.10.7 --with numpy python \
        docs/research/knowledge/time-series/data-preparation/assets/make_figures.py

Every figure is synthetic and illustrative: made from simple formulas, with a fixed
random seed, so the same command always draws the same picture. The PNGs are committed
next to this file; rerun it after changing a figure, and commit both.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

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


def toy_series(length: int) -> np.ndarray:
    t = np.arange(length)
    return np.sin(2 * np.pi * t / 24) + 0.003 * t + 0.15 * RNG.standard_normal(length)


def draw_windows(ax, x, window: int, stride: int, color: str, max_windows: int = 99):
    ax.plot(x, color=GRAY, lw=1)
    lo, hi = x.min() - 0.3, x.max() + 0.3
    count = 0
    for start in range(0, len(x) - window + 1, stride):
        if count >= max_windows:
            break
        offset = (count % 4) * 0.12
        ax.add_patch(
            Rectangle(
                (start, lo - offset),
                window - 1,
                hi - lo,
                fill=True,
                alpha=0.10,
                color=color,
                lw=0,
            )
        )
        ax.add_patch(
            Rectangle(
                (start, lo - offset),
                window - 1,
                hi - lo,
                fill=False,
                ec=color,
                lw=1.2,
            )
        )
        count += 1
    ax.set_ylim(lo - 0.6, hi + 0.2)
    ax.set_yticks([])
    return count


def sliding_windows() -> None:
    """Cutting a series into windows of size W, moving by stride S."""
    x = toy_series(120)
    fig, ax = plt.subplots(figsize=(11, 2.8))
    n = draw_windows(ax, x, window=36, stride=12, color=BLUE)
    ax.annotate(
        "",
        xy=(12, x.max() + 0.25),
        xytext=(0, x.max() + 0.25),
        arrowprops=dict(arrowstyle="->", color=RED, lw=1.5),
    )
    ax.text(6, x.max() + 0.35, "stride S = 12", color=RED, ha="center", fontsize=9)
    ax.annotate(
        "",
        xy=(35, x.min() - 0.85),
        xytext=(0, x.min() - 0.85),
        arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.5),
    )
    ax.text(
        17.5, x.min() - 1.05, "window size W = 36", color=BLUE, ha="center", fontsize=9
    )
    ax.set(
        title=f"A series of 120 steps cut into {n} windows (W = 36, S = 12)",
        xlabel="time step",
    )
    ax.set_ylim(x.min() - 1.2, x.max() + 0.6)
    save(fig, "sliding-windows")


def stride_overlap() -> None:
    """The same window size with three strides: no overlap, half overlap, maximal."""
    x = toy_series(96)
    window = 24
    cases = [
        (24, "S = W = 24: no overlap", GREEN),
        (12, "S = 12: half overlap", BLUE),
        (2, "S = 2: heavy overlap (every 2 steps; S = 1 would be denser still)", RED),
    ]
    fig, axes = plt.subplots(3, 1, figsize=(11, 6.3), sharex=True)
    for ax, (stride, label, color) in zip(axes, cases, strict=True):
        n = draw_windows(ax, x, window, stride, color)
        ax.set_title(f"{label} → {n} windows", loc="left", fontsize=10)
    axes[-1].set_xlabel("time step (series of 96 steps, window size W = 24)")
    save(fig, "stride-overlap")


def window_count() -> None:
    """How many windows a series gives, as a function of the stride."""
    length, window = 1000, 100
    strides = np.arange(1, window + 1)
    counts = (length - window) // strides + 1
    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.plot(strides, counts, color=BLUE)
    for s in (1, 10, 50, 100):
        c = (length - window) // s + 1
        ax.plot(s, c, "o", color=RED)
        ax.annotate(
            f"S = {s}: {c}",
            (s, c),
            textcoords="offset points",
            xytext=(8, 6),
            fontsize=9,
        )
    ax.set(
        xlabel="stride S",
        ylabel="number of windows",
        title="T = 1000 steps, W = 100: windows = ⌊(T - W) / S⌋ + 1",
        yscale="log",
    )
    save(fig, "window-count")


def forecast_window() -> None:
    """A forecasting window: the model sees the context and predicts the horizon."""
    x = toy_series(130)
    context, horizon = 96, 24
    start = 6
    fig, ax = plt.subplots(figsize=(11, 3))
    ax.plot(x, color=GRAY, lw=1)
    seen = slice(start, start + context)
    hidden = slice(start + context, start + context + horizon)
    ax.plot(range(seen.start, seen.stop), x[seen], color=BLUE, lw=2)
    ax.plot(range(hidden.start, hidden.stop), x[hidden], color=ORANGE, lw=2)
    ax.axvspan(seen.start, seen.stop - 1, color=BLUE, alpha=0.08)
    ax.axvspan(hidden.start, hidden.stop - 1, color=ORANGE, alpha=0.12)
    top = x.max() + 0.3
    ax.text(
        start + context / 2,
        top,
        "context (look-back) L = 96: given",
        ha="center",
        color=BLUE,
    )
    ax.text(
        start + context + horizon / 2,
        top,
        "horizon H = 24:\nto predict",
        ha="center",
        color=ORANGE,
        fontsize=9,
    )
    ax.set(
        title="One forecasting window = context + horizon (here 96 + 24 = 120 steps)",
        xlabel="time step",
    )
    ax.set_yticks([])
    ax.set_ylim(x.min() - 0.3, top + 0.6)
    save(fig, "forecast-window")


def split_leakage() -> None:
    """Windows must not straddle the train/test boundary, and the split comes first."""
    x = toy_series(120)
    boundary = 84
    window = 24
    fig, axes = plt.subplots(2, 1, figsize=(11, 4.8), sharex=True)
    for ax in axes:
        ax.plot(x, color=GRAY, lw=1)
        ax.axvline(boundary, color="black", lw=1.5)
        ax.text(boundary - 2, x.max() + 0.25, "train  ", ha="right", fontsize=9)
        ax.text(boundary + 2, x.max() + 0.25, "  test", ha="left", fontsize=9)
        ax.set_yticks([])
        ax.set_ylim(x.min() - 0.5, x.max() + 0.6)

    lo, hi = x.min() - 0.3, x.max() + 0.1
    # Both windows contain steps on each side of the boundary (66-89 and 78-101).
    for i, start in enumerate((66, 78)):
        axes[0].add_patch(
            Rectangle(
                (start, lo - 0.12 * i), window - 1, hi - lo, fill=False, ec=RED, lw=1.5
            )
        )
    axes[0].set_title(
        "Wrong: windows cut across the boundary mix training and test data",
        loc="left",
        color=RED,
        fontsize=10,
    )

    parts = [
        (range(0, boundary - window + 1, 12), GREEN),
        (range(boundary, len(x) - window + 1, 12), BLUE),
    ]
    for starts, color in parts:
        for i, start in enumerate(starts):
            axes[1].add_patch(
                Rectangle(
                    (start, lo - 0.12 * (i % 3)),
                    window - 1,
                    hi - lo,
                    fill=False,
                    ec=color,
                    lw=1.2,
                )
            )
    axes[1].set_title(
        "Right: split the series by time first, then cut windows inside each part",
        loc="left",
        color=GREEN,
        fontsize=10,
    )
    axes[1].set_xlabel("time step")
    save(fig, "split-leakage")


if __name__ == "__main__":
    sliding_windows()
    stride_overlap()
    window_count()
    forecast_window()
    split_leakage()
