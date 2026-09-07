"""Public API contract. Resource surface only. No endpoint implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from consulting.marriage.dto.history import MarriageHistoryRecord
from consulting.marriage.dto.request import MarriageConsultationRequest
from consulting.marriage.dto.response import MarriageConsultationSummary, MarriageRuntimeResponse
from consulting.marriage.models.result import MarriageDecisionResult


class MarriageApiContract(ABC):
    """Public API contract for TV-01. Follows COMMON API Pattern."""

    @abstractmethod
    def create_consultation(
        self,
        request: MarriageConsultationRequest,
    ) -> MarriageRuntimeResponse:
        """POST /api/v1/consulting/marriage"""

    @abstractmethod
    def get_consultation(self, consultation_id: str) -> MarriageDecisionResult:
        """GET /api/v1/consulting/marriage/{consultation_id}"""

    @abstractmethod
    def get_summary(self, consultation_id: str) -> MarriageConsultationSummary:
        """GET /api/v1/consulting/marriage/{consultation_id}/summary"""

    @abstractmethod
    def get_report(self, consultation_id: str) -> MarriageDecisionResult:
        """GET /api/v1/consulting/marriage/{consultation_id}/report"""

    @abstractmethod
    def list_history(self) -> list[MarriageHistoryRecord]:
        """GET /api/v1/consulting/marriage/history"""
