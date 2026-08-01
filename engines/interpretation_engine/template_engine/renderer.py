"""Template Engine renderer — produce binding/render shells.

Infrastructure renderer binds values to template references.
Does not render template prose. No hard-coded templates.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.exceptions.template_error import TemplateEngineError
from engines.interpretation_engine.template_engine.metadata import (
    TemplateBinding,
    TemplateRef,
    TemplateRenderShell,
)
from engines.interpretation_engine.template_engine.resolver import Resolver
from engines.interpretation_engine.template_engine.validator import Validator
from engines.interpretation_engine.utils.ids import new_id


class Renderer:
    """Produce ``TemplateRenderShell`` artifacts from refs + bindings.

    Output is a structural shell (ref + binding). Never generated text.
    """

    def __init__(
        self,
        *,
        resolver: Resolver | None = None,
        validator: Validator | None = None,
    ) -> None:
        """Initialize renderer collaborators."""
        self._resolver = resolver
        self._validator = validator or Validator()

    def render(
        self,
        ref: TemplateRef,
        values: Mapping[str, Any],
        *,
        render_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        require_all_slots: bool = True,
        allow_unknown_slots: bool = False,
    ) -> TemplateRenderShell:
        """Bind values to a template reference and return a render shell."""
        if not ref.validate():
            raise TemplateEngineError("template_ref_invalid")
        self._validator.assert_binding(
            ref,
            values,
            require_all_slots=require_all_slots,
            allow_unknown_slots=allow_unknown_slots,
        )
        binding = TemplateBinding(
            template_ref_id=ref.ref_id,
            values=dict(values),
            metadata={},
        )
        return TemplateRenderShell(
            render_id=render_id or new_id("trender"),
            template_ref=ref,
            binding=binding,
            status="bound",
            metadata=dict(metadata or {}),
        )

    def render_by_id(
        self,
        template_ref: str,
        values: Mapping[str, Any],
        *,
        render_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        require_all_slots: bool = True,
        allow_unknown_slots: bool = False,
    ) -> TemplateRenderShell:
        """Resolve a template ref id, then produce a render shell."""
        if self._resolver is None:
            raise TemplateEngineError("template_resolver_required")
        ref = self._resolver.resolve(template_ref)
        return self.render(
            ref,
            values,
            render_id=render_id,
            metadata=metadata,
            require_all_slots=require_all_slots,
            allow_unknown_slots=allow_unknown_slots,
        )

    def bind(
        self,
        template_ref: str,
        values: Mapping[str, Any],
    ) -> TemplateBinding:
        """Create a binding shell for a template reference id."""
        if not self._validator.validate_ref_id(template_ref):
            raise TemplateEngineError("template_ref_required")
        if self._resolver is not None:
            ref = self._resolver.resolve(template_ref)
            self._validator.assert_binding(ref, values)
        return TemplateBinding(
            template_ref_id=template_ref,
            values=dict(values),
            metadata={},
        )
