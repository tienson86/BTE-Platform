"""Tests for dependency and priority models."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.interpreter_framework import (
    ConfigurationError,
    DependencyError,
    DependencyResolver,
    InterpreterDependency,
    InterpreterPriority,
    order_ids_by_priority,
    sort_by_priority,
)


def test_dependency_edge_validate() -> None:
    """Dependency edges reject self-deps and empties."""
    assert InterpreterDependency("a", "b").validate() is True
    assert InterpreterDependency("a", "a").validate() is False
    assert InterpreterDependency("", "b").validate() is False


def test_dependency_resolver_order_and_optional_missing() -> None:
    """Resolver orders by required deps and reports optional gaps."""
    resolver = DependencyResolver()
    resolution = resolver.resolve(
        interpreter_ids=("c", "a", "b"),
        required={"b": ("a",), "c": ("b",)},
        optional={"c": ("missing_opt",)},
    )
    assert resolution.order == ("a", "b", "c")
    assert resolution.missing_optional == ("c->missing_opt",)
    assert resolution.validate() is True


def test_dependency_resolver_missing_required_and_cycle() -> None:
    """Resolver raises on missing required deps and cycles."""
    resolver = DependencyResolver()
    with pytest.raises(DependencyError):
        resolver.resolve(
            interpreter_ids=("a",),
            required={"a": ("missing",)},
        )
    with pytest.raises(DependencyError):
        resolver.resolve(
            interpreter_ids=("a", "b"),
            required={"a": ("b",), "b": ("a",)},
        )


def test_priority_sort_and_order_ids() -> None:
    """Priority helpers sort deterministically."""
    items = (
        InterpreterPriority("b", 20),
        InterpreterPriority("a", 10),
        InterpreterPriority("c", 10),
    )
    assert all(item.validate() for item in items)
    ordered = sort_by_priority(items)
    assert [item.interpreter_id for item in ordered] == ["a", "c", "b"]

    assert order_ids_by_priority({"x": 2, "y": 1}) == ("y", "x")
    with pytest.raises(ConfigurationError):
        order_ids_by_priority({"x": 1}, ids=("x", "missing"))
    assert InterpreterPriority("", 1).validate() is False
