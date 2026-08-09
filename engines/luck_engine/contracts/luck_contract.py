"""Published Canonical Luck Pipeline contract surface (AX-4)."""

from __future__ import annotations

from typing import Any

from engines.luck_engine.pipeline.luck_result import RESULT_FIELDS
from engines.luck_engine.pipeline.stage_registry import (
    ACTIVE_LUCK_STAGES,
    INACTIVE_FUTURE_STAGES,
    PIPELINE_ID,
    PIPELINE_VERSION,
)


def luck_pipeline_contract() -> dict[str, Any]:
    """Return the canonical published luck pipeline field contract."""
    return {
        "contract_id": "bte.luck.pipeline.v1",
        "pipeline_id": PIPELINE_ID,
        "luck_pipeline_version": PIPELINE_VERSION,
        "active_stages": list(ACTIVE_LUCK_STAGES),
        "future_stages": list(INACTIVE_FUTURE_STAGES),
        "outputs": list(RESULT_FIELDS),
        "interpretation": False,
        "reports": False,
    }
