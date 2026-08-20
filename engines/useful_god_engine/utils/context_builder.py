"""Useful God context builder from PatternContext V2."""

from __future__ import annotations

from typing import Any

from engines.bazi_engine.ten_god import ten_god_name
from engines.pattern_engine.follow_tokens import canonicalize_follow_token
from engines.pattern_engine.override_eligibility import (
    LEVEL_1_SPECIAL_TOKENS,
    classify_pattern_override,
)
from engines.useful_god_engine.context import UsefulGodContext

_CHINH_QUAN = "Chính Quan"
_PILLARS = ("year", "month", "day", "hour")


def build_useful_god_context(pattern_context: Any, pattern_result: Any = None) -> UsefulGodContext:
    """Convert PatternContext V2 into UsefulGodContext for rule matching."""
    main_pattern = None
    follow_pattern = None
    detected_special = None

    if pattern_result is not None:
        main_pattern = str(getattr(pattern_result, "pattern", "") or "") or None
        follow_pattern = canonicalize_follow_token(
            getattr(pattern_result, "follow_type", None)
        )
        if main_pattern in LEVEL_1_SPECIAL_TOKENS:
            detected_special = main_pattern

    if main_pattern is None:
        main_pattern = str(getattr(pattern_context, "main_pattern", "") or "") or None
    if follow_pattern is None:
        follow_pattern = canonicalize_follow_token(
            getattr(pattern_context, "follow_pattern", None)
        )
    if detected_special is None:
        context_special = str(getattr(pattern_context, "special_pattern", "") or "") or None
        if context_special in LEVEL_1_SPECIAL_TOKENS:
            detected_special = context_special
        elif main_pattern in LEVEL_1_SPECIAL_TOKENS:
            detected_special = main_pattern

    override = classify_pattern_override(main_pattern, follow_pattern)
    # LEVEL-1 chuyên stay detected; they do not feed spc_* matcher fields.
    special_pattern = None
    matcher_follow = override.follow_pattern if override.ug_override_eligible else None

    officer_elements, officer_provenance = _officer_elements_with_hidden_chinh_quan(
        pattern_context
    )
    metadata = {
        "builder": "useful_god_context_builder_v2",
        "officer_provenance": officer_provenance,
        "chinh_quan_visibility": _chinh_quan_visibility_class(officer_provenance),
        "detected_special_pattern": detected_special,
        "qualification_level": override.qualification_level,
        "ug_override_eligible": override.ug_override_eligible,
        "suppressed_special_ug_override": bool(detected_special)
        and not override.ug_override_eligible,
    }
    return UsefulGodContext(
        day_master=getattr(pattern_context, "day_master", None),
        day_master_element=getattr(pattern_context, "day_master_element", None),
        day_master_yin_yang=getattr(pattern_context, "day_master_yin_yang", None),
        month_branch=getattr(pattern_context, "month_branch", None),
        month_branch_element=getattr(pattern_context, "month_branch_element", None),
        month_branch_ten_god=getattr(pattern_context, "month_branch_ten_god", None),
        strength_level=getattr(pattern_context, "strength_level", None),
        season=getattr(pattern_context, "season", None),
        season_phase=getattr(pattern_context, "season_phase", None),
        temperature_type=getattr(pattern_context, "temperature_type", None),
        element_distribution=dict(getattr(pattern_context, "element_distribution", {}) or {}),
        support_elements=list(getattr(pattern_context, "support_elements", []) or []),
        resource_elements=list(getattr(pattern_context, "resource_elements", []) or []),
        wealth_elements=list(getattr(pattern_context, "wealth_elements", []) or []),
        officer_elements=officer_elements,
        output_elements=list(getattr(pattern_context, "output_elements", []) or []),
        companion_elements=list(getattr(pattern_context, "companion_elements", []) or []),
        ten_gods_list=list(getattr(pattern_context, "ten_gods_list", []) or []),
        follow_pattern=matcher_follow,
        special_pattern=special_pattern,
        main_pattern=main_pattern,
        ug_override_eligible=override.ug_override_eligible,
        officer_provenance=officer_provenance,
        metadata=metadata,
        source_pattern_context=pattern_context,
    )


def _officer_elements_with_hidden_chinh_quan(
    pattern_context: Any,
) -> tuple[list[str], list[dict[str, Any]]]:
    """Add canonical hidden Chính Quan once. Does not duplicate a visible token."""
    officer_elements = list(getattr(pattern_context, "officer_elements", []) or [])
    day_master = str(getattr(pattern_context, "day_master", "") or "")
    provenance = _chinh_quan_provenance(pattern_context, day_master)
    hidden_present = any(item.get("visibility") == "hidden" for item in provenance)
    if hidden_present and _CHINH_QUAN not in officer_elements:
        officer_elements.append(_CHINH_QUAN)
    return officer_elements, provenance


