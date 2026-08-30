"""Narrative V2 Evidence Builder public surface."""

from __future__ import annotations

from engines.narrative_v2.evidence.evidence_builder import EvidenceBuilder
from engines.narrative_v2.evidence.evidence_context import (
    EvidenceContractGap,
    NarrativeEvidenceContext,
)
from engines.narrative_v2.evidence.evidence_errors import (
    EvidenceError,
    EvidenceValidationError,
)
from engines.narrative_v2.evidence.evidence_item import EvidenceItem
from engines.narrative_v2.evidence.evidence_reference import EvidenceReference
from engines.narrative_v2.evidence.evidence_registry import (
    ALLOWED_DOMAINS,
    EvidenceRegistry,
)
from engines.narrative_v2.evidence.evidence_validator import (
    EvidenceValidator,
    EvidenceValidationOutcome,
)

__all__ = [
    "ALLOWED_DOMAINS",
    "EvidenceBuilder",
    "EvidenceContractGap",
    "EvidenceError",
    "EvidenceItem",
    "EvidenceReference",
    "EvidenceRegistry",
    "EvidenceValidationError",
    "EvidenceValidationOutcome",
    "EvidenceValidator",
    "NarrativeEvidenceContext",
]
