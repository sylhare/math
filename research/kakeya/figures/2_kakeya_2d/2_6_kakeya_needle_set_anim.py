"""Animation: the Kakeya needle set (Wikipedia image), built up by increasing granularity.

The Wikipedia "Kakeya needle set" picture is a small triangular core with THREE dense sprays of
needles fanning outward from its three corners (up, down-left, down-right) at 120 degrees: it is a
Besicovitch set drawn as its needle family, and the three sprays are the three rotated Perron trees
that make up the set (Besicovitch set = three rotations of a Perron tree from an equilateral
triangle; confirmed against the Wikipedia "Kakeya set" article and the Indiana University math
gallery).  A true Besicovitch set has area 0 (a limit, ~1/log N Keich decay) and cannot be drawn;
the exact small-area construction is the Perron tree / Pal join in 2_4 and 2_5.  This figure is the
"what it looks like" payoff, a POSITIONAL APPROXIMATION.

Why three sprays at the corners: anchor a unit needle for each direction at the core's SUPPORT point
(the corner farthest in that direction) and let it stick out.  For a triangle the support corner is
fixed over a 120 degree range of directions, so each corner emits a 120 degree fan; the three fans
overlap to cover every direction.  That is exactly the three-tree silhouette of the Wikipedia image.

We do NOT build it one needle at a time.  Every frame draws the WHOLE shape and adds granularity
(more directions), so the coarse three-pronged star sharpens into the dense Wikipedia sunburst.

Run: uv run --with matplotlib \
     python research/kakeya/figures/2_kakeya_2d/2_6_kakeya_needle_set_anim.py
"""
import math

import numpy as np
from _shared import COLORS, SQRT3, math_check, save_gif
from matplotlib.collections import PolyCollection

RC = 0.30       # core radius: centre -> corner of the small equilateral core
LEN = 0.95      # needle length (~ unit); sticks out well past the small core
HALFW = 0.006   # half-width of a drawn needle sliver
CORE = "#f4ec7a"
EDGE = "#5f5f2a"

# granularity schedule: number of directions per frame (coarse -> fine), then hold on the finished set
GRAN = [12, 16, 21, 28, 37, 49, 64, 84, 110, 145, 190, 250]
GRAN = GRAN + [GRAN[-1]] * 8

VERTS = np.array([[RC * math.cos(math.radians(d)), RC * math.sin(math.radians(d))] for d in (90, 210, 330)])


def sliver_quads(m: int):
    """One needle per direction (m directions over the full turn): a thin sliver anchored at the core
    corner farthest in that direction, sticking out by LEN."""
    quads = []
    for th in np.linspace(0.0, 2 * math.pi, m, endpoint=False):
        d = np.array([math.cos(th), math.sin(th)])
        anchor = VERTS[int(np.argmax(VERTS @ d))]
        tip = anchor + LEN * d
        perp = np.array([-d[1], d[0]]) * HALFW
        quads.append([anchor - perp, anchor + perp, tip + perp, tip - perp])
    return quads


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    # --- checks (approximation is deliberate; assert refinement + full direction coverage) ---------
    assert all(GRAN[i] <= GRAN[i + 1] for i in range(len(GRAN) - 1)) and GRAN[-1] >= 200, "granularity must rise"
    dirs_fine = np.linspace(0.0, math.pi, GRAN[-1], endpoint=False)  # distinct line directions in [0,180)
    gaps = np.diff(np.sort(dirs_fine % math.pi))
    assert np.max(gaps) < math.radians(2.0), "finest set must have a needle within ~2 deg of every direction"
    core_area = 3.0 * SQRT3 / 4.0 * RC ** 2  # area of the equilateral core (side = RC*sqrt3)

    math_check(
        "Kakeya needle set (Wikipedia image, refined by granularity)",
        [
            ("granularity schedule", f"{GRAN[0]} -> {GRAN[-1]} directions over the full turn"),
            ("shape", "small triangular core + three 120-deg needle sprays at its corners (= 3 Perron trees)"),
            ("directions at finest", f"{GRAN[-1]}  (a needle within {math.degrees(np.max(gaps)):.1f} deg of every direction)"),
            ("needle length", f"{LEN:.2f}  (~unit; sticks out past the core of radius {RC})"),
            ("core area", f"{core_area:.3f}  (small central overlap; the spikes are the needle family)"),
            ("nature of this figure", "positional approximation of the Besicovitch needle set (exact small-area math in 2_4/2_5)"),
            ("true Besicovitch area", "-> 0 as N->inf, but only ~1/log N (Keich): not drawable"),
        ],
    )

    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    ax.set_aspect("equal")
    ax.axis("off")
    lim = RC + LEN + 0.12
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_title("Kakeya needle set: a needle in every direction, from a small core", fontsize=10)

    ax.fill(VERTS[:, 0], VERTS[:, 1], facecolor=CORE, edgecolor="none", zorder=3)  # the core, drawn once
    counter = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top", fontsize=10, color=COLORS["guide"])
    holder = {"pc": None}

    def update(i):
        if holder["pc"] is not None:
            holder["pc"].remove()
        m = GRAN[i]
        pc = PolyCollection(sliver_quads(m), facecolors=CORE, edgecolors=EDGE, linewidths=0.35, zorder=2)
        ax.add_collection(pc)
        holder["pc"] = pc
        counter.set_text(f"granularity: {m} directions")
        return [pc, counter]

    anim = FuncAnimation(fig, update, frames=len(GRAN), interval=180, blit=False)
    print("wrote", save_gif(anim, fps=6, dpi=95))


if __name__ == "__main__":
    main()
