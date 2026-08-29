"""UI-02R — customer-facing date/time display is DD/MM/YYYY and 24-hour HH:mm."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.config import PORTAL_ROOT

_ANALYZE = PORTAL_ROOT / "templates" / "analyze.html"
_JS = PORTAL_ROOT / "static" / "js" / "analyze.js"


def _client() -> TestClient:
    return TestClient(create_app())


def test_date_input_uses_ddmmyyyy_placeholder() -> None:
    html = _client().get("/analyze").text
    assert 'id="birth_date"' in html
    assert 'placeholder="DD/MM/YYYY"' in html
    assert 'type="date"' not in html


def test_time_input_uses_24h_placeholder() -> None:
    html = _client().get("/analyze").text
    assert 'id="birth_time"' in html
    assert 'placeholder="HH:mm"' in html
    assert 'type="time"' not in html
    assert "AM" not in html
    assert "PM" not in html


def test_submit_still_posts_year_month_day_hour_minute() -> None:
    js = _JS.read_text(encoding="utf-8")
    assert r"/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/" in js
    assert r"/^(\d{1,2}):(\d{2})$/" in js
    assert 'BtePortal.post("/api/v1/analyze"' in js
    assert "year: input.year" in js
    assert "month: input.month" in js
    assert "day: input.day" in js
    assert "hour: input.hour" in js
    assert "minute: input.minute" in js
    html = _ANALYZE.read_text(encoding="utf-8")
    assert 'placeholder="DD/MM/YYYY"' in html
    assert 'placeholder="HH:mm"' in html
