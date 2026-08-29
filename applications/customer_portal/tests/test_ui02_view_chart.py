"""UI-02 Screen 01 — View Chart / Xem lá số (V1–V12)."""

from __future__ import annotations

import re

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.config import PORTAL_ROOT
from applications.customer_portal.i18n import load_catalog, t

_PRODUCT_LABELS = ("Trang chủ", "Chọn ngày tốt", "Xem lá số")
_CANONICAL_FIELDS = ("full_name", "gender", "birth_date", "birth_time", "birth_place")
_ACCURACY_NOTE = (
    "Lưu ý: Giờ sinh và nơi sinh càng chính xác thì kết quả luận giải càng đáng tin cậy."
)


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


def test_v1_analyze_title_is_xem_la_so() -> None:
    catalog = load_catalog()
    assert t(catalog, "analyze.title") == "Xem lá số"
    main = _main_html(_client().get("/analyze").text)
    assert re.search(r"<h1[^>]*>Xem lá số</h1>", main)
    heading = re.search(r"<h1[^>]*>.*?</h1>", main, flags=re.S)
    assert heading is not None
    assert "Luận giải" not in heading.group(0)


def test_v2_visible_form_has_exactly_five_canonical_fields() -> None:
    main = _main_html(_client().get("/analyze").text)
    fields = re.findall(r'data-analyze-field="([^"]+)"', main)
    assert fields == list(_CANONICAL_FIELDS)
    assert "Họ và tên" in main
    assert "Giới tính" in main
    assert "Ngày sinh" in main
    assert "Giờ sinh" in main
    assert "Nơi sinh" in main


def test_v3_no_visible_timezone_field() -> None:
    main = _main_html(_client().get("/analyze").text)
    assert "Múi giờ" not in main
    assert 'id="timezone"' in main
    assert re.search(r'<input[^>]*type="hidden"[^>]*id="timezone"', main) or re.search(
        r'<input[^>]*id="timezone"[^>]*type="hidden"', main
    )
    assert 'id="calendar_type"' not in main


def test_v4_no_visible_lunar_date_field() -> None:
    main = _main_html(_client().get("/analyze").text)
    for label in ("Âm lịch", "Can Chi", "Tiết khí", "Cung Phi", "Mệnh Quái", "Nhóm Trạch"):
        assert label not in main


def test_v5_accuracy_note_is_visible() -> None:
    catalog = load_catalog()
    assert t(catalog, "analyze.accuracy_note") == _ACCURACY_NOTE
    main = _main_html(_client().get("/analyze").text)
    assert _ACCURACY_NOTE in main
    assert 'data-testid="analyze-accuracy-note"' in main


def test_v6_primary_cta_is_phan_tich_la_so() -> None:
    catalog = load_catalog()
    assert t(catalog, "analyze.run") == "Phân tích lá số"
    main = _main_html(_client().get("/analyze").text)
    assert re.search(r'id="btnAnalyze"[^>]*>Phân tích lá số<', main)
    assert main.lower().count("xuất pdf") == 0
    assert 'id="dsExportPdf"' not in main


def test_v7_required_validation_uses_customer_language() -> None:
    catalog = load_catalog()
    assert t(catalog, "analyze.gender_required") == "Vui lòng chọn giới tính."
    assert t(catalog, "analyze.date_required") == "Vui lòng chọn ngày sinh."
    js = (PORTAL_ROOT / "static" / "js" / "analyze.js").read_text(encoding="utf-8")
    assert "analyze.gender_required" in js
    assert "analyze.date_required" in js
    html = _client().get("/analyze").text
    assert "novalidate" in html
    assert 'value="male" checked' not in html
    assert 'id="birth_date"' in html


def test_v8_submit_still_uses_existing_analyze_api() -> None:
    js = (PORTAL_ROOT / "static" / "js" / "analyze.js").read_text(encoding="utf-8")
    assert 'BtePortal.post("/api/v1/analyze"' in js
    assert "saveLastResult" in js
    assert "ResultStore.load" in js


def test_v9_successful_analysis_still_routes_to_result() -> None:
    js = (PORTAL_ROOT / "static" / "js" / "analyze.js").read_text(encoding="utf-8")
    assert 'window.location.assign("/result")' in js
    response = _client().get("/result")
    assert response.status_code == 200
    assert 'data-mount="PortalPage"' in response.text


def test_v10_customer_nav_remains_three_items() -> None:
    nav = _primary_nav(_client().get("/analyze").text)
    assert _nav_labels(nav) == list(_PRODUCT_LABELS)
    for label in ("Kết quả", "Báo cáo", "Lịch sử", "Hướng dẫn"):
        assert label not in nav
    assert 'data-nav-id="analyze"' in nav
    assert 'aria-current="page"' in nav


def test_v11_duplicate_submit_is_blocked_while_processing() -> None:
    js = (PORTAL_ROOT / "static" / "js" / "analyze.js").read_text(encoding="utf-8")
    assert "if (analyzing) return;" in js
    assert "analyzing = true;" in js
    assert "btn.disabled = on;" in js


def test_v12_mobile_form_does_not_overflow() -> None:
    css = (PORTAL_ROOT / "static" / "css" / "pages.css").read_text(encoding="utf-8")
    assert ".analyze-page" in css
    assert "overflow-x: hidden" in css
    html = _client().get("/analyze").text
    assert "form-section-grid" not in html
    assert "analyze-fields" in html
    assert "max-width: 100%" in css
