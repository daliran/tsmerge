"""Draw the figures of the structure docs, in the folder above, into this folder.

usage (from the repository root; matplotlib runs in a temporary uv environment, so it
is not a project dependency):
    uv run --no-project --with matplotlib==3.10.7 --with numpy python \
        docs/research/knowledge/time-series/structure/assets/make_figures.py

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


def decomposition() -> None:
    """A series built as trend + seasonality + noise, and its three parts."""
    t = np.arange(24 * 14)
    trend = 0.02 * t
    seasonal = 2 * np.sin(2 * np.pi * t / 24)
    noise = 0.5 * RNG.standard_normal(t.size)
    parts = [
        (
            trend + seasonal + noise,
            "the series = trend + seasonality + remainder",
            GRAY,
        ),
        (trend, "trend: the long-term direction", BLUE),
        (seasonal, "seasonality: a pattern repeating every 24 steps", GREEN),
        (noise, "remainder: what's left (here, pure noise)", ORANGE),
    ]
    fig, axes = plt.subplots(4, 1, figsize=(10, 7), sharex=True)
    for ax, (y, label, color) in zip(axes, parts, strict=True):
        ax.plot(t, y, color=color, lw=1.2)
        ax.set_title(label, loc="left", fontsize=10)
        ax.set_yticks([])
    axes[-1].set_xlabel("time step (hours, 14 days)")
    save(fig, "decomposition")


def additive_multiplicative() -> None:
    """Seasonal swings of constant size vs swings that grow with the level."""
    t = np.arange(24 * 12)
    level = 10 + 0.05 * t
    season = np.sin(2 * np.pi * t / 24)
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.4), sharey=True)
    axes[0].plot(t, level + 3 * season, color=BLUE)
    axes[0].set(
        title="Additive: swings stay the same size",
        xlabel="time step",
        ylabel="value",
    )
    axes[1].plot(t, level * (1 + 0.3 * season), color=ORANGE)
    axes[1].set(title="Multiplicative: swings grow with the level", xlabel="time step")
    save(fig, "additive-multiplicative")


def seasonal_cyclic() -> None:
    """Seasonality has a fixed period; cycles rise and fall irregularly."""
    t = np.arange(400)
    seasonal = np.sin(2 * np.pi * t / 50)
    lengths = [70, 110, 60, 95, 80]
    cyclic = np.concatenate(
        [np.sin(np.linspace(0, 2 * np.pi, n, endpoint=False)) for n in lengths]
    )[: t.size]
    fig, axes = plt.subplots(2, 1, figsize=(10, 4.6), sharex=True)
    axes[0].plot(t, seasonal, color=GREEN)
    for k in range(0, 400, 50):
        axes[0].axvline(k, color=GRAY, lw=0.5, ls=":")
    axes[0].set_title(
        "Seasonal: the same period every time (here 50 steps)", loc="left", fontsize=10
    )
    axes[1].plot(t, cyclic, color=RED)
    edges = np.cumsum([0, *lengths])
    for k in edges[edges < 400]:
        axes[1].axvline(k, color=GRAY, lw=0.5, ls=":")
    axes[1].set_title(
        "Cyclic: rises and falls of varying length (70, 110, 60, 95, … steps)",
        loc="left",
        fontsize=10,
    )
    axes[1].set_xlabel("time step")
    for ax in axes:
        ax.set_yticks([])
    save(fig, "seasonal-cyclic")


def multiple_seasonality() -> None:
    """A daily and a weekly pattern in the same hourly series."""
    t = np.arange(24 * 21)
    daily = np.sin(2 * np.pi * t / 24)
    weekday = np.where((t // 24) % 7 < 5, 1.0, -1.5)
    y = 5 + daily + weekday + 0.2 * RNG.standard_normal(t.size)
    fig, ax = plt.subplots(figsize=(11, 3))
    ax.plot(t, y, color=BLUE, lw=1)
    for d in range(0, t.size, 24 * 7):
        ax.axvspan(d + 24 * 5, d + 24 * 7, color=GRAY, alpha=0.15)
    ax.set(
        title="Two seasonalities: a daily pattern, and lower weekends (shaded)",
        xlabel="time step (hours, 3 weeks)",
    )
    ax.set_yticks([])
    save(fig, "multiple-seasonality")


def stationarity() -> None:
    """A stationary series vs two non-stationary ones."""
    n = 300
    white = RNG.standard_normal(n)
    walk = np.cumsum(RNG.standard_normal(n))
    trended = 0.03 * np.arange(n) + RNG.standard_normal(n)
    cases = [
        (white, "Stationary: same mean and spread everywhere (white noise)", GREEN),
        (trended, "Not stationary: the mean drifts upward (trend)", RED),
        (walk, "Not stationary: wanders with no fixed level (random walk)", RED),
    ]
    fig, axes = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
    for ax, (y, label, color) in zip(axes, cases, strict=True):
        ax.plot(y, color=color, lw=1)
        ax.set_title(label, loc="left", fontsize=10)
        ax.set_yticks([])
    axes[-1].set_xlabel("time step")
    save(fig, "stationarity")


def autocorrelation() -> None:
    """The autocorrelation of a seasonal series: peaks at the seasonal lags."""
    t = np.arange(24 * 20)
    y = np.sin(2 * np.pi * t / 24) + 0.5 * RNG.standard_normal(t.size)
    y = y - y.mean()
    lags = np.arange(0, 73)
    acf = np.array([np.sum(y[k:] * y[: y.size - k]) for k in lags]) / np.sum(y * y)
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.bar(lags, acf, width=0.6, color=BLUE)
    for k in (24, 48, 72):
        ax.annotate(
            f"lag {k}",
            (k, acf[k]),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=9,
            color=RED,
        )
    ax.axhline(0, color="black", lw=0.6)
    ax.set(
        title="Autocorrelation of a series with daily seasonality: peaks every 24 lags",
        xlabel="lag (steps between the two values compared)",
        ylabel="autocorrelation",
    )
    save(fig, "autocorrelation")


if __name__ == "__main__":
    decomposition()
    additive_multiplicative()
    seasonal_cyclic()
    multiple_seasonality()
    stationarity()
    autocorrelation()
