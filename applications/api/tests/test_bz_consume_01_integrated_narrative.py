"""BZ-CONSUME-01 — publish IntegratedNarrative onto Analysis Result."""

from __future__ import annotations

from applications.api.services.integrated_narrative_publish import (
    publish_integrated_narrative,
)
from applications.api.services.orchestrator import OrchestratorService


def test_publisher_returns_six_integrated_blocks() -> None:
    """Publisher consumes frozen composers and returns IntegratedNarrative dict."""
    payload = publish_integrated_narrative(
        {
            "strength": {"strength_level": "Thân vượng", "strength_score": 12.0},
            "useful_god": {"useful_god": "Hỏa", "hy_than": "Hỏa", "ky_than": "Thủy"},
            "pattern": {"cach_cuc": "Chính Quan"},
            "luck": {},
        }
    )
    assert payload["topic_id"] == "integrated"
    for slot in (
        "executive_summary",
        "observation",
        "reasoning",
        "impact",
        "recommendation",
        "summary",
    ):
        assert slot in payload
        assert "sentences" in payload[slot]


def test_analyze_publishes_integrated_narrative_without_replacing_pack05() -> None:
    """Live analyze attaches IntegratedNarrative next to Pack 05 NarrativeResult."""
    payload = OrchestratorService().analyze(
        year=1987,
        month=1,
        day=21,
        hour=4,
        minute=30,
        gender="male",
    )
    integrated = payload["integrated_narrative"]
    assert integrated["topic_id"] == "integrated"
    assert integrated.get("status") in {"complete", "partial", "insufficient"}
    for slot in (
        "executive_summary",
        "observation",
        "reasoning",
        "impact",
        "recommendation",
        "summary",
    ):
        block = integrated[slot]
        assert "sentences" in block
        assert "available" in block
    narrative_result = payload["narrative_result"]
    assert narrative_result.get("contract") == "pack05_narrative_result_v1"
    assert "sections" in narrative_result
    assert "identity" in payload
    assert "report" in payload
