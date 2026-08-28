"""BZ-UI-01 Result Workspace V2 — page shell (no data binding)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app


def test_result_workspace_renders_layout_shell() -> None:
    """Workspace route serves chrome + ten panel slots without engine payload."""
    client = TestClient(create_app())
    response = client.get("/result-workspace")
    assert response.status_code == 200
    body = response.text
    assert 'data-workspace="bazi-result-v2"' in body
    assert 'data-binding="none"' in body
    assert 'data-grid="10"' in body
    assert 'data-panel="tu-tru"' in body
    assert 'data-span="6"' in body
    assert 'data-span="4"' in body
    assert "Tứ Trụ" in body
    assert "Kết Luận &amp; Hành Động" in body or "Kết Luận & Hành Động" in body
    assert "78 / 100" not in body
    assert "4 lượng 8 chỉ" not in body
    assert "/backend/" not in body
    assert "year_ganzhi" not in body
    assert "ResultStore" not in body
