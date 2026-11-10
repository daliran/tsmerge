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


def per_channel_scaling() -> None:
    """Four channels of a small plant, raw and after per-channel standard scaling."""
    t = np.arange(72)
    channels = {
        "temperature (°C)": 20
        + 5 * np.sin(2 * np.pi * t / 24)
        + 0.3 * RNG.standard_normal(t.size),
        "power load (kW)": 500
        + 100 * np.sin(2 * np.pi * (t - 3) / 24)
        + 10 * RNG.standard_normal(t.size),
        "valve (0 closed, 1 open)": ((t // 6) % 2).astype(float),
        "pressure setpoint (bar, constant)": np.full(t.size, 3.0),
    }
    colors = [BLUE, ORANGE, GREEN, GRAY]
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
    for (name, x), c in zip(channels.items(), colors, strict=True):
        axes[0].plot(t, x, color=c, label=name)
        sd = x.std()
        scaled = (x - x.mean()) / (
            sd if sd > 0 else 1.0
        )  # a constant channel stays unscaled
        axes[1].plot(t, scaled, color=c)
    axes[0].set(
        xlabel="time step (hours)", title="raw: one channel dominates the scale"
    )
    axes[0].legend(loc="center right", fontsize=7)
    axes[1].set(
        xlabel="time step (hours)",
        title="each channel scaled with its own mean and spread",
    )
    save(fig, "per-channel-scaling")


def constant_channel() -> None:
    """A channel constant during training that changes slightly at test time."""
    t = np.arange(240)
    split = 160
    rise = np.where(t >= 190, 0.05, 0.0) * (t < 215)
    noisy = 1.0 + 0.001 * RNG.standard_normal(t.size) + rise
    exact = 1.0 + rise
    train = slice(0, split)
    fig, axes = plt.subplots(3, 1, figsize=(10, 6.4), sharex=True)
    axes[0].plot(t, noisy, color=BLUE)
    axes[0].set_title(
        "raw: almost constant in training, then a small rise of 0.05",
        loc="left",
        fontsize=10,
    )
    z = (noisy - noisy[train].mean()) / noisy[train].std()
    axes[1].plot(t, z, color=RED)
    axes[1].set_title(
        f"standard scaling, training spread {noisy[train].std():.4f}: "
        "the small rise becomes huge",
        loc="left",
        fontsize=10,
    )
    sd = exact[train].std()
    z0 = (exact - exact[train].mean()) / (sd if sd > 0 else 1.0)
    axes[2].plot(t, z0, color=ORANGE)
    axes[2].set_ylim(-1, 1)
    axes[2].set_title(
        "training spread exactly 0, left unscaled: the rise stays tiny",
        loc="left",
        fontsize=10,
    )
    for ax in axes:
        ax.axvspan(split - 0.5, t.size - 0.5, color=GRAY, alpha=0.12)
    axes[0].set_ylabel("value")
    axes[1].set_ylabel("scaled value")
    axes[2].set_ylabel("scaled value")
    axes[0].text(split + 2, axes[0].get_ylim()[1], "test", va="top", fontsize=9)
    axes[-1].set_xlabel("time step")
    save(fig, "constant-channel")


def evaluation_schemes() -> None:
    """One small figure per evaluation scheme of the splitting doc."""
    TRAIN, TEST, PAST, IDLE = BLUE, ORANGE, GREEN, "#e6e6e6"

    def cell(ax, y, x0, x1, color, text="", h=0.7, fontsize=8):
        ax.barh(y, x1 - x0, left=x0, color=color, edgecolor="white", height=h)
        if text:
            ax.text(
                (x0 + x1) / 2,
                y,
                text,
                ha="center",
                va="center",
                fontsize=fontsize,
                color="white" if color in (TRAIN, PAST) else "black",
            )

    def frame(ax, xmax, time_y, left):
        """Axes off, a time arrow, and a left margin just wide enough for the labels."""
        ax.set(xlim=(left, xmax), yticks=[], xticks=[])
        for side in ("left", "bottom"):
            ax.spines[side].set_visible(False)
        ax.annotate(
            "",
            xy=(xmax, time_y),
            xytext=(0, time_y),
            arrowprops={"arrowstyle": "->", "color": GRAY},
        )
        ax.text(
            xmax, time_y - 0.15, "time", ha="right", va="top", fontsize=8, color=GRAY
        )
        top = ax.get_ylim()[1]
        ax.set_ylim(time_y - 0.6, top)

    # 1. One split
    fig, ax = plt.subplots(figsize=(9, 1.4))
    cell(ax, 0, 0, 8, TRAIN, "train on the past")
    cell(ax, 0, 8, 10, TEST, "test")
    frame(ax, 10, -0.7, left=0)
    save(fig, "eval-one-split")

    # 2. Rolling origin
    fig, ax = plt.subplots(figsize=(9, 3.0))
    for i, cut in enumerate(range(5, 10)):
        y = 4 - i
        cell(ax, y, 0, cut, TRAIN, "train" if i == 0 else "")
        cell(ax, y, cut, cut + 1, TEST, "test")
        if cut + 1 < 10:
            cell(ax, y, cut + 1, 10, IDLE)
        ax.text(-0.2, y, f"split {i + 1}", ha="right", va="center", fontsize=8)
    frame(ax, 10, -0.8, left=-1.0)
    ax.set_title("score = average of the 5 test errors", loc="right", fontsize=9)
    save(fig, "eval-rolling-origin")

    # 3. Prequential
    fig, ax = plt.subplots(figsize=(9, 2.2))
    for k in range(6):
        if k == 0:
            cell(ax, -0.4, 0, 1, TRAIN, "learn", h=0.75)
            continue
        cell(ax, 0.4, k, k + 1, TEST, "1. predict", h=0.75)
        cell(ax, -0.4, k, k + 1, TRAIN, "2. learn", h=0.75)
    for k in range(6):
        ax.text(k + 0.5, 1.0, f"piece {k + 1}", ha="center", fontsize=8)
    ax.text(-0.2, 0.4, "first: test", ha="right", va="center", fontsize=8)
    ax.text(-0.2, -0.4, "then: train", ha="right", va="center", fontsize=8)
    frame(ax, 6, -1.1, left=-0.9)
    ax.set_ylim(-1.6, 1.3)
    save(fig, "eval-prequential")

    # 4. Every period
    fig, ax = plt.subplots(figsize=(9, 3.4))
    periods = 5
    for k in range(periods):
        y = periods - 1 - k
        for j in range(periods):
            if j < k:
                color, text = PAST, "remembered?"
            elif j == k:
                color, text = TRAIN, "latest learned"
            else:
                color, text = TEST, "not seen yet"
            cell(ax, y, 2 * j, 2 * j + 2, color, text, fontsize=7)
        learned = "period 1" if k == 0 else f"periods 1 to {k + 1}"
        ax.text(
            -0.2, y, f"after learning {learned}", ha="right", va="center", fontsize=8
        )
    for j in range(periods):
        ax.text(
            2 * j + 1,
            periods - 0.35,
            f"test on period {j + 1}",
            ha="center",
            fontsize=8,
        )
    frame(ax, 10, -0.8, left=-2.8)
    ax.set_ylim(-1.3, periods)
    save(fig, "eval-every-period")

    # 5. Controlled permutation
    fig, ax = plt.subplots(figsize=(9, 2.2))
    orders = [
        ("real order", [1, 2, 3, 4, 5, 6, 7, 8]),
        ("reordering A", [2, 1, 3, 4, 6, 5, 7, 8]),
        ("reordering B", [1, 3, 2, 4, 5, 7, 6, 8]),
    ]
    shades = plt.cm.Blues(np.linspace(0.35, 0.95, 8))
    for i, (name, order) in enumerate(orders):
        y = 2 - i
        for pos, piece in enumerate(order):
            ax.barh(
                y, 1, left=pos, color=shades[piece - 1], edgecolor="white", height=0.7
            )
            ax.text(
                pos + 0.5,
                y,
                str(piece),
                ha="center",
                va="center",
                fontsize=8,
                color="white" if piece > 4 else "black",
            )
        ax.text(-0.2, y, name, ha="right", va="center", fontsize=8)
    ax.set_title(
        "pieces numbered by real time; neighbors stay close; "
        "run the evaluation on each order",
        loc="right",
        fontsize=9,
    )
    frame(ax, 8, -0.8, left=-1.1)
    save(fig, "eval-permutation")

    # 6. State the question
    fig, axes = plt.subplots(1, 2, figsize=(10, 1.6))
    for ax, title, question in (
        (axes[0], "question A: predict what comes next?", "A"),
        (axes[1], "question B: still work on every period learned?", "B"),
    ):
        for j in range(5):
            if j < 4:
                color, text = (
                    (PAST, "learned, test") if question == "B" else (TRAIN, "learned")
                )
            else:
                color, text = (TEST, "test") if question == "A" else (IDLE, "")
            cell(ax, 0, 2 * j, 2 * j + 2, color, text)
        ax.set_ylim(-0.5, 0.5)
        ax.set_title(title, loc="left", fontsize=9)
        frame(ax, 10, -0.6, left=-0.2)
    save(fig, "eval-question")


def global_vs_window() -> None:
    """Two anomalous test windows (a level shift, a spike) next to a normal one: raw,
    scaled once with training statistics, and scaled per window. Per-window scaling
    erases the level shift but keeps the spike."""
    rng = np.random.default_rng(11)
    t = np.arange(48)
    normal = 20 + 1.5 * np.sin(2 * np.pi * t / 16) + rng.normal(0, 0.3, t.size)
    train_mean, train_std = 20.0, 1.1
    cases = [
        ("a level shift: the whole window +5", normal + 5),
        ("a spike: one value +6", normal + np.where(t == 30, 6.0, 0.0)),
    ]
    columns = [
        ("raw", lambda w: w),
        ("scaled once (training statistics)", lambda w: (w - train_mean) / train_std),
        ("scaled per window (its own statistics)", lambda w: (w - w.mean()) / w.std()),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(11, 4.6))
    for i, (case, anomalous) in enumerate(cases):
        for j, (name, scale) in enumerate(columns):
            ax = axes[i, j]
            ax.plot(t, scale(anomalous), color=RED, lw=2, label="anomalous window")
            ax.plot(
                t, scale(normal), color="black", lw=1, ls="--", label="normal window"
            )
            ax.set_xticks([])
            if i == 0:
                ax.set_title(name, fontsize=10)
            if j == 0:
                ax.set_ylabel(case, fontsize=9)
    axes[0, 2].text(
        24,
        1.9,
        "the two lines coincide:\nthe shift is gone",
        ha="center",
        fontsize=8,
        color=RED,
    )
    axes[0, 2].set_ylim(-2.3, 2.8)
    axes[0, 0].legend(fontsize=8, loc="center left", frameon=False)
    save(fig, "global-vs-window")


if __name__ == "__main__":
    sliding_windows()
    stride_overlap()
    window_count()
    forecast_window()
    split_leakage()
    per_channel_scaling()
    constant_channel()
    evaluation_schemes()
    global_vs_window()
