"""Combination Engine domain models."""

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
class RelationOutcome:
    """One detected structural relation outcome."""

    relation_type: str
    relation_id: str
    members: tuple[str, ...]
    pillars: tuple[str, ...]
    status: str
    result_element: str | None = None
    priority: int = 0
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))


@dataclass(slots=True, frozen=True)
class TransformationOutcome:
    """Transformation success/failure evaluation for a combination."""

    source_relation_id: str
    success: bool
    result_element: str | None
    reason_codes: tuple[str, ...] = ()
    priority: int = 0


@dataclass(slots=True, frozen=True)
class RejectedAlternative:
    """Rejected competing outcome retained for explainability."""

    subject: str
    rejected_value: str
    selected_value: str
    reason_code: str


@dataclass(slots=True)
class CombinationResult:
    """Immutable public output of the Combination Engine."""

    stem_combinations: tuple[RelationOutcome, ...]
    branch_combinations: tuple[RelationOutcome, ...]
    clashes: tuple[RelationOutcome, ...]
    harms: tuple[RelationOutcome, ...]
    punishments: tuple[RelationOutcome, ...]
    destructions: tuple[RelationOutcome, ...]
    hidden_combinations: tuple[RelationOutcome, ...]
    transformations: tuple[TransformationOutcome, ...]
    active_relations: tuple[RelationOutcome, ...]
    rejected_alternatives: tuple[RejectedAlternative, ...]
    confidence: ConfidenceEvaluation
    evidence: tuple[RuleEvidence, ...]
    diagnostics: tuple[DiagnosticInfo, ...]
    knowledge_module_id: str = "combination_knowledge"
    knowledge_version: str | None = None
    summary: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary", MappingProxyType(dict(self.summary)))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for StageResult payload and tests."""

        def relation_dict(item: RelationOutcome) -> dict[str, Any]:
            return {
                "relation_type": item.relation_type,
                "relation_id": item.relation_id,
                "members": list(item.members),
                "pillars": list(item.pillars),
                "status": item.status,
                "result_element": item.result_element,
                "priority": item.priority,
                "details": dict(item.details),
            }

        return {
            "stem_combinations": [relation_dict(item) for item in self.stem_combinations],
            "branch_combinations": [
                relation_dict(item) for item in self.branch_combinations
            ],
            "clashes": [relation_dict(item) for item in self.clashes],
            "harms": [relation_dict(item) for item in self.harms],
            "punishments": [relation_dict(item) for item in self.punishments],
            "destructions": [relation_dict(item) for item in self.destructions],
            "hidden_combinations": [
                relation_dict(item) for item in self.hidden_combinations
            ],
            "transformations": [
                {
                    "source_relation_id": item.source_relation_id,
                    "success": item.success,
                    "result_element": item.result_element,
                    "reason_codes": list(item.reason_codes),
                    "priority": item.priority,
                }
                for item in self.transformations
            ],
            "active_relations": [
                relation_dict(item) for item in self.active_relations
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
    def from_stage_result(cls, stage_result: StageResult) -> CombinationResult:
        """Rebuild CombinationResult from a published StageResult payload."""
        payload = stage_result.payload
        confidence_raw = payload.get("confidence") or {}

        def parse_relation(item: dict[str, Any]) -> RelationOutcome:
            return RelationOutcome(
                relation_type=item["relation_type"],
                relation_id=item["relation_id"],
                members=tuple(item.get("members") or ()),
                pillars=tuple(item.get("pillars") or ()),
                status=item["status"],
                result_element=item.get("result_element"),
                priority=int(item.get("priority", 0)),
                details=dict(item.get("details") or {}),
            )

        return cls(
            stem_combinations=tuple(
                parse_relation(item) for item in payload.get("stem_combinations", [])
            ),
            branch_combinations=tuple(
                parse_relation(item) for item in payload.get("branch_combinations", [])
            ),
            clashes=tuple(parse_relation(item) for item in payload.get("clashes", [])),
            harms=tuple(parse_relation(item) for item in payload.get("harms", [])),
            punishments=tuple(
                parse_relation(item) for item in payload.get("punishments", [])
            ),
            destructions=tuple(
                parse_relation(item) for item in payload.get("destructions", [])
            ),
            hidden_combinations=tuple(
                parse_relation(item) for item in payload.get("hidden_combinations", [])
            ),
            transformations=tuple(
                TransformationOutcome(
                    source_relation_id=item["source_relation_id"],
                    success=bool(item["success"]),
                    result_element=item.get("result_element"),
                    reason_codes=tuple(item.get("reason_codes") or ()),
                    priority=int(item.get("priority", 0)),
                )
                for item in payload.get("transformations", [])
            ),
            active_relations=tuple(
                parse_relation(item) for item in payload.get("active_relations", [])
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
                payload.get("knowledge_module_id", "combination_knowledge")
            ),
            knowledge_version=payload.get("knowledge_version"),
            summary=dict(payload.get("summary") or {}),
        )
