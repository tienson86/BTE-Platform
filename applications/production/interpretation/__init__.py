"""Generic multi-domain interpretation composition — Sprint 4."""

from applications.production.interpretation.contracts import (
    DomainInterpretationResult,
    DomainSection,
    DomainStatus,
    KnowledgeStatus,
)
from applications.production.interpretation.service import (
    MultiDomainInterpretationService,
)

__all__ = [
    "DomainInterpretationResult",
    "DomainSection",
    "DomainStatus",
    "KnowledgeStatus",
    "MultiDomainInterpretationService",
]
