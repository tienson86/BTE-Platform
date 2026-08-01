"""Public interpretation response envelope."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from engines.interpretation_engine.models.interpretation_result_model import (
    InterpretationResultModel,
)


class InterpretationResponseStatus(str, Enum):
    """Response status codes for the public API facade."""

    SUCCESS = "success"
    FAILURE = "failure"
    INVALID = "invalid"
    NOT_IMPLEMENTED = "not_implemented"


@dataclass(frozen=True, slots=True)
class InterpretationResponse:
    """Response contract for Pack 03 public API."""

    id: str
    status: InterpretationResponseStatus
    result: InterpretationResultModel | None = None
    errors: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate response structural contract."""
        if not self.id:
            return False
        if self.status == InterpretationResponseStatus.SUCCESS and self.result is None:
            return False
        return True
