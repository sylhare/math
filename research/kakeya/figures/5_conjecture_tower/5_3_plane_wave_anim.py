"""Traveling plane wave u(x, t) = cos(2 pi (x . xi - c t)) in R^2 (kakeya.md Part 4).

Rigid parallel stripes sliding along their normal. Wavefronts x . xi = const perpendicular to xi,
wavelength 1/|xi| (constant); crest advances at phase speed c/|xi| (displacement c/|xi| * dt per
frame). Wavelength and crest position measured from the dominant FFT bin each frame.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/plane_wave_anim.py
"""
import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation


def wave_field(xi: tuple[float, float], c: float, t: float, L: float, n: int) -> np.ndarray:
    """Sample cos(2 pi (x . xi - c t)) on an n x n grid over [0, L]^2."""
    coords = np.linspace(0.0, L, n, endpoint=False)  # periodic sampling for a clean FFT
    xg, yg = np.meshgrid(coords, coords)
    return np.cos(2 * np.pi * (xg * xi[0] + yg * xi[1] - c * t))


def measure_freq_phase(field: np.ndarray, L: float) -> tuple[float, float]:
    """From the dominant FFT bin, return (|frequency|, phase). Phase encodes the crest position.

    A real field has equal peaks at +xi and -xi; pick the one in a canonical half-plane
    (fx > 0, or fx == 0 and fy > 0) so the phase is tracked consistently across frames."""
    n = field.shape[0]
    spec = np.fft.fft2(field)
    mag = np.abs(spec)
    freqs = np.fft.fftfreq(n, d=L / n)
    fx = freqs[None, :] * np.ones((n, 1))
    fy = freqs[:, None] * np.ones((1, n))
    half = (fx > 1e-9) | ((np.abs(fx) <= 1e-9) & (fy > 1e-9))
    mag = np.where(half, mag, 0.0)  # keep only the canonical half-plane (drops DC too)
    iy, ix = np.unravel_index(int(np.argmax(mag)), mag.shape)
    freq_mag = float(np.hypot(freqs[ix], freqs[iy]))
    return freq_mag, float(np.angle(spec[iy, ix]))


def main():
    L, n = 2.0, 400          # integer-ish domain keeps xi close to FFT bins
    xi = (2.0, 1.0)
    xi_vec = np.array(xi)
    mag = float(np.hypot(*xi))         # |xi| = sqrt(5) ~ 2.2361
    wavelength = 1.0 / mag
    c = 1.0                             # phase speed factor
    frames = 50
    T = 1.5
    dt = T / frames
    ts = np.arange(frames) * dt

    # measure wavelength + crest position per frame
    lambdas, phases = [], []
    for t in ts:
        fmag, ph = measure_freq_phase(wave_field(xi, c, t, L, n), L)
        lambdas.append(1.0 / fmag)
        phases.append(ph)
    lambdas = np.array(lambdas)
    phases = np.unwrap(np.array(phases))
    # field ~ Re[e^{2 pi i x.xi} e^{-2 pi i c t}], so bin phase = -2 pi c t; crest normal
    # position s(t) = c t / |xi| = -phase / (2 pi |xi|). Per-frame displacement:
    crest_pos = -phases / (2 * np.pi * mag)
    disp = np.diff(crest_pos)
    disp_expected = c * dt / mag

    lambda_const = float(lambdas.std()) < 1e-6
    disp_const = float(disp.std()) < 1e-3
    disp_matches = abs(float(disp.mean()) - disp_expected) < 1e-3

    math_check(
        "traveling plane wave  cos(2 pi (x . xi - c t))  (animated)",
        [
            ("field", "u(x,t) = cos(2 pi (x . xi - c t))"),
            ("xi", f"{xi}   |xi| = {mag:.4f}"),
            ("wavelength 1/|xi| (constant?)", f"{wavelength:.4f}   measured min {lambdas.min():.4f} max {lambdas.max():.4f}  ->  {'YES' if lambda_const else 'NO'}"),
            ("phase speed c/|xi|", f"{c/mag:.4f}  (crest normal per unit t)"),
            ("per-frame displacement expected", f"{disp_expected:.5f}  (= c/|xi| * dt, dt={dt:.4f})"),
            ("per-frame displacement measured", f"mean {disp.mean():.5f}  std {disp.std():.2e}"),
            ("displacement constant & matches?", f"{'YES' if disp_const and disp_matches else 'NO'}"),
        ],
    )
    assert lambda_const, "wavelength 1/|xi| must be constant across frames"
    assert disp_const, "per-frame crest displacement must be constant (constant phase speed)"
    assert disp_matches, "measured crest displacement must equal c/|xi| * dt"

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    im = ax.imshow(wave_field(xi, c, 0.0, L, n), origin="lower", extent=(0, L, 0, L),
                   cmap="RdBu", vmin=-1, vmax=1, animated=True)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # static arrow along xi (one wavelength long), from the domain centre
    ctr = np.array([L / 2, L / 2])
    u = xi_vec / mag
    ax.annotate("", xy=tuple(ctr + u * wavelength), xytext=tuple(ctr),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["guide"], lw=2.0))
    ax.text(*(ctr - u * 0.12 + np.array([0.03, 0.0])), "xi", color=COLORS["guide"],
            fontsize=12, weight="bold")

    # moving wavefront: the crest line x.xi = c t, perpendicular to xi
    perp = np.array([-u[1], u[0]])
    front, = ax.plot([], [], color="k", lw=1.6)

    def update(i):
        t = ts[i]
        im.set_data(wave_field(xi, c, t, L, n))
        # crest nearest domain centre: signed offset so that (base) . xi = c t
        s = crest_pos[i]
        base = s * u
        base = base + np.round((ctr @ u - s) / wavelength) * wavelength * u  # shift to a crest near centre
        p0 = base - perp * L
        p1 = base + perp * L
        front.set_data([p0[0], p1[0]], [p0[1], p1[1]])
        ax.set_title(f"t = {t:.3f}    wavelength 1/|xi| = {wavelength:.3f}    crest at s = {s:.3f}")
        return im, front

    anim = FuncAnimation(fig, update, frames=frames, interval=60, blit=False)
    print("wrote", save_gif(anim, fps=18, dpi=76))


if __name__ == "__main__":
    main()
