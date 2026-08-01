"""Dispatcher-focused integration tests."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)
from engines.interpretation_engine.interpreter_runtime.registries import (
    InterpreterRegistry,
)
from engines.interpretation_engine.runtime.registry_base import RegistryError
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context


def test_dispatcher_with_registry_auto_registration() -> None:
    """Dispatcher execution order follows registry dependency/priority wiring."""
    dispatcher = InterpreterDispatcher()
    registry = InterpreterRegistry(dispatcher=dispatcher)
    registry.auto_register()

    order = dispatcher.execution_order()
    assert "strength_interpreter" in order
    assert order.index("strength_interpreter") < order.index("summary_interpreter")
    assert order.index("pattern_interpreter") < order.index("useful_god_interpreter")

    context = make_pack_context(result_id="fr_dispatch_int")
    results = dispatcher.dispatch(context)
    assert len(results) == 12
    assert all(payload.success for _, payload in results)


def test_dispatcher_dependency_and_priority_integration() -> None:
    """Custom dependency + priority ordering integrates with dispatch."""
    dispatcher = InterpreterDispatcher()
    seen: list[str] = []

    def make_handler(name: str):
        def _handler(context: object) -> str:
            seen.append(name)
            return name

        return _handler

    dispatcher.register("c", make_handler("c"), priority=5, dependencies=("a", "b"))
    dispatcher.register("b", make_handler("b"), priority=20, dependencies=("a",))
    dispatcher.register("a", make_handler("a"), priority=50)
    assert dispatcher.execution_order() == ("a", "b", "c")
    dispatcher.dispatch(object())
    assert seen == ["a", "b", "c"]


def test_dispatcher_cycle_detection_integration() -> None:
    """Circular dependencies fail closed."""
    dispatcher = InterpreterDispatcher()
    dispatcher.register("a", lambda ctx: None, dependencies=("b",))
    dispatcher.register("b", lambda ctx: None, dependencies=("a",))
    with pytest.raises(RegistryError, match="dispatcher_circular_dependency"):
        dispatcher.execution_order()
