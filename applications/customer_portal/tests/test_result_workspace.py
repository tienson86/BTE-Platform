"""BZ-UI-03 Result Workspace — mount shell for canonical current-result binding."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app


def test_result_workspace_renders_layout_shell() -> None:
    """Workspace route serves the React mount + ResultStore current-result scripts."""
    client = TestClient(create_app())
    response = client.get("/result-workspace")
    assert response.status_code == 200
    body = response.text
    assert 'data-workspace-mount="bazi-result-v2"' in body
    assert 'data-grid="10"' in body
    assert 'id="result-workspace-root"' in body
    assert "/static/js/result_store.js" in body
    assert "/static/dist/workspace.js" in body
    assert "/static/css/result_workspace.css" in body
    assert "4 lượng 8 chỉ" not in body
    assert "78 / 100" not in body
    assert "Bính Ngọ" not in body
    assert "/backend/" not in body
    assert "year_ganzhi" not in body
    assert "previewFixture" not in body


def test_result_workspace_preview_query_is_client_side_only() -> None:
    """Normal HTML does not embed fixture; preview remains a query flag."""
    client = TestClient(create_app())
    response = client.get("/result-workspace?preview=1")
    assert response.status_code == 200
    body = response.text
    assert "4 lượng 8 chỉ" not in body
    assert "Kiến Lộc dụng Thực" not in body
    assert "/static/dist/workspace.js" in body
