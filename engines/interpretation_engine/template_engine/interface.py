"""Template binding interface. No hard-coded templates. Infrastructure only."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping

from engines.interpretation_engine.template_engine.loader import Loader
from engines.interpretation_engine.template_engine.metadata import (
    TemplateBinding,
    TemplateRef,
    TemplateRenderShell,
)
from engines.interpretation_engine.template_engine.renderer import Renderer
from engines.interpretation_engine.template_engine.resolver import Resolver
from engines.interpretation_engine.template_engine.validator import Validator


class TemplateEngineInterface(ABC):
    """Template binding interface over references only.

    Implementations must not embed template bodies or hard-coded templates.
    """

    @abstractmethod
    def bind(self, template_ref: str, values: Mapping[str, Any]) -> TemplateBinding:
        """Bind values to a template reference."""

    @abstractmethod
    def validate(self, template_ref: str) -> bool:
        """Validate template reference identifier structure."""


class TemplateEngine(TemplateEngineInterface):
    """Default Template Engine facade over loader/resolver/validator/renderer.

    Infrastructure only — no template library, no prose rendering.
    """

    def __init__(
        self,
        *,
        catalog: tuple[TemplateRef, ...] = (),
    ) -> None:
        """Initialize with an optional in-memory template-ref catalog."""
        self._catalog = catalog
        self._loader = Loader()
        self._validator = Validator()
        self._resolver = Resolver(
            ref_provider=lambda: self._catalog,
            loader=self._loader,
        )
        self._renderer = Renderer(
            resolver=self._resolver,
            validator=self._validator,
        )

    @property
    def loader(self) -> Loader:
        """Return the bound loader."""
        return self._loader

    @property
    def resolver(self) -> Resolver:
        """Return the bound resolver."""
        return self._resolver

    @property
    def validator(self) -> Validator:
        """Return the bound validator."""
        return self._validator

    @property
    def renderer(self) -> Renderer:
        """Return the bound renderer."""
        return self._renderer

    def set_catalog(self, catalog: tuple[TemplateRef, ...]) -> None:
        """Replace the in-memory template-ref catalog."""
        self._catalog = catalog

    def bind(self, template_ref: str, values: Mapping[str, Any]) -> TemplateBinding:
        """Bind values to a template reference (no prose output)."""
        return self._renderer.bind(template_ref, values)

    def validate(self, template_ref: str) -> bool:
        """Validate template reference id and optional catalog presence."""
        from engines.interpretation_engine.exceptions.template_error import TemplateEngineError

        if not self._validator.validate_ref_id(template_ref):
            return False
        if not self._catalog:
            return True
        try:
            ref = self._resolver.resolve(template_ref)
        except TemplateEngineError:
            return False
        return self._validator.validate_ref(ref)

    def render(
        self,
        template_ref: str,
        values: Mapping[str, Any],
    ) -> TemplateRenderShell:
        """Produce a render shell for a template reference (no prose)."""
        return self._renderer.render_by_id(template_ref, values)
