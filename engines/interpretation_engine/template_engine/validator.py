"""Template Engine validator — validate template refs and bindings.

Validates structural contracts only.
No template body validation. No hard-coded templates.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.exceptions.template_error import TemplateEngineError
from engines.interpretation_engine.template_engine.metadata import (
    TemplateBinding,
    TemplateRef,
    TemplateRenderShell,
)


class Validator:
    """Validate template reference and binding infrastructure contracts."""

    def validate_ref_id(self, template_ref: str) -> bool:
        """Validate that a template reference id is a non-empty string."""
        return isinstance(template_ref, str) and bool(template_ref.strip())

    def validate_ref(self, ref: TemplateRef) -> bool:
        """Validate a template reference descriptor."""
        return ref.validate()

    def validate_binding(
        self,
        ref: TemplateRef,
        values: Mapping[str, Any],
        *,
        require_all_slots: bool = True,
        allow_unknown_slots: bool = False,
    ) -> bool:
        """Validate binding values against declared slot names."""
        if not ref.validate():
            return False
        declared = set(ref.slot_names)
        provided = set(values.keys())
        if require_all_slots and not declared.issubset(provided):
            return False
        if not allow_unknown_slots and not provided.issubset(declared):
            return False
        return True

    def validate_binding_object(
        self,
        ref: TemplateRef,
        binding: TemplateBinding,
        *,
        require_all_slots: bool = True,
        allow_unknown_slots: bool = False,
    ) -> bool:
        """Validate a binding object against a template reference."""
        if binding.template_ref_id != ref.ref_id:
            return False
        if not binding.validate():
            return False
        return self.validate_binding(
            ref,
            binding.values,
            require_all_slots=require_all_slots,
            allow_unknown_slots=allow_unknown_slots,
        )

    def validate_render_shell(self, shell: TemplateRenderShell) -> bool:
        """Validate a render shell structural contract."""
        return shell.validate()

    def assert_binding(
        self,
        ref: TemplateRef,
        values: Mapping[str, Any],
        *,
        require_all_slots: bool = True,
        allow_unknown_slots: bool = False,
    ) -> None:
        """Raise when binding values violate the template ref contract."""
        if not self.validate_binding(
            ref,
            values,
            require_all_slots=require_all_slots,
            allow_unknown_slots=allow_unknown_slots,
        ):
            declared = set(ref.slot_names)
            provided = set(values.keys())
            missing = tuple(sorted(declared - provided))
            unknown = tuple(sorted(provided - declared))
            raise TemplateEngineError(
                f"template_binding_invalid:missing={missing}:unknown={unknown}"
            )
