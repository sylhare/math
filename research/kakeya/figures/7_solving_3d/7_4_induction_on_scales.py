"""Induction on scales, the dimension ratchet (kakeya.md beat 7e).

Induction on scales: assume the dimension bound K(d), bootstrap to K(d + alpha) for a fixed gain
alpha > 0, repeat until d reaches 3. The per-step multiplicity inequality decides the outcome:
  * lossy ("Chinese whispers"): mu <~ mu_fat * mu_fine over-counts the fat tube, so the estimate
    stalls below 3.
  * graininess: grains disjoint in a fat tube give mu <~ mu_coarse * mu_fine with mu_coarse <<
    mu_fat (mu_coarse = multiplicity of U_{T c T_rho} T), so each step gains alpha and the estimate
    ratchets 2.5 -> 3.

Schematic: alpha, start 2.5 and cap 3 are exact; the lossy leak is illustrative.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/induction_on_scales.py
"""
import numpy as np
from _shared import COLORS, math_check, save_preview

D_START = 2.5    # Wolff's 1995 lower bound in R^3 = (n+2)/2
D_TARGET = 3.0   # full dimension (Wang-Zahl)
ALPHA = 0.1      # fixed per-step gain of the graininess induction


def ratchet(d_start: float, d_target: float, alpha: float):
    """Graininess induction: gain exactly alpha per step, capped at d_target."""
    ds = [d_start]
    while ds[-1] < d_target - 1e-12:
        ds.append(min(d_target, ds[-1] + alpha))
    return np.array(ds)


def lossy(d_start: float, alpha: float, leak: float, n_steps: int):
    """Chinese-whispers induction: nominal gain alpha but a compounding leak, so the net gain
    per step shrinks and the estimate converges to a ceiling < 3."""
    ds = [d_start]
    for _ in range(n_steps):
        gain = alpha - leak * (ds[-1] - d_start)   # leak grows as we climb -> stalls
        ds.append(ds[-1] + max(0.0, gain))
    return np.array(ds)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    good = ratchet(D_START, D_TARGET, ALPHA)
    n_steps = len(good) - 1
    bad = lossy(D_START, ALPHA, leak=0.28, n_steps=n_steps)

    math_check(
        "induction on scales (dimension ratchet)",
        [
            ("start estimate K(d)", f"d = {D_START}  (Wolff 1995 bound (n+2)/2 in R^3)"),
            ("fixed per-step gain", f"alpha = {ALPHA}  ->  K(d) => K(d + alpha)"),
            ("steps to close the gap", f"{n_steps}  = (3 - 2.5) / alpha"),
            ("graininess ratchet reaches", f"{good[-1]:.3f}  (terminates at exactly 3)"),
            ("per-step increments", "  ".join(f"{good[i + 1] - good[i]:.2f}" for i in range(n_steps)) + "  (each = alpha)"),
            ("lossy 'Chinese whispers' stalls", f"{bad[-1]:.3f}  (< 3: compounding leak never closes the gap)"),
            ("lossy inequality", "mu <~ mu_fat * mu_fine        (fat tube over-counted -> wasteful)"),
            ("graininess inequality", "mu <~ mu_coarse * mu_fine     mu_coarse = mult of U_{T c T_rho} T"),
            ("why it works", "grains disjoint in a fat tube => mu_coarse << mu_fat => gain, not loss"),
        ],
    )

    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    steps = np.arange(n_steps + 1)

    ax.axhline(D_TARGET, color=COLORS["accent"], ls="--", lw=1.2, alpha=0.7)
    ax.text(0.05, D_TARGET + 0.008, "dimension 3 (Wang-Zahl: full)", color=COLORS["accent"], fontsize=10)

    # graininess ratchet: staircase up to 3 (red = grains)
    ax.step(steps, good, where="post", color=COLORS["accent"], lw=2.2, label="graininess: mu ~ mu_coarse * mu_fine")
    ax.plot(steps, good, "o", color=COLORS["accent"], ms=5)
    for i in range(n_steps):
        ax.annotate("", xy=(steps[i], good[i + 1]), xytext=(steps[i], good[i]),
                    arrowprops=dict(arrowstyle="->", color=COLORS["accent"], lw=1.1))
    ax.text(n_steps - 0.5, good[-1] - 0.045, "+alpha each step", color=COLORS["accent"], fontsize=9, ha="right")

    # lossy induction: stalls below 3 (blue = fat tube)
    ax.step(steps, bad, where="post", color=COLORS["outer"], lw=2.0, label="lossy: mu ~ mu_fat * mu_fine")
    ax.plot(steps, bad, "s", color=COLORS["outer"], ms=4)
    ax.text(n_steps, bad[-1] - 0.05, f"stalls at {bad[-1]:.2f}", color=COLORS["outer"], fontsize=9, ha="right")

    ax.axhline(D_START, color=COLORS["guide"], ls=":", lw=0.9, alpha=0.6)
    ax.text(0.05, D_START - 0.05, "start 2.5  (Wolff 1995)", color=COLORS["guide"], fontsize=9)

    ax.set_xlabel("induction step (scale)")
    ax.set_ylabel("dimension estimate")
    ax.set_ylim(2.35, 3.12)
    ax.set_xlim(-0.3, n_steps + 0.3)
    ax.set_xticks(steps)
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
    ax.set_title("Induction on scales: the dimension ratchet 2.5 -> 3", fontsize=12)
    ax.grid(True, alpha=0.15)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
