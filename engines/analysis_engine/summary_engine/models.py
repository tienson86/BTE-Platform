"""Summary Engine domain models."""

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

UPSTREAM_STAGES: tuple[str, ...] = (
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "ten_gods",
    "combination",
    "shensha",
    "luck",
)


@dataclass(slots=True, frozen=True)
class DomainSummaryView:
    """Non-destructive projection of one upstream StageResult."""

    stage_id: str
    status: str
    module_version: str
    highlight_keys: tuple[str, ...]
    payload_digest: Mapping[str, Any]
    confidence_score: float | None = None
    confidence_level: str | None = None
    evidence_count: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "payload_digest",
            MappingProxyType(dict(self.payload_digest)),
        )


@dataclass(slots=True, frozen=True)
class ConsistencyIssue:
    """One cross-stage consistency finding."""

    code: str
    severity: str
    message: str
    stages: tuple[str, ...] = ()
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))


@dataclass(slots=True, frozen=True)
class CrossStageConsistencyReport:
    """Outcome of cross-stage consistency validation."""

    status: str
    issue_count: int
    issues: tuple[ConsistencyIssue, ...] = ()


@dataclass(slots=True, frozen=True)
class ConsolidatedConfidenceSummary:
    """Aggregated confidence profile across upstream stages."""

    score: float
    level: str
    stage_scores: Mapping[str, float]
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "stage_scores",
            MappingProxyType(dict(self.stage_scores)),
        )
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))


@dataclass(slots=True, frozen=True)
class EvidenceIndexEntry:
    """Indexed evidence entry preserving upstream traceability."""

    stage_id: str
    rule_id: str
    category: str
    priority: int
    reference: str
    version: str = "1.0.0"
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))


@dataclass(slots=True)
class SummaryResult:
    """Immutable public output of the Summary Engine."""

    strength_summary: DomainSummaryView
    temperature_summary: DomainSummaryView
    pattern_summary: DomainSummaryView
    useful_god_summary: DomainSummaryView
    ten_gods_summary: DomainSummaryView
    combination_summary: DomainSummaryView
    shensha_summary: DomainSummaryView
    luck_summary: DomainSummaryView
    consistency: CrossStageConsistencyReport
    consolidated_confidence: ConsolidatedConfidenceSummary
    evidence_index: tuple[EvidenceIndexEntry, ...]
    confidence: ConfidenceEvaluation
    evidence: tuple[RuleEvidence, ...]
    diagnostics: tuple[DiagnosticInfo, ...]
    summary: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary", MappingProxyType(dict(self.summary)))

    def domain_views(self) -> tuple[DomainSummaryView, ...]:
        """Return domain summary views in canonical order."""
        return (
            self.strength_summary,
            self.temperature_summary,
            self.pattern_summary,
            self.useful_god_summary,
            self.ten_gods_summary,
            self.combination_summary,
            self.shensha_summary,
            self.luck_summary,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize for StageResult payload and tests."""

        def view_dict(view: DomainSummaryView) -> dict[str, Any]:
            return {
                "stage_id": view.stage_id,
                "status": view.status,
                "module_version": view.module_version,
                "highlight_keys": list(view.highlight_keys),
                "payload_digest": dict(view.payload_digest),
                "confidence_score": view.confidence_score,
                "confidence_level": view.confidence_level,
                "evidence_count": view.evidence_count,
            }

        return {
            "strength_summary": view_dict(self.strength_summary),
            "temperature_summary": view_dict(self.temperature_summary),
            "pattern_summary": view_dict(self.pattern_summary),
            "useful_god_summary": view_dict(self.useful_god_summary),
            "ten_gods_summary": view_dict(self.ten_gods_summary),
            "combination_summary": view_dict(self.combination_summary),
            "shensha_summary": view_dict(self.shensha_summary),
            "luck_summary": view_dict(self.luck_summary),
            "consistency": {
                "status": self.consistency.status,
                "issue_count": self.consistency.issue_count,
                "issues": [
                    {
                        "code": item.code,
                        "severity": item.severity,
                        "message": item.message,
                        "stages": list(item.stages),
                        "details": dict(item.details),
                    }
                    for item in self.consistency.issues
                ],
            },
            "consolidated_confidence": {
                "score": self.consolidated_confidence.score,
                "level": self.consolidated_confidence.level,
                "stage_scores": dict(self.consolidated_confidence.stage_scores),
                "details": dict(self.consolidated_confidence.details),
            },
            "evidence_index": [
                {
                    "stage_id": item.stage_id,
                    "rule_id": item.rule_id,
                    "category": item.category,
                    "priority": item.priority,
                    "reference": item.reference,
                    "version": item.version,
                    "details": dict(item.details),
                }
                for item in self.evidence_index
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
            "summary": dict(self.summary),
        }

    @classmethod
    def from_stage_result(cls, stage_result: StageResult) -> SummaryResult:
        """Rebuild SummaryResult from a published StageResult payload."""
        payload = stage_result.payload
        confidence_raw = payload.get("confidence") or {}
        consistency_raw = payload.get("consistency") or {}
        consolidated_raw = payload.get("consolidated_confidence") or {}

        def parse_view(raw: dict[str, Any]) -> DomainSummaryView:
            return DomainSummaryView(
                stage_id=str(raw["stage_id"]),
                status=str(raw["status"]),
                module_version=str(raw.get("module_version") or "1.0.0"),
                highlight_keys=tuple(raw.get("highlight_keys") or ()),
                payload_digest=dict(raw.get("payload_digest") or {}),
                confidence_score=raw.get("confidence_score"),
                confidence_level=raw.get("confidence_level"),
                evidence_count=int(raw.get("evidence_count", 0)),
            )

        return cls(
            strength_summary=parse_view(payload["strength_summary"]),
            temperature_summary=parse_view(payload["temperature_summary"]),
            pattern_summary=parse_view(payload["pattern_summary"]),
            useful_god_summary=parse_view(payload["useful_god_summary"]),
            ten_gods_summary=parse_view(payload["ten_gods_summary"]),
            combination_summary=parse_view(payload["combination_summary"]),
            shensha_summary=parse_view(payload["shensha_summary"]),
            luck_summary=parse_view(payload["luck_summary"]),
            consistency=CrossStageConsistencyReport(
                status=str(consistency_raw.get("status") or "unknown"),
                issue_count=int(consistency_raw.get("issue_count", 0)),
                issues=tuple(
                    ConsistencyIssue(
                        code=item["code"],
                        severity=item["severity"],
                        message=item["message"],
                        stages=tuple(item.get("stages") or ()),
                        details=dict(item.get("details") or {}),
                    )
                    for item in consistency_raw.get("issues", [])
                ),
            ),
            consolidated_confidence=ConsolidatedConfidenceSummary(
                score=float(consolidated_raw.get("score", 0.0)),
                level=str(consolidated_raw.get("level") or "low"),
                stage_scores=dict(consolidated_raw.get("stage_scores") or {}),
                details=dict(consolidated_raw.get("details") or {}),
            ),
            evidence_index=tuple(
                EvidenceIndexEntry(
                    stage_id=item["stage_id"],
                    rule_id=item["rule_id"],
                    category=item.get("category", ""),
                    priority=int(item.get("priority", 0)),
                    reference=item.get("reference", ""),
                    version=item.get("version", "1.0.0"),
                    details=dict(item.get("details") or {}),
                )
                for item in payload.get("evidence_index", [])
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
            summary=dict(payload.get("summary") or {}),
        )
