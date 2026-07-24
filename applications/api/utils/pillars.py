"""Pillar / birth helpers for orchestration (no engine business rules)."""

from __future__ import annotations

from typing import Any


def pillar_text(pillar: Any) -> str:
    """Format a Bazi pillar object as ``Stem Branch``."""
    stem = getattr(pillar, "stem", "")
    branch = getattr(pillar, "branch", "")
    return f"{stem} {branch}".strip()
