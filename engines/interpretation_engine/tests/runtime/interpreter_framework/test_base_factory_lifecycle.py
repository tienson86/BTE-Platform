"""Tests for BaseInterpreter lifecycle and InterpreterFactory."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.interpreter_framework import (
    BaseInterpreter,
    ConfigurationError,
    EmptyFrameworkInterpreter,
    ExecutionError,
    FrameworkInterpreterResult,
    InterpreterFactory,
    InterpreterMetadata,
    ValidationError,
)
from engines.interpretation_engine.interpreter_framework.interpreter_builder import (
    InterpretationSectionBuilder,
)
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context


class _BoomInterpreter(BaseInterpreter):
    """Interpreter that raises ExecutionError."""

    interpreter_id = "boom_interpreter"
    section_type = "boom"
    version = "1.0.0"
    category = "test"

    def interpret(
        self, context: PackInterpretationContext
    ) -> FrameworkInterpreterResult:
        raise ExecutionError("boom")


class _InvalidResultInterpreter(BaseInterpreter):
    """Interpreter that returns an invalid framework result."""

    interpreter_id = "invalid_result_interpreter"
    section_type = "invalid"
    version = "1.0.0"
    category = "test"

    def interpret(
        self, context: PackInterpretationContext
    ) -> FrameworkInterpreterResult:
        section = (
            self.new_builder()
            .for_interpreter(
                interpreter_id=self.interpreter_id,
                section_type=self.section_type,
                context_id=context.id,
            )
            .build()
        )
        return FrameworkInterpreterResult(
            section=section,
            metadata=InterpreterMetadata(interpreter_id="", version="1.0.0"),
            confidence=0.5,
        )


class _UnexpectedInterpreter(BaseInterpreter):
    """Interpreter that raises a generic exception."""

    interpreter_id = "unexpected_interpreter"
    section_type = "unexpected"
    version = "1.0.0"
    category = "test"

    def interpret(
        self, context: PackInterpretationContext
    ) -> FrameworkInterpreterResult:
        raise RuntimeError("unexpected")


def test_empty_framework_interpreter_lifecycle() -> None:
    """EmptyFrameworkInterpreter supports full lifecycle contract."""
    runtime = EmptyFrameworkInterpreter()
    assert runtime.health() is HealthStatus.UNKNOWN
    assert runtime.validate() is False

    runtime.initialize()
    assert runtime.health() is HealthStatus.READY
    assert runtime.validate() is True
    assert runtime.capability().validate() is True

    context = make_pack_context(result_id="fr_fw_life")
    result = runtime.execute(context)
    assert result.success is True
    assert "empty_framework_interpreter_ok" in result.messages
    assert result.payload["section"].section_type == "framework"
    assert result.payload["interpretation_section"] is result.payload["section"]
    assert runtime._before_called is True
    assert runtime._after_called is True

    metrics = runtime.metrics()
    assert metrics.execution_count == 1
    assert metrics.success_count == 1
    assert metrics.validate() is True

    runtime.shutdown()
    assert runtime.health() is HealthStatus.DISABLED


def test_base_interpreter_rejects_invalid_context() -> None:
    """Framework execute fails fast on invalid context type."""
    runtime = EmptyFrameworkInterpreter()
    runtime.initialize()
    result = runtime.execute(object())
    assert result.success is False
    assert "validation_error" in result.messages


def test_base_interpreter_execution_and_unexpected_errors() -> None:
    """ExecutionError and unexpected exceptions are surfaced as failed results."""
    boom = _BoomInterpreter()
    boom.initialize()
    out = boom.execute(make_pack_context(result_id="fr_boom"))
    assert out.success is False
    assert "execution_error" in out.messages

    bad = _InvalidResultInterpreter()
    bad.initialize()
    out_bad = bad.execute(make_pack_context(result_id="fr_bad"))
    assert out_bad.success is False
    assert "validation_error" in out_bad.messages

    unexpected = _UnexpectedInterpreter()
    unexpected.initialize()
    out_u = unexpected.execute(make_pack_context(result_id="fr_u"))
    assert out_u.success is False
    assert "execution_error" in out_u.messages


def test_factory_registry_create_without_switch() -> None:
    """Factory creates interpreters by registry lookup only."""
    factory = InterpreterFactory()
    factory.register("empty_framework_interpreter", EmptyFrameworkInterpreter)
    assert factory.has("empty_framework_interpreter") is True
    assert "empty_framework_interpreter" in factory.registered_ids()

    instance = factory.create("empty_framework_interpreter")
    assert isinstance(instance, BaseInterpreter)
    assert instance.interpreter_id == "empty_framework_interpreter"

    all_instances = factory.create_all()
    assert len(all_instances) == 1

    factory.unregister("empty_framework_interpreter")
    assert factory.has("empty_framework_interpreter") is False
    with pytest.raises(ConfigurationError):
        factory.create("missing")

    with pytest.raises(ConfigurationError):
        factory.register("", EmptyFrameworkInterpreter)

    def _bad(**kwargs):
        return object()

    factory.register("bad", _bad)
    with pytest.raises(ConfigurationError):
        factory.create("bad")
