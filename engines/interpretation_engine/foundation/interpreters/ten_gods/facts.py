"""TenGodFacts — domain truth copied from TenGodsEngine, not recalculated."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.interpretation_engine.foundation.facts.ten_gods import (
    TenGodInterpretationFacts,
    TenGodPositionFact,
)
from engines.interpretation_engine.foundation.knowledge.diagnostics import (
    INVALID_POSITION,
    INVALID_TEN_GOD,
)
from engines.interpretation_engine.foundation.knowledge.domain_classes import (
    INTERPRETATION_CLASS_RELATIONSHIP,
)
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    TEN_GOD_KEYS,
    TEN_GOD_PILLAR_KEYS,
)
from engines.interpretation_engine.foundation.status import DataAvailability

_ENGINE_RELATION_TO_CANONICAL: Mapping[str, str] = {
    "generation": "generates",
    "restriction": "controls",
    "support": "supports",
}


@dataclass(frozen=True, slots=True)
class TenGodPosition:
    """One copied Ten God occurrence with pillar position."""

    name: str
    pillar: str
    stem: str
    branch: str
    visibility: str
    god_id: str = ""
    weight: float | None = None
    evidence: str = ""
    count: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize one position without customer prose."""
        return {
            "name": self.name,
            "pillar": self.pillar,
            "stem": self.stem,
            "branch": self.branch,
            "visibility": self.visibility,
            "god_id": self.god_id,
            "weight": self.weight,
            "evidence": self.evidence,
            "count": self.count,
        }


