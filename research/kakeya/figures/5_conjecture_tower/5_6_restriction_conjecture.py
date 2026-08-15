"""Stein's restriction/extension conjecture (kakeya.md 5c-i).

Extension operator on a curved surface S^{n-1}:

    E g(x) = int_{S^{n-1}} g(w) e^{2 pi i x . w} dsigma(w),

each frequency-localised piece a wave packet: a thin tube tangent to the surface. The conjecture:

    || E g ||_{L^q(R^n)}  <~  || g ||_{L^inf(S^{n-1})}        for  q > 2n/(n-1),

with sharp threshold q = 2n/(n-1) (n = 2: q = 4; n = 3: q = 3). Drawn over a parabola y = a x^2
carpeted with tangent wave packets (centre on the curve, long axis along the tangent).

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/restriction_conjecture.py
"""
import numpy as np
from _shared import COLORS, math_check, new_axes, save_preview


def threshold_q(n: int) -> float:
    """Sharp restriction exponent q = 2n/(n-1)."""
    return 2.0 * n / (n - 1)


def parabola(a: float, xs: np.ndarray) -> np.ndarray:
    return np.column_stack([xs, a * xs * xs])


def tangent_unit(a: float, x: float) -> np.ndarray:
    """Unit tangent to y = a x^2 at x (dy/dx = 2 a x)."""
    d = np.array([1.0, 2.0 * a * x])
    return d / np.linalg.norm(d)


def wave_packet(a: float, x: float, length: float, width: float) -> np.ndarray:
    """Corners of a thin tube of given length/width, centred on the parabola at x, along the tangent."""
    p = np.array([x, a * x * x])
    t = tangent_unit(a, x)
    nrm = np.array([-t[1], t[0]])
    return np.array([
        p - (length / 2) * t - (width / 2) * nrm,
        p + (length / 2) * t - (width / 2) * nrm,
        p + (length / 2) * t + (width / 2) * nrm,
        p - (length / 2) * t + (width / 2) * nrm,
    ])


def main():
    a = 0.7
    xs_tube = np.linspace(-1.15, 1.15, 9)
    length, width = 0.55, 0.10
    packets = [wave_packet(a, float(x), length, width) for x in xs_tube]

    # tangency verification: long axis parallel to the curve tangent; centre on the curve
    angle_errs, center_errs = [], []
    for x, pk in zip(xs_tube, packets, strict=True):
        long_axis = pk[1] - pk[0]
        long_axis = long_axis / np.linalg.norm(long_axis)
        t = tangent_unit(a, float(x))
        angle_errs.append(abs(1.0 - abs(float(np.dot(long_axis, t)))))  # 0 iff parallel
        center = pk.mean(axis=0)
        center_errs.append(abs(float(center[1] - a * center[0] ** 2)))

    q2, q3 = threshold_q(2), threshold_q(3)
    math_check(
        "Restriction conjecture (Stein): threshold and tangency",
        [
            ("Eg(x) = int_{S^{n-1}} g e^{2pi i x.w} dsigma", "extension operator"),
            ("bound  ||Eg||_{L^q} <~ ||g||_inf", "for q > 2n/(n-1)"),
            ("threshold q = 2n/(n-1),  n = 2", f"{q2:.4f}  (want 4)"),
            ("threshold q = 2n/(n-1),  n = 3", f"{q3:.4f}  (want 3)"),
            ("n = 2 exact 2*2/(2-1)", "4"),
            ("n = 3 exact 2*3/(3-1)", "3"),
            ("packets drawn", f"{len(packets)}"),
            ("tangency: max |1 - |axis.tangent||", f"{max(angle_errs):.2e}  (< 1e-9 ok)"),
            ("centre-on-curve: max |y - a x^2|", f"{max(center_errs):.2e}  (< 1e-9 ok)"),
        ],
    )

    fig, ax = new_axes(1, figsize=(8, 6))
    xs = np.linspace(-1.35, 1.35, 400)
    curve = parabola(a, xs)
    ax.plot(curve[:, 0], curve[:, 1], color=COLORS["accent"], lw=2.4, zorder=3)
    for pk in packets:
        poly_xy = np.vstack([pk, pk[0]])
        ax.fill(poly_xy[:, 0], poly_xy[:, 1], color="#c8d0f0", alpha=0.75, zorder=1)
        ax.plot(poly_xy[:, 0], poly_xy[:, 1], color=COLORS["outer"], lw=1.1, zorder=2)
    # outward normal arrow on one packet
    x0 = 0.8625
    p0 = np.array([x0, a * x0 * x0])
    t0 = tangent_unit(a, x0)
    ext = np.array([t0[1], -t0[0]])  # exterior normal
    ax.annotate("", xy=tuple(p0 + 0.30 * ext), xytext=tuple(p0),
                arrowprops=dict(arrowstyle="->", color=COLORS["guide"], lw=1.3))
    ax.text(*(p0 + 0.37 * ext), r"$\omega$", fontsize=13, ha="left", va="top")
    ax.text(0.0, a * 1.35 ** 2 * 0.62,
            r"$Eg(x)=\int_{S^{n-1}} g(\omega)\,e^{2\pi i x\cdot\omega}\,d\sigma(\omega)$",
            ha="center", va="center", fontsize=13)
    ax.text(0.0, a * 1.35 ** 2 * 0.40,
            r"$\|Eg\|_{L^q}\lesssim\|g\|_\infty,\quad q>\frac{2n}{n-1}$",
            ha="center", va="center", fontsize=13)
    ax.set_title("Restriction: wave packets tangent to the paraboloid")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.35, a * 1.35 ** 2 + 0.15)
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
