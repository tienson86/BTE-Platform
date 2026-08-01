"""Tests for Pack 03 Interpreter Framework — exceptions, metadata, capability."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.interpreter_framework import (
    ConfigurationError,
    DependencyError,
    ExecutionError,
    InterpreterCapability,
    InterpreterError,
    InterpreterMetadata,
    ValidationError,
)


def test_exception_hierarchy_and_codes() -> None:
    """Framework exceptions expose stable codes."""
    base = InterpreterError("x")
    assert base.code == "interpreter_error"
    assert str(base) == "x"

    assert ValidationError("v").code == "validation_error"
    assert DependencyError("d").code == "dependency_error"
    assert ExecutionError("e").code == "execution_error"
    assert ConfigurationError("c").code == "configuration_error"
    assert issubclass(ValidationError, InterpreterError)


def test_metadata_validate_and_to_dict() -> None:
    """Metadata validates and serializes."""
    meta = InterpreterMetadata(
        interpreter_id="a",
        version="1.0.0",
        category="test",
        description="d",
        attributes={"k": 1},
    )
    assert meta.validate() is True
    assert meta.to_dict()["interpreter_id"] == "a"
    assert InterpreterMetadata(interpreter_id="", version="1").validate() is False
    assert InterpreterMetadata(interpreter_id="a", version="").validate() is False


def test_capability_validate_overlap_and_require() -> None:
    """Capability rejects overlapping required/optional deps."""
    ok = InterpreterCapability(
        interpreter_id="x",
        category="c",
        priority=10,
        dependencies=("a",),
        optional_dependencies=("b",),
        version="1.0.0",
    )
    assert ok.validate() is True
    ok.require_valid()
    assert "dependencies" in ok.to_dict()

    bad = InterpreterCapability(
        interpreter_id="x",
        category="c",
        priority=10,
        dependencies=("a",),
        optional_dependencies=("a",),
    )
    assert bad.validate() is False
    with pytest.raises(ConfigurationError):
        bad.require_valid()

    assert InterpreterCapability(
        interpreter_id="", category="c", priority=1
    ).validate() is False
    assert InterpreterCapability(
        interpreter_id="x", category="", priority=1
    ).validate() is False
