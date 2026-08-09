"""Published Canonical Interpretation Pipeline contract surface (IX-1)."""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.pipeline.interpretation_result import RESULT_FIELDS
from engines.interpretation_engine.pipeline.stage_registry import (
    ACTIVE_INTERPRETATION_STAGES,
    INACTIVE_FUTURE_STAGES,
    PIPELINE_ID,
    PIPELINE_VERSION,
)


def interpretation_pipeline_contract() -> dict[str, Any]:
    """Return the canonical published interpretation pipeline field contract."""
    return {
        "contract_id": "bte.interpretation.pipeline.v1",
        "pipeline_id": PIPELINE_ID,
        "interpretation_pipeline_version": PIPELINE_VERSION,
        "active_stages": list(ACTIVE_INTERPRETATION_STAGES),
        "future_stages": list(INACTIVE_FUTURE_STAGES),
        "outputs": list(RESULT_FIELDS),
        "reports": False,
        "ai_rewrite": False,
    }
