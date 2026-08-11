"""Animation of the Perron tree sprouting level by level (kakeya.md 2d-2f).

Start from the 2^n thin slivers tiling the base-1 equilateral triangle (they carry its whole 60 deg
apex fan). Run the cut-and-shift merge one level at a time: neighbouring blocks slide together and
OVERLAP. Every move is a pure horizontal translation, so each segment keeps its direction, the fan
stays 60..120 deg, and the union footprint shrinks.

This fixed-fraction merge reduces area to a plateau near ~47% of the triangle, not to zero; the true
Besicovitch area -> 0 only ~1/log N (Keich), not drawable.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/perron_sprout_anim.py
"""
import numpy as np
from _shared import COLORS, SQRT3, equilateral, math_check, new_axes, poly, save_gif, triangle_fan_degrees
from matplotlib.animation import FuncAnimation
from shapely.ops import unary_union

H = SQRT3 / 2.0          # height of the base-1 equilateral triangle
APEX = np.array([0.5, H])

N_LEVELS = 5             # 2^5 = 32 slivers
S = 0.2                 # fraction of fresh base kept per merge (fixed-fraction schedule)
HOLD_START = 4
SLIDE = 14              # frames sliding within each level
HOLD_END = 8


def build_plan(n: int, s: float):
    """Per-sliver cumulative x-offset at the start of each merge level, and the per-level delta.

    Returns (base_tris, start_offsets, delta) where base_tris[i] is the i-th sliver [baseL,baseR,apex]
    and start_offsets[L], delta[L] are length-N arrays: offset[i] = start_offsets[L][i] + f*delta[L][i]
    for a slide fraction f in [0,1] within level L.
    """
    N = 2 ** n
    w0 = 1.0 / N
    base_tris = [np.array([[i * w0, 0.0], [(i + 1) * w0, 0.0], APEX]) for i in range(N)]

    groups = [[i] for i in range(N)]      # merged blocks as lists of sliver indices
    cur = np.zeros(N)
    start_offsets = [cur.copy()]
    delta = []
    w = w0
    for _ in range(n):
        step = 0.5 * (1.0 - s) * w
        d = np.zeros(N)
        new_groups = []
        for i in range(0, len(groups), 2):
            gA, gB = groups[i], groups[i + 1]
            for k in gA:
                d[k] += step
            for k in gB:
                d[k] -= step
            new_groups.append(gA + gB)
        groups = new_groups
        delta.append(d)
        cur = cur + d
        start_offsets.append(cur.copy())
        w *= (1.0 + s)
    return base_tris, start_offsets, delta


def tris_at(base_tris, off):
    return [t + np.array([off[i], 0.0]) for i, t in enumerate(base_tris)]


def fan_span(tris):
    lohi = [triangle_fan_degrees(t) for t in tris]
    return min(lo for lo, _ in lohi), max(hi for _, hi in lohi)


def main():
    base_tris, start_offsets, delta = build_plan(N_LEVELS, S)
    base_area = poly(equilateral(1.0)).area

    # frame plan: (level, slide-fraction)
    frame_plan = [(0, 0.0)] * HOLD_START
    for L in range(N_LEVELS):
        frame_plan += [(L, j / SLIDE) for j in range(1, SLIDE + 1)]
    frame_plan += [(N_LEVELS - 1, 1.0)] * HOLD_END

    # precompute geometry per frame
    offs = [start_offsets[L] + f * delta[L] for (L, f) in frame_plan]
    tri_sets = [tris_at(base_tris, o) for o in offs]
    unions = [unary_union([poly(t) for t in ts]) for ts in tri_sets]
    areas = [u.area for u in unions]
    spans = [fan_span(ts) for ts in tri_sets]

    # --- INVARIANT checks ---
    # checkpoint per completed level: within a level the union can wiggle, but each merge shrinks it
    level_area = {L: unary_union([poly(t) for t in tris_at(base_tris, start_offsets[L + 1])]).area
                  for L in range(N_LEVELS)}
    checkpoints = [areas[0]] + [level_area[L] for L in range(N_LEVELS)]
    non_increasing = all(checkpoints[i + 1] <= checkpoints[i] + 1e-9 for i in range(len(checkpoints) - 1))
    span_lo = min(lo for lo, _ in spans)
    span_hi = max(hi for _, hi in spans)
    fan_locked = abs(span_lo - 60.0) < 1e-6 and abs(span_hi - 120.0) < 1e-6

    math_check(
        "Perron sprout (cut-and-shift, level by level)",
        [
            ("slivers / levels", f"2^{N_LEVELS} = {2 ** N_LEVELS} slivers, {N_LEVELS} merge levels, s = {S}"),
            ("start area (slivers tile triangle)", f"{areas[0]:.4f}  (sqrt3/4 = {SQRT3 / 4:.4f})"),
            ("area after level n", "  ".join(f"n={L + 1}:{level_area[L]:.3f}" for L in range(N_LEVELS))),
            ("final area (visible)", f"{areas[-1]:.4f} = {areas[-1] / base_area * 100:.0f}% of triangle"),
            ("area non-increasing across levels?", f"{non_increasing}  (each merge shrinks the footprint)"),
            ("fan span over all frames", f"{span_lo:.1f}..{span_hi:.1f} deg  (want 60..120)"),
            ("fan locked at 60..120?", f"{fan_locked}  (horizontal translation preserves direction)"),
            ("true Besicovitch area", "-> 0 (~1/log N, Keich); this fixed-fraction merge plateaus, not drawable to 0"),
        ],
    )
    assert non_increasing, "union area must be non-increasing across merge levels"
    assert fan_locked, "direction fan must stay 60..120 deg"

    # --- animation ---
    fig, ax = new_axes(1, figsize=(7.2, 5.2))
    allx = np.concatenate([np.array([t[:, 0] for t in ts]).ravel() for ts in tri_sets])
    ax.set_xlim(allx.min() - 0.08, allx.max() + 0.08)
    ax.set_ylim(-0.08, H + 0.14)

    def update(i):
        ax.clear()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(allx.min() - 0.08, allx.max() + 0.08)
        ax.set_ylim(-0.08, H + 0.14)
        u = unions[i]
        geoms = u.geoms if u.geom_type == "MultiPolygon" else [u]
        for g in geoms:
            ax.fill(*g.exterior.xy, color=COLORS["region"], alpha=0.75, edgecolor="none")
        # needle rays base-midpoint -> apex for a sample of slivers (the direction family)
        ts = tri_sets[i]
        for t in ts[:: max(1, len(ts) // 24)]:
            bm = 0.5 * (t[0] + t[1])
            ax.plot([bm[0], t[2][0]], [bm[1], t[2][1]], color=COLORS["needle"], lw=0.6, alpha=0.75)
        L, f = frame_plan[i]
        done = L + (1 if f >= 1.0 - 1e-9 else 0)
        ax.set_title("Perron tree: cut and shift", fontsize=13)
        ax.text(0.02, 0.98, f"level {done}/{N_LEVELS}\narea = {areas[i]:.3f}   fan 60..120 deg",
                transform=ax.transAxes, va="top", ha="left", fontsize=10, color=COLORS["guide"])
        return []

    anim = FuncAnimation(fig, update, frames=len(frame_plan), interval=70, blit=False)
    print("wrote", save_gif(anim, fps=16, dpi=95))


if __name__ == "__main__":
    main()
