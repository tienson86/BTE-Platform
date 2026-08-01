"""Placeholder Engine binder — bind values to placeholder references.

Creates binding shells from refs + opaque values.
No interpretation.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.exceptions.placeholder_error import PlaceholderEngineError
from engines.interpretation_engine.placeholder_engine.formatter import Formatter
from engines.interpretation_engine.placeholder_engine.metadata import (
    PlaceholderBinding,
    PlaceholderRef,
    PlaceholderValue,
)
from engines.interpretation_engine.placeholder_engine.validator import Validator
from engines.interpretation_engine.utils.ids import new_id


class Binder:
    """Bind opaque values to placeholder references.

    Output is a ``PlaceholderBinding`` shell — never interpreted narrative.
    """

    def __init__(
        self,
        *,
        validator: Validator | None = None,
        formatter: Formatter | None = None,
    ) -> None:
        """Initialize binder collaborators."""
        self._validator = validator or Validator()
        self._formatter = formatter or Formatter(validator=self._validator)

    def bind(
        self,
        refs: tuple[PlaceholderRef, ...],
        values: Mapping[str, Any],
        *,
        binding_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        require_all_required: bool = True,
        allow_unknown: bool = False,
        format_values: bool = True,
    ) -> PlaceholderBinding:
        """Bind values to placeholders and optionally format them."""
        if not refs:
            raise PlaceholderEngineError("placeholder_refs_required")
        self._validator.assert_binding(
            refs,
            values,
            require_all_required=require_all_required,
            allow_unknown=allow_unknown,
        )

        bound: dict[str, PlaceholderValue] = {}
        for ref in refs:
            if ref.ref_id not in values:
                continue
            raw = values[ref.ref_id]
            if format_values:
                bound[ref.ref_id] = self._formatter.format_value(ref, raw)
            else:
                bound[ref.ref_id] = PlaceholderValue(
                    placeholder_ref_id=ref.ref_id,
                    raw_value=raw,
                    formatted_value=raw,
                    format_id="raw",
                    metadata={},
                )

        return PlaceholderBinding(
            binding_id=binding_id or new_id("phbind"),
            values=bound,
            metadata=dict(metadata or {}),
        )
