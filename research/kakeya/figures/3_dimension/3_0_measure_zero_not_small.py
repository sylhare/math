r"""Measure zero does not mean small (kakeya.md Section 3).

Three rulers pointed at three sets of measure zero:
  * the rationals: measure zero, yet dense (every interval holds one);
  * the Cantor set: measure zero, yet uncountable (a full interval's worth of points);
  * a Besicovitch set: measure zero, yet a unit segment in every direction.

Left: the total cover length of each set collapses to zero (each can be covered by intervals of
total length < eps). Right: what each set still contains.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/3_dimension/3_0_measure_zero_not_small.py
"""

import numpy as np
from _shared import COLORS, math_check, new_axes, save_preview


def cantor_points(depth: int) -> np.ndarray:
    """Endpoints of the Cantor middle-thirds construction at the given depth."""
    intervals = [(0.0, 1.0)]
    for _ in range(depth):
        intervals = [(a, a + (b - a) / 3) for a, b in intervals] + [(b - (b - a) / 3, b) for a, b in intervals]
    return np.array(sorted(intervals))


def main():
    depth = 7
    cantor = cantor_points(depth)
    total_len = float((cantor[:, 1] - cantor[:, 0]).sum())
    math_check(
        "measure zero is not small (Section 3)",
        [
            ("rationals in [0,1]", "measure 0 (cover by total length eps), yet dense"),
            ("Cantor set", f"measure 0 (depth-{depth} cover = {(2 / 3.0) ** depth:.2e}), yet uncountable"),
            ("Besicovitch set", "measure 0, yet a unit segment in every direction"),
            ("moral", "zero area means no thickness, not no points; dimension is the other ruler"),
        ],
    )
    assert abs(total_len - (2.0 / 3.0) ** depth) < 1e-9

    fig, ax = new_axes(2, figsize=(13.0, 5.2))
    ax[0].set_aspect("auto")
    ax[0].axis("on")

    # Left: total cover length collapsing to zero (log-log), one line per set
    eps = np.logspace(-1, -6, 60)
    ax[0].loglog(eps, eps, color=COLORS["needle"], lw=2.2, label="rationals")
    ax[0].loglog(eps, eps, color=COLORS["accent"], lw=2.2, ls="--", label="Cantor")
    ax[0].loglog(eps, eps, color=COLORS["outer"], lw=2.2, ls=":", label="Besicovitch")
    ax[0].set_xlabel("allowed total cover length (finer to the left)")
    ax[0].set_ylabel("measured length")
    ax[0].set_title("All three: cover length -> 0 (measure zero)", fontsize=11)
    ax[0].legend(fontsize=9, loc="lower right")

    # Right: what each set still contains
    ax[1].set_aspect("auto")
    ax[1].axis("on")
    rng = np.random.default_rng(3)
    rats = rng.random(500)
    ax[1].scatter(rats, np.full_like(rats, 2.0), s=6, color=COLORS["needle"], alpha=0.6)
    cpts = cantor.flatten()
    ax[1].scatter(cpts, np.full_like(cpts, 1.0), s=10, color=COLORS["accent"])
    th = np.linspace(0, np.pi, 9, endpoint=False)
    for a in th:
        ax[1].plot(
            [0.5 - 0.5 * np.cos(a), 0.5 + 0.5 * np.cos(a)],
            [0.0 - 0.18 * np.sin(a), 0.0 + 0.18 * np.sin(a)],
            color=COLORS["outer"],
            lw=1.4,
            alpha=0.8,
        )
    ax[1].set_yticks([2.0, 1.0, 0.0])
    ax[1].set_yticklabels(["rationals: dense", "Cantor: uncountable", "Besicovitch: all directions"])
    ax[1].set_ylim(-0.5, 2.5)
    ax[1].set_title("...yet each is still large in another sense", fontsize=11)

    fig.suptitle("Measure zero means no thickness, not no points", fontsize=12)
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
