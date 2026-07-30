"""Luck Engine domain models."""

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
class LuckPillar:
    """Stem/branch pillar for a luck layer."""

    stem: str
    branch: str
    index: int = 0
    label: str = ""


@dataclass(slots=True, frozen=True)
class LuckLayerOutcome:
    """Evaluated outcome for one luck layer entry."""

    layer: str
    pillar: LuckPillar
    status: str
    favorability: str
    activation: str
    timing_phase: str
    priority: int = 0
    parent_layer: str | None = None
    reason_codes: tuple[str, ...] = ()
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))


@dataclass(slots=True, frozen=True)
class LuckInteractionOutcome:
    """Luck–natal interaction outcome."""

    layer: str
    dimension: str
    upstream_class: str
    effect: str
    priority: int = 0


@dataclass(slots=True, frozen=True)
class RejectedAlternative:
    """Rejected competing outcome retained for explainability."""

    subject: str
    rejected_value: str
    selected_value: str
    reason_code: str


@dataclass(slots=True)
class LuckResult:
    """Immutable public output of the Luck Engine."""

    da_yun: tuple[LuckLayerOutcome, ...]
    liu_nian: tuple[LuckLayerOutcome, ...]
    liu_yue: tuple[LuckLayerOutcome, ...]
    liu_ri: tuple[LuckLayerOutcome, ...]
    liu_shi: tuple[LuckLayerOutcome, ...]
    interactions: tuple[LuckInteractionOutcome, ...]
    active_layers: tuple[LuckLayerOutcome, ...]
    rejected_alternatives: tuple[RejectedAlternative, ...]
    confidence: ConfidenceEvaluation
    evidence: tuple[RuleEvidence, ...]
    diagnostics: tuple[DiagnosticInfo, ...]
    knowledge_module_id: str = "luck_knowledge"
    knowledge_version: str | None = None
    summary: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary", MappingProxyType(dict(self.summary)))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for StageResult payload and tests."""

        def pillar_dict(pillar: LuckPillar) -> dict[str, Any]:
            return {
                "stem": pillar.stem,
                "branch": pillar.branch,
                "index": pillar.index,
                "label": pillar.label,
            }

        def layer_dict(item: LuckLayerOutcome) -> dict[str, Any]:
            return {
                "layer": item.layer,
                "pillar": pillar_dict(item.pillar),
                "status": item.status,
                "favorability": item.favorability,
                "activation": item.activation,
                "timing_phase": item.timing_phase,
                "priority": item.priority,
                "parent_layer": item.parent_layer,
                "reason_codes": list(item.reason_codes),
                "details": dict(item.details),
            }

        return {
            "da_yun": [layer_dict(item) for item in self.da_yun],
            "liu_nian": [layer_dict(item) for item in self.liu_nian],
            "liu_yue": [layer_dict(item) for item in self.liu_yue],
            "liu_ri": [layer_dict(item) for item in self.liu_ri],
            "liu_shi": [layer_dict(item) for item in self.liu_shi],
            "interactions": [
                {
                    "layer": item.layer,
                    "dimension": item.dimension,
                    "upstream_class": item.upstream_class,
                    "effect": item.effect,
                    "priority": item.priority,
                }
                for item in self.interactions
            ],
            "active_layers": [layer_dict(item) for item in self.active_layers],
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
    def from_stage_result(cls, stage_result: StageResult) -> LuckResult:
        """Rebuild LuckResult from a published StageResult payload."""
        payload = stage_result.payload
        confidence_raw = payload.get("confidence") or {}

        def parse_pillar(raw: dict[str, Any]) -> LuckPillar:
            return LuckPillar(
                stem=str(raw["stem"]),
                branch=str(raw["branch"]),
                index=int(raw.get("index", 0)),
                label=str(raw.get("label") or ""),
            )

        def parse_layer(raw: dict[str, Any]) -> LuckLayerOutcome:
            return LuckLayerOutcome(
                layer=str(raw["layer"]),
                pillar=parse_pillar(raw["pillar"]),
                status=str(raw["status"]),
                favorability=str(raw["favorability"]),
                activation=str(raw["activation"]),
                timing_phase=str(raw["timing_phase"]),
                priority=int(raw.get("priority", 0)),
                parent_layer=raw.get("parent_layer"),
                reason_codes=tuple(raw.get("reason_codes") or ()),
                details=dict(raw.get("details") or {}),
            )

        return cls(
            da_yun=tuple(parse_layer(item) for item in payload.get("da_yun", [])),
            liu_nian=tuple(parse_layer(item) for item in payload.get("liu_nian", [])),
            liu_yue=tuple(parse_layer(item) for item in payload.get("liu_yue", [])),
            liu_ri=tuple(parse_layer(item) for item in payload.get("liu_ri", [])),
            liu_shi=tuple(parse_layer(item) for item in payload.get("liu_shi", [])),
            interactions=tuple(
                LuckInteractionOutcome(**item)
                for item in payload.get("interactions", [])
            ),
            active_layers=tuple(
                parse_layer(item) for item in payload.get("active_layers", [])
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
                payload.get("knowledge_module_id", "luck_knowledge")
            ),
            knowledge_version=payload.get("knowledge_version"),
            summary=dict(payload.get("summary") or {}),
        )
