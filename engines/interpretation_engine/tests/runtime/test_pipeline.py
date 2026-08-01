"""Runtime pipeline and execution manager tests."""

from __future__ import annotations

from engines.interpretation_engine.models.interpretation_result import InterpretationResult
from engines.interpretation_engine.orchestration.execution_manager import ExecutionManager
from engines.interpretation_engine.orchestration.runtime_pipeline import RuntimePipeline
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context
from engines.interpretation_engine.legacy_runtime.context import (
    InterpretationContext as LegacyInterpretationContext,
)


def test_runtime_pipeline_happy_path() -> None:
    """Pipeline runs ordered stages and returns InterpretationResult shell."""
    pipeline = RuntimePipeline()
    pipeline.initialize()
    assert pipeline.validate() is True
    assert [stage.runtime_id for stage in pipeline.stages] == [
        "interpreter_runtime",
        "sentence_runtime",
        "template_runtime",
        "placeholder_runtime",
        "explanation_runtime",
    ]

    result = pipeline.execute(make_pack_context())
    assert result.success is True
    assert "runtime_pipeline_ok" in result.messages
    interpretation = result.payload["interpretation_result"]
    assert isinstance(interpretation, InterpretationResult)
    assert interpretation.validate() is True
    assert interpretation.success is True
    assert interpretation.trace.stage_ids == (
        "interpreter_runtime",
        "sentence_runtime",
        "template_runtime",
        "placeholder_runtime",
        "explanation_runtime",
    )
    assert result.payload["stage_order"][3] == "placeholder_runtime"

    pipeline.shutdown()
    assert pipeline.health() is HealthStatus.DISABLED


def test_runtime_pipeline_rejects_legacy_context() -> None:
    """Pipeline rejects legacy InterpretationContext."""
    pipeline = RuntimePipeline()
    pipeline.initialize()
    result = pipeline.execute(LegacyInterpretationContext())
    assert result.success is False
    assert "pack_interpretation_context_required" in result.messages


def test_execution_manager_lifecycle() -> None:
    """ExecutionManager wraps pipeline lifecycle and metrics/health."""
    manager = ExecutionManager()
    assert manager.health() is HealthStatus.DISABLED
    assert manager.validate() is False
    failed = manager.execute(make_pack_context())
    assert failed.success is False

    manager.initialize()
    assert manager.validate() is True
    assert manager.health() is HealthStatus.READY
    result = manager.execute(make_pack_context(result_id="fr_mgr"))
    assert result.success is True
    assert manager.metrics().execution_count == 1
    manager.shutdown()
    assert manager.health() is HealthStatus.DISABLED
