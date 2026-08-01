"""Metadata validator interface.

No validation logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata
from engines.analysis_engine.validation.validator_contract import ValidatorContract


class MetadataValidator(ValidatorContract, ABC):
    """Public interface for metadata validation contracts."""

    @abstractmethod
    def validate_metadata(self, metadata: AnalysisMetadata) -> bool:
        """Validate an analysis metadata instance."""

    @abstractmethod
    def validate_required_keys(
        self,
        metadata: Mapping[str, Any],
        required_keys: tuple[str, ...],
    ) -> bool:
        """Validate that required metadata keys are present."""

    @abstractmethod
    def validate_trace(self, trace: tuple[str, ...]) -> bool:
        """Validate a metadata trace sequence."""
