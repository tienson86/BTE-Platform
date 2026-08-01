"""Interpreter dispatcher tests."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)
from engines.interpretation_engine.runtime.registry_base import RegistryError
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context


def test_dispatcher_priority_and_dependency_order() -> None:
    """Dispatcher orders by dependencies then priority."""
    dispatcher = InterpreterDispatcher()
    order: list[str] = []

    def make_handler(name: str):
        def _handler(context: object) -> str:
            order.append(name)
            return name

        return _handler

    dispatcher.register("c", make_handler("c"), priority=10, dependencies=("a", "b"))
    dispatcher.register("b", make_handler("b"), priority=50, dependencies=("a",))
    dispatcher.register("a", make_handler("a"), priority=100)
    dispatcher.register("d", make_handler("d"), priority=1, enabled=False)

    assert dispatcher.execution_order() == ("a", "b", "c")
    results = dispatcher.dispatch(make_pack_context())
    assert [item[0] for item in results] == ["a", "b", "c"]
    assert order == ["a", "b", "c"]
    assert "d" not in dispatcher.execution_order()


def test_dispatcher_circular_dependency() -> None:
    """Circular dependencies raise RegistryError."""
    dispatcher = InterpreterDispatcher()
    dispatcher.register("a", lambda ctx: "a", dependencies=("b",))
    dispatcher.register("b", lambda ctx: "b", dependencies=("a",))
    with pytest.raises(RegistryError, match="dispatcher_circular_dependency"):
        dispatcher.execution_order()


def test_dispatcher_register_validation() -> None:
    """Dispatcher rejects empty ids / missing handlers."""
    dispatcher = InterpreterDispatcher()
    with pytest.raises(RegistryError):
        dispatcher.register("", lambda ctx: None)
    with pytest.raises(RegistryError):
        dispatcher.register("x", None)  # type: ignore[arg-type]
    dispatcher.register("x", lambda ctx: "x")
    assert dispatcher.list() == ("x",)
    dispatcher.unregister("x")
    assert dispatcher.list() == ()
