"""CK-01A Consulting Knowledge models. Contracts only."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.consulting_knowledge.contracts import (
    CONSULTING_DOMAINS,
    FRAMEWORK_VERSION,
    INSUFFICIENT_COPY,
    KNOWLEDGE_UNIT_FIELDS,
    SOURCE_PATH,
    UNIT_SCHEMA,
)
from engines.consulting_knowledge.exceptions import ConsultingKnowledgeError

_VALID_STATUS = frozenset({"complete", "partial", "insufficient"})


@dataclass(slots=True)
class ConsultingKnowledgeUnit:
    """One catalog consulting unit. Wording is stored. Never generated."""

    unit_id: str
    domain: str
    condition: Mapping[str, Any]
    applicable_scope: Mapping[str, Any]
    consulting_meaning: str
    customer_wording: tuple[str, ...]
    recommended_actions: tuple[str, ...]
    references: tuple[str, ...]
    status: str = "complete"
    schema_version: str = UNIT_SCHEMA

    def __post_init__(self) -> None:
        """Reject units that drop required consulting fields or domains."""
        if self.domain not in CONSULTING_DOMAINS:
            raise ConsultingKnowledgeError(f"Unknown domain: {self.domain}")
        if self.status not in _VALID_STATUS:
            raise ConsultingKnowledgeError(f"Invalid status: {self.status}")
        if not self.unit_id.strip():
            raise ConsultingKnowledgeError("unit_id is required.")
        if self.status == "complete" and not self.customer_wording:
            raise ConsultingKnowledgeError("Complete units must include customer wording.")

    def to_dict(self) -> dict[str, Any]:
        """Serialize the knowledge unit."""
        return {
            "unit_id": self.unit_id,
            "domain": self.domain,
            "condition": dict(self.condition),
            "applicable_scope": dict(self.applicable_scope),
            "consulting_meaning": self.consulting_meaning,
            "customer_wording": list(self.customer_wording),
            "recommended_actions": list(self.recommended_actions),
            "references": list(self.references),
            "status": self.status,
            "schema_version": self.schema_version,
            "required_fields": list(KNOWLEDGE_UNIT_FIELDS),
        }


@dataclass(slots=True)
class ConsultingKnowledgePack:
    """Matched consulting units for one published result."""

    units: tuple[ConsultingKnowledgeUnit, ...] = ()
    status: str = "insufficient"
    source_path: str = SOURCE_PATH
    schema_version: str = UNIT_SCHEMA
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Reject packs with an invalid status."""
        if self.status not in _VALID_STATUS:
            raise ConsultingKnowledgeError(f"Invalid pack status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        """Serialize the pack."""
        return {
            "schema_version": self.schema_version,
            "source_path": self.source_path,
            "status": self.status,
            "units": [unit.to_dict() for unit in self.units],
            "evidence_refs": list(self.evidence_refs),
            "framework_version": FRAMEWORK_VERSION,
            "empty_copy": INSUFFICIENT_COPY if self.status == "insufficient" else "",
        }


def empty_knowledge_unit(domain: str = "career") -> ConsultingKnowledgeUnit:
    """Return an insufficient unit with all required fields present."""
    return ConsultingKnowledgeUnit(
        unit_id="ck-empty",
        domain=domain,
        condition={},
        applicable_scope={"domain": domain},
        consulting_meaning="",
        customer_wording=(),
        recommended_actions=(),
        references=(),
        status="insufficient",
    )


def empty_knowledge_pack() -> ConsultingKnowledgePack:
    """Return a structurally complete insufficient pack."""
    return ConsultingKnowledgePack(status="insufficient")
