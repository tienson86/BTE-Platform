"""Evidence Priority and supporting ecosystem shells.

Ranking is implemented by evidence_priority.engine. These objects are the
canonical result containers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import (
    SCHEMA_EVIDENCE_PRIORITY,
    SCHEMA_RESULT,
)
from engines.detailed_interpretation_engine.enums import EvaluationStatus, PriorityTier
from engines.detailed_interpretation_engine.shen_sha.models import (
    ShenShaEcosystemResult,
    ShenShaInterpretationCollection,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.models import TenGodCombinationCollection
from engines.detailed_interpretation_engine.ten_gods.ecosystem.models import TenGodEcosystemResult
from engines.detailed_interpretation_engine.ten_gods.models import TenGodInterpretationCollection
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue, TraceRef


@dataclass(frozen=True, slots=True)
class TenGodEcosystem:
    """Ten God natal interpretation plus DI-04 ecosystem shell."""

    schema_version: str = SCHEMA_RESULT
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    finding_ids: tuple[str, ...] = ()
    trace: TraceRef = field(default_factory=TraceRef)
    natal: TenGodInterpretationCollection = field(default_factory=TenGodInterpretationCollection)
    combinations: TenGodCombinationCollection = field(default_factory=TenGodCombinationCollection)
    ecosystem: TenGodEcosystemResult = field(default_factory=TenGodEcosystemResult)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TenGodEcosystem:
        """Rebuild a Ten God ecosystem shell."""
        payload = data or {}
        natal_raw = payload.get("natal")
        combinations_raw = payload.get("combinations")
        ecosystem_raw = payload.get("ecosystem")
        return cls(
            schema_version=as_str(payload.get("schema_version"), SCHEMA_RESULT),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            finding_ids=as_str_tuple(payload.get("finding_ids")),
            trace=TraceRef.from_dict(payload.get("trace") if isinstance(payload.get("trace"), Mapping) else payload),
            natal=TenGodInterpretationCollection.from_dict(
                natal_raw if isinstance(natal_raw, Mapping) else None
            ),
            combinations=TenGodCombinationCollection.from_dict(
                combinations_raw if isinstance(combinations_raw, Mapping) else None
            ),
            ecosystem=TenGodEcosystemResult.from_dict(
                ecosystem_raw if isinstance(ecosystem_raw, Mapping) else None
            ),
        )


@dataclass(frozen=True, slots=True)
class ShenShaEcosystem:
    """Shen Sha natal interpretation plus DI-06 ecosystem shell."""

    schema_version: str = SCHEMA_RESULT
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    finding_ids: tuple[str, ...] = ()
    trace: TraceRef = field(default_factory=TraceRef)
    individual: ShenShaInterpretationCollection = field(default_factory=ShenShaInterpretationCollection)
    ecosystem: ShenShaEcosystemResult = field(default_factory=ShenShaEcosystemResult)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ShenShaEcosystem:
        """Rebuild a Shen Sha ecosystem shell."""
        payload = data or {}
        individual_raw = payload.get("individual")
        ecosystem_raw = payload.get("ecosystem")
        return cls(
            schema_version=as_str(payload.get("schema_version"), SCHEMA_RESULT),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            finding_ids=as_str_tuple(payload.get("finding_ids")),
            trace=TraceRef.from_dict(payload.get("trace") if isinstance(payload.get("trace"), Mapping) else payload),
            individual=ShenShaInterpretationCollection.from_dict(
                individual_raw if isinstance(individual_raw, Mapping) else None
            ),
            ecosystem=ShenShaEcosystemResult.from_dict(
                ecosystem_raw if isinstance(ecosystem_raw, Mapping) else None
            ),
        )


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True, slots=True)
class EvidencePriorityFinding:
    """One ranked evidence node after merge. Codes and labels, not prose."""

    finding_id: str = ""
    node_id: str = ""
    tier: PriorityTier = PriorityTier.P5
    rank: int = 0
    domain: str = ""
    category: str = ""
    importance: str = ""
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    source_refs: tuple[str, ...] = ()
    supporting_evidence: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    tier_reason: str = ""
    merge_origin: str = ""
    confidence_source: str = ""
    source_kind: str = ""
    semantic_key: str = ""
    customer_label: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> EvidencePriorityFinding:
        """Rebuild one ranked finding."""
        payload = data or {}
        return cls(
            finding_id=as_str(payload.get("finding_id")),
            node_id=as_str(payload.get("node_id")),
            tier=as_enum(PriorityTier, payload.get("tier"), PriorityTier.P5),
            rank=_as_int(payload.get("rank")),
            domain=as_str(payload.get("domain")),
            category=as_str(payload.get("category")),
            importance=as_str(payload.get("importance")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            source_refs=as_str_tuple(payload.get("source_refs")),
            supporting_evidence=as_str_tuple(payload.get("supporting_evidence")),
            conditions=as_str_tuple(payload.get("conditions")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            tier_reason=as_str(payload.get("tier_reason")),
            merge_origin=as_str(payload.get("merge_origin")),
            confidence_source=as_str(payload.get("confidence_source")),
            source_kind=as_str(payload.get("source_kind")),
            semantic_key=as_str(payload.get("semantic_key")),
            customer_label=as_str(payload.get("customer_label")),
        )


@dataclass(frozen=True, slots=True)
class EvidencePriorityResult:
    """DI-07 ranked-evidence container bound on interpretation.evidence_priority."""

    schema_version: str = SCHEMA_EVIDENCE_PRIORITY
    ruleset_version: str = ""
    analysis_id: str = ""
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    dominant_evidence: tuple[str, ...] = ()
    supporting_evidence: tuple[str, ...] = ()
    risk_evidence: tuple[str, ...] = ()
    opportunity_evidence: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    ranked_domains: tuple[str, ...] = ()
    graph: dict[str, Any] = field(default_factory=dict)
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    warnings_engine: tuple[str, ...] = ()
    findings: tuple[EvidencePriorityFinding, ...] = ()
    mc01_grade: str = ""
    score_engine_grade: str = ""
    driver_ids: tuple[str, ...] = ()
    bottleneck_ids: tuple[str, ...] = ()

    @property
    def state(self) -> EvaluationStatus:
        """Frozen contract alias for status."""
        return self.status

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> EvidencePriorityResult:
        """Rebuild evidence priority from a mapping."""
        payload = data or {}
        graph_raw = payload.get("graph")
        graph = dict(graph_raw) if isinstance(graph_raw, Mapping) else {}
        confidence_raw = payload.get("confidence")
        findings_raw = payload.get("findings") or ()
        status_raw = payload.get("status") if payload.get("status") is not None else payload.get("state")
        return cls(
            schema_version=as_str(payload.get("schema_version"), SCHEMA_EVIDENCE_PRIORITY),
            ruleset_version=as_str(payload.get("ruleset_version")),
            analysis_id=as_str(payload.get("analysis_id")),
            status=as_enum(
                EvaluationStatus,
                status_raw,
                EvaluationStatus.NOT_EVALUATED,
            ),
            dominant_evidence=as_str_tuple(payload.get("dominant_evidence")),
            supporting_evidence=as_str_tuple(payload.get("supporting_evidence")),
            risk_evidence=as_str_tuple(payload.get("risk_evidence")),
            opportunity_evidence=as_str_tuple(payload.get("opportunity_evidence")),
            conditions=as_str_tuple(payload.get("conditions")),
            warnings=as_str_tuple(payload.get("warnings")),
            ranked_domains=as_str_tuple(payload.get("ranked_domains")),
            graph=graph,
            confidence=ConfidenceValue.from_dict(confidence_raw),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            warnings_engine=as_str_tuple(payload.get("warnings_engine")),
            findings=tuple(
                EvidencePriorityFinding.from_dict(item if isinstance(item, Mapping) else None)
                for item in findings_raw
            ),
            mc01_grade=as_str(payload.get("mc01_grade")),
            score_engine_grade=as_str(payload.get("score_engine_grade")),
            driver_ids=as_str_tuple(payload.get("driver_ids")),
            bottleneck_ids=as_str_tuple(payload.get("bottleneck_ids")),
        )


@dataclass(frozen=True, slots=True)
class InterpretationSection:
    """Pack 07 structured meaning layer. No UI formatting."""

    ten_gods: TenGodEcosystem = field(default_factory=TenGodEcosystem)
    shen_sha: ShenShaEcosystem = field(default_factory=ShenShaEcosystem)
    evidence_priority: EvidencePriorityResult = field(default_factory=EvidencePriorityResult)
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    trace_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> InterpretationSection:
        """Rebuild the interpretation section."""
        payload = data or {}
        ten_raw = payload.get("ten_gods")
        shen_raw = payload.get("shen_sha")
        epr_raw = payload.get("evidence_priority")
        return cls(
            ten_gods=TenGodEcosystem.from_dict(ten_raw if isinstance(ten_raw, Mapping) else None),
            shen_sha=ShenShaEcosystem.from_dict(shen_raw if isinstance(shen_raw, Mapping) else None),
            evidence_priority=EvidencePriorityResult.from_dict(
                epr_raw if isinstance(epr_raw, Mapping) else None
            ),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )
