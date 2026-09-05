"""Pack 07 narrative graph shells. No wording generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import SCHEMA_COMPOSER
from engines.detailed_interpretation_engine.enums import (
    EvaluationStatus,
    NarrativeEdgeType,
    NarrativeLayer,
    NarrativeNodeType,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class NarrativeNode:
    """One NarrativeGraph node. Empty until Composer runs."""

    node_id: str = ""
    node_type: NarrativeNodeType = NarrativeNodeType.SUPPORTING_EVIDENCE
    layer: NarrativeLayer = NarrativeLayer.COMMERCIAL
    evidence_ids: tuple[str, ...] = ()
    message_key: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> NarrativeNode:
        """Rebuild a narrative node."""
        payload = data or {}
        return cls(
            node_id=as_str(payload.get("node_id")),
            node_type=as_enum(
                NarrativeNodeType,
                payload.get("node_type"),
                NarrativeNodeType.SUPPORTING_EVIDENCE,
            ),
            layer=as_enum(NarrativeLayer, payload.get("layer"), NarrativeLayer.COMMERCIAL),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            message_key=as_str(payload.get("message_key")),
        )


@dataclass(frozen=True, slots=True)
class NarrativeEdge:
    """One NarrativeGraph edge."""

    source_id: str = ""
    target_id: str = ""
    edge_type: NarrativeEdgeType = NarrativeEdgeType.SUPPORTS

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> NarrativeEdge:
        """Rebuild a narrative edge."""
        payload = data or {}
        return cls(
            source_id=as_str(payload.get("source_id")),
            target_id=as_str(payload.get("target_id")),
            edge_type=as_enum(
                NarrativeEdgeType,
                payload.get("edge_type"),
                NarrativeEdgeType.SUPPORTS,
            ),
        )


@dataclass(frozen=True, slots=True)
class NarrativeGraph:
    """Single narrative graph for all consumers (DI-19)."""

    nodes: tuple[NarrativeNode, ...] = ()
    edges: tuple[NarrativeEdge, ...] = ()
    schema_version: str = SCHEMA_COMPOSER

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> NarrativeGraph:
        """Rebuild a narrative graph."""
        payload = data or {}
        nodes_raw = payload.get("nodes") or ()
        edges_raw = payload.get("edges") or ()
        nodes = tuple(
            NarrativeNode.from_dict(item) for item in nodes_raw if isinstance(item, Mapping)
        )
        edges = tuple(
            NarrativeEdge.from_dict(item) for item in edges_raw if isinstance(item, Mapping)
        )
        return cls(
            nodes=nodes,
            edges=edges,
            schema_version=as_str(payload.get("schema_version"), SCHEMA_COMPOSER),
        )


@dataclass(frozen=True, slots=True)
class NarrativeResult:
    """Composer output shell. Does not infer."""

    schema_version: str = SCHEMA_COMPOSER
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    executive_summary: str = ""
    strengths: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    opportunities: tuple[str, ...] = ()
    domains: dict[str, str] = field(default_factory=dict)
    temporal: str = ""
    optimization: str = ""
    closing_summary: str = ""
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    trace: tuple[str, ...] = ()
    graph: NarrativeGraph = field(default_factory=NarrativeGraph)
    mc01_summary_ref: str = ""
    warnings: tuple[str, ...] = ()
    layers: dict[str, tuple[str, ...]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> NarrativeResult:
        """Rebuild narrative result from a mapping."""
        payload = data or {}
        domains_raw = payload.get("domains")
        domains = (
            {str(key): str(item) for key, item in domains_raw.items()}
            if isinstance(domains_raw, Mapping)
            else {}
        )
        layers_raw = payload.get("layers")
        layers: dict[str, tuple[str, ...]] = {}
        if isinstance(layers_raw, Mapping):
            for key, item in layers_raw.items():
                if isinstance(item, Mapping):
                    layers[str(key)] = as_str_tuple(item.get("node_ids") or item.get("blocks"))
                else:
                    layers[str(key)] = as_str_tuple(item)
        graph_raw = payload.get("graph")
        return cls(
            schema_version=as_str(payload.get("schema_version"), SCHEMA_COMPOSER),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            executive_summary=as_str(payload.get("executive_summary")),
            strengths=as_str_tuple(payload.get("strengths")),
            risks=as_str_tuple(payload.get("risks")),
            opportunities=as_str_tuple(payload.get("opportunities")),
            domains=domains,
            temporal=as_str(payload.get("temporal")),
            optimization=as_str(payload.get("optimization")),
            closing_summary=as_str(payload.get("closing_summary")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            trace=as_str_tuple(payload.get("trace")),
            graph=NarrativeGraph.from_dict(graph_raw if isinstance(graph_raw, Mapping) else None),
            mc01_summary_ref=as_str(payload.get("mc01_summary_ref")),
            warnings=as_str_tuple(payload.get("warnings")),
            layers=layers,
        )


@dataclass(frozen=True, slots=True)
class NarrativeSection:
    """Published narrative layer of CanonicalRuntimeResult."""

    graph: NarrativeGraph = field(default_factory=NarrativeGraph)
    result: NarrativeResult = field(default_factory=NarrativeResult)
    executive_summary: str = ""
    layers: dict[str, tuple[str, ...]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> NarrativeSection:
        """Rebuild the narrative section."""
        payload = data or {}
        result = NarrativeResult.from_dict(
            payload.get("result") if isinstance(payload.get("result"), Mapping) else payload
        )
        graph_raw = payload.get("graph")
        graph = (
            NarrativeGraph.from_dict(graph_raw)
            if isinstance(graph_raw, Mapping)
            else result.graph
        )
        layers_raw = payload.get("layers")
        layers: dict[str, tuple[str, ...]] = dict(result.layers)
        if isinstance(layers_raw, Mapping):
            for key, item in layers_raw.items():
                layers[str(key)] = as_str_tuple(item if not isinstance(item, Mapping) else item.get("node_ids"))
        return cls(
            graph=graph,
            result=result,
            executive_summary=as_str(payload.get("executive_summary"), result.executive_summary),
            layers=layers,
        )
