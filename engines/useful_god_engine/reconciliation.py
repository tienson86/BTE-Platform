"""Cross-layer reconciliation after the Useful God winner is known."""

from __future__ import annotations

from typing import Any


def reconcile_temperature_recommendations(
    useful_god_result: Any,
    temperature_result: Any,
) -> None:
    """Prevent seasonal warming advice from contradicting a formed structure."""
    rule_id = str(getattr(useful_god_result, "winning_rule_id", "") or "")
    if not rule_id.startswith("str_full_"):
        return
    reason = str(getattr(useful_god_result, "climate_reason", "") or "").strip()
    temperature_result.recommendations = [reason] if reason else []
    temperature_result.balancing_need = "structural_reconciliation"
    temperature_result.balancing_need_label = "Điều hậu phục tùng cân bằng toàn cục"

