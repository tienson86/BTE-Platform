"""Read-only upstream Shen Sha detection facts. Does not recalculate stars."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_str
from engines.detailed_interpretation_engine.shen_sha.constants import (
    KNOWN_STAR_IDS,
    NAME_TO_ID,
    UNRESOLVED_BANDS,
)
from engines.detailed_interpretation_engine.shen_sha.models import ShenShaOccurrence


@dataclass(frozen=True, slots=True)
class DetectedShenSha:
    """One canonical star published by the upstream detector."""

    shen_sha_id: str
    canonical_name: str = ""
    positions: tuple[ShenShaOccurrence, ...] = ()
    evidence_id: str = ""


@dataclass(frozen=True, slots=True)
class UpstreamShenShaFacts:
    """Detection list plus optional structural domain support."""

    available: bool = False
    matches: tuple[DetectedShenSha, ...] = ()
    unknown_ids: tuple[str, ...] = ()
    domain_support: dict[str, str] = field(default_factory=dict)
    mc01_bound: bool = False
    rescue_present: bool = False
    risk_surface: bool = False


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _normalize_star_id(raw_id: str, canonical_name: str) -> str:
    token = raw_id.strip().lower().replace("-", " ").replace(" ", "_")
    if token in KNOWN_STAR_IDS:
        return token
    name = canonical_name.strip()
    if name in NAME_TO_ID:
        return NAME_TO_ID[name]
    lowered = name.lower()
    if lowered in NAME_TO_ID:
        return NAME_TO_ID[lowered]
    return ""


def _positions(match: Mapping[str, Any]) -> tuple[ShenShaOccurrence, ...]:
    found: list[ShenShaOccurrence] = []
    for item in match.get("occurrences") or ():
        if not isinstance(item, Mapping):
            continue
        found.append(
            ShenShaOccurrence(
                pillar=as_str(item.get("pillar")),
                location=as_str(item.get("location")),
                target_value=as_str(item.get("target_value")),
            )
        )
    if found:
        return tuple(found)
    pillar = as_str(match.get("pillar"))
    if not pillar:
        return ()
    return (
        ShenShaOccurrence(
            pillar=pillar,
            location=as_str(match.get("location")),
            target_value=as_str(match.get("target_value")),
        ),
    )


def _domain_band(raw: Any) -> str:
    if isinstance(raw, Mapping):
        token = as_str(raw.get("state") or raw.get("band") or raw.get("level")).strip().lower()
    else:
        token = as_str(raw).strip().lower()
    return token.replace("-", "_")


def _domain_support(payload: Mapping[str, Any]) -> dict[str, str]:
    block = _mapping(payload.get("pack07_domain_support")) or _mapping(payload.get("domain_support"))
    if not block:
        domains = _mapping(payload.get("domains"))
        if domains:
            block = domains
    support: dict[str, str] = {}
    for key, value in block.items():
        band = _domain_band(value)
        if band:
            support[str(key).strip().lower()] = band
    return support


def has_shen_sha_facts(payload: Mapping[str, Any] | None) -> bool:
    """True when upstream Shen Sha detection is present."""
    data = payload or {}
    bazi = _mapping(data.get("bazi"))
    matches = bazi.get("shensha_matches") or data.get("shensha_matches")
    names = bazi.get("shensha") or data.get("shensha")
    return bool(matches or names)


def extract_shen_sha_facts(payload: Mapping[str, Any] | None) -> UpstreamShenShaFacts:
    """Copy detector matches. Do not synthesize undetected stars."""
    data = payload or {}
    bazi = _mapping(data.get("bazi"))
    raw_matches = bazi.get("shensha_matches") or data.get("shensha_matches") or ()
    detected: list[DetectedShenSha] = []
    unknown: list[str] = []
    seen: set[str] = set()
    if isinstance(raw_matches, (list, tuple)):
        for index, item in enumerate(raw_matches):
            if not isinstance(item, Mapping):
                continue
            name = as_str(item.get("canonical_name") or item.get("name"))
            star_id = _normalize_star_id(as_str(item.get("id") or item.get("shen_sha_id")), name)
            if not star_id:
                token = as_str(item.get("id") or name)
                if token and token not in unknown:
                    unknown.append(token)
                continue
            if star_id in seen:
                continue
            seen.add(star_id)
            detected.append(
                DetectedShenSha(
                    shen_sha_id=star_id,
                    canonical_name=name,
                    positions=_positions(item),
                    evidence_id=as_str(item.get("evidence_id")) or f"E-DI-SS-{star_id}-{index}",
                )
            )
    if not detected:
        for index, name in enumerate(bazi.get("shensha") or data.get("shensha") or ()):
            text = as_str(name).strip()
            star_id = _normalize_star_id("", text)
            if not star_id or star_id in seen:
                if text and not star_id and text not in unknown:
                    unknown.append(text)
                continue
            seen.add(star_id)
            detected.append(
                DetectedShenSha(
                    shen_sha_id=star_id,
                    canonical_name=text,
                    evidence_id=f"E-DI-SS-{star_id}-name-{index}",
                )
            )
    mc01 = _mapping(data.get("mc01")) or _mapping(data.get("mingju"))
    support = _domain_support(data)
    risk_band = support.get("risk", "")
    rescue_ids = mc01.get("rescue_ids") or data.get("rescue_ids")
    rescue_present = bool(data.get("rescue_present")) or support.get("rescue", "") in {
        "present",
        "true",
    }
    if isinstance(rescue_ids, (list, tuple)):
        rescue_present = rescue_present or bool(rescue_ids)
    elif as_str(rescue_ids).strip():
        rescue_present = True
    return UpstreamShenShaFacts(
        available=bool(detected or unknown or raw_matches),
        matches=tuple(detected),
        unknown_ids=tuple(unknown),
        domain_support=support,
        mc01_bound=bool(as_str(mc01.get("mingju_result_id") or mc01.get("id"))),
        rescue_present=rescue_present,
        risk_surface=bool(data.get("risk_surface"))
        or risk_band not in UNRESOLVED_BANDS and risk_band not in {"", "absent"},
    )
