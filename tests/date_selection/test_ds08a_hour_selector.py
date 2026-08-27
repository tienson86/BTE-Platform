"""DS-08A hour selector labels — presentation only."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app as create_portal_app
from engines.date_selection.hour import window_for_branch

REPO = Path(__file__).resolve().parents[2]
JS = REPO / "applications" / "customer_portal" / "static" / "js" / "date_selection.js"
TSX = (
    REPO
    / "applications"
    / "customer_portal"
    / "src"
    / "features"
    / "date_selection"
    / "components.tsx"
)
TYPES = (
    REPO
    / "applications"
    / "customer_portal"
    / "src"
    / "features"
    / "date_selection"
    / "types.ts"
)
HOUR_PY = REPO / "engines" / "date_selection" / "hour.py"

EXPECTED = [
    ("Tý", "23:01–01:00"),
    ("Sửu", "01:01–03:00"),
    ("Dần", "03:01–05:00"),
    ("Mão", "05:01–07:00"),
    ("Thìn", "07:01–09:00"),
    ("Tỵ", "09:01–11:00"),
    ("Ngọ", "11:01–13:00"),
    ("Mùi", "13:01–15:00"),
    ("Thân", "15:01–17:00"),
    ("Dậu", "17:01–19:00"),
    ("Tuất", "19:01–21:00"),
    ("Hợi", "21:01–23:00"),
]


def test_dropdown_labels_cover_all_twelve_hours() -> None:
    js = JS.read_text(encoding="utf-8")
    types = TYPES.read_text(encoding="utf-8")
    tsx = TSX.read_text(encoding="utf-8")
    assert "hourOptionLabel" in js
    assert "hourOptionLabel" in tsx
    for branch, span in EXPECTED:
        label = f"Giờ {branch} ({span})"
        assert label in types or f"{branch}: \"{span}\"" in types
        assert "Giờ " in js
    assert 'option.value = branch' in js
    assert "option.textContent = hourOptionLabel(branch)" in js


def test_labels_match_canonical_hour_windows() -> None:
    for branch, span in EXPECTED:
        assert window_for_branch(branch).time_range == span


def test_hour_arithmetic_file_unchanged_by_selector() -> None:
    source = HOUR_PY.read_text(encoding="utf-8")
    assert "Giờ Tý" not in source
    portal = TestClient(create_portal_app())
    page = portal.get("/good-date")
    assert page.status_code == 200
    assert "dsHourSelect" in page.text
