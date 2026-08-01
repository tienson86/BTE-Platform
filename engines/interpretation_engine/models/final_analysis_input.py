"""Input model wrapper contract for Pack 02 FinalAnalysisResult."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult


@dataclass(frozen=True, slots=True)
class FinalAnalysisInput:
    """Architecture input shell referencing Pack 02 final analysis result only."""

    id: str
    version: str
    final_result: FinalResult
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate structural input contract."""
        if not self.id or not self.version:
            return False
        if self.final_result is None:
            return False
        return True
