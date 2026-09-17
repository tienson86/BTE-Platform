"""Shared activation semantics for every Useful God rule group."""

from __future__ import annotations

from typing import Any


def is_rule_active(rule: dict[str, Any]) -> bool:
    """Return true only for rules explicitly available to the runtime."""
    status = str(rule.get("status", "active") or "active").strip().lower()
    enabled = str(rule.get("enabled", "true")).strip().lower()
    return status == "active" and enabled not in {"false", "0", "no"}
