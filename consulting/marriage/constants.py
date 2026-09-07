"""TV-01 Marriage Consulting identity and pipeline contract.

Architecture constants only. No business rules.
"""

from __future__ import annotations

from typing import Final

MODULE_ID: Final[str] = "TV-01_MARRIAGE"
BUILD_PHASE: Final[str] = "TV1-B01"
MODULE_VERSION: Final[str] = "0.0.0-b01"

PIPELINE_STAGES: Final[tuple[str, ...]] = (
    "request_validation",
    "birth_input_normalization",
    "canonical_analysis_a",
    "canonical_analysis_b",
    "canonical_contract_validation",
    "snapshot_builder",
    "relationship_context_builder",
    "evidence_builder",
    "evidence_validation",
    "domain_decision",
    "cross_domain_resolver",
    "overall_decision",
    "score_engine",
    "confidence_engine",
    "recommendation_builder",
    "timing_analysis",
    "decision_validation",
    "narrative_composer",
    "presentation_adapter",
    "persistence",
)
