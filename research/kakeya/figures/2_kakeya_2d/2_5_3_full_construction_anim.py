"""Animation: the whole Perron construction as one continuous motion (kakeya.md 2d; Accromath kakeya19).

kakeya19 stacks the construction as rows of still frames; here it is the motion those rows imply. The
triangle carries a 60-degree fan; its base is cut into 2^k thin sub-triangles; then the pieces SLIDE,
even ones right, odd ones left, so consecutive triangles overlap. That small back-and-forth shear is
the Pal shift: the wide triangle combs into strands and collapses into the spiky Perron tree, tips
fanning at the top and bases stacking into a trunk, while every direction of the fan is kept. A closing
pass sweeps the fan of piece-spines inside the finished tree: the same 60 degrees of directions, a
fraction of the area.

  1. fan     the triangle and the unit needle sweeping its 60-degree fan
  2. cut     break the base into 2^k sub-triangles (all share the apex direction-fan)
  3. shear   slide the pieces (back and forth) to overlap: footprint falls toward ~37%
  4. keep    sweep the fan of directions still present inside the tree

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_5_3_full_construction_anim.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

APEX = np.array([0.0, 1.0])  # height-1 triangle: unit needles from the apex fit
HB = 1.0 / math.sqrt(3.0)  # half base
NLEV = 5  # 2^5 = 32 sub-triangles: the triangle visibly combs into strands, and the tree looks like one
ALPHA_MAX = 0.7  # final overlap fraction per level (footprint ~37% of the triangle)
TRI = Polygon([(-HB, 0.0), (HB, 0.0), tuple(APEX)])
TRI_AREA = TRI.area
AR = math.atan2(-1.0, HB)  # apex -> right corner
AL = math.atan2(-1.0, -HB)  # apex -> left corner


def base_pieces():
    xs = np.linspace(-HB, HB, 2**NLEV + 1)
    return [Polygon([(xs[i], 0.0), (xs[i + 1], 0.0), tuple(APEX)]) for i in range(2**NLEV)]


def sprout_pieces(alpha):
    """The 2^NLEV sub-triangles after sliding to overlap by fraction `alpha`, kept as SEPARATE polygons
    so the motion (and the darkening overlaps) is visible. alpha = 0 tiles the original triangle."""
    groups = [[p] for p in base_pieces()]
    w = 2 * HB / 2**NLEV
    for _ in range(NLEV):
        step = 0.5 * alpha * w
        groups = [
            [shp_translate(p, xoff=+step) for p in groups[i]] + [shp_translate(p, xoff=-step) for p in groups[i + 1]]
            for i in range(0, len(groups), 2)
        ]
        w *= 1.0 + alpha
    return [p for g in groups for p in g]


def spine(piece):
    """Apex-to-base-midpoint segment of a (translated) sub-triangle: an honest chord of the tree that
    points in that piece's fan direction."""
    xy = np.array(piece.exterior.coords)[:-1]
    apex = xy[np.argmax(xy[:, 1])]
    base = xy[xy[:, 1] < 0.5]
    return apex, base.mean(axis=0)


def main():
    alphas = np.linspace(0.0, ALPHA_MAX, 18)
    area_frac = [unary_union(sprout_pieces(a)).area / TRI_AREA for a in alphas]
    assert abs(area_frac[0] - 1.0) < 1e-6, "alpha=0 must tile the whole triangle"
    assert area_frac[-1] < 0.6, "sliding to overlap must cut the footprint well below the triangle"

    final_pieces = sprout_pieces(ALPHA_MAX)
    spines = [spine(p) for p in final_pieces]
    spans = [math.degrees(math.atan2(b[0] - a[0], a[1] - b[1])) for a, b in spines]  # signed from vertical
    fan_span = max(spans) - min(spans)
    assert min(np.linalg.norm(np.subtract(b, a)) for a, b in spines) > 0.99, "each spine is a unit-ish chord"

    math_check(
        "full construction: fan -> cut -> shear/overlap (Perron tree) -> keep the fan",
        [
            ("sub-triangles", f"2^{NLEV} = {2**NLEV} (shared apex, 60-degree fan)"),
            ("shear shrinks area", f"{area_frac[0] * 100:.0f}% -> {area_frac[-1] * 100:.0f}% of the triangle"),
            ("shear move", "even pieces slide right, odd slide left, so neighbours overlap"),
            ("fan kept", f"piece spines still span ~{fan_span:.0f} degrees inside the shrunk tree"),
        ],
    )

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    tri_xy = np.array(TRI.exterior.coords)
    xs_div = np.linspace(-HB, HB, 2**NLEV + 1)
    allx = np.concatenate([np.array(p.exterior.coords)[:, 0] for p in final_pieces])
    xlim = 1.12 * max(HB, allx.max(), -allx.min())

    FAN, CUT, SLIDE, TREE, KEEP, END = 18, 10, len(alphas), 6, len(final_pieces), 8
    frames = (
        [("fan", (i + 1) / FAN) for i in range(FAN)]
        + [("cut", i / (CUT - 1)) for i in range(CUT)]
        + [("slide", i) for i in range(SLIDE)]
        + [("slide", SLIDE - 1)] * TREE
        + [("keep", i) for i in range(KEEP)]
        + [("keep", KEEP - 1)] * END
    )

    fig, ax = plt.subplots(figsize=(6.6, 6.8))

    def fan_needle(frac):
        ang = AR + (AL - AR) * frac
        return APEX, APEX + np.array([math.cos(ang), math.sin(ang)])

    def draw_pieces(pieces, lw=0.6):
        for p in pieces:
            ax.fill(*p.exterior.xy, facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=lw, alpha=0.34)

    def update(fi):
        kind, val = frames[fi]
        ax.cla()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-xlim, xlim)
        ax.set_ylim(-0.18, 1.18)

        if kind == "fan":
            ax.fill(
                tri_xy[:, 0], tri_xy[:, 1], facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=1.2, alpha=0.55
            )
            for g in np.linspace(0.0, val, 6):
                a, b = fan_needle(g)
                ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=0.7, alpha=0.3)
            a, b = fan_needle(val)
            ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=3.0, zorder=4)
            ax.set_title("1. the triangle and its 60-degree fan", fontsize=12)

        elif kind == "cut":
            ax.fill(
                tri_xy[:, 0], tri_xy[:, 1], facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=1.2, alpha=0.55
            )
            for x in xs_div:
                ax.plot([x, APEX[0]], [0.0, APEX[1]], color=COLORS["guide"], lw=0.6, alpha=0.35 + 0.55 * val)
            ax.set_title(f"2. cut the base into 2^{NLEV} = {2**NLEV} pieces", fontsize=12)

        elif kind == "slide":
            draw_pieces(sprout_pieces(alphas[val]))
            ax.set_title(
                f"3. slide to overlap (shear back and forth): {area_frac[val] * 100:.0f}% of the triangle", fontsize=11
            )

        else:  # keep: the fan of directions is still present inside the finished tree
            draw_pieces(final_pieces)
            for a, b in spines:
                ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=0.7, alpha=0.22)
            a, b = spines[val]
            ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["accent"], lw=2.6, zorder=4)
            ax.set_title(f"4. same fan of directions, ~{area_frac[-1] * 100:.0f}% of the area", fontsize=12)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=105, blit=False)
    print("wrote", save_gif(anim, fps=9, dpi=95))


if __name__ == "__main__":
    main()
