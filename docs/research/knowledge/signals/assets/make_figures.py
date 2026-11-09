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
        xlabel="position in the sequence",
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
    axes[1].set(
        title="2. Sampled: discrete time", xlabel="time (s), one sample every 0.04 s"
    )

    axes[2].plot(t, x, color=GRAY, alpha=0.35)
    for q in np.arange(-1.5, 1.51, levels):
        axes[2].axhline(q, color=GRAY, lw=0.4, alpha=0.5)
    axes[2].stem(n, xq, linefmt=ORANGE, markerfmt="o", basefmt=" ")
    axes[2].set(
        title="3. Sampled + quantized: digital",
        xlabel="time (s), one sample every 0.04 s",
    )
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


def nyquist_reconstruction() -> None:
    """A signal with no frequency above 3 Hz, rebuilt from its samples with the
    Whittaker-Shannon (sinc) formula: exact above 6 samples per second, wrong below."""
    t = np.linspace(0, 2, 2000)

    def signal(x):
        return np.sin(2 * np.pi * 1 * x) + 0.6 * np.sin(2 * np.pi * 3 * x + 0.5)

    fig, axes = plt.subplots(2, 1, figsize=(9, 5.2), sharex=True)
    for ax, fs, ok in ((axes[0], 8, True), (axes[1], 4, False)):
        # Samples well beyond the plotted span, so the finite sum is accurate inside it.
        n = np.arange(-20, 22, 1 / fs)
        rebuilt = np.sinc((t[:, None] - n[None, :]) * fs) @ signal(n)
        shown = (n >= 0) & (n <= 2)
        ax.plot(t, signal(t), color=GRAY, lw=3, alpha=0.5, label="original signal")
        ax.plot(
            t,
            rebuilt,
            color=GREEN if ok else RED,
            ls="-" if ok else "--",
            label="rebuilt from the samples",
        )
        ax.plot(n[shown], signal(n[shown]), "o", color=BLUE, ms=6, label="samples")
        verdict = (
            "more than 2B = 6: rebuilt exactly" if ok else "fewer than 2B = 6: wrong"
        )
        ax.set_title(f"{fs} samples per second, {verdict}", loc="left", fontsize=10)
        ax.set_ylabel("value")
        ax.set_ylim(-2.2, 2.4)
        ax.legend(loc="upper right", fontsize=8, ncols=3)
    axes[1].set_xlabel("time (s)")
    fig.suptitle(
        "A signal with no frequency above B = 3 Hz, rebuilt from its samples",
        fontweight="bold",
    )
    save(fig, "nyquist-reconstruction")


def fourier_sum() -> None:
    """A signal made of three sine waves, and its spectrum: one peak per wave."""
    fs, seconds = 100, 2
    t = np.arange(0, seconds, 1 / fs)
    parts = [(2, 1.0), (5, 0.5), (11, 0.3)]
    waves = [a * np.sin(2 * np.pi * f * t) for f, a in parts]
    x = np.sum(waves, axis=0)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), width_ratios=[1.4, 1])
    for (f, a), w, c in zip(parts, waves, (BLUE, ORANGE, GREEN), strict=True):
        axes[0].plot(t, w - 3, color=c, lw=1, label=f"{f} Hz, strength {a}")
    axes[0].plot(t, x + 1.5, color="black", lw=1.4, label="their sum: the signal")
    axes[0].set(
        xlabel="time (s)", yticks=[], title="Time domain: the signal and its parts"
    )
    axes[0].legend(loc="upper right", fontsize=7, ncols=2)
    axes[0].set_ylim(-4.6, 4.2)
    freqs = np.fft.rfftfreq(t.size, 1 / fs)
    strength = 2 * np.abs(np.fft.rfft(x)) / t.size
    axes[1].stem(freqs, strength, basefmt=" ", markerfmt=".", linefmt=GRAY)
    for f, a in parts:
        axes[1].annotate(f"{f} Hz", (f, a), textcoords="offset points", xytext=(4, 4))
    axes[1].set(
        xlabel="frequency (Hz)",
        ylabel="strength",
        xlim=(0, 20),
        title="Frequency domain: one peak per wave",
    )
    save(fig, "fourier-sum")


def fourier_periods() -> None:
    """An hourly signal with daily and weekly repeating patterns, and its spectrum."""
    hours = np.arange(24 * 7 * 8)  # eight weeks
    x = (
        np.sin(2 * np.pi * hours / 24)
        + 0.6 * np.sin(2 * np.pi * hours / 168)
        + 0.3 * RNG.standard_normal(hours.size)
    )
    fig, axes = plt.subplots(2, 1, figsize=(9, 5.2))
    axes[0].plot(hours / 24, x, color=BLUE, lw=0.7)
    axes[0].set(
        xlabel="time (days)",
        ylabel="value",
        title="Eight weeks of an hourly signal: daily and weekly patterns, noise",
    )
    per_day = np.fft.rfftfreq(hours.size, 1 / 24)  # cycles per day
    strength = 2 * np.abs(np.fft.rfft(x)) / hours.size
    axes[1].plot(per_day, strength, color=BLUE, lw=1)
    for f, label in (
        (1 / 7, "weekly: 1 cycle every 7 days"),
        (1, "daily: 1 cycle per day"),
    ):
        k = np.argmin(np.abs(per_day - f))
        axes[1].annotate(
            label,
            (per_day[k], strength[k]),
            textcoords="offset points",
            xytext=(8, -4),
            fontsize=9,
        )
    axes[1].set(
        xlabel="frequency (cycles per day)",
        ylabel="strength",
        xlim=(0, 3),
        title="Its spectrum: one peak per repeating pattern",
    )
    save(fig, "fourier-periods")


if __name__ == "__main__":
    signal_examples()
    analog_to_digital()
    aliasing()
    nyquist_reconstruction()
    fourier_sum()
    fourier_periods()
