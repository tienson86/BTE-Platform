"""Interpretation output metadata model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.version_info import VersionInfo


@dataclass(frozen=True, slots=True)
class Metadata:
    """Immutable metadata contract for Pack 03 interpretation outputs.

    Holds governance/identity fields only. No report rendering content.
    """

    id: str
    version_info: VersionInfo
    created_at: str
    updated_at: str | None = None
    completed_at: str | None = None
    locale: str = ""
    tags: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate metadata structural integrity."""
        if not self.id or not self.created_at:
            return False
        return self.version_info.validate()
