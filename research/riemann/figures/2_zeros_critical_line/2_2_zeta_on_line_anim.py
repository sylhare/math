"""Animation: Hardy's Z(t) scanned up the critical line.

    Z(t) = e^{i theta(t)} zeta(1/2 + it)          real-valued, |Z(t)| = |zeta(1/2 + it)|
    Z(gamma_k) = 0  <=>  zeta(1/2 + i gamma_k) = 0

A zero on the line is an ordinary sign change of the real function Z. Scanning t left to
right, every sign change is a nontrivial zero with beta = 1/2. The 10 ordinates gamma_k < 50
in ZETA_ZEROS each straddle one sign change.

ASSERT: the number of sign changes of Z on [0, 50] equals #{gamma_k < 50} = 10.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
     python research/riemann/figures/2_zeros_critical_line/2_2_zeta_on_line_anim.py
"""

import numpy as np
from _shared import COLORS, ZETA_ZEROS, math_check, save_gif

TMAX = 50.0
N_GRID = 600
N_FRAMES = 80
START_HOLD = 4
END_HOLD = 8


def hardy_z(ts: np.ndarray) -> np.ndarray:
    """Hardy Z(t) on the grid ts via mpmath.siegelz."""
    import mpmath

    return np.array([float(mpmath.siegelz(t)) for t in ts])


def sign_change_times(ts: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Linear-interpolated t at each sign change of z (the on-line zeros)."""
    idx = np.where(np.sign(z[:-1]) * np.sign(z[1:]) < 0)[0]
    out = []
    for i in idx:
        t0, t1, z0, z1 = ts[i], ts[i + 1], z[i], z[i + 1]
        out.append(t0 - z0 * (t1 - t0) / (z1 - z0))
    return np.array(out)


def main():
    ts = np.linspace(0.0, TMAX, N_GRID)
    z = hardy_z(ts)
    crossings = sign_change_times(ts, z)

    gammas_below = ZETA_ZEROS[ZETA_ZEROS < TMAX]
    n_expected = len(gammas_below)

    assert len(crossings) == n_expected, f"Z has {len(crossings)} sign changes on [0,50], expected {n_expected}"
    matched = [float(np.min(np.abs(crossings - g))) for g in gammas_below]
    assert max(matched) < 0.2, f"a gamma_k is not matched by a sign change (max gap {max(matched):.3f})"

    math_check(
        "Zeros on the line: sign changes of Hardy Z(t) on [0, 50]",
        [
            ("sign changes of Z on [0,50]", f"{len(crossings)}   (want 10)"),
            ("ZETA_ZEROS with gamma < 50", f"{n_expected}"),
            ("first crossings of Z", "  ".join(f"{c:.2f}" for c in crossings[:5]) + " ..."),
            ("first gamma_k < 50", "  ".join(f"{g:.2f}" for g in gammas_below[:5]) + " ..."),
            ("max |crossing - gamma_k|", f"{max(matched):.4f}   (< 0.2)"),
            ("|Z(t)| = |zeta(1/2+it)|", "real proxy for the modulus on the line"),
        ],
    )

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.grid(True, color="#e6e6e6", lw=0.8)
    ax.set_axisbelow(True)

    zmax = float(np.max(np.abs(z))) * 1.1
    schedule = [0] * START_HOLD + list(range(1, N_FRAMES + 1)) + [N_FRAMES] * END_HOLD

    def update(fi):
        ax.cla()
        ax.grid(True, color="#e6e6e6", lw=0.8)
        ax.set_axisbelow(True)
        frac = schedule[fi] / N_FRAMES
        t_now = frac * TMAX
        mask = ts <= t_now

        ax.axhline(0.0, color=COLORS["guide"], lw=0.8, ls="--")
        ax.plot(ts[mask], z[mask], color=COLORS["zero"], lw=1.6)

        revealed = crossings[crossings <= t_now]
        ax.plot(revealed, np.zeros_like(revealed), "o", color=COLORS["line"], ms=6, zorder=4)

        if mask.any():
            ax.plot([ts[mask][-1]], [z[mask][-1]], "o", color=COLORS["prime"], ms=8, zorder=5)

        ax.set_xlim(0, TMAX)
        ax.set_ylim(-zmax, zmax)
        ax.set_xlabel("t")
        ax.set_ylabel("Z(t)")
        ax.set_title(f"Zeros on the line: Z(t)   ({len(revealed)} sign changes)")
        return []

    anim = FuncAnimation(fig, update, frames=len(schedule), interval=120, blit=False)
    print("wrote", save_gif(anim, fps=12, dpi=100))


if __name__ == "__main__":
    main()
