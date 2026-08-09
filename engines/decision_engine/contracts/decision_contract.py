"""Public Decision Pipeline contracts (AX-3)."""

from __future__ import annotations

from typing import Any

from engines.decision_engine.pipeline.decision_result import (
    RESULT_FIELDS,
    CanonicalDecisionResult,
)
from engines.decision_engine.pipeline.stage_registry import (
    ACTIVE_DECISION_STAGES,
    CANONICAL_STAGE_ORDER,
    INACTIVE_FUTURE_STAGES,
    PIPELINE_ID,
    PIPELINE_VERSION,
)


def decision_result_contract() -> dict[str, Any]:
    """Return the published Canonical Decision Result field contract."""
    return {
        "pipeline_id": PIPELINE_ID,
        "decision_pipeline_version": PIPELINE_VERSION,
        "fields": list(RESULT_FIELDS),
        "active_stages": list(ACTIVE_DECISION_STAGES),
        "inactive_stages": list(INACTIVE_FUTURE_STAGES),
        "canonical_order": list(CANONICAL_STAGE_ORDER),
    }


__all__ = [
    "RESULT_FIELDS",
    "CanonicalDecisionResult",
    "decision_result_contract",
]
