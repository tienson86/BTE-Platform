"""Interpretation service facade contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engines.interpretation_engine.api.interpretation_request import InterpretationRequest
    from engines.interpretation_engine.api.interpretation_response import InterpretationResponse
    from engines.interpretation_engine.api.interpretation_session import InterpretationSession


class InterpretationService(ABC):
    """Service-layer facade contract. Orchestration only; no content logic."""

    @abstractmethod
    def interpret(self, request: InterpretationRequest) -> InterpretationResponse:
        """Run interpretation for a request."""

    @abstractmethod
    def validate_request(self, request: InterpretationRequest) -> bool:
        """Validate a public interpretation request."""

    @abstractmethod
    def open_session(self, *, pipeline_id: str | None = None) -> InterpretationSession:
        """Open an interpretation session."""

    @abstractmethod
    def close_session(self, session_id: str) -> None:
        """Close an interpretation session."""
