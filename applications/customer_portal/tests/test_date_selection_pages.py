"""Date Selection portal page tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app


def test_date_selection_pages_render() -> None:
    client = TestClient(create_app())
    good = client.get("/good-date")
    choose = client.get("/choose-date")
    assert good.status_code == 200
    assert choose.status_code == 200
    assert "Ngày tốt" in good.text
    assert "Xem ngày tốt/xấu" in good.text
    assert "Chọn ngày tốt" in good.text
    assert "Tiểu Lục Nhâm" not in good.text
    assert "Tiểu Lục Nhâm" not in choose.text
    assert "ds-clock" in good.text
    assert "ds-left" in good.text
    assert "ds-right" in good.text
    assert good.text.find("ds-calendar-card") < good.text.find("ds-clock-card")
    assert "dsFullName" in choose.text
    assert 'id="dsExportPdf"' in choose.text
    assert "Xuất DOCX" in choose.text
    assert choose.text.find('id="dsResults"') < choose.text.find('id="dsExport"')
    assert 'id="dsExport"' in choose.text
    assert "hidden" in choose.text.split('id="dsExport"', 1)[1].split(">", 1)[0]
    assert 'id="dsExportPdf"' not in good.text
    nav_start = choose.text.find("nav-dropdown")
    nav_chunk = choose.text[nav_start : choose.text.find('class="ds-page"')]
    assert 'id="dsExportPdf"' not in nav_chunk
    assert "dsGender" in choose.text
    assert 'type="radio"' in choose.text
    assert 'select id="dsGender"' not in choose.text
    assert "dsBirth" in choose.text
    assert "DD/MM/YYYY" in choose.text
    assert 'type="date"' not in choose.text
    assert "Tháng cần tìm ngày tốt" in choose.text
    assert 'type="month"' not in choose.text


def test_existing_routes_still_work() -> None:
    client = TestClient(create_app())
    for path in ("/dashboard", "/analyze", "/reports", "/history", "/profile"):
        response = client.get(path)
        assert response.status_code == 200, path
    result = client.get("/result")
    assert result.status_code == 200
    interpretation = client.get("/interpretation")
    assert interpretation.status_code == 200
