"""Tests for builder, validator, context, result, and trace."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.interpreter_framework import (
    ConfigurationError,
    DependencyError,
    ExecutionStatistics,
    FrameworkInterpreterContext,
    FrameworkInterpreterResult,
    InterpretationSectionBuilder,
    InterpreterCapability,
    InterpreterDependency,
    InterpreterMetadata,
    InterpreterTrace,
    InterpreterValidator,
    ValidationError,
)
from engines.interpretation_engine.models.paragraph_result import ParagraphResult
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context


def test_builder_builds_valid_section() -> None:
    """Builder produces a valid InterpretationSection."""
    section = (
        InterpretationSectionBuilder()
        .for_interpreter(
            interpreter_id="demo",
            section_type="demo",
            context_id="ctx1",
        )
        .with_title_ref("demo.title")
        .add_message("ok")
        .update_attributes({"framework": True})
        .with_success(True)
        .build()
    )
    assert section.id == "section_demo_ctx1"
    assert section.validate() is True
    assert section.messages == ("ok",)


def test_builder_requires_id_and_section_type() -> None:
    """Builder raises when required fields missing."""
    with pytest.raises(ConfigurationError):
        InterpretationSectionBuilder().build()


def test_builder_rejects_invalid_paragraph_link() -> None:
    """Builder validate fails when paragraph section_id mismatches."""
    with pytest.raises(ConfigurationError):
        (
            InterpretationSectionBuilder()
            .with_id("sec1")
            .with_section_type("demo")
            .add_paragraph(
                ParagraphResult(id="p1", section_id="other")
            )
            .build()
        )


def test_validator_input_result_dependency() -> None:
    """Validator covers input/result/dependency paths."""
    validator = InterpreterValidator()
    ctx = make_pack_context(result_id="fr_fw_1")
    assert validator.validate_input(ctx) is True
    assert validator.require_input(ctx) is ctx
    with pytest.raises(ValidationError):
        validator.require_input(object())

    capability = InterpreterCapability(
        interpreter_id="x", category="c", priority=1, version="1.0.0"
    )
    assert validator.validate_capability(capability) is True
    validator.require_capability(capability)

    section = (
        InterpretationSectionBuilder()
        .for_interpreter(interpreter_id="x", section_type="x", context_id=ctx.id)
        .build()
    )
    assert validator.validate_section(section) is True
    validator.require_section(section)

    result = FrameworkInterpreterResult(
        section=section,
        metadata=InterpreterMetadata(interpreter_id="x", version="1.0.0"),
        confidence=0.9,
    )
    assert validator.validate_result(result) is True
    validator.require_result(result)

    assert validator.validate_dependencies(
        interpreter_ids=("a", "b"),
        required={"b": ("a",)},
    )
    assert validator.require_dependencies(
        interpreter_ids=("a", "b"),
        required={"b": ("a",)},
    ) == ("a", "b")
    assert (
        validator.validate_dependencies(
            interpreter_ids=("a",),
            required={"a": ("missing",)},
        )
        is False
    )
    with pytest.raises(DependencyError):
        validator.require_dependencies(
            interpreter_ids=("a",),
            required={"a": ("missing",)},
        )
    assert validator.validate_dependency_edge(
        InterpreterDependency("a", "b")
    )


def test_framework_context_and_result_trace() -> None:
    """Framework context/result/trace helpers work."""
    pack = make_pack_context(result_id="fr_fw_2")
    meta = InterpreterMetadata(interpreter_id="x", version="1.0.0")
    fw = FrameworkInterpreterContext.from_pack_context(
        pack, runtime_metadata=meta, attributes={"a": 1}
    )
    assert fw.id == pack.id
    assert fw.final_result.id == pack.final_result.id
    assert fw.validate() is True
    fw.require_valid()

    bad = FrameworkInterpreterContext.from_pack_context(
        pack,
        runtime_metadata=InterpreterMetadata(interpreter_id="", version="1"),
    )
    assert bad.validate() is False
    with pytest.raises(ValidationError):
        bad.require_valid()

    section = (
        InterpretationSectionBuilder()
        .for_interpreter(interpreter_id="x", section_type="x", context_id=pack.id)
        .build()
    )
    trace = InterpreterTrace().with_event("a").with_event("b", detail="d")
    assert trace.names() == ("a", "b")
    assert trace.validate() is True
    stats = ExecutionStatistics(duration_ms=1.5)
    assert stats.validate() is True
    result = FrameworkInterpreterResult(
        section=section,
        metadata=meta,
        trace=trace,
        confidence=50.0,
        statistics=stats,
        warnings=("w",),
    )
    assert result.validate() is True
    payload = result.to_payload()
    assert payload["section"] is section
    assert payload["warnings"] == ["w"]

    invalid = FrameworkInterpreterResult(
        section=section,
        metadata=meta,
        confidence=-5.0,
    )
    assert invalid.validate() is False
