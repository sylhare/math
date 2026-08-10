r"""Figure: the Kakeya maximal function (kakeya.md section 5a).

The analytic form of the conjecture the harmonic analysts chase.  For a direction e in S^{n-1} the
Kakeya maximal function of f averages |f| over the delta-tube in direction e that maximises the
average through the point:

    f^*_delta(e)(x) = sup_{ x in T, T // e } (1/|T|) \int_T |f| ,

and the Kakeya maximal function conjecture bounds it on the sphere by f itself, losing only an
epsilon power of delta:

    || f^*_delta ||_{L^n(S^{n-1})}  <=  C_eps  delta^{-eps}  || f ||_{L^n(R^n)}   for all eps > 0.

The exponent is n, the dimension of the ambient space (n = 2, 3 the solved cases).

Left panel: several delta-tubes through one common point x0 (a fan of thin rectangles), the object
the sup is taken over.  Right panel: a heatmap of the maximal average M f(y) over a delta-tube
family, with f the indicator of a small disc.  By construction the maximal average at any point is
the sup of the individual tube averages there, so it dominates each of them.

INVARIANT (printed + asserted): at the common point x0 the maximal average equals the largest, and
is >= each, of the individual tube averages there; prints the exponent n (= 2, 3) and the bound.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/kakeya_maximal.py
"""
import numpy as np
from _shared import COLORS, math_check, new_axes, save_preview

DELTA = 0.06          # tube radius (half-width); tube dimensions delta x 1
BLOB_C = (0.22, 0.14)  # centre of the indicator disc f = 1_{disc}
BLOB_R = 0.12
GRID_N = 160
EXTENT = 0.62


def tube_mask(X, Y, angle, p0=(0.0, 0.0), length=1.0, half_width=DELTA / 2):
    """Boolean grid mask of the delta-tube through p0 in direction `angle` (length 1, radius delta/2)."""
    ca, sa = np.cos(angle), np.sin(angle)
    dx, dy = X - p0[0], Y - p0[1]
    along = dx * ca + dy * sa        # coordinate along the tube axis
    perp = -dx * sa + dy * ca        # signed distance from the axis
    return (np.abs(perp) <= half_width) & (np.abs(along) <= length / 2)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    xs = np.linspace(-EXTENT, EXTENT, GRID_N)
    X, Y = np.meshgrid(xs, xs)
    f = (((X - BLOB_C[0]) ** 2 + (Y - BLOB_C[1]) ** 2) <= BLOB_R ** 2).astype(float)

    # Family of delta-tubes through the common point x0 = origin, delta-separated directions.
    angles = np.linspace(0.0, np.pi, 60, endpoint=False)
    tube_avgs = []
    Mf = np.zeros_like(f)
    for a in angles:
        m = tube_mask(X, Y, a)
        if not m.any():
            continue
        avg = float(f[m].mean())          # (1/|T|) int_T f  on the discretised tube
        tube_avgs.append(avg)
        Mf = np.maximum(Mf, np.where(m, avg, 0.0))
    tube_avgs = np.array(tube_avgs)

    # --- INVARIANT: maximal average at x0 dominates every individual tube average there ----------
    oi = int(np.argmin(np.abs(xs)))       # grid index nearest x0 = origin (in every tube)
    m_at_x0 = float(Mf[oi, oi])
    assert m_at_x0 >= tube_avgs.max() - 1e-12          # sup >= max
    assert all(m_at_x0 >= a - 1e-12 for a in tube_avgs)  # >= each individual tube average

    math_check(
        "Kakeya maximal function conjecture",
        [
            ("bound", "|| f*_delta ||_{L^n(S^{n-1})} <= C_eps delta^{-eps} || f ||_{L^n(R^n)}"),
            ("exponent n (solved cases)", "n = 2 (Davies), n = 3 (Wang-Zahl 2025)"),
            ("delta (tube radius)", f"{DELTA}"),
            ("# tubes through x0", f"{len(tube_avgs)}   (delta-separated directions)"),
            ("individual tube averages at x0", f"min {tube_avgs.min():.3f}  max {tube_avgs.max():.3f}"),
            ("maximal average M f(x0)", f"{m_at_x0:.3f}   (= sup over tubes = max individual)"),
            ("invariant  M f(x0) >= each avg", "YES  (maximal average dominates every tube)"),
        ],
    )

    fig, ax = new_axes(2, figsize=(12.0, 6.0))

    # --- Left: several delta-tubes through the common point x0 -------------------------------------
    ax[0].set_xlim(-EXTENT, EXTENT)
    ax[0].set_ylim(-EXTENT, EXTENT)
    fan = np.linspace(0.0, np.pi, 7, endpoint=False)
    for a in fan:
        ca, sa = np.cos(a), np.sin(a)
        axis = np.array([ca, sa])
        perp = np.array([-sa, ca])
        c = 0.5 * axis
        corners = np.array([c - (DELTA / 2) * perp, c + (DELTA / 2) * perp,
                            -c + (DELTA / 2) * perp, -c - (DELTA / 2) * perp])
        ax[0].add_patch(plt.Polygon(corners, closed=True, facecolor=COLORS["needle"],
                                    edgecolor=COLORS["needle"], alpha=0.35, lw=0.8))
    th = np.linspace(0, 2 * np.pi, 200)
    ax[0].plot(BLOB_C[0] + BLOB_R * np.cos(th), BLOB_C[1] + BLOB_R * np.sin(th),
               color=COLORS["accent"], lw=1.4)
    ax[0].text(BLOB_C[0], BLOB_C[1], "f=1", color=COLORS["accent"], ha="center", va="center", fontsize=9)
    ax[0].plot([0], [0], "o", color=COLORS["guide"], ms=7, zorder=5)
    ax[0].text(0.02, -0.06, "x0", color=COLORS["guide"], fontsize=10)
    ax[0].set_title("delta-tubes through a common point x0", fontsize=12)

    # --- Right: maximal-average heatmap over the tube family ---------------------------------------
    im = ax[1].imshow(np.ma.masked_where(Mf <= 0, Mf), origin="lower",
                      extent=(-EXTENT, EXTENT, -EXTENT, EXTENT), cmap="magma", vmin=0.0)
    ax[1].plot(BLOB_C[0] + BLOB_R * np.cos(th), BLOB_C[1] + BLOB_R * np.sin(th),
               color="white", lw=1.2, alpha=0.9)
    ax[1].plot([0], [0], "o", color="white", ms=6, zorder=5)
    ax[1].set_xlim(-EXTENT, EXTENT)
    ax[1].set_ylim(-EXTENT, EXTENT)
    ax[1].set_title("maximal average  M f  over the delta-tube family", fontsize=12)
    fig.colorbar(im, ax=ax[1], fraction=0.046, pad=0.04, label="(1/|T|) int_T f")

    fig.suptitle(
        "Kakeya maximal function:  || f*_delta ||_{L^n(S^{n-1})} <= C_eps delta^{-eps} || f ||_{L^n(R^n)}"
        "   (n = 2, 3)", fontsize=11)
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
