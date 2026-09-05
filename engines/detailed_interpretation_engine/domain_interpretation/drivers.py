"""Elect frozen DI-12~17 Domain Drivers. Labels are display only."""

from __future__ import annotations

from dataclasses import dataclass

from engines.detailed_interpretation_engine.domain_interpretation.constants import (
    CAI_SHENG_GUAN_COMBINATIONS,
    GUAN_YIN_COMBINATIONS,
    HIGH_BANDS,
    MAIN_DOMAIN_IDS,
    OUTPUT_WEALTH_COMBINATIONS,
    QI_SHA_YIN_COMBINATIONS,
)
from engines.detailed_interpretation_engine.domain_interpretation.facts import (
    DomainFacts,
    classification_of,
)
from engines.detailed_interpretation_engine.domain_interpretation.labels import DRIVER_LABELS
from engines.detailed_interpretation_engine.domain_interpretation.states import strongest_band
from engines.detailed_interpretation_engine.enums import DomainState


@dataclass(frozen=True, slots=True)
class CanonicalDriver:
    """Canonical mechanism plus display label. Not EP customer text."""

    driver_id: str
    label: str


def elect_canonical_driver(
    domain_id: str,
    facts: DomainFacts,
    dimensions: dict[str, str],
    state: DomainState,
) -> CanonicalDriver:
    """Pick one frozen driver mechanism. Do not copy EP/Damage/dimension labels."""
    if domain_id not in MAIN_DOMAIN_IDS:
        return CanonicalDriver("", "")
    if state is DomainState.UNRESOLVED:
        return CanonicalDriver("not_applicable", "")
    elected = _elect(domain_id, facts, dimensions)
    if not elected:
        return CanonicalDriver("unresolved", "")
    return CanonicalDriver(elected, DRIVER_LABELS.get(elected, ""))


def _elect(domain_id: str, facts: DomainFacts, dimensions: dict[str, str]) -> str:
    if domain_id == "authority":
        return _pick(_authority_candidates(facts, dimensions), mixed="mixed")
    if domain_id == "career":
        return _pick(_career_candidates(facts, dimensions), mixed="hybrid")
    if domain_id == "wealth":
        return _pick(_wealth_candidates(facts, dimensions), mixed="hybrid")
    if domain_id == "relationship":
        return _pick(_relationship_candidates(dimensions), mixed="hybrid")
    if domain_id == "legacy":
        return _pick(_legacy_candidates(dimensions), mixed="hybrid")
    if domain_id == "vitality":
        return _vitality_driver(dimensions)
    return ""


def _pick(candidates: list[str], *, mixed: str) -> str:
    unique = list(dict.fromkeys(item for item in candidates if item))
    if not unique:
        return ""
    if len(unique) == 1:
        return unique[0]
    return mixed


def _authority_candidates(facts: DomainFacts, dimensions: dict[str, str]) -> list[str]:
    items: list[str] = []
    if _is_zheng_guan(facts.pattern):
        items.append("zheng_guan_primary")
    if any(item in QI_SHA_YIN_COMBINATIONS for item in facts.combination_ids):
        items.append("qi_sha_yin_chain")
    if any(item in CAI_SHENG_GUAN_COMBINATIONS for item in facts.combination_ids):
        items.append("cai_sheng_guan")
    if any(item in GUAN_YIN_COMBINATIONS for item in facts.combination_ids):
        items.append("guan_yin_chain")
    if classification_of(facts.achievement, "management") in HIGH_BANDS or dimensions.get(
        "managerial_authority"
    ) in HIGH_BANDS:
        items.append("management_structure")
    if classification_of(facts.achievement, "academic") in HIGH_BANDS or dimensions.get(
        "professional_authority"
    ) in HIGH_BANDS:
        items.append("professional_authority")
    return items


