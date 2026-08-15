"""Animation: Pal joins turn the Perron tree (a Besicovitch set) into a Kakeya needle set (kakeya.md 2d-2e).

The Perron tree contains a unit segment in every direction of its 60-degree fan, but those segments sit
in separate branches: it is a Besicovitch set, not something a needle can be turned inside continuously.
The Pal join repairs that. To carry the needle from one branch to the neighbouring one without sweeping
much area: slide it out along its own axis (free, it stays on its line), make the small turn far out
where a tiny angle suffices, then slide back into the next branch. The swept extra is only the little
turn slivers; chaining the joins across every branch lets the needle rotate continuously through the
whole fan, so the tree plus the thin slivers is a needle set (small positive area, not zero).

Two parts in one clip:
  1. detail  one Pal join between two adjacent branches, slowly: slide out, small turn, slide back.
  2. full    chain the joins across all branches: the needle turns through the whole 60-degree fan,
             the detour slivers accumulate into a thin fringe below the tree.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_5_4_pal_tree_needle_set_anim.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

APEX = np.array([0.0, 1.0])
HB = 1.0 / math.sqrt(3.0)
NLEV = 4  # 16 branches: separated enough that a single Pal join is easy to see
ALPHA = 0.6
S_DETAIL = 0.75  # how far the needle slides out on the slow detour (bigger = more visible)
S_FULL = 0.45  # slide-out on each quick detour in the chained sweep


def sprout_pieces(alpha=ALPHA):
    xs = np.linspace(-HB, HB, 2**NLEV + 1)
    pieces = [[Polygon([(xs[i], 0.0), (xs[i + 1], 0.0), tuple(APEX)])] for i in range(2**NLEV)]
    w = 2 * HB / 2**NLEV
    for _ in range(NLEV):
        step = 0.5 * alpha * w
        pieces = [
            [shp_translate(p, xoff=+step) for p in pieces[i]] + [shp_translate(p, xoff=-step) for p in pieces[i + 1]]
            for i in range(0, len(pieces), 2)
        ]
        w *= 1.0 + alpha
    return [p for g in pieces for p in g]


def branch_needle(piece):
    xy = np.array(piece.exterior.coords)[:-1]
    apex = xy[np.argmax(xy[:, 1])]
    basemid = xy[xy[:, 1] < 0.5].mean(axis=0)
    d = basemid - apex
    return apex, d / np.linalg.norm(d)  # (tip, unit direction pointing down the branch)


def pal_pose(tip_a, u_a, tip_b, u_b, s_out, f):
    """The needle (A, B) partway (fraction f in [0,1]) through a Pal join from branch (tip_a, u_a) to
    branch (tip_b, u_b): slide out along u_a, small turn far out, slide back along u_b."""
    pivot = tip_a + (1.0 + s_out) * u_a  # far bottom end where the turn happens
    if f < 0.4:  # slide out along the axis (free)
        top = tip_a + (s_out * f / 0.4) * u_a
        return top, top + u_a, None
    if f < 0.6:  # small turn far out about the bottom pivot
        u = (f - 0.4) / 0.2
        ang = math.atan2(u_a[1], u_a[0]) + u * (math.atan2(u_b[1], u_b[0]) - math.atan2(u_a[1], u_a[0]))
        d = np.array([math.cos(ang), math.sin(ang)])
        return pivot - d, pivot, (pivot, math.atan2(u_a[1], u_a[0]), ang)
    u = (f - 0.6) / 0.4  # slide back along u_b into branch b
    post_top = pivot - u_b
    top = post_top + u * (tip_b - post_top)
    return top, top + u_b, (pivot, math.atan2(u_a[1], u_a[0]), math.atan2(u_b[1], u_b[0]))


def wedge(center, a0, a1, r=1.0, n=20):
    a = np.linspace(a0, a1, n)
    return np.array([tuple(center), *[(center[0] + r * math.cos(t), center[1] + r * math.sin(t)) for t in a]])


def main():
    pieces = sprout_pieces()
    tree = unary_union(pieces)
    needles = sorted((branch_needle(p) for p in pieces), key=lambda tu: math.atan2(tu[1][1], tu[1][0]) % math.pi)
    fan = math.degrees(
        max(math.atan2(u[1], u[0]) % math.pi for _, u in needles)
        - min(math.atan2(u[1], u[0]) % math.pi for _, u in needles)
    )
    turn_sector = 0.5 * (math.radians(fan) / (len(needles) - 1))  # one small turn between adjacent branches

    math_check(
        "Pal joins on the Perron tree -> a Kakeya needle set",
        [
            ("branches", f"{len(needles)} unit needles, fan {fan:.0f} degrees (a Besicovitch set)"),
            ("one Pal join", "slide out (free) -> small turn far out -> slide back into the next branch"),
            ("turn cost", f"one sector ~ {turn_sector:.3f}; slides are free, so only turns add area"),
            ("result", "chained joins rotate the needle continuously -> a needle set (small positive area)"),
        ],
    )

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    i_a, i_b = len(needles) // 2 - 2, len(needles) // 2 + 1  # a few branches apart, so the turn is visible
    DETAIL, PER, HOLD, END = 34, 7, 10, 10
    frames = [("intro", t) for t in range(HOLD)]
    frames += [("detail", f / (DETAIL - 1)) for f in range(DETAIL)]
    frames += [("detail", 1.0)] * 5
    for i in range(len(needles) - 1):
        frames += [("full", (i, f / (PER - 1))) for f in range(PER)]
    frames += [("full", (len(needles) - 2, 1.0))] * END

    fig, ax = plt.subplots(figsize=(6.8, 6.9))

    def draw_tree():
        for gg in tree.geoms if tree.geom_type == "MultiPolygon" else [tree]:
            ax.fill(*gg.exterior.xy, facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=0.7, alpha=0.5)

    def setup():
        ax.cla()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-1.0, 1.0)
        ax.set_ylim(-1.15, 1.15)

    def draw_needle(a, b, sect):
        if sect is not None:
            piv, a0, a1 = sect
            ax.fill(*wedge(piv, a0, a1).T, facecolor=COLORS["accent"], edgecolor="none", alpha=0.75, zorder=2)
        ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=3.2, zorder=4, solid_capstyle="round")

    def update(fi):
        kind, val = frames[fi]
        setup()
        draw_tree()
        if kind == "intro":
            for tip, u in needles:
                ax.plot([tip[0], tip[0] + u[0]], [tip[1], tip[1] + u[1]], color=COLORS["needle"], lw=0.8, alpha=0.3)
            ax.set_title("Perron tree: a unit needle in every direction, but in separate branches", fontsize=11)
        elif kind == "detail":
            ta, ua = needles[i_a]
            tb, ub = needles[i_b]
            for tip, u in (needles[i_a], needles[i_b]):  # the two branches being joined
                ax.plot([tip[0], tip[0] + u[0]], [tip[1], tip[1] + u[1]], color=COLORS["needle"], lw=2.0, alpha=0.3)
            a, b, sect = pal_pose(ta, ua, tb, ub, S_DETAIL, val)
            draw_needle(a, b, sect)
            step = (
                "slide out along the axis (free)"
                if val < 0.4
                else "small turn far out (the only area cost)"
                if val < 0.6
                else "slide back into the other branch"
            )
            ax.set_title(f"One Pal join: {step}", fontsize=12)
        else:
            i, f = val
            for j in range(i + 1):  # accumulate the detour slivers already swept
                ta, ua = needles[j]
                tb, ub = needles[j + 1]
                for g in np.linspace(0, 1, 6):
                    a, b, _ = pal_pose(ta, ua, tb, ub, S_FULL, g)
                    ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=0.6, alpha=0.16)
            ta, ua = needles[i]
            tb, ub = needles[i + 1]
            a, b, sect = pal_pose(ta, ua, tb, ub, S_FULL, f)
            draw_needle(a, b, sect)
            turned = fan * (i + f) / (len(needles) - 1)
            ax.set_title(
                f"Chaining Pal joins: the needle turns continuously ({turned:.0f} of {fan:.0f} deg)", fontsize=11
            )
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=95, blit=False)
    print("wrote", save_gif(anim, fps=11, dpi=95))


if __name__ == "__main__":
    main()
