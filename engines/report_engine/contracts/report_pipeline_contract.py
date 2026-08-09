"""Published Canonical Report Pipeline contract surface (RX-1)."""

from __future__ import annotations

from typing import Any

from engines.report_engine.pipeline.report_result import RESULT_FIELDS
from engines.report_engine.pipeline.stage_registry import (
    ACTIVE_REPORT_STAGES,
    INACTIVE_FUTURE_STAGES,
    PIPELINE_ID,
    PIPELINE_VERSION,
)


def report_pipeline_contract() -> dict[str, Any]:
    """Return the canonical published report pipeline field contract."""
    return {
        "contract_id": "bte.report.pipeline.v1",
        "pipeline_id": PIPELINE_ID,
        "report_pipeline_version": PIPELINE_VERSION,
        "active_stages": list(ACTIVE_REPORT_STAGES),
        "future_stages": list(INACTIVE_FUTURE_STAGES),
        "outputs": list(RESULT_FIELDS),
        "publisher": False,
        "delivery": False,
        "print": False,
    }
