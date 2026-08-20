"""Resolve Useful God tokens through canonical G1-01 Ten God truth."""

from __future__ import annotations

from typing import Any

from engines.bazi_engine.ten_god import STEM_META, stem_element, stem_for_ten_god, ten_god_name

from .layers import OVERALL_INCOMPLETE_MESSAGE
from .models import UsefulGodResult


def resolve_god_token(day_master: str, token: str) -> dict[str, str]:
    """Map a CSV stem or Ten God token to Ten God + stem + element."""
    raw = str(token or "").strip()
    master = str(day_master or "").strip()
    if not raw:
        return {"ten_god": "", "stem": "", "element": "", "label": ""}
    if raw in STEM_META:
        return {
            "ten_god": ten_god_name(master, raw) if master else "",
            "stem": raw,
            "element": stem_element(raw),
            "label": raw,
        }
    stem = stem_for_ten_god(master, raw) if master else ""
    return {
        "ten_god": raw,
        "stem": stem,
        "element": stem_element(stem) if stem else "",
        "label": raw,
    }


def format_god_role(role: dict[str, str]) -> str:
    """Format one role as ``Element · Stem · Ten God``."""
    parts = [
        str(role.get("element") or "").strip(),
        str(role.get("stem") or "").strip(),
        str(role.get("ten_god") or "").strip(),
    ]
    return " · ".join(part for part in parts if part)


def format_god_roles(roles: list[dict[str, str]]) -> str:
    """Join role displays without deriving new gods."""
    return " / ".join(
        display for display in (format_god_role(role) for role in roles) if display
    )


def _enrich_candidate(candidate: dict[str, Any], day_master: str) -> dict[str, Any]:
    mapped = resolve_god_token(day_master, str(candidate.get("useful_god") or ""))
    enriched = dict(candidate)
    enriched["ten_god"] = mapped["ten_god"]
    enriched["stem"] = mapped["stem"]
    enriched["element"] = mapped["element"]
    enriched["match_status"] = "matched"
    return enriched


def enrich_useful_god_result(result: UsefulGodResult, day_master: str) -> UsefulGodResult:
    """Attach G1-01 mapping onto Overall and Điều hậu layers."""
    result.candidate_list = [
        _enrich_candidate(candidate, day_master) for candidate in result.candidate_list
    ]
    result.overall_candidate_list = [
        _enrich_candidate(candidate, day_master)
        for candidate in result.overall_candidate_list
    ]
    result.climate_candidate_list = [
        _enrich_candidate(candidate, day_master)
        for candidate in result.climate_candidate_list
    ]
    if result.useful_god:
        useful = resolve_god_token(day_master, result.useful_god)
        result.useful_ten_god = useful["ten_god"]
        result.useful_stem = useful["stem"]
        result.useful_element = useful["element"]
        result.useful_display = format_god_role(useful)
        result.favorable_roles = [
            resolve_god_token(day_master, token) for token in result.favorable_gods
        ]
        result.unfavorable_roles = [
            resolve_god_token(day_master, token) for token in result.unfavorable_gods
        ]
        result.favorable_display = format_god_roles(result.favorable_roles)
        result.unfavorable_display = format_god_roles(result.unfavorable_roles)
    elif not result.useful_display:
        result.useful_display = OVERALL_INCOMPLETE_MESSAGE

    if result.climate_candidate:
        climate = resolve_god_token(day_master, result.climate_candidate)
        result.climate_ten_god = climate["ten_god"]
        result.climate_stem = climate["stem"]
        result.climate_element = climate["element"]
        result.climate_display = format_god_role(climate)
        if climate["element"]:
            result.climate_preference_label = f"Điều hậu ưu tiên {climate['element']}"

    trace = result.metadata.get("trace") if isinstance(result.metadata, dict) else None
    if isinstance(trace, dict):
        winner = trace.get("winner")
        if isinstance(winner, dict) and winner:
            trace["winner"] = _enrich_candidate(winner, day_master)
        climate_winner = trace.get("climate_winner")
        if isinstance(climate_winner, dict) and climate_winner:
            trace["climate_winner"] = _enrich_candidate(climate_winner, day_master)
        for key in ("candidate_list", "overall_candidate_list", "climate_candidate_list"):
            items = trace.get(key)
            if isinstance(items, list):
                trace[key] = [
                    _enrich_candidate(item, day_master) if isinstance(item, dict) else item
                    for item in items
                ]
    return result
