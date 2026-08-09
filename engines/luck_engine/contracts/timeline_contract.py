"""Published Luck Timeline contract surface (LE-1)."""

from __future__ import annotations

from typing import Any

from engines.luck_engine.timeline_constants import (
    FOUNDATION_VERSION,
    PACKAGE_ID,
    PUBLISHED_INPUTS,
    PUBLISHED_OUTPUTS,
    TIMELINE_CONTRACT_ID,
    TIMELINE_VERSION,
)


def timeline_contract() -> dict[str, Any]:
    """Return the canonical published timeline field contract."""
    return {
        "contract_id": TIMELINE_CONTRACT_ID,
        "timeline_version": TIMELINE_VERSION,
        "foundation_version": FOUNDATION_VERSION,
        "package_id": PACKAGE_ID,
        "inputs": list(PUBLISHED_INPUTS),
        "outputs": list(PUBLISHED_OUTPUTS),
        "scores": False,
        "judgments": False,
        "interpretation": False,
    }
