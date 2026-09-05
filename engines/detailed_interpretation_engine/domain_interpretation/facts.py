"""Read MC-01 profiles and Evidence Priority. Does not rerank or rescore."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.evidence import (
    EvidencePriorityFinding,
    EvidencePriorityResult,
)
from engines.detailed_interpretation_engine.mc01 import Mc01StructuralSnapshot, snapshot_from_live_payload
from engines.detailed_interpretation_engine.ten_gods.combinations.helpers import ACTIVE_STATES


@dataclass(frozen=True, slots=True)
class ProfileAxis:
    """One copied MC-01 classification. Not a new score."""

    name: str
    classification: str
    polarity: str = ""
    source_ref: str = ""


@dataclass(frozen=True, slots=True)
class DomainFacts:
    """Canonical inputs Domain Interpretation may explain."""

    snapshot: Mc01StructuralSnapshot | None
    ep: EvidencePriorityResult
    achievement: dict[str, ProfileAxis] = field(default_factory=dict)
    wealth: dict[str, ProfileAxis] = field(default_factory=dict)
    career: dict[str, ProfileAxis] = field(default_factory=dict)
    dominant_capabilities: tuple[str, ...] = ()
    work_styles: tuple[str, ...] = ()
    damage_types: tuple[str, ...] = ()
    rescue_types: tuple[str, ...] = ()
    combination_ids: tuple[str, ...] = ()
    shen_sha_keys: tuple[str, ...] = ()
    integrity: str = ""
    pattern: str = ""
    grade: str = ""
    has_rescue: bool = False


def collect_domain_facts(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> DomainFacts:
    """Copy ranked evidence and MC-01 profile axes. Do not invent classifications."""
    data = payload or {}
    snapshot = snapshot_from_live_payload(data)
    mingju = _mingju_view(data)
    achievement_block = _mapping(mingju.get("achievement"))
    wealth_block = _mapping(mingju.get("wealth"))
    career_block = _mapping(mingju.get("career"))
    damage = _string_field(mingju.get("damage"), "damage_type")
    rescue = _string_field(mingju.get("rescue"), "rescue_type")
    if snapshot:
        if not damage:
            damage = tuple(snapshot.damage_ids)
        if not rescue:
            rescue = tuple(snapshot.rescue_ids)
    interpretation = context.runtime.interpretation
    combination_ids = tuple(
        item.combination_id
        for item in interpretation.ten_gods.combinations.items
        if item.state in ACTIVE_STATES and item.combination_id
    )
    shen_keys = tuple(
        item.shen_sha_id.strip().lower()
        for item in interpretation.shen_sha.individual.items
        if item.shen_sha_id
    )
    return DomainFacts(
        snapshot=snapshot,
        ep=interpretation.evidence_priority,
        achievement=_axes(achievement_block, "mc01.achievement")
        or _dominant_axes(
            snapshot.achievement if snapshot else str(data.get("achievement") or ""),
            "mc01.achievement",
        ),
        wealth=_axes(wealth_block, "mc01.wealth")
        or _wealth_fallback(snapshot.wealth_profile if snapshot else str(data.get("wealth_profile") or "")),
        career=_axes(career_block, "mc01.career"),
        dominant_capabilities=_tuple_or_split(
            achievement_block.get("dominant_capabilities"),
            snapshot.achievement if snapshot else str(data.get("achievement") or ""),
        ),
        work_styles=_tuple_or_split(
            career_block.get("dominant_work_styles"),
            snapshot.career_profile if snapshot else str(data.get("career_profile") or ""),
        ),
        damage_types=damage,
        rescue_types=rescue,
        combination_ids=combination_ids,
        shen_sha_keys=shen_keys,
        integrity=(snapshot.integrity if snapshot else "") or str(_mapping(mingju.get("integrity")).get("state") or ""),
        pattern=(snapshot.pattern if snapshot else ""),
        grade=(snapshot.grade if snapshot else ""),
        has_rescue=bool(rescue),
    )


def classification_of(axes: Mapping[str, ProfileAxis], name: str) -> str:
    """Return a copied MC-01 classification or empty."""
    item = axes.get(name)
    return item.classification if item else ""


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _mingju_view(payload: Mapping[str, Any]) -> dict[str, Any]:
    snapshot = _mapping(payload.get("_mingju"))
    public = _mapping(payload.get("mingju"))
    merged = dict(snapshot)
    merged.update(public)
    if snapshot.get("damage"):
        merged["damage"] = snapshot["damage"]
    if snapshot.get("rescue"):
        merged["rescue"] = snapshot["rescue"]
    return merged


def _axes(block: Mapping[str, Any], prefix: str) -> dict[str, ProfileAxis]:
    items: dict[str, ProfileAxis] = {}
    for raw in block.get("dimensions") or ():
        if not isinstance(raw, Mapping):
            continue
        name = str(raw.get("dimension") or "").strip()
        classification = str(raw.get("classification") or "").strip()
        if not name or not classification:
            continue
        items[name] = ProfileAxis(
            name=name,
            classification=classification,
            polarity=str(raw.get("polarity") or ""),
            source_ref=f"{prefix}.{name}",
        )
    return items


def _dominant_axes(raw: str, prefix: str) -> dict[str, ProfileAxis]:
    items: dict[str, ProfileAxis] = {}
    for token in (part.strip() for part in raw.split(",")):
        if not token or ":" in token:
            continue
        items[token] = ProfileAxis(
            name=token,
            classification="above_average",
            source_ref=f"{prefix}.{token}",
        )
    return items


def _wealth_fallback(raw: str) -> dict[str, ProfileAxis]:
    items: dict[str, ProfileAxis] = {}
    for token in (part.strip() for part in raw.split(",") if part.strip()):
        if ":" not in token:
            continue
        name, classification = token.split(":", 1)
        items[name] = ProfileAxis(
            name=name,
            classification=classification,
            source_ref=f"mc01.wealth.{name}",
        )
    return items


def _tuple_or_split(value: Any, fallback: str) -> tuple[str, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(str(item).strip() for item in value if str(item).strip())
    return tuple(part.strip() for part in fallback.split(",") if part.strip() and ":" not in part)


def _string_field(value: Any, key: str) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        return ()
    found: list[str] = []
    for item in value:
        if isinstance(item, Mapping):
            text = str(item.get(key) or "").strip()
        else:
            text = str(item).strip()
        if text:
            found.append(text)
    return tuple(found)


def finding_lookup(ep: EvidencePriorityResult) -> dict[str, EvidencePriorityFinding]:
    """Index ranked findings by id."""
    return {item.finding_id: item for item in ep.findings if item.finding_id}
