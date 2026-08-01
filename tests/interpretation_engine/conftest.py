"""Fixtures for Interpretation Engine tests.

Preserves legacy analysis-interpretation fixtures and adds Pack 03
infrastructure fixtures (mock-only).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.analysis_engine.interpretation_engine import (
    InterpretationContext,
    InterpretationEngine,
    create_default_knowledge_session,
)
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.final_result import FinalResult
from engines.analysis_engine.runtime.constants import CANONICAL_STAGES
from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    AnalysisResult,
    ExecutionMetadata,
    ExecutionTrace,
    PerformanceMetrics,
    StageResult,
)
from engines.interpretation_engine.pipeline.execution_context import PipelineContext
from engines.interpretation_engine.registry.metadata import InterpreterRegistryEntry
from engines.interpretation_engine.sentence_engine.metadata import SentenceRef
from engines.interpretation_engine.template_engine.metadata import TemplateRef


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
    """Return a default knowledge session for legacy interpretation tests."""
    return create_default_knowledge_session()


@pytest.fixture
def analysis_result() -> AnalysisResult:
    """Return a complete analysis result stub for legacy tests."""
    return build_analysis_result()


@pytest.fixture
def context(analysis_result, knowledge_session) -> InterpretationContext:
    """Return a legacy interpretation context fixture."""
    return InterpretationContext(
        analysis_result=analysis_result,
        chart={"day_master": "Giáp"},
        knowledge_session=knowledge_session,
        knowledge_version="1.0.0",
        metadata={"source": "interpretation-test"},
    )


@pytest.fixture
def engine() -> InterpretationEngine:
    """Return a legacy InterpretationEngine instance."""
    return InterpretationEngine()


# ---------------------------------------------------------------------------
# Pack 03 infrastructure fixtures (mock-only)
# ---------------------------------------------------------------------------


@pytest.fixture
def interpretation_engine_root() -> Path:
    """Return the Interpretation Engine package root path."""
    return Path(__file__).resolve().parents[2] / "engines" / "interpretation_engine"


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the fixtures directory path."""
    return Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def final_result_stub() -> FinalResult:
    """Return a minimal valid Pack 02 FinalResult stub."""
    timestamps = ModelTimestamps(created_at="2026-01-01T00:00:00Z")
    metadata = AnalysisMetadata(
        id="meta_fr_stub",
        version="1.0.0",
        metadata={},
        trace=(),
        timestamps=timestamps,
    )
    return FinalResult(
        id="fr_stub_1",
        version="1.0.0",
        metadata=metadata,
        trace=("analysis",),
        timestamps=timestamps,
        pipeline_id="analysis_pipeline",
        success=True,
        summary_codes=("ok",),
    )


@pytest.fixture
def pipeline_context_stub() -> PipelineContext:
    """Return a shared interpretation pipeline context stub."""
    return PipelineContext(
        context_id="pipe_ctx_1",
        pipeline_id="interp_pipeline",
        source_final_result_id="fr_stub_1",
        attributes={"source": "test_stub"},
    )


@pytest.fixture
def sentence_ref_catalog() -> tuple[SentenceRef, ...]:
    """Return a mock sentence-ref catalog (no sentence library text)."""
    return (
        SentenceRef(
            ref_id="s_a",
            domain="personality",
            section="intro",
            status="active",
            priority=10,
            tags=("core", "vi"),
        ),
        SentenceRef(
            ref_id="s_b",
            domain="personality",
            section="intro",
            status="active",
            priority=5,
            tags=("alt",),
        ),
        SentenceRef(
            ref_id="s_c",
            domain="career",
            section="body",
            status="draft",
            priority=1,
            tags=("core",),
        ),
    )


@pytest.fixture
def template_ref_catalog() -> tuple[TemplateRef, ...]:
    """Return a mock template-ref catalog (no template bodies)."""
    return (
        TemplateRef(
            ref_id="tpl_a",
            domain="personality",
            status="active",
            slot_names=("subject", "tone"),
        ),
        TemplateRef(
            ref_id="tpl_b",
            domain="career",
            status="active",
            slot_names=("role",),
        ),
    )


@pytest.fixture
def interpreter_registry_entries() -> tuple[InterpreterRegistryEntry, ...]:
    """Return mock interpreter registry entries."""
    return (
        InterpreterRegistryEntry(
            entry_id="personality",
            interpreter_id="personality",
            name="Personality",
            version="1.0.0",
            status="active",
            domain="personality",
        ),
        InterpreterRegistryEntry(
            entry_id="summary",
            interpreter_id="summary",
            name="Summary",
            version="1.0.0",
            status="active",
            domain="summary",
            dependencies=("personality",),
        ),
    )