def _chinh_quan_provenance(
    pattern_context: Any,
    day_master: str,
) -> list[dict[str, Any]]:
    """Visible then hidden Chính Quan with G1-01 stem mapping. Dedup hidden slots."""
    if not day_master:
        return []
    entries = _visible_chinh_quan_entries(pattern_context, day_master)
    seen_hidden: set[tuple[str, str]] = set()
    for item in _hidden_chinh_quan_entries(pattern_context, day_master):
        key = (str(item.get("pillar") or ""), str(item.get("stem") or ""))
        if key in seen_hidden:
            continue
        seen_hidden.add(key)
        entries.append(item)
    return entries


def _visible_chinh_quan_entries(
    pattern_context: Any,
    day_master: str,
) -> list[dict[str, Any]]:
    """Record visible heavenly-stem Chính Quan. Skip Nhật Chủ."""
    entries: list[dict[str, Any]] = []
    bazi = getattr(pattern_context, "bazi", None)
    if bazi is not None:
        for pillar_name in _PILLARS:
            pillar = getattr(bazi, f"{pillar_name}_pillar", None)
            stem = str(getattr(pillar, "stem", "") or "")
            branch = str(getattr(pillar, "branch", "") or "")
            if not stem or stem == day_master:
                continue
            if ten_god_name(day_master, stem) != _CHINH_QUAN:
                continue
            entries.append(
                _provenance_entry(
                    visibility="visible",
                    pillar=pillar_name,
                    stem=stem,
                    branch=branch,
                    source="g1_01_visible_stem",
                )
            )
        return entries
    if _CHINH_QUAN in list(getattr(pattern_context, "ten_gods_list", []) or []):
        entries.append(
            _provenance_entry(
                visibility="visible",
                source="ten_gods_list",
            )
        )
    elif _CHINH_QUAN in list(getattr(pattern_context, "officer_elements", []) or []):
        entries.append(
            _provenance_entry(
                visibility="visible",
                source="officer_elements",
            )
        )
    return entries


def _hidden_chinh_quan_entries(
    pattern_context: Any,
    day_master: str,
) -> list[dict[str, Any]]:
    """Map Pattern hidden stems with G1-01 names. Same CSV as Ten Gods Core."""
    entries: list[dict[str, Any]] = []
    bazi = getattr(pattern_context, "bazi", None)
    for pillar_name in _PILLARS:
        stems = list(getattr(pattern_context, f"{pillar_name}_hidden_stems", []) or [])
        branch = _pillar_branch(pattern_context, bazi, pillar_name)
        for stem in stems:
            raw = str(stem or "")
            if not raw or raw == day_master:
                continue
            if ten_god_name(day_master, raw) != _CHINH_QUAN:
                continue
            entries.append(
                _provenance_entry(
                    visibility="hidden",
                    pillar=pillar_name,
                    stem=raw,
                    branch=branch,
                    source="g1_01_hidden_stem",
                )
            )
    return entries


def _pillar_branch(pattern_context: Any, bazi: Any, pillar_name: str) -> str:
    """Branch label for provenance; prefer live BaZi pillar."""
    if bazi is not None:
        pillar = getattr(bazi, f"{pillar_name}_pillar", None)
        branch = str(getattr(pillar, "branch", "") or "")
        if branch:
            return branch
    text = str(getattr(pattern_context, f"{pillar_name}_pillar", "") or "").strip()
    parts = text.split()
    return parts[-1] if parts else ""


def _provenance_entry(
    *,
    visibility: str,
    pillar: str = "",
    stem: str = "",
    branch: str = "",
    source: str,
) -> dict[str, Any]:
    """One Chính Quan occurrence for matcher evidence."""
    return {
        "ten_god": _CHINH_QUAN,
        "visibility": visibility,
        "pillar": pillar,
        "stem": stem,
        "branch": branch,
        "source": source,
    }


def _chinh_quan_visibility_class(provenance: list[dict[str, Any]]) -> str:
    """A visible / B hidden-only / C both / D none."""
    visibilities = {str(item.get("visibility") or "") for item in provenance}
    has_visible = "visible" in visibilities
    has_hidden = "hidden" in visibilities
    if has_visible and has_hidden:
        return "visible+hidden"
    if has_visible:
        return "visible"
    if has_hidden:
        return "hidden"
    return "none"
