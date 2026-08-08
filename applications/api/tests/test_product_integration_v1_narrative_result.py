"""Product Integration V1 — Pack 05 NarrativeResult on analyze payload."""

from __future__ import annotations

from applications.api.services.orchestrator import OrchestratorService


def test_analyze_publishes_pack05_narrative_result() -> None:
    payload = OrchestratorService().analyze(
        year=1987,
        month=1,
        day=21,
        hour=4,
        minute=30,
        gender="male",
    )
    assert "narrative_result" in payload
    narrative_result = payload["narrative_result"]
    assert narrative_result.get("contract") == "pack05_narrative_result_v1"
    assert "summary" in narrative_result
    assert isinstance(narrative_result.get("sections"), list)
    assert len(narrative_result["sections"]) == 7
    assert "recommendations" in narrative_result
    assert narrative_result.get("status") in {
        "complete",
        "partial_insufficient",
        "failed",
    }
    # Legacy delivery narrative remains for BC (ReportEngine markdown).
    assert "narrative" in payload
    assert "title" in payload["narrative"]
    assert "markdown" in payload["narrative"]
    # Legacy interpretation remains available but Portal prefers narrative_result.
    assert "interpretation" in payload
    assert payload.get("narrative_result_source", {}).get("contract") == (
        "pack05_narrative_result_v1"
    )
