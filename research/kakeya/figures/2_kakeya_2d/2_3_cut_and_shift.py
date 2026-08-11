"""One cut-and-shift (Perron sprouting) step (kakeya.md 2d).

Bisect a triangle's base into two subtriangles that together carry the whole apex fan, then
TRANSLATE them to overlap. Translation preserves every segment's direction, so the fan is unchanged
while the union footprint shrinks below the original triangle.

Equilateral triangle of base 1, height h = sqrt3/2:
  area(before)  = sqrt3/4  ~ 0.4330                two disjoint subtriangles, nothing overlaps
  area(after)   < area(before)                     union once each shifts inward by t = 1/4
  fan(before)   = fan(after) = 60 deg              apex fan 60..120 deg, split 60..90 | 90..120

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/cut_and_shift.py
"""
import numpy as np
from _shared import COLORS, SQRT3, math_check, new_axes, poly, save_preview, triangle_fan_degrees
from shapely.ops import unary_union

H = SQRT3 / 2.0          # height of the base-1 equilateral triangle
SHIFT = 0.25             # inward translation of each subtriangle (maximal sprout: bases coincide)


def subtriangles(shift: float):
    """Left/right subtriangles of the bisected base-1 triangle, each translated inward by `shift`.

    shift = 0 -> the original bisection (disjoint, union = whole triangle).
    shift > 0 -> each slid toward the centre; a pure horizontal translation, so directions are kept.
    Returns rows [baseL, baseR, apex] for each so the fan helper can read them directly.
    """
    d1 = np.array([[0.0, 0.0], [0.5, 0.0], [0.5, H]])   # left half, apex at top-centre
    d2 = np.array([[0.5, 0.0], [1.0, 0.0], [0.5, H]])   # right half, same apex
    d1 = d1 + np.array([+shift, 0.0])
    d2 = d2 + np.array([-shift, 0.0])
    return d1, d2


def _draw_tri(ax, tri, fill=False):
    """Outline a subtriangle and draw its apex fan of unit-direction segments."""
    ring = np.vstack([tri, tri[0]])
    if fill:
        ax.fill(*poly(tri).exterior.xy, color=COLORS["region"], alpha=0.55, edgecolor="none")
    ax.plot(ring[:, 0], ring[:, 1], color=COLORS["guide"], lw=1.6)
    (bl, br, ap) = tri
    for f in np.linspace(0.0, 1.0, 11):          # fan: apex -> points along the base
        base_pt = bl + f * (br - bl)
        ax.plot([ap[0], base_pt[0]], [ap[1], base_pt[1]], color=COLORS["needle"], lw=0.7, alpha=0.85)


def main():
    # --- geometry ---
    b1, b2 = subtriangles(0.0)                 # before: disjoint bisection
    s1, s2 = subtriangles(SHIFT)               # after: shifted inward, crossing

    area_before = unary_union([poly(b1), poly(b2)]).area
    area_after = unary_union([poly(s1), poly(s2)]).area
    overlap = poly(s1).intersection(poly(s2)).area

    fan_b = [triangle_fan_degrees(b1), triangle_fan_degrees(b2)]
    fan_a = [triangle_fan_degrees(s1), triangle_fan_degrees(s2)]
    combined_before = (min(f[0] for f in fan_b), max(f[1] for f in fan_b))
    combined_after = (min(f[0] for f in fan_a), max(f[1] for f in fan_a))

    math_check(
        "cut-and-shift (Perron sprouting), one step",
        [
            ("area before (disjoint)", f"{area_before:.4f}  (whole triangle = sqrt3/4 = {SQRT3 / 4:.4f})"),
            ("overlap subtracted", f"{overlap:.4f}  (the shared crossing region)"),
            ("area after (shifted)", f"{area_after:.4f}  = before - overlap"),
            ("strictly smaller?", f"{area_after < area_before}  ({area_after:.4f} < {area_before:.4f})"),
            ("fan before", f"Delta1 {fan_b[0][0]:.0f}..{fan_b[0][1]:.0f}, Delta2 {fan_b[1][0]:.0f}..{fan_b[1][1]:.0f} -> {combined_before[0]:.0f}..{combined_before[1]:.0f} deg"),
            ("fan after", f"Delta1 {fan_a[0][0]:.0f}..{fan_a[0][1]:.0f}, Delta2 {fan_a[1][0]:.0f}..{fan_a[1][1]:.0f} -> {combined_after[0]:.0f}..{combined_after[1]:.0f} deg"),
            ("fan unchanged?", f"{combined_before == combined_after}  (translation preserves directions)"),
        ],
    )

    # --- preview ---
    fig, ax = new_axes(2, figsize=(11, 5.4))
    # (a) cut
    _draw_tri(ax[0], b1)
    _draw_tri(ax[0], b2)
    ax[0].text(0.22, 0.16, r"$\triangle_1$", fontsize=15, color=COLORS["guide"], ha="center")
    ax[0].text(0.78, 0.16, r"$\triangle_2$", fontsize=15, color=COLORS["guide"], ha="center")
    ax[0].set_title(f"(a) cut: bisect the base   area = {area_before:.3f}")

    # (b) shift: draw the overlap fill first, then the two crossing subtriangles + inward arrows
    ax[1].fill(*poly(s1).intersection(poly(s2)).exterior.xy, color=COLORS["region"], alpha=0.7, edgecolor="none")
    _draw_tri(ax[1], s1)
    _draw_tri(ax[1], s2)
    _arrow = dict(arrowstyle="->", color=COLORS["guide"], lw=2.0)
    ax[1].annotate("", xy=(0.16, H / 2), xytext=(-0.06, H / 2), arrowprops=_arrow)   # push right
    ax[1].annotate("", xy=(0.84, H / 2), xytext=(1.06, H / 2), arrowprops=_arrow)    # push left
    ax[1].set_title(f"(b) shift inward: overlap   area = {area_after:.3f}  (smaller)")

    for a in ax:
        a.set_xlim(-0.18, 1.18)
        a.set_ylim(-0.08, H + 0.08)
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
