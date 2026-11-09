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
    """A series built as trend-cycle + seasonality + remainder, and its parts. The
    trend-cycle panel shows the smooth trend (dashed) and the cycle around it."""
    t = np.arange(24 * 14)
    trend = 0.02 * t
    # The cycle: rises and falls of irregular length (80, 120, 60, 76 steps).
    cycle = np.concatenate(
        [
            sign * 1.5 * np.sin(np.pi * np.arange(n) / n)
            for sign, n in zip((1, -1, 1, -1), (80, 120, 60, 76), strict=True)
        ]
    )
    seasonal = 2 * np.sin(2 * np.pi * t / 24)
    noise = 0.5 * RNG.standard_normal(t.size)
    fig, axes = plt.subplots(4, 1, figsize=(10, 7.5), sharex=True)
    axes[0].plot(t, trend + cycle + seasonal + noise, color=GRAY, lw=1.2)
    axes[0].set_title(
        "the series = trend-cycle + seasonality + remainder", loc="left", fontsize=10
    )
    axes[1].plot(t, trend, color=BLUE, lw=1.2, ls="--", label="trend")
    axes[1].plot(t, trend + cycle, color=BLUE, lw=1.6, label="trend + cycle")
    axes[1].set_title(
        "trend-cycle: the long-term direction (dashed), plus slow waves of irregular "
        "length (the cycle)",
        loc="left",
        fontsize=10,
    )
    axes[1].legend(loc="upper left", fontsize=8)
    axes[2].plot(t, seasonal, color=GREEN, lw=1.2)
    axes[2].set_title(
        "seasonality: a pattern repeating every 24 steps", loc="left", fontsize=10
    )
    axes[3].plot(t, noise, color=ORANGE, lw=1.2)
    axes[3].set_title(
        "remainder: what's left (here, pure noise)", loc="left", fontsize=10
    )
    for ax in axes:
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


def smoothing_window() -> None:
    """One series, its trend-cycle estimated with a small and a large moving average:
    the small window keeps the cycle, the large one leaves it in the remainder."""
    t = np.arange(24 * 14)
    trend = 0.02 * t
    cycle = np.concatenate(
        [
            sign * 1.5 * np.sin(np.pi * np.arange(n) / n)
            for sign, n in zip((1, -1, 1, -1, 1), (70, 60, 80, 56, 70), strict=True)
        ]
    )
    seasonal = 2 * np.sin(2 * np.pi * t / 24)
    noise = 0.4 * RNG.standard_normal(t.size)
    y = trend + cycle + seasonal + noise

    def centered_ma(x, m):
        """2xm moving average: cancels a seasonality of period m (m even)."""
        w = np.ones(m + 1)
        w[0] = w[-1] = 0.5
        out = np.full(x.size, np.nan)
        out[m // 2 : x.size - m // 2] = np.convolve(x, w / m, mode="valid")
        return out

    fig = plt.figure(figsize=(11, 7), layout="constrained")
    grid = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1])
    top = fig.add_subplot(grid[0, :])
    top.plot(t, y, color=GRAY, lw=1)
    top.set_title(
        "the series: trend + cycle + daily seasonality + noise", loc="left", fontsize=10
    )
    for col, (m, name) in enumerate(
        (
            (24, "small window: 2x24 moving average"),
            (168, "large window: 2x168 moving average"),
        )
    ):
        tc = centered_ma(y, m)
        ax = fig.add_subplot(grid[1, col])
        ax.plot(t, trend + cycle, color=GRAY, ls="--", lw=1, label="true trend + cycle")
        ax.plot(t, tc, color=BLUE, lw=1.6, label="estimated trend-cycle")
        ax.set_title(f"{name}\ntrend-cycle", loc="left", fontsize=10)
        ax.legend(loc="upper left", fontsize=7)
        ax2 = fig.add_subplot(grid[2, col], sharex=ax)
        ax2.plot(t, y - tc - seasonal, color=ORANGE, lw=1)
        ax2.set_ylim(-3, 3)
        verdict = "only noise" if m == 24 else "the cycle is here, with the noise"
        ax2.set_title(f"remainder: {verdict}", loc="left", fontsize=10)
        ax2.set_xlabel("time step (hours, 14 days)")
        for a in (ax, ax2):
            a.set_yticks([])
    top.set_yticks([])
    fig.savefig(OUT / "smoothing-window.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote smoothing-window.png")


def to_stationary() -> None:
    """Three non-stationary series and the transformation that makes each stationary:
    differencing, seasonal differencing, logarithm then seasonal differencing."""
    t = np.arange(24 * 10)
    trend = 0.05 * t + np.cumsum(0.3 * RNG.standard_normal(t.size))
    seasonal = (
        0.03 * t + 2 * np.sin(2 * np.pi * t / 24) + 0.3 * RNG.standard_normal(t.size)
    )
    growing = np.exp(0.008 * t) * (1 + 0.4 * np.sin(2 * np.pi * t / 24))
    growing = growing * np.exp(0.05 * RNG.standard_normal(t.size))
    rows = [
        (trend, "a trend", np.diff(trend), "differencing: $y_t - y_{t-1}$"),
        (
            seasonal,
            "a trend and a daily seasonality",
            seasonal[24:] - seasonal[:-24],
            "seasonal differencing: $y_t - y_{t-24}$",
        ),
        (
            growing,
            "swings growing with the level",
            np.log(growing)[24:] - np.log(growing)[:-24],
            "logarithm, then seasonal differencing",
        ),
    ]
    fig, axes = plt.subplots(3, 2, figsize=(11, 7), sharex=True)
    for row, (before, what, after, how) in zip(axes, rows, strict=True):
        row[0].plot(t, before, color=RED, lw=1)
        row[0].set_title(f"not stationary: {what}", loc="left", fontsize=10)
        row[1].plot(t[t.size - after.size :], after, color=GREEN, lw=1)
        row[1].set_title(f"stationary after {how}", loc="left", fontsize=10)
        for ax in row:
            ax.set_yticks([])
    for ax in axes[-1]:
        ax.set_xlabel("time step (hours, 10 days)")
    save(fig, "to-stationary")


if __name__ == "__main__":
    decomposition()
    additive_multiplicative()
    seasonal_cyclic()
    multiple_seasonality()
    stationarity()
    autocorrelation()
    smoothing_window()
    to_stationary()
