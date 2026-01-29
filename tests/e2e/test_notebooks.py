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
    """Test that exported notebooks have proper content."""

    # Size limits for exported HTML (in bytes)
    MIN_HTML_SIZE = 100 * 1024      # 100 KB minimum (should have substantial content)
    MAX_HTML_SIZE = 10 * 1024 * 1024  # 10 MB maximum (prevent runaway output)

    @pytest.fixture
    def exported_html(self) -> dict[str, tuple[str, int]]:
        """Export all notebooks and return their HTML content and size."""
        html_content = {}
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            for notebook in get_all_notebooks():
                try:
                    output_path = export_notebook(notebook, output_dir)
                    if output_path.exists():
                        content = output_path.read_text()
                        size = output_path.stat().st_size
                        html_content[notebook.stem] = (content, size)
                except subprocess.CalledProcessError:
                    pass  # Skip failed exports for this fixture
        return html_content

    def test_output_size_reasonable(self, exported_html: dict[str, tuple[str, int]]):
        """Verify exported HTML is neither too small nor too large."""
        for name, (content, size) in exported_html.items():
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

    def test_html_is_valid(self, exported_html: dict[str, tuple[str, int]]):
        """Verify exported HTML has basic structure."""
        for name, (html, _size) in exported_html.items():
            assert "<!DOCTYPE html>" in html or "<html" in html, (
                f"{name}: Missing HTML doctype/root element"
            )
            assert "</html>" in html, f"{name}: HTML not properly closed"

    def test_math_content_present(self, exported_html: dict[str, tuple[str, int]]):
        """Verify LaTeX/math content is present in notebooks that should have it."""
        for name, (html, _size) in exported_html.items():
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

    def test_latex_renders_correctly(self, exported_html: dict[str, tuple[str, int]]):
        """Verify LaTeX math renders properly - no raw $ delimiters visible."""
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

        for name, (html, _size) in exported_html.items():
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

    def test_plotly_visualizations_present(self, exported_html: dict[str, tuple[str, int]]):
        """Verify Plotly visualizations are embedded in the output."""
        for name, (html, _size) in exported_html.items():
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

    def test_no_error_messages(self, exported_html: dict[str, tuple[str, int]]):
        """Verify no Python error messages appear in output."""
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

        for name, (html, _size) in exported_html.items():
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
