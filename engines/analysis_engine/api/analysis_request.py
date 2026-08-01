"""Public Analysis API request contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class AnalysisRequest:
    """Immutable public API request for an analysis run.

    Facade contract only. Does not encode BaZi business rules.
    """

    pipeline_id: str
    request_id: str = field(default_factory=lambda: str(uuid4()))
    chart_id: str | None = None
    context_id: str | None = None
    session_id: str | None = None
    version: str = "1.0.0"
    attributes: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)
    finalize: bool = False

    def validate(self) -> bool:
        """Validate structural request fields only."""
        if not self.pipeline_id:
            return False
        if not self.request_id:
            return False
        if not self.version:
            return False
        return True
