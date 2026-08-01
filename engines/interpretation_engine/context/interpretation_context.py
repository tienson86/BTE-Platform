"""Pack 03 Interpretation Context — immutable runtime context.

Built from Pack 02 FinalAnalysisResult / FinalResult only.
No BaZi interpretation logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult


@dataclass(frozen=True, slots=True)
class InterpretationContext:
    """Immutable Interpretation Context produced from Pack 02 final analysis.

    This is the Pack 03 architecture/runtime context.
    Legacy BaZi-field context remains under ``legacy_runtime.context``.
    """

    id: str
    version: str
    pipeline_id: str
    source_final_result_id: str
    final_result: FinalResult
    attributes: Mapping[str, Any] = field(default_factory=dict)
    trace: tuple[str, ...] = ()
    created_at: str = ""
    updated_at: str | None = None
    completed_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate structural integrity of the interpretation context."""
        if not self.id or not self.version or not self.pipeline_id:
            return False
        if not self.source_final_result_id or not self.created_at:
            return False
        if self.final_result is None:
            return False
        if self.final_result.id != self.source_final_result_id:
            return False
        return self.final_result.validate()
