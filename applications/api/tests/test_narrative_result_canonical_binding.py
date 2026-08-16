"""Canonical NarrativeResult binding — API, adapter, Portal payload, Huỳnh trace."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.adapters.report_adapter import ReportAdapter
from applications.api.app import create_app
from applications.api.contracts.analyze_request import AnalyzeRequest, ChartInput
from applications.api.contracts.report_response import ReportResponse
from applications.api.services.orchestrator import OrchestratorService
from engines.narrative_engine.engine import NarrativeEngine
from engines.report_engine.commercial.builder import CommercialReportBuilder
from engines.report_engine.commercial.models import CommercialBuildRequest
from engines.report_engine.engine import ReportEngine
from engines.report_engine.narrative_binding import (
    CANONICAL_SECTION_IDS,
    NARRATIVE_SOURCE,
)

HUYNH = {
    "year": 1966,
    "month": 9,
    "day": 24,
    "hour": 4,
    "minute": 15,
    "gender": "male",
}

ANALYZE_BODY = {
    "request_id": "narrative-binding-001",
    "api_version": "1.0.0",
    "language": "vi",
    "chart": {
        "year": 1990,
        "month": 5,
        "day": 15,
        "hour": 10,
        "minute": 30,
        "gender": "male",
        "timezone": "Asia/Ho_Chi_Minh",
    },
    "report_template": "standard",
    "options": {},
}


def test_a_narrative_created_before_report_single_compose(monkeypatch) -> None:
    """A + single-generation: Narrative Composer V2 runs once before report consume."""
    v2_calls = {"count": 0}
    pack05_calls = {"count": 0}
    from applications.api.services import narrative_result_truth as truth

    original_v2 = truth.compose_narrative_v2_from_production
    original_pack05 = NarrativeEngine.compose_narrative_result

    def _counted_v2(output):
        v2_calls["count"] += 1
        return original_v2(output)

    def _counted_pack05(self, *args, **kwargs):
        pack05_calls["count"] += 1
        return original_pack05(self, *args, **kwargs)

    monkeypatch.setattr(truth, "compose_narrative_v2_from_production", _counted_v2)
    monkeypatch.setattr(NarrativeEngine, "compose_narrative_result", _counted_pack05)
    payload = OrchestratorService().analyze(
        year=1990,
        month=5,
        day=15,
        hour=10,
        minute=30,
        gender="male",
    )
    assert v2_calls["count"] == 1
    assert pack05_calls["count"] == 0
    assert payload["narrative_result"]["contract"] == "pack05_narrative_result_v1"
    assert payload["narrative_result"].get("generator") == "narrative_composer_v2"
    report = ReportEngine().render_from_analysis(
        type("Analysis", (), {"interpretation": object(), "narrative_result": None})(),
        narrative_result=payload["narrative_result"],
    )
    assert report.source == NARRATIVE_SOURCE
    assert report.to_portal_report_dict()["section_count"] == 7


def test_c_post_analysis_preserves_narrative_result() -> None:
    """C. POST /analysis preserves narrative_result."""
    client = TestClient(create_app())
    response = client.post("/analysis", json=ANALYZE_BODY)
    assert response.status_code == 200
    body = response.json()
    ReportResponse.model_validate(body)
    narrative = body.get("narrative_result")
    assert isinstance(narrative, dict)
    assert narrative.get("contract") == "pack05_narrative_result_v1"
    assert len(narrative.get("sections") or []) == 7
    assert "interpretation" in body
    assert body["interpretation"]["sections"] is not None


def test_d_report_adapter_does_not_drop_narrative_result() -> None:
    """D. ReportAdapter does not drop narrative_result."""
    request = AnalyzeRequest(
        request_id="adapter-nr-001",
        api_version="1.0.0",
        language="vi",
        report_template="standard",
        chart=ChartInput(
            year=1990,
            month=5,
            day=15,
            hour=10,
            minute=30,
            gender="male",
            timezone="Asia/Ho_Chi_Minh",
        ),
    )
    adapted = ReportAdapter().execute(request)
    assert adapted.narrative_result is not None
    assert adapted.narrative_result.get("contract") == "pack05_narrative_result_v1"
    assert isinstance(adapted.narrative_result.get("sections"), list)
    assert len(adapted.narrative_result["sections"]) == 7
    assert adapted.report.blocks


def test_g_portal_payload_prefers_narrative_result() -> None:
    """G. Portal live payload carries narrative_result; interpretation stays separate."""
    payload = OrchestratorService().analyze(
        year=1990,
        month=5,
        day=15,
        hour=10,
        minute=30,
        gender="male",
    )
    narrative = payload["narrative_result"]
    interpretation = payload["interpretation"]
    report = payload["report"]
    assert narrative.get("contract") == "pack05_narrative_result_v1"
    assert len(narrative["sections"]) == 7
    assert interpretation.get("section_count", 0) >= 1
    assert report["section_count"] == 7
    first_title = narrative["sections"][0]["title"]
    assert first_title in report["markdown"]


def test_h_interpretation_result_remains_available() -> None:
    """H. InterpretationResult remains available separately."""
    payload = OrchestratorService().analyze(
        year=1990,
        month=5,
        day=15,
        hour=10,
        minute=30,
        gender="male",
    )
    assert "interpretation" in payload
    assert "narrative_result" in payload
    assert payload["interpretation"] is not payload["narrative_result"]
    assert payload["interpretation"].get("sections")
    assert payload["narrative_result"].get("contract") == "pack05_narrative_result_v1"


def test_luong_ngoc_huynh_binding_identity() -> None:
    """Lương Ngọc Huỳnh: same NarrativeResult for Portal, report, and PDF spine."""
    payload = OrchestratorService().analyze(**HUYNH)
    narrative = payload["narrative_result"]
    assert len(narrative["sections"]) == 7
    ids = [section["id"] for section in narrative["sections"]]
    assert ids == list(CANONICAL_SECTION_IDS)
    report_result = ReportEngine().render_from_analysis(
        type("Analysis", (), {"interpretation": object(), "narrative_result": None})(),
        narrative_result=narrative,
    )
    assert report_result.source == NARRATIVE_SOURCE
    commercial = CommercialReportBuilder().build(
        CommercialBuildRequest(
            client_name="Lương Ngọc Huỳnh",
            birth_place="Hà Nội",
            gender="male",
            narrative_result=narrative,
        )
    )
    pdf_ids = [section.section_id for section in commercial.chapters[0].sections]
    assert pdf_ids == list(CANONICAL_SECTION_IDS)
    assert commercial.canonical_narrative is narrative or (
        commercial.canonical_narrative["sections"] == narrative["sections"]
    )
    portal_titles = [section["title"] for section in narrative["sections"]]
    pdf_titles = [section.title for section in commercial.chapters[0].sections]
    assert portal_titles == pdf_titles
    for section in commercial.chapters[0].sections:
        assert section.paragraphs
