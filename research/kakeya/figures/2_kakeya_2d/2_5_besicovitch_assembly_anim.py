"""Animation: assembling a Besicovitch set from three Perron trees (beats 2e-2f of ../kakeya.md).

Mirrors besicovitch_assembly.py in motion. One finished Perron tree carries only its 60 deg apex fan
(here 60..120 deg). Translation preserves direction, so rotating three copies of the tree by
0 / 120 / 240 deg about the shared apex spreads those fans over the full 180 deg of directions (a
direction and its reverse are the same), giving an all-directions set.

The animation brings the copies in one at a time: the first tree sits at 0 deg, the second sweeps
0 -> 120 deg, the third sweeps 0 -> 240 deg. A half-disc gauge fills with the covered directions,
completing the [0,180] deg span exactly when the third tree lands.

Honesty note (kakeya.md 2f): the true |K| = 0 is a limit (n -> inf, ~1/log N Keich decay), not
drawable; this is the minimum-visible finite-level approximation.

INVARIANT: by the final frame the covered-direction span is exactly 0..180 deg (all 180 one-degree
bins), verified from the actual rotated triangles' apex fans. Printed in the MATH CHECK.

The cut-and-shift merge is replicated locally (do NOT import perron_tree.py).

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/besicovitch_assembly_anim.py
"""
import numpy as np
from _shared import COLORS, SQRT3, equilateral, math_check, new_axes, poly, save_gif, triangle_fan_degrees
from matplotlib.animation import FuncAnimation
from shapely.affinity import rotate as shp_rotate
from shapely.affinity import translate as shp_translate
from shapely.ops import unary_union

H = SQRT3 / 2.0
APEX = (0.5, H)
N_TREE = 6              # 2^6 subtriangles per tree
S = 0.2
TARGETS = (0.0, 120.0, 240.0)


def _slivers(n: int):
    N = 2 ** n
    w = 1.0 / N
    return [[poly(np.array([[i * w, 0.0], [(i + 1) * w, 0.0], APEX]))] for i in range(N)]


def perron_tree(n: int, s: float = 0.2):
    """Symmetric cut-and-shift merge over n levels; returns (union, list of triangle polys)."""
    shapes = _slivers(n)
    w = 1.0 / (2 ** n)
    for _ in range(n):
        step = 0.5 * (1.0 - s) * w
        shapes = [
            [shp_translate(p, xoff=+step) for p in shapes[i]] + [shp_translate(p, xoff=-step) for p in shapes[i + 1]]
            for i in range(0, len(shapes), 2)
        ]
        w *= (1.0 + s)
    tris = [p for shp in shapes for p in shp]
    return unary_union(tris), tris


def covered_bins(tris, rotations):
    """Boolean coverage of 1-deg direction bins in [0,180) from the apex fans of all rotated tris."""
    covered = np.zeros(180, dtype=bool)
    for ang in rotations:
        for t in tris:
            rt = shp_rotate(t, ang, origin=APEX)
            xy = np.array(rt.exterior.coords)[:3]
            lo, hi = triangle_fan_degrees(xy)
            for d in range(int(np.floor(lo)), int(np.ceil(hi)) + 1):
                covered[d % 180] = True
    return covered


def _fill(ax, geom, color, alpha):
    geoms = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    for g in geoms:
        ax.fill(*g.exterior.xy, color=color, alpha=alpha, edgecolor="none")


