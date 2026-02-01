"""
Notebook export utilities.

This module provides functions to:
- Discover notebooks in the notebooks directory
- Extract metadata (title, description, tags) from notebooks
- Export notebooks to HTML
- Generate the index.html page dynamically
"""

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
DOCS_DIR = PROJECT_ROOT / "docs"


@dataclass
class NotebookMetadata:
    """Metadata extracted from a notebook."""

    number: str
    stem: str
    title: str
    description: str
    tags: list[str]
    path: Path


def get_all_notebooks() -> list[Path]:
    """Get all notebook files in the notebooks directory, sorted by name."""
    return sorted(NOTEBOOKS_DIR.glob("*.py"))


def extract_metadata(notebook_path: Path) -> NotebookMetadata:
    """Extract metadata from a notebook file.

    Parses the notebook to find:
    - Number: from filename (e.g., "001" from "001_functions.py")
    - Title: from the first markdown heading
    - Description: from the docstring or first paragraph
    - Tags: inferred from content or explicit markers
    """
    content = notebook_path.read_text()
    stem = notebook_path.stem

    # Extract number from filename (e.g., "001" from "001_functions_and_derivatives")
    number_match = re.match(r"^(\d+)", stem)
    number = number_match.group(1) if number_match else "000"

    # Extract title from first markdown heading (# Title)
    title_match = re.search(r'mo\.md\(\s*r?"""[^"]*?#\s+([^\n]+)', content)
    if title_match:
        title = title_match.group(1).strip()
        # Clean up any trailing asterisks or formatting
        title = re.sub(r"\*+$", "", title).strip()
    else:
        # Fallback: convert filename to title
        title = stem.replace("_", " ").title()
        if number_match:
            title = title[len(number) :].strip()

    # Extract description from docstring at top of file
    docstring_match = re.match(r'^"""([^"]+)"""', content, re.MULTILINE)
    if docstring_match:
        desc_lines = docstring_match.group(1).strip().split("\n")
        # Skip the title line if present, get the description
        description = " ".join(
            line.strip() for line in desc_lines[1:] if line.strip()
        ).strip()
        if not description and desc_lines:
            description = desc_lines[0].strip()
    else:
        description = f"Interactive exploration of {title.lower()}."

    # Truncate description if too long
    if len(description) > 200:
        description = description[:197] + "..."

    # Infer tags from content
    tags = _infer_tags(content, stem)

    return NotebookMetadata(
        number=number,
        stem=stem,
        title=title,
        description=description,
        tags=tags,
        path=notebook_path,
    )


def _infer_tags(content: str, stem: str) -> list[str]:
    """Infer tags from notebook content and filename."""
    tags = []
    content_lower = content.lower()

    # Tag mappings: keyword -> tag
    tag_keywords = {
        "derivative": "Derivatives",
        "integral": "Integration",
        "limit": "Limits",
        "calculus": "Calculus",
        "riemann": "Riemann Sums",
        "gradient": "Gradients",
        "partial": "Partial Derivatives",
        "surface": "Surfaces",
        "set theory": "Set Theory",
        "axiom": "Axioms",
        "relation": "Relations",
        "function": "Functions",
        "cardinality": "Cardinality",
        "ordinal": "Ordinals",
        "cardinal": "Cardinals",
        "axiom of choice": "Axiom of Choice",
        "lattice": "Lattices",
        "cantor": "Cantor",
        "zorn": "Zorn's Lemma",
        "dedekind": "Dedekind Cuts",
        "numerical": "Numerical Methods",
        "monte carlo": "Monte Carlo",
        "history": "History",
        "double integral": "Double Integrals",
        "probability": "Probability",
        "bayes": "Bayes' Theorem",
        "conditional": "Conditional Probability",
        "distribution": "Distributions",
        "binomial": "Binomial",
        "poisson": "Poisson",
        "normal": "Normal Distribution",
        "expected value": "Expected Value",
        "variance": "Variance",
        "random": "Random Variables",
    }

    for keyword, tag in tag_keywords.items():
        if keyword in content_lower or keyword in stem.lower():
            if tag not in tags:
                tags.append(tag)

    # Limit to 4 most relevant tags
    return tags[:4] if tags else ["Mathematics"]


