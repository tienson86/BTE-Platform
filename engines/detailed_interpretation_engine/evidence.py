"""Evidence Priority and supporting ecosystem shells.

These objects hold structure only. Ranking and inference are not implemented.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import (
    SCHEMA_EVIDENCE_PRIORITY,
    SCHEMA_RESULT,
)
from engines.detailed_interpretation_engine.enums import EvaluationStatus
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


@dataclass(frozen=True, slots=True)
class EvidencePriorityResult:
    """DI-07 ranked-evidence container. Empty until the engine is implemented."""

    schema_version: str = SCHEMA_EVIDENCE_PRIORITY
    ruleset_version: str = ""
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    dominant_evidence: tuple[str, ...] = ()
    supporting_evidence: tuple[str, ...] = ()
    risk_evidence: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    ranked_domains: tuple[str, ...] = ()
    graph: dict[str, Any] = field(default_factory=dict)
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    warnings_engine: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> EvidencePriorityResult:
        """Rebuild evidence priority from a mapping."""
        payload = data or {}
        graph_raw = payload.get("graph")
        graph = dict(graph_raw) if isinstance(graph_raw, Mapping) else {}
        confidence_raw = payload.get("confidence")
        return cls(
            schema_version=as_str(payload.get("schema_version"), SCHEMA_EVIDENCE_PRIORITY),
            ruleset_version=as_str(payload.get("ruleset_version")),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            dominant_evidence=as_str_tuple(payload.get("dominant_evidence")),
            supporting_evidence=as_str_tuple(payload.get("supporting_evidence")),
            risk_evidence=as_str_tuple(payload.get("risk_evidence")),
            conditions=as_str_tuple(payload.get("conditions")),
            warnings=as_str_tuple(payload.get("warnings")),
            ranked_domains=as_str_tuple(payload.get("ranked_domains")),
            graph=graph,
            confidence=ConfidenceValue.from_dict(confidence_raw),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            warnings_engine=as_str_tuple(payload.get("warnings_engine")),
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
