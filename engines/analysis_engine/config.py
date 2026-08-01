"""Analysis Engine configuration skeleton."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AnalysisEngineConfig:
    """Configuration container for the Analysis Engine architecture layer."""

    enabled: bool = True
    deterministic: bool = True
    schema_version: str = "0.0.0"
