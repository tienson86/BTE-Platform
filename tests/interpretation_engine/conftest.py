"""Fixtures for Interpretation Engine tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.interpretation_engine import (
    InterpretationContext,
    InterpretationEngine,
    create_default_knowledge_session,
)
from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    AnalysisResult,
    ExecutionMetadata,
    ExecutionTrace,
    PerformanceMetrics,
    StageResult,
)
from engines.analysis_engine.runtime.constants import CANONICAL_STAGES


def make_stage(stage_id: str, payload: dict | None = None) -> StageResult:
    """Build a successful StageResult for tests."""
    defaults: dict[str, dict] = {
        "strength": {"classification": "strong", "score": 0.82},
        "temperature": {"classification": "balanced"},
        "pattern": {"pattern_id": "zheng_guan_ge", "name": "Zheng Guan Ge"},
        "useful_god": {
            "useful_gods": ["zheng_guan", "shi_shen"],
            "favorable": ["zheng_guan"],
            "unfavorable": ["shang_guan"],
        },
        "ten_gods": {"presence": [{"god_id": "zheng_guan"}]},
        "combination": {"clashes": []},
        "shensha": {
            "presence": [{"shensha_id": "tianyi_guiren"}],
            "auspicious": [],
        },
        "luck": {
            "summary": {"active_count": 4, "current_da_yun_index": 2},
        },
        "summary": {
            "stage_ids": list(CANONICAL_STAGES),
            "upstream_stage_count": 8,
        },
    }
    return StageResult(
        stage_id=stage_id,
        status="success",
        payload=payload if payload is not None else dict(defaults[stage_id]),
    )


def publish_all_stages(context: AnalysisContext) -> None:
    """Publish all canonical analytical stage results."""
    for stage_id in CANONICAL_STAGES:
        context.publish_stage_result(make_stage(stage_id))


def build_analysis_result(request_id: str = "interp-req-001") -> AnalysisResult:
    """Assemble a complete AnalysisResult for interpretation tests."""
    ctx = AnalysisContext(
        request_id=request_id,
        chart={"day_master": "Giáp"},
    )
    publish_all_stages(ctx)
    return AnalysisResult.from_context(
        ctx,
        execution_metadata=ExecutionMetadata(
            request_id=request_id,
            status="success",
        ),
        performance_metrics=PerformanceMetrics(),
        execution_trace=ExecutionTrace(request_id=request_id),
    )


@pytest.fixture
def knowledge_session():
    return create_default_knowledge_session()


@pytest.fixture
def analysis_result() -> AnalysisResult:
    return build_analysis_result()


@pytest.fixture
def context(analysis_result, knowledge_session) -> InterpretationContext:
    return InterpretationContext(
        analysis_result=analysis_result,
        chart={"day_master": "Giáp"},
        knowledge_session=knowledge_session,
        knowledge_version="1.0.0",
        metadata={"source": "interpretation-test"},
    )


@pytest.fixture
def engine() -> InterpretationEngine:
    return InterpretationEngine()
