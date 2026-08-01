"""Architecture tests for interpretation context runtime."""

from __future__ import annotations

import json

import pytest

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context import (
    ContextBuilder,
    ContextFactory,
    ContextLifecyclePhase,
    ContextManager,
    ContextSerializer,
    InterpretationContext as LegacyInterpretationContext,
    PackInterpretationContext,
)
from engines.interpretation_engine.exceptions.context_error import InterpretationContextError


def _final_result(*, result_id: str = "fr_1") -> FinalResult:
    """Build a minimal valid Pack 02 FinalResult for tests."""
    timestamps = ModelTimestamps(created_at="2026-01-01T00:00:00Z")
    metadata = AnalysisMetadata(
        id=f"meta_{result_id}",
        version="1.0.0",
        metadata={},
        trace=(),
        timestamps=timestamps,
    )
    return FinalResult(
        id=result_id,
        version="1.0.0",
        metadata=metadata,
        trace=("analysis",),
        timestamps=timestamps,
        pipeline_id="analysis_pipeline",
        success=True,
        summary_codes=("ok",),
    )


def test_legacy_context_reexport() -> None:
    """Legacy InterpretationContext remains importable from context package."""
    ctx = LegacyInterpretationContext()
    assert ctx.bazi is not None


def test_builder_from_final_result() -> None:
    """Builder produces Pack 03 InterpretationContext from FinalResult only."""
    final = _final_result()
    context = (
        ContextBuilder()
        .with_final_result(final)
        .with_pipeline_id("interp_pipe")
        .build_context()
    )
    assert isinstance(context, PackInterpretationContext)
    assert context.source_final_result_id == "fr_1"
    assert context.final_result.id == "fr_1"
    assert context.validate() is True


def test_factory_create_from_final_result() -> None:
    """Factory create wraps Pack 02 FinalResult."""
    factory = ContextFactory()
    context = factory.create_from_final_result(_final_result(result_id="fr_2"))
    assert context.source_final_result_id == "fr_2"
    assert context.pipeline_id == "analysis_pipeline"


def test_manager_lifecycle() -> None:
    """Manager runs create → initialize → expand → validate → finalize → dispose."""
    manager = ContextManager()
    created = manager.create(final_result=_final_result(result_id="fr_3"))
    assert manager.phase == ContextLifecyclePhase.CREATED
    assert created.source_final_result_id == "fr_3"

    manager.initialize(init_attributes={"locale": "vi"})
    assert manager.phase == ContextLifecyclePhase.INITIALIZED

    manager.expand({"section": "personality"})
    assert manager.phase == ContextLifecyclePhase.EXPANDED

    assert manager.validate() is True
    assert manager.phase == ContextLifecyclePhase.VALIDATED

    finalized = manager.finalize()
    assert finalized.completed_at is not None
    assert manager.phase == ContextLifecyclePhase.FINALIZED

    snap = manager.snapshot(label="final")
    assert snap.phase == ContextLifecyclePhase.FINALIZED
    assert manager.history is not None
    assert manager.history.revision_count() >= 5

    manager.dispose()
    assert manager.phase == ContextLifecyclePhase.DISPOSED


def test_serializer_roundtrip() -> None:
    """Serializer round-trips Pack 03 InterpretationContext JSON."""
    context = ContextFactory().create(final_result=_final_result(result_id="fr_4"))
    serializer = ContextSerializer()
    payload = serializer.to_json(context)
    restored = serializer.from_json(payload)
    assert restored.id == context.id
    assert restored.source_final_result_id == context.source_final_result_id
    assert restored.validate() is True
    assert json.loads(payload)["source_final_result_id"] == "fr_4"


def test_manager_rejects_create_without_dispose() -> None:
    """Second create while active raises."""
    manager = ContextManager()
    manager.create(final_result=_final_result(result_id="fr_5"))
    with pytest.raises(InterpretationContextError, match="context_already_active"):
        manager.create(final_result=_final_result(result_id="fr_6"))
