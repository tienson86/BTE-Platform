"""Placeholder Engine formatter — format bound placeholder values.

Applies structural format ids only (raw/string/identity).
No interpretation. No natural language generation.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.exceptions.placeholder_error import PlaceholderEngineError
from engines.interpretation_engine.placeholder_engine.metadata import (
    PlaceholderRef,
    PlaceholderValue,
)
from engines.interpretation_engine.placeholder_engine.validator import Validator


class Formatter:
    """Format opaque placeholder values into structural shells.

    Supported format ids: ``raw``, ``string``, ``identity``.
    Does not interpret BaZi meaning or produce narrative text.
    """

    def __init__(self, *, validator: Validator | None = None) -> None:
        """Initialize formatter with an optional validator."""
        self._validator = validator or Validator()

    def format_value(self, ref: PlaceholderRef, raw_value: Any) -> PlaceholderValue:
        """Format a single raw value according to the placeholder ref format_id."""
        if not self._validator.validate_ref(ref):
            raise PlaceholderEngineError(f"placeholder_ref_invalid:{ref.ref_id}")
        if not self._validator.validate_value(ref, raw_value):
            raise PlaceholderEngineError(
                f"placeholder_value_type_invalid:{ref.ref_id}:{ref.value_type}"
            )

        format_id = ref.format_id or "raw"
        if format_id == "raw" or format_id == "identity":
            formatted: Any = raw_value
        elif format_id == "string":
            formatted = "" if raw_value is None else str(raw_value)
        else:
            raise PlaceholderEngineError(f"placeholder_format_unsupported:{format_id}")

        return PlaceholderValue(
            placeholder_ref_id=ref.ref_id,
            raw_value=raw_value,
            formatted_value=formatted,
            format_id=format_id,
            metadata={},
        )

    def format_many(
        self,
        refs: tuple[PlaceholderRef, ...],
        values: dict[str, Any],
    ) -> tuple[PlaceholderValue, ...]:
        """Format many values, preserving ref order."""
        index = {ref.ref_id: ref for ref in refs}
        formatted: list[PlaceholderValue] = []
        for ref in refs:
            if ref.ref_id not in values:
                if ref.required:
                    raise PlaceholderEngineError(
                        f"placeholder_value_missing:{ref.ref_id}"
                    )
                continue
            formatted.append(self.format_value(ref, values[ref.ref_id]))
        # Ignore unknown keys here; binder/validator enforce unknown policy.
        _ = index
        return tuple(formatted)
