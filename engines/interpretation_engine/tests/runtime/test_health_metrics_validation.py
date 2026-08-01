"""Health, metrics, validation, and legacy adapter tests."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.health.health_manager import HealthManager
from engines.interpretation_engine.legacy_runtime.context import (
    InterpretationContext as LegacyInterpretationContext,
)
from engines.interpretation_engine.metrics.runtime_metrics import RuntimeMetricsCollector
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.runtime.legacy_adapter import (
    LEGACY_COMPATIBILITY_ADAPTER,
    LegacyContextAdapter,
)
from engines.interpretation_engine.sentence_runtime.runtime import SentenceRuntime
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context
from engines.interpretation_engine.validation.runtime_validator import (
    RuntimeValidator,
    ValidationReport,
)
from engines.interpretation_engine.sentence_runtime.registry import SentenceRuntimeRegistry


def test_health_manager() -> None:
    """HealthManager aggregates READY/FAILED/DISABLED/UNKNOWN states."""
    manager = HealthManager()
    assert manager.overall() is HealthStatus.UNKNOWN
    assert manager.validate() is False

    ready = SentenceRuntime()
    ready.initialize()
    disabled = SentenceRuntime(runtime_id="disabled_runtime")
    manager.register("ready", ready)
    manager.register("disabled", disabled)
    assert manager.overall() is HealthStatus.UNKNOWN
    snapshot = manager.snapshot()
    assert snapshot["ready"] == "READY"
    assert snapshot["overall"] in {"UNKNOWN", "READY", "DISABLED"}

    manager.unregister("disabled")
    assert manager.overall() is HealthStatus.READY
    assert manager.validate() is True

    with pytest.raises(ValueError, match="health_runtime_id_required"):
        manager.register("", ready)


def test_runtime_metrics_collector() -> None:
    """RuntimeMetricsCollector aggregates execution counters."""
    collector = RuntimeMetricsCollector()
    assert collector.aggregate().health is HealthStatus.UNKNOWN

    runtime = SentenceRuntime()
    runtime.initialize()
    runtime.execute(make_pack_context())
    collector.register("sentence", runtime)
    aggregate = collector.aggregate()
    assert aggregate.execution_count == 1
    assert aggregate.success_count == 1
    as_dict = collector.as_dict()
    assert as_dict["sentence"]["execution_count"] == 1
    assert as_dict["aggregate"]["success_count"] == 1
    collector.unregister("sentence")
    with pytest.raises(ValueError):
        collector.register("", runtime)


def test_runtime_validator() -> None:
    """RuntimeValidator covers config/registry/deps/contract/state."""
    validator = RuntimeValidator()
    assert validator.validate_configuration(None).success is False
    assert validator.validate_configuration({"runtime_id": ""}).success is False
    assert validator.validate_configuration({"runtime_id": "x"}).success is True

    registry = SentenceRuntimeRegistry()
    assert validator.validate_registry(registry).success is True
    deps_ok = validator.validate_dependencies(
        required=("a", "b"),
        available=("a", "b", "c"),
    )
    assert deps_ok.success is True
    deps_bad = validator.validate_dependencies(required=("a", "z"), available=("a",))
    assert deps_bad.success is False
    assert deps_bad.details["missing"] == ["z"]

    runtime = SentenceRuntime()
    assert validator.validate_contract(runtime).success is False
    runtime.initialize()
    assert validator.validate_contract(runtime).success is True
    state = validator.validate_runtime_state(runtime)
    assert state.success is True
    assert ValidationReport(success=True).validate() is True


def test_legacy_adapter() -> None:
    """Legacy adapter keeps legacy packages while enforcing Pack 03 context."""
    assert LEGACY_COMPATIBILITY_ADAPTER is True
    adapter = LegacyContextAdapter()
    pack = make_pack_context()
    legacy = LegacyInterpretationContext()

    assert adapter.is_pack03(pack) is True
    assert adapter.is_legacy(legacy) is True
    assert adapter.require_pack03(pack) is pack
    assert adapter.describe(pack)["kind"] == "pack03"
    assert adapter.describe(legacy)["kind"] == "legacy"
    assert adapter.describe(object())["kind"] == "unknown"

    with pytest.raises(TypeError, match="legacy_rejected"):
        adapter.require_pack03(legacy)
    with pytest.raises(TypeError, match="pack_interpretation_context_required"):
        adapter.require_pack03(object())
