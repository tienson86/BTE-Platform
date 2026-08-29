"""UI-01A Customer Portal navigation consistency (A1–A8)."""

from __future__ import annotations

import re
from pathlib import Path

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.config import PORTAL_ROOT
from applications.customer_portal.i18n import load_catalog, t
from applications.customer_portal.pages import CUSTOMER_NAV_ITEMS

_FORBIDDEN_NAV_LABELS = ("Kết quả", "Báo cáo", "Lịch sử")
_PRODUCT_LABELS = ("Trang chủ", "Chọn ngày tốt", "Xem lá số")


def _client() -> TestClient:
    return TestClient(create_app())


def _primary_nav(html: str) -> str:
    match = re.search(
        r'<nav[^>]*data-customer-nav="primary"[^>]*>(.*?)</nav>',
        html,
        flags=re.S,
    )
    assert match is not None, "customer primary navigation is missing"
    return match.group(1)


def _nav_labels(nav_html: str) -> list[str]:
    return re.findall(r">([^<]+)</a>", nav_html)


def _main_html(html: str) -> str:
    match = re.search(r'<main[^>]*id="mainContent"[^>]*>(.*?)</main>', html, flags=re.S)
    return match.group(1) if match else html


def test_a1_result_primary_nav_has_three_product_items() -> None:
    nav = _primary_nav(_client().get("/result").text)
    assert _nav_labels(nav) == list(_PRODUCT_LABELS)


def test_a2_result_primary_nav_hides_legacy_items() -> None:
    nav = _primary_nav(_client().get("/result").text)
    for label in _FORBIDDEN_NAV_LABELS:
        assert label not in nav


def test_a3_analyze_screen_title_is_xem_la_so() -> None:
    catalog = load_catalog()
    assert t(catalog, "analyze.title") == "Xem lá số"
    html = _client().get("/analyze").text
    main = _main_html(html)
    assert re.search(r"<h1[^>]*>Xem lá số</h1>", main)
    assert t(catalog, "nav.view_chart") == "Xem lá số"


def test_a4_analyze_primary_cta_is_phan_tich_la_so() -> None:
    catalog = load_catalog()
    assert t(catalog, "analyze.run") == "Phân tích lá số"
    html = _client().get("/analyze").text
    main = _main_html(html)
    assert 'id="btnAnalyze"' in main
    assert re.search(r'id="btnAnalyze"[^>]*>Phân tích lá số<', main)


def test_a5_analyze_success_still_opens_result() -> None:
    analyze_js = (PORTAL_ROOT / "static" / "js" / "analyze.js").read_text(encoding="utf-8")
    assert 'window.location.assign("/result")' in analyze_js
    html = _client().get("/analyze").text
    assert 'id="analyzeForm"' in html
    result = _client().get("/result")
    assert result.status_code == 200
    assert 'data-mount="PortalPage"' in result.text
    assert "/static/js/result_store.js" in result.text


def test_a6_result_routing_host_is_unchanged() -> None:
    html = _client().get("/result").text
    assert 'data-result-ui="canonical-desktop-v2"' in html
    assert 'id="canonical-desktop-root"' in html
    assert "/static/dist/result.js" in html
    assert "/static/js/result_store.js" in html
    interpretation = _client().get("/interpretation")
    assert interpretation.status_code == 200
    assert 'data-mount="PortalPage"' in interpretation.text


def test_a7_good_date_and_choose_date_nav_unchanged() -> None:
    client = _client()
    for path in ("/good-date", "/choose-date"):
        labels = _nav_labels(_primary_nav(client.get(path).text))
        assert labels == list(_PRODUCT_LABELS)
        for label in _FORBIDDEN_NAV_LABELS:
            assert label not in _primary_nav(client.get(path).text)
    home = client.get("/good-date")
    assert 'data-screen="lookup"' in home.text
    choose = client.get("/choose-date")
    assert 'data-screen="search"' in choose.text


def test_a8_single_customer_header_source() -> None:
    templates = PORTAL_ROOT / "templates"
    layout = (templates / "_layout.html").read_text(encoding="utf-8")
    result = (templates / "result_desktop.html").read_text(encoding="utf-8")
    util = Path(PORTAL_ROOT / "templates_util.py").read_text(encoding="utf-8")
    portal_page = (
        PORTAL_ROOT / "src" / "screens" / "canonical_desktop" / "PortalPage.tsx"
    ).read_text(encoding="utf-8")
    chrome = (
        PORTAL_ROOT / "src" / "screens" / "canonical_desktop" / "shell" / "PortalChrome.tsx"
    ).read_text(encoding="utf-8")
    nav_items = (PORTAL_ROOT / "src" / "layouts" / "Navigation" / "navItems.ts").read_text(
        encoding="utf-8"
    )

    assert "{{HEADER}}" in layout
    assert "{{HEADER}}" in result
    assert layout.count("{{HEADER}}") == 1
    assert result.count("{{HEADER}}") == 1
    assert "def _customer_header_html" in util
    assert util.count("def _customer_header_html") == 1
    assert "<PortalHeader" not in portal_page
    assert "cd-header__nav" not in chrome
    assert 'label: "Xem lá số"' in nav_items
    assert [item.path for item in CUSTOMER_NAV_ITEMS] == [
        "/good-date",
        "/choose-date",
        "/analyze",
    ]
    assert [item.key for item in CUSTOMER_NAV_ITEMS] == ["home", "choose-date", "analyze"]
