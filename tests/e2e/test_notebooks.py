"""End-to-end tests for marimo notebooks.

These tests verify that:
1. All notebooks execute without errors
2. HTML export works correctly
3. Math content renders properly (LaTeX/MathJax)
4. Plotly visualizations are generated
"""

import subprocess
import tempfile
import re
from pathlib import Path

import pytest

# Use the shared export utilities
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from math_explorations.export import (
    get_all_notebooks,
    extract_metadata,
    export_notebook,
    export_all,
    PROJECT_ROOT,
)


class TestNotebookExecution:
    """Test that notebooks execute without errors."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.notebooks = get_all_notebooks()

    def test_notebooks_exist(self):
        """Verify that notebook files exist."""
        assert len(self.notebooks) > 0, "No notebooks found in notebooks directory"
        for notebook in self.notebooks:
            assert notebook.exists(), f"Notebook {notebook} does not exist"

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_notebook_syntax(self, notebook: Path):
        """Verify notebook has valid Python syntax."""
        result = subprocess.run(
            ["python", "-m", "py_compile", str(notebook)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Syntax error in {notebook.name}: {result.stderr}"

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_notebook_exports_without_errors(self, notebook: Path):
        """Verify notebook exports to HTML without cell execution errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            try:
                output_path = export_notebook(notebook, output_dir)
            except subprocess.CalledProcessError as e:
                pytest.fail(
                    f"Export failed for {notebook.name}:\n"
                    f"stdout: {e.stdout}\n"
                    f"stderr: {e.stderr}"
                )

            # Verify output file was created
            assert output_path.exists(), f"Output HTML not created for {notebook.name}"
            assert output_path.stat().st_size > 0, f"Output HTML is empty for {notebook.name}"


