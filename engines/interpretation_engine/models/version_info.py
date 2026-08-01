"""Interpretation output version information model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VersionInfo:
    """Immutable version contract for Pack 03 interpretation outputs.

    Describes schema/engine version labels only. No report rendering.
    """

    schema_version: str
    engine_version: str = "0.0.0-architecture"
    model_version: str = "1.0.0"

    def validate(self) -> bool:
        """Validate version information structural integrity."""
        return bool(self.schema_version and self.engine_version and self.model_version)