@dataclass(frozen=True, slots=True)
class TenGodFacts:
    """Structured Ten Gods domain facts for relationship + knowledge.

    Copies TenGodInterpretationFacts and optional TenGodsResult fields.
    Does not rerun TenGodsEngine.
    """

    selected_roles: tuple[str, ...]
    visible_roles: tuple[str, ...]
    hidden_roles: tuple[str, ...]
    positions: tuple[TenGodPosition, ...]
    related_stems: tuple[str, ...]
    related_branches: tuple[str, ...]
    counts: tuple[dict[str, Any], ...]
    strength_context: str
    rule_ids: tuple[str, ...]
    day_master: str
    pattern_label: str
    useful_god_selected: str
    engine_relationships: tuple[dict[str, str], ...]
    status: DataAvailability
    interpretation_class: str = INTERPRETATION_CLASS_RELATIONSHIP
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize Ten God facts without customer prose."""
        return {
            "selected_roles": list(self.selected_roles),
            "visible_roles": list(self.visible_roles),
            "hidden_roles": list(self.hidden_roles),
            "positions": [item.to_dict() for item in self.positions],
            "related_stems": list(self.related_stems),
            "related_branches": list(self.related_branches),
            "counts": [dict(item) for item in self.counts],
            "strength_context": self.strength_context,
            "rule_ids": list(self.rule_ids),
            "day_master": self.day_master,
            "pattern_label": self.pattern_label,
            "useful_god_selected": self.useful_god_selected,
            "engine_relationships": [dict(item) for item in self.engine_relationships],
            "status": self.status.value,
            "interpretation_class": self.interpretation_class,
            "diagnostics": list(self.diagnostics),
        }


def build_ten_god_facts(
    facts: TenGodInterpretationFacts,
    *,
    ten_gods_result: Any | None = None,
    strength_level: str = "",
    pattern_label: str = "",
    useful_god_selected: str = "",
    pillar_branches: Mapping[str, str] | None = None,
) -> TenGodFacts:
    """Copy existing engine truth into TenGodFacts. Do not recalculate."""
    branches = dict(pillar_branches or {})
    god_ids = _god_id_index(ten_gods_result)
    visible_positions = tuple(
        _copy_position(item, god_ids, branches) for item in facts.visible
    )
    hidden_positions = tuple(
        _copy_position(item, god_ids, branches) for item in facts.hidden
    )
    positions = (*visible_positions, *hidden_positions)
    visible_roles = _unique(item.name for item in visible_positions)
    hidden_roles = _unique(item.name for item in hidden_positions)
    selected_roles = visible_roles
    related_stems = _unique(item.stem for item in positions)
    related_branches = _unique(
        (*(item.branch for item in positions), *branches.values())
    )
    counts = _counts(facts, ten_gods_result)
    rule_ids = _rule_ids(positions, ten_gods_result)
    engine_relationships = _engine_relationships(ten_gods_result)
    diagnostics = list(facts.diagnostics)
    for item in positions:
        if item.pillar and item.pillar not in TEN_GOD_PILLAR_KEYS:
            diagnostics.append(INVALID_POSITION)
        if item.name and item.name not in TEN_GOD_KEYS:
            diagnostics.append(INVALID_TEN_GOD)
    return TenGodFacts(
        selected_roles=selected_roles,
        visible_roles=visible_roles,
        hidden_roles=hidden_roles,
        positions=positions,
        related_stems=related_stems,
        related_branches=related_branches,
        counts=counts,
        strength_context=str(strength_level or ""),
        rule_ids=rule_ids,
        day_master=str(facts.day_master or ""),
        pattern_label=str(pattern_label or ""),
        useful_god_selected=str(useful_god_selected or ""),
        engine_relationships=engine_relationships,
        status=facts.status,
        diagnostics=tuple(dict.fromkeys(diagnostics)),
    )


def _copy_position(
    item: TenGodPositionFact,
    god_ids: Mapping[tuple[str, str, str], str],
    branches: Mapping[str, str],
) -> TenGodPosition:
    """Copy one position fact; fill branch from existing pillar strings only."""
    pillar = str(item.pillar or "")
    branch = str(item.branch or branches.get(pillar) or "")
    visibility = str(item.visibility or "")
    name = str(item.name or "")
    return TenGodPosition(
        name=name,
        pillar=pillar,
        stem=str(item.stem or ""),
        branch=branch,
        visibility=visibility,
        god_id=god_ids.get((visibility, pillar, name), ""),
        weight=item.weight,
        evidence=str(item.evidence or ""),
        count=item.count,
    )


def _god_id_index(ten_gods_result: Any | None) -> dict[tuple[str, str, str], str]:
    """Index god_id by visibility, pillar, and label from engine output."""
    index: dict[tuple[str, str, str], str] = {}
    if ten_gods_result is None:
        return index
    for item in getattr(ten_gods_result, "visible", ()) or ():
        index[("visible", str(item.pillar), str(item.ten_god))] = str(item.god_id)
    for item in getattr(ten_gods_result, "hidden", ()) or ():
        index[("hidden", str(item.pillar), str(item.ten_god))] = str(item.god_id)
    return index


def _counts(
    facts: TenGodInterpretationFacts,
    ten_gods_result: Any | None,
) -> tuple[dict[str, Any], ...]:
    """Copy distribution counts already published by the engine."""
    rows = []
    source = getattr(ten_gods_result, "distribution", None) if ten_gods_result else None
    if source:
        for entry in source:
            rows.append(
                {
                    "god_id": str(getattr(entry, "god_id", "") or ""),
                    "label": str(getattr(entry, "label", "") or ""),
                    "occurrence_count": int(getattr(entry, "occurrence_count", 0) or 0),
                    "visible_count": int(getattr(entry, "visible_count", 0) or 0),
                    "hidden_weight": float(getattr(entry, "hidden_weight", 0.0) or 0.0),
                    "weighted_contribution": float(
                        getattr(entry, "weighted_contribution", 0.0) or 0.0
                    ),
                }
            )
        return tuple(rows)
    for item in facts.distribution:
        rows.append(dict(item))
    return tuple(rows)


def _rule_ids(
    positions: tuple[TenGodPosition, ...],
    ten_gods_result: Any | None,
) -> tuple[str, ...]:
    """Copy evidence strings; TenGodsResult has no separate rule_ids field."""
    values: list[str] = []
    for item in positions:
        if item.evidence:
            values.append(item.evidence)
    if ten_gods_result is not None:
        for entry in getattr(ten_gods_result, "diagnostics", ()) or ():
            code = str(getattr(entry, "code", "") or "")
            if code:
                values.append(code)
    return _unique(values)


def _engine_relationships(ten_gods_result: Any | None) -> tuple[dict[str, str], ...]:
    """Copy engine family edges, mapping relation names to canonical types."""
    if ten_gods_result is None:
        return ()
    labels = _label_by_god_id(ten_gods_result)
    rows: list[dict[str, str]] = []
    for edge in getattr(ten_gods_result, "relationships", ()) or ():
        canonical = _ENGINE_RELATION_TO_CANONICAL.get(str(edge.relation or ""))
        if not canonical:
            continue
        source = labels.get(str(edge.from_god_id), "")
        target = labels.get(str(edge.to_god_id), "")
        if not source or not target:
            continue
        rows.append(
            {
                "source": source,
                "type": canonical,
                "target": target,
            }
        )
    return tuple(rows)


def _label_by_god_id(ten_gods_result: Any) -> dict[str, str]:
    """Collect god_id → label from copied engine entries."""
    labels: dict[str, str] = {}
    for item in getattr(ten_gods_result, "visible", ()) or ():
        labels[str(item.god_id)] = str(item.ten_god)
    for item in getattr(ten_gods_result, "hidden", ()) or ():
        labels[str(item.god_id)] = str(item.ten_god)
    for entry in getattr(ten_gods_result, "distribution", ()) or ():
        labels[str(entry.god_id)] = str(entry.label)
    return labels


def _unique(values: Any) -> tuple[str, ...]:
    """Drop empty duplicates, keep order."""
    return tuple(dict.fromkeys(str(item) for item in values if str(item).strip()))