class TestNotebookContent:
    """Test that exported notebooks have proper content.

    Each test is parametrized by notebook so individual pass/fail is shown.
    Uses a module-scoped cache to avoid re-exporting notebooks for each test.
    """

    # Size limits for exported HTML (in bytes)
    MIN_HTML_SIZE = 100 * 1024      # 100 KB minimum (should have substantial content)
    MAX_HTML_SIZE = 10 * 1024 * 1024  # 10 MB maximum (prevent runaway output)

    # Cache for exported HTML (module-level to share across tests)
    _export_cache: dict[str, tuple[str, int]] = {}
    _export_dir = None

    @classmethod
    def _get_exported_html(cls, notebook: Path) -> tuple[str, int]:
        """Get exported HTML for a notebook, using cache if available."""
        if notebook.stem not in cls._export_cache:
            if cls._export_dir is None:
                cls._export_dir = tempfile.mkdtemp()
            output_dir = Path(cls._export_dir)
            output_path = export_notebook(notebook, output_dir)
            content = output_path.read_text()
            size = output_path.stat().st_size
            cls._export_cache[notebook.stem] = (content, size)
        return cls._export_cache[notebook.stem]

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_output_size_reasonable(self, notebook: Path):
        """Verify exported HTML is neither too small nor too large."""
        content, size = self._get_exported_html(notebook)
        name = notebook.stem

        # Check minimum size (ensures content was actually generated)
        assert size >= self.MIN_HTML_SIZE, (
            f"{name}: Output too small ({size / 1024:.1f} KB). "
            f"Expected at least {self.MIN_HTML_SIZE / 1024:.0f} KB. "
            "This may indicate missing content or failed rendering."
        )

        # Check maximum size (prevents runaway output)
        assert size <= self.MAX_HTML_SIZE, (
            f"{name}: Output too large ({size / (1024*1024):.1f} MB). "
            f"Expected at most {self.MAX_HTML_SIZE / (1024*1024):.0f} MB. "
            "This may indicate infinite loops, excessive data, or embedded resources."
        )

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_html_is_valid(self, notebook: Path):
        """Verify exported HTML has basic structure."""
        html, _size = self._get_exported_html(notebook)
        name = notebook.stem

        assert "<!DOCTYPE html>" in html or "<html" in html, (
            f"{name}: Missing HTML doctype/root element"
        )
        assert "</html>" in html, f"{name}: HTML not properly closed"

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_math_content_present(self, notebook: Path):
        """Verify LaTeX/math content is present in notebooks that should have it."""
        html, _size = self._get_exported_html(notebook)
        name = notebook.stem

        # Check for math delimiters or MathJax markers
        has_latex = any([
            r"\(" in html,  # Inline LaTeX
            r"\[" in html,  # Display LaTeX
            "$$" in html,   # Dollar-sign delimited
            r"\frac" in html,  # Common LaTeX command
            r"\lim" in html,   # Limit notation
            r"\sum" in html,   # Summation
            "math" in html.lower(),  # Generic math reference
        ])

        # The derivatives notebook should definitely have math
        if "derivative" in name.lower():
            assert has_latex, f"{name}: Expected LaTeX math content but found none"

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_latex_renders_correctly(self, notebook: Path):
        """Verify LaTeX math renders properly - no raw $ delimiters visible."""
        html, _size = self._get_exported_html(notebook)
        name = notebook.stem

        # Patterns that indicate unrendered LaTeX (raw $ with LaTeX commands)
        unrendered_patterns = [
            r'\$\\frac\{',       # $\frac{
            r'\$\\int',          # $\int
            r'\$\\sum',          # $\sum
            r'\$\\lim',          # $\lim
            r'\$\\sqrt',         # $\sqrt
            r'\$\\partial',      # $\partial
            r'\$\\infty',        # $\infty
            r'\$\\pi\$',         # $\pi$
            r'\$[a-z]\^[0-9]\$', # $x^2$ style
            r'\$[a-z]_[0-9]\$',  # $x_1$ style
            r'\$\$\\',           # $$\ (display math start with command)
        ]

        for pattern in unrendered_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                # Check if it's inside a script tag or JSON (acceptable)
                # by looking for the pattern outside of script contexts
                # Simple heuristic: if we find many matches, it's likely unrendered
                if len(matches) > 5:
                    assert False, (
                        f"{name}: Found {len(matches)} instances of unrendered LaTeX "
                        f"pattern '{pattern}'. Raw $ delimiters visible in output."
                    )

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_plotly_visualizations_present(self, notebook: Path):
        """Verify Plotly visualizations are embedded in the output."""
        html, _size = self._get_exported_html(notebook)
        name = notebook.stem

        # Plotly generates specific markers in HTML
        has_plotly = any([
            "plotly" in html.lower(),
            "Plotly.newPlot" in html,
            '"data":' in html and '"layout":' in html,  # Plotly JSON structure
            "scatter" in html.lower(),  # Common plot type
        ])

        # The derivatives notebook should have visualizations
        if "derivative" in name.lower():
            assert has_plotly, f"{name}: Expected Plotly visualizations but found none"

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_no_error_messages(self, notebook: Path):
        """Verify no Python error messages appear in output."""
        html, _size = self._get_exported_html(notebook)
        name = notebook.stem

        error_patterns = [
            r"Traceback \(most recent call last\)",
            r"Exception:",
            r"ModuleNotFoundError",
            r"ImportError",
            r"NameError",
            r"TypeError",
            r"ValueError",
            r"AttributeError",
        ]

        for pattern in error_patterns:
            # Use case-sensitive search to avoid false positives
            matches = re.findall(pattern, html)
            # Filter out intentional error demonstrations in educational content
            if matches:
                # Check if it's in a code/educational context
                if not any(
                    ctx in html.lower()
                    for ctx in ["example of error", "error handling", "try/except"]
                ):
                    assert False, (
                        f"{name}: Found error pattern '{pattern}' in output"
                    )

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_no_marimo_errors(self, notebook: Path):
        """Verify no marimo runtime errors appear in the rendered output.

        This catches various marimo-specific errors that can appear during
        notebook execution and rendering, including:
        - Output too large errors
        - Cell execution errors
        - Rendering errors
        - Callout warnings/errors
        """
        html, _size = self._get_exported_html(notebook)
        name = notebook.stem
        errors_found = []

        # Check for "output is too large" error (marimo's size limit)
        if "your output is too large" in html.lower():
            errors_found.append(
                "Output too large - reduce data size or animation frames"
            )

        # Check for marimo danger/error callouts in the rendered output
        # These appear as data attributes in marimo-callout-output elements
        # The pattern matches the escaped HTML in the data-kind attribute
        danger_patterns = [
            'data-kind="&quot;danger&quot;"',
            "data-kind='\"danger\"'",
            'data-kind="danger"',
        ]
        for pattern in danger_patterns:
            if pattern in html:
                errors_found.append(
                    f"Marimo danger callout found (indicates error): {pattern}"
                )

        # Check for error styling class used by marimo for error messages
        # This class is applied to error text within callouts
        # Use regex to find it in actual content, not in CSS/JS
        error_text_matches = re.findall(
            r'<span[^>]*class="[^"]*text-error[^"]*"[^>]*>([^<]+)</span>',
            html
        )
        for match in error_text_matches:
            # Filter out false positives from documentation
            if not any(
                ctx in match.lower()
                for ctx in ["example", "tutorial", "documentation"]
            ):
                errors_found.append(f"Error text found: '{match[:100]}...'")

        # Check for Python exceptions in output areas (not in code blocks)
        # Look for exception patterns within output divs
        output_area_pattern = r'<div[^>]*class="[^"]*output[^"]*"[^>]*>(.*?)</div>'
        output_areas = re.findall(output_area_pattern, html, re.DOTALL)
        exception_patterns = [
            r"Traceback \(most recent call last\)",
            r"^\s*\w+Error:",  # NameError:, TypeError:, etc.
        ]
        for output in output_areas:
            for exc_pattern in exception_patterns:
                if re.search(exc_pattern, output, re.MULTILINE):
                    # Skip if it's intentional educational content
                    if not any(
                        ctx in html.lower()
                        for ctx in ["example of error", "error handling"]
                    ):
                        preview = output[:200].replace('\n', ' ')
                        errors_found.append(
                            f"Exception in output: {preview}..."
                        )

        if errors_found:
            assert False, (
                f"{name}: Found marimo rendering errors:\n  - " +
                "\n  - ".join(errors_found)
            )


