"""Pal join (Pal worm) lemma (kakeya.md 2d).

Given two PARALLEL unit needles G1, G2 and any eps > 0, there is a set J with area(J) < eps inside
which the needle moves CONTINUOUSLY from G1 to G2 by a far detour: slide out along its own axis a
distance D (sweeps ~0 area), rotate a little far out, slide across, rotate back, slide home.

Crossing the fixed lateral gap g from a pivot ~D away turns the needle through

    phi(D) = 2 * arctan( g / (2D) )

and each unit-needle rotation sweeps a sector A_sector = (1/2) r^2 phi = phi/2 (r = 1); sliding
sweeps ~0 area, so the total swept area

    A(D)  ~  2 * A_sector  =  phi(D)  =  2 * arctan( g / (2D) )   -> 0   as D grows.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/pal_join.py
"""
import math
from itertools import pairwise

import numpy as np
from _shared import COLORS, math_check, save_preview
from shapely.geometry import Polygon
from shapely.ops import unary_union

GAP = 0.3          # fixed lateral gap between the two parallel unit needles (lines y=0 and y=GAP)
LEN = 1.0          # needle length (fixed; geometric honesty)


def maneuver_needles(D: float, n: int = 400) -> list[np.ndarray]:
    """Sampled needle endpoints [[x0,y0],[x1,y1]] along the full Pal-join maneuver for detour D.

    Phases (needle always length 1):
      1. slide G1 out along +x by D                 (along own axis -> ~0 area)
      2. rotate up by phi about the far trailing end (sweeps a sector, area phi/2)
      3. slide along the tilted axis until the trailing end rises by the gap g  (own axis -> ~0)
      4. rotate back down by phi                     (sweeps a sector, area phi/2)
      5. slide back along -x to land on G2           (own axis -> ~0)
    """
    phi = 2.0 * math.atan(GAP / (2.0 * D))
    needles: list[np.ndarray] = []

    def add(trail, ang):
        tip = trail + LEN * np.array([math.cos(ang), math.sin(ang)])
        needles.append(np.array([trail, tip]))

    n1 = max(2, n // 5)
    # 1. slide out along +x, trailing end (0,0) -> (D,0)
    for x in np.linspace(0.0, D, n1):
        add(np.array([x, 0.0]), 0.0)
    # 2. rotate up by phi about the far trailing end (D,0)
    piv = np.array([D, 0.0])
    for a in np.linspace(0.0, phi, n1):
        add(piv, a)
    # 3. slide along the tilted axis until trailing end reaches height GAP
    s = GAP / math.sin(phi)
    for u in np.linspace(0.0, s, n1):
        add(piv + u * np.array([math.cos(phi), math.sin(phi)]), phi)
    # 4. rotate back down to horizontal about the raised trailing end
    piv2 = piv + s * np.array([math.cos(phi), math.sin(phi)])
    for a in np.linspace(phi, 0.0, n1):
        add(piv2, a)
    # 5. slide back along -x to land the needle on line y = GAP at x in [0,1]
    for x in np.linspace(piv2[0], 0.0, n1):
        add(np.array([x, GAP]), 0.0)
    return needles


def swept_area(needles: list[np.ndarray]) -> float:
    """Area of the region swept by the moving needle = union of quads between consecutive positions."""
    quads = []
    for a, b in pairwise(needles):
        q = Polygon([a[0], a[1], b[1], b[0]])
        if q.is_valid and q.area > 0:
            quads.append(q)
        else:
            q = q.buffer(0)               # fix bow-tie / degenerate quads
            if not q.is_empty:
                quads.append(q)
    return unary_union(quads).area


def main():
    Ds = [2.0, 4.0, 8.0, 16.0]
    measured = {D: swept_area(maneuver_needles(D)) for D in Ds}
    predicted = {D: 2.0 * math.atan(GAP / (2.0 * D)) for D in Ds}
    decreasing = all(measured[a] > measured[b] for a, b in pairwise(Ds))

    math_check(
        "Pal join: swept area shrinks with detour distance D",
        [
            ("gap g (fixed), needle length", f"g = {GAP}, L = {LEN}"),
            ("turn angle phi(D) = 2 arctan(g/2D)", "  ".join(f"D={D:g}:{math.degrees(predicted[D]):.1f} deg" for D in Ds)),
            ("predicted area ~ phi(D) (rad)", "  ".join(f"D={D:g}:{predicted[D]:.4f}" for D in Ds)),
            ("MEASURED swept area (drawn)", "  ".join(f"D={D:g}:{measured[D]:.4f}" for D in Ds)),
            ("monotone decreasing in D?", f"{decreasing}"),
            ("area -> 0 as D -> inf?", f"{measured[Ds[-1]] < measured[Ds[0]]}  (schematic; lemma: area < eps for every eps > 0)"),
        ],
    )

    # --- preview: the maneuver for a mid D, plus the area-vs-D trend ---
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(12, 5.2))

    Dshow = 4.0
    needles = maneuver_needles(Dshow)
    swept = unary_union(
        [Polygon([a[0], a[1], b[1], b[0]]).buffer(0) for a, b in pairwise(needles)]
    )
    geoms = swept.geoms if swept.geom_type == "MultiPolygon" else [swept]
    for g in geoms:
        axL.fill(*g.exterior.xy, color=COLORS["region"], alpha=0.7, edgecolor="none")
    for nd in needles[:: max(1, len(needles) // 60)]:
        axL.plot(nd[:, 0], nd[:, 1], color=COLORS["needle"], lw=0.6, alpha=0.7)
    # the two parallel unit needles G1, G2, drawn bold
    axL.plot([0, 1], [0, 0], color=COLORS["accent"], lw=3.0, solid_capstyle="round")
    axL.plot([0, 1], [GAP, GAP], color=COLORS["accent"], lw=3.0, solid_capstyle="round")
    axL.text(0.5, -0.12, "$G_1$", color=COLORS["accent"], ha="center", fontsize=13)
    axL.text(0.5, GAP + 0.06, "$G_2$", color=COLORS["accent"], ha="center", fontsize=13)
    axL.annotate("far detour (slide out along axis)", xy=(Dshow, 0.0), xytext=(Dshow * 0.45, -0.55),
                 color=COLORS["guide"], fontsize=9,
                 arrowprops=dict(arrowstyle="->", color=COLORS["guide"]))
    axL.set_aspect("equal")
    axL.axis("off")
    axL.set_title(f"Pal join, D = {Dshow:g}  (schematic; measured area {measured.get(Dshow, swept.area):.3f})")

    axR.plot(Ds, [measured[D] for D in Ds], "o-", color=COLORS["accent"], label="measured (drawn)")
    axR.plot(Ds, [predicted[D] for D in Ds], "s--", color=COLORS["outer"], label=r"$\phi(D)=2\arctan(g/2D)$")
    axR.set_xlabel("detour distance $D$")
    axR.set_ylabel("swept area")
    axR.set_title("area decreases as the detour goes farther out")
    axR.grid(True, alpha=0.3)
    axR.legend()

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
