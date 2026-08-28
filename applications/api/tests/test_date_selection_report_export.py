"""Date Selection report export API — displayed SearchResult only."""

from __future__ import annotations

import io
import zipfile

from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.services.date_selection_report_export import (
    MISSING_RESULT_MESSAGE,
    NO_RECOMMENDATIONS_MESSAGE,
)
from engines.date_selection.service import DateSelectionService


def test_report_routes_are_registered() -> None:
    client = TestClient(create_app())
    spec = client.get("/openapi.json").json()
    paths = spec["paths"]
    assert "/api/v1/date-selection/report/pdf" in paths
    assert "/api/v1/date-selection/report/docx" in paths
    assert "post" in paths["/api/v1/date-selection/report/pdf"]
    assert "post" in paths["/api/v1/date-selection/report/docx"]


_SEARCH = {
    "full_name": "Nguyễn Tiến Sơn",
    "gender": "male",
    "birth_year": 1987,
    "birth_month": 1,
    "birth_day": 21,
    "target_year": 2026,
    "target_month": 9,
}


def _search_payload(client: TestClient) -> dict:
    response = client.post("/api/v1/date-selection/search", json=_SEARCH)
    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["dates"]
    return payload


def test_docx_export_reuses_displayed_search_result(monkeypatch) -> None:
    client = TestClient(create_app())
    payload = _search_payload(client)

    def boom(*_args, **_kwargs):
        raise AssertionError("Date Selection must not rerun")

    monkeypatch.setattr(
        "applications.api.routes.date_selection._SERVICE.search",
        boom,
    )
    monkeypatch.setattr(DateSelectionService, "search", boom)
    response = client.post(
        "/api/v1/date-selection/report/docx",
        json={"search_result": payload},
    )
    assert response.status_code == 200
    assert "vnd.openxmlformats-officedocument" in response.headers["content-type"]
    disposition = response.headers.get("content-disposition", "")
    assert "bao-cao-chon-ngay-tot_" in disposition
    assert disposition.endswith(".docx") or ".docx" in disposition
    assert "Traceback" not in response.text
    data = response.content
    assert data[:2] == b"PK"
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        assert "word/document.xml" in archive.namelist()
    xml = zipfile.ZipFile(io.BytesIO(data)).read("word/document.xml").decode("utf-8")
    assert "Nguyễn Tiến Sơn" in xml
    assert payload["dates"][0]["day"]["calendar"]["solar_label"] in xml


def test_pdf_export_from_displayed_search_result(monkeypatch) -> None:
    client = TestClient(create_app())
    payload = _search_payload(client)
    monkeypatch.setattr(
        "applications.api.routes.date_selection._SERVICE.search",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("Date Selection must not rerun")
        ),
    )
    response = client.post(
        "/api/v1/date-selection/report/pdf",
        json={"search_result": payload},
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert response.content[:5] == b"%PDF-"
    assert "bao-cao-chon-ngay-tot_" in response.headers.get("content-disposition", "")


def test_export_rejects_empty_recommendations() -> None:
    client = TestClient(create_app())
    payload = _search_payload(client)
    payload["dates"] = []
    response = client.post(
        "/api/v1/date-selection/report/pdf",
        json={"search_result": payload},
    )
    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["message"] == NO_RECOMMENDATIONS_MESSAGE
    assert "Traceback" not in response.text
    assert "engines/" not in response.text
    assert "temp" not in body["message"].lower()


def test_export_rejects_missing_search_result() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/date-selection/report/docx",
        json={"search_result": {}},
    )
    assert response.status_code == 400
    body = response.json()
    assert body["message"] == MISSING_RESULT_MESSAGE
    assert body["code"] == "export_missing_search_result"
    assert "Traceback" not in response.text
