"""Analysis Engine compiler build context model."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class BuildContext:
    """Public contract for compiler build context."""

    build_id: str
    source_root: Path
    output_root: Path
    schema_version: str = "0.0.0"
    attributes: dict[str, Any] = field(default_factory=dict)
    input_paths: tuple[Path, ...] = ()

    def get_attribute(self, key: str) -> Any:
        """Return a build attribute by key."""
        raise NotImplementedError

    def set_attribute(self, key: str, value: Any) -> None:
        """Assign a build attribute by key."""
        raise NotImplementedError
