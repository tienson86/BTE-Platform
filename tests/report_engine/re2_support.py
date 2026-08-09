"""Shared RE-2 test helpers. Reuses RE-1 snapshots without mutating them."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from engines.report_engine.context.canonical_report_context import build_report_context
from tests.report_engine.re1_snapshots import (
    ax2_snapshot,
    ax3_snapshot,
    ax4_snapshot,
    ix1_snapshot,
)


def frozen_clock() -> datetime:
    """Return a fixed UTC clock for deterministic traces."""
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def ix1_layout_snapshot() -> dict[str, Any]:
    """IX-1 snapshot with assembled interpretation sections for layout mapping."""
    snapshot = ix1_snapshot()
    sections = (
        {"section_id": "SEC-overview", "module_id": "overview", "status": "assembled"},
        {"section_id": "SEC-luck", "module_id": "luck", "status": "assembled"},
        {"section_id": "SEC-summary", "module_id": "summary", "status": "assembled"},
    )
    composition = {
        "assembly_version": "1.0.0",
        "success": True,
        "sections": list(sections),
    }
    snapshot["composition_result"] = composition
    snapshot["canonical_interpretation"] = composition
    return snapshot


def assemble_layout_inputs() -> dict[str, Any]:
    """Build sealed RE-1 context plus IX-1 interpretation result."""
    analysis = ax2_snapshot()
    decision = ax3_snapshot()
    luck = ax4_snapshot()
    interpretation = ix1_layout_snapshot()
    report_context = build_report_context(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
        interpretation_result=interpretation,
    )
    return {
        "analysis_result": analysis,
        "decision_result": decision,
        "luck_result": luck,
        "interpretation_result": interpretation,
        "report_context": report_context,
    }
