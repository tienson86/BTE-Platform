"""Compact Strength evidence from already-matched rules. Does not rescore."""

from __future__ import annotations

from typing import Any


def format_signed_points(score: float) -> str:
    """Format a raw rule contribution for compact evidence."""
    value = float(score)
    if value.is_integer():
        as_int = int(value)
        return f"+{as_int}" if as_int > 0 else str(as_int)
    if value > 0:
        return f"+{value}"
    return str(value)


def compact_evidence(matches: list[dict[str, Any]]) -> str:
    """Join matched rule reasons and raw scores. Does not change totals."""
    parts: list[str] = []
    for rule in matches:
        reason = str(rule.get("reason") or rule.get("description") or rule.get("rule_id") or "")
        reason = reason.strip()
        if not reason:
            continue
        score = float(rule.get("score") or 0.0)
        parts.append(f"{reason} {format_signed_points(score)}")
    return " · ".join(parts)
