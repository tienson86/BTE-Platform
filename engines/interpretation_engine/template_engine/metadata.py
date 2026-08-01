"""Template Engine metadata models.

Describes template *references* and binding shells only.
No template bodies. No hard-coded templates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.exceptions.template_error import TemplateEngineError


@dataclass(frozen=True, slots=True)
class TemplateRef:
    """Immutable identifier for a template reference.

    Holds structural identity and slot names only — never template body text.
    """

    ref_id: str
    version: str = "0.0.0"
    domain: str = ""
    section: str = ""
    locale: str = ""
    status: str = "draft"
    slot_names: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate structural template reference integrity."""
        if not self.ref_id or not self.version:
            return False
        if any(not name for name in self.slot_names):
            return False
        return True


@dataclass(frozen=True, slots=True)
class TemplateBinding:
    """Bound values keyed by declared slot names.

    Values are opaque infrastructure payloads — not rendered text.
    """

    template_ref_id: str
    values: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate binding structural integrity."""
        return bool(self.template_ref_id)


@dataclass(frozen=True, slots=True)
class TemplateRenderShell:
    """Render shell produced by infrastructure renderer.

    Contains reference id + binding only — never generated template prose.
    """

    render_id: str
    template_ref: TemplateRef
    binding: TemplateBinding
    status: str = "bound"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate render shell structural integrity."""
        if not self.render_id:
            return False
        if self.binding.template_ref_id != self.template_ref.ref_id:
            return False
        return self.template_ref.validate() and self.binding.validate()


class Metadata:
    """Normalize template-reference metadata without loading templates."""

    def from_ref(self, ref: TemplateRef) -> dict[str, Any]:
        """Return a normalized metadata dictionary for a template reference."""
        metadata = dict(ref.metadata)
        metadata.setdefault("ref_id", ref.ref_id)
        metadata.setdefault("version", ref.version)
        metadata.setdefault("domain", ref.domain)
        metadata.setdefault("section", ref.section)
        metadata.setdefault("locale", ref.locale)
        metadata.setdefault("status", ref.status)
        metadata.setdefault("slot_names", list(ref.slot_names))
        metadata.setdefault("tags", list(ref.tags))
        return metadata

    def from_binding(self, binding: TemplateBinding) -> dict[str, Any]:
        """Return normalized metadata for a binding shell."""
        metadata = dict(binding.metadata)
        metadata.setdefault("template_ref_id", binding.template_ref_id)
        metadata.setdefault("slot_keys", list(binding.values.keys()))
        return metadata

    def from_render_shell(self, shell: TemplateRenderShell) -> dict[str, Any]:
        """Return normalized metadata for a render shell."""
        metadata = dict(shell.metadata)
        metadata.setdefault("render_id", shell.render_id)
        metadata.setdefault("template_ref_id", shell.template_ref.ref_id)
        metadata.setdefault("status", shell.status)
        return metadata

    def from_mapping(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        """Extract metadata from a flat or nested template-ref mapping."""
        if "metadata" in payload and isinstance(payload["metadata"], Mapping):
            metadata = dict(payload["metadata"])
            for key in ("ref_id", "version", "domain", "section", "locale", "status"):
                if key in payload and key not in metadata:
                    metadata[key] = payload[key]
            return metadata
        if "ref_id" in payload or "template_ref_id" in payload or "render_id" in payload:
            return dict(payload)
        raise TemplateEngineError("template_metadata_payload_unsupported")
