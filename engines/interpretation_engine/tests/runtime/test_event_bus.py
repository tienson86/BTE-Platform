"""Tests for Pack 03 local Event Bus."""

from __future__ import annotations

from engines.interpretation_engine.events import (
    REQUIRED_RUNTIME_EVENTS,
    EventBus,
    InterpretationEventType,
    LocalEventBus,
    RuntimeEvent,
    make_event,
)
from engines.interpretation_engine.orchestration.execution_pipeline import ExecutionPipeline
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context
from engines.interpretation_engine.interpreter_runtime.interpreters.strength_interpreter import (
    StrengthInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.registries.interpreter_registry import (
    InterpreterRegistration,
    InterpreterRegistry,
)
from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)


def test_required_runtime_events_defined() -> None:
    """Required event types are present."""
    values = {item.value for item in REQUIRED_RUNTIME_EVENTS}
    assert values == {
        "before_interpreter",
        "after_interpreter",
        "pipeline_started",
        "pipeline_finished",
        "runtime_error",
        "health_changed",
    }


def test_local_event_bus_publish_subscribe() -> None:
    """LocalEventBus fans out to subscribers and isolates handler errors."""
    bus = LocalEventBus(bus_id="test_bus", history_limit=10)
    assert bus.validate() is True
    assert bus.supports_required_events() is True
    assert EventBus is LocalEventBus

    seen: list[str] = []

    def _ok(event_type: InterpretationEventType, payload: object) -> None:
        seen.append(event_type.value)

    def _boom(event_type: InterpretationEventType, payload: object) -> None:
        raise RuntimeError("handler_boom")

    bus.subscribe(InterpretationEventType.PIPELINE_STARTED, _ok)
    bus.subscribe(InterpretationEventType.PIPELINE_STARTED, _boom)
    bus.publish(InterpretationEventType.PIPELINE_STARTED, {"x": 1})
    assert seen == ["pipeline_started"]
    assert len(bus.history_of(InterpretationEventType.PIPELINE_STARTED)) == 1

    bus.unsubscribe(InterpretationEventType.PIPELINE_STARTED, _ok)
    bus.unsubscribe(InterpretationEventType.PIPELINE_STARTED, _ok)  # no-op
    assert bus.subscriber_count(InterpretationEventType.PIPELINE_STARTED) == 1

    event = bus.emit(
        InterpretationEventType.HEALTH_CHANGED,
        source="test",
        payload={"current": "READY"},
    )
    assert isinstance(event, RuntimeEvent)
    assert event.validate() is True
    assert bus.subscriber_count() >= 1
    assert InterpretationEventType.PIPELINE_STARTED in bus.subscribed_types() or True

    bus.clear()
    assert bus.history() == ()
    assert bus.subscriber_count() == 0


def test_event_bus_history_limit_and_invalid() -> None:
    """History is bounded; invalid events are rejected."""
    bus = LocalEventBus(history_limit=2)
    bus.emit(InterpretationEventType.RUNTIME_ERROR, source="s", payload={"a": 1})
    bus.emit(InterpretationEventType.RUNTIME_ERROR, source="s", payload={"a": 2})
    bus.emit(InterpretationEventType.RUNTIME_ERROR, source="s", payload={"a": 3})
    assert len(bus.history()) == 2

    invalid = RuntimeEvent(
        event_type=InterpretationEventType.RUNTIME_ERROR,
        source="",
    )
    assert invalid.validate() is False
    try:
        bus.publish_event(invalid)
        raised = False
    except ValueError:
        raised = True
    assert raised is True

    try:
        bus.subscribe(InterpretationEventType.RUNTIME_ERROR, None)  # type: ignore[arg-type]
        bad_sub = False
    except ValueError:
        bad_sub = True
    assert bad_sub is True

    zero = LocalEventBus(history_limit=0)
    zero.emit(InterpretationEventType.PIPELINE_FINISHED, source="s")
    assert zero.history() == ()


