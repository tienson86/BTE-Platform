"""Fixtures for Report Generator tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.interpretation_engine.models import (
    BoundSentence,
    InterpretationParagraph,
    InterpretationResult,
    InterpretationSection,
)
from engines.analysis_engine.report_generator import (
    FormatProfile,
    ReportAssemblyContext,
    ReportGenerator,
)
from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    AnalysisResult,
    ConfidenceEvaluation,
    DiagnosticInfo,
    ExecutionMetadata,
    ExecutionTrace,
    PerformanceMetrics,
    RuleEvidence,
    StageResult,
)
from engines.analysis_engine.runtime.constants import CANONICAL_STAGES


def make_stage(stage_id: str, payload: dict | None = None) -> StageResult:
    """Build a successful StageResult for tests."""
    defaults: dict[str, dict] = {
        "strength": {"classification": "strong"},
        "temperature": {"classification": "balanced"},
        "pattern": {"pattern_id": "zheng_guan_ge"},
        "useful_god": {"useful_gods": ["zheng_guan"]},
        "ten_gods": {"presence": [{"god_id": "zheng_guan"}]},
        "combination": {"clashes": []},
        "shensha": {"presence": [{"shensha_id": "tianyi_guiren"}]},
        "luck": {"summary": {"active_count": 4, "current_da_yun_index": 2}},
        "summary": {"upstream_stage_count": 8},
    }
    return StageResult(
        stage_id=stage_id,
        status="success",
        payload=payload if payload is not None else dict(defaults[stage_id]),
    )


def build_analysis_result(request_id: str = "rpt-req-001") -> AnalysisResult:
    """Assemble a complete AnalysisResult."""
    ctx = AnalysisContext(request_id=request_id, chart={"day_master": "Giáp"})
    for stage_id in CANONICAL_STAGES:
        ctx.publish_stage_result(make_stage(stage_id))
    return AnalysisResult.from_context(
        ctx,
        execution_metadata=ExecutionMetadata(request_id=request_id, status="success"),
        performance_metrics=PerformanceMetrics(),
        execution_trace=ExecutionTrace(request_id=request_id),
    )


def _section(
    section_id: str,
    title: str,
    body: str,
    *,
    sentence_id: str | None = None,
) -> InterpretationSection:
    sid = sentence_id or f"{section_id}_s1"
    sentence = BoundSentence(
        sentence_id=sid,
        section_id=section_id,
        source_stage="summary" if section_id in {"overview", "recommendations"} else section_id,
        template_id=f"tpl_{section_id}",
        text=body,
        priority=80,
    )
    paragraph = InterpretationParagraph(
        section_id=section_id,
        sentences=(sentence,),
        text=body,
    )
    return InterpretationSection(
        section_id=section_id,
        title=title,
        paragraphs=(paragraph,),
        body=body,
        sentence_ids=(sid,),
        source_stages=(sentence.source_stage,),
    )


def build_interpretation_result(
    request_id: str = "rpt-req-001",
) -> InterpretationResult:
    """Build a deterministic InterpretationResult for report tests."""
    sections = (
        _section(
            "overview",
            "Tổng quan",
            "Bản luận giải cho Nhật Chủ Giáp được tổng hợp từ toàn bộ kết quả phân tích.",
        ),
        _section(
            "strength",
            "Vượng suy",
            "Nhật Chủ Giáp thuộc loại strong, lực lượng vững.",
        ),
        _section(
            "pattern",
            "Cách cục",
            "Cách cục chủ đạo là zheng_guan_ge.",
        ),
        _section(
            "luck",
            "Vận hạn",
            "Lớp vận hạn đang hoạt động: 4, Đại vận hiện tại index 2.",
        ),
    )
    return InterpretationResult(
        request_id=request_id,
        sections=sections,
        overview=sections[0].body,
        confidence=ConfidenceEvaluation(score=0.85, level="high"),
        evidence=(
            RuleEvidence(
                rule_id="overview_intro",
                category="overview",
                priority=100,
                reference="tpl_overview",
            ),
        ),
        diagnostics=(
            DiagnosticInfo(
                code="interpretation.assembled",
                message="ok",
                stage_id="interpretation",
            ),
        ),
        knowledge_version="1.0.0",
    )


@pytest.fixture
def analysis_result() -> AnalysisResult:
    return build_analysis_result()


@pytest.fixture
def interpretation_result() -> InterpretationResult:
    return build_interpretation_result()


@pytest.fixture
def format_profile() -> FormatProfile:
    return FormatProfile.full_publication(
        title="BTE Test Report",
        mandatory_sections=("overview",),
    )


@pytest.fixture
def assembly_context(
    interpretation_result: InterpretationResult,
    analysis_result: AnalysisResult,
    format_profile: FormatProfile,
) -> ReportAssemblyContext:
    return ReportAssemblyContext(
        interpretation_result=interpretation_result,
        analysis_result=analysis_result,
        format_profile=format_profile,
        request_id="rpt-req-001",
    )


@pytest.fixture
def generator() -> ReportGenerator:
    return ReportGenerator()
