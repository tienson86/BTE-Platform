"""Placeholder resolution interface. Infrastructure only. No interpretation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping

from engines.interpretation_engine.placeholder_engine.binder import Binder
from engines.interpretation_engine.placeholder_engine.formatter import Formatter
from engines.interpretation_engine.placeholder_engine.metadata import (
    PlaceholderRef,
    PlaceholderResolution,
)
from engines.interpretation_engine.placeholder_engine.resolver import Resolver
from engines.interpretation_engine.placeholder_engine.validator import Validator


class PlaceholderEngineInterface(ABC):
    """Placeholder resolution interface over references only.

    Implementations must not perform BaZi interpretation.
    """

    @abstractmethod
    def resolve(
        self,
        placeholders: tuple[str, ...],
        context: Mapping[str, Any] | None = None,
    ) -> PlaceholderResolution:
        """Resolve placeholder refs against opaque context values."""

    @abstractmethod
    def validate(self, placeholders: tuple[str, ...]) -> bool:
        """Validate placeholder reference identifier structure."""


class PlaceholderEngine(PlaceholderEngineInterface):
    """Default Placeholder Engine facade over resolver/binder/formatter/validator.

    Infrastructure only — no interpretation.
    """

    def __init__(
        self,
        *,
        catalog: tuple[PlaceholderRef, ...] = (),
    ) -> None:
        """Initialize with an optional in-memory placeholder-ref catalog."""
        self._catalog = catalog
        self._validator = Validator()
        self._formatter = Formatter(validator=self._validator)
        self._binder = Binder(validator=self._validator, formatter=self._formatter)
        self._resolver = Resolver(
            ref_provider=lambda: self._catalog,
            validator=self._validator,
            binder=self._binder,
            formatter=self._formatter,
        )

    @property
    def resolver(self) -> Resolver:
        """Return the bound resolver."""
        return self._resolver

    @property
    def binder(self) -> Binder:
        """Return the bound binder."""
        return self._binder

    @property
    def formatter(self) -> Formatter:
        """Return the bound formatter."""
        return self._formatter

    @property
    def validator(self) -> Validator:
        """Return the bound validator."""
        return self._validator

    def set_catalog(self, catalog: tuple[PlaceholderRef, ...]) -> None:
        """Replace the in-memory placeholder-ref catalog."""
        self._catalog = catalog

    def resolve(
        self,
        placeholders: tuple[str, ...],
        context: Mapping[str, Any] | None = None,
    ) -> PlaceholderResolution:
        """Resolve placeholder refs against opaque context values."""
        return self._resolver.resolve(placeholders, context)

    def validate(self, placeholders: tuple[str, ...]) -> bool:
        """Validate placeholder reference ids and optional catalog presence."""
        from engines.interpretation_engine.exceptions.placeholder_error import (
            PlaceholderEngineError,
        )

        if not self._validator.validate_ref_ids(placeholders):
            return False
        if not self._catalog:
            return True
        try:
            refs = self._resolver.resolve_refs(placeholders)
        except PlaceholderEngineError:
            return False
        return all(self._validator.validate_ref(ref) for ref in refs)
