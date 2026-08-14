"""Animation: building the Perron tree step by step, needle sweep -> subdivide -> sprout (kakeya.md 2d).

Follows the Accromath kakeya19 sequence, top to bottom:
  1. a triangle carries a 60-degree fan of directions; the needle sweeps it (directions covered 0..60).
  2. subdivide the base into 2^n thin sub-triangles (all keep the shared apex, so the fan is unchanged).
  3. sprout: slide the sub-triangles to overlap; the footprint area drops while the 60-degree fan of
     directions is preserved (overlap is not counted twice).

Two readouts run throughout: area (percent of the original triangle) falling, and directions covered
(the fan) staying at 60 degrees.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_4_perron_steps_anim.py
"""

import math

import numpy as np
from _shared import COLORS, SQRT3, math_check, save_gif
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

H = SQRT3 / 2.0  # height of the base-1 equilateral triangle
APEX = np.array([0.0, H])
NLEV = 6  # 2^NLEV sub-triangles
ALPHA_MAX = 0.6  # final overlap fraction
FAN = 60.0  # apex angle in degrees

DIRR = np.array([0.5, 0.0]) - APEX  # apex -> right base corner (unit, length = side = 1)
DIRL = np.array([-0.5, 0.0]) - APEX  # apex -> left base corner


def subdivided():
    xs = np.linspace(-0.5, 0.5, 2**NLEV + 1)
    return [Polygon([(xs[i], 0.0), (xs[i + 1], 0.0), tuple(APEX)]) for i in range(2**NLEV)]


def sprout(alpha):
    """Continuous cut-and-shift: alpha=0 is the whole triangle, alpha>0 overlaps the pieces."""
    pieces = [[p] for p in subdivided()]
    w = 1.0 / 2**NLEV
    for _ in range(NLEV):
        step = 0.5 * alpha * w
        pieces = [
            [shp_translate(p, xoff=+step) for p in pieces[i]] + [shp_translate(p, xoff=-step) for p in pieces[i + 1]]
            for i in range(0, len(pieces), 2)
        ]
        w *= 1.0 + alpha
    return unary_union([p for g in pieces for p in g])


def main():
    tri_area = Polygon([(-0.5, 0.0), (0.5, 0.0), tuple(APEX)]).area
    alphas = np.linspace(0.0, ALPHA_MAX, 22)
    area_frac = [sprout(a).area / tri_area for a in alphas]

    assert abs(area_frac[0] - 1.0) < 1e-6, "alpha=0 must be the whole triangle (100%)"
    assert all(area_frac[i] <= area_frac[i - 1] + 1e-9 for i in range(1, len(area_frac))), "area must fall"
    assert area_frac[-1] < 0.6, "sprouting must cut the area well below 100%"

    math_check(
        "Perron steps: subdivide + sprout; area falls, 60-degree fan kept",
        [
            ("sub-triangles", f"2^{NLEV} = {2**NLEV} (shared apex)"),
            ("fan of directions", f"{FAN:.0f} deg (apex angle), preserved through the sprout"),
            ("area alpha=0 -> max", f"{area_frac[0] * 100:.0f}% -> {area_frac[-1] * 100:.0f}% of the triangle"),
            ("area monotone down", f"min step {min(np.diff(area_frac)):.3e} (<= 0)"),
            ("true limit", "area -> 0 like 1/log N (Keich); the fan stays 60 deg the whole way"),
        ],
    )

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    tri = np.array([[-0.5, 0.0], [0.5, 0.0], APEX, [-0.5, 0.0]])
    xs_div = np.linspace(-0.5, 0.5, 2**NLEV + 1)

    SWEEP, SUBH, END = 22, 8, 10
    # frames: ("sweep", f) needle sweeps the fan; ("sub", 1) show subdivision; ("sprout", i) alpha index
    frames = ([("sweep", (i + 1) / SWEEP) for i in range(SWEEP)]
              + [("sub", 1.0)] * SUBH
              + [("sprout", i) for i in range(len(alphas))]
              + [("sprout", len(alphas) - 1)] * END)

    fig, ax = plt.subplots(figsize=(6.2, 6.4))

    def cover_gauge(ax, deg):
        """small arc gauge, bottom-left, filling 0..60 deg."""
        cx, cy, r = -0.62, 0.15, 0.16
        a = np.linspace(0, math.radians(deg), 30)
        ax.plot(cx + r * np.cos(np.linspace(0, math.radians(FAN), 30)),
                cy + r * np.sin(np.linspace(0, math.radians(FAN), 30)), color=COLORS["muted"], lw=1.0)
        if deg > 0:
            ax.plot(cx + r * np.cos(a), cy + r * np.sin(a), color=COLORS["accent"], lw=3.0)
        ax.text(cx, cy - 0.12, f"fan {deg:.0f} deg", fontsize=8, ha="center", color=COLORS["guide"])

    def update(fi):
        kind, val = frames[fi]
        ax.cla()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-0.8, 0.8)
        ax.set_ylim(-0.12, H + 0.16)

        if kind == "sweep":
            ax.fill(tri[:, 0], tri[:, 1], facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=1.3, alpha=0.6)
            frac = val
            for g in np.linspace(0.0, frac, 6):  # faint fan of swept needles
                d = DIRR + (DIRL - DIRR) * g
                ax.plot([APEX[0], APEX[0] + d[0]], [APEX[1], APEX[1] + d[1]],
                        color=COLORS["needle"], lw=0.7, alpha=0.3)
            d = DIRR + (DIRL - DIRR) * frac
            ax.plot([APEX[0], APEX[0] + d[0]], [APEX[1], APEX[1] + d[1]], color=COLORS["needle"], lw=3.0, zorder=4)
            cover_gauge(ax, FAN * frac)
            ax.set_title("1. a triangle carries a 60 deg fan\nthe needle sweeps every direction", fontsize=11)

        elif kind == "sub":
            ax.fill(tri[:, 0], tri[:, 1], facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=1.3, alpha=0.6)
            for x in xs_div[::2]:
                ax.plot([x, APEX[0]], [0.0, APEX[1]], color=COLORS["guide"], lw=0.4, alpha=0.7)
            cover_gauge(ax, FAN)
            ax.set_title(f"2. subdivide the base into 2^{NLEV} = {2**NLEV}\nthin sub-triangles (shared apex)",
                         fontsize=11)

        else:  # sprout
            i = val
            geom = sprout(alphas[i])
            polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
            for g in polys:
                ax.fill(*g.exterior.xy, facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=0.8, alpha=0.7)
            cover_gauge(ax, FAN)
            ax.set_title(f"3. sprout: slide to overlap\narea {area_frac[i] * 100:.0f}% of the triangle, fan still 60 deg",
                         fontsize=11)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=120, blit=False)
    print("wrote", save_gif(anim, fps=8, dpi=95))


if __name__ == "__main__":
    main()
