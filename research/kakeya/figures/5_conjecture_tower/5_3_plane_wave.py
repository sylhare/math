"""Figure: level sets of a plane wave  x -> cos(2 pi x . xi)  in R^2 (Hickman Fig 4, Part 4).

A single Fourier mode  e^{2 pi i x . xi}  has real part  cos(2 pi x . xi).  Its level sets are
parallel straight stripes:

  * wavefronts (lines  x . xi = const) are PERPENDICULAR to the frequency vector xi;
  * successive crests are one WAVELENGTH apart, and the wavelength is  1 / |xi|.

This is the building block behind the whole Fourier tower in ../kakeya.md: a "wave packet" is such
a plane wave cut off to a tube, and stacking packets tangent to a curved surface is what makes
Kakeya geometry control the Fourier transform.

Verification is a genuine measurement, not a restatement of the formula: we sample the field on a
grid, take its 2D FFT, and read the dominant frequency bin. The measured frequency vector recovers
xi, so measured spacing = 1/|xi| and measured stripe normal = xi/|xi|. Two different xi are shown.

Reference: Hickman Fig 4 (not downloaded; redrawn from the description). Equal-aspect spatial plot.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/plane_wave.py
"""
import numpy as np
from _shared import COLORS, math_check, save_preview


def plane_wave_field(xi: tuple[float, float], L: float, n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Sample cos(2 pi x . xi) on an n x n grid over [0, L]^2. Returns (X, Y, field)."""
    coords = np.linspace(0.0, L, n, endpoint=False)  # periodic sampling for a clean FFT
    xg, yg = np.meshgrid(coords, coords)
    field = np.cos(2 * np.pi * (xg * xi[0] + yg * xi[1]))
    return xg, yg, field


def measure_frequency(field: np.ndarray, L: float) -> np.ndarray:
    """Recover the frequency vector (cycles per unit length) from the dominant FFT bin."""
    n = field.shape[0]
    spec = np.abs(np.fft.fft2(field))
    spec[0, 0] = 0.0  # ignore the DC term
    iy, ix = np.unravel_index(int(np.argmax(spec)), spec.shape)
    freqs = np.fft.fftfreq(n, d=L / n)  # bin -> cycles per unit length
    return np.array([abs(freqs[ix]), abs(freqs[iy])])


def main():
    L, n = 3.0, 600  # integer L keeps chosen xi exactly on FFT bins
    cases = [(3.0, 0.0), (2.0, 2.0)]  # vertical stripes; diagonal stripes

    rows = [("field", "cos(2 pi x . xi);  wavelength = 1/|xi|, wavefronts perp. to xi")]
    fields = []
    for xi in cases:
        xg, yg, field = plane_wave_field(xi, L, n)
        fields.append((xg, yg, field))
        xi_vec = np.array(xi)
        mag = np.hypot(*xi)
        meas = measure_frequency(field, L)
        meas_mag = np.hypot(*meas)
        spacing_true, spacing_meas = 1.0 / mag, 1.0 / meas_mag
        normal_true = xi_vec / mag
        normal_meas = meas / meas_mag
        cos_align = float(np.dot(normal_true, normal_meas))
        rows.append((f"xi = {xi}   |xi| = {mag:.4f}", ""))
        rows.append(("  spacing  1/|xi|", f"true {spacing_true:.4f}  measured {spacing_meas:.4f}"))
        rows.append(("  stripe normal  xi/|xi|", f"true [{normal_true[0]:.3f},{normal_true[1]:.3f}] measured [{normal_meas[0]:.3f},{normal_meas[1]:.3f}]"))
        rows.append(("  spacing match / normal aligned?", f"{'YES' if abs(spacing_true-spacing_meas) < 1e-3 else 'NO'} / cos={cos_align:.4f}"))
    math_check("plane wave level sets", rows)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 2, figsize=(11.5, 5.6))
    for a, xi, (xg, yg, field) in zip(ax, cases, fields, strict=True):
        a.imshow(field, origin="lower", extent=(0, L, 0, L), cmap="RdBu", vmin=-1, vmax=1)
        a.contour(xg, yg, field, levels=[0.0], colors="k", linewidths=0.5, alpha=0.4)
        a.set_aspect("equal")
        # arrow along xi from the centre, length one wavelength for scale
        mag = np.hypot(*xi)
        c = L / 2.0
        u = np.array(xi) / mag
        a.annotate(
            "", xy=(c + u[0] / mag, c + u[1] / mag), xytext=(c, c),
            arrowprops=dict(arrowstyle="-|>", color=COLORS["guide"], lw=2.0),
        )
        a.text(c, c - 0.18, "xi", color=COLORS["guide"], fontsize=11, ha="center", va="top", weight="bold")
        a.set_title(f"xi = {xi},  spacing = 1/|xi| = {1/mag:.3f}")
        a.set_xlabel("x")
        a.set_ylabel("y")
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
