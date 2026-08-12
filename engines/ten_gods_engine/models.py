"""Ten Gods Core Engine domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from engines.ten_gods_engine.constants import ENGINE_VERSION


@dataclass(frozen=True, slots=True)
class DayMasterInfo:
    """Published day master facts."""

    stem: str
    element: str
    yin_yang: str


@dataclass(frozen=True, slots=True)
class VisibleTenGodEntry:
    """Visible heavenly stem Ten God occurrence."""

    pillar: str
    stem: str
    ten_god: str
    god_id: str
    visibility: str
    evidence: str


@dataclass(frozen=True, slots=True)
class HiddenTenGodEntry:
    """Hidden stem Ten God occurrence."""

    pillar: str
    branch: str
    hidden_stem: str
    hidden_position: int
    position_name: str
    weight: float
    ten_god: str
    god_id: str
    evidence: str


@dataclass(frozen=True, slots=True)
class DistributionEntry:
    """Separate occurrence and weighted totals for one Ten God."""

    god_id: str
    label: str
    occurrence_count: int
    weighted_contribution: float
    visible_count: int
    hidden_weight: float


@dataclass(frozen=True, slots=True)
class WeightEntry:
    """Explicit weight ledger line."""

    god_id: str
    label: str
    layer: str
    pillar: str
    weight: float
    evidence: str


@dataclass(frozen=True, slots=True)
class DominanceResult:
    """Dominance resolution outcome."""

    status: str
    primary_god_ids: tuple[str, ...]
    policy: str
    weighted_totals: Mapping[str, float]


@dataclass(frozen=True, slots=True)
class HierarchyEntry:
    """Hierarchy tier for one Ten God."""

    god_id: str
    label: str
    tier: str
    weighted_contribution: float


@dataclass(frozen=True, slots=True)
class RelationshipEdge:
    """Structural relationship between two present Ten Gods."""

    from_god_id: str
    to_god_id: str
    relation: str


@dataclass(frozen=True, slots=True)
class InteractionCell:
    """Deterministic interaction matrix cell."""

    row_god_id: str
    col_god_id: str
    state: str


@dataclass(frozen=True, slots=True)
class DiagnosticEntry:
    """Engine diagnostic record."""

    code: str
    message: str
    level: str = "info"


@dataclass(slots=True)
class TenGodsResult:
    """Canonical public output of the Ten Gods Core Engine."""

    day_master: DayMasterInfo
    visible: tuple[VisibleTenGodEntry, ...]
    hidden: tuple[HiddenTenGodEntry, ...]
    distribution: tuple[DistributionEntry, ...]
    weights: tuple[WeightEntry, ...]
    dominant: DominanceResult
    hierarchy: tuple[HierarchyEntry, ...]
    relationships: tuple[RelationshipEdge, ...]
    interaction_matrix: tuple[InteractionCell, ...]
    missing_data: tuple[str, ...]
    diagnostics: tuple[DiagnosticEntry, ...]
    version: str = ENGINE_VERSION

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a deterministic JSON-compatible dict."""
        return {
            "version": self.version,
            "day_master": {
                "stem": self.day_master.stem,
                "element": self.day_master.element,
                "yin_yang": self.day_master.yin_yang,
            },
            "visible": [
                {
                    "pillar": item.pillar,
                    "stem": item.stem,
                    "ten_god": item.ten_god,
                    "god_id": item.god_id,
                    "visibility": item.visibility,
                    "evidence": item.evidence,
                }
                for item in self.visible
            ],
            "hidden": [
                {
                    "pillar": item.pillar,
                    "branch": item.branch,
                    "hidden_stem": item.hidden_stem,
                    "hidden_position": item.hidden_position,
                    "position_name": item.position_name,
                    "weight": item.weight,
                    "ten_god": item.ten_god,
                    "god_id": item.god_id,
                    "evidence": item.evidence,
                }
                for item in self.hidden
            ],
            "distribution": [
                {
                    "god_id": item.god_id,
                    "label": item.label,
                    "occurrence_count": item.occurrence_count,
                    "weighted_contribution": item.weighted_contribution,
                    "visible_count": item.visible_count,
                    "hidden_weight": item.hidden_weight,
                }
                for item in self.distribution
            ],
            "weights": [
                {
                    "god_id": item.god_id,
                    "label": item.label,
                    "layer": item.layer,
                    "pillar": item.pillar,
                    "weight": item.weight,
                    "evidence": item.evidence,
                }
                for item in self.weights
            ],
            "dominant": {
                "status": self.dominant.status,
                "primary_god_ids": list(self.dominant.primary_god_ids),
                "policy": self.dominant.policy,
                "weighted_totals": dict(self.dominant.weighted_totals),
            },
            "hierarchy": [
                {
                    "god_id": item.god_id,
                    "label": item.label,
                    "tier": item.tier,
                    "weighted_contribution": item.weighted_contribution,
                }
                for item in self.hierarchy
            ],
            "relationships": [
                {
                    "from_god_id": item.from_god_id,
                    "to_god_id": item.to_god_id,
                    "relation": item.relation,
                }
                for item in self.relationships
            ],
            "interaction_matrix": [
                {
                    "row_god_id": item.row_god_id,
                    "col_god_id": item.col_god_id,
                    "state": item.state,
                }
                for item in self.interaction_matrix
            ],
            "missing_data": list(self.missing_data),
            "diagnostics": [
                {
                    "code": item.code,
                    "message": item.message,
                    "level": item.level,
                }
                for item in self.diagnostics
            ],
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> TenGodsResult:
        """Rebuild TenGodsResult from serialized payload."""
        dm = payload["day_master"]
        dominant = payload["dominant"]
        return cls(
            day_master=DayMasterInfo(
                stem=str(dm["stem"]),
                element=str(dm["element"]),
                yin_yang=str(dm["yin_yang"]),
            ),
            visible=tuple(
                VisibleTenGodEntry(**item) for item in payload.get("visible", [])
            ),
            hidden=tuple(
                HiddenTenGodEntry(**item) for item in payload.get("hidden", [])
            ),
            distribution=tuple(
                DistributionEntry(**item) for item in payload.get("distribution", [])
            ),
            weights=tuple(WeightEntry(**item) for item in payload.get("weights", [])),
            dominant=DominanceResult(
                status=str(dominant["status"]),
                primary_god_ids=tuple(dominant.get("primary_god_ids") or ()),
                policy=str(dominant["policy"]),
                weighted_totals=MappingProxyType(
                    dict(dominant.get("weighted_totals") or {})
                ),
            ),
            hierarchy=tuple(
                HierarchyEntry(**item) for item in payload.get("hierarchy", [])
            ),
            relationships=tuple(
                RelationshipEdge(**item) for item in payload.get("relationships", [])
            ),
            interaction_matrix=tuple(
                InteractionCell(**item)
                for item in payload.get("interaction_matrix", [])
            ),
            missing_data=tuple(payload.get("missing_data") or ()),
            diagnostics=tuple(
                DiagnosticEntry(**item) for item in payload.get("diagnostics", [])
            ),
            version=str(payload.get("version") or ENGINE_VERSION),
        )