def export_notebook(notebook_path: Path, output_dir: Path, include_code: bool = False) -> Path:
    """Export a single notebook to HTML.

    Args:
        notebook_path: Path to the notebook file
        output_dir: Directory to write the HTML file
        include_code: Whether to include source code in output

    Returns:
        Path to the generated HTML file

    Raises:
        subprocess.CalledProcessError: If export fails
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{notebook_path.stem}.html"

    cmd = [
        "uv", "run", "marimo", "export", "html",
        str(notebook_path),
        "-o", str(output_path),
    ]
    if not include_code:
        cmd.append("--no-include-code")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        timeout=180,
    )

    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd, result.stdout, result.stderr
        )

    return output_path


def generate_index_html(notebooks: list[NotebookMetadata], output_dir: Path) -> Path:
    """Generate the index.html page from notebook metadata.

    Args:
        notebooks: List of notebook metadata
        output_dir: Directory to write the index.html file

    Returns:
        Path to the generated index.html file
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate notebook cards
    cards_html = "\n".join(_generate_card(nb) for nb in notebooks)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Math Explorations</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: Georgia, 'Times New Roman', Times, serif;
            background: #ffffff;
            color: #1a1a1a;
            min-height: 100vh;
            padding: 3rem 2rem;
            line-height: 1.7;
        }}

        .container {{
            max-width: 720px;
            margin: 0 auto;
        }}

        header {{
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid #e0e0e0;
        }}

        h1 {{
            font-size: 2.5rem;
            font-weight: normal;
            font-style: italic;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }}

        .subtitle {{
            font-size: 1.1rem;
            color: #c41e3a;
            margin-bottom: 1.5rem;
            font-style: normal;
        }}

        .description {{
            font-size: 1rem;
            color: #444444;
            line-height: 1.8;
        }}

        .notebooks {{
            display: flex;
            flex-direction: column;
            gap: 0;
        }}

        .card {{
            background: transparent;
            border: none;
            border-bottom: 1px solid #e0e0e0;
            padding: 1.5rem 0;
            text-decoration: none;
            color: inherit;
            display: block;
            transition: background-color 0.2s ease;
        }}

        .card:hover {{
            background-color: #fafafa;
        }}

        .card:last-child {{
            border-bottom: none;
        }}

        .card-number {{
            font-size: 0.9rem;
            color: #c41e3a;
            margin-bottom: 0.25rem;
            font-family: Georgia, serif;
        }}

        .card-title {{
            font-size: 1.25rem;
            font-weight: normal;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }}

        .card-description {{
            font-size: 0.95rem;
            color: #555555;
            line-height: 1.6;
            margin-bottom: 0.75rem;
        }}

        .card-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}

        .tag {{
            background: transparent;
            color: #888888;
            padding: 0;
            font-size: 0.85rem;
            font-style: italic;
        }}

        .tag::after {{
            content: ",";
        }}

        .tag:last-child::after {{
            content: "";
        }}

        footer {{
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #e0e0e0;
            color: #888888;
            font-size: 0.9rem;
        }}

        footer a {{
            color: #c41e3a;
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 2rem 1rem;
            }}

            h1 {{
                font-size: 1.8rem;
            }}

            .subtitle {{
                font-size: 1rem;
            }}

            .card-title {{
                font-size: 1.1rem;
            }}
        }}

        @media (max-width: 480px) {{
            body {{
                padding: 1.5rem 0.75rem;
            }}

            h1 {{
                font-size: 1.5rem;
            }}

            .card {{
                padding: 1rem 0;
            }}

            .card-title {{
                font-size: 1rem;
            }}

            .card-description {{
                font-size: 0.9rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Math Explorations</h1>
            <p class="subtitle">Interactive Mathematics</p>
            <p class="description">
                A collection of interactive notebooks exploring mathematics through
                historical narrative, animated visualizations, and hands-on exploration.
            </p>
        </header>

        <main class="notebooks">
{cards_html}
        </main>

        <footer>
            <p>
                Built with <a href="https://marimo.io">marimo</a> and
                <a href="https://plotly.com">Plotly</a>
            </p>
        </footer>
    </div>
</body>
</html>'''

    output_path = output_dir / "index.html"
    output_path.write_text(html)
    return output_path


def _generate_card(nb: NotebookMetadata) -> str:
    """Generate HTML for a single notebook card."""
    tags_html = "\n                    ".join(
        f'<span class="tag">{tag}</span>' for tag in nb.tags
    )

    return f'''            <a href="{nb.stem}.html" class="card">
                <div class="card-number">{nb.number}</div>
                <h2 class="card-title">{nb.title}</h2>
                <p class="card-description">
                    {nb.description}
                </p>
                <div class="card-tags">
                    {tags_html}
                </div>
            </a>'''


def export_all(output_dir: Path | None = None, include_code: bool = False) -> list[Path]:
    """Export all notebooks and generate index.html.

    Args:
        output_dir: Directory to write files (defaults to PROJECT_ROOT/docs)
        include_code: Whether to include source code in notebook exports

    Returns:
        List of all generated file paths
    """
    if output_dir is None:
        output_dir = DOCS_DIR

    output_dir.mkdir(parents=True, exist_ok=True)
    generated_files = []

    # Get all notebooks and extract metadata
    notebooks = get_all_notebooks()
    metadata_list = [extract_metadata(nb) for nb in notebooks]

    # Export each notebook
    print("Exporting marimo notebooks...")
    for meta in metadata_list:
        print(f"  Exporting {meta.stem}...")
        output_path = export_notebook(meta.path, output_dir, include_code)
        generated_files.append(output_path)

    # Generate index.html
    print("Generating index.html...")
    index_path = generate_index_html(metadata_list, output_dir)
    generated_files.append(index_path)

    print(f"Done! Output in {output_dir}/")
    return generated_files


if __name__ == "__main__":
    export_all()