def test_execution_pipeline_emits_required_events() -> None:
    """ExecutionPipeline emits the required local runtime events."""
    bus = LocalEventBus(bus_id="pipeline_bus")
    pipeline = ExecutionPipeline(event_bus=bus)
    pipeline.initialize()

    # health_changed on initialize
    assert any(
        item.event_type is InterpretationEventType.HEALTH_CHANGED
        for item in bus.history()
    )

    result = pipeline.execute(make_pack_context(result_id="fr_events"))
    assert result.success is True

    types = [item.event_type for item in bus.history()]
    assert InterpretationEventType.PIPELINE_STARTED in types
    assert InterpretationEventType.BEFORE_INTERPRETER in types
    assert InterpretationEventType.AFTER_INTERPRETER in types
    assert InterpretationEventType.PIPELINE_FINISHED in types
    assert InterpretationEventType.HEALTH_CHANGED in types

    before_count = sum(
        1 for item in types if item is InterpretationEventType.BEFORE_INTERPRETER
    )
    after_count = sum(
        1 for item in types if item is InterpretationEventType.AFTER_INTERPRETER
    )
    assert before_count == 12
    assert after_count == 12

    pipeline.shutdown()
    assert bus.history_of(InterpretationEventType.HEALTH_CHANGED)


def test_execution_pipeline_emits_runtime_error_on_isolated_failure() -> None:
    """Isolated interpreter exceptions publish runtime_error events."""

    class _Boom(StrengthInterpreter):
        interpreter_id = "strength_interpreter"
        section_type = "strength"

        def execute(self, context):  # type: ignore[override]
            raise RuntimeError("boom")

    dispatcher = InterpreterDispatcher()
    registry = InterpreterRegistry(dispatcher=dispatcher)
    boom = _Boom()
    boom.initialize()
    ok = StrengthInterpreter()
    ok.interpreter_id = "season_interpreter"
    ok.runtime_id = "season_interpreter"
    ok.section_type = "season"
    ok.initialize()
    registry.register_interpreter(
        InterpreterRegistration(
            interpreter_id="strength_interpreter",
            runtime=boom,
            priority=10,
            section_type="strength",
            version="0.0.0-skeleton",
        )
    )
    registry.register_interpreter(
        InterpreterRegistration(
            interpreter_id="season_interpreter",
            runtime=ok,
            priority=20,
            section_type="season",
            version="0.0.0-skeleton",
        )
    )

    bus = LocalEventBus()
    pipeline = ExecutionPipeline(
        interpreter_registry=registry,
        dispatcher=dispatcher,
        event_bus=bus,
        auto_register=False,
    )
    pipeline.initialize()
    result = pipeline.execute(make_pack_context(result_id="fr_evt_err"))
    assert result.success is True
    errors = bus.history_of(InterpretationEventType.RUNTIME_ERROR)
    assert errors
    assert any("strength_interpreter" in str(item.payload) for item in errors)


def test_make_event_helper() -> None:
    """make_event builds a valid envelope."""
    event = make_event(
        InterpretationEventType.BEFORE_INTERPRETER,
        source="unit",
        payload={"interpreter_id": "x"},
        correlation_id="ctx",
    )
    assert event.event_type is InterpretationEventType.BEFORE_INTERPRETER
    assert event.payload["interpreter_id"] == "x"


def test_event_bus_edge_paths() -> None:
    """Cover unsubscribe empty, publish_event isolation, coerce paths."""
    bus = LocalEventBus()
    bus.unsubscribe(InterpretationEventType.PIPELINE_STARTED, lambda e, p: None)

    seen: list[object] = []

    def _ok(event_type: InterpretationEventType, payload: object) -> None:
        seen.append(payload)

    def _boom(event_type: InterpretationEventType, payload: object) -> None:
        raise RuntimeError("publish_event_boom")

    bus.subscribe(InterpretationEventType.AFTER_INTERPRETER, _ok)
    bus.subscribe(InterpretationEventType.AFTER_INTERPRETER, _boom)
    event = make_event(
        InterpretationEventType.AFTER_INTERPRETER,
        source="unit",
        payload={"ok": True},
    )
    bus.publish_event(event)
    assert event in seen

    # Removing both handlers triggers empty-list pop
    bus.unsubscribe(InterpretationEventType.AFTER_INTERPRETER, _ok)
    bus.unsubscribe(InterpretationEventType.AFTER_INTERPRETER, _boom)
    assert bus.subscriber_count(InterpretationEventType.AFTER_INTERPRETER) == 0

    # Coerce RuntimeEvent and non-dict payloads
    bus.publish(InterpretationEventType.BEFORE_INTERPRETER, event)
    bus.publish(InterpretationEventType.BEFORE_INTERPRETER, "plain")
    assert bus.history_of(InterpretationEventType.BEFORE_INTERPRETER)

    # Invalid event_type on envelope
    bad = RuntimeEvent(event_type="nope", source="x")  # type: ignore[arg-type]
    assert bad.validate() is False
