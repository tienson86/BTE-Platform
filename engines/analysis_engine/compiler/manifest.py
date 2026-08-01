"""Analysis Engine compiler manifest model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CompilerManifest:
    """Public contract for a compiler package manifest."""

    manifest_id: str
    package_name: str
    version: str
    schema_version: str = "0.0.0"
    entries: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def entry_count(self) -> int:
        """Return the number of manifest entries."""
        raise NotImplementedError
