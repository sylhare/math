"""Animation: one fattened Perron pile read by two rulers, area -> 0 and box-count slope -> 2.

The same Perron cut-and-shift pile from 2_7 (sprout(n): subdivide the core into 2^n sub-triangles
and translate to overlap, every direction kept) is grown deeper and, at the same time, measured on a
finer grid. Couple depth and scale exactly as the theorem does: frame k uses depth n = k and grid
cell delta_k = W / 2^k (W = pile bounding width, so 1/delta_k = 2^k).

  * area   = shapely-measured union area of K_n           -> slides toward 0 (the 2_7 shrink)
  * N(delta) = grid cells the union meets                 -> keeps the slope-2 growth of a solid
  * slope  = fitted log N(delta) / log(1/delta)           -> creeps up toward 2

So the log-log curve stays parallel to the dimension-2 (filled square) line and peels away from the
dimension-1 (single needle) line: area 0, dimension 2. The slope only rises loglog-slowly, so the
reading is "parallel to slope 2, peeling from slope 1", not "slope hits 2 on screen".

Companion to 2_7 (the same sprout) and 4_1 (the delta^2/sin theta overlap engine).

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/4_kakeya_dimension/4_2_area_dimension_boxcount_anim.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from shapely.affinity import scale as shp_scale
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon
from shapely.geometry import box as shp_box
from shapely.ops import unary_union
from shapely.prepared import prep

SIDE = 1.0
R = SIDE / math.sqrt(3.0)
CORNERS_DEG = (90.0, 210.0, 330.0)
DEPTHS = list(range(1, 8))  # frame k -> depth n = k, k = 1..7 (grid up to 128 x 128)
HOLD = 6  # hold on the first (coarsest) stage
END_HOLD = 8  # hold on the last (finest) stage

VERTS = np.array([R * np.array([math.cos(math.radians(d)), math.sin(math.radians(d))]) for d in CORNERS_DEG])
_EDIR = (VERTS[2] - VERTS[1]) / np.linalg.norm(VERTS[2] - VERTS[1])


# Geometry: the exact sprout(n) cut-and-shift from 2_7
def sprout(n):
    """Perron cut-and-shift of the core triangle to depth n (overlap alpha 1.0 -> 0.5);
    returns the 2^n sub-triangle polygons whose union is the shrunk core."""
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


# Box counting: cells of side delta a geometry meets
def box_count(geom, k):
    """Grid over the unit square with 2^k cells per side (delta = 1/2^k); return the hit
    (i, j) cell indices the geometry intersects (prepared-geometry test)."""
    n = 2**k
    delta = 1.0 / n
    minx, miny, maxx, maxy = geom.bounds
    i0 = max(0, math.floor(minx / delta))
    i1 = min(n - 1, math.floor((maxx - 1e-12) / delta))
    j0 = max(0, math.floor(miny / delta))
    j1 = min(n - 1, math.floor((maxy - 1e-12) / delta))
    pg = prep(geom)
    hits = []
    for i in range(i0, i1 + 1):
        for j in range(j0, j1 + 1):
            if pg.intersects(shp_box(i * delta, j * delta, (i + 1) * delta, (j + 1) * delta)):
                hits.append((i, j))
    return hits, delta


def main():
    # 1. build every pile once, raw geometry (area is measured in original coordinates)
    unions_raw = {n: unary_union(sprout(n)) for n in DEPTHS}
    area_raw = {n: unions_raw[n].area for n in DEPTHS}

    # 2. fixed domain: the global bounding box over all depths, made square (side W)
    bounds = np.array([unions_raw[n].bounds for n in DEPTHS])
    x0, y0 = bounds[:, 0].min(), bounds[:, 1].min()
    x1, y1 = bounds[:, 2].max(), bounds[:, 3].max()
    W = max(x1 - x0, y1 - y0)  # pile bounding width; delta_k = W / 2^k

    def normalize(geom):
        return shp_scale(shp_translate(geom, -x0, -y0), xfact=1.0 / W, yfact=1.0 / W, origin=(0, 0))

    unions_norm = {n: normalize(unions_raw[n]) for n in DEPTHS}

    # 3. couple depth and scale: frame k uses depth n = k and grid delta_k = 1/2^k
    stages = []
    for n in DEPTHS:
        hits, delta = box_count(unions_norm[n], n)  # k == n
        Nbox = len(hits)
        stages.append(
            dict(
                n=n,
                delta=delta,
                Nbox=Nbox,
                hits=hits,
                x=math.log(1.0 / delta),
                logN=math.log(Nbox),
                area_raw=area_raw[n],
                area_norm=unions_norm[n].area,
                N_needle=round(1.0 / delta),
                N_square=round(1.0 / delta) ** 2,
            )
        )

    xs = [s["x"] for s in stages]
    logN = [s["logN"] for s in stages]
    log_needle = [math.log(s["N_needle"]) for s in stages]
    log_square = [math.log(s["N_square"]) for s in stages]

    # cumulative fitted slope of the Kakeya curve (frames so far)
    cum_slope = [math.nan]
    for j in range(1, len(stages)):
        cum_slope.append(float(np.polyfit(xs[: j + 1], logN[: j + 1], 1)[0]))

    # reference fits: single needle -> slope 1, filled square -> slope 2 (exact)
    fit_needle = float(np.polyfit(xs, log_needle, 1)[0])
    fit_square = float(np.polyfit(xs, log_square, 1)[0])

    # Assertions: everything drawn is measured and matches the theorem
    areas = [stages[j]["area_raw"] for j in range(len(stages))]
    diffs = np.diff(areas)
    assert (diffs < 0).all(), "measured union area must strictly decrease with depth n"
    assert areas[-1] < areas[0], "A_n < A_1"

    Nseq = [s["Nbox"] for s in stages]
    assert all(Nseq[j] > Nseq[j - 1] for j in range(1, len(Nseq))), "N(delta) must strictly grow as delta shrinks"

    # box-count identity: N(delta) * delta^2 approximates the normalized leftover area, order 1
    ratios = [stages[j]["Nbox"] * stages[j]["delta"] ** 2 / stages[j]["area_norm"] for j in range(len(stages))]
    assert all(1.0 <= r <= 12.0 for r in ratios), f"N*delta^2 vs area must be order 1: ratios {ratios}"

    final_slope = cum_slope[-1]
    fitted = [cum_slope[j] for j in range(1, len(stages))]
    assert all(1.5 < v < 2.0 for v in fitted), f"every fitted Kakeya slope must land in (1.5, 2.0): {fitted}"
    assert final_slope > fitted[0], (
        f"the fitted slope must climb net toward 2, got {fitted[0]:.3f} -> {final_slope:.3f}"
    )
    # once the grid resolves the pile (>= 16 x 16, n >= 4) the cumulative slope is strictly non-decreasing;
    # the 2x2 and 4x4 grids are too coarse to resolve a thin pile, so the first two fits wiggle.
    resolved = [cum_slope[j] for j in range(len(stages)) if stages[j]["n"] >= 4]
    assert all(resolved[j] > resolved[j - 1] for j in range(1, len(resolved))), (
        f"resolved-grid cumulative slope must creep up toward 2: {resolved}"
    )

    assert abs(fit_needle - 1.0) < 1e-6, f"single-needle reference slope must be 1, got {fit_needle}"
    assert abs(fit_square - 2.0) < 1e-6, f"filled-square reference slope must be 2, got {fit_square}"

    math_check(
        "fattened Perron pile: area down, box-count slope -> 2",
        [
            ("mechanism", "one sprout(n) pile, depth n = grid k coupled; delta_k = W/2^k, 1/delta = 2^k"),
            ("AREA A_n (measured, n=1..7)", "  ".join(f"{a:.4f}" for a in areas)),
            (
                "AREA strictly down, A_n < A_1",
                f"min step {float(diffs.max()):.2e} (<0); {areas[-1]:.4f} < {areas[0]:.4f}",
            ),
            ("N(delta) (measured, n=1..7)", "  ".join(f"{s['Nbox']}" for s in stages)),
            ("N*delta^2 / area (order 1)", "  ".join(f"{r:.2f}" for r in ratios)),
            ("Kakeya cumulative slope", "  ".join(f"{v:.3f}" for v in cum_slope[1:])),
            ("slope creeps up (resolved n>=4)", "  ".join(f"{v:.3f}" for v in resolved) + "  (strictly up)"),
            ("final fitted slope in (1.5,2)", f"{final_slope:.4f}   (coarse 2x2,4x4 wiggle then climbs)"),
            ("single-needle reference fit", f"{fit_needle:.6f}   (want 1)"),
            ("filled-square reference fit", f"{fit_square:.6f}   (want 2)"),
            ("reading", "area -> 0, curve stays parallel to slope 2, peels from slope 1: dimension 2"),
        ],
    )

    # Figure
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots(1, 2, figsize=(12.6, 6.3))
    fig.suptitle("area -> 0, box-count slope -> 2", fontsize=13)
    axL, axR = ax
    axL.set_aspect("equal")

    frame_stage = [0] * HOLD + list(range(len(stages))) + [len(stages) - 1] * END_HOLD

    xmax = xs[-1] + 0.6
    ymax = log_square[-1] + 0.6

    def update(fi):
        s = stages[frame_stage[fi]]
        upto = frame_stage[fi] + 1
        n, delta = s["n"], s["delta"]
        ncell = 2**n

        # Left: the fattened pile, the delta grid, and the highlighted boxes it meets
        axL.cla()
        axL.set_aspect("equal")
        axL.set_xlim(-0.03, 1.03)
        axL.set_ylim(-0.03, 1.03)
        axL.set_xticks([])
        axL.set_yticks([])

        # the delta grid (bottom)
        gl = min(0.6, 0.6 * 32.0 / ncell + 0.12)
        for kk in range(ncell + 1):
            c = kk * delta
            axL.plot([0, 1], [c, c], color=COLORS["muted"], lw=gl, alpha=0.5, zorder=1)
            axL.plot([c, c], [0, 1], color=COLORS["muted"], lw=gl, alpha=0.5, zorder=1)

        # the shapely union of the pile, shaded (no edge yet)
        geom = unions_norm[n]
        polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
        for g in polys:
            gx, gy = g.exterior.xy
            axL.fill(gx, gy, facecolor=COLORS["region"], edgecolor="none", alpha=0.70, zorder=2)

        # highlighted boxes (the N(delta) cells the union meets), tinted over the pile so the count is visible
        mask = np.zeros((ncell, ncell))
        for i, j in s["hits"]:
            mask[j, i] = 1.0
        axL.imshow(
            np.ma.masked_where(mask < 0.5, mask),
            extent=(0, 1, 0, 1),
            origin="lower",
            cmap=matplotlib.colors.ListedColormap([COLORS["accent"]]),
            alpha=0.28,
            vmin=0,
            vmax=1,
            zorder=3,
            interpolation="nearest",
        )

        # the union outline on top so the thinning shape stays readable
        for g in polys:
            gx, gy = g.exterior.xy
            axL.plot(gx, gy, color=COLORS["needle"], lw=1.0, zorder=4)

        # two big synced readouts on top
        axL.text(
            0.015,
            0.975,
            f"AREA |K_n| = {s['area_raw']:.4f}",
            transform=axL.transAxes,
            va="top",
            ha="left",
            fontsize=13,
            color=COLORS["needle"],
            weight="bold",
            bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=COLORS["needle"], alpha=0.9),
            zorder=6,
        )
        slope_txt = f"{cum_slope[upto - 1]:.3f}" if upto >= 2 else "..."
        axL.text(
            0.985,
            0.975,
            f"SLOPE = {slope_txt}",
            transform=axL.transAxes,
            va="top",
            ha="right",
            fontsize=13,
            color=COLORS["accent"],
            weight="bold",
            bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=COLORS["accent"], alpha=0.9),
            zorder=6,
        )
        axL.set_title(
            f"sprout depth n = {n} ({2**n} pieces),  delta = W/{ncell},  N(delta) = {s['Nbox']} lit cells", fontsize=10
        )

        # Right: log N vs log(1/delta), points accumulating between slope-1 and slope-2 lines
        axR.cla()
        axR.set_xlim(0, xmax)
        axR.set_ylim(0, ymax)
        axR.set_xlabel("log(1/delta)")
        axR.set_ylabel("log N(delta)")
        axR.grid(True, color=COLORS["muted"], alpha=0.25, lw=0.5)

        xr = np.array([0.0, xmax])
        axR.plot(xr, 2.0 * xr, "--", color=COLORS["muted"], lw=1.4, label="filled square, slope 2")
        axR.plot(xr, 1.0 * xr, "--", color=COLORS["guide"], lw=1.4, label="single needle, slope 1")

        axR.plot(
            xs[:upto], logN[:upto], "-o", color=COLORS["accent"], ms=6, lw=1.6, label="Kakeya pile N(delta)", zorder=5
        )
        axR.plot(xs[upto - 1], logN[upto - 1], "o", color=COLORS["accent"], ms=12, mfc="none", mew=2, zorder=6)

        if upto >= 2:
            axR.set_title(f"log N / log(1/delta) = {cum_slope[upto - 1]:.3f}   (-> 2, loglog-slowly)", fontsize=10)
        else:
            axR.set_title("log N / log(1/delta)   (accumulating)", fontsize=10)
        axR.legend(loc="upper left", fontsize=9)
        return []

    anim = FuncAnimation(fig, update, frames=len(frame_stage), interval=150, blit=False)
    print("wrote", save_gif(anim, fps=7, dpi=95))


if __name__ == "__main__":
    main()
