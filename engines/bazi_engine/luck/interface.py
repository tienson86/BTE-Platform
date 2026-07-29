"""
Luck / Đại Vận — legacy design notes (Sprint 3).

Production Luck runtime lives in ``engines.luck_engine`` (Sprint 4).
This module keeps a thin compatibility stub for older imports.
"""

from __future__ import annotations

from typing import Any

from engines.luck_engine import LuckContext, LuckEngine

__all__ = ["LuckContext", "LuckEngine", "luck_context_stub"]


def luck_context_stub(*, reason: str = "missing_upstream_luck_producer") -> dict[str, Any]:
    """Empty dict shape for RuleContext ``luck`` section (Stage 5 stub)."""
    return {
        "available": False,
        "pillars": [],
        "status": None,
        "phase": None,
        "support": None,
        "attack": None,
        "reason": reason,
    }
