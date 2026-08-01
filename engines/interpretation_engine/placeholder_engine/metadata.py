"""Placeholder Engine metadata models.

Describes placeholder *references*, bindings, and formatted value shells.
No interpretation logic. No hard-coded narrative content.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.exceptions.placeholder_error import PlaceholderEngineError


@dataclass(frozen=True, slots=True)
class PlaceholderRef:
    """Immutable identifier for a placeholder reference.

    Declares structural identity and value type hints only.
    """

    ref_id: str
    version: str = "0.0.0"
    domain: str = ""
    value_type: str = "string"
    format_id: str = "raw"
    required: bool = True
    status: str = "draft"
    tags: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate structural placeholder reference integrity."""
        return bool(self.ref_id and self.version and self.value_type)


@dataclass(frozen=True, slots=True)
class PlaceholderValue:
    """Opaque placeholder value shell before/after formatting."""

    placeholder_ref_id: str
    raw_value: Any = None
    formatted_value: Any = None
    format_id: str = "raw"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate value shell structural integrity."""
        return bool(self.placeholder_ref_id)


@dataclass(frozen=True, slots=True)
class PlaceholderBinding:
    """Binding of placeholder refs to opaque values."""

    binding_id: str
    values: Mapping[str, PlaceholderValue] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate binding structural integrity."""
        if not self.binding_id:
            return False
        return all(value.validate() for value in self.values.values())


@dataclass(frozen=True, slots=True)
class PlaceholderResolution:
    """Resolution result for a set of placeholder references."""

    resolution_id: str
    placeholder_ids: tuple[str, ...] = ()
    refs: tuple[PlaceholderRef, ...] = ()
    binding: PlaceholderBinding | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate resolution structural integrity."""
        if not self.resolution_id:
            return False
        if self.refs and self.placeholder_ids:
            ref_ids = tuple(ref.ref_id for ref in self.refs)
            if ref_ids != self.placeholder_ids:
                return False
        if self.binding is not None and not self.binding.validate():
            return False
        return True


class Metadata:
    """Normalize placeholder metadata without interpretation."""

    def from_ref(self, ref: PlaceholderRef) -> dict[str, Any]:
        """Return a normalized metadata dictionary for a placeholder reference."""
        metadata = dict(ref.metadata)
        metadata.setdefault("ref_id", ref.ref_id)
        metadata.setdefault("version", ref.version)
        metadata.setdefault("domain", ref.domain)
        metadata.setdefault("value_type", ref.value_type)
        metadata.setdefault("format_id", ref.format_id)
        metadata.setdefault("required", ref.required)
        metadata.setdefault("status", ref.status)
        metadata.setdefault("tags", list(ref.tags))
        return metadata

    def from_binding(self, binding: PlaceholderBinding) -> dict[str, Any]:
        """Return normalized metadata for a binding shell."""
        metadata = dict(binding.metadata)
        metadata.setdefault("binding_id", binding.binding_id)
        metadata.setdefault("placeholder_ids", list(binding.values.keys()))
        return metadata

    def from_mapping(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        """Extract metadata from a flat or nested placeholder mapping."""
        if "metadata" in payload and isinstance(payload["metadata"], Mapping):
            metadata = dict(payload["metadata"])
            for key in ("ref_id", "version", "domain", "value_type", "format_id"):
                if key in payload and key not in metadata:
                    metadata[key] = payload[key]
            return metadata
        if "ref_id" in payload or "binding_id" in payload or "resolution_id" in payload:
            return dict(payload)
        raise PlaceholderEngineError("placeholder_metadata_payload_unsupported")
