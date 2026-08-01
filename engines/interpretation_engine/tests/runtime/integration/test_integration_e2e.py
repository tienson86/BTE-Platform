"""End-to-end integration tests for Pack 03 runtime infrastructure.

Wires registry + dispatcher + execution pipeline + events + monitoring + validation.
Infrastructure only. No BaZi business logic.
"""

from __future__ import annotations

from engines.interpretation_engine.cache import CacheManager
from engines.interpretation_engine.events import (
    InterpretationEventType,
    LocalEventBus,
)
from engines.interpretation_engine.health import HealthManager
from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)
from engines.interpretation_engine.interpreter_runtime.registries import (
    InterpreterRegistry,
    PipelineRegistry,
    RuntimeRegistry,
)
from engines.interpretation_engine.metrics.runtime_metrics import RuntimeMetricsCollector
from engines.interpretation_engine.models.interpretation_result import InterpretationResult
from engines.interpretation_engine.models.metadata import Metadata
from engines.interpretation_engine.models.version_info import VersionInfo
from engines.interpretation_engine.monitoring import RuntimeMonitor
from engines.interpretation_engine.orchestration import ExecutionPipeline
from engines.interpretation_engine.orchestration.async_executor import ExecutionMode
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context
from engines.interpretation_engine.validation import ValidationFramework


def test_full_runtime_integration_happy_path() -> None:
    """Integrate registry, dispatcher, pipeline, events, monitor, cache, validation."""
    bus = LocalEventBus(bus_id="integration_bus")
    monitor = RuntimeMonitor(monitor_id="integration_monitor")
    dispatcher = InterpreterDispatcher()
    interpreter_registry = InterpreterRegistry(dispatcher=dispatcher)
    runtime_registry = RuntimeRegistry()
    cache = CacheManager()
    health = HealthManager()
    metrics = RuntimeMetricsCollector()
    validator = ValidationFramework()

    pipeline = ExecutionPipeline(
        interpreter_registry=interpreter_registry,
        dispatcher=dispatcher,
        event_bus=bus,
        monitor=monitor,
        execution_mode=ExecutionMode.DEPENDENCY,
        auto_register=True,
    )
    pipeline.initialize()

    # Nested registries/cache/health/metrics wiring
    runtime_registry.auto_register()
    pipeline_registry = PipelineRegistry(
        interpreter_registry=interpreter_registry,
        runtime_registry=runtime_registry,
    )
    pipeline_registry.auto_register(
        interpreter_registry=interpreter_registry,
        runtime_registry=runtime_registry,
        initialize_pipeline=False,
    )

    health.register("execution_pipeline", pipeline)
    for stage in runtime_registry.list():
        entry = runtime_registry.lookup(stage)
        assert entry is not None
        health.register(stage, entry.runtime)
        metrics.register(stage, entry.runtime)
    metrics.register("execution_pipeline", pipeline)

    context = make_pack_context(result_id="fr_integration")
    cache.context.set(context.id, {"context_id": context.id})
    cache.registry.set("strength_interpreter", {"skeleton": True})

    validation = validator.validate_all(
        runtime=pipeline,
        registry=interpreter_registry,
        context=context,
        metadata=Metadata(
            id="meta_integration",
            version_info=VersionInfo(schema_version="1.0.0"),
            created_at=context.created_at,
        ),
        required_dependencies=("strength_interpreter",),
        available_dependencies=interpreter_registry.list(),
        version_info=VersionInfo(schema_version="1.0.0"),
    )
    assert validation.success is True

    result = pipeline.execute(context)
    assert result.success is True
    interpretation = result.payload["interpretation_result"]
    assert isinstance(interpretation, InterpretationResult)
    assert len(interpretation.sections) == 12
    assert result.payload["monitoring"].last_pipeline_latency is not None

    event_types = {item.event_type for item in bus.history()}
    assert InterpretationEventType.PIPELINE_STARTED in event_types
    assert InterpretationEventType.BEFORE_INTERPRETER in event_types
    assert InterpretationEventType.AFTER_INTERPRETER in event_types
    assert InterpretationEventType.PIPELINE_FINISHED in event_types

    assert health.overall() in {HealthStatus.READY, HealthStatus.RUNNING}
    assert metrics.aggregate().execution_count >= 1
    assert cache.context.get(context.id) is not None
    assert pipeline_registry.validate_registry() is True

    pipeline.shutdown()
    assert pipeline.health() is HealthStatus.DISABLED
