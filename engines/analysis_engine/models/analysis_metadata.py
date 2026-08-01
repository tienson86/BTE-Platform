"""Analysis metadata model skeleton."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AnalysisMetadata:
    """Metadata contract for analysis context and results."""

    schema_version: str
    engine_version: str
    source: str | None = None
    tags: tuple[str, ...] = ()
