"""Ten Gods Engine domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from engines.analysis_engine.runtime.models import (
    ConfidenceEvaluation,
    DiagnosticInfo,
    RuleEvidence,
    StageResult,
)


TEN_GOD_IDS: tuple[str, ...] = (
    "bi_jian",
    "jie_cai",
    "shi_shen",
    "shang_guan",
    "pian_cai",
    "zheng_cai",
    "qi_sha",
    "zheng_guan",
    "pian_yin",
    "zheng_yin",
)


@dataclass(slots=True, frozen=True)
class TenGodPresence:
    """One detected Ten God occurrence."""

    god_id: str
    label: str
    source_pillar: str
    source_stem: str
    polarity_class: str
    count: int = 1


@dataclass(slots=True, frozen=True)
class RelationshipOutcome:
    """Relationship between two present Ten Gods."""

    left_god_id: str
    right_god_id: str
    relation: str
    priority: int = 0


@dataclass(slots=True, frozen=True)
class InteractionOutcome:
    """Interaction of Ten Gods with an upstream classification."""

    dimension: str
    upstream_class: str
    god_id: str
    effect: str
    priority: int = 0


@dataclass(slots=True, frozen=True)
class FavorabilityOutcome:
    """Favorability class for a Ten God under resolved conditions."""

    god_id: str
    favorability: str
    reason_codes: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class LifeAreaConcept:
    """Analytical concept tag for a life area (not narrative text)."""

    area: str
    god_id: str
    concept_id: str
    tag: str


@dataclass(slots=True, frozen=True)
class RejectedAlternative:
    """Rejected competing outcome retained for explainability."""

    subject: str
    rejected_value: str
    selected_value: str
    reason_code: str


@dataclass(slots=True)
class TenGodsResult:
    """Immutable public output of the Ten Gods Engine."""

    presence: tuple[TenGodPresence, ...]
    relationships: tuple[RelationshipOutcome, ...]
    interactions: tuple[InteractionOutcome, ...]
    favorability: tuple[FavorabilityOutcome, ...]
    life_areas: tuple[LifeAreaConcept, ...]
    rejected_alternatives: tuple[RejectedAlternative, ...]
    confidence: ConfidenceEvaluation
    evidence: tuple[RuleEvidence, ...]
    diagnostics: tuple[DiagnosticInfo, ...]
    knowledge_module_id: str = "ten_gods_knowledge"
    knowledge_version: str | None = None
    summary: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary", MappingProxyType(dict(self.summary)))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for StageResult payload and tests."""
        return {
            "presence": [
                {
                    "god_id": item.god_id,
                    "label": item.label,
                    "source_pillar": item.source_pillar,
                    "source_stem": item.source_stem,
                    "polarity_class": item.polarity_class,
                    "count": item.count,
                }
                for item in self.presence
            ],
            "relationships": [
                {
                    "left_god_id": item.left_god_id,
                    "right_god_id": item.right_god_id,
                    "relation": item.relation,
                    "priority": item.priority,
                }
                for item in self.relationships
            ],
            "interactions": [
                {
                    "dimension": item.dimension,
                    "upstream_class": item.upstream_class,
                    "god_id": item.god_id,
                    "effect": item.effect,
                    "priority": item.priority,
                }
                for item in self.interactions
            ],
            "favorability": [
                {
                    "god_id": item.god_id,
                    "favorability": item.favorability,
                    "reason_codes": list(item.reason_codes),
                }
                for item in self.favorability
            ],
            "life_areas": [
                {
                    "area": item.area,
                    "god_id": item.god_id,
                    "concept_id": item.concept_id,
                    "tag": item.tag,
                }
                for item in self.life_areas
            ],
            "rejected_alternatives": [
                {
                    "subject": item.subject,
                    "rejected_value": item.rejected_value,
                    "selected_value": item.selected_value,
                    "reason_code": item.reason_code,
                }
                for item in self.rejected_alternatives
            ],
            "confidence": {
                "score": self.confidence.score,
                "level": self.confidence.level,
                "details": dict(self.confidence.details),
            },
            "evidence": [
                {
                    "rule_id": item.rule_id,
                    "version": item.version,
                    "category": item.category,
                    "priority": item.priority,
                    "reference": item.reference,
                    "details": dict(item.details),
                }
                for item in self.evidence
            ],
            "diagnostics": [
                {
                    "code": item.code,
                    "message": item.message,
                    "level": item.level,
                    "stage_id": item.stage_id,
                    "details": dict(item.details),
                }
                for item in self.diagnostics
            ],
            "knowledge_module_id": self.knowledge_module_id,
            "knowledge_version": self.knowledge_version,
            "summary": dict(self.summary),
        }

    @classmethod
    def from_stage_result(cls, stage_result: StageResult) -> TenGodsResult:
        """Rebuild TenGodsResult from a published StageResult payload."""
        payload = stage_result.payload
        confidence_raw = payload.get("confidence") or {}
        return cls(
            presence=tuple(
                TenGodPresence(**item) for item in payload.get("presence", [])
            ),
            relationships=tuple(
                RelationshipOutcome(**item)
                for item in payload.get("relationships", [])
            ),
            interactions=tuple(
                InteractionOutcome(**item)
                for item in payload.get("interactions", [])
            ),
            favorability=tuple(
                FavorabilityOutcome(
                    god_id=item["god_id"],
                    favorability=item["favorability"],
                    reason_codes=tuple(item.get("reason_codes") or ()),
                )
                for item in payload.get("favorability", [])
            ),
            life_areas=tuple(
                LifeAreaConcept(**item) for item in payload.get("life_areas", [])
            ),
            rejected_alternatives=tuple(
                RejectedAlternative(**item)
                for item in payload.get("rejected_alternatives", [])
            ),
            confidence=ConfidenceEvaluation(
                score=confidence_raw.get("score"),
                level=confidence_raw.get("level"),
                details=dict(confidence_raw.get("details") or {}),
            ),
            evidence=tuple(
                RuleEvidence(
                    rule_id=item["rule_id"],
                    version=item.get("version", "1.0.0"),
                    category=item.get("category", ""),
                    priority=int(item.get("priority", 0)),
                    reference=item.get("reference", ""),
                    details=dict(item.get("details") or {}),
                )
                for item in payload.get("evidence", [])
            ),
            diagnostics=tuple(
                DiagnosticInfo(
                    code=item["code"],
                    message=item["message"],
                    level=item.get("level", "info"),
                    stage_id=item.get("stage_id"),
                    details=dict(item.get("details") or {}),
                )
                for item in payload.get("diagnostics", [])
            ),
            knowledge_module_id=str(
                payload.get("knowledge_module_id", "ten_gods_knowledge")
            ),
            knowledge_version=payload.get("knowledge_version"),
            summary=dict(payload.get("summary") or {}),
        )
