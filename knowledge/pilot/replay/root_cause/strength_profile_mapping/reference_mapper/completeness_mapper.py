"""Evidence completeness mapping from field presence only."""

from __future__ import annotations

from typing import Any

from .ascii_utils import SCHEMA_VERSION
from .source_reader import RuntimeBundle


def map_completeness(bundle: RuntimeBundle) -> dict[str, Any]:
    """Classify completeness from whether source fields exist (no invention)."""
    ctx = bundle.context
    by_dim = {
        "calendar": _calendar(bundle),
        "season": _present(ctx.get("month_status") or ctx.get("season"), partial_ok=True),
        "roots": _present(ctx.get("root_level") or ctx.get("root_count") is not None, partial_ok=True),
        "support": _present(ctx.get("support_type") or bundle.profile_buckets.get("support") is not None),
        "pressure": _present(ctx.get("control_type") or bundle.profile_buckets.get("control") is not None),
        "drain": _present(ctx.get("drain_type") or bundle.profile_buckets.get("drain") is not None),
        "structure": _present(
            (bundle.profile_buckets.get("combination") not in (None, 0.0))
            or (bundle.profile_buckets.get("special") not in (None, 0.0))
            or any(str(r).startswith(("cmb_", "spc_")) for r in bundle.matched_rules)
        ),
        "temperature": _temperature(bundle),
        "expert_review": "partial" if bundle.expert_external else "unknown",
    }
    values = list(by_dim.values())
    if all(v == "unknown" for v in values):
        overall = "unknown"
    elif any(v == "unknown" for v in values) or any(v == "limited" for v in values):
        overall = "partial"
    elif all(v == "complete" for v in values):
        overall = "complete"
    else:
        overall = "partial"
    return {
        "schema_version": SCHEMA_VERSION,
        "overall": overall,
        "by_dimension": by_dim,
        "notes": "completeness reflects source field presence only",
    }


def _present(flag: Any, *, partial_ok: bool = False) -> str:
    if flag is None or flag is False:
        return "limited" if partial_ok else "unknown"
    return "partial"


def _calendar(bundle: RuntimeBundle) -> str:
    if bundle.calendar_status in {"VERIFIED", "VERIFIED_CORRECTED_PROJECTION"}:
        return "partial"
    if bundle.calendar_status in {"not_verified", None}:
        return "unknown" if bundle.population == "synthetic_stress" else "unknown"
    return "unknown"


def _temperature(bundle: RuntimeBundle) -> str:
    temp = bundle.temperature or {}
    if temp.get("from_strength_context") or temp.get("temperature_type"):
        if temp.get("from_temperature_engine"):
            return "partial"
        return "limited"
    return "unknown"
