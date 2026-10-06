"""Durable marriage profiles and customer document exports."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.api.http import build_marriage_router
from consulting.marriage.report.export import export_marriage_file
from consulting.marriage.repository.json_file import JsonMarriageRepository
from consulting.marriage.runtime.api_wiring import wire_marriage_api_runtime
from tests.consulting.api_fixtures import valid_body
from tests.consulting.runtime_fixtures import FakeCanonicalRunner


def _client(path: Path) -> tuple[TestClient, JsonMarriageRepository]:
    repository = JsonMarriageRepository(path)
    container = wire_marriage_api_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=FakeCanonicalRunner()),
        repository=repository,
    )
    app = FastAPI()
    app.include_router(build_marriage_router(container), prefix="/api/v1")
    return TestClient(app), repository


def test_json_repository_retains_complete_consultation_after_restart(tmp_path: Path) -> None:
    path = tmp_path / "marriage_consultations.json"
    client, _ = _client(path)
    created = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    consultation_id = created["consultation_id"]

    reloaded_client, reloaded = _client(path)
    assert reloaded.get(consultation_id) is not None
    assert reloaded.list_history()[0].display_label == "An / Binh"
    response = reloaded_client.get(f"/api/v1/consulting/marriage/{consultation_id}/report")
    assert response.status_code == 200
    assert response.json()["data"]["sections"]


def test_docx_endpoint_exports_the_stored_customer_report(tmp_path: Path) -> None:
    client, _ = _client(tmp_path / "records.json")
    created = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    response = client.get(
        f"/api/v1/consulting/marriage/{created['consultation_id']}/export/docx"
    )
    assert response.status_code == 200
    assert "vnd.openxmlformats-officedocument" in response.headers["content-type"]
    assert response.content[:2] == b"PK"
    with zipfile.ZipFile(io.BytesIO(response.content), "r") as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8")
    assert "TƯ VẤN HÔN NHÂN" in document_xml
    assert "An" in document_xml and "Binh" in document_xml


def test_pdf_export_uses_the_same_stored_report(tmp_path: Path) -> None:
    client, repository = _client(tmp_path / "records.json")
    created = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    stored = repository.get(created["consultation_id"])
    assert stored is not None

    class FakePdfBackend:
        def html_to_pdf(self, content: str, output_path: Path, *, title: str) -> int:
            assert "BẢN LUẬN GIẢI TƯ VẤN HÔN NHÂN" in content
            assert "An" in title and "Binh" in title
            output_path.write_bytes(b"%PDF-1.4\n" + content.encode("utf-8") + b"0" * 2048)
            return 1

    artifact = export_marriage_file(
        stored,
        "pdf",
        output_root=tmp_path / "export",
        pdf_backend=FakePdfBackend(),
    )
    assert artifact.path.read_bytes().startswith(b"%PDF")
    assert artifact.filename.endswith(".pdf")
