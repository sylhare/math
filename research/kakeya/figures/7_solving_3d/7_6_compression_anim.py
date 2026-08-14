"""Animation: the Besicovitch compression phenomenon measured (kakeya.md 7d).

The Perron cut-and-shift pile (the same sprout(n) as 2_7 / 4_2) keeps 2^n triangle pieces and only
translates them. Translation preserves area, so the sum of the piece areas is pinned at the original
triangle area A_0 for every depth, while the measured union area falls like 1/log N. Their ratio
is the compression factor:

    content    S_n = sum_i |P_i| = A_0          (flat; the "areas sum to >= 1" side)
    footprint  U_n = | union_i P_i | -> 0        (the "union has measure < eta" side, ~ 1/log N)
    compression C_n = S_n / U_n -> infinity       (total content pressed into a shrinking footprint)

This is Zahl's Besicovitch compression phenomenon: total tube-content ~ 1, actual footprint < eta.
The decay is only 1/log N, so on screen the ratio climbs modestly (about 1.3x -> 4x), matching 2f.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/7_solving_3d/7_6_compression_anim.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

SIDE = 1.0
R = SIDE / math.sqrt(3.0)
CORNERS_DEG = (90.0, 210.0, 330.0)
DEPTHS = list(range(1, 9))  # subdivision depth n = 1..8 (N = 2^n pieces)
HOLD = 6
END_HOLD = 8

VERTS = np.array([R * np.array([math.cos(math.radians(d)), math.sin(math.radians(d))]) for d in CORNERS_DEG])
_EDIR = (VERTS[2] - VERTS[1]) / np.linalg.norm(VERTS[2] - VERTS[1])


# Geometry: the exact sprout(n) cut-and-shift from 2_7 / 4_2
def sprout(n):
    """Perron cut-and-shift of the core triangle to depth n; returns the 2^n translated
    sub-triangle pieces whose union is the shrunk core (each piece keeps its area)."""
    v0, v1, v2 = VERTS
    if n == 0:
        return [Polygon([tuple(v0), tuple(v1), tuple(v2)])]
    alphas = np.linspace(1.0, 0.5, n)
    N = 2**n
    pieces = [
        [Polygon([tuple(v1 + (v2 - v1) * (i / N)), tuple(v1 + (v2 - v1) * ((i + 1) / N)), tuple(v0)])] for i in range(N)
    ]
    w = np.linalg.norm(v2 - v1) / N
    for k in range(n):
        step = 0.5 * alphas[k] * w * _EDIR
        pieces = [
            [shp_translate(p, *(+step)) for p in pieces[i]] + [shp_translate(p, *(-step)) for p in pieces[i + 1]]
            for i in range(0, len(pieces), 2)
        ]
        w *= 1.0 + alphas[k]
    return [p for grp in pieces for p in grp]


def main():
    A0 = Polygon([tuple(v) for v in VERTS]).area  # original triangle area (the pinned content)

    stages = []
    for n in DEPTHS:
        pieces = sprout(n)
        union = unary_union(pieces)
        s_sum = float(sum(p.area for p in pieces))  # sum of piece areas (content)
        u_area = float(union.area)  # union area (footprint)
        stages.append(
            dict(
                n=n,
                pieces=pieces,
                union=union,
                content=s_sum / A0,  # normalised so content == 1 ("areas sum to 1")
                footprint=u_area / A0,  # union as a fraction of A_0
                compression=s_sum / u_area,  # S_n / U_n
            )
        )

    contents = [s["content"] for s in stages]
    footprints = [s["footprint"] for s in stages]
    comps = [s["compression"] for s in stages]

    # Assertions: content is pinned, footprint falls, compression climbs
    assert max(abs(c - 1.0) for c in contents) < 1e-9, f"sum of piece areas must equal A_0 (content=1): {contents}"
    fdiffs = np.diff(footprints)
    assert (fdiffs < 0).all(), f"footprint (union/A_0) must strictly decrease: {footprints}"
    cdiffs = np.diff(comps)
    assert (cdiffs > 0).all(), f"compression S_n/U_n must strictly increase: {comps}"
    assert comps[0] > 1.0, "compression must exceed 1 (union already smaller than the content)"

    math_check(
        "Besicovitch compression: content pinned, footprint -> 0, ratio -> infinity",
        [
            ("mechanism", "sprout(n) only TRANSLATES 2^n pieces; sum of areas invariant, union shrinks"),
            ("A_0 (triangle area)", f"{A0:.4f}   (content is normalised to this, so content == 1)"),
            ("content S_n / A_0 (n=1..8)", "  ".join(f"{c:.3f}" for c in contents) + "   (flat = 1)"),
            ("footprint U_n / A_0 (n=1..8)", "  ".join(f"{f:.3f}" for f in footprints) + "   (falls)"),
            ("compression S_n / U_n (n=1..8)", "  ".join(f"{c:.2f}" for c in comps) + "   (climbs)"),
            ("footprint strictly down", f"max step {float(fdiffs.max()):.2e}  (< 0)"),
            ("compression strictly up", f"{comps[0]:.2f} -> {comps[-1]:.2f}  (> 1, and 1/logN-slow)"),
            ("reading", "total content ~ 1 pressed into a footprint < eta"),
        ],
    )

    # Figure
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots(1, 2, figsize=(12.6, 6.3))
    fig.suptitle("content pinned ~ 1, footprint -> 0, compression -> infinity", fontsize=13)
    axL, axR = ax
    axL.set_aspect("equal")

    # fixed drawing window over all depths
    allb = np.array([s["union"].bounds for s in stages])
    x0, y0, x1, y1 = allb[:, 0].min(), allb[:, 1].min(), allb[:, 2].max(), allb[:, 3].max()
    padx, pady = 0.06 * (x1 - x0), 0.06 * (y1 - y0)

    frame_stage = [0] * HOLD + list(range(len(stages))) + [len(stages) - 1] * END_HOLD
    ns = [s["n"] for s in stages]

    def update(fi):
        s = stages[frame_stage[fi]]
        upto = frame_stage[fi] + 1

        # LEFT: the pile; translucent pieces so overlaps stack darker (multiplicity = compression)
        axL.cla()
        axL.set_aspect("equal")
        axL.set_xlim(x0 - padx, x1 + padx)
        axL.set_ylim(y0 - pady, y1 + pady)
        axL.set_xticks([])
        axL.set_yticks([])
        for p in s["pieces"]:
            px, py = p.exterior.xy
            axL.fill(px, py, facecolor=COLORS["region"], edgecolor="none", alpha=0.22, zorder=1)
        u = s["union"]
        geoms = u.geoms if u.geom_type == "MultiPolygon" else [u]
        for g in geoms:
            gx, gy = g.exterior.xy
            axL.plot(gx, gy, color=COLORS["needle"], lw=1.2, zorder=3)
        axL.text(
            0.015,
            0.975,
            f"CONTENT = {s['content']:.2f}",
            transform=axL.transAxes,
            va="top",
            ha="left",
            fontsize=12,
            color=COLORS["outer"],
            weight="bold",
            bbox=dict(boxstyle="round,pad=0.26", fc="white", ec=COLORS["outer"], alpha=0.9),
            zorder=6,
        )
        axL.text(
            0.985,
            0.975,
            f"FOOTPRINT = {s['footprint']:.2f}",
            transform=axL.transAxes,
            va="top",
            ha="right",
            fontsize=12,
            color=COLORS["accent"],
            weight="bold",
            bbox=dict(boxstyle="round,pad=0.26", fc="white", ec=COLORS["accent"], alpha=0.9),
            zorder=6,
        )
        axL.text(
            0.5,
            0.02,
            f"compression = content / footprint = {s['compression']:.2f}x",
            transform=axL.transAxes,
            va="bottom",
            ha="center",
            fontsize=12,
            color=COLORS["guide"],
            weight="bold",
            zorder=6,
        )
        axL.set_title(f"Perron pile, depth n = {s['n']}  ({2 ** s['n']} translated pieces)", fontsize=10)

        # RIGHT: content (flat 1) vs footprint (falling); the shaded gap is the compression
        axR.cla()
        axR.set_xlim(ns[0] - 0.4, ns[-1] + 0.4)
        axR.set_ylim(0, 1.12)
        axR.set_xlabel("subdivision depth n  (N = 2^n pieces)")
        axR.set_ylabel("area / A_0")
        axR.grid(True, color=COLORS["muted"], alpha=0.25, lw=0.5)
        xr = ns[:upto]
        axR.plot(xr, contents[:upto], "-o", color=COLORS["outer"], ms=6, lw=1.8, label="content: sum of piece areas")
        axR.plot(xr, footprints[:upto], "-o", color=COLORS["accent"], ms=6, lw=1.8, label="footprint: union area")
        axR.fill_between(xr, footprints[:upto], contents[:upto], color=COLORS["accent"], alpha=0.12)
        axR.plot(ns[upto - 1], footprints[upto - 1], "o", color=COLORS["accent"], ms=12, mfc="none", mew=2)
        axR.set_title(f"content / footprint = {stages[upto - 1]['compression']:.2f}x   (climbs ~ log N)", fontsize=10)
        axR.legend(loc="upper right", fontsize=9)
        return []

    anim = FuncAnimation(fig, update, frames=len(frame_stage), interval=150, blit=False)
    print("wrote", save_gif(anim, fps=7, dpi=95))


if __name__ == "__main__":
    main()
