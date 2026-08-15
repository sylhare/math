"""Animation of a Besicovitch set from three Perron trees (kakeya.md 2e-2f).

One finished Perron tree carries only its 60 deg apex fan (here 60..120 deg). Translation preserves
direction, so rotating three copies by 0 / 120 / 240 deg about the shared apex spreads those fans
over the full 180 deg (a direction and its reverse are the same): an all-directions set.

The copies come in one at a time: first at 0 deg, second sweeping 0 -> 120 deg, third 0 -> 240 deg;
each adds 60 deg, so coverage steps 60 -> 120 -> 180 deg.

True |K| = 0 is a limit (n -> inf, ~1/log N Keich decay), not drawable; this is the minimum-visible
finite-level approximation.

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

    trees_final = [shp_rotate(tree, a, origin=APEX) for a in TARGETS]
    besic = unary_union(trees_final)

    # view centred on the apex (rotation pivot); half-width r_max holds a tree at any angle, no clip
    _apex = np.array(APEX)
    _verts = np.vstack([np.array(t.exterior.coords)[:3] for t in tris])
    r_max = float(np.max(np.linalg.norm(_verts - _apex, axis=1)))
    _pad = 0.10 * r_max
    xl = (APEX[0] - r_max - _pad, APEX[0] + r_max + _pad)
    yl = (APEX[1] - r_max - _pad, APEX[1] + r_max + _pad)

    # Frame plan: (angles, n_landed) -- n_landed = copies that have reached their target
    HOLD = 5
    SWEEP = 26
    frames = []
    frames += [((0.0, 0.0, 0.0), 1)] * HOLD
    for j in range(1, SWEEP + 1):
        frames.append(((0.0, 120.0 * j / SWEEP, 0.0), 1))       # 2nd copy rotating in
    frames += [((0.0, 120.0, 0.0), 2)] * (HOLD + 2)
    for j in range(1, SWEEP + 1):
        frames.append(((0.0, 120.0, 240.0 * j / SWEEP), 2))     # 3rd copy rotating in
    frames += [((0.0, 120.0, 240.0), 3)] * (HOLD + 4)

    # Invariant: final coverage is exactly 0..180
    final_cover = covered_bins(tris, TARGETS)
    full = bool(final_cover.all())
    idx = np.where(final_cover)[0]
    span = f"{idx.min()}..{idx.max() + 1}"

    math_check(
        "Besicovitch assembly (three Perron trees rotating 0/120/240 deg)",
        [
            ("one tree apex fan", f"{lo0:.0f}..{hi0:.0f} deg  (60 deg wide)"),
            ("copies rotate to", "0, 120, 240 deg about the apex"),
            ("each copy adds", "60 deg of directions -> 60, 120, 180 as they lock in"),
            ("base triangle area", f"{base_area:.4f}  (sqrt3/4)"),
            ("assembled area (visible)", f"{besic.area:.4f}  (finite-level approximation)"),
            ("covered-direction span, final", f"{span} deg  ({int(final_cover.sum())}/180)"),
            ("spans 0..180 deg?", f"{full}  (a unit segment in every direction)"),
            ("true |K|", "= 0 (Besicovitch), reached as n -> inf; ~1/log N (Keich), not drawable"),
        ],
    )
    assert full and idx.min() == 0 and idx.max() + 1 == 180, "final coverage must be exactly 0..180 deg"

    # Animation: one panel, the three coloured Perron trees rotating into place
    fig, ax = new_axes(1, figsize=(6.6, 6.9))
    tree_colors = [COLORS["region"], COLORS["needle"], COLORS["accent"]]

    def update(i):
        angles, nland = frames[i]
        n_visible = 1 + sum(1 for a in angles[1:] if a > 0.0)  # copy 0 always; later copies once moving
        ax.clear(); ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(*xl); ax.set_ylim(*yl)  # centred on the apex; holds every rotation, no clipping
        for k in range(n_visible):
            _fill(ax, shp_rotate(tree, angles[k], origin=APEX), tree_colors[k], 0.62)
        ax.plot(*APEX, marker="o", color=COLORS["guide"], ms=4)
        ax.set_title("Besicovitch set: three Perron trees rotated into place", fontsize=12)
        rotating = "   (rotating the next copy into place)" if n_visible > nland else ""
        ax.text(0.5, 0.03, f"trees in place: {nland}/3      directions covered: {60 * nland} of 180 deg{rotating}",
                transform=ax.transAxes, ha="center", fontsize=11, color=COLORS["guide"])
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=70, blit=False)
    print("wrote", save_gif(anim, fps=16, dpi=95))


if __name__ == "__main__":
    main()
