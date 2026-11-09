"""Draw the figures of the anomaly-detection docs, in the folder above, into this one.

usage (from the repository root; matplotlib runs in a temporary uv environment, so it
is not a project dependency):
    uv run --no-project --with matplotlib==3.10.7 --with numpy python \
        docs/research/knowledge/anomaly-detection/assets/make_figures.py

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


def anomaly_types() -> None:
    """Point, contextual and collective anomalies."""
    t = np.arange(240)
    base = np.sin(2 * np.pi * t / 48) + 0.1 * RNG.standard_normal(t.size)
    point, contextual, collective = base.copy(), base.copy(), base.copy()
    point[100] += 2.5
    contextual[84] = 0.95  # one peak-level value at the bottom of a trough (step 84)
    collective[130:160] = 0.05 * RNG.standard_normal(30)  # the rhythm stops
    cases = [
        (point, "Point: one value far from all the others", (100, 101)),
        (
            contextual,
            "Contextual: a peak-level value, in the middle of a trough",
            (84, 85),
        ),
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


def anomaly_types_images() -> None:
    """The three kinds of anomalies on synthetic images: a scratched part among
    intact ones, a patch of sky color in the grass, a shifted patch in a weave."""
    fig = plt.figure(figsize=(11, 3.8), layout="constrained")
    left, middle, right = fig.subfigures(1, 3, width_ratios=[1, 1.15, 1.15])

    # Point: six photos of a round part; one has a scratch.
    yy, xx = np.mgrid[-1:1:64j, -1:1:64j]
    for i, ax in enumerate(left.subplots(2, 3).flat):
        part = np.where(xx**2 + yy**2 < 0.6, 0.8, 0.15)
        part = part + 0.04 * RNG.standard_normal(part.shape)
        if i == 4:
            scratch = (np.abs(yy - 0.6 * xx - 0.05) < 0.04) & (xx**2 + yy**2 < 0.5)
            part[scratch] = 0.25
            for side in ax.spines.values():
                side.set(color=RED, linewidth=3, visible=True)
        ax.imshow(part, cmap="gray", vmin=0, vmax=1)
        ax.set(xticks=[], yticks=[])
    left.suptitle("Point: one scratched part\namong intact ones", weight="bold")

    # Contextual: sky above, grass below; a patch of sky color in the grass.
    ax = middle.subplots()
    scene = np.zeros((60, 90, 3))
    scene[:30] = (0.55, 0.75, 0.95)  # sky
    scene[30:] = (0.35, 0.65, 0.3)  # grass
    scene += 0.03 * RNG.standard_normal(scene.shape)
    scene[42:50, 55:65] = (0.55, 0.75, 0.95)  # sky color, in the grass
    ax.imshow(np.clip(scene, 0, 1))
    ax.add_patch(Rectangle((52.5, 39.5), 15, 13, fill=False, ec=RED, lw=2))
    ax.set(xticks=[], yticks=[])
    middle.suptitle("Contextual: a normal color,\nin the wrong place", weight="bold")

    # Collective: wide diagonal stripes; one patch is shifted by half a stripe.
    ax = right.subplots()
    r, c = np.mgrid[0:60, 0:90]
    weave = np.where(((c + r) // 8) % 2 == 0, 0.8, 0.2)
    shifted = np.where(((c + r + 8) // 8) % 2 == 0, 0.8, 0.2)
    patch = (r >= 18) & (r < 42) & (c >= 36) & (c < 66)
    weave[patch] = shifted[patch]
    ax.imshow(weave, cmap="gray", vmin=0, vmax=1)
    ax.add_patch(Rectangle((33.5, 15.5), 35, 29, fill=False, ec=RED, lw=2))
    ax.set(xticks=[], yticks=[])
    right.suptitle(
        "Collective: each pixel is normal,\nthe pattern breaks", weight="bold"
    )
    fig.savefig(
        OUT / "anomaly-types-images.png", bbox_inches="tight", facecolor="white"
    )
    plt.close(fig)
    print("wrote anomaly-types-images.png")


if __name__ == "__main__":
    anomaly_types()
    anomaly_types_images()
