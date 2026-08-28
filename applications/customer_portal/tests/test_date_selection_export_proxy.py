"""Portal /backend proxy: canonical SearchResult JSON → real PDF/DOCX."""

from __future__ import annotations

import json
from urllib.parse import urlparse

import httpx
from fastapi.testclient import TestClient

from applications.api.app import create_app as create_api_app
from applications.customer_portal.app import create_app as create_portal_app

_SEARCH = {
    "full_name": "Nguyễn Tiến Sơn",
    "gender": "male",
    "birth_year": 1987,
    "birth_month": 1,
    "birth_day": 21,
    "target_year": 2026,
    "target_month": 9,
}


def _forwarding_client(api: TestClient):
    class Upstream:
        def __init__(self, response: object) -> None:
            self.status_code = response.status_code
            self.content = response.content
            self.headers = response.headers

    class FakeClient:
        def __init__(self, *args, **kwargs) -> None:
            del args, kwargs

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def request(self, method, url, headers=None, content=None):
            path = urlparse(url).path
            body = json.loads(content) if content else None
            response = api.request(method, path, json=body, headers=headers)
            return Upstream(response)

    return FakeClient


def test_portal_proxy_search_then_pdf_and_docx(monkeypatch) -> None:
    api = TestClient(create_api_app())
    search = api.post("/api/v1/date-selection/search", json=_SEARCH)
    assert search.status_code == 200
    payload = search.json()["data"]
    assert payload["dates"]
    assert payload["person"]["full_name"] == "Nguyễn Tiến Sơn"
    monkeypatch.setattr(httpx, "AsyncClient", _forwarding_client(api))
    portal = TestClient(create_portal_app())
    pdf = portal.post(
        "/backend/api/v1/date-selection/report/pdf",
        json={"search_result": payload},
    )
    assert pdf.status_code == 200
    assert pdf.headers["content-type"].startswith("application/pdf")
    assert "bao-cao-chon-ngay-tot_nguyen-tien-son_09-2026.pdf" in pdf.headers.get(
        "content-disposition", ""
    )
    assert pdf.content[:5] == b"%PDF-"
    assert payload["dates"][0]["day"]["calendar"]["solar_label"]
    docx = portal.post(
        "/backend/api/v1/date-selection/report/docx",
        json={"search_result": payload},
    )
    assert docx.status_code == 200
    assert "vnd.openxmlformats-officedocument" in docx.headers["content-type"]
    assert "bao-cao-chon-ngay-tot_nguyen-tien-son_09-2026.docx" in docx.headers.get(
        "content-disposition", ""
    )
    assert docx.content[:2] == b"PK"
    assert len(pdf.content) > 1000
    assert len(docx.content) > 1000
