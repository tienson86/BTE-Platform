"""Runtime hook: bind CDR theme ids to Commercial Theme Library V1.0."""

from __future__ import annotations

from engines.report_engine.commercial.models import ThemeResolution, WritingVariant
from engines.report_engine.commercial.theme_catalog import (
    BLOCK_IDS,
    OPERATING_THEMES,
    OVERLAY_THEMES,
    canonical_theme_id,
    get_theme,
)

_CAPACITY_WEAK = frozenset({"weak", "very_weak", "CAPACITY_WEAK", "THEME_CAPACITY_WEAK"})


def select_writing_variant(
    *,
    purchase_package: str = "",
    writing_variant: str = "",
) -> WritingVariant:
    """Pick Layer-3 variant. Product Context may override."""
    raw = (writing_variant or "").strip().lower()
    for item in WritingVariant:
        if item.value == raw:
            return item
    package = (purchase_package or "").upper()
    if package in {"PACKAGE_C", "PACKAGE_D"}:
        return WritingVariant.PREMIUM
    if package == "PACKAGE_A":
        return WritingVariant.SHORT
    return WritingVariant.FORMAL


def resolve_theme(
    *,
    primary_theme: str,
    active_theme_ids: list[str] | None = None,
    capacity_level: str = "",
    has_conflicts: bool = False,
    purchase_package: str = "",
    writing_variant: str = "",
) -> ThemeResolution:
    """Select one operating theme + 0–2 overlays from published ids only."""
    published = [canonical_theme_id(item) for item in (active_theme_ids or []) if item]
    primary = canonical_theme_id(primary_theme)
    if primary and primary not in published:
        published.insert(0, primary)

    operating = ""
    if primary in OPERATING_THEMES:
        operating = primary
    else:
        operating = next((item for item in published if item in OPERATING_THEMES), "")

    overlays: list[str] = []
    for item in published:
        if item in OVERLAY_THEMES and item not in overlays:
            overlays.append(item)
    capacity = (capacity_level or "").strip().lower()
    if capacity in {"weak", "very_weak"} or any(
        token in _CAPACITY_WEAK for token in published
    ):
        if "CONSERVING" not in overlays:
            overlays.append("CONSERVING")
    if has_conflicts and "TENSION_HOLDER" not in overlays:
        overlays.append("TENSION_HOLDER")

    overlays = overlays[:2]
    record = get_theme(operating)
    return ThemeResolution(
        operating_theme_id=operating,
        customer_name=record.customer_name if record else "",
        overlays=overlays,
        variant=select_writing_variant(
            purchase_package=purchase_package,
            writing_variant=writing_variant,
        ),
        block_ids=list(BLOCK_IDS),
    )


def is_theme_library_wired() -> bool:
    """Runtime hook health — catalog present and selectable."""
    sample = resolve_theme(primary_theme="OPERATING_OUTPUT")
    return sample.operating_theme_id == "OPERATING_OUTPUT" and bool(sample.customer_name)
