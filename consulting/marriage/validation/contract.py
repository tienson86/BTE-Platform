"""Marriage validation contract. Business validation only. Does not change COMMON."""

from __future__ import annotations

from abc import ABC, abstractmethod

from consulting.marriage.adapters.contract import CanonicalAnalysis
from consulting.marriage.dto.request import MarriageConsultationRequest
from consulting.marriage.models.evidence import MarriageEvidence
from consulting.marriage.models.result import MarriageDecisionResult


class MarriageValidationContract(ABC):
    """TV-01 business validation. Must not replace COMMON Validation."""

    @abstractmethod
    def validate_request(self, request: MarriageConsultationRequest) -> None:
        """Validate a marriage consultation request."""

    @abstractmethod
    def validate_canonical_contract(
        self,
        analysis_a: CanonicalAnalysis,
        analysis_b: CanonicalAnalysis,
    ) -> None:
        """Validate Canonical analysis contracts before TV-01 reads them."""

    @abstractmethod
    def validate_evidence(self, evidence: list[MarriageEvidence]) -> None:
        """Validate evidence atoms and source traces."""

    @abstractmethod
    def validate_decision(self, result: MarriageDecisionResult) -> None:
        """Validate a factual decision before narrative or presentation."""
