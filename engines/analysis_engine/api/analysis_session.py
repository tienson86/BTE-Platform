"""Public Analysis API session contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping
from uuid import uuid4

from engines.analysis_engine.api.analysis_request import AnalysisRequest
from engines.analysis_engine.api.analysis_response import AnalysisResponse
from engines.analysis_engine.exceptions.runtime_error import AnalysisRuntimeError
from engines.analysis_engine.models.analysis_context import AnalysisContext


class AnalysisSessionStatus(str, Enum):
    """Lifecycle status for an analysis API session."""

    OPEN = "open"
    BOUND = "bound"
    SUBMITTED = "submitted"
    COMPLETED = "completed"
    CLOSED = "closed"
    FAILED = "failed"


@dataclass(slots=True)
class AnalysisSession:
    """Mutable public API session shell for one analysis interaction.

    Tracks request/context/response identifiers only.
    Does not implement analyzer business logic.
    """

    session_id: str = field(default_factory=lambda: str(uuid4()))
    pipeline_id: str | None = None
    status: AnalysisSessionStatus = AnalysisSessionStatus.OPEN
    request: AnalysisRequest | None = None
    context: AnalysisContext | None = None
    response: AnalysisResponse | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def bind_request(self, request: AnalysisRequest) -> None:
        """Bind a validated request to the session."""
        self._assert_not_closed()
        if not request.validate():
            raise AnalysisRuntimeError("analysis_request_invalid")
        self.request = request
        self.pipeline_id = request.pipeline_id
        if self.status == AnalysisSessionStatus.OPEN:
            self.status = AnalysisSessionStatus.BOUND

    def bind_context(self, context: AnalysisContext) -> None:
        """Bind an analysis context to the session."""
        self._assert_not_closed()
        self.context = context
        if self.pipeline_id is None:
            self.pipeline_id = context.pipeline_id
        if self.status in {AnalysisSessionStatus.OPEN, AnalysisSessionStatus.BOUND}:
            self.status = AnalysisSessionStatus.BOUND

    def mark_submitted(self) -> None:
        """Mark the session as submitted for analysis."""
        self._assert_not_closed()
        self.status = AnalysisSessionStatus.SUBMITTED

    def complete(self, response: AnalysisResponse) -> None:
        """Attach a response and mark the session completed or failed."""
        self._assert_not_closed()
        self.response = response
        self.status = (
            AnalysisSessionStatus.COMPLETED
            if response.success
            else AnalysisSessionStatus.FAILED
        )

    def close(self) -> None:
        """Close the session."""
        self.status = AnalysisSessionStatus.CLOSED

    def is_open(self) -> bool:
        """Return True when the session can still accept work."""
        return self.status not in {
            AnalysisSessionStatus.CLOSED,
            AnalysisSessionStatus.FAILED,
        }

    def describe(self) -> Mapping[str, Any]:
        """Return a public description of the session state."""
        return {
            "session_id": self.session_id,
            "pipeline_id": self.pipeline_id,
            "status": self.status.value,
            "request_id": None if self.request is None else self.request.request_id,
            "context_id": None if self.context is None else self.context.id,
            "response_status": (
                None if self.response is None else self.response.status.value
            ),
            "metadata": dict(self.metadata),
        }

    def _assert_not_closed(self) -> None:
        """Reject mutations after close."""
        if self.status == AnalysisSessionStatus.CLOSED:
            raise AnalysisRuntimeError("analysis_session_closed")
