"""CK-01D commercial consulting models. Composer consumes matched units only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.commercial_composer.exceptions import CommercialComposerError
from engines.consulting_knowledge.contracts import CATALOG_ID, CONSULTING_DOMAINS
from engines.consulting_knowledge.models import ConsultingKnowledgeUnit

CONSULTING_COMPOSER_SCHEMA: str = "1.0.0"


@dataclass(slots=True)
class CommercialComposerInput:
    """Structured composer input. Matched units are already resolved."""

    matched_units: tuple[ConsultingKnowledgeUnit, ...] = ()
    analysis: Mapping[str, Any] | None = None


@dataclass(slots=True)
class CommercialConsultingSection:
    """One customer-facing consulting section traced to catalog units."""

    domain: str
    title: str
    summary: str
    meaning: tuple[str, ...]
    recommendations: tuple[str, ...]
    references: tuple[str, ...]
    source_unit_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        """Reject sections that drop domain, wording source, or traceability."""
        if self.domain not in CONSULTING_DOMAINS:
            raise CommercialComposerError(f"Unknown consulting domain: {self.domain}")
        if not self.source_unit_ids:
            raise CommercialComposerError(
                f"Section {self.domain} must cite source_unit_ids."
            )

    def to_dict(self) -> dict[str, Any]:
        """Serialize customer-facing section fields only."""
        return {
            "domain": self.domain,
            "title": self.title,
            "summary": self.summary,
            "meaning": list(self.meaning),
            "recommendations": list(self.recommendations),
            "references": list(self.references),
            "source_unit_ids": list(self.source_unit_ids),
        }


@dataclass(slots=True)
class CommercialComposerResult:
    """Structured commercial consulting output. Not an HTML blob."""

    sections: tuple[CommercialConsultingSection, ...] = ()
    status: str = "insufficient"
    catalog_id: str = CATALOG_ID
    schema_version: str = CONSULTING_COMPOSER_SCHEMA

    def to_dict(self) -> dict[str, Any]:
        """Serialize the composer result."""
        return {
            "schema_version": self.schema_version,
            "catalog_id": self.catalog_id,
            "status": self.status,
            "sections": [section.to_dict() for section in self.sections],
        }


def empty_commercial_composer_result() -> CommercialComposerResult:
    """Return an empty consulting composition. No invented advice."""
    return CommercialComposerResult(status="insufficient")
