"""Tests for InterpreterRegistry / RuntimeRegistry / PipelineRegistry integration."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.catalog import (
    INTERPRETER_SKELETON_IDS,
)
from engines.interpretation_engine.interpreter_runtime.registries import (
    DependencyGraph,
    ExecutionGraph,
    GraphNode,
    InterpreterRegistration,
    InterpreterRegistry,
    PipelineRegistry,
    PriorityGraph,
    RuntimeRegistration,
    RuntimeRegistry,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.strength_interpreter import (
    StrengthInterpreter,
)
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.runtime.registry_base import RegistryError
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context


def test_interpreter_registry_auto_register_all_twelve() -> None:
    """Auto-register integrates every interpreter skeleton."""
    registry = InterpreterRegistry()
    registrations = registry.auto_register()
    assert len(registrations) == 12
    assert set(registry.list()) == set(INTERPRETER_SKELETON_IDS)
    assert registry.auto_registered is True
    assert registry.health() is HealthStatus.READY

    report = registry.validate_registry()
    assert report.success is True
    assert "interpreter_registry_ok" in report.messages
    assert set(report.details["execution_order"]) == set(INTERPRETER_SKELETON_IDS)

    # Dependency-aware order places strength before dependents.
    order = registry.execution_graph_order()
    assert order.index("strength_interpreter") < order.index("pattern_interpreter")
    assert order.index("pattern_interpreter") < order.index("useful_god_interpreter")
    assert order.index("scoring_interpreter") < order.index("summary_interpreter")
    assert registry.priority_graph_order()[0] == "strength_interpreter"

    registry.shutdown_all()
    assert registry.health() is HealthStatus.DISABLED


def test_interpreter_registry_with_dispatcher() -> None:
    """InterpreterRegistry syncs into injected dispatcher."""
    dispatcher = InterpreterDispatcher()
    registry = InterpreterRegistry(dispatcher=dispatcher)
    registry.auto_register()
    assert dispatcher.execution_order()
    context = make_pack_context(result_id="fr_reg_dispatch")
    results = dispatcher.dispatch(context)
    assert len(results) == 12
    assert all(payload.success for _, payload in results)


def test_interpreter_registry_unregister_and_invalid() -> None:
    """Unregister rebuilds graphs; invalid registration raises."""
    registry = InterpreterRegistry()
    registry.auto_register()
    registry.unregister_interpreter("summary_interpreter")
    assert "summary_interpreter" not in registry.list()
    report = registry.validate_registry()
    assert report.success is False
    assert "interpreters_missing" in report.messages

    with pytest.raises(RegistryError):
        registry.register_interpreter(
            InterpreterRegistration(
                interpreter_id="bad",
                runtime=StrengthInterpreter(),
                priority=1,
            )
        )


def test_runtime_registry_auto_register() -> None:
    """RuntimeRegistry auto-registers five stage runtimes."""
    registry = RuntimeRegistry()
    registrations = registry.auto_register()
    assert len(registrations) == 5
    assert registry.execution_order() == (
        "interpreter_runtime",
        "sentence_runtime",
        "template_runtime",
        "placeholder_runtime",
        "explanation_runtime",
    )
    assert registry.priority_order()[0] == "interpreter_runtime"
    assert registry.validate_registry() is True
    assert registry.health() is HealthStatus.READY
    assert registry.health_map()["sentence_runtime"] is HealthStatus.READY
    registry.shutdown_all()
    assert registry.health() is HealthStatus.DISABLED


def test_runtime_registry_invalid_registration() -> None:
    """RuntimeRegistry rejects mismatched runtime ids."""
    registry = RuntimeRegistry()
    with pytest.raises(RegistryError):
        registry.register_runtime(
            RuntimeRegistration(
                runtime_id="wrong",
                runtime=StrengthInterpreter(),
                priority=1,
            )
        )


def test_pipeline_registry_auto_register() -> None:
    """PipelineRegistry wires interpreter + runtime registries and orchestration."""
    pipeline_registry = PipelineRegistry()
    registrations = pipeline_registry.auto_register()
    assert len(registrations) == 4
    assert pipeline_registry.auto_registered is True
    assert pipeline_registry.validate_registry() is True
    assert pipeline_registry.health() is HealthStatus.READY
    assert pipeline_registry.execution_order()[-1] == "execution_manager"
    health = pipeline_registry.health_map()
    assert health["interpreter_registry"] == "READY"
    assert "interpreter:strength_interpreter" in health
    assert pipeline_registry.interpreter_registry is not None
    assert len(pipeline_registry.interpreter_registry.list()) == 12
    assert pipeline_registry.runtime_registry is not None
    assert len(pipeline_registry.runtime_registry.list()) == 5


def test_graphs_validation_and_cycles() -> None:
    """Dependency/priority/execution graphs validate and detect cycles."""
    dep = DependencyGraph()
    dep.add_node(GraphNode(node_id="a", priority=1, dependencies=("b",)))
    dep.add_node(GraphNode(node_id="b", priority=2, dependencies=("a",)))
    assert dep.has_cycle() is True
    with pytest.raises(RegistryError):
        dep.topological_order()

    priority = PriorityGraph()
    priority.set_priority("x", 2)
    priority.set_priority("y", 1)
    assert priority.ordered() == ("y", "x")
    assert priority.validate() is True
    priority.remove("x")
    assert priority.priority_of("x") is None

    graph = ExecutionGraph()
    graph.rebuild_from_nodes(
        (
            GraphNode(node_id="a", priority=10, dependencies=()),
            GraphNode(node_id="b", priority=20, dependencies=("a",)),
        )
    )
    assert graph.validate() is True
    assert graph.execution_order() == ("a", "b")

    with pytest.raises(RegistryError):
        DependencyGraph().add_node(GraphNode(node_id="", priority=1))
    with pytest.raises(RegistryError):
        PriorityGraph().set_priority("", 1)

    missing = DependencyGraph()
    missing.add_node(GraphNode(node_id="a", dependencies=("missing",)))
    assert missing.missing_dependencies() == ("missing",)
    assert missing.validate() is False
    assert missing.dependencies_of("a") == ("missing",)
    assert missing.get("a") is not None
    missing.remove_node("a")
    assert missing.nodes() == ()


def test_no_singleton_instances_are_independent() -> None:
    """Each registry instance is independently constructed (DI only)."""
    left = InterpreterRegistry()
    right = InterpreterRegistry()
    left.auto_register()
    assert right.list() == ()
    assert left is not right
