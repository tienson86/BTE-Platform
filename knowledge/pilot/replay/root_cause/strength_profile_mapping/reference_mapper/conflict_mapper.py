"""Conflict mapping only when opposing signed buckets are explicitly observed."""

from __future__ import annotations

from typing import Any

from .ascii_utils import SCHEMA_VERSION
from .source_reader import RuntimeBundle


def map_conflicts(bundle: RuntimeBundle, evidence_ids: list[str]) -> list[dict[str, Any]]:
    """Create conflict records from observable opposing bucket signs."""
    buckets = bundle.profile_buckets
    conflicts: list[dict[str, Any]] = []

    season = buckets.get("season")
    root = buckets.get("root")
    support = buckets.get("support")
    control = buckets.get("control")
    drain = buckets.get("drain")

    def _ids_for(*prefixes: str) -> list[str]:
        found = [e for e in evidence_ids if any(p in e for p in prefixes)]
        return found or evidence_ids[:2] or ["EV-UNKNOWN"]

    if _opp(season, root):
        conflicts.append(
            _conflict(
                "CF-SEA-ROOT",
                "season_vs_root",
                ["seasonal_strength", "rooting"],
                _ids_for("SEA", "ROOT", "BUCKET-SEASON", "BUCKET-ROOT", "CTX-ROOT"),
            )
        )
    if _opp(support, control) or _opp(season, control):
        conflicts.append(
            _conflict(
                "CF-SUP-PRESS",
                "support_vs_pressure",
                ["same_element_support", "officer_pressure", "seasonal_strength"],
                _ids_for("SUP", "CTL", "BUCKET-SUPPORT", "BUCKET-CONTROL", "SEA"),
            )
        )
    if _opp(support, drain) or _opp(root, drain):
        conflicts.append(
            _conflict(
                "CF-RES-DRAIN",
                "resource_support_vs_drain",
                ["resource_support", "output_drain", "rooting"],
                _ids_for("SUP", "FLW", "BUCKET-DRAIN", "BUCKET-SUPPORT", "ROOT"),
            )
        )
    if _opp(root, control):
        conflicts.append(
            _conflict(
                "CF-ROOT-CTL",
                "root_vs_control",
                ["rooting", "officer_pressure"],
                _ids_for("ROOT", "CTL", "BUCKET-ROOT", "BUCKET-CONTROL"),
            )
        )
    return conflicts


def _opp(a: float | None, b: float | None) -> bool:
    if a is None or b is None:
        return False
    return (a > 0 and b < 0) or (a < 0 and b > 0)


def _conflict(
    conflict_id: str,
    conflict_type: str,
    dimensions: list[str],
    evidence_ids: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "conflict_id": conflict_id,
        "conflict_type": conflict_type,
        "dimensions": dimensions,
        "evidence_ids": evidence_ids,
        "severity": "unknown",
        "resolution_status": "unresolved",
        "confidence": "unknown",
        "notes": "observable opposing signed contributions; not resolved",
    }
