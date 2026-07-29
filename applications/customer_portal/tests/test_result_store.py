"""Portal Result Storage tests.

Guards the single-owner storage contract: only ``BtePortal.ResultStore`` may
touch Web Storage, ``last_result`` and ``history`` live under separate keys, and
opening an existing chart never rewrites ``last_result``.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from applications.customer_portal.config import PORTAL_ROOT

JS_DIR = PORTAL_ROOT / "static" / "js"
STORE_JS = JS_DIR / "result_store.js"
FLOW_HARNESS = Path(__file__).parent / "js" / "result_store_flow.js"
READ_ONLY_PAGES = ("dashboard.js", "history.js", "reports.js")
REQUIRED_API = (
    "save",
    "load",
    "clear",
    "saveHistory",
    "loadHistory",
    "selectForView",
    "loadForView",
    "clearView",
)


def read_js(name: str) -> str:
    """Return the source of a portal static script."""
    return (JS_DIR / name).read_text(encoding="utf-8")


def test_result_store_module_exists() -> None:
    assert STORE_JS.is_file()


def test_result_store_exposes_public_api() -> None:
    source = read_js("result_store.js")
    for name in REQUIRED_API:
        assert f"{name}: {name}," in source, name


def test_last_result_and_history_use_separate_keys() -> None:
    source = read_js("result_store.js")
    assert 'const LAST_KEY = "bte_last_result";' in source
    assert 'const HISTORY_KEY = "bte_history";' in source
    assert 'const VIEW_KEY = "bte_view_result";' in source


def test_layout_loads_store_before_api() -> None:
    layout = (PORTAL_ROOT / "templates" / "_layout.html").read_text(encoding="utf-8")
    assert "/static/js/result_store.js" in layout
    assert layout.index("/static/js/result_store.js") < layout.index("/static/js/api.js")


@pytest.mark.parametrize("page", READ_ONLY_PAGES)
def test_pages_never_touch_web_storage(page: str) -> None:
    source = read_js(page)
    assert "sessionStorage" not in source, page
    assert "localStorage" not in source, page


@pytest.mark.parametrize("page", READ_ONLY_PAGES)
def test_pages_never_write_last_result(page: str) -> None:
    source = read_js(page)
    assert "saveLastResult" not in source, page
    assert "ResultStore.save(" not in source, page


def test_api_client_delegates_to_result_store() -> None:
    source = read_js("api.js")
    assert "bte_portal_last_result" not in source
    assert "bte_portal_history" not in source
    for wrapper in ("saveLastResult", "getLastResult", "getHistory"):
        assert wrapper in source, wrapper
    assert "resultStore().save(payload)" in source
    assert "resultStore().load()" in source
    assert "resultStore().loadHistory()" in source


def test_result_page_reads_view_selection() -> None:
    assert "ResultStore.loadForView()" in read_js("result.js")


def test_result_store_flow() -> None:
    """Analyze -> Result -> Dashboard -> History -> Reports -> Result."""
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is required to execute the ResultStore harness")
    completed = subprocess.run(
        [node, str(FLOW_HARNESS)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "FAILED 0" in completed.stdout
