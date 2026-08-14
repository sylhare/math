"""Sticky vs non-sticky tubes (kakeya.md section 7a, Hickman Def. 5.8).

At an intermediate scale delta <= rho <= 1 there are rho^-2 fat rho-tubes and delta^-2 thin
delta-tubes. Sticky: each fat tube holds #{ T : T subset of T_rho } ~ (rho/delta)^2 thin tubes of
one direction. Non-sticky: same-direction thin tubes scatter, so no fat tube reaches that occupancy.
rho = 1/4, delta = 1/16: (rho/delta)^2 = 16 thin per fat, rho^-2 = 16 fat, delta^-2 = 256 = 16 x 16.

2D cross-section: thin delta-tube = red dot, fat rho-tube = blue rho x rho square; one
direction-family outlined in guide grey.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/sticky_vs_nonsticky.py
"""
import numpy as np
from _shared import COLORS, math_check, save_preview


# Geometry (pure numpy, portable): cross-section positions of thin tubes
def fat_centers(rho: float) -> np.ndarray:
    """Centres of the rho^-2 fat tubes on a regular grid tiling the unit square cross-section."""
    m = round(1.0 / rho)
    xs = (np.arange(m) + 0.5) * rho
    gx, gy = np.meshgrid(xs, xs)
    return np.column_stack([gx.ravel(), gy.ravel()])


def sub_offsets(rho: float, delta: float) -> np.ndarray:
    """The (rho/delta)^2 sub-grid offsets of thin tubes packed inside one fat tube."""
    k = round(rho / delta)
    xs = (np.arange(k) - (k - 1) / 2) * delta
    gx, gy = np.meshgrid(xs, xs)
    return np.column_stack([gx.ravel(), gy.ravel()])


def sticky_positions(rho, delta):
    """Each direction-bin -> one fat tube; its (rho/delta)^2 thin tubes clustered inside it.
    Returns (positions [N,2], bin_id [N]). Bin i is the family of same-direction thin tubes."""
    centers = fat_centers(rho)
    offs = sub_offsets(rho, delta)
    pos, bins = [], []
    for i, c in enumerate(centers):
        pos.append(c + offs)
        bins.append(np.full(len(offs), i))
    return np.vstack(pos), np.concatenate(bins)


def nonsticky_positions(rho, delta, rng):
    """Same bins/counts, but each direction-bin's thin tubes scattered across the whole square."""
    n_bins = round(1.0 / rho) ** 2
    per = round(rho / delta) ** 2
    pos, bins = [], []
    for i in range(n_bins):
        pos.append(rng.uniform(0.0, 1.0, size=(per, 2)))
        bins.append(np.full(per, i))
    return np.vstack(pos), np.concatenate(bins)


def occupancy(pos, bins, rho):
    """For each direction-bin, the max #same-direction thin tubes inside one rho-tube.
    A rho-tube cross-section is a rho x rho square, so the window is L-infinity of side rho.
    Returns the mean over bins. Sticky ~ (rho/delta)^2 ; non-sticky ~ 1."""
    r = rho / 2.0
    per_bin = []
    for i in np.unique(bins):
        p = pos[bins == i]
        # densest rho x rho square: anchor it on each thin tube, take the largest count
        best = max(int(np.sum(np.all(np.abs(p - q) <= r, axis=1))) for q in p)
        per_bin.append(best)
    return float(np.mean(per_bin))


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rho, delta = 0.25, 0.0625
    per_fat = (rho / delta) ** 2      # 16
    n_fat = round(1.0 / rho) ** 2     # 16
    n_thin = round(1.0 / delta) ** 2  # 256

    pos_s, bins_s = sticky_positions(rho, delta)
    pos_n, bins_n = nonsticky_positions(rho, delta, np.random.default_rng(11))
    occ_s = occupancy(pos_s, bins_s, rho)
    occ_n = occupancy(pos_n, bins_n, rho)

    math_check(
        "sticky vs non-sticky: (rho/delta)^2 occupancy per fat tube",
        [
            ("rho, delta", f"{rho}, {delta}   rho/delta = {rho/delta:.0f}"),
            ("thin per fat (rho/delta)^2", f"{per_fat:.0f}"),
            ("# fat tubes  rho^-2", f"{n_fat}"),
            ("# thin tubes  delta^-2", f"{n_thin}   (= {n_fat} x {per_fat:.0f})"),
            ("STICKY occupancy / fat tube", f"{occ_s:.1f}   (~ (rho/delta)^2 = {per_fat:.0f})  YES"),
            ("NON-STICKY occupancy / fat tube", f"{occ_n:.1f}   (<< {per_fat:.0f})  NO"),
        ],
    )

    # Preview
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.2))
    centers = fat_centers(rho)
    hi = 5  # highlighted direction-family

    for ax, pos, bins, title in [
        (axes[0], pos_s, bins_s, "sticky: same-direction tubes clump in one fat tube"),
        (axes[1], pos_n, bins_n, "non-sticky: same-direction tubes scattered"),
    ]:
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title)
        for c in centers:  # fat rho-tubes (rho x rho cross-section)
            ax.add_patch(plt.Rectangle(c - rho / 2, rho, rho, fill=False, ec=COLORS["outer"], lw=1.3, alpha=0.9))
        other = bins != hi
        ax.scatter(pos[other, 0], pos[other, 1], s=8, color=COLORS["accent"], alpha=0.55)
        fam = bins == hi  # one direction-family, outlined in guide grey
        ax.scatter(pos[fam, 0], pos[fam, 1], s=42, facecolor=COLORS["accent"],
                   edgecolor=COLORS["guide"], linewidths=1.4, zorder=3)
        ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.05, 1.05)

    axes[0].legend(handles=[
        plt.Line2D([], [], marker="o", ls="", mfc=COLORS["accent"], mec=COLORS["accent"], label="thin delta-tube"),
        plt.Line2D([], [], marker="s", ls="", mfc="none", mec=COLORS["outer"], label="fat rho-tube"),
        plt.Line2D([], [], marker="o", ls="", mfc=COLORS["accent"], mec=COLORS["guide"], label="one direction-family"),
    ], loc="upper center", bbox_to_anchor=(1.05, -0.02), ncol=3, frameon=False, fontsize=9)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
