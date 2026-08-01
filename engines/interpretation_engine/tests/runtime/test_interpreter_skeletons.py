"""Tests for Pack 03 interpreter runtime skeletons."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)
from engines.interpretation_engine.interpreter_runtime.interpreters import (
    INTERPRETER_SKELETON_CLASSES,
    INTERPRETER_SKELETON_IDS,
    InterpretationSection,
    InterpreterSkeletonRuntime,
    create_all_interpreter_skeletons,
    empty_interpretation_section,
    register_interpreter_skeletons,
)
from engines.interpretation_engine.interpreter_runtime.registry import (
    InterpreterRuntimeRegistry,
)
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.tests.runtime.conftest import (
    make_final_result,
    make_pack_context,
)


EXPECTED_IDS = (
    "strength_interpreter",
    "season_interpreter",
    "temperature_interpreter",
    "pattern_interpreter",
    "useful_god_interpreter",
    "combination_interpreter",
    "conflict_interpreter",
    "ten_gods_interpreter",
    "shensha_interpreter",
    "luck_interpreter",
    "scoring_interpreter",
    "summary_interpreter",
)


def test_catalog_contains_all_twelve_interpreters() -> None:
    """Catalog lists exactly the twelve required skeleton interpreters."""
    assert INTERPRETER_SKELETON_IDS == EXPECTED_IDS
    assert len(INTERPRETER_SKELETON_CLASSES) == 12


@pytest.mark.parametrize("cls", INTERPRETER_SKELETON_CLASSES)
def test_interpreter_skeleton_lifecycle_contract(cls: type[InterpreterSkeletonRuntime]) -> None:
    """Each skeleton implements initialize/validate/execute/shutdown/health/metrics."""
    runtime = cls()
    assert runtime.health() is HealthStatus.UNKNOWN
    assert runtime.validate() is False

    runtime.initialize()
    assert runtime.health() is HealthStatus.READY
    assert runtime.validate() is True

    context = make_pack_context(result_id=f"fr_{runtime.interpreter_id}")
    result = runtime.execute(context)
    assert result.success is True
    assert "interpreter_skeleton_ok" in result.messages

    section = result.payload["interpretation_section"]
    assert isinstance(section, InterpretationSection)
    assert section.paragraphs == ()
    assert section.interpreter_id == runtime.interpreter_id
    assert section.section_type == runtime.section_type
    assert section.validate() is True
    assert result.payload["section"] is section

    metrics = runtime.metrics()
    assert metrics.execution_count == 1
    assert metrics.success_count == 1
    assert metrics.failure_count == 0
    assert metrics.validate() is True

    runtime.shutdown()
    assert runtime.health() is HealthStatus.DISABLED
    assert runtime.validate() is False


def test_empty_interpretation_section_helper() -> None:
    """Helper builds empty InterpretationSection shells."""
    section = empty_interpretation_section(
        interpreter_id="strength_interpreter",
        section_type="strength",
        context_id="ctx_1",
    )
    assert section.id == "section_strength_interpreter_ctx_1"
    assert section.paragraphs == ()
    assert section.validate() is True


def test_execute_rejects_invalid_context() -> None:
    """Skeletons require valid PackInterpretationContext."""
    runtime = create_all_interpreter_skeletons()[0]
    runtime.initialize()
    assert runtime.execute(object()).success is False

    final = make_final_result(result_id="fr_bad_skel")
    invalid = PackInterpretationContext(
        id="",
        version="1.0.0",
        pipeline_id="p",
        source_final_result_id=final.id,
        final_result=final,
        created_at="2026-01-01T00:00:00Z",
    )
    assert runtime.execute(invalid).success is False


def test_register_interpreter_skeletons_with_registry_and_dispatcher() -> None:
    """Skeletons register into DI registry and dispatcher without singletons."""
    registry = InterpreterRuntimeRegistry()
    dispatcher = InterpreterDispatcher()
    skeletons = create_all_interpreter_skeletons()
    for skeleton in skeletons:
        skeleton.initialize()

    registered = register_interpreter_skeletons(
        registry=registry,
        dispatcher=dispatcher,
        skeletons=skeletons,
    )
    assert len(registered) == 12
    assert registry.list() == tuple(sorted(EXPECTED_IDS))
    assert dispatcher.execution_order() == EXPECTED_IDS

    context = make_pack_context(result_id="fr_dispatch_all")
    results = dispatcher.dispatch(context)
    assert len(results) == 12
    for entry_id, payload in results:
        assert entry_id in EXPECTED_IDS
        assert payload.success is True
        section = payload.payload["interpretation_section"]
        assert section.paragraphs == ()


def test_register_without_optional_targets() -> None:
    """Factory works when registry/dispatcher are omitted."""
    instances = register_interpreter_skeletons()
    assert len(instances) == 12
    assert all(isinstance(item, InterpreterSkeletonRuntime) for item in instances)


def test_register_custom_skeleton_uses_fallback_priority() -> None:
    """Unknown interpreter ids receive fallback dispatcher priority."""

    class _Custom(InterpreterSkeletonRuntime):
        interpreter_id = "custom_interpreter"
        section_type = "custom"

    dispatcher = InterpreterDispatcher()
    custom = _Custom()
    custom.initialize()
    register_interpreter_skeletons(dispatcher=dispatcher, skeletons=(custom,))
    assert dispatcher.execution_order() == ("custom_interpreter",)
