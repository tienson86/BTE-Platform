"""Public interpretation request envelope."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.final_analysis_input import FinalAnalysisInput


@dataclass(frozen=True, slots=True)
class InterpretationRequest:
    """Request contract wrapping Pack 02 FinalAnalysisResult input only."""

    id: str
    version: str
    final_input: FinalAnalysisInput
    options: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate request structural contract."""
        if not self.id or not self.version:
            return False
        return self.final_input.validate()