def main():
    tree, tris = perron_tree(N_TREE, S)
    base_area = poly(equilateral(1.0)).area
    lo0, hi0 = triangle_fan_degrees(equilateral(1.0))

    # rotated tree geometry, precomputed for the three copies at their targets
    trees_final = [shp_rotate(tree, a, origin=APEX) for a in TARGETS]
    besic = unary_union(trees_final)

    # --- frame plan: current rotation angle of each of the three copies, and which are visible ---
    HOLD = 5
    SWEEP = 26
    frames = []  # (angles tuple, n_visible)
    frames += [((0.0, 0.0, 0.0), 1)] * HOLD
    for j in range(1, SWEEP + 1):
        frames.append(((0.0, 120.0 * j / SWEEP, 0.0), 2))
    frames += [((0.0, 120.0, 0.0), 2)] * 3
    for j in range(1, SWEEP + 1):
        frames.append(((0.0, 120.0, 240.0 * j / SWEEP), 3))
    frames += [((0.0, 120.0, 240.0), 3)] * (HOLD + 4)

    # coverage per frame, from the actual rotated triangles (rigorous)
    cover_per_frame = []
    for angles, nvis in frames:
        cover_per_frame.append(covered_bins(tris, angles[:nvis]))

    # --- INVARIANT: final coverage is exactly 0..180 ---
    final_cover = covered_bins(tris, TARGETS)
    full = bool(final_cover.all())
    idx = np.where(final_cover)[0]
    span = f"{idx.min()}..{idx.max() + 1}"

    math_check(
        "Besicovitch assembly (three Perron trees rotating 0/120/240 deg)",
        [
            ("one tree apex fan", f"{lo0:.0f}..{hi0:.0f} deg  (60 deg wide)"),
            ("copies rotate to", "0, 120, 240 deg about the apex"),
            ("base triangle area", f"{base_area:.4f}  (sqrt3/4)"),
            ("assembled area (visible)", f"{besic.area:.4f}  (finite-level approximation)"),
            ("covered bins, final", f"{int(final_cover.sum())}/180 deg"),
            ("covered-direction span, final", f"{span} deg"),
            ("spans 0..180 deg?", f"{full}  (a unit segment in every direction)"),
            ("true |K|", "= 0 (Besicovitch), reached as n -> inf; ~1/log N (Keich), not drawable"),
        ],
    )
    assert full and idx.min() == 0 and idx.max() + 1 == 180, "final coverage must be exactly 0..180 deg"

    # --- animation: left = assembling trees, right = coverage gauge ---
    fig, ax = new_axes(2, figsize=(11, 5.6))
    tree_colors = [COLORS["region"], COLORS["needle"], COLORS["accent"]]

    def update(i):
        angles, nvis = frames[i]
        cover = cover_per_frame[i]

        axL = ax[0]
        axL.clear(); axL.set_aspect("equal"); axL.axis("off")
        axL.set_xlim(-1.15, 1.15); axL.set_ylim(-0.95, 1.35)
        for k in range(nvis):
            rt = shp_rotate(tree, angles[k], origin=APEX)
            _fill(axL, rt, tree_colors[k], 0.62)
        axL.plot(*APEX, marker="o", color=COLORS["guide"], ms=4)
        axL.set_title("three Perron trees into place", fontsize=13)
        axL.text(0.5, -0.9, f"copies placed: {nvis}/3", transform=axL.transData,
                 ha="center", fontsize=10, color=COLORS["guide"])

        axR = ax[1]
        axR.clear(); axR.set_aspect("equal"); axR.axis("off")
        axR.set_xlim(-1.25, 1.25); axR.set_ylim(-0.35, 1.25)
        # protractor arc [0,180]; covered bins drawn as bold wedge-rays
        th = np.linspace(0, np.pi, 181)
        axR.plot(np.cos(th), np.sin(th), color=COLORS["muted"], lw=1)
        axR.plot([-1, 1], [0, 0], color=COLORS["muted"], lw=1)
        for d in range(180):
            if cover[d]:
                a = np.deg2rad(d + 0.5)
                axR.plot([0, np.cos(a)], [0, np.sin(a)], color=COLORS["accent"], lw=1.4, alpha=0.85)
        axR.set_title("directions covered", fontsize=13)
        axR.text(0, -0.28, f"{int(cover.sum())} / 180 deg", ha="center", fontsize=11, color=COLORS["guide"])
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=70, blit=False)
    print("wrote", save_gif(anim, fps=16, dpi=95))


if __name__ == "__main__":
    main()
