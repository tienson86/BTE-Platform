"""Analysis decision validator interface.

No validation logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.models.analysis_decision import AnalysisDecision
from engines.analysis_engine.models.analysis_evidence import AnalysisEvidence
from engines.analysis_engine.validation.validator_contract import ValidatorContract


class DecisionValidator(ValidatorContract, ABC):
    """Public interface for validating analysis decision contracts."""

    @abstractmethod
    def validate_decision(self, decision: AnalysisDecision) -> bool:
        """Validate an analysis decision instance."""

    @abstractmethod
    def validate_evidence(self, evidence: AnalysisEvidence) -> bool:
        """Validate an analysis evidence instance."""

    @abstractmethod
    def validate_decision_set(self, decisions: tuple[AnalysisDecision, ...]) -> bool:
        """Validate a set of analysis decisions."""
