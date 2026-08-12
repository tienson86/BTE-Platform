"""Tests for ReportInputV1Adapter."""

from __future__ import annotations

from applications.api.models.analysis_result import (
    AnalysisResult,
    InterpretationSectionView,
    InterpretationView,
    PillarView,
)
from engines.report_engine.adapters.report_input_v1_adapter import (
    ReportInputV1Adapter,
    ReportInputV1Source,
)
from engines.report_engine.contracts.report_input_v1 import ReportProfileV1


def _minimal_analysis() -> AnalysisResult:
    pillar = PillarView(stem="Canh", branch="Ngọ", hidden_stems=["Đinh", "Kỷ"])
    from applications.api.models.analysis_result import BaziView

    return AnalysisResult(
        bazi=BaziView(
            year_pillar=pillar,
            month_pillar=pillar,
            day_pillar=pillar,
            hour_pillar=pillar,
            day_master="Canh",
            day_master_element="Kim",
            day_master_yin_yang="Dương",
            ten_gods=["Thực Thần"],
            hidden_stems=["Đinh"],
            shensha=["Đào Hoa"],
        )
    )


def test_adapter_maps_profile_and_pillars() -> None:
    """Adapter maps profile metadata and four pillars."""
    source = ReportInputV1Source(
        analysis=_minimal_analysis(),
        profile=ReportProfileV1(
            full_name="Nguyễn Tiến Sơn",
            gender="male",
            birth_date="1987-01-21",
            birth_time="04:30",
            birth_place="Hà Tây, Việt Nam",
        ),
        case_id="CASE-0001",
    )
    report_input = ReportInputV1Adapter().build(source)
    assert report_input.profile.full_name == "Nguyễn Tiến Sơn"
    assert report_input.pillars.day.stem == "Canh"
    assert report_input.metadata.case_id == "CASE-0001"


def test_adapter_maps_interpretation_from_analysis_view() -> None:
    """Adapter falls back to AnalysisResult.interpretation view."""
    analysis = _minimal_analysis()
    analysis.interpretation = InterpretationView(
        sections=[
            InterpretationSectionView(
                id="career",
                title="Sự nghiệp",
                body="Phù hợp quản lý.",
            )
        ],
        confidence=0.7,
        summary="Tóm tắt.",
    )
    report_input = ReportInputV1Adapter().build(
        ReportInputV1Source(analysis=analysis, case_id="CASE-X")
    )
    assert report_input.interpretation.executive_summary == "Tóm tắt."
    assert report_input.interpretation.sections[0].id == "career"
    assert "AnalysisResult.interpretation.InterpretationView" in report_input.diagnostics.source_contracts


def test_adapter_records_missing_fields() -> None:
    """Missing optional runtime slices are recorded in diagnostics."""
    report_input = ReportInputV1Adapter().build(
        ReportInputV1Source(analysis=_minimal_analysis())
    )
    assert "calendar" in report_input.diagnostics.missing_fields
    assert "luck_cycles" in report_input.diagnostics.missing_fields


def test_adapter_maps_shensha_list() -> None:
    """Shen sha names map to structured list entries."""
    report_input = ReportInputV1Adapter().build(
        ReportInputV1Source(analysis=_minimal_analysis())
    )
    assert len(report_input.shensha) == 1
    assert report_input.shensha[0].name == "Đào Hoa"
