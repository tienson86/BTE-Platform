"""Architecture tests for placeholder engine infrastructure."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.exceptions import PlaceholderEngineError
from engines.interpretation_engine.placeholder_engine import (
    Binder,
    Formatter,
    PlaceholderEngine,
    PlaceholderRef,
    Resolver,
    Validator,
)


def _catalog() -> tuple[PlaceholderRef, ...]:
    """Build a small in-memory placeholder-ref catalog."""
    return (
        PlaceholderRef(
            ref_id="ph_day_master",
            domain="chart",
            value_type="string",
            format_id="string",
            required=True,
            status="active",
        ),
        PlaceholderRef(
            ref_id="ph_score",
            domain="score",
            value_type="int",
            format_id="raw",
            required=False,
            status="active",
        ),
        PlaceholderRef(
            ref_id="ph_flag",
            domain="flags",
            value_type="bool",
            format_id="identity",
            required=False,
            status="active",
        ),
    )


def test_validator_checks_types_and_required() -> None:
    """Validator enforces structural types without interpretation."""
    refs = _catalog()
    validator = Validator()
    assert validator.validate_binding(refs, {"ph_day_master": "Jia"}) is True
    assert validator.validate_binding(refs, {"ph_day_master": 1}) is False
    assert validator.validate_binding(refs, {}) is False
    with pytest.raises(PlaceholderEngineError, match="placeholder_binding_invalid"):
        validator.assert_binding(refs, {"ph_day_master": "Jia", "unknown": 1})


def test_formatter_string_and_raw() -> None:
    """Formatter applies structural format ids only."""
    formatter = Formatter()
    day = _catalog()[0]
    score = _catalog()[1]
    formatted_day = formatter.format_value(day, "Jia")
    assert formatted_day.formatted_value == "Jia"
    assert formatted_day.format_id == "string"
    formatted_score = formatter.format_value(score, 12)
    assert formatted_score.formatted_value == 12
    assert formatted_score.format_id == "raw"


def test_binder_builds_binding_shell() -> None:
    """Binder produces binding shells from opaque values."""
    binder = Binder()
    binding = binder.bind(
        _catalog(),
        {"ph_day_master": "Yi", "ph_score": 7},
    )
    assert binding.validate() is True
    assert binding.values["ph_day_master"].formatted_value == "Yi"
    assert binding.values["ph_score"].raw_value == 7


def test_resolver_resolves_and_binds_context() -> None:
    """Resolver hydrates refs and binds opaque context values."""
    resolver = Resolver(ref_provider=_catalog)
    resolution = resolver.resolve(
        ("ph_day_master", "ph_score"),
        {"values": {"ph_day_master": "Bing", "ph_score": 3}},
    )
    assert resolution.validate() is True
    assert resolution.placeholder_ids == ("ph_day_master", "ph_score")
    assert resolution.binding is not None
    assert resolution.binding.values["ph_day_master"].formatted_value == "Bing"
    with pytest.raises(PlaceholderEngineError, match="placeholder_ref_not_found"):
        resolver.resolve_ref("missing")


def test_placeholder_engine_facade() -> None:
    """Facade resolves placeholders without interpretation."""
    engine = PlaceholderEngine(catalog=_catalog())
    resolution = engine.resolve(
        ("ph_day_master", "ph_flag"),
        {"ph_day_master": "Ding", "ph_flag": True},
    )
    assert resolution.binding is not None
    assert resolution.binding.values["ph_flag"].formatted_value is True
    assert engine.validate(("ph_day_master",)) is True
    assert engine.validate(("",)) is False
