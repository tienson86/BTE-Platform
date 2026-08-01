"""Placeholder Engine validator — validate placeholder refs and bindings.

Structural validation only. No interpretation.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.exceptions.placeholder_error import PlaceholderEngineError
from engines.interpretation_engine.placeholder_engine.metadata import (
    PlaceholderBinding,
    PlaceholderRef,
    PlaceholderResolution,
    PlaceholderValue,
)

_SUPPORTED_VALUE_TYPES: frozenset[str] = frozenset(
    {
        "string",
        "int",
        "float",
        "bool",
        "ref",
        "raw",
    }
)
_SUPPORTED_FORMAT_IDS: frozenset[str] = frozenset(
    {
        "raw",
        "string",
        "identity",
    }
)


class Validator:
    """Validate placeholder reference and binding infrastructure contracts."""

    def validate_ref_id(self, placeholder_id: str) -> bool:
        """Validate that a placeholder id is a non-empty string."""
        return isinstance(placeholder_id, str) and bool(placeholder_id.strip())

    def validate_ref_ids(self, placeholders: tuple[str, ...]) -> bool:
        """Validate a tuple of placeholder identifiers."""
        if not placeholders:
            return False
        return all(self.validate_ref_id(item) for item in placeholders)

    def validate_ref(self, ref: PlaceholderRef) -> bool:
        """Validate a placeholder reference descriptor."""
        if not ref.validate():
            return False
        if ref.value_type not in _SUPPORTED_VALUE_TYPES:
            return False
        if ref.format_id not in _SUPPORTED_FORMAT_IDS:
            return False
        return True

    def validate_value(self, ref: PlaceholderRef, value: Any) -> bool:
        """Validate a raw value against the declared value_type (structural)."""
        if value is None:
            return not ref.required
        if ref.value_type == "string":
            return isinstance(value, str)
        if ref.value_type == "int":
            return isinstance(value, int) and not isinstance(value, bool)
        if ref.value_type == "float":
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        if ref.value_type == "bool":
            return isinstance(value, bool)
        if ref.value_type in {"ref", "raw"}:
            return True
        return False

    def validate_binding(
        self,
        refs: tuple[PlaceholderRef, ...],
        values: Mapping[str, Any],
        *,
        require_all_required: bool = True,
        allow_unknown: bool = False,
    ) -> bool:
        """Validate opaque values against placeholder refs."""
        index = {ref.ref_id: ref for ref in refs}
        if require_all_required:
            for ref in refs:
                if ref.required and ref.ref_id not in values:
                    return False
        if not allow_unknown:
            for key in values:
                if key not in index:
                    return False
        for key, raw in values.items():
            ref = index.get(key)
            if ref is None:
                continue
            if not self.validate_value(ref, raw):
                return False
        return True

    def validate_binding_object(self, binding: PlaceholderBinding) -> bool:
        """Validate a binding object shell."""
        return binding.validate()

    def validate_resolution(self, resolution: PlaceholderResolution) -> bool:
        """Validate a resolution shell."""
        return resolution.validate()

    def assert_binding(
        self,
        refs: tuple[PlaceholderRef, ...],
        values: Mapping[str, Any],
        *,
        require_all_required: bool = True,
        allow_unknown: bool = False,
    ) -> None:
        """Raise when binding values violate placeholder contracts."""
        if not self.validate_binding(
            refs,
            values,
            require_all_required=require_all_required,
            allow_unknown=allow_unknown,
        ):
            declared = {ref.ref_id for ref in refs}
            required = {ref.ref_id for ref in refs if ref.required}
            provided = set(values.keys())
            missing = tuple(sorted(required - provided))
            unknown = tuple(sorted(provided - declared))
            raise PlaceholderEngineError(
                f"placeholder_binding_invalid:missing={missing}:unknown={unknown}"
            )

    def assert_value_shell(self, value: PlaceholderValue) -> None:
        """Raise when a value shell is structurally invalid."""
        if not value.validate():
            raise PlaceholderEngineError(
                f"placeholder_value_invalid:{value.placeholder_ref_id}"
            )
