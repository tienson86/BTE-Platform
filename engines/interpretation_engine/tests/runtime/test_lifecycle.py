"""Runtime lifecycle contract tests."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.explanation_runtime.runtime import ExplanationRuntime
from engines.interpretation_engine.interpreter_runtime.runtime import InterpreterRuntime
from engines.interpretation_engine.placeholder_runtime.runtime import PlaceholderRuntime
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.sentence_runtime.runtime import SentenceRuntime
from engines.interpretation_engine.template_runtime.runtime import TemplateRuntime
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context


@pytest.mark.parametrize(
    "runtime_cls",
    [
        InterpreterRuntime,
        SentenceRuntime,
        TemplateRuntime,
        PlaceholderRuntime,
        ExplanationRuntime,
    ],
)
def test_runtime_lifecycle_contract(runtime_cls: type) -> None:
    """Each runtime exposes initialize/shutdown/validate/execute/metrics/health."""
    runtime = runtime_cls()
    assert runtime.health() is HealthStatus.UNKNOWN
    assert runtime.validate() is False

    runtime.initialize()
    assert runtime.health() is HealthStatus.READY
    assert runtime.validate() is True

    context = make_pack_context()
    result = runtime.execute(context)
    assert result.success is True
    assert result.validate() is True
    metrics = runtime.metrics()
    assert metrics.execution_count == 1
    assert metrics.success_count == 1
    assert metrics.failure_count == 0
    assert metrics.last_execution is not None
    assert metrics.validate() is True
    assert runtime.health() is HealthStatus.READY

    runtime.shutdown()
    assert runtime.health() is HealthStatus.DISABLED
    assert runtime.validate() is False


def test_execute_requires_initialization() -> None:
    """Execute before initialize returns failure and FAILED health."""
    runtime = SentenceRuntime()
    result = runtime.execute(make_pack_context())
    assert result.success is False
    assert "runtime_not_initialized" in result.messages
    assert runtime.health() is HealthStatus.FAILED


def test_execute_rejects_non_pack_context() -> None:
    """Stage runtimes require PackInterpretationContext."""
    runtime = PlaceholderRuntime()
    runtime.initialize()
    result = runtime.execute(object())
    assert result.success is False
    assert "pack_interpretation_context_required" in result.messages
