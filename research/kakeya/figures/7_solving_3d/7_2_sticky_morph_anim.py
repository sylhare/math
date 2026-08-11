"""Morph non-sticky -> sticky tubes (kakeya.md section 7a, Hickman Def. 5.8).

Motion version of `sticky_vs_nonsticky.py`. Each thin tube travels in a straight line from a
scattered (non-sticky) position to a clumped (sticky) position; the total thin-tube count
delta^-2 = 256 is conserved every frame. At the sticky end each fat rho-tube holds
~(rho/delta)^2 = 16 same-direction thin tubes.
rho = 1/4, delta = 1/16: (rho/delta)^2 = 16 thin per fat, rho^-2 = 16 fat, delta^-2 = 256 = 16 x 16.

2D cross-section: thin delta-tube = red dot, fat rho-tube = blue rho x rho square; one
direction-family outlined in guide grey.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/sticky_morph_anim.py
"""
import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation


def fat_centers(rho):
    """Centres of the rho^-2 fat tubes on a regular grid tiling the unit-square cross-section."""
    m = round(1.0 / rho)
    xs = (np.arange(m) + 0.5) * rho
    gx, gy = np.meshgrid(xs, xs)
    return np.column_stack([gx.ravel(), gy.ravel()])


def sub_offsets(rho, delta):
    """The (rho/delta)^2 sub-grid offsets of thin tubes packed inside one fat tube."""
    k = round(rho / delta)
    xs = (np.arange(k) - (k - 1) / 2) * delta
    gx, gy = np.meshgrid(xs, xs)
    return np.column_stack([gx.ravel(), gy.ravel()])


def sticky_positions(rho, delta):
    """Each direction-bin -> one fat tube; its (rho/delta)^2 thin tubes clustered inside it."""
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
    """Mean over direction-bins of the max #same-direction thin tubes inside one rho x rho window."""
    r = rho / 2.0
    per_bin = []
    for i in np.unique(bins):
        p = pos[bins == i]
        best = max(int(np.sum(np.all(np.abs(p - q) <= r, axis=1))) for q in p)
        per_bin.append(best)
    return float(np.mean(per_bin))


def smoothstep(t):
    return t * t * (3 - 2 * t)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rho, delta = 0.25, 0.0625
    per_fat = round((rho / delta) ** 2)   # 16
    n_fat = round(1.0 / rho) ** 2         # 16
    n_thin = round(1.0 / delta) ** 2      # 256

    pos_s, bins_s = sticky_positions(rho, delta)
    pos_n, bins_n = nonsticky_positions(rho, delta, np.random.default_rng(11))
    assert np.array_equal(bins_s, bins_n)      # index-aligned correspondence for the morph
    assert len(pos_s) == n_thin == len(pos_n)

    occ_n = occupancy(pos_n, bins_n, rho)
    occ_s = occupancy(pos_s, bins_s, rho)

    # --- INVARIANT assertions ------------------------------------------------
    assert n_thin == 256 and per_fat == 16 and n_fat == 16
    assert n_fat * per_fat == n_thin
    assert abs(occ_s - per_fat) < 1e-9, occ_s      # sticky end realizes (rho/delta)^2
    assert occ_n < per_fat / 2, occ_n              # non-sticky end far fewer

    math_check(
        "sticky morph: (rho/delta)^2 occupancy, delta^-2 conserved",
        [
            ("rho, delta", f"{rho}, {delta}   rho/delta = {rho / delta:.0f}"),
            ("thin per fat (rho/delta)^2", f"{per_fat}"),
            ("# fat tubes rho^-2", f"{n_fat}"),
            ("# thin tubes delta^-2 (conserved)", f"{n_thin}   (= {n_fat} x {per_fat})"),
            ("NON-STICKY occupancy / fat tube", f"{occ_n:.1f}   (<< {per_fat})"),
            ("STICKY occupancy / fat tube", f"{occ_s:.1f}   (~ (rho/delta)^2 = {per_fat})"),
        ],
    )

    H0, MORPH, H1 = 8, 40, 12
    ts = np.concatenate([np.zeros(H0), smoothstep(np.linspace(0, 1, MORPH)), np.ones(H1)])
    centers = fat_centers(rho)
    hi = 5  # highlighted direction-family

    fig, ax = plt.subplots(figsize=(6.4, 6.6))

    def update(fi):
        t = float(ts[fi])
        pos = (1 - t) * pos_n + t * pos_s
        assert len(pos) == n_thin  # conservation in every frame
        occ = occupancy(pos, bins_s, rho)

        ax.clear()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.12, 1.10)
        for c in centers:
            ax.add_patch(plt.Rectangle(c - rho / 2, rho, rho, fill=False, ec=COLORS["outer"], lw=1.3, alpha=0.9))
        other = bins_s != hi
        ax.scatter(pos[other, 0], pos[other, 1], s=9, color=COLORS["accent"], alpha=0.55)
        fam = bins_s == hi
        ax.scatter(pos[fam, 0], pos[fam, 1], s=44, facecolor=COLORS["accent"],
                   edgecolor=COLORS["guide"], linewidths=1.4, zorder=3)

        regime = "sticky" if t > 0.5 else "non-sticky"
        ax.set_title(f"non-sticky -> sticky  (2D cross-section):  {regime}", fontsize=12)
        ax.text(0.5, -0.09,
                f"thin tubes: {n_thin} (conserved)   |   mean occupancy / fat tube: {occ:.1f}"
                f"   ->   (rho/delta)^2 = {per_fat}",
                ha="center", va="center", fontsize=9.5, color=COLORS["guide"])
        return []

    anim = FuncAnimation(fig, update, frames=len(ts), interval=70, blit=False)
    print("wrote", save_gif(anim, fps=14, dpi=95))


if __name__ == "__main__":
    main()
