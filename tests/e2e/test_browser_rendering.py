"""Browser rendering tests for exported marimo notebooks.

Uses Playwright to verify that exported HTML actually renders
in a real browser — catching JS failures, blank pages, and
missing content that static HTML parsing would miss.
"""

import contextlib
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from math_explorations.export import export_notebook, get_all_notebooks

RENDER_TIMEOUT = 10
MIN_OUTPUT_COUNT = 3
PAGE_TIMEOUT = 60000


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
    """Serve the exported docs via file:// URI."""
    doc_dir = next(iter(exported_docs.values())).parent
    return f"file://{doc_dir}"


@pytest.fixture(scope="module")
def browser_context(http_server, exported_docs):
    """Launch a shared browser context with warmed CDN cache for all tests."""
    _ensure_playwright_browsers()
    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context()
    context.route("**/health", lambda route: route.fulfill(status=404, body=""))
    context.route(
        "**/gtag/js*", lambda route: route.fulfill(status=200, content_type="application/javascript", body="")
    )
    context.route("*google-analytics*/**", lambda route: route.fulfill(status=204, body=""))

    first_html = next(iter(exported_docs.values())).name
    warmup_page = context.new_page()
    try:
        warmup_page.goto(f"{http_server}/{first_html}", wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)
        with contextlib.suppress(Exception):
            warmup_page.wait_for_selector(".marimo", timeout=RENDER_TIMEOUT * 1000)
    finally:
        warmup_page.close()

    yield context
    context.close()
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
        page.goto(f"{http_server}/{html_file}", wait_until="commit", timeout=PAGE_TIMEOUT)
        page.wait_for_selector("#root", timeout=10000)
        page.close()

    @pytest.mark.parametrize("notebook", get_all_notebooks(), ids=lambda p: p.stem)
    def test_no_javascript_errors(self, notebook, exported_docs, http_server, browser_context):
        """Verify no uncaught JavaScript exceptions during rendering."""
        page = browser_context.new_page()
        page_errors = []
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        html_file = exported_docs[notebook.stem].name
        page.goto(f"{http_server}/{html_file}", wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)
        with contextlib.suppress(Exception):
            page.wait_for_selector(".marimo", timeout=RENDER_TIMEOUT * 1000)
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
        page.goto(f"{http_server}/{html_file}", wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)
        with contextlib.suppress(Exception):
            page.wait_for_selector(".marimo", timeout=RENDER_TIMEOUT * 1000)
        page.close()

        if failed:
            pytest.fail(f"{notebook.stem}: {len(failed)} failed resource(s):\n" + "\n".join(failed[:10]))
