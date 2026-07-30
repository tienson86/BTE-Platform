"""ShenSha Engine domain models."""

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


@dataclass(slots=True, frozen=True)
class ShenShaPresence:
    """One detected ShenSha identity occurrence."""

    shensha_id: str
    label: str
    polarity: str
    anchor: str
    anchor_value: str
    location_pillar: str
    location_value: str
    status: str = "active"
    priority: int = 0


@dataclass(slots=True, frozen=True)
class InteractionOutcome:
    """Interaction between co-present ShenSha identities."""

    left_id: str
    right_id: str
    relation: str
    effect: str
    priority: int = 0


@dataclass(slots=True, frozen=True)
class CompatibilityOutcome:
    """Compatibility class for a ShenSha identity under chart conditions."""

    shensha_id: str
    compatibility: str
    reason_codes: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class ExceptionOutcome:
    """Exception override or suppression applied to a ShenSha outcome."""

    shensha_id: str
    action: str
    reason_code: str
    priority: int = 0


@dataclass(slots=True, frozen=True)
class RejectedAlternative:
    """Rejected competing outcome retained for explainability."""

    subject: str
    rejected_value: str
    selected_value: str
    reason_code: str


@dataclass(slots=True)
class ShenShaResult:
    """Immutable public output of the ShenSha Engine."""

    auspicious: tuple[ShenShaPresence, ...]
    inauspicious: tuple[ShenShaPresence, ...]
    presence: tuple[ShenShaPresence, ...]
    interactions: tuple[InteractionOutcome, ...]
    compatibility: tuple[CompatibilityOutcome, ...]
    exceptions: tuple[ExceptionOutcome, ...]
    rejected_alternatives: tuple[RejectedAlternative, ...]
    confidence: ConfidenceEvaluation
    evidence: tuple[RuleEvidence, ...]
    diagnostics: tuple[DiagnosticInfo, ...]
    knowledge_module_id: str = "shensha_knowledge"
    knowledge_version: str | None = None
    summary: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary", MappingProxyType(dict(self.summary)))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for StageResult payload and tests."""

        def presence_dict(item: ShenShaPresence) -> dict[str, Any]:
            return {
                "shensha_id": item.shensha_id,
                "label": item.label,
                "polarity": item.polarity,
                "anchor": item.anchor,
                "anchor_value": item.anchor_value,
                "location_pillar": item.location_pillar,
                "location_value": item.location_value,
                "status": item.status,
                "priority": item.priority,
            }

        return {
            "auspicious": [presence_dict(item) for item in self.auspicious],
            "inauspicious": [presence_dict(item) for item in self.inauspicious],
            "presence": [presence_dict(item) for item in self.presence],
            "interactions": [
                {
                    "left_id": item.left_id,
                    "right_id": item.right_id,
                    "relation": item.relation,
                    "effect": item.effect,
                    "priority": item.priority,
                }
                for item in self.interactions
            ],
            "compatibility": [
                {
                    "shensha_id": item.shensha_id,
                    "compatibility": item.compatibility,
                    "reason_codes": list(item.reason_codes),
                }
                for item in self.compatibility
            ],
            "exceptions": [
                {
                    "shensha_id": item.shensha_id,
                    "action": item.action,
                    "reason_code": item.reason_code,
                    "priority": item.priority,
                }
                for item in self.exceptions
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
    def from_stage_result(cls, stage_result: StageResult) -> ShenShaResult:
        """Rebuild ShenShaResult from a published StageResult payload."""
        payload = stage_result.payload
        confidence_raw = payload.get("confidence") or {}

        def parse_presence(item: dict[str, Any]) -> ShenShaPresence:
            return ShenShaPresence(
                shensha_id=item["shensha_id"],
                label=item["label"],
                polarity=item["polarity"],
                anchor=item["anchor"],
                anchor_value=item["anchor_value"],
                location_pillar=item["location_pillar"],
                location_value=item["location_value"],
                status=item.get("status", "active"),
                priority=int(item.get("priority", 0)),
            )

        return cls(
            auspicious=tuple(
                parse_presence(item) for item in payload.get("auspicious", [])
            ),
            inauspicious=tuple(
                parse_presence(item) for item in payload.get("inauspicious", [])
            ),
            presence=tuple(
                parse_presence(item) for item in payload.get("presence", [])
            ),
            interactions=tuple(
                InteractionOutcome(**item) for item in payload.get("interactions", [])
            ),
            compatibility=tuple(
                CompatibilityOutcome(
                    shensha_id=item["shensha_id"],
                    compatibility=item["compatibility"],
                    reason_codes=tuple(item.get("reason_codes") or ()),
                )
                for item in payload.get("compatibility", [])
            ),
            exceptions=tuple(
                ExceptionOutcome(**item) for item in payload.get("exceptions", [])
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
                payload.get("knowledge_module_id", "shensha_knowledge")
            ),
            knowledge_version=payload.get("knowledge_version"),
            summary=dict(payload.get("summary") or {}),
        )