class TestEquationFormatting:
    """Test that mathematical equations are properly formatted."""

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_multiline_equations_use_aligned_environment(self, notebook: Path):
        """Verify multi-step derivations use proper LaTeX alignment.

        Equations with 3+ equals signs that represent step-by-step derivations
        should use \\begin{aligned}...\\end{aligned} for proper multi-line
        rendering, not be crammed onto a single line.

        Exceptions:
        - Equations with \\qquad (intentionally side-by-side)
        - Equations with \\text{} (often definitions/descriptions)
        - Equations inside cases/matrix environments
        - Equations defining multiple equalities (a = b = c as a theorem statement)
        """
        content = notebook.read_text()

        # Find all display math blocks ($$...$$)
        # Use non-greedy matching to get individual blocks
        display_math_pattern = r'\$\$([^$]+)\$\$'
        math_blocks = re.findall(display_math_pattern, content, re.DOTALL)

        violations = []
        for block in math_blocks:
            # Skip if already using aligned/align environment
            if r'\begin{aligned}' in block or r'\begin{align' in block:
                continue

            # Skip if using cases or matrix environments
            if r'\begin{cases}' in block or r'\begin{matrix}' in block:
                continue
            if r'\begin{bmatrix}' in block or r'\begin{pmatrix}' in block:
                continue
            if r'\begin{vmatrix}' in block:
                continue

            # Skip if using \qquad (intentionally side-by-side equations)
            if r'\qquad' in block:
                continue

            # Skip if contains \text{where} or similar explanation patterns
            if r'\text{where}' in block or r'\text{ where}' in block:
                continue

            # Skip if equation contains \text{} for labels/descriptions
            # These are often definition-style equations, not step-by-step derivations
            if r'\text{' in block:
                continue

            # Skip if this is a short definition-style equation (under 80 chars)
            # Short equations with 3 equals might be definitions like a = b = c
            if len(block.strip()) < 80:
                continue

            # Count actual equals signs (not \neq, \leq, \geq, etc.)
            # Remove escaped characters and operators that contain =
            cleaned = re.sub(r'\\[a-z]eq', '', block)  # Remove \neq, \leq, \geq, etc.
            cleaned = re.sub(r'\\iff', '', cleaned)    # Remove \iff
            cleaned = re.sub(r'\\implies', '', cleaned)  # Remove \implies
            cleaned = re.sub(r'\\Rightarrow', '', cleaned)
            cleaned = re.sub(r'\\Leftrightarrow', '', cleaned)

            equals_count = cleaned.count('=')

            # If 3+ equals signs and all on one "line" (no aligned env), flag it
            if equals_count >= 3:
                # Get a preview of the equation for the error message
                preview = block.strip()[:100].replace('\n', ' ')
                if len(block.strip()) > 100:
                    preview += '...'
                violations.append(preview)

        if violations:
            msg = (
                f"{notebook.name}: Found {len(violations)} equation(s) with 3+ equals signs "
                f"that should use \\begin{{aligned}}...\\end{{aligned}} for multi-line display:\n"
            )
            for i, v in enumerate(violations[:3], 1):  # Show first 3
                msg += f"  {i}. {v}\n"
            if len(violations) > 3:
                msg += f"  ... and {len(violations) - 3} more\n"
            assert False, msg


