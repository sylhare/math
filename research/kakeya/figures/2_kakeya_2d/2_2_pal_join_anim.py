"""Animation: the Pal join (Pal worm) detour (beat 2d of ../kakeya.md).

Mirrors pal_join.py in motion. A unit needle travels continuously from needle G1 (on the line y=0)
to the parallel needle G2 (on y=GAP) by a FAR detour that keeps the swept area tiny:

  1. slide out along its own axis by D          (sliding along the axis sweeps ~0 area)
  2. rotate up by a small angle phi about the far trailing end   (a thin sector, area phi/2)
  3. slide along the tilted axis until it has crossed the gap    (~0 area)
  4. rotate back down by phi                                     (a thin sector, area phi/2)
  5. slide home along -x to land on G2                           (~0 area)

The needle is drawn bold at its current position; past positions accumulate faintly and the swept
region (union of the quads between consecutive needle positions) fills in and its measured area is
read out live.

Because the two turns happen a distance ~D out, the needle only turns through
phi(D) = 2*arctan(g/2D), so the whole swept area A(D) ~ phi(D) -> 0 as D grows.

INVARIANT: the needle length is exactly 1 in every frame (geometric honesty). The final measured
swept area is small; both are printed. This is a SCHEMATIC of a concrete maneuver; the rigorous
lemma is area(J) < eps for every eps > 0 (the limit D -> inf), not the area of any one picture.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/pal_join_anim.py
"""
import math
from itertools import pairwise

import numpy as np
from _shared import COLORS, math_check, new_axes, save_gif
from matplotlib.animation import FuncAnimation
from shapely.geometry import Polygon
from shapely.ops import unary_union

GAP = 0.3          # fixed lateral gap between the two parallel unit needles (lines y=0 and y=GAP)
LEN = 1.0          # needle length (fixed; geometric honesty)
D = 3.0            # detour distance
NPHASE = 20        # samples per phase -> ~100 needle positions, one frame each


def maneuver_needles(d: float, nphase: int) -> list[np.ndarray]:
    """Sampled needle endpoints [[trail],[tip]] along the full Pal-join maneuver (always length 1)."""
    phi = 2.0 * math.atan(GAP / (2.0 * d))
    needles: list[np.ndarray] = []

    def add(trail, ang):
        tip = trail + LEN * np.array([math.cos(ang), math.sin(ang)])
        needles.append(np.array([trail, tip]))

    for x in np.linspace(0.0, d, nphase):                      # 1. slide out along +x
        add(np.array([x, 0.0]), 0.0)
    piv = np.array([d, 0.0])
    for a in np.linspace(0.0, phi, nphase):                    # 2. rotate up about far end
        add(piv, a)
    s = GAP / math.sin(phi)
    for u in np.linspace(0.0, s, nphase):                      # 3. slide along tilted axis
        add(piv + u * np.array([math.cos(phi), math.sin(phi)]), phi)
    piv2 = piv + s * np.array([math.cos(phi), math.sin(phi)])
    for a in np.linspace(phi, 0.0, nphase):                    # 4. rotate back down
        add(piv2, a)
    for x in np.linspace(piv2[0], 0.0, nphase):                # 5. slide home to land on G2
        add(np.array([x, GAP]), 0.0)
    return needles


def main():
    needles = maneuver_needles(D, NPHASE)
    phi = 2.0 * math.atan(GAP / (2.0 * D))

    # cumulative swept region (union of quads between consecutive positions) and its area per frame
    quads = []
    for a, b in pairwise(needles):
        q = Polygon([a[0], a[1], b[1], b[0]]).buffer(0)        # buffer(0) fixes bow-tie quads
        if not q.is_empty:
            quads.append(q)
    swept_per_frame = [unary_union(quads[:i]) if i else Polygon() for i in range(len(needles))]
    area_per_frame = [g.area for g in swept_per_frame]
    final_area = area_per_frame[-1]

    # --- INVARIANT: needle length == 1 in every frame ---
    lengths = [float(np.linalg.norm(nd[1] - nd[0])) for nd in needles]
    len_ok = max(abs(length - LEN) for length in lengths) < 1e-9

    math_check(
        "Pal join: unit needle travels the detour G1 -> G2",
        [
            ("gap g (fixed), needle length L", f"g = {GAP}, L = {LEN}"),
            ("detour distance D", f"{D:g}"),
            ("turn angle phi = 2 arctan(g/2D)", f"{math.degrees(phi):.1f} deg = {phi:.4f} rad"),
            ("predicted area ~ phi(D)", f"{phi:.4f}"),
            ("MEASURED final swept area", f"{final_area:.4f}  (small; -> 0 as D -> inf)"),
            ("needle length min/max (all frames)", f"{min(lengths):.6f} / {max(lengths):.6f}  (want 1.000000)"),
            ("needle length == 1 every frame?", f"{len_ok}"),
            ("status", "schematic; lemma area < eps is rigorous (limit D -> inf, for every eps > 0)"),
        ],
    )
    assert len_ok, "needle length must be exactly 1 in every frame"

    # --- animation ---
    fig, ax = new_axes(1, figsize=(11, 3.4))
    allpts = np.array(needles).reshape(-1, 2)
    xpad, ypad = 0.15, 0.2
    xlim = (allpts[:, 0].min() - xpad, allpts[:, 0].max() + xpad)
    ylim = (allpts[:, 1].min() - ypad, allpts[:, 1].max() + ypad)

    def update(i):
        ax.clear(); ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(*xlim); ax.set_ylim(*ylim)
        # accumulated swept region
        g = swept_per_frame[i]
        if not g.is_empty:
            geoms = g.geoms if g.geom_type == "MultiPolygon" else [g]
            for gg in geoms:
                if gg.area > 0:
                    ax.fill(*gg.exterior.xy, color=COLORS["region"], alpha=0.7, edgecolor="none")
        # faint trail of past needle positions
        for nd in needles[: i + 1: max(1, (i + 1) // 40)]:
            ax.plot(nd[:, 0], nd[:, 1], color=COLORS["needle"], lw=0.5, alpha=0.3)
        # the two parallel unit needles G1, G2
        ax.plot([0, 1], [0, 0], color=COLORS["accent"], lw=3.0, solid_capstyle="round")
        ax.plot([0, 1], [GAP, GAP], color=COLORS["accent"], lw=3.0, solid_capstyle="round")
        ax.text(0.5, -0.14, "$G_1$", color=COLORS["accent"], ha="center", fontsize=12)
        ax.text(0.5, GAP + 0.08, "$G_2$", color=COLORS["accent"], ha="center", fontsize=12)
        # the live needle (bold, length 1)
        nd = needles[i]
        ax.plot(nd[:, 0], nd[:, 1], color=COLORS["needle"], lw=2.6, solid_capstyle="round")
        ax.set_title("Pal join: far detour, tiny swept area", fontsize=12)
        ax.text(0.01, 0.97,
                f"D = {D:g}   needle length = 1\nswept area = {area_per_frame[i]:.3f}  (schematic; lemma area < eps is rigorous)",
                transform=ax.transAxes, va="top", ha="left", fontsize=9, color=COLORS["guide"])
        return []

    anim = FuncAnimation(fig, update, frames=len(needles), interval=70, blit=False)
    print("wrote", save_gif(anim, fps=16, dpi=95))


if __name__ == "__main__":
    main()
