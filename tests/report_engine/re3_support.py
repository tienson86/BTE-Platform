"""Shared RE-3 test helpers. Consumes RE-2 without mutating it."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from engines.report_engine.layout.layout_engine import ReportLayoutEngine
from engines.report_engine.layout.layout_result import CanonicalReportLayout
from tests.report_engine.re2_support import assemble_layout_inputs, frozen_clock


def assemble_canonical_layout() -> CanonicalReportLayout:
    """Run RE-2 once to obtain a successful CanonicalReportLayout."""
    payload = assemble_layout_inputs()
    return ReportLayoutEngine(clock=frozen_clock).run(
        report_context=payload["report_context"],
        interpretation_result=payload["interpretation_result"],
    )


def frozen_render_clock() -> datetime:
    """Return a fixed UTC clock for deterministic render traces."""
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def layout_without_assets() -> dict[str, Any]:
    """Copy a successful layout and drop assets for ASSET-MISSING tests."""
    snapshot = assemble_canonical_layout().to_dict()
    snapshot["assets"] = []
    return snapshot
