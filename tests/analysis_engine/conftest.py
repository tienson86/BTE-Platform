"""Shared fixtures for Analysis Engine infrastructure tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.analysis_engine.context.context_factory import ContextFactory
from engines.analysis_engine.models.analysis_context import AnalysisContext
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


@pytest.fixture
def analysis_engine_root() -> Path:
    """Return the Analysis Engine package root path."""
    return Path(__file__).resolve().parents[2] / "engines" / "analysis_engine"


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the fixtures directory path."""
    return Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def snapshots_dir() -> Path:
    """Return the snapshots directory path."""
    return Path(__file__).resolve().parent / "snapshots"


@pytest.fixture
def golden_dir() -> Path:
    """Return the golden dataset directory path."""
    return Path(__file__).resolve().parent / "golden"


@pytest.fixture
def analysis_context_stub() -> AnalysisContext:
    """Return a shared analysis context stub for infrastructure wiring."""
    return ContextFactory().create(
        pipeline_id="test_pipeline",
        context_id="test_context",
        chart_id="test_chart",
        attributes={"source": "test_stub"},
    )


@pytest.fixture
def pipeline_context_stub() -> PipelineContext:
    """Return a shared pipeline context stub."""
    return PipelineContext(
        context_id="pipe_ctx_1",
        pipeline_id="test_pipeline",
        chart_id="test_chart",
        attributes={"source": "test_stub"},
    )
