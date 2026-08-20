"""Useful God context builder from PatternContext V2."""

from __future__ import annotations

from typing import Any

from engines.pattern_engine.follow_tokens import canonicalize_follow_token
from engines.useful_god_engine.context import UsefulGodContext


_SPECIAL_CODES = {"khuc_truc", "viem_thuong", "nhuan_ha", "gia_sac", "jia_wang"}


def build_useful_god_context(pattern_context: Any, pattern_result: Any = None) -> UsefulGodContext:
    """Convert PatternContext V2 into UsefulGodContext for rule matching."""
    main_pattern = None
    follow_pattern = None
    special_pattern = None

    if pattern_result is not None:
        main_pattern = str(getattr(pattern_result, "pattern", "") or "") or None
        follow_pattern = canonicalize_follow_token(
            getattr(pattern_result, "follow_type", None)
        )
        if main_pattern in _SPECIAL_CODES:
            special_pattern = main_pattern

    if main_pattern is None:
        main_pattern = str(getattr(pattern_context, "main_pattern", "") or "") or None
    if follow_pattern is None:
        follow_pattern = canonicalize_follow_token(
            getattr(pattern_context, "follow_pattern", None)
        )
    if special_pattern is None:
        special_pattern = str(getattr(pattern_context, "special_pattern", "") or "") or None

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
        officer_elements=list(getattr(pattern_context, "officer_elements", []) or []),
        output_elements=list(getattr(pattern_context, "output_elements", []) or []),
        companion_elements=list(getattr(pattern_context, "companion_elements", []) or []),
        ten_gods_list=list(getattr(pattern_context, "ten_gods_list", []) or []),
        follow_pattern=follow_pattern,
        special_pattern=special_pattern,
        main_pattern=main_pattern,
        metadata={"builder": "useful_god_context_builder_v2"},
        source_pattern_context=pattern_context,
    )
