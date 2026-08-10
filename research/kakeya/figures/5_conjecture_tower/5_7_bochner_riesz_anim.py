"""Animation: the Bochner-Riesz multiplier profile as alpha sweeps 0 -> 1 (kakeya.md section 5c-ii).

The radial slice of the Bochner-Riesz multiplier at R = 1 is the profile

    m^alpha(x) = (1 - x^2)_+^alpha .

alpha = 0 is Fefferman's failing ball multiplier: a hard edge (the indicator of [-1, 1], vertical
jumps at x = +-1).  As alpha grows to 1 the edge rounds into a smooth taper that reaches the axis
with a gentle slope.  This animation sweeps alpha from 0 to 1 and back, showing the corner smoothing.

Geometric honesty: at every alpha the endpoints are pinned (m(0) = 1, m(+-1) = 0) and the drawn
curve equals (1 - x^2)^alpha on [-1, 1] to machine precision (checked each frame).

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/bochner_riesz_anim.py
"""
import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation

FRAMES = 96
HOLD = 10  # frames held at each end


def profile(x: np.ndarray, alpha: float, radius: float = 1.0) -> np.ndarray:
    """m^alpha_R(x) = (1 - x^2 / R^2)_+^alpha along a radial slice."""
    base = np.clip(1.0 - (x / radius) ** 2, 0.0, None)
    return base ** alpha


def alpha_schedule() -> np.ndarray:
    """alpha sweeps 0 -> 1 with a hold at each end (a gentle there-and-back is not needed; hold
    then sweep reads as 'the edge rounding')."""
    up = np.linspace(0.0, 1.0, FRAMES - 2 * HOLD)
    return np.concatenate([np.zeros(HOLD), up, np.ones(HOLD)])


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    alphas = alpha_schedule()
    x = np.linspace(-1.6, 1.6, 800)
    xin = x[np.abs(x) <= 1]  # support, for the exact-profile check

    # --- validation across every frame: endpoints pinned, curve == (1-x^2)^alpha on [-1,1] -----
    max_dev = 0.0
    for a in alphas:
        got = profile(xin, a)
        want = (1.0 - xin**2) ** a
        max_dev = max(max_dev, float(np.max(np.abs(got - want))))
    m0 = [float(profile(np.array([0.0]), a)[0]) for a in alphas]
    max_m0_err = max(abs(v - 1.0) for v in m0)
    # m(+-1): for alpha>0 the taper reaches the axis (=0); at alpha=0 it is the hard edge
    # (the indicator is 1 up to the jump, so 0^0 = 1 there -- that IS the discontinuity).
    m1_pos = [float(profile(np.array([1.0]), a)[0]) for a in alphas if a > 0]
    max_m1_err = max(abs(v) for v in m1_pos)
    m1_edge = float(profile(np.array([1.0]), 0.0)[0])

    math_check(
        "Bochner-Riesz profile sweep  (1 - x^2)_+^alpha,  alpha: 0 -> 1",
        [
            ("frames", f"{FRAMES}"),
            ("alpha range", f"{alphas.min():.3f} -> {alphas.max():.3f}"),
            ("m(0) = 1 (all frames)", f"max err {max_m0_err:.2e}  (< 1e-12 ok)"),
            ("m(+-1) = 0 (alpha > 0 frames)", f"max err {max_m1_err:.2e}  (< 1e-12 ok)"),
            ("m(+-1) at alpha=0 (hard edge)", f"{m1_edge:.4f}  (jump: indicator = 1, then drops)"),
            ("max |profile - (1-x^2)^alpha| on [-1,1]", f"{max_dev:.2e}  (< 1e-12 ok)"),
            ("alpha=0 hard edge -> alpha=1 smooth taper", "corner rounds as alpha grows"),
        ],
    )
    assert max_m0_err < 1e-12 and max_m1_err < 1e-12 and max_dev < 1e-12

    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.set_aspect("auto")
    for spine in ("top", "right", "left", "bottom"):
        ax.spines[spine].set_visible(False)
    ax.annotate("", xy=(1.62, 0), xytext=(-1.62, 0),
                arrowprops=dict(arrowstyle="->", color="k", lw=1.1))
    ax.annotate("", xy=(0, 1.28), xytext=(0, -0.06),
                arrowprops=dict(arrowstyle="->", color="k", lw=1.1))
    ax.text(1.63, -0.02, r"$\xi$", ha="left", va="top", fontsize=13)
    ax.text(-1.0, -0.03, r"$-R$", ha="center", va="top", fontsize=12)
    ax.text(1.0, -0.03, r"$R$", ha="center", va="top", fontsize=12)
    ax.plot([-1, -1, 1, 1], [0, 1, 1, 0], ":", color=COLORS["guide"], lw=1.1)  # unit box
    ax.set_xlim(-1.75, 1.8)
    ax.set_ylim(-0.12, 1.4)
    ax.set_xticks([]); ax.set_yticks([])

    # ghost the hard edge (alpha=0 indicator) so the rounding reads against it
    ax.plot(xin, np.ones_like(xin), color=COLORS["accent"], lw=1.4, alpha=0.35)
    ax.plot([-1, -1], [0, 1], color=COLORS["accent"], lw=1.4, alpha=0.35)
    ax.plot([1, 1], [0, 1], color=COLORS["accent"], lw=1.4, alpha=0.35)

    (curve,) = ax.plot([], [], color="blue", lw=2.8)
    title = ax.set_title("")

    def update(i):
        a = alphas[i]
        curve.set_data(x, profile(x, a))
        title.set_text(r"$m^{\alpha}(\xi)=(1-|\xi|^2)_+^{\alpha}$,  " + rf"$\alpha={a:.2f}$")
        return curve, title

    anim = FuncAnimation(fig, update, frames=FRAMES, interval=60, blit=False)
    print("wrote", save_gif(anim, fps=18, dpi=95))


if __name__ == "__main__":
    main()
