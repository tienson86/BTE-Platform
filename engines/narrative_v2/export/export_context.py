"""Export context — ordered Presentation blocks. No new Meaning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ExportBlock:
    """One copied Presentation string. Field path is schema, not customer copy."""

    field: str
    text: str


@dataclass(frozen=True, slots=True)
class ExportContext:
    """Shared render input for every consumer. Immutable."""

    version: str
    status: str
    language: str
    blocks: tuple[ExportBlock, ...]
    presentation: Mapping[str, Any]
    shadow_mode: bool = True
    replaces_pack05: bool = False