def _career_candidates(facts: DomainFacts, dimensions: dict[str, str]) -> list[str]:
    items: list[str] = []
    if _fit(dimensions, "academic_fit") or "academic_research" in facts.work_styles:
        items.append("academic_depth")
    if (
        _fit(dimensions, "management_fit")
        or _fit(dimensions, "leadership_fit")
        or "managerial" in facts.work_styles
        or "leadership_command" in facts.work_styles
    ):
        items.append("authority_management")
    if _fit(dimensions, "entrepreneurial_fit") or "entrepreneurship" in facts.dominant_capabilities:
        items.append("entrepreneurship")
    if _fit(dimensions, "technical_fit") or _fit(dimensions, "specialist_fit"):
        items.append("technical_specialization")
    if _fit(dimensions, "creative_fit"):
        items.append("creative_output")
    if any(item in OUTPUT_WEALTH_COMBINATIONS for item in facts.combination_ids):
        items.append("commercial_chain")
    if _fit(dimensions, "public_facing_fit"):
        items.append("public_visibility")
    return items


def _wealth_candidates(facts: DomainFacts, dimensions: dict[str, str]) -> list[str]:
    items: list[str] = []
    if any(item in OUTPUT_WEALTH_COMBINATIONS for item in facts.combination_ids):
        items.append("output")
    if dimensions.get("commercialization") in HIGH_BANDS:
        items.append("commercial")
    if classification_of(facts.achievement, "authority") in HIGH_BANDS or any(
        item in CAI_SHENG_GUAN_COMBINATIONS for item in facts.combination_ids
    ):
        items.append("authority")
    if classification_of(facts.achievement, "academic") in HIGH_BANDS and "technical" in facts.work_styles:
        items.append("technical")
    if classification_of(facts.achievement, "creative") in HIGH_BANDS and any(
        item in OUTPUT_WEALTH_COMBINATIONS for item in facts.combination_ids
    ):
        items.append("creative")
    if classification_of(facts.achievement, "management") in HIGH_BANDS:
        items.append("management")
    if (
        "entrepreneurship" in facts.dominant_capabilities
        or classification_of(facts.career, "entrepreneurial_fit") in HIGH_BANDS
    ):
        items.append("entrepreneurship")
    return items


def _relationship_candidates(dimensions: dict[str, str]) -> list[str]:
    ranked = (
        "communication",
        "trust",
        "commitment",
        "compatibility",
        "shared_growth",
        "mutual_support",
    )
    aliases = {"shared_growth": "mutual_growth", "mutual_support": "relationship_support"}
    items: list[str] = []
    for driver_id in ranked:
        key = aliases.get(driver_id, driver_id)
        if dimensions.get(key):
            items.append(driver_id)
            break
    return items


def _legacy_candidates(dimensions: dict[str, str]) -> list[str]:
    mapping = (
        ("knowledge", "knowledge_legacy"),
        ("creative", "creative_legacy"),
        ("business", "business_legacy"),
        ("community", "community_legacy"),
        ("family", "family_legacy"),
    )
    highs = [driver_id for driver_id, axis in mapping if dimensions.get(axis) in HIGH_BANDS]
    if highs:
        return list(dict.fromkeys(highs[:3]))
    if dimensions.get("knowledge_legacy"):
        return ["knowledge"]
    if dimensions.get("creative_legacy"):
        return ["creative"]
    if dimensions.get("business_legacy"):
        return ["business"]
    return []


def _vitality_driver(dimensions: dict[str, str]) -> str:
    scores = {
        "capacity": dimensions.get("capacity", ""),
        "recovery": dimensions.get("recovery", ""),
        "resilience": dimensions.get("resilience", ""),
        "energy": strongest_band(
            (dimensions.get("energy_efficiency", ""), dimensions.get("energy_stability", ""))
        ),
    }
    present = {key: value for key, value in scores.items() if value}
    if not present:
        return ""
    top = strongest_band(tuple(present.values()))
    winners = [key for key, value in present.items() if value == top]
    if len(winners) > 1:
        return "hybrid"
    return winners[0]


def _fit(dimensions: dict[str, str], key: str) -> bool:
    return dimensions.get(key) in HIGH_BANDS


def _is_zheng_guan(pattern: str) -> bool:
    text = pattern.strip().lower()
    return text in {"chính quan", "chinh quan", "zheng_guan"} or "zheng_guan" in text
