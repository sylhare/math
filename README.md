# Math Explorations

Interactive mathematics explorations using [marimo](https://marimo.io) notebooks.

## Overview

This project presents mathematical concepts through:
- **Historical narrative** — Learn how ideas developed, who discovered them, and why they matter
- **Animated visualizations** — Interactive Plotly charts that make abstract concepts tangible
- **Primary sources** — Links to original papers and modern learning resources

## Notebooks

### 001 — Functions and Derivatives

A journey through the birth of calculus:
- The Great Problem of the 17th Century
- Newton's Method of Fluxions and Leibniz's Infinitesimals
- What is a function? Interactive explorer
- From secant lines to tangent lines: the limit process
- The Power Rule, Chain Rule, and more
- Applications: projectile motion, optimization
- A glimpse of integration: Riemann sums

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/math.git
cd math

# Install dependencies with uv
uv sync

# Or with pip
pip install -e .
```

### Running Notebooks

```bash
# Interactive editing
uv run marimo edit notebooks/001_functions_and_derivatives.py

# Run as app (read-only)
uv run marimo run notebooks/001_functions_and_derivatives.py
```

### Exporting to HTML

```bash
# Export all notebooks to docs/
./scripts/export_notebooks.sh
```

### Running Tests

```bash
# Run all tests including e2e notebook tests
uv run pytest

# Run only notebook e2e tests
uv run pytest tests/e2e/
```

## Technologies

- **[marimo](https://marimo.io)** — Reactive Python notebooks
- **[Plotly](https://plotly.com)** — Interactive visualizations
- **[SymPy](https://sympy.org)** — Symbolic mathematics
- **[NumPy](https://numpy.org)** — Numerical computing
- **[Polars](https://pola.rs)** — Data manipulation

## Inspiration

This project is inspired by:
- Grant Sanderson's [3Blue1Brown](https://www.3blue1brown.com) visual mathematics
- The belief that mathematics should be explored, not just memorized

## License

MIT
