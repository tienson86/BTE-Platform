"""Balance stage for Useful God pipeline."""

from __future__ import annotations

from typing import Any


def run_balance_stage(context: Any) -> dict[str, Any]:
    """Produce balance summary from element distribution."""
    dist = dict(context.element_distribution or {})
    if not dist:
        return {"status": "unknown", "reason": "missing_element_distribution"}
    values = list(dist.values())
    spread = max(values) - min(values)
    if spread <= 1:
        status = "balanced"
    elif spread <= 3:
        status = "slightly_unbalanced"
    else:
        status = "unbalanced"
    dominant = max(dist, key=dist.get)
    weakest = min(dist, key=dist.get)
    return {
        "status": status,
        "dominant_element": dominant,
        "weakest_element": weakest,
        "spread": spread,
    }
