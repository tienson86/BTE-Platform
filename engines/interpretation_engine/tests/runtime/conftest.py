"""Shared fixtures for Pack 03 runtime infrastructure tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)


def make_final_result(*, result_id: str = "fr_runtime_1") -> FinalResult:
    """Build a minimal valid Pack 02 FinalResult for runtime tests."""
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


def make_pack_context(*, result_id: str = "fr_runtime_1") -> PackInterpretationContext:
    """Build a PackInterpretationContext from Pack 02 FinalResult only."""
    final = make_final_result(result_id=result_id)
    return PackInterpretationContext(
        id=f"ctx_{result_id}",
        version="1.0.0",
        pipeline_id="interp_pipeline",
        source_final_result_id=final.id,
        final_result=final,
        attributes={},
        trace=("built",),
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
        completed_at=None,
        metadata={},
    )


@pytest.fixture
def pack_context() -> PackInterpretationContext:
    """Pytest fixture for PackInterpretationContext."""
    return make_pack_context()
