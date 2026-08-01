"""Immutable interpretation context architecture model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.final_analysis_input import FinalAnalysisInput


@dataclass(frozen=True, slots=True)
class InterpretationContextModel:
    """Architecture context contract built from Pack 02 final analysis input."""

    id: str
    version: str
    pipeline_id: str
    input: FinalAnalysisInput
    attributes: Mapping[str, Any] = field(default_factory=dict)
    trace: tuple[str, ...] = ()

    def validate(self) -> bool:
        """Validate structural context contract."""
        if not self.id or not self.pipeline_id or not self.version:
            return False
        return self.input.validate()
