"""DS-08 visual freeze — presentation copy and CSS only."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app as create_portal_app

REPO = Path(__file__).resolve().parents[2]
JS = REPO / "applications" / "customer_portal" / "static" / "js" / "date_selection.js"
CSS = REPO / "applications" / "customer_portal" / "static" / "css" / "date_selection.css"
I18N = REPO / "applications" / "customer_portal" / "static" / "i18n" / "vi.json"
TSX = (
    REPO
    / "applications"
    / "customer_portal"
    / "src"
    / "features"
    / "date_selection"
    / "components.tsx"
)
RANKING = REPO / "engines" / "date_selection" / "ranking.py"
MODELS = REPO / "engines" / "date_selection" / "models.py"


def test_positive_time_heading_is_user_facing() -> None:
    js = JS.read_text(encoding="utf-8")
    tsx = TSX.read_text(encoding="utf-8")
    i18n = I18N.read_text(encoding="utf-8")
    assert "Các thời điểm đẹp" in js
    assert "Các thời điểm đẹp" in tsx
    assert "Các thời điểm đẹp" in i18n
    assert '"positive_ke": "Các thời điểm đẹp"' in i18n


def test_choose_date_heading_no_longer_says_khac() -> None:
    tsx = TSX.read_text(encoding="utf-8")
    assert "<h3>Các khắc tốt</h3>" not in tsx
    portal = TestClient(create_portal_app())
    page = portal.get("/choose-date")
    assert page.status_code == 200
    assert "Kết quả giờ" not in page.text


def test_visual_polish_css_present() -> None:
    css = CSS.read_text(encoding="utf-8")
    assert "align-items: end" in css
    assert "min-height: 2.5rem" in css
    assert ".ds-cards .ds-result:hover" in css
    assert "border: 0" in css
    assert "white-space: nowrap" in css
    assert "prefers-reduced-motion" in css


def test_cung_combined_presentation_unchanged() -> None:
    js = JS.read_text(encoding="utf-8")
    tsx = TSX.read_text(encoding="utf-8")
    assert "cungWithElement" in js
    assert "hourRowLabel" in tsx
    assert "Cấn (Thổ)" not in RANKING.read_text(encoding="utf-8")


def test_engines_untouched_by_visual_sprint() -> None:
    ranking = RANKING.read_text(encoding="utf-8")
    models = MODELS.read_text(encoding="utf-8")
    assert "Các thời điểm đẹp" not in ranking
    assert "ds-badge" not in models
    portal = TestClient(create_portal_app())
    assert portal.get("/good-date").status_code == 200
    assert portal.get("/choose-date").status_code == 200
