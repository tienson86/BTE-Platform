"""Public Analysis API response contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.final_result import FinalResult


class AnalysisResponseStatus(str, Enum):
    """Public API response status values."""

    ACCEPTED = "accepted"
    COMPLETED = "completed"
    FINALIZED = "finalized"
    FAILED = "failed"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True)
class AnalysisResponse:
    """Immutable public API response for an analysis run.

    Facade contract only. Does not generate interpretive report content.
    """

    request_id: str
    success: bool
    status: AnalysisResponseStatus
    session_id: str | None = None
    pipeline_id: str | None = None
    context_id: str | None = None
    analysis_result: AnalysisResult | None = None
    final_result: FinalResult | None = None
    errors: tuple[str, ...] = ()
    messages: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate structural response fields only."""
        if not self.request_id:
            return False
        if self.success and self.status == AnalysisResponseStatus.FAILED:
            return False
        if not self.success and self.status == AnalysisResponseStatus.COMPLETED:
            return False
        return True