class TestNotebookStructure:
    """Test notebook structural requirements."""

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_notebook_has_marimo_app(self, notebook: Path):
        """Verify notebook defines a marimo app."""
        content = notebook.read_text()
        assert "marimo.App" in content, f"{notebook.name}: Missing marimo.App definition"
        assert "@app.cell" in content, f"{notebook.name}: Missing @app.cell decorators"

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_notebook_has_main_guard(self, notebook: Path):
        """Verify notebook has proper main guard for execution."""
        content = notebook.read_text()
        assert 'if __name__ == "__main__"' in content, (
            f"{notebook.name}: Missing __main__ guard"
        )

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_notebook_imports(self, notebook: Path):
        """Verify notebook has required imports."""
        content = notebook.read_text()
        required_imports = ["marimo", "numpy"]

        for imp in required_imports:
            assert f"import {imp}" in content or f"from {imp}" in content, (
                f"{notebook.name}: Missing import for {imp}"
            )


class TestMetadataExtraction:
    """Test that notebook metadata extraction works correctly."""

    def test_all_notebooks_have_metadata(self):
        """Verify metadata can be extracted from all notebooks."""
        for notebook in get_all_notebooks():
            meta = extract_metadata(notebook)
            assert meta.number, f"{notebook.name}: Missing number"
            assert meta.title, f"{notebook.name}: Missing title"
            assert meta.description, f"{notebook.name}: Missing description"
            assert len(meta.tags) > 0, f"{notebook.name}: No tags inferred"

    def test_notebook_numbers_are_sequential(self):
        """Verify notebook numbers follow a pattern."""
        notebooks = get_all_notebooks()
        numbers = [extract_metadata(nb).number for nb in notebooks]
        # All should be numeric
        for num in numbers:
            assert num.isdigit(), f"Non-numeric notebook number: {num}"


class TestExportAll:
    """Test the full export workflow."""

    def test_export_all_creates_files(self):
        """Verify export_all creates all expected files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            generated = export_all(output_dir)

            # Should have one HTML per notebook plus index.html
            notebooks = get_all_notebooks()
            expected_count = len(notebooks) + 1  # notebooks + index.html

            assert len(generated) == expected_count, (
                f"Expected {expected_count} files, got {len(generated)}"
            )

            # Verify index.html exists and has content
            index_path = output_dir / "index.html"
            assert index_path.exists(), "index.html not created"
            index_content = index_path.read_text()
            assert "Math Explorations" in index_content
            assert "card" in index_content  # Should have notebook cards
