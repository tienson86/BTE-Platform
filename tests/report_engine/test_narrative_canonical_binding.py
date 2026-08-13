"""Canonical NarrativeResult binding — Report Engine + Commercial PDF."""

from __future__ import annotations

from applications.api.models.analysis_result import (
    AnalysisResult,
    BaziView,
    InterpretationSectionView,
    InterpretationView,
    PillarView,
)
from engines.report_engine.commercial.builder import CommercialReportBuilder
from engines.report_engine.commercial.models import (
    CommercialBuildRequest,
    CommercialFeatureInput,
)
from engines.report_engine.engine import ReportEngine
from engines.report_engine.narrative_binding import (
    CANONICAL_SECTION_IDS,
    MISSING_NARRATIVE_DIAGNOSTIC,
    NARRATIVE_SOURCE,
    extract_canonical_sections,
)

_SECTION_SPECS = (
    ("sec-executive_summary", "overview", "Tóm tắt điều hành", "Executive text"),
    ("sec-observation", "observation", "Quan sát", "Observation text"),
    ("sec-reasoning", "reasoning", "Lý giải", "Reasoning text"),
    ("sec-impact", "impact", "Tác động", "Impact text"),
    ("sec-recommendation", "priority", "Khuyến nghị", "Recommendation text"),
    ("sec-warning", "warning", "Lưu ý", "Warning text"),
    ("sec-conclusion", "closing", "Kết luận", "Conclusion text"),
)


def _pack05_narrative() -> dict:
    """Deterministic Pack 05 NarrativeResult public representation."""
    return {
        "contract": "pack05_narrative_result_v1",
        "status": "complete",
        "summary": {"identity": "Nhật chủ Bính"},
        "recommendations": [{"id": "rec-1", "action": "Ưu tiên Thủy"}],
        "primary_recommendation": {"composed_text": "Ưu tiên Thủy"},
        "commercial_executive_summary": {"composed_text": "Executive text"},
        "sections": [
            {
                "id": section_id,
                "intent": intent,
                "title": title,
                "paragraphs": [{"id": f"{section_id}-p1", "text": body}],
            }
            for section_id, intent, title, body in _SECTION_SPECS
        ],
    }


def _analysis_with_legacy_interpretation() -> AnalysisResult:
    pillar = PillarView(stem="Bính", branch="Tuất")
    return AnalysisResult(
        bazi=BaziView(
            year_pillar=pillar,
            month_pillar=pillar,
            day_pillar=pillar,
            hour_pillar=pillar,
            day_master="Bính",
            day_master_element="Hỏa",
            day_master_yin_yang="yang",
        ),
        interpretation=InterpretationView(
            sections=[
                InterpretationSectionView(
                    id="legacy-1",
                    title="Tổng quan",
                    body="Áp dụng bảng trạng thái luận giải — legacy dump.",
                )
            ],
            section_count=1,
            sentence_count=1,
        ),
    )


def test_a_narrative_exists_before_report_consumes_it() -> None:
    """A. NarrativeResult is created before report generation."""
    analysis = _analysis_with_legacy_interpretation()
    narrative = _pack05_narrative()
    analysis.narrative_result = narrative
    result = ReportEngine().render_from_analysis(
        analysis,
        narrative_result=analysis.narrative_result,
    )
    assert analysis.narrative_result is narrative
    assert result.canonical_narrative is not None
    assert result.source == NARRATIVE_SOURCE


def test_b_report_generation_consumes_narrative_result() -> None:
    """B. Report generation consumes NarrativeResult."""
    analysis = _analysis_with_legacy_interpretation()
    narrative = _pack05_narrative()
    result = ReportEngine().render_from_analysis(
        analysis,
        include_narrative=True,
        narrative_result=narrative,
    )
    report = result.to_portal_report_dict()
    assert report["section_count"] == 7
    assert "Executive text" in report["markdown"]
    assert "Áp dụng bảng trạng thái" not in report["markdown"]
    assert result.canonical_narrative["sections"][0]["id"] == "sec-executive_summary"


def test_e_commercial_builder_receives_canonical_narrative() -> None:
    """E. CommercialReportBuilder receives canonical narrative."""
    narrative = _pack05_narrative()
    report = CommercialReportBuilder().build(
        CommercialBuildRequest(
            client_name="Test",
            identity=CommercialFeatureInput(
                feature_id="identity",
                title="Danh tính",
                status="AVAILABLE",
                body="Identity feature body",
                sections=[("id-core", "Tôi là ai", ["Identity feature body"])],
            ),
            career=CommercialFeatureInput(
                feature_id="career",
                title="Sự nghiệp",
                status="AVAILABLE",
                body="Career feature body",
                sections=[("ca-core", "Sự nghiệp", ["Career feature body"])],
            ),
            executive=CommercialFeatureInput(
                feature_id="executive",
                title="Tư vấn tổng hợp",
                status="AVAILABLE",
                body="Executive feature body",
                sections=[("ex-core", "Tổng hợp", ["Executive feature body"])],
            ),
            narrative_result=narrative,
        )
    )
    assert report.diagnostics["narrative_source"] == NARRATIVE_SOURCE
    assert report.canonical_narrative is not None
    assert report.canonical_narrative["contract"] == "pack05_narrative_result_v1"
    assert [chapter.chapter_id for chapter in report.chapters] == ["canonical_narrative"]
    assert {item.chapter_id for item in report.supporting_chapters} == {
        "identity",
        "career",
        "executive",
    }


def test_f_pdf_model_contains_seven_canonical_sections() -> None:
    """F. PDF model contains all seven canonical narrative sections."""
    report = CommercialReportBuilder().build(
        CommercialBuildRequest(
            client_name="Test",
            narrative_result=_pack05_narrative(),
        )
    )
    assert len(report.chapters) == 1
    section_ids = [section.section_id for section in report.chapters[0].sections]
    assert section_ids == list(CANONICAL_SECTION_IDS)
    texts = [section.paragraphs[0] for section in report.chapters[0].sections]
    assert texts == [spec[3] for spec in _SECTION_SPECS]


def test_i_legacy_interpretation_is_not_successful_fallback() -> None:
    """I. Legacy InterpretationView is not used as successful canonical fallback."""
    analysis = _analysis_with_legacy_interpretation()
    result = ReportEngine().render_from_analysis(analysis, include_narrative=True)
    report = result.to_portal_report_dict()
    assert result.source == MISSING_NARRATIVE_DIAGNOSTIC
    assert report["section_count"] == 0
    assert report["markdown"] == ""
    assert "Áp dụng bảng trạng thái" not in report["html"]
    assert analysis.interpretation is not None
    assert analysis.interpretation.sections[0].body.startswith("Áp dụng bảng trạng thái")


def test_extract_preserves_pack05_order() -> None:
    sections = extract_canonical_sections(_pack05_narrative())
    assert [item["id"] for item in sections] == list(CANONICAL_SECTION_IDS)
