"""Browser rendering tests for exported marimo notebooks.

Uses Playwright to verify that exported HTML actually renders
in a real browser — catching JS failures, blank pages, and
missing content that static HTML parsing would miss.
"""

import http.server
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from math_explorations.export import export_notebook, get_all_notebooks

# How long to wait for marimo's JS to render (seconds)
RENDER_TIMEOUT = 20
# Minimum number of cell outputs expected from a successful export
MIN_OUTPUT_COUNT = 3


def _ensure_playwright_browsers():
    """Install Playwright browsers if not already installed."""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            p.chromium.launch(headless=True).close()
    except Exception:
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
            capture_output=True,
        )


@pytest.fixture(scope="module")
def exported_docs(tmp_path_factory):
    """Export all notebooks to a temp directory once per module."""
    output_dir = tmp_path_factory.mktemp("docs")
    notebooks = get_all_notebooks()
    paths = {}
    for nb in notebooks:
        output_path = export_notebook(nb, output_dir)
        paths[nb.stem] = output_path
    return paths


@pytest.fixture(scope="module")
def http_server(exported_docs):
    """Start a local HTTP server serving the exported docs."""
    doc_dir = next(iter(exported_docs.values())).parent

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(doc_dir), **kwargs)

        def log_message(self, format, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), QuietHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


@pytest.fixture(scope="module")
def browser_context():
    """Launch a shared browser instance for all tests."""
    _ensure_playwright_browsers()
    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    yield browser
    browser.close()
    pw.stop()


class TestBrowserRendering:
    """Verify notebooks render visible content in a real browser."""

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_export_has_outputs(self, notebook, exported_docs, http_server, browser_context):
        """Verify the export captured cell outputs and the page loads in a browser."""
        html_path = exported_docs[notebook.stem]
        html_content = html_path.read_text()

        output_count = html_content.count('"outputs": [')
        assert output_count >= MIN_OUTPUT_COUNT, (
            f"{notebook.stem}: Expected at least {MIN_OUTPUT_COUNT} cell outputs, found {output_count}"
        )

        page = browser_context.new_page()
        html_file = html_path.name
        page.goto(f"{http_server}/{html_file}", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_selector("#root", timeout=10000)
        page.close()

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_no_javascript_errors(self, notebook, exported_docs, http_server, browser_context):
        """Verify no uncaught JavaScript exceptions during rendering."""
        page = browser_context.new_page()
        page_errors = []
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        html_file = exported_docs[notebook.stem].name
        page.goto(f"{http_server}/{html_file}", wait_until="domcontentloaded", timeout=30000)
        time.sleep(RENDER_TIMEOUT)
        page.close()

        if page_errors:
            pytest.fail(f"{notebook.stem}: {len(page_errors)} JS error(s):\n" + "\n".join(page_errors[:5]))

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_no_critical_network_failures(self, notebook, exported_docs, http_server, browser_context):
        """Verify CDN resources (JS, CSS) load without errors.

        Ignores /health polling (expected 404 in static mode).
        """
        page = browser_context.new_page()
        failed = []

        def on_response(response):
            if response.status >= 400 and "/health" not in response.url:
                failed.append(f"{response.status} {response.url}")

        page.on("response", on_response)

        html_file = exported_docs[notebook.stem].name
        page.goto(f"{http_server}/{html_file}", wait_until="domcontentloaded", timeout=30000)
        time.sleep(RENDER_TIMEOUT)
        page.close()

        if failed:
            pytest.fail(f"{notebook.stem}: {len(failed)} failed resource(s):\n" + "\n".join(failed[:10]))
