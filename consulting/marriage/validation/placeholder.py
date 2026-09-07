"""Validation placeholder. No business validation rules in TV1-B01."""

from __future__ import annotations

from consulting.marriage.adapters.contract import CanonicalAnalysis
from consulting.marriage.dto.request import MarriageConsultationRequest
from consulting.marriage.models.evidence import MarriageEvidence
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.validation.contract import MarriageValidationContract


class PlaceholderMarriageValidation(MarriageValidationContract):
    """Skeleton placeholder. Does not execute validation rules."""

    def validate_request(self, request: MarriageConsultationRequest) -> None:
        """Refuse request validation."""
        raise NotImplementedError("TV1-B01: validation is not implemented")

    def validate_canonical_contract(
        self,
        analysis_a: CanonicalAnalysis,
        analysis_b: CanonicalAnalysis,
    ) -> None:
        """Refuse canonical contract validation."""
        raise NotImplementedError("TV1-B01: validation is not implemented")

    def validate_evidence(self, evidence: list[MarriageEvidence]) -> None:
        """Refuse evidence validation."""
        raise NotImplementedError("TV1-B01: validation is not implemented")

    def validate_decision(self, result: MarriageDecisionResult) -> None:
        """Refuse decision validation."""
        raise NotImplementedError("TV1-B01: validation is not implemented")
