"""Static: the closed-form moments, and G >= 0 built from real zeros.

Panel A reproduces the two closed forms the finite Weil form is measured against: Montgomery's
Cauchy-Schwarz form factor F(lambda) = lambda / (1 + lambda^2/3) (which is identically
1 / (1/lambda + lambda/3)) and the second-moment constant 1/lambda + lambda/3, over the known
bandwidth range lambda in [0.5, 1]. The marked point is F(1) = 3/4.

Panel B builds the finite compression G_{kl} = sum_j window(gamma_j - tau_k) window(gamma_j - tau_l)
from real zeta ordinates over an interior height window, with the tau_k spaced at one mean gap
(bandwidth lambda = 1) and window width sigma = mean gap. Because every zero at these heights is on
the line, G = sum_j v_j v_j^T is a Gram matrix and so G >= 0. Its sorted eigenvalues are all >= 0;
the minimum eigenvalue readout is the exact check. RH is verified this low, so this certifies
nothing new: G >= 0 from real zeros is the exact check.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
  python research/riemann/figures/7_numerical_framework/7_1_moments_convergence.py
"""

import numpy as np
from _shared import COLORS, math_check, plot_axes, save_preview

ZEROS_CACHE = "research/riemann/framework/zeros_cache.npy"
WIN_LO_IDX, WIN_HI_IDX = 100, 260


def form_factor(lam):
    """Montgomery's form factor F(lambda) = lambda / (1 + lambda^2/3) = 1/(1/lambda + lambda/3)."""
    return lam / (1.0 + lam**2 / 3.0)


def second_moment_constant(lam):
    """Closed form of tr G^2 / N in the proof's units: 1/lambda + lambda/3."""
    return 1.0 / lam + lam / 3.0


def build_gram(gammas, taus, sigma):
    """Finite compression G_{kl} = sum_j window(gamma_j - tau_k) window(gamma_j - tau_l), G >= 0."""
    atoms = np.exp(-0.5 * ((gammas[None, :] - taus[:, None]) / sigma) ** 2)
    return atoms @ atoms.T


def real_zero_gram():
    """Build G at bandwidth lambda = 1 from cached real ordinates over an interior window."""
    gammas = np.load(ZEROS_CACHE)
    lo, hi = gammas[WIN_LO_IDX], gammas[WIN_HI_IDX]
    inwin = gammas[(gammas >= lo) & (gammas <= hi)]
    mean_gap = float(np.mean(np.diff(inwin)))
    taus = np.arange(lo, hi, mean_gap)
    G = build_gram(gammas, taus, sigma=mean_gap)
    eig = np.linalg.eigvalsh((G + G.T) / 2.0)
    return eig, len(taus), mean_gap


def main():
    eig, d, mean_gap = real_zero_gram()
    eig_sorted = np.sort(eig)
    min_eig = float(eig_sorted[0])

    math_check(
        "moments: closed forms and G >= 0 from real zeros",
        [
            ("F(1) = 1/(1/1 + 1/3)", f"{form_factor(1.0):.4f}  (= 3/4)"),
            ("1/lambda + lambda/3 at lambda=1", f"{second_moment_constant(1.0):.4f}  (= 4/3)"),
            ("identity F = 1/(1/l+l/3) at l=0.7", f"{form_factor(0.7):.6f} = {1 / second_moment_constant(0.7):.6f}"),
            ("real-zero Gram size d", f"{d}"),
            ("min eigenvalue of G", f"{min_eig:+.3e}  (>= 0: on-line zeros give G >= 0)"),
            ("certifies nothing new here", "RH verified at these heights; G >= 0 is the exact check"),
        ],
    )
    assert min_eig > -1e-6, "on-line zeros must give a positive-semidefinite Gram matrix"
    assert abs(form_factor(1.0) - 0.75) < 1e-12
    assert abs(second_moment_constant(1.0) - 4.0 / 3.0) < 1e-12

    fig, axes = plot_axes(ncols=2, figsize=(11.6, 4.9))
    ax_a, ax_b = axes

    lams = np.linspace(0.5, 1.0, 200)
    ax_a.plot(lams, form_factor(lams), color=COLORS["zero"], lw=2.2, label=r"$F(\lambda)=\lambda/(1+\lambda^2/3)$")
    ax_a.plot(lams, second_moment_constant(lams), color=COLORS["prime"], lw=2.2, label=r"$1/\lambda+\lambda/3$")
    ax_a.plot([1.0], [0.75], "o", color=COLORS["zero"], ms=7, zorder=5)
    ax_a.annotate(
        r"$F(1)=3/4$",
        xy=(1.0, 0.75),
        xytext=(0.72, 0.92),
        fontsize=10,
        color=COLORS["zero"],
        arrowprops=dict(arrowstyle="->", color=COLORS["zero"], lw=1.0),
    )
    ax_a.plot([1.0], [4.0 / 3.0], "o", color=COLORS["prime"], ms=7, zorder=5)
    ax_a.text(0.83, 1.40, r"$4/3$", fontsize=10, color=COLORS["prime"])
    ax_a.set_xlim(0.5, 1.0)
    ax_a.set_ylim(0.35, 2.25)
    ax_a.set_xlabel(r"bandwidth $\lambda$")
    ax_a.set_title("Closed forms")
    ax_a.legend(loc="upper left", fontsize=9)

    idx = np.arange(1, len(eig_sorted) + 1)
    ax_b.bar(idx, eig_sorted, color=COLORS["onlinepos"], width=0.9, zorder=2)
    ax_b.axhline(0.0, color=COLORS["line"], lw=1.0, zorder=3)
    ax_b.text(
        0.03,
        0.95,
        f"real zeros, d = {d}\nmin eig = {min_eig:+.2e}\nall $\\geq 0$: $G \\succeq 0$",
        transform=ax_b.transAxes,
        va="top",
        ha="left",
        fontsize=10,
        color=COLORS["onlinepos"],
    )
    pad = 0.05 * float(eig_sorted[-1])
    ax_b.set_ylim(min(min_eig - pad, -pad), float(eig_sorted[-1]) + pad)
    ax_b.set_xlim(0.4, len(eig_sorted) + 0.6)
    ax_b.set_xlabel("eigenvalue index (sorted)")
    ax_b.set_title(r"Real zeros: $G \succeq 0$")

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
