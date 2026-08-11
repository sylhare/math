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

    # View must be centred on the APEX (the rotation pivot) and large enough to hold a tree at ANY
    # angle: every tree point stays within R_max of the apex, so a square of half-width R_max around
    # the apex contains all three copies in every frame (no clipping as they turn).
    _apex = np.array(APEX)
    _verts = np.vstack([np.array(t.exterior.coords)[:3] for t in tris])
    r_max = float(np.max(np.linalg.norm(_verts - _apex, axis=1)))
    _pad = 0.10 * r_max
    xl = (APEX[0] - r_max - _pad, APEX[0] + r_max + _pad)
    yl = (APEX[1] - r_max - _pad, APEX[1] + r_max + _pad)

    # --- frame plan: (angles, n_visible, n_landed) ---------------------------------------------
    # n_landed = how many copies have reached their target and LOCKED their directions.  The gauge
    # counts only landed copies, so it steps 60 -> 120 -> 180 monotonically (the sweeping copy's fan
    # is shown separately as a moving "pending" wedge, not added to the count until it lands).
    HOLD = 5
    SWEEP = 26
    frames = []
    frames += [((0.0, 0.0, 0.0), 1, 1)] * HOLD
    for j in range(1, SWEEP + 1):
        frames.append(((0.0, 120.0 * j / SWEEP, 0.0), 2, 1))
    frames += [((0.0, 120.0, 0.0), 2, 2)] * (HOLD + 2)
    for j in range(1, SWEEP + 1):
        frames.append(((0.0, 120.0, 240.0 * j / SWEEP), 3, 2))
    frames += [((0.0, 120.0, 240.0), 3, 3)] * (HOLD + 4)

    # each copy contributes ONE 60-deg band; drawn in that copy's colour so the half-circle shows
    # three coloured slices (copy 0 -> [60,120], copy 1 -> [0,60], copy 2 -> [120,180]).
    band_per_tree = [covered_bins(tris, [a]) for a in TARGETS]

    # per frame: locked coverage (landed copies at their targets, monotone) and the pending fan (the
    # copy currently rotating into place), both from the actual rotated triangles (rigorous)
    locked_per_frame, pending_per_frame = [], []
    for angles, nvis, nland in frames:
        locked_per_frame.append(covered_bins(tris, TARGETS[:nland]))
        pending_per_frame.append(covered_bins(tris, [angles[nland]]) if nvis > nland else None)

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
        angles, nvis, nland = frames[i]
        locked = locked_per_frame[i]
        pending = pending_per_frame[i]

        axL = ax[0]
        axL.clear(); axL.set_aspect("equal"); axL.axis("off")
        axL.set_xlim(*xl); axL.set_ylim(*yl)  # centred on the apex; holds every rotation, no clipping
        for k in range(nvis):
            rt = shp_rotate(tree, angles[k], origin=APEX)
            _fill(axL, rt, tree_colors[k], 0.62)
        axL.plot(*APEX, marker="o", color=COLORS["guide"], ms=4)
        axL.set_title("three Perron trees into place", fontsize=13)
        axL.text(0.5, 0.02, f"copies placed: {nvis}/3", transform=axL.transAxes,
                 ha="center", fontsize=10, color=COLORS["guide"])

        axR = ax[1]
        axR.clear(); axR.set_aspect("equal"); axR.axis("off")
        axR.set_xlim(-1.25, 1.25); axR.set_ylim(-0.35, 1.25)
        # protractor [0,180]; covered directions drawn as clean filled wedges (contiguous runs),
        # not 180 separate rays (which merge into a featureless blob).
        th = np.linspace(0, np.pi, 181)

        def _wedges(mask, color, alpha):
            d = 0
            while d < 180:
                if mask[d]:
                    s = d
                    while d < 180 and mask[d]:
                        d += 1
                    aa = np.deg2rad(np.arange(s, d + 1))
                    axR.fill(np.concatenate([[0.0], np.cos(aa), [0.0]]),
                             np.concatenate([[0.0], np.sin(aa), [0.0]]),
                             color=color, alpha=alpha, edgecolor="none")
                else:
                    d += 1

        # each landed copy fills its own 60-deg slice in that copy's colour (three coloured slices
        # tiling the half circle); the copy still rotating shows its current fan as a faint pending
        # wedge in its colour, NOT counted until it lands.
        for k in range(nland):
            _wedges(band_per_tree[k], tree_colors[k], 0.6)
        if pending is not None:
            _wedges(pending & ~locked, tree_colors[nland], 0.28)
        axR.plot(np.cos(th), np.sin(th), color=COLORS["guide"], lw=1.2)  # arc outline on top
        axR.plot([-1, 1], [0, 0], color=COLORS["guide"], lw=1.2)
        axR.set_title("directions covered", fontsize=13)
        axR.text(0, -0.28, f"{int(locked.sum())} / 180 deg  (locked: {nland}/3 copies)",
                 ha="center", fontsize=11, color=COLORS["guide"])
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=70, blit=False)
    print("wrote", save_gif(anim, fps=16, dpi=95))


if __name__ == "__main__":
    main()
