"""Stable version tokens for TV1-B03 Marriage Policy. Not scoring constants."""

from __future__ import annotations

from typing import Final

POLICY_ID: Final[str] = "marriage.policy.v1"
POLICY_VERSION: Final[str] = "1.0.0"
DECISION_MATHEMATICS_VERSION: Final[str] = "common.decision_mathematics.v1"
DECISION_ENGINE_VERSION: Final[str] = "common.decision_engine.v1"
EVIDENCE_MODEL_VERSION: Final[str] = "common.evidence_model.v1"
EVIDENCE_CATALOG_VERSION: Final[str] = "marriage.evidence.catalog.v1@1.0.0"
FINDING_MODEL_VERSION: Final[str] = "common.finding_model.v1"
SCORE_MODEL_VERSION: Final[str] = "unavailable"


def policy_version_token() -> str:
    """Return the bound Marriage Policy identity."""
    return f"{POLICY_ID}@{POLICY_VERSION}"
