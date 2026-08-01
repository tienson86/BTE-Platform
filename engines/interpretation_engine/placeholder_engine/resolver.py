"""Placeholder Engine resolver — resolve placeholder references.

Resolves placeholder ids against a caller-supplied catalog and optional
context attribute map. No interpretation.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from engines.interpretation_engine.exceptions.placeholder_error import PlaceholderEngineError
from engines.interpretation_engine.placeholder_engine.binder import Binder
from engines.interpretation_engine.placeholder_engine.formatter import Formatter
from engines.interpretation_engine.placeholder_engine.metadata import (
    Metadata,
    PlaceholderRef,
    PlaceholderResolution,
)
from engines.interpretation_engine.placeholder_engine.validator import Validator
from engines.interpretation_engine.utils.ids import new_id


class Resolver:
    """Resolve placeholder reference ids to refs and optional bindings.

    Context values are treated as opaque key/value attributes only.
    """

    def __init__(
        self,
        *,
        ref_provider: Callable[[], tuple[PlaceholderRef, ...]] | None = None,
        validator: Validator | None = None,
        binder: Binder | None = None,
        formatter: Formatter | None = None,
        metadata: Metadata | None = None,
    ) -> None:
        """Initialize resolver collaborators."""
        self._ref_provider = ref_provider or (lambda: ())
        self._validator = validator or Validator()
        self._formatter = formatter or Formatter(validator=self._validator)
        self._binder = binder or Binder(
            validator=self._validator,
            formatter=self._formatter,
        )
        self._metadata = metadata or Metadata()

    @property
    def validator(self) -> Validator:
        """Return the bound validator."""
        return self._validator

    @property
    def binder(self) -> Binder:
        """Return the bound binder."""
        return self._binder

    @property
    def formatter(self) -> Formatter:
        """Return the bound formatter."""
        return self._formatter

    @property
    def metadata(self) -> Metadata:
        """Return the bound metadata helper."""
        return self._metadata

    def resolve_ref(self, placeholder_id: str) -> PlaceholderRef:
        """Resolve a single placeholder reference by id."""
        if not self._validator.validate_ref_id(placeholder_id):
            raise PlaceholderEngineError("placeholder_id_required")
        for ref in self._ref_provider():
            if ref.ref_id == placeholder_id and self._validator.validate_ref(ref):
                return ref
        raise PlaceholderEngineError(f"placeholder_ref_not_found:{placeholder_id}")

    def resolve_refs(self, placeholders: tuple[str, ...]) -> tuple[PlaceholderRef, ...]:
        """Resolve many placeholder references, preserving request order."""
        if not self._validator.validate_ref_ids(placeholders):
            raise PlaceholderEngineError("placeholder_ids_invalid")
        index = {
            ref.ref_id: ref
            for ref in self._ref_provider()
            if self._validator.validate_ref(ref)
        }
        resolved: list[PlaceholderRef] = []
        missing: list[str] = []
        for placeholder_id in placeholders:
            ref = index.get(placeholder_id)
            if ref is None:
                missing.append(placeholder_id)
                continue
            resolved.append(ref)
        if missing:
            raise PlaceholderEngineError(
                f"placeholder_refs_not_found:{','.join(missing)}"
            )
        return tuple(resolved)

    def resolve(
        self,
        placeholders: tuple[str, ...],
        context: Mapping[str, Any] | None = None,
        *,
        bind: bool = True,
        allow_unknown: bool = False,
    ) -> PlaceholderResolution:
        """Resolve placeholder ids and optionally bind opaque context values.

        ``context`` may contain a nested ``values`` mapping or flat placeholder
        keys. No interpretation is performed on context contents.
        """
        refs = self.resolve_refs(placeholders)
        values = self._extract_values(context)
        binding = None
        if bind:
            # Only bind keys that correspond to requested placeholders.
            scoped = {
                key: values[key]
                for key in placeholders
                if key in values
            }
            binding = self._binder.bind(
                refs,
                scoped,
                require_all_required=False,
                allow_unknown=allow_unknown,
            )
        return PlaceholderResolution(
            resolution_id=new_id("phres"),
            placeholder_ids=placeholders,
            refs=refs,
            binding=binding,
            metadata={},
        )

    def resolve_metadata(self, placeholder_id: str) -> Mapping[str, object]:
        """Resolve normalized metadata for a placeholder reference."""
        return self._metadata.from_ref(self.resolve_ref(placeholder_id))

    def _extract_values(
        self,
        context: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        """Extract opaque placeholder values from a context mapping."""
        if context is None:
            return {}
        nested = context.get("values")
        if isinstance(nested, Mapping):
            return dict(nested)
        return {
            key: value
            for key, value in context.items()
            if key not in {"metadata", "attributes", "trace"}
        }
