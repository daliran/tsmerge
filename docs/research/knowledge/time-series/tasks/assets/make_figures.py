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


def daily(t, noise=0.15):
    """An hourly series with a daily pattern, a slight trend and noise."""
    return np.sin(2 * np.pi * t / 24) + 0.004 * t + noise * RNG.standard_normal(t.size)


def forecasting_example() -> None:
    """The context, the forecast for the horizon with a widening band, and the truth."""
    t = np.arange(168)
    y = daily(t)
    L = 120
    h = t[L:]
    forecast = np.sin(2 * np.pi * h / 24) + 0.004 * h
    band = 0.12 * np.sqrt(np.arange(1, h.size + 1))
    fig, ax = plt.subplots(figsize=(10, 3.4))
    ax.plot(t[:L], y[:L], color=BLUE, label="the past: the context (given)")
    ax.plot(h, y[L:], color=GRAY, ls="--", label="what really happened")
    ax.plot(h, forecast, color=ORANGE, lw=2, label="the forecast")
    ax.fill_between(
        h,
        forecast - band,
        forecast + band,
        color=ORANGE,
        alpha=0.2,
        label="uncertainty: grows with the horizon",
    )
    ax.axvline(L - 0.5, color="black", lw=0.8)
    ax.text(L / 2, 2.6, "context", ha="center")
    ax.text(L + (t.size - L) / 2, 2.6, "horizon", ha="center")
    ax.set(xlabel="time step (hours)", ylabel="value", ylim=(-2.4, 3.0))
    ax.legend(loc="lower left", fontsize=8, ncols=2)
    save(fig, "forecasting-example")


def imputation_example() -> None:
    """A series with two gaps, the values filled in, and the hidden truth."""
    t = np.arange(200)
    y = daily(t)
    gaps = ((t >= 40) & (t < 56)) | ((t >= 120) & (t < 152))
    filled = np.sin(2 * np.pi * t / 24) + 0.004 * t
    fig, ax = plt.subplots(figsize=(10, 3.2))
    observed = np.where(gaps, np.nan, y)
    ax.plot(t, observed, color=BLUE, label="observed")
    ax.plot(
        t, np.where(gaps, y, np.nan), color=GRAY, ls="--", label="missing: the truth"
    )
    ax.plot(t, np.where(gaps, filled, np.nan), color=ORANGE, lw=2, label="filled in")
    for start, end in ((40, 56), (120, 152)):
        ax.axvspan(start - 0.5, end - 0.5, color=GRAY, alpha=0.12)
    ax.set(xlabel="time step (hours)", ylabel="value", ylim=(-1.8, 2.6))
    ax.legend(loc="upper left", fontsize=8, ncols=3)
    save(fig, "imputation-example")


def anomaly_detection_example() -> None:
    """A series, its anomaly score per step, and the threshold that flags steps."""
    t = np.arange(240)
    expected = np.sin(2 * np.pi * t / 48)
    y = expected + 0.1 * RNG.standard_normal(t.size)
    y[70] += 2.0  # a point anomaly
    y[150:175] = 0.05 * RNG.standard_normal(25)  # a collective one: the rhythm stops
    score = np.convolve(np.abs(y - expected), np.ones(3) / 3, mode="same")
    threshold = 0.35
    flagged = score > threshold
    fig, axes = plt.subplots(2, 1, figsize=(10, 4.6), sharex=True)
    axes[0].plot(t, y, color=BLUE)
    axes[0].set(ylabel="value", title="the series")
    axes[1].plot(t, score, color=GRAY)
    axes[1].axhline(threshold, color=RED, ls="--", label="threshold")
    axes[1].set(
        xlabel="time step",
        ylabel="score",
        title="the anomaly score per step; above the threshold, the step is flagged",
    )
    axes[1].legend(loc="upper right", fontsize=8)
    for ax in axes:
        for k in np.flatnonzero(flagged):
            ax.axvspan(k - 0.5, k + 0.5, color=RED, alpha=0.15, lw=0)
    save(fig, "anomaly-detection-example")


def classification_example() -> None:
    """Short motion recordings of three activities: one label per recording."""
    t = np.arange(100)
    kinds = [
        ("walking", lambda: np.sin(2 * np.pi * t / 25)),
        ("running", lambda: 2 * np.sin(2 * np.pi * t / 10)),
        (
            "cycling",
            lambda: 0.8 * np.sin(2 * np.pi * t / 18) + 0.4 * np.sin(2 * np.pi * t / 9),
        ),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(10, 4), sharey=True)
    for col, (label, make) in enumerate(kinds):
        for row in range(2):
            x = make() + 0.2 * RNG.standard_normal(t.size)
            axes[row, col].plot(t, x, color=[BLUE, ORANGE, GREEN][col], lw=1)
            axes[row, col].set_title(f"label: {label}", fontsize=10)
            axes[row, col].set_yticks([])
            if row == 1:
                axes[row, col].set_xlabel("time step")
    fig.suptitle(
        "Each recording gets one label: walking, running or cycling", fontweight="bold"
    )
    save(fig, "classification-example")


if __name__ == "__main__":
    tasks()
    forecasting_example()
    imputation_example()
    anomaly_detection_example()
    classification_example()
